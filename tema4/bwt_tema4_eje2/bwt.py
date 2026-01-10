#!/usr/bin/env python3
"""Burrows–Wheeler Transform (Tema 4 - Ejercicio 2).
"""


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
    

if __name__ == '__main__':
    main()
