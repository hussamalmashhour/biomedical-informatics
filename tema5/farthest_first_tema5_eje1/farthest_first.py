#!/usr/bin/env python3
"""Farthest-first clustering (Tema 5 - Ejercicio 1)."""

import os
import numpy as np


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


def get_dgenes(data, gene_names, threshold=2.3):
    abs_data = np.abs(data)
    mask = np.any(abs_data > threshold, axis=1)
    indices = np.where(mask)[0]
    dm = data[indices]
    dgenes = gene_names[indices]
    return dm, dgenes, indices


def compute_distances_to_centers(E, centers):
    distances = np.full(E.shape[0], np.inf)
    for center in centers:
        dists = np.linalg.norm(E - center, axis=1)
        distances = np.minimum(distances, dists)
    return distances


def farthestFirst(E, k, init):
    centers = [np.array(init)]
    for i in range(k - 1):
        distances = compute_distances_to_centers(E, centers)
        farthest_idx = np.argmax(distances)
        centers.append(E[farthest_idx].copy())
    return np.array(centers)


def main():
    expr_dir = os.path.join(os.path.dirname(__file__), '..', 'expresion_tema5_eje0')
    data_file = os.path.join(expr_dir, '2010diauxic-edited.txt')
    
    if not os.path.exists(data_file):
        return
    
    data, gene_names = load_expression_data(data_file)
    dm, dgenes, indices = get_dgenes(data, gene_names, threshold=2.3)
    
    k = 3
    init = np.array([-0.23, -0.09, -0.27, 0.2, 0.56, 1.52, 2.64])
    centroids = farthestFirst(dm, k, init)
    
    out_path = os.path.join(os.path.dirname(__file__), 'centroids.npy')
    np.save(out_path, centroids)


if __name__ == '__main__':
    main()
