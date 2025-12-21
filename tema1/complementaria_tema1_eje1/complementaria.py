#!/usr/bin/env python3
"""
Read a genome from a local text file, extract the 20 nucleotides
in the center (ignoring non-ACGT/N characters) and print that sequence and
its reverse-complement using the function `complementaria(seq)`.

Usage: python complementaria_tema1_eje1/complementaria.py [path/to/data.txt]
If no path is provided, defaults to a `data.txt` next to this script.
"""
from __future__ import annotations
import re
import sys
import os


def complementaria(seq: str) -> str:
    """Return the reverse complement of seq.

    Maps A<->T, C<->G. Preserves case (upper->upper, lower->lower).
    Non-ACGT/N characters are returned unchanged but typically input will
    only contain ACGT/N.
    """
    trans = {
        'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C', 'N': 'N',
        'a': 't', 't': 'a', 'c': 'g', 'g': 'c', 'n': 'n'
    }
    complemented = ''.join(trans.get(b, b) for b in seq)
    return complemented[::-1]


def read_genome_file(file_path: str) -> str:
    """Read text from a local file and return only the A/C/G/T/N characters joined as a single sequence."""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        raw = f.read()
    letters = re.findall(r'[ACGTNacgtn]', raw)
    return ''.join(letters)


def main() -> int:
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = os.path.join(os.path.dirname(__file__), 'data.txt')
    print('Reading genome from:', file_path)
    try:
        genome = read_genome_file(file_path)
    except OSError as e:
        print(f'Error reading file: {e}', file=sys.stderr)
        return 2
    n = len(genome)
    if n == 0:
        print('Error: no nucleotide letters found in file.', file=sys.stderr)
        return 2
    print(f'Genome length (ACGT/N letters only): {n}')
    # center 20 nucleotides: start is middle-10
    start = max(0, (n // 2) - 10)
    seq = genome[start:start + 20]
    print('\nCenter 20-nt sequence:')
    print(seq)
    print('\nReverse complement (complementaria(seq)):')
    print(complementaria(seq))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
