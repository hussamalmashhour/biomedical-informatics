#!/usr/bin/env python3
"""First occurrence helper (Tema 4 - Ejercicio 5).

Provides:
- firstOccurrence(symbol, text): returns the first index of symbol in text (or -1).
- computeAllFirstOccurrences(text): dictionary of first positions for all distinct symbols.

This helper is useful when building LF-mapping / FM-index tables for BWT-based
search, where the first occurrence of each character in the first column is
needed.
"""

import os


def firstOccurrence(symbol, text):
    """Return the first index of symbol in text (or -1 if absent).

    Raises ValueError if symbol is not a single character or text is empty.
    """
    if len(symbol) != 1:
        raise ValueError("symbol must be a single character")
    if not text:
        raise ValueError("text must be non-empty")
    try:
        return text.index(symbol)
    except ValueError:
        return -1


def computeAllFirstOccurrences(text):
    """Return a dict {char: first_index} for all distinct characters in text."""
    if not text:
        raise ValueError("text must be non-empty")
    return {c: text.index(c) for c in sorted(set(text))}


def main():
    # Example from statement
    text = "$aaaaaabmnnps"
    symbol = "n"

    idx = firstOccurrence(symbol, text)
    all_first = computeAllFirstOccurrences(text)

    print(f"Text: {text}")
    print(f"Symbol: {symbol}")
    print(f"First occurrence index: {idx}")
    print("All first occurrences:")
    print(all_first)

    out_path = os.path.join(os.path.dirname(__file__), 'first_occurrences.txt')
    with open(out_path, 'w') as f:
        f.write(f"Text: {text}\n")
        f.write(f"Symbol: {symbol}\n")
        f.write(f"First occurrence: {idx}\n")
        f.write("All first occurrences:\n")
        for k, v in all_first.items():
            f.write(f"{k}: {v}\n")
    print(f"\nWritten results to {out_path}")


if __name__ == '__main__':
    main()
