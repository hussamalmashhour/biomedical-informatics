#!/usr/bin/env python3
"""Suffix array (Tema 4 - Ejercicio 1).

Simple O(n^2 log n) implementation by sorting all suffixes.
Advanced linear-time algorithms (e.g., SA-IS) exist but are not required here.
"""

import os


def validate_text(text):
    """Ensure text ends with a unique sentinel '$'."""
    if text.count('$') != 1 or not text.endswith('$'):
        raise ValueError("Input text must contain a single sentinel '$' at the end.")


def suffixArray(text):
    """Return suffix array of text: starting indices of suffixes in lexicographic order."""
    validate_text(text)
    suffixes = [(text[i:], i) for i in range(len(text))]
    suffixes.sort(key=lambda x: x[0])
    return [idx for _, idx in suffixes]


def printSuffixes(text, sa):
    """Print sorted suffixes for verification (debug helper)."""
    for idx in sa:
        print(f"{idx:>3}: {text[idx:]}")


def main():
    text = "panamabananas$"
    sa = suffixArray(text)

    print("Text:", text)
    print("Suffix array:", sa)
    print("\nSorted suffixes (for verification):")
    printSuffixes(text, sa)

    out_path = os.path.join(os.path.dirname(__file__), 'suffix_array.txt')
    with open(out_path, 'w') as f:
        f.write(' '.join(map(str, sa)))
    print(f"\nWritten suffix array to {out_path}")


if __name__ == '__main__':
    main()
