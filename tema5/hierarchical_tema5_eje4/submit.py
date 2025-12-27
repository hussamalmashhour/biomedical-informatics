#!/usr/bin/env python3
"""
Submission script for Exercise 4 - Hierarchical Clustering (UPGMA)
Generates the submission URL with the computed clusters on dm matrix.
"""

import numpy as np
import os
import sys

# Add parent directory to path to import config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
import config

# Import the hierarchicalClustering function
from hierarchical import hierarchicalClustering


def load_dm_matrix():
    """Load the dm matrix from Exercise 0."""
    # Try multiple possible paths
    paths = [
        os.path.join(os.path.dirname(__file__), '..', 'expresion_tema5_eje0', '2010diauxic-edited.txt'),
        os.path.join(os.path.dirname(__file__), '..', '..', 'tema5', 'expresion_tema5_eje0', '2010diauxic-edited.txt'),
    ]
    
    for data_file in paths:
        if os.path.exists(data_file):
            print(f"Loading data from: {data_file}")
            
            # Load expression data
            data = np.genfromtxt(
                data_file,
                delimiter='\t',
                skip_header=1,
                usecols=range(1, 8),
                filling_values=0
            )
            
            # Load gene names
            gene_names = np.genfromtxt(
                data_file,
                delimiter='\t',
                skip_header=1,
                usecols=0,
                dtype=str
            )
            
            # Select dgenes with |log2 fc| > 2.3
            abs_data = np.abs(data)
            mask = np.any(abs_data > 2.3, axis=1)
            
            dm = data[mask]
            dgenes = gene_names[mask]
            
            print(f"OK Loaded dm matrix: {dm.shape}")
            print(f"OK dgenes: {len(dgenes)}")
            
            return dm, dgenes
    
    print("❌ Could not find expression data file")
    return None, None


def run_test_case():
    """Run the test case from the exercise."""
    print("=" * 70)
    print("EXERCISE 4 - HIERARCHICAL CLUSTERING (UPGMA)")
    print("=" * 70)
    
    # Load dm matrix from Exercise 0
    print("\n[STEP 1] Loading dm matrix from Exercise 0...")
    dm, dgenes = load_dm_matrix()
    
    if dm is None:
        print("❌ Error: Could not load dm matrix")
        return None
    
    # Test parameters
    k = 6
    
    print(f"\n[STEP 2] Running hierarchical clustering...")
    print(f"  Input shape: {dm.shape}")
    print(f"  k (target clusters): {k}")
    print(f"  Algorithm: UPGMA (average linkage)")
    
    # Run hierarchical clustering
    clusters, tree = hierarchicalClustering(dm, k)
    
    print(f"\n[STEP 3] Results")
    print("-" * 70)
    
    print(f"\nFinal Clusters (k={k}):")
    for cluster_id in sorted(clusters.keys()):
        leaves = clusters[cluster_id]
        print(f"  Cluster {cluster_id}: {len(leaves)} genes (indices: {leaves[:5]}{'...' if len(leaves) > 5 else ''})")
    
    # Show gene names for each cluster
    print(f"\nCluster Composition (by gene names):")
    for cluster_id in sorted(clusters.keys()):
        leaves = clusters[cluster_id]
        genes_in_cluster = [dgenes[i] for i in leaves]
        print(f"\n  Cluster {cluster_id} ({len(leaves)} genes):")
        print(f"    First 5 genes: {genes_in_cluster[:5]}")
        if len(genes_in_cluster) > 5:
            print(f"    Last 5 genes: {genes_in_cluster[-5:]}")
    
    # Validate
    all_leaves = set()
    for leaves in clusters.values():
        all_leaves.update(leaves)
    
    expected_leaves = set(range(dm.shape[0]))
    if all_leaves == expected_leaves:
        print(f"\nOK All {len(expected_leaves)} genes covered in {k} clusters")
    else:
        print(f"\nERROR Coverage error")
    
    return clusters


def format_clusters_for_submission(clusters):
    """
    Format clusters dictionary for API submission.
    
    The API expects a dict like: {12:[1,2,3], 14:[4,5,6], ...}
    Keys and values should be plain Python ints/lists.
    """
    formatted = {}
    for cluster_id, leaves in clusters.items():
        # Convert to plain Python types
        formatted[int(cluster_id)] = [int(leaf) for leaf in leaves]
    
    return formatted


def build_submission_url(clusters):
    """Build the submission URL for the hierarchical clustering exercise."""
    # Get exercise info from config
    session, exercise, description = config.get_exercise_info("hierarchical_tema5_eje4")
    
    # Format clusters
    response = format_clusters_for_submission(clusters)
    
    # Build URL using config helper
    url = config.build_test_url(session, exercise, response)
    
    return url


def main():
    print("=" * 70)
    print("HIERARCHICAL CLUSTERING - SUBMISSION GENERATOR")
    print("=" * 70)
    
    # Run test case
    clusters = run_test_case()
    
    if clusters is None:
        return
    
    # Build submission URL
    url = build_submission_url(clusters)
    
    print("\n" + "=" * 70)
    print("SUBMISSION FORMAT")
    print("=" * 70)
    
    formatted_clusters = format_clusters_for_submission(clusters)
    print(f"\nClusters dictionary:")
    for cluster_id in sorted(formatted_clusters.keys()):
        leaves = formatted_clusters[cluster_id]
        if len(leaves) == 1:
            print(f"  {cluster_id}: [{leaves[0]}] ({len(leaves)} gene)")
        elif len(leaves) <= 3:
            print(f"  {cluster_id}: {leaves} ({len(leaves)} genes)")
        else:
            print(f"  {cluster_id}: [{leaves[0]}, {leaves[1]}, ..., {leaves[-1]}] ({len(leaves)} genes)")
    
    print("\n" + "=" * 70)
    print("SUBMISSION URL")
    print("=" * 70)
    print(f"\n{url}")
    
    print("\n" + "=" * 70)
    print("EXPLANATION")
    print("=" * 70)
    print("""
Hierarchical Clustering (UPGMA):

1. Start with n singleton clusters (one per gene)
2. Compute pairwise Euclidean distances
3. Repeatedly merge two closest clusters:
   - Create new internal node
   - Update distances using UPGMA average linkage:
     d(new, other) = (|C1|*d(C1,other) + |C2|*d(C2,other)) / (|C1| + |C2|)
4. Stop when k clusters remain
5. Return dict mapping cluster IDs -> leaf indices

Tree Structure:
  - Leaves (0 to n-1): Original data points
  - Internal nodes (n onwards): Merged clusters
  - Final k clusters are the k internal nodes that remain

Output Format:
  - Dictionary: {cluster_node_id: [list of leaf indices]}
  - Keys: Internal node IDs from the tree
  - Values: Lists of original gene indices in that cluster

Applied to dm matrix:
  - 229 differentially expressed genes
  - 7-dimensional expression profiles
  - Clustered into 6 groups
    """)
    
    # Save to file
    output_file = os.path.join(os.path.dirname(__file__), 'submission_url.txt')
    with open(output_file, 'w') as f:
        f.write("Exercise 4 - Hierarchical Clustering (UPGMA)\n")
        f.write("=" * 70 + "\n\n")
        f.write("Submission URL:\n")
        f.write(url + "\n\n")
        f.write(f"Clusters (k=6):\n")
        for cluster_id in sorted(formatted_clusters.keys()):
            leaves = formatted_clusters[cluster_id]
            f.write(f"  Cluster {cluster_id}: {len(leaves)} genes\n")
    
    print(f"\nOK URL also saved to: {output_file}")


if __name__ == "__main__":
    main()
