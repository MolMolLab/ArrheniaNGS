# IlluminaMetaPipeline

## Getting started

This pipeline is based on the open-source code [QIIME](https://qiime2.org/) 2 for amplicon-based metabarcoding. We tested the pipeline using ITS2 amplicons. [(Filippova, Nina et al., 2024)](https://bdj.pensoft.net/article/119851/)

## Installation

Linux, [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) and QIIME2 must be installed.
```
git clone
cd IlluminaMetaPipeline
```

## Usage

In `main.py` specify the location of the sequences, reference sequences in `fasta` format, for example from the [UNITE](https://unite.ut.ee/repository.php) database, adapters and a pre-trained classifier. [Сlassifier training tutorial](https://docs.qiime2.org/2024.10/tutorials/feature-classifier/)

After

```
python main.py
```

At the output we get a table, sequences and a taxonomic table for further taxonomic analysis
