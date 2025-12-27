#!/usr/bin/env python3
"""BWMatching (Tema 4 - Ejercicio 4).

Implements backward search over the Burrows–Wheeler Transform.
Includes helpers to build LF-mapping (first-to-last), to compute BWT,
and to run example tests.

Complexity: O(m * n) for pattern length m and text length n (simple version).
"""

import os
import re
from collections import defaultdict

# ------------------------------------------------------------
# Helpers: validation and parsing
# ------------------------------------------------------------

def validate_text(text):
    if text.count('$') != 1 or not text.endswith('$'):
        raise ValueError("Text must contain exactly one sentinel '$' at the end.")


def read_fasta_first_sequence(path):
    """Read the first sequence from a FASTA-like file (ignores headers)."""
    seq = []
    in_first_sequence = False
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('>'):
                if in_first_sequence:
                    # We've hit the second sequence header, stop
                    break
                else:
                    # This is the first header, start reading
                    in_first_sequence = True
                    continue
            if in_first_sequence:
                seq.append(line)
    return ''.join(seq)

# ------------------------------------------------------------
# BWT and mapping builders
# ------------------------------------------------------------

def rotations(text):
    return [text[i:] + text[:i] for i in range(len(text))]


def bwt(text):
    """Compute BWT via sorted rotations (O(n^2 log n))."""
    validate_text(text)
    rots = rotations(text)
    rots.sort()
    last_col = ''.join(r[-1] for r in rots)
    return last_col


def compute_ranks(column):
    counts = defaultdict(int)
    ranks = []
    for ch in column:
        ranks.append(counts[ch])
        counts[ch] += 1
    return ranks


def build_first_to_last(last_col):
    """Build LF-mapping from last to first column.

    Returns a list lf where lf[i] is the row in the first column that
    corresponds to row i in the last column.
    """
    first_col = ''.join(sorted(last_col))
    last_ranks = compute_ranks(last_col)
    first_ranks = compute_ranks(first_col)

    pos_in_first = {}
    for idx, (ch, r) in enumerate(zip(first_col, first_ranks)):
        pos_in_first[(ch, r)] = idx

    lf = [pos_in_first[(ch, r)] for ch, r in zip(last_col, last_ranks)]
    return lf

# ------------------------------------------------------------
# BWMatching (backward search)
# ------------------------------------------------------------

def bwMatching(lastColumn, firstToLast, pattern):
    """Backward search over BWT.

    Returns list of row indices where the pattern occurs in the BWT matrix.
    """
    top = 0
    bottom = len(lastColumn) - 1
    p = list(pattern)

    while top <= bottom:
        if p:
            symbol = p.pop()  # last character
            # slice to inspect
            window = lastColumn[top:bottom + 1]
            if symbol not in window:
                return []
            # find first and last occurrence inside window
            first = top + window.index(symbol)
            last = bottom - window[::-1].index(symbol)
            top = firstToLast[first]
            bottom = firstToLast[last]
        else:
            return list(range(top, bottom + 1))
    return []

# ------------------------------------------------------------
# Main / Tests
# ------------------------------------------------------------

def run_example(text, pattern):
    last_col = bwt(text)
    lf = build_first_to_last(last_col)
    rows = bwMatching(last_col, lf, pattern)
    return last_col, lf, rows


def main():
    results = []

    # Example from lecture
    text = "panamabananas$"
    pattern = "ana"
    last_col, lf, rows = run_example(text, pattern)
    results.append((pattern, rows))
    print("Example text:", text)
    print("Pattern:", pattern)
    print("Rows:", rows)
    print()

    # Genome test: Vibrio cholerae oriC (first sequence in provided file)
    folder = os.path.dirname(__file__)
    oric_path = os.path.join(folder, 'oric.txt')
    if os.path.exists(oric_path):
        seq = read_fasta_first_sequence(oric_path) + '$'  # Keep original case (lowercase)
        pattern2 = "cgga"  # Pattern in lowercase as specified in exercise
        last_col2 = bwt(seq)
        lf2 = build_first_to_last(last_col2)
        rows2 = bwMatching(last_col2, lf2, pattern2)
        results.append((pattern2, rows2))
        print("Genome test (V. cholerae oriC):")
        print(f"  Pattern: {pattern2}")
        print(f"  Matches (row indices): {rows2}")
        print(f"  Total matches: {len(rows2)}")
    else:
        print(f"oric.txt not found at {oric_path}")

    # Write results
    out_path = os.path.join(folder, 'bwmatching_results.txt')
    with open(out_path, 'w') as f:
        for pat, rows in results:
            f.write(f"Pattern: {pat}\n")
            f.write(f"Rows: {rows}\n\n")
    print(f"\nWritten results to {out_path}")


if __name__ == '__main__':
    main()
