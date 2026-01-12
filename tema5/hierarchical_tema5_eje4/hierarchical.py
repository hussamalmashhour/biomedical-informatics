#!/usr/bin/env python3
"""Hierarchical Clustering - UPGMA (Tema 5 - Ejercicio 4)."""

import numpy as np


def hierarchicalClustering(E, k):
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
    
    while len(active_clusters) > k:
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
        
        size_i = len(cluster_members[merge_i])
        size_j = len(cluster_members[merge_j])
        size_new = size_i + size_j
        
        tree[next_node_id] = [merge_i, merge_j]
        cluster_members[next_node_id] = cluster_members[merge_i] | cluster_members[merge_j]
        
        for other in active_clusters:
            if other != merge_i and other != merge_j:
                key_i = (min(merge_i, other), max(merge_i, other))
                key_j = (min(merge_j, other), max(merge_j, other))
                new_dist = (size_i * dist[key_i] + size_j * dist[key_j]) / size_new
                key_new = (min(next_node_id, other), max(next_node_id, other))
                dist[key_new] = new_dist
        
        active_clusters.discard(merge_i)
        active_clusters.discard(merge_j)
        active_clusters.add(next_node_id)
        
        next_node_id += 1
    
    clusters = {}
    for cluster_id in active_clusters:
        clusters[cluster_id] = sorted(list(cluster_members[cluster_id]))
    
    return clusters, tree


def main():
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
        [10.2, 1., 9.2]
    ])
    
    k = 3
    hierarchicalClustering(E, k)


if __name__ == '__main__':
    main()
