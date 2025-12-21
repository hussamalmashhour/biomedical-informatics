#!/usr/bin/env python3
"""Lloyd's algorithm (k-means) (Tema 5 - Ejercicio 3).

Implements the Lloyd/k-means algorithm for clustering data points.
Iteratively assigns points to nearest centroid and updates centroids
until convergence or iteration limit.

Complexity: O(iterations * n * k) for n points and k clusters.
"""

import os
import numpy as np


def lloyd(points, k, convergence, iterations, initCenters=None):
    """Perform Lloyd's algorithm (k-means clustering).

    Args:
        points: (n, d) array of data points
        k: number of clusters
        convergence: threshold for average centroid movement
        iterations: maximum number of iterations
        initCenters: (k, d) array of initial centroids (optional)

    Returns:
        labels: (n,) array of cluster indices for each point
        centers: (k, d) array of final centroids
    """
    # Initialize centroids
    if initCenters is None:
        # Random initialization: choose k random distinct points
        indices = np.random.choice(points.shape[0], k, replace=False)
        centers = points[indices].copy().astype(float)
    else:
        centers = np.array(initCenters, dtype=float)
    
    print(f"Initial centers:\n{centers}\n")
    
    # Iterate
    for iteration in range(iterations):
        # Step 1: Assign each point to nearest centroid
        distances = np.zeros((points.shape[0], k))
        for i, center in enumerate(centers):
            distances[:, i] = np.linalg.norm(points - center, axis=1)
        
        labels = np.argmin(distances, axis=1)
        
        # Step 2: Recompute centroids as mean of assigned points
        new_centers = np.zeros_like(centers)
        for j in range(k):
            cluster_points = points[labels == j]
            if len(cluster_points) > 0:
                new_centers[j] = np.mean(cluster_points, axis=0)
            else:
                # Keep old center if no points assigned (empty cluster)
                new_centers[j] = centers[j]
        
        # Step 3: Compute average movement of centroids
        movements = np.linalg.norm(new_centers - centers, axis=1)
        avg_movement = np.mean(movements)
        
        print(f"Iteration {iteration+1}: avg_movement = {avg_movement:.6f}")
        
        centers = new_centers
        
        # Step 4: Check convergence
        if avg_movement <= convergence:
            print(f"Converged after {iteration+1} iterations\n")
            break
    
    # Final assignment
    distances = np.zeros((points.shape[0], k))
    for i, center in enumerate(centers):
        distances[:, i] = np.linalg.norm(points - center, axis=1)
    
    labels = np.argmin(distances, axis=1)
    
    return labels, centers


def main():
    # Test data
    points = np.array([
        [3, 20], [4, 22], [5, 23], [3, 18], [4, 21], [5, 24],
        [21, 10], [22, 12], [23, 13], [21, 8], [20, 11], [24, 13],
        [11, 2], [12, 1], [13, 3], [15, 4], [11, 3], [14, 2]
    ], dtype=float)
    
    k = 3
    convergence = 0.1
    iterations = 100
    
    # Example 1: Random initialization
    print("=" * 50)
    print("Example 1: Random initialization")
    print("=" * 50)
    np.random.seed(42)  # For reproducibility
    labels1, centers1 = lloyd(points, k, convergence, iterations)
    print(f"Final centers:\n{centers1}\n")
    print(f"Cluster assignments: {labels1}\n")
    
    # Example 2: Explicit initialization
    print("=" * 50)
    print("Example 2: Explicit initialization")
    print("=" * 50)
    initCenters = np.array([[3, 20], [24, 13], [14, 2]], dtype=float)
    labels2, centers2 = lloyd(points, k, convergence, iterations, initCenters=initCenters)
    print(f"Final centers:\n{centers2}\n")
    print(f"Cluster assignments: {labels2}\n")
    
    # Write results
    out_path = os.path.join(os.path.dirname(__file__), 'lloyd_clusters.txt')
    with open(out_path, 'w') as f:
        f.write("Lloyd's Algorithm (k-means) Results\n")
        f.write("=" * 50 + "\n\n")
        f.write("Example 1: Random initialization\n")
        f.write(f"Final centers:\n{centers1}\n")
        f.write(f"Cluster assignments: {labels1}\n\n")
        f.write("Example 2: Explicit initialization\n")
        f.write(f"Initial centers:\n{initCenters}\n")
        f.write(f"Final centers:\n{centers2}\n")
        f.write(f"Cluster assignments: {labels2}\n")
    
    print(f"Written results to {out_path}")


if __name__ == '__main__':
    main()
