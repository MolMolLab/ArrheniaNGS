# ArrheniaNGS

## Описание

Анализ микробиомов природных сообществ стал значительно более доступным благодаря развитию методов метабаркодинга. Однако эффективная обработка данных секвенирования eDNA требует адаптации параметров обработки под особенности конкретных данных и исследуемых организмов. В связи с этим был разработан и оптимизирован пайплайн для анализа грибных сообществ на основе ITS2-региона, секвенированного на платформе Illumina MiSeq.

Основные особенности пайплайна

* Гибкость: позволяет адаптировать параметры обработки данных в зависимости от качества сырых последовательностей и целей исследования.
* Автоматизированная обработка: включает ключевые этапы от предобработки данных до таксономической классификации, что минимизирует ручные операции.
* Использование современных алгоритмов: базируется на инструменте [QIIME 2](https://qiime2.org/) и реализован на Python 3 через интерфейс Artifact API, обеспечивая воспроизводимость и интеграцию с другими аналитическими платформами.
* Высокая точность идентификации: использует наивный байесовский классификатор и blast, что позволяет достигать высокого уровня достоверности определения таксонов.

Пайплайн включает следующие этапы: обрезку адаптеров, объединение парных чтений, фильтрацию, дерепликацию, кластеризацию, удаление химерных последовательностей и таксономическую классификацию.

Пайплайн был протестирован на данных секвенирования 210 образцов из природных субстратов (торф, растительный опад, древесина, микоризные корневые окончания). Полученные результаты подтверждают корректность работы пайплайна и его применимость для оценки биоразнообразия грибов. Подробнее результаты описаны в работе [(Filippova et al., 2024)](https://bdj.pensoft.net/article/119851/)

## Установка
### Зависимости
- Linux
- [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
------------

Для установки пайплайна выполните следующие команды:
```bash
git clone https://github.com/MolMolLab/Arrhenia.git
cd Arrhenia
conda env create -f environment.yml -n Arrhenia
```

## Использование

В `main.py` укажите расположение последовательностей, референсных последовательностей в формате FASTA (например, из базы данных [UNITE](https://unite.ut.ee/repository.php)), адаптеров и предварительно обученного классификатора. См. [classifier training tutorial](https://docs.qiime2.org/2024.10/tutorials/feature-classifier/) ([github](https://github.com/colinbrislawn/unite-train/releases) с обученными классификаторами UNITE).

После настройки запустите:
```bash
conda activate Arrhenia
python main.py
```

Результат будет включать таблицу, последовательности, классификацию blast и sklearn в формате артефактов qiime2 для дальнейшего таксономического анализа.

## Контакты

Mail: sibmyco@gmail.com

## Цитирование

Ишманов Т., Звягина Е., Рудыкина Е., Филиппов И., Бульонкова Т., Добрынина А., Филиппова Н. ArrheniaNGS. https://github.com/MolMolLab/ArrheniaNGS

---------------
## Getting started

This pipeline is based on the open-source code [QIIME 2](https://qiime2.org/) for amplicon-based metabarcoding. We tested the pipeline using ITS2 amplicons [(Filippova et al., 2024)](https://bdj.pensoft.net/article/119851/)

## Installation
### Dependencies
- Linux
- [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
------------

To install the pipeline, run the following commands:
```bash
git clone https://github.com/MolMolLab/Arrhenia.git
cd Arrhenia
conda env create -f environment.yml -n Arrhenia
```

## Usage

In `main.py`, specify the location of the sequences, reference sequences in FASTA format (for example, from the [UNITE](https://unite.ut.ee/repository.php) database), adapters, and a pre-trained classifier. Refer to the [classifier training tutorial](https://docs.qiime2.org/2024.10/tutorials/feature-classifier/)

After setting up, run:
```bash
conda activate Arrhenia
python main.py
```

The output will include a table, sequences and a taxonomic table for further taxonomic analysis.

## Communication

Mail: sibmyco@gmail.com

## Citation

Ishmanov T., Zvyagina E., Rudykina E., Filippov I., Bulyonkova T., Dobrynina A., Filippova N. ArrheniaNGS. https://github.com/MolMolLab/ArrheniaNGS
