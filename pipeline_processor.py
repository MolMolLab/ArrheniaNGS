import os
import re
import shutil
import tempfile
import logging
import json
import qiime2
from qiime2 import Artifact
from qiime2.plugins.cutadapt.methods import trim_paired
from qiime2.plugins.vsearch.methods import merge_pairs
from qiime2.plugins.quality_filter.methods import q_score
from qiime2.plugins.vsearch.methods import dereplicate_sequences
from qiime2.plugins.vsearch.methods import cluster_features_de_novo
from qiime2.plugins.vsearch.methods import cluster_features_closed_reference
from qiime2.plugins.vsearch.methods import uchime_ref
from qiime2.plugins.feature_table.methods import filter_features, filter_seqs
from qiime2.plugins.feature_classifier.methods import classify_sklearn

logging.basicConfig(level=logging.INFO)

class PipelineProcessor:
    def __init__(self, folder_path, sequences_folder_path, resources_folder_path, adapter_file, classifier_file, reference_sequences_file, threads=1):
        self.folder_path = folder_path
        self.sequences_folder_path = sequences_folder_path
        self.resources_folder_path = resources_folder_path
        self.adapter_list = self.load_adapters(os.path.join(resources_folder_path, adapter_file))
        self.classifier = Artifact.load(os.path.join(resources_folder_path, classifier_file))
        self.reference_sequences_file = self.create_reference_sequences_artifact(reference_sequences_file)
        self.threads = threads

    def load_adapters(self, json_file_path):
        with open(json_file_path, "r") as file:
            return json.load(file)

    def create_reference_sequences_artifact(self, reference_sequences_file):
        folder_path_reference_sequences = os.path.join(self.resources_folder_path, reference_sequences_file)
        return Artifact.import_data(type='FeatureData[Sequence]', view=folder_path_reference_sequences)

    def find_paired_files(self):
        pattern = re.compile(r"(\d+)_S(\d+)_L001_R([12])_001\.fastq\.gz")
        paired_files = {}

        for file_name in os.listdir(self.sequences_folder_path):
            match = pattern.match(file_name)
            if match:
                key = (match.group(1), match.group(2))
                read_type = f"R{match.group(3)}"

                if key not in paired_files:
                    paired_files[key] = {}
                paired_files[key][read_type] = os.path.join(self.sequences_folder_path, file_name)

        return {k: v for k, v in paired_files.items() if "R1" in v and "R2" in v}

    def process_paired_files(self):
        paired_files = self.find_paired_files()

        for (sample_id, j), files in paired_files.items():
            with tempfile.TemporaryDirectory() as temp_dir:
                logging.info(f"Processing paired files: {files['R1']} and {files['R2']}")

                shutil.copy2(files["R1"], temp_dir)
                shutil.copy2(files["R2"], temp_dir)

                paired_end_artifact = Artifact.import_data(
                    type='SampleData[PairedEndSequencesWithQuality]',
                    view=temp_dir,
                    view_type='CasavaOneEightSingleLanePerSampleDirFmt'
                )

                self.trim_adapters(paired_end_artifact, sample_id)

    def trim_adapters(self, paired_end_artifact, sample_id):
        logging.info(f"Trimming adapters for {sample_id}")
        trim_paired_end_artifact, = trim_paired(
            demultiplexed_sequences=paired_end_artifact,
            adapter_f=self.adapter_list["forward_adapters"],
            adapter_r=self.adapter_list["reverse_adapters"]
        )
        self.merge_trimmed_pairs(trim_paired_end_artifact, sample_id)

    def merge_trimmed_pairs(self, trim_paired_end_artifact, sample_id):
        logging.info(f"Merging pairs for {sample_id}")
        merge_sequences_artifact, _ = merge_pairs(demultiplexed_seqs=trim_paired_end_artifact, minlen=150, maxns=5, maxee=2, threads=self.threads)
        self.filter_by_quality_score(merge_sequences_artifact, sample_id)

    def filter_by_quality_score(self, merge_sequences_artifact, sample_id):
        logging.info(f"Filtering sequences for {sample_id}")
        score_sequences_artifact, _ = q_score(demux=merge_sequences_artifact, min_quality=20, max_ambiguous=2)
        self.dereplicate(score_sequences_artifact, sample_id)

    def dereplicate(self, score_sequences_artifact, sample_id):
        logging.info(f"Dereplicating sequences for {sample_id}")
        d_table_artifact, d_sequences_artifact = dereplicate_sequences(sequences=score_sequences_artifact)
        self.cluster_de_novo(d_table_artifact, d_sequences_artifact, sample_id)

    def cluster_de_novo(self, d_table_artifact, d_sequences_artifact, sample_id):
        logging.info(f"Clustering features de novo for {sample_id}")
        clustered_de_novo_table_artifact, clustered_de_novo_sequences_artifact = cluster_features_de_novo(
            sequences=d_sequences_artifact, table=d_table_artifact, perc_identity=0.99, threads=self.threads
        )
        self.cluster_close(clustered_de_novo_table_artifact, clustered_de_novo_sequences_artifact, sample_id)

    def cluster_close(self, clustered_de_novo_table_artifact, clustered_de_novo_sequences_artifact, sample_id):
        logging.info(f"Performing closed-reference clustering for {sample_id}")
        clustered_close_table_artifact, clustered_close_sequences_artifact, _ = cluster_features_closed_reference(
            sequences=clustered_de_novo_sequences_artifact,
            table=clustered_de_novo_table_artifact,
            reference_sequences=self.reference_sequences_file,
            perc_identity=0.99,
            threads=self.threads
        )
        self.remove_chimeras(clustered_close_table_artifact, clustered_close_sequences_artifact, sample_id)

    def remove_chimeras(self, clustered_close_table_artifact, clustered_close_sequences_artifact, sample_id):
        logging.info(f"Removing chimeras for {sample_id}")
        chimeras, nonchimeras_sequences_artifact, stats = uchime_ref(
            sequences=clustered_close_sequences_artifact, table=clustered_close_table_artifact,
            reference_sequences=self.reference_sequences_file, threads=self.threads
        )

        filtered_table_artifact, = filter_features(table=clustered_close_table_artifact, metadata=nonchimeras_sequences_artifact.view(qiime2.Metadata))
        filtered_sequences_artifact, = filter_seqs(data=clustered_close_sequences_artifact, metadata=nonchimeras_sequences_artifact.view(qiime2.Metadata))

        filtered_table_artifact.save(os.path.join(self.folder_path, f"{sample_id}_Table.qza"))
        filtered_sequences_artifact.save(os.path.join(self.folder_path, f"{sample_id}_Sequences.qza"))

        self.classify_sequences(filtered_sequences_artifact, sample_id)

    def classify_sequences(self, filtered_sequences_artifact, sample_id):
        logging.info(f"Classifying sequences for {sample_id}")
        classification_artifact, = classify_sklearn(reads=filtered_sequences_artifact, classifier=self.classifier, n_jobs=1)
        classification_artifact.save(os.path.join(self.folder_path, f"{sample_id}_Classification.qza"))
