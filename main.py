from pipeline_processor import PipelineProcessor

if __name__ == "__main__":
    folder_path = "/..."                # Рабочая директория                                                  | Working directory
    sequences_folder_path = "/..."      # Директория с сиквенсами                                             | Sequence directory
    resources_folder_path = "/..."      # Директория с классификатором, референсной базой и списком адаптеров | Directory with classifier, reference base and list of adapters
    adapter_file='...json'              # Список адаптеров в формате json                                     | List of adapters in json format
    classifier_file='...qza'            # Артефакт классификатора                                             | Classifier artifact
    reference_sequences_file="...fasta" # Референсная база в формате FASTA                                    | Reference base in FASTA format
    threads = 8                         # Количество потоков                                                  | Number of threads

    processor = PipelineProcessor(folder_path, sequences_folder_path, resources_folder_path, adapter_file, classifier_file, reference_sequences_file, threads)
    processor.process_paired_files()
