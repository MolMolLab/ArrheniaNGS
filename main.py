from pipeline_processor import PipelineProcessor

if __name__ == "__main__":
    folder_path = "/..." # Рабочая директория
    sequences_folder_path = "/..." # Директория с сиквенсами
    resources_folder_path = "/..." # Директория с классификатором, референсной базой и списком адаптеров
    adapter_file='illumina adapters.json' # Список адаптеров
    classifier_file='...qza' # Классификатор
    reference_sequences_file="...fasta" # Референсная база
    threads = 8 # Количество потоков

    processor = PipelineProcessor(folder_path, sequences_folder_path, resources_folder_path, adapter_file, classifier_file, reference_sequences_file, threads)
    processor.process_paired_files()
