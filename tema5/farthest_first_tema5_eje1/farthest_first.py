#!/usr/bin/env python3
"""Farthest-first clustering (Tema 5 - Ejercicio 1).

Complete workflow:
1. Load DeRisi expression data from Exercise 0
2. Get dm matrix (dgenes with |log2 fc| > 2.3)
3. Apply farthestFirst clustering to find k expression patterns

Implements the farthest-first heuristic for selecting k cluster centers from
a data matrix. Greedy approach: start with an initial center, then repeatedly
select the point farthest from all currently selected centers.

Complexity: O(k * n * m) for k centers, n points, m dimensions.
"""

import os
import sys
import numpy as np
from typing import Tuple, List


# ------------------------------------------------------------
# PART 1: GET THE DM MATRIX FROM EXERCISE 0
# ------------------------------------------------------------
def load_expression_data(filename):
    """
    Load the DeRisi expression matrix from file.
    
    Args:
        filename: Path to expression data file
        
    Returns:
        tuple: (data, gene_names) where data is expression matrix and gene_names are IDs
    """
    print(f"Loading data from {filename}...")
    
    # Load expression data (skip header, columns 1-7)
    data = np.genfromtxt(
        filename,
        delimiter='\t',
        skip_header=1,
        usecols=range(1, 8),
        filling_values=0
    )
    
    # Load gene names (column 0)
    gene_names = np.genfromtxt(
        filename,
        delimiter='\t',
        skip_header=1,
        usecols=0,
        dtype=str
    )
    
    print(f"✓ Loaded matrix: {data.shape[0]} genes × {data.shape[1]} timepoints")
    return data, gene_names


def get_dgenes(data, gene_names, threshold=2.3):
    """
    Select genes with |log2 fc| > threshold for any timepoint.
    
    Args:
        data: Full expression matrix
        gene_names: Array of gene names
        threshold: Absolute log2 fold change threshold
        
    Returns:
        tuple: (dm, dgenes, indices) where:
               - dm is expression matrix for selected genes
               - dgenes are the names of selected genes
               - indices are the original indices
    """
    print(f"\nSelecting genes with |log2 fc| > {threshold} for any timepoint...")
    
    # Find genes where ANY timepoint has |expression| > threshold
    abs_data = np.abs(data)
    mask = np.any(abs_data > threshold, axis=1)
    
    # Get indices
    indices = np.where(mask)[0]
    
    # Extract dm matrix and dgenes
    dm = data[indices]
    dgenes = gene_names[indices]
    
    print(f"✓ Selected {len(dgenes)} differentially expressed genes (dgenes)")
    print(f"  Matrix dm shape: {dm.shape}")
    
    return dm, dgenes, indices


# ------------------------------------------------------------
# PART 2: FARTHEST FIRST ALGORITHM
# ------------------------------------------------------------
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
    
    for i in range(k - 1):
        # Compute minimum distance from each point to any current center
        distances = compute_distances_to_centers(E, centers)
        
        # Select the point with maximum minimum distance
        farthest_idx = np.argmax(distances)
        max_distance = distances[farthest_idx]
        
        centers.append(E[farthest_idx].copy())
        
        print(f"  Centroid {i+2}: index {farthest_idx}, max min-distance = {max_distance:.4f}")
    
    return np.array(centers)




# ------------------------------------------------------------
# PART 3: ANALYSIS AND VISUALIZATION
# ------------------------------------------------------------
def analyze_centroids(centroids, dm, dgenes):
    """Analyze and interpret the clustering results."""
    print("\n" + "=" * 70)
    print("CLUSTER ANALYSIS")
    print("=" * 70)
    
    timepoints = ['0 hr', '9.5 hr', '11.5 hr', '13.5 hr', '15.5 hr', '18.5 hr', '20.5 hr']
    
    for i, centroid in enumerate(centroids):
        print(f"\n--- Centroid {i + 1} ---")
        print(f"Expression pattern:")
        for t, val in zip(timepoints, centroid):
            print(f"  {t:8s}: {val:7.3f}")
        
        # Find closest gene to centroid
        distances = np.linalg.norm(dm - centroid, axis=1)
        closest_idx = np.argmin(distances)
        closest_gene = dgenes[closest_idx]
        closest_distance = distances[closest_idx]
        
        print(f"\nClosest gene: {closest_gene} (distance: {closest_distance:.4f})")
        
        # Pattern analysis
        early_mean = np.mean(centroid[:3])   # 0-11.5 hr
        late_mean = np.mean(centroid[4:])    # 15.5-20.5 hr
        change = late_mean - early_mean
        
        if change > 1:
            trend = "UP-REGULATED (late phase)"
        elif change < -1:
            trend = "DOWN-REGULATED (late phase)"
        else:
            trend = "STABLE across timepoints"
        
        print(f"Trend: {trend} (change: {change:.2f} log2 fc)")


def save_results(centroids, dm, dgenes, filename='farthest_first_results.txt'):
    """Save clustering results to file."""
    out_path = os.path.join(os.path.dirname(__file__), filename)
    
    with open(out_path, 'w') as f:
        f.write("Farthest-First Clustering Results\n")
        f.write("DeRisi Expression Data (dgenes with |log2 fc| > 2.3)\n")
        f.write("=" * 70 + "\n\n")
        
        f.write(f"Input matrix (dm): {dm.shape[0]} genes × {dm.shape[1]} timepoints\n")
        f.write(f"Number of clusters (k): {len(centroids)}\n\n")
        
        f.write("Centroids:\n")
        f.write("-" * 70 + "\n")
        timepoints = ['0 hr', '9.5 hr', '11.5 hr', '13.5 hr', '15.5 hr', '18.5 hr', '20.5 hr']
        
        for i, centroid in enumerate(centroids):
            f.write(f"\nCentroid {i + 1}:\n")
            for t, val in zip(timepoints, centroid):
                f.write(f"  {t:8s}: {val:7.3f}\n")
    
    print(f"\n✓ Results saved to {out_path}")
    
    # Also save centroids as numpy array
    np_path = os.path.join(os.path.dirname(__file__), 'centroids.npy')
    np.save(np_path, centroids)
    print(f"✓ Centroids array saved to {np_path}")


# ------------------------------------------------------------
# TESTING
# ------------------------------------------------------------
def test_2d_example():
    """Test farthestFirst with the 2D example from the exercise."""
    print("=" * 70)
    print("TEST: 2D Example")
    print("=" * 70)
    
    E = np.array([
        [3, 20], [4, 22], [5, 23], [3, 18], [4, 21], [5, 24],
        [21, 10], [22, 12], [23, 13], [21, 8], [20, 11], [24, 13],
        [11, 2], [12, 1], [13, 3], [15, 4], [11, 3], [14, 2]
    ], dtype=float)
    
    k = 3
    init = np.array([3, 20])
    expected = np.array([[3, 20], [24, 13], [11, 2]])
    
    print(f"E shape: {E.shape}")
    print(f"k: {k}")
    print(f"init: {init}")
    
    result = farthestFirst(E, k, init)
    
    print(f"\nExpected centroids:\n{expected}")
    print(f"\nComputed centroids:\n{result}")
    
    match = np.allclose(result, expected, atol=1e-6)
    print(f"\n✓ Test {'PASSED' if match else 'FAILED'}")
    print("=" * 70 + "\n")
    
    return match


# ------------------------------------------------------------
# MAIN EXECUTION
# ------------------------------------------------------------
def main():
    """Execute complete workflow: get dm matrix and apply farthestFirst."""
    print("=" * 70)
    print("EJERCICIO 1: Farthest First Clustering")
    print("DeRisi Expression Data")
    print("=" * 70)
    
    # -----------------------------------------------------------------
    # STEP 1: Load expression data from Exercise 0
    # -----------------------------------------------------------------
    print("\n[STEP 1] Loading DeRisi expression data from Exercise 0...")
    
    # Path to expression data file (from exercise 0)
    expr_dir = os.path.join(os.path.dirname(__file__), '..', 'expresion_tema5_eje0')
    data_file = os.path.join(expr_dir, '2010diauxic-edited.txt')
    
    if not os.path.exists(data_file):
        print(f"❌ Error: Expression data not found at {data_file}")
        print("Please run Exercise 0 first to download the data.")
        
        # Run 2D test anyway
        print("\nRunning 2D test instead...")
        test_2d_example()
        return
    
    # Load data
    data, gene_names = load_expression_data(data_file)
    
    # -----------------------------------------------------------------
    # STEP 2: Get dm matrix (dgenes)
    # -----------------------------------------------------------------
    print("\n[STEP 2] Selecting differentially expressed genes (dgenes)...")
    dm, dgenes, indices = get_dgenes(data, gene_names, threshold=2.3)
    
    print(f"\nFirst 5 dgenes:")
    for i in range(min(5, len(dgenes))):
        print(f"  {dgenes[i]}: {dm[i]}")
    
    # -----------------------------------------------------------------
    # STEP 3: Test with 2D example first
    # -----------------------------------------------------------------
    print("\n[STEP 3] Testing algorithm with 2D example...")
    if not test_2d_example():
        print("❌ Algorithm test failed. Please check implementation.")
        return
    
    # -----------------------------------------------------------------
    # STEP 4: Apply farthestFirst to dm matrix
    # -----------------------------------------------------------------
    print("\n[STEP 4] Applying farthestFirst to dm matrix...")
    
    # Parameters from exercise
    k = 3
    init = np.array([-0.23, -0.09, -0.27, 0.2, 0.56, 1.52, 2.64])
    
    print(f"\nClustering parameters:")
    print(f"  k (clusters): {k}")
    print(f"  init point: {init}")
    print(f"  dm shape: {dm.shape}")
    
    print(f"\nRunning farthestFirst clustering...")
    centroids = farthestFirst(dm, k, init)
    
    print(f"\n✓ Found {len(centroids)} centroids")
    
    # -----------------------------------------------------------------
    # STEP 5: Analyze and save results
    # -----------------------------------------------------------------
    print("\n[STEP 5] Analyzing results...")
    analyze_centroids(centroids, dm, dgenes)
    
    # Save results
    save_results(centroids, dm, dgenes)
    
    # -----------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"✓ Loaded expression data: {data.shape[0]} genes × {data.shape[1]} timepoints")
    print(f"✓ Selected dgenes: {len(dgenes)} genes (|log2 fc| > 2.3)")
    print(f"✓ Applied farthestFirst clustering with k={k}")
    print(f"✓ Found {len(centroids)} expression pattern centroids")
    print("=" * 70)


if __name__ == '__main__':
    main()
