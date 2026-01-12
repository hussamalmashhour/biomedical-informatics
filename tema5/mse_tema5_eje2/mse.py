#!/usr/bin/env python3
"""Mean Squared Error (MSE) for clustering (Tema 5 - Ejercicio 2)."""

import numpy as np


def mse(points, centers):
    if points.shape[1] != centers.shape[1]:
        raise ValueError("points and centers must have same number of dimensions")
    
    min_sq_distances = np.full(points.shape[0], np.inf)
    
    for center in centers:
        sq_distances = np.sum((points - center) ** 2, axis=1)
        min_sq_distances = np.minimum(min_sq_distances, sq_distances)
    
    return np.mean(min_sq_distances)


def main():
    points1 = np.array([
        [ 1, 24], [ 4,  2], [23, 20], [24, 22], [25, 23], [23, 18],
        [24, 21], [25, 24], [31, 10], [32, 12], [33, 13], [31,  8],
        [30, 11], [34, 13], [21,  2], [22,  1], [23,  3], [25,  4],
        [21,  3], [24,  2]
    ], dtype=float)
    centers1 = np.array([[1, 24], [31, 8], [4, 2]], dtype=float)
    mse(points1, centers1)
    
    points2 = np.array([
        [3, 20], [4, 22], [5, 23], [3, 18], [4, 21], [5, 24],
        [21, 10], [22, 12], [23, 13], [21, 8], [20, 11], [24, 13],
        [11, 2], [12, 1], [13, 3], [15, 4], [11, 3], [14, 2]
    ], dtype=float)
    centers2 = np.array([[3, 20], [24, 13], [14, 2]], dtype=float)
    mse(points2, centers2)


if __name__ == '__main__':
    main()
