#!/usr/bin/env python3
"""Hierarchical Clustering - UPGMA (Tema 5 - Ejercicio 4).

Implements agglomerative hierarchical clustering using UPGMA
(Unweighted Pair Group Method with Arithmetic Mean).

The algorithm:
1. Start with n singleton clusters (one per point).
2. Compute pairwise Euclidean distances between all points.
3. Repeat until k clusters remain:
   - Find two closest clusters.
   - Merge them with a new node ID (n, n+1, ...).
   - Update distances using UPGMA average linkage.
   - Remove merged clusters, add new cluster.
4. Return dict mapping cluster IDs to lists of leaf indices.

Tree representation:
- Leaves: keys 0..n-1 → empty lists.
- Internal nodes: keys n, n+1, ... → [left_child, right_child].

Complexity: O(n³) naive, O(n²) with optimized data structures.
"""

import os
import numpy as np


def hierarchicalClustering(E, k):
    """Build hierarchical clustering tree using UPGMA.
    
    Args:
        E: (n, d) array of data points.
        k: number of clusters to produce.
    
    Returns:
        clusters: dict {cluster_id: [leaf_indices]} for k final clusters.
        tree: dict {node_id: children_list} representing full tree.
    """
    n = E.shape[0]
    
    # Initialize: each point is its own cluster
    active_clusters = set(range(n))  # Current cluster IDs
    cluster_members = {i: {i} for i in range(n)}  # Leaves: {node_id: set of leaf indices}
    tree = {i: [] for i in range(n)}  # Tree structure: leaf → empty, internal → [left, right]
    
    # Use dictionary for distance matrix (allows dynamic sizing)
    dist = {}
    for i in range(n):
        for j in range(n):
            if i != j:
                d = np.linalg.norm(E[i] - E[j])
                dist[(i, j)] = d
    
    next_node_id = n
    
    # Merge until k clusters remain
    while len(active_clusters) > k:
        # Find two closest active clusters
        min_dist = float('inf')
        merge_i, merge_j = None, None
        
        active_list = sorted(active_clusters)
        for idx in range(len(active_list)):
            for jdx in range(idx + 1, len(active_list)):
                i, j = active_list[idx], active_list[jdx]
                key = (min(i, j), max(i, j))
                if key in dist and dist[key] < min_dist:
                    min_dist = dist[key]
                    merge_i, merge_j = i, j
        
        # Create new cluster
        size_i = len(cluster_members[merge_i])
        size_j = len(cluster_members[merge_j])
        size_new = size_i + size_j
        
        # Update tree
        tree[next_node_id] = [merge_i, merge_j]
        cluster_members[next_node_id] = cluster_members[merge_i] | cluster_members[merge_j]
        
        # Update distances using UPGMA (average linkage)
        # d(new, other) = (size_i * d(i, other) + size_j * d(j, other)) / (size_i + size_j)
        for other in active_clusters:
            if other != merge_i and other != merge_j:
                key_i = (min(merge_i, other), max(merge_i, other))
                key_j = (min(merge_j, other), max(merge_j, other))
                new_dist = (size_i * dist[key_i] + size_j * dist[key_j]) / size_new
                key_new = (min(next_node_id, other), max(next_node_id, other))
                dist[key_new] = new_dist
        
        # Remove merged clusters, add new cluster
        active_clusters.discard(merge_i)
        active_clusters.discard(merge_j)
        active_clusters.add(next_node_id)
        
        next_node_id += 1
    
    # Build final clusters dictionary
    clusters = {}
    for cluster_id in active_clusters:
        clusters[cluster_id] = sorted(list(cluster_members[cluster_id]))
    
    return clusters, tree


def print_tree(tree, indent=0, node_id=None):
    """Pretty-print tree structure (optional)."""
    if node_id is None:
        # Find root (highest node ID)
        node_id = max(tree.keys())
    
    if tree[node_id] == []:
        # Leaf
        print("  " * indent + f"Leaf {node_id}")
    else:
        # Internal node
        left, right = tree[node_id]
        print("  " * indent + f"Node {node_id}")
        print_tree(tree, indent + 1, left)
        print_tree(tree, indent + 1, right)


def main():
    # Test data from specification
    E = np.array([
        [10., 8., 10.],
        [10., 0., 9.],
        [4., 8.5, 3.],
        [9.5, 0.5, 8.5],
        [4.5, 8.5, 2.5],
        [10.5, 9., 12.],
        [5., 8.5, 11.],
        [3.7, 8.7, 2.],
        [9.7, 2., 9.],
        [9.7, 2., 9.]
    ])
    
    k = 3
    clusters, tree = hierarchicalClustering(E, k)
    
    # Expected: {12:[7,2,4], 14:[8,9,1,3], 16:[6,0,5]} (or similar structure)
    # Note: Internal node IDs may vary based on merge order, but cluster
    # membership should be consistent (within ~1 point variation due to ties)
    
    print("=" * 60)
    print("Hierarchical Clustering - UPGMA")
    print("=" * 60)
    print(f"\nInput: {E.shape[0]} points, {E.shape[1]} dimensions")
    print(f"Target: {k} clusters\n")
    
    print("Point coordinates:")
    for i, point in enumerate(E):
        print(f"  Point {i}: {point}")
    
    print("\nFinal Clusters:")
    for cluster_id in sorted(clusters.keys()):
        print(f"  Cluster {cluster_id}: {clusters[cluster_id]}")
    
    print("\nTree structure (from root):")
    root = max(tree.keys())
    print_tree(tree, node_id=root)
    
    # Validate cluster coverage
    all_leaves = set()
    for cluster_id, leaves in clusters.items():
        all_leaves.update(leaves)
    
    expected_leaves = set(range(E.shape[0]))
    if all_leaves == expected_leaves:
        print(f"\n✓ All {len(expected_leaves)} leaves covered in {k} clusters")
    else:
        print(f"\n✗ Coverage error: missing {expected_leaves - all_leaves}")
    
    # Write results
    out_path = os.path.join(os.path.dirname(__file__), 'hierarchical_clusters.txt')
    with open(out_path, 'w') as f:
        f.write("Hierarchical Clustering (UPGMA) Results\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Input: {E.shape[0]} points, {E.shape[1]} dimensions\n")
        f.write(f"Target clusters: {k}\n\n")
        f.write("Point coordinates:\n")
        for i, point in enumerate(E):
            f.write(f"  Point {i}: {point}\n")
        f.write("\nALGORITHM EXPLANATION:\n")
        f.write("- Start with 10 singleton clusters (one per point)\n")
        f.write("- Compute pairwise Euclidean distances\n")
        f.write("- Merge two closest clusters iteratively (7 merges)\n")
        f.write("- Use UPGMA: d(new, other) = (size_i * d(i, other) + size_j * d(j, other)) / (size_i + size_j)\n")
        f.write("- Stop when 3 clusters remain\n\n")
        f.write("Final Clusters:\n")
        for cluster_id in sorted(clusters.keys()):
            leaves = clusters[cluster_id]
            f.write(f"  Cluster {cluster_id}: {leaves} ({len(leaves)} members)\n")
        f.write(f"\nTotal leaves: {len(all_leaves)}\n")
        f.write(f"Cluster coverage: {'VALID' if all_leaves == expected_leaves else 'INVALID'}\n")
    
    print(f"\nResults written to {out_path}")


if __name__ == '__main__':
    main()
