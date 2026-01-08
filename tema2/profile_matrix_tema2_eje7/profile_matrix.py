#!/usr/bin/env python3
"""Profile matrix with optional Laplace smoothing (Tema 2 - Exercise 7).

Functions
---------
- profile(Dna, Laplace=True): builds a probability profile over A/C/G/T for
  a list of equal-length DNA strings.
- read_motifs(path): reads motifs (one per line) from a text file.

Behavior
--------
For each column i in the motifs:
- Count A/C/G/T.
- If Laplace is True, add +1 to each count and divide by (t + 4).
- If Laplace is False, use raw counts and divide by t.

A profile is returned as a dictionary {"A": [...], "C": [...], "G": [...], "T": [...]}.
"""

import os
from collections import defaultdict


def clean_line(line):
    """Strip whitespace and return uppercase DNA without spaces."""
    return ''.join(line.strip().split()).upper()


def read_motifs(path):
    """Read motifs (one per line) from a text file, ignoring empty lines."""
    motifs = []
    with open(path, 'r') as f:
        for raw in f:
            # Remove all spaces and convert to uppercase
            seq = raw.strip().replace(" ", "").upper()
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


def profile(Dna, Laplace=True):
    """Build a profile matrix with optional Laplace smoothing."""
    if Dna is None:
        raise ValueError("Dna no puede ser None")
    
    # Clean and validate sequences
    seqs = [s.strip().upper() for s in Dna if s and s.strip()]
    if not seqs:
        return {b: [] for b in ('A', 'C', 'G', 'T')}
    
    n = len(seqs[0])
    if any(len(s) != n for s in seqs):
        raise ValueError("Todas las cadenas deben tener la misma longitud")
    
    # Count nucleotides at each position
    counts = {b: [0]*n for b in ('A', 'C', 'G', 'T')}
    
    for s in seqs:
        for i, ch in enumerate(s):
            if ch not in counts:
                raise ValueError(f"Nucleótido inválido '{ch}' en posición {i}")
            counts[ch][i] += 1
    
    # Calculate probabilities
    t = len(seqs)
    denom = (t * 2) if Laplace else t
    
    prof = {}
    for b in ('A', 'C', 'G', 'T'):
        if Laplace:
            prof[b] = [(c + 1) / denom for c in counts[b]]
        else:
            prof[b] = [c / denom for c in counts[b]]
    
    return prof


def print_profile(p):
    """Pretty-print the profile dictionary."""
    for b in "ACGT":
        probs = ' '.join(f"{v:.3f}" for v in p[b])
        print(f"{b}: {probs}")


def test_example():
    """Run the provided test case."""
    Dna = ["TAAC", "GTCT", "ACTA", "AGGT"]
    expected = {
        'A': [0.375, 0.25, 0.25, 0.25],
        'C': [0.125, 0.25, 0.25, 0.25],
        'G': [0.25, 0.25, 0.25, 0.125],
        'T': [0.25, 0.25, 0.25, 0.375],
    }
    result = profile(Dna, Laplace=True)

    print("Test (Laplace=True) on Dna = ['TAAC', 'GTCT', 'ACTA', 'AGGT']")
    print("Result profile:")
    print_profile(result)

    # Simple numerical check with rounding to 3 decimals
    ok = True
    for b in "ACGT":
        for got, exp in zip(result[b], expected[b]):
            if round(got, 3) != round(exp, 3):
                ok = False
                break
    print(f"Matches expected (rounded to 3 decimals): {ok}\n")


def main():
    # Run provided test
    test_example()

    # Profile for nfkbMotifs.txt (Laplace = True)
    folder = os.path.dirname(__file__)
    nfkb_path = os.path.join(folder, 'nfkbMotifs.txt')
    if os.path.exists(nfkb_path):
        motifs = read_motifs(nfkb_path)
        prof = profile(motifs, Laplace=True)
        print(f"Profile for nfkbMotifs.txt ({len(motifs)} motifs, length {len(motifs[0])}) with Laplace=True:")
        print_profile(prof)
        print()  # Empty line for clarity
        # Print the raw dictionary as the last line for submission
        print(prof)
    else:
        print(f"File not found: {nfkb_path}")


if __name__ == '__main__':
    main()
