#!/usr/bin/env python3
"""Farthest-first clustering (Tema 5 - Ejercicio 1).

Implements the farthest-first heuristic for selecting k cluster centers from
a data matrix. Greedy approach: start with an initial center, then repeatedly
select the point farthest from all currently selected centers.

Complexity: O(k * n * m) for k centers, n points, m dimensions.
"""

import os
import numpy as np


def compute_distances_to_centers(E, centers):
    """Compute minimum distance from each point in E to the nearest center.

    Args:
        E: (n, m) array of points
        centers: list of center vectors (each of shape (m,))

    Returns:
        (n,) array where distances[i] = min distance from E[i] to any center
    """
    distances = np.full(E.shape[0], np.inf)
    for center in centers:
        dists = np.linalg.norm(E - center, axis=1)
        distances = np.minimum(distances, dists)
    return distances


def farthestFirst(E, k, init):
    """Select k cluster centers using farthest-first heuristic.

    Args:
        E: (n, m) array of data points
        k: number of centers to select
        init: initial center (1D array of length m)

    Returns:
        (k, m) array of selected centers
    """
    centers = [np.array(init)]
    
    for _ in range(k - 1):
        # Compute minimum distance from each point to any current center
        distances = compute_distances_to_centers(E, centers)
        
        # Select the point with maximum minimum distance
        farthest_idx = np.argmax(distances)
        centers.append(E[farthest_idx].copy())
    
    return np.array(centers)


def main():
    # Example from statement
    E = np.array([
        [3, 20], [4, 22], [5, 23], [3, 18], [4, 21], [5, 24],
        [21, 10], [22, 12], [23, 13], [21, 8], [20, 11], [24, 13],
        [11, 2], [12, 1], [13, 3], [15, 4], [11, 3], [14, 2]
    ], dtype=float)
    
    k = 3
    init = np.array([3, 20])
    
    centers = farthestFirst(E, k, init)
    
    print("Synthetic test:")
    print(f"k = {k}, init = {init}")
    print("Selected centers:")
    for i, c in enumerate(centers):
        print(f"  {i}: {c}")
    print(f"Expected: [[3, 20], [24, 13], [11, 2]]")
    
    # Write results
    out_path = os.path.join(os.path.dirname(__file__), 'farthest_first_centers.txt')
    with open(out_path, 'w') as f:
        f.write("Farthest-First Clustering Results\n")
        f.write("=" * 40 + "\n\n")
        f.write(f"k = {k}\n")
        f.write(f"Initial center: {init}\n\n")
        f.write("Selected centers:\n")
        for i, c in enumerate(centers):
            f.write(f"  {i}: {c}\n")
    
    print(f"\nWritten results to {out_path}")


if __name__ == '__main__':
    main()
