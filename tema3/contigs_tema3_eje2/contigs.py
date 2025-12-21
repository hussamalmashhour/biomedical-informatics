#!/usr/bin/env python3
"""Contigs from De Bruijn graph (Tema 3 - Ejercicio 2).

Build a De Bruijn graph from k-mers and extract maximal non-branching paths.
Deterministic output via sorted adjacency.
"""

import os
import re
from collections import defaultdict, Counter

# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def read_kmers(path):
    """Read kmers from a file that may contain quotes/commas/whitespace."""
    with open(path, "r") as f:
        text = f.read()
    return re.findall(r"[ACGT]+", text.upper())

# ---------------------------------------------------------------------------
# Graph helpers
# ---------------------------------------------------------------------------

def build_debruijn_graph(kmers):
    """Return adjacency dict: prefix -> list of suffixes (sorted)."""
    graph = defaultdict(list)
    for kmer in kmers:
        prefix = kmer[:-1]
        suffix = kmer[1:]
        graph[prefix].append(suffix)
    for node in graph:
        graph[node].sort()
    return graph


def compute_degrees(graph):
    indeg = Counter()
    outdeg = Counter()
    for u, vs in graph.items():
        outdeg[u] += len(vs)
        for v in vs:
            indeg[v] += 1
    nodes = set(indeg) | set(outdeg)
    for n in nodes:
        indeg.setdefault(n, 0)
        outdeg.setdefault(n, 0)
    return indeg, outdeg

# ---------------------------------------------------------------------------
# Contigs extraction
# ---------------------------------------------------------------------------

def _path_to_string(path):
    if not path:
        return ""
    pieces = [path[0]]
    for node in path[1:]:
        pieces.append(node[-1])
    return "".join(pieces)


def contigs(kmers):
    graph = build_debruijn_graph(kmers)
    indeg, outdeg = compute_degrees(graph)
    paths = []

    # helper to extend a path starting from edge (v -> w)
    def extend_path(v, w):
        path = [v, w]
        while indeg[w] == 1 and outdeg[w] == 1:
            nxt = graph[w][0]
            path.append(nxt)
            w = nxt
        return path

    # Non-branching paths starting at nodes that are not 1-in/1-out
    for v in sorted(graph):
        if outdeg[v] > 0 and not (indeg[v] == 1 and outdeg[v] == 1):
            for w in graph[v]:
                path = extend_path(v, w)
                paths.append(path)

    # Cycles among 1-in/1-out nodes not yet used
    visited = set()
    for path in paths:
        visited.update(path)

    for v in sorted(graph):
        if (indeg[v] == 1 and outdeg[v] == 1) and v not in visited:
            cycle = [v]
            w = graph[v][0]
            while True:
                cycle.append(w)
                visited.add(w)
                if w == v:
                    break
                w = graph[w][0]
            paths.append(cycle)

    contig_strings = [_path_to_string(p) for p in paths]
    return contig_strings

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    folder = os.path.dirname(__file__)
    kmers_path = os.path.join(folder, '10mers.txt')
    kmers = read_kmers(kmers_path)
    if not kmers:
        print("No kmers found.")
        return
    k = len(kmers[0])

    contig_list = contigs(kmers)
    lengths = sorted(len(c) for c in contig_list)

    print(f"Loaded {len(kmers)} k-mers (k={k})")
    print(f"Contigs found: {len(contig_list)}")
    print(f"Lengths (sorted): {lengths}")
    print("First bases of each contig:")
    for i, c in enumerate(contig_list):
        print(f"  {i+1}: len={len(c)} start={c[:20]}")

    out_path = os.path.join(folder, 'contigs.txt')
    with open(out_path, 'w') as f:
        for c in contig_list:
            f.write(c + "\n")
    print(f"Written contigs to {out_path}")


if __name__ == '__main__':
    main()
