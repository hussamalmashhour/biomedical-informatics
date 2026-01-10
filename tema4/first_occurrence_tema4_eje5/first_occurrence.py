#!/usr/bin/env python3
"""First occurrence helper (Tema 4 - Ejercicio 5)."""

def firstOccurrence(symbol, text):
    if len(symbol) != 1:
        raise ValueError("symbol must be a single character")
    if not text:
        raise ValueError("text must be non-empty")
    try:
        return text.index(symbol)
    except ValueError:
        return -1


def computeAllFirstOccurrences(text):
    if not text:
        raise ValueError("text must be non-empty")
    return {c: text.index(c) for c in sorted(set(text))}


def main():
    text = "$aaaaaabmnnps"
    symbol = "n"
    
    idx = firstOccurrence(symbol, text)
    all_first = computeAllFirstOccurrences(text)
    


if __name__ == '__main__':
    main()
