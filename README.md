# IlluminaMetaPipeline

## Введение

Этот пайплайн основан на открытом исходном коде [QIIME 2](https://qiime2.org/) для метабаркодинга на основе ампликонов. Мы протестировали конвейер с использованием ампликонов ITS2 [(Filippova et al., 2024)](https://bdj.pensoft.net/article/119851/)

## Getting started

This pipeline is based on the open-source code [QIIME 2](https://qiime2.org/) for amplicon-based metabarcoding. We tested the pipeline using ITS2 amplicons [(Filippova et al., 2024)](https://bdj.pensoft.net/article/119851/)

## Установка/Installation
### Зависимости/Dependencies
- Linux
- [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
------------

Для установки пайплайна выполните следующие команды:

To install the pipeline, run the following commands:
```bash
git clone https://github.com/MolMolLab/IlluminaMetaPipeline.git
cd IlluminaMetaPipeline
conda env create -f environment.yml
```

## Использование

В `main.py` укажите расположение последовательностей, референсных последовательностей в формате FASTA (например, из базы данных [UNITE](https://unite.ut.ee/repository.php)), адаптеров и предварительно обученного классификатора. См. [classifier training tutorial](https://docs.qiime2.org/2024.10/tutorials/feature-classifier/)

## Usage

In `main.py`, specify the location of the sequences, reference sequences in FASTA format (for example, from the [UNITE](https://unite.ut.ee/repository.php) database), adapters, and a pre-trained classifier. Refer to the [classifier training tutorial](https://docs.qiime2.org/2024.10/tutorials/feature-classifier/)

После настройки запустите:

After setting up, run:

```bash
conda activate illumina_meta_pipeline
python main.py
```

Результат будет включать таблицу, последовательности и таксономическую таблицу для дальнейшего таксономического анализа.

The output will include a table, sequences and a taxonomic table for further taxonomic analysis.

## Communication

Mail ...

## Citation
Если вы используете наш пайплайн в научной публикации, мы будем признательны за ссылки: ...

If you use our pipeline in a scientific publication, we would appreciate citations: ...

