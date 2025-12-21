#!/usr/bin/env python3
"""Mean Squared Error (MSE) for clustering (Tema 5 - Ejercicio 2).

Computes the MSE between a set of points and cluster centers, where each
point is assigned to its nearest center. Lower MSE indicates better clustering.

Complexity: O(n * k) for n points and k centers.
"""

import os
import numpy as np


def mse(points, centers):
    """Compute mean squared error of clustering.

    Args:
        points: (n, d) array of data points
        centers: (k, d) array of cluster centers

    Returns:
        float: mean squared error

    Raises:
        ValueError if dimensions don't match
    """
    if points.shape[1] != centers.shape[1]:
        raise ValueError("points and centers must have same number of dimensions")
    
    # For each point, compute minimum squared distance to any center
    min_sq_distances = np.full(points.shape[0], np.inf)
    
    for center in centers:
        # Vectorized distance computation for all points to this center
        sq_distances = np.sum((points - center) ** 2, axis=1)
        min_sq_distances = np.minimum(min_sq_distances, sq_distances)
    
    # Return average squared distance
    return np.mean(min_sq_distances)


def main():
    # Example 1
    print("=" * 50)
    print("Example 1")
    print("=" * 50)
    
    points1 = np.array([
        [ 1, 24], [ 4,  2], [23, 20], [24, 22], [25, 23], [23, 18],
        [24, 21], [25, 24], [31, 10], [32, 12], [33, 13], [31,  8],
        [30, 11], [34, 13], [21,  2], [22,  1], [23,  3], [25,  4],
        [21,  3], [24,  2]
    ], dtype=float)
    
    centers1 = np.array([[1, 24], [31, 8], [4, 2]], dtype=float)
    
    mse1 = mse(points1, centers1)
    print(f"Points shape: {points1.shape}")
    print(f"Centers shape: {centers1.shape}")
    print(f"MSE: {mse1:.2f}")
    print(f"Expected: 104.95\n")
    
    # Example 2
    print("=" * 50)
    print("Example 2")
    print("=" * 50)
    
    points2 = np.array([
        [3, 20], [4, 22], [5, 23], [3, 18], [4, 21], [5, 24],
        [21, 10], [22, 12], [23, 13], [21, 8], [20, 11], [24, 13],
        [11, 2], [12, 1], [13, 3], [15, 4], [11, 3], [14, 2]
    ], dtype=float)
    
    centers2 = np.array([[3, 20], [24, 13], [14, 2]], dtype=float)
    
    mse2 = mse(points2, centers2)
    print(f"Points shape: {points2.shape}")
    print(f"Centers shape: {centers2.shape}")
    print(f"MSE: {mse2:.2f}\n")
    
    # Write results
    out_path = os.path.join(os.path.dirname(__file__), 'mse_results.txt')
    with open(out_path, 'w') as f:
        f.write("Mean Squared Error (MSE) Results\n")
        f.write("=" * 50 + "\n\n")
        f.write("Example 1:\n")
        f.write(f"  Points shape: {points1.shape}\n")
        f.write(f"  Centers shape: {centers1.shape}\n")
        f.write(f"  MSE: {mse1:.2f}\n")
        f.write(f"  Expected: 104.95\n\n")
        f.write("Example 2:\n")
        f.write(f"  Points shape: {points2.shape}\n")
        f.write(f"  Centers shape: {centers2.shape}\n")
        f.write(f"  MSE: {mse2:.2f}\n")
    
    print(f"Written results to {out_path}")


if __name__ == '__main__':
    main()
