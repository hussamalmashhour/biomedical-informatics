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
    """Compute the Burrows–Wheeler Transform of text.
    
    Returns:
        list: BWT as list of characters (e.g., ['s', 'm', 'n', ...])
    """
    validate_text(text)
    rots = rotations(text)
    rots.sort()  # lexicographic order
    last_column = [r[-1] for r in rots]
    return last_column


def print_rotations(rots):
    for r in rots:
        print(r)


def main():
    text = "panamabananas$"
    bwt_result = bwt(text)

    print("Text:", text)
    print("BWT (as list):", bwt_result)
    print("BWT (as string):", ''.join(bwt_result))
    
    # Show first few sorted rotations for verification
    rots = rotations(text)
    rots.sort()
    print("\nFirst 5 sorted rotations (for verification):")
    for r in rots[:5]:
        print(f"  {r} → last char: '{r[-1]}'")

    out_path = os.path.join(os.path.dirname(__file__), 'bwt.txt')
    with open(out_path, 'w') as f:
        f.write(''.join(bwt_result))
    print(f"\nWritten BWT to {out_path}")


if __name__ == '__main__':
    main()
