#!/usr/bin/env python3
"""Motif scoring (Tema 2 - Exercise 6).

The score(Dna) function measures how far a set of motifs is from a perfect
consensus. For each column, it counts A/C/G/T, takes the maximum frequency,
and adds (t - max_frequency) to the total score, where t is the number of
strings.

This script reads motifs from text files (one motif per line), ignoring empty
lines and whitespace, and prints scores for two datasets:
1) nfkbMotifs.txt (expected score: 30)
2) dataset_40_9.txt
"""

import os
import sys
from collections import Counter


def clean_line(line):
    """Return an uppercase DNA string with spaces removed."""
    return ''.join(line.strip().split()).upper()


def read_motifs(path):
    """Read motifs (one per line) from a text file, cleaning whitespace.

    Empty lines are ignored. All motifs must have the same length.
    """
    motifs = []
    with open(path, 'r') as f:
        for raw in f:
            cleaned = clean_line(raw)
            if not cleaned:
                continue
            motifs.append(cleaned)

    if not motifs:
        raise ValueError(f"No motifs found in {path}")

    length = len(motifs[0])
    for m in motifs:
        if len(m) != length:
            raise ValueError(
                f"All motifs must have equal length (expected {length}, got {len(m)})"
            )
    return motifs


def score(Dna):
    """Compute motif score for a list of equal-length DNA strings."""
    if not Dna:
        return 0

    t = len(Dna)
    n = len(Dna[0])

    total = 0
    for i in range(n):
        column = [dna[i] for dna in Dna]
        counts = Counter(column)
        max_freq = max(counts.values())
        total += t - max_freq
    return total


def main():
    folder = os.path.dirname(__file__)

    # Example 1: nfkbMotifs.txt
    nfkb_path = os.path.join(folder, 'nfkbMotifs.txt')
    motifs_nfkb = read_motifs(nfkb_path)
    score_nfkb = score(motifs_nfkb)
    print('nfkbMotifs.txt:')
    print(f'  motifs: {len(motifs_nfkb)}')
    print(f'  length: {len(motifs_nfkb[0])}')
    print(f'  score: {score_nfkb} (expected 30)\n')

    # Example 2: dataset_40_9.txt
    dataset_path = os.path.join(folder, 'dataset_40_9.txt')
    motifs_dataset = read_motifs(dataset_path)
    score_dataset = score(motifs_dataset)
    print('dataset_40_9.txt:')
    print(f'  motifs: {len(motifs_dataset)}')
    print(f'  length: {len(motifs_dataset[0])}')
    print(f'  score: {score_dataset}')


if __name__ == '__main__':
    main()
