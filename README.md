# Procrustes

Procrustes is a Python package containing tools for transformation of exome-capture-based RNA-Seq 
gene expression into polyA-like processed RNA-Seq gene expression. 

## System Requirements

- **Operating System:** Ubuntu 22.04.1 or compatible Linux distributions
- **Python Version:** 3.8 or higher
- **Hardware:** No specific requirements, but a standard computer with enough RAM 
- for in-memory operations is necessary.

## Installation

To install Procrustes, follow these steps. Note that installation may take up to 20 minutes 
on a standard desktop computer.

```bash
git clone https://github.com/BostonGene/Procrustes
cd Procrustes
pip install -e .
```

## Running the Demo
To run the demo, open the "Demo_run.ipynb" Jupyter notebook and execute all cells. 
The demo outputs bar plots with CCC (Concordance Correlation Coefficient) values divided into intervals. 
Completing the demo may take up to 30 minutes on a standard desktop computer.

## Using Procrustes with Your Own Data
To analyze your own RNA-Seq expression data with Procrustes, ensure the following:

Your data is calculated utilizing kallisto based on gencode version 23 (Homo Sapiens) 
and TPM normalized.
Transform TPM-expression values using np.log2(exp+1) before analysis.
RNA-Seq libraries should be prepared using either the Agilent V4, V7, 
or V7_UTR library preparation kit.
Input the data in the function Procrustes_predict in the format rows x cols. 
The output will be similar to the demo run, 
allowing you to compare your results with polyA data of interest.