# IlluminaMetaPipeline

## Getting started

This pipeline is based on the open-source code [QIIME 2](https://qiime2.org/) for amplicon-based metabarcoding. We tested the pipeline using ITS2 amplicons [(Filippova, Nina et al., 2024)](https://bdj.pensoft.net/article/119851/)

## Installation

Ensure that Linux, [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) and QIIME 2 are installed.
```
git clone https://github.com/MolMolLab/IlluminaMetaPipeline.git
cd IlluminaMetaPipeline
```

## Usage

In `main.py`, specify the location of the sequences, reference sequences in fasta format (for example, from the [UNITE](https://unite.ut.ee/repository.php) database), adapters, and a pre-trained classifier. Refer to the [classifier training tutorial](https://docs.qiime2.org/2024.10/tutorials/feature-classifier/)

After setting up, run:

```
python main.py
```

The output will include a table, sequences and a taxonomic table for further taxonomic analysis.
