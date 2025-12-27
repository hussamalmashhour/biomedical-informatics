#!/usr/bin/env python3
"""String Reconstruction via De Bruijn graph and Eulerian path (Tema 3 - Exercise 1).

Steps
-----
1) Build De Bruijn graph from k-mers (nodes are (k-1)-mers, edges are k-mers).
2) Find an Eulerian path using Hierholzer's algorithm.
3) Reconstruct the original string from the path.

Also includes a simple k-mer composition helper for quick tests.
"""

import os
import re
from collections import defaultdict, Counter

# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def read_kmers(path):
    """Read kmers from a file that may contain quotes/commas/whitespace.

    Returns a list of uppercase kmers.
    """
    with open(path, "r") as f:
        text = f.read()
    return re.findall(r"[ACGT]+", text.upper())


def composition(text, k):
    """Return the list of all k-mers of text (order preserved)."""
    return [text[i:i + k] for i in range(len(text) - k + 1)]

# ---------------------------------------------------------------------------
# De Bruijn graph
# ---------------------------------------------------------------------------

def build_debruijn_graph(kmers):
    """Build De Bruijn graph from kmers. Returns adjacency dict node -> list of dests (sorted)."""
    graph = defaultdict(list)
    for kmer in kmers:
        prefix = kmer[:-1]
        suffix = kmer[1:]
        graph[prefix].append(suffix)
    # sort adjacency for deterministic traversal
    for node in graph:
        graph[node].sort()
    return graph


def _compute_degrees(graph):
    indeg = Counter()
    outdeg = Counter()
    for u, vs in graph.items():
        outdeg[u] += len(vs)
        for v in vs:
            indeg[v] += 1
    # ensure all nodes appear in both counters
    nodes = set(indeg) | set(outdeg)
    for n in nodes:
        indeg.setdefault(n, 0)
        outdeg.setdefault(n, 0)
    return indeg, outdeg


def balanced(graph):
    """Check if directed graph is balanced (Eulerian).
    
    A graph is balanced if indegree = outdegree for all nodes.
    
    Args:
        graph: Adjacency dict {node: [neighbors]}
    
    Returns:
        True if balanced, False otherwise.
    """
    indeg, outdeg = _compute_degrees(graph)
    for node in set(indeg) | set(outdeg):
        if indeg[node] != outdeg[node]:
            return False
    return True


def eulerianCycle(graph):
    """Find Eulerian cycle in a balanced directed graph.
    
    Uses Hierholzer's algorithm. Assumes graph has Eulerian cycle.
    
    Args:
        graph: Adjacency dict {node: [neighbors]}
    
    Returns:
        List of nodes forming Eulerian cycle.
    """
    if not graph:
        return []
    
    # Check if balanced
    if not balanced(graph):
        raise ValueError("Graph must be balanced for Eulerian cycle")
    
    # Use find_eulerian_path which handles both cycles and paths
    path = find_eulerian_path(graph)
    return path

# ---------------------------------------------------------------------------
# Eulerian path (Hierholzer)
# ---------------------------------------------------------------------------

def find_eulerian_path(graph):
    """Find an Eulerian path in the given directed graph.

    Assumes a path exists. Uses deterministic traversal: edges consumed in
    lexicographic order by storing adjacency reversed and popping from end.
    """
    indeg, outdeg = _compute_degrees(graph)

    start = None
    for node in sorted(set(indeg) | set(outdeg)):
        if outdeg[node] - indeg[node] == 1:
            start = node
            break
    if start is None:
        # fall back to any node with outgoing edge
        for node in sorted(graph):
            if outdeg[node] > 0:
                start = node
                break
    if start is None:
        return []

    # Copy adjacency with reversed order so we can pop() to get lexicographic order
    adj = {u: list(reversed(vs)) for u, vs in graph.items()}

    path = []
    stack = [start]
    while stack:
        v = stack[-1]
        if adj.get(v):
            nxt = adj[v].pop()
            stack.append(nxt)
        else:
            path.append(stack.pop())
    path.reverse()
    return path

# ---------------------------------------------------------------------------
# Reconstruction
# ---------------------------------------------------------------------------

def reconstruct_from_path(path):
    """Reconstruct string from Eulerian path of (k-1)-mer nodes."""
    if not path:
        return ""
    result = [path[0]]
    for node in path[1:]:
        result.append(node[-1])
    return "".join(result)


def stringReconstruction(kmers):
    graph = build_debruijn_graph(kmers)
    path = find_eulerian_path(graph)
    return reconstruct_from_path(path)

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    folder = os.path.dirname(__file__)
    # Prefer local copy of 10mers.txt placed alongside this script
    kmers_path = os.path.join(folder, '10mers.txt')
    kmers = read_kmers(kmers_path)
    if not kmers:
        print("No kmers found.")
        return
    k = len(kmers[0])
    seq = stringReconstruction(kmers)

    print(f"Loaded {len(kmers)} k-mers of length {k}")
    print(f"Reconstructed sequence length: {len(seq)}")
    print(f"Starts with: {seq[:20]}")
    print(f"Ends with:   {seq[-20:]}")
    print(f"First 100 bp: {seq[:100]}")

    out_path = os.path.join(folder, 'reconstructed_sequence.txt')
    with open(out_path, 'w') as f:
        f.write(seq)
    print(f"Written to {out_path}")


if __name__ == '__main__':
    main()
