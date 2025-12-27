#!/usr/bin/env python3
"""Profile Most Probable k-mer (Tema 2 - Exercise 9).

Functions
---------
- read_motifs(path): read motifs (one per line), cleaning whitespace/case.
- build_profile_raw(motifs): build profile without Laplace smoothing.
- Pr(profile, motif): probability of a motif under the profile.
- mostProbableKmer(profile, text, k): scan text and return the k-mer with
  highest probability (first in case of ties).

Notes
-----
- No Laplace smoothing here; profiles use raw frequencies.
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


def build_profile(motifs, laplace=False):
    """Build a profile from motifs (optionally Laplace-smoothed).

    laplace=False -> raw frequencies (counts / t)
    laplace=True  -> add +1 to each nucleotide before normalizing.
    """
    if not motifs:
        return {b: [] for b in "ACGT"}
    t = len(motifs)
    n = len(motifs[0])

    profile = {b: [] for b in "ACGT"}
    add = 1 if laplace else 0
    denom = t + 4 * add

    for i in range(n):
        column = [m[i] for m in motifs]
        counts = Counter(column)
        if add:
            for b in "ACGT":
                counts[b] = counts.get(b, 0) + add
        for b in "ACGT":
            profile[b].append(counts.get(b, 0) / denom)
    return profile


def Pr(profile, motif):
    """Compute probability of motif given profile."""
    prob = 1.0
    for i, base in enumerate(motif):
        prob *= profile[base][i]
    return prob


def mostProbableKmer(profile, text, k):
    """Return the most probable k-mer in text according to profile."""
    best_kmer = text[:k]
    best_prob = Pr(profile, best_kmer)

    for i in range(1, len(text) - k + 1):
        kmer = text[i:i + k]
        p = Pr(profile, kmer)
        if p > best_prob:
            best_prob = p
            best_kmer = kmer
    return best_kmer


def run_example():
    """Run the provided example test.

    Note: The expected answer assumes Laplace smoothing, so we enable it
    when building the profile. The search itself uses the provided profile
    (no smoothing inside Pr/mostProbableKmer).
    """
    motifs = ["TTATATCGG", "GTCTACACA", "ACTAGGAGC", "AGGTTTATA"]
    profile = build_profile(motifs, laplace=True)
    text = "TTATGTTTGGAAACTCTATCACCGACTGCTAGCA"
    k = 9
    result = mostProbableKmer(profile, text, k)
    print("Example profile (Laplace-smoothed when building)")
    print(f"Most probable k-mer (k={k}): {result} (expected ATGTTTGGA)\n")


def run_nfkb():
    """Run the NF-κB test using nfkbMotifs.txt (no Laplace in Pr)."""
    folder = os.path.dirname(__file__)
    nfkb_path = os.path.join(folder, 'nfkbMotifs.txt')
    motifs = read_motifs(nfkb_path)
    # Keep raw frequencies unless you want smoothing; here stay raw.
    profile = build_profile(motifs, laplace=False)

    text = "GGTACGGGGATTACCT"
    k = len(motifs[0])  # 12
    result = mostProbableKmer(profile, text, k)
    print("NF-κB profile (raw frequencies)")
    print(f"Text: {text}")
    print(f"k = {k}")
    print(f"Most probable k-mer: {result}\n")


def main():
    run_example()
    run_nfkb()


if __name__ == '__main__':
    main()
