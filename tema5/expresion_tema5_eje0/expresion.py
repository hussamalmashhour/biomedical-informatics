"""Ejercicio 0 - Análisis de Expresión Génica"""

import numpy as np
import urllib.request
import os


def download_data(url, filename):
    if not os.path.exists(filename):
        urllib.request.urlretrieve(url, filename)


def load_expression_data(filename):
    data = np.genfromtxt(
        filename,
        delimiter='\t',
        skip_header=1,
        usecols=range(1, 8),
        filling_values=0
    )
    
    gene_names = np.genfromtxt(
        filename,
        delimiter='\t',
        skip_header=1,
        usecols=0,
        dtype=str
    )
    
    return data, gene_names


def select_differentially_expressed_genes(data, gene_names, threshold=2.3):
    abs_data = np.abs(data)
    mask = np.any(abs_data > threshold, axis=1)
    indices = np.where(mask)[0]
    dm = data[indices]
    dgenes = gene_names[indices]
    return dm, dgenes, indices


def main():
    url = "http://vis.usal.es/rodrigo/documentos/bioinfo/expresion/2010diauxic-edited.txt"
    filename = "2010diauxic-edited.txt"
    
    download_data(url, filename)
    data, gene_names = load_expression_data(filename)
    dm, dgenes, indices = select_differentially_expressed_genes(data, gene_names, threshold=2.3)


if __name__ == "__main__":
    main()
