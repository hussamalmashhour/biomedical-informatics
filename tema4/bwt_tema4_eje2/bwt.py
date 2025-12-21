#!/usr/bin/env python3
"""Burrows–Wheeler Transform (Tema 4 - Ejercicio 2).

Simple O(n^2 log n) implementation by sorting all cyclic rotations.
More advanced O(n) approaches exist via suffix arrays, but are not required here.
"""

import os


def validate_text(text):
    """Ensure the input has a single trailing sentinel '$'."""
    if text.count('$') != 1 or not text.endswith('$'):
        raise ValueError("Input text must contain exactly one sentinel '$' at the end.")


def rotations(text):
    """Return all cyclic rotations of text."""
    n = len(text)
    return [text[i:] + text[:i] for i in range(n)]


def bwt(text):
    """Compute the Burrows–Wheeler Transform of text."""
    validate_text(text)
    rots = rotations(text)
    rots.sort()  # lexicographic order
    last_column = [r[-1] for r in rots]
    return ''.join(last_column), rots


def print_rotations(rots):
    for r in rots:
        print(r)


def main():
    text = "panamabananas$"
    bwt_str, rots = bwt(text)

    print("Text:", text)
    print("BWT:", bwt_str)
    print("\nSorted rotations (for verification):")
    print_rotations(rots)

    out_path = os.path.join(os.path.dirname(__file__), 'bwt.txt')
    with open(out_path, 'w') as f:
        f.write(bwt_str)
    print(f"\nWritten BWT to {out_path}")


if __name__ == '__main__':
    main()
