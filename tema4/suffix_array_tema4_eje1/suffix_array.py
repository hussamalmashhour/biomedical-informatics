#!/usr/bin/env python3
"""Suffix array (Tema 4 - Ejercicio 1).
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
    print("\nSorted suffixes:")
    printSuffixes(text, sa)

if __name__ == '__main__':
    main()
