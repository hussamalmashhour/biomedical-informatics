#!/usr/bin/env python3
"""Probability of a motif given a profile (Tema 2 - Exercise 8).

Functions
---------
- read_motifs(path): read DNA motifs (one per line), cleaning whitespace/case.
- build_profile_raw(motifs): build profile without Laplace smoothing.
- Pr(profile, motif): compute probability of a motif under the profile.

Notes
-----
- No Laplace smoothing is applied in this exercise.
- All motifs must have equal length.
- Only standard Python is used.
"""

import os
from collections import Counter


def clean_line(line):
    """Strip whitespace and return uppercase DNA without spaces."""
    return ''.join(line.strip().split()).upper()


def read_motifs(path):
    """Read motifs (one per line) from a text file, ignoring empty lines."""
    motifs = []
    with open(path, 'r') as f:
        for raw in f:
            seq = clean_line(raw)
            if not seq:
                continue
            motifs.append(seq)

    if not motifs:
        raise ValueError(f"No motifs found in {path}")

    length = len(motifs[0])
    for m in motifs:
        if len(m) != length:
            raise ValueError(
                f"All motifs must have equal length (expected {length}, got {len(m)})"
            )
    return motifs


def build_profile_raw(motifs):
    """Build a profile (no smoothing) from motifs."""
    if not motifs:
        return {b: [] for b in "ACGT"}
    t = len(motifs)
    n = len(motifs[0])

    profile = {b: [] for b in "ACGT"}
    for i in range(n):
        column = [m[i] for m in motifs]
        counts = Counter(column)
        for b in "ACGT":
            profile[b].append(counts.get(b, 0) / t)
    return profile


def Pr(profile, motif):
    """Compute probability of motif given profile (no smoothing applied here)."""
    prob = 1.0
    for i, base in enumerate(motif):
        prob *= profile[base][i]
    return prob


def main():
    folder = os.path.dirname(__file__)
    nfkb_path = os.path.join(folder, '..', 'nfkbMotifs.txt')

    motifs = read_motifs(nfkb_path)
    prof = build_profile_raw(motifs)

    # Example motif (expected ~0.000839808)
    motif1 = "ACGGGGATTACC"
    p1 = Pr(prof, motif1)
    print("nfkbMotifs profile (no Laplace)")
    print(f"Motifs: {len(motifs)}, length: {len(motifs[0])}\n")
    print(f"motif1 = {motif1}\nP = {p1:.9f} (expected 0.000839808)\n")

    # Test motif provided
    motif2 = "TCGGGGATTTCC"
    p2 = Pr(prof, motif2)
    print(f"motif2 = {motif2}\nP = {p2:.9f}")


if __name__ == '__main__':
    main()
