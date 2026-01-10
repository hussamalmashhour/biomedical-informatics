#!/usr/bin/env python3
"""Inverse Burrows–Wheeler Transform (Tema 4 - Ejercicio 3).
"""

from collections import defaultdict


def validate_bwt(bwt_text):
    """Ensure there is exactly one sentinel '$'."""
    if bwt_text.count('$') != 1:
        raise ValueError("BWT must contain exactly one sentinel '$'.")


def compute_ranks(column):
    """Compute occurrence ranks for each character position in the column.

    Returns a list of ranks (0-based) per position.
    """
    counts = defaultdict(int)
    ranks = []
    for ch in column:
        ranks.append(counts[ch])
        counts[ch] += 1
    return ranks


def lf_mapping(bwt_text):
    """Build LF-mapping arrays: first_col indices for each row.

    Returns (first_col, lf), where:
    - first_col is the sorted characters (first column)
    - lf maps row index in BWT (last column) to row index in first column.
    """
    validate_bwt(bwt_text)
    first_col = ''.join(sorted(bwt_text))

    # ranks for last column (BWT) and first column
    last_ranks = compute_ranks(bwt_text)
    first_ranks = compute_ranks(first_col)

    # map from (char, rank) to position in first column
    pos_in_first = {}
    for idx, (ch, r) in enumerate(zip(first_col, first_ranks)):
        pos_in_first[(ch, r)] = idx

    lf = []
    for ch, r in zip(bwt_text, last_ranks):
        lf.append(pos_in_first[(ch, r)])

    return first_col, lf


def ibwt(bwt_text):
    """Inverse BWT using LF-mapping.

    Reconstructs original text ending with '$'.
    """
    first_col, lf = lf_mapping(bwt_text)

    # start from the row with sentinel in BWT (last column)
    row = bwt_text.index('$')
    result = []
    for _ in range(len(bwt_text)):
        ch = bwt_text[row]
        result.append(ch)
        row = lf[row]

    # We traversed from '$' backward; reverse to get original text
    return ''.join(reversed(result))


def main():
    bwt_text = "smnpbnnaaaaa$a"
    original = ibwt(bwt_text)
    

if __name__ == '__main__':
    main()
