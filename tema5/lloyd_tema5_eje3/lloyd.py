#!/usr/bin/env python3
"""Lloyd's algorithm (k-means) (Tema 5 - Ejercicio 3)."""

import numpy as np


def lloyd(points, k, convergence, iterations, initCenters=None):
    if initCenters is None:
        indices = np.random.choice(points.shape[0], k, replace=False)
        centers = points[indices].copy().astype(float)
    else:
        centers = np.array(initCenters, dtype=float)
    
    for iteration in range(iterations):
        distances = np.zeros((points.shape[0], k))
        for i, center in enumerate(centers):
            distances[:, i] = np.linalg.norm(points - center, axis=1)
        
        labels = np.argmin(distances, axis=1)
        
        new_centers = np.zeros_like(centers)
        for j in range(k):
            cluster_points = points[labels == j]
            if len(cluster_points) > 0:
                new_centers[j] = np.mean(cluster_points, axis=0)
            else:
                new_centers[j] = centers[j]
        
        movements = np.linalg.norm(new_centers - centers, axis=1)
        avg_movement = np.mean(movements)
        centers = new_centers
        
        if avg_movement <= convergence:
            break
    
    distances = np.zeros((points.shape[0], k))
    for i, center in enumerate(centers):
        distances[:, i] = np.linalg.norm(points - center, axis=1)
    
    labels = np.argmin(distances, axis=1)
    
    return labels, centers


def main():
    points = np.array([
        [3, 20], [4, 22], [5, 23], [3, 18], [4, 21], [5, 24],
        [21, 10], [22, 12], [23, 13], [21, 8], [20, 11], [24, 13],
        [11, 2], [12, 1], [13, 3], [15, 4], [11, 3], [14, 2]
    ], dtype=float)
    
    k = 3
    convergence = 0.1
    iterations = 100
    
    np.random.seed(42)
    lloyd(points, k, convergence, iterations)
    
    initCenters = np.array([[3, 20], [24, 13], [14, 2]], dtype=float)
    lloyd(points, k, convergence, iterations, initCenters=initCenters)


if __name__ == '__main__':
    main()
