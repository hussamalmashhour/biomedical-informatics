#!/usr/bin/env python3
"""
Compute nucleotide frequency dictionary for a sequence.

Reads a plain-text file, keeps only A/C/G/T/N letters, computes
frequencies with `frecuencia(seq)` and prints counts and fractional
frequencies.

Usage:
    python "d:\\Biomedical Informatics\\frecuencia_tema1_eje2\\frecuencia.py" [path_to_data]

If no path is given, `data.txt` in the same folder is used.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path
from collections import Counter
from typing import Dict


def frecuencia(seq: str) -> Dict[str, float]:
    """Return a dictionary {nucleotide: frequency} for seq.

    Counts all letters present among A,C,G,T,N (case-insensitive).
    Frequencies are computed as count / total_count where total_count is
    the number of letters counted (including 'N' if present).
    Returned keys are upper-case letters only for letters seen in seq.
    """
    seq = seq.upper()
    allowed = ['A', 'C', 'G', 'T', 'N']
    counts = Counter(ch for ch in seq if ch in allowed)
    total = sum(counts.values())
    if total == 0:
        return {}
    freqs = {base: counts[base] / total for base in sorted(counts)}
    return freqs


def load_sequence(path: Path) -> str:
    """Return concatenated A/C/G/T/N letters from a text file."""
    try:
        raw = path.read_text(encoding='utf-8', errors='ignore')
    except FileNotFoundError:
        print(f'File not found: {path}', file=sys.stderr)
        return ''
    letters = re.findall(r'[ACGTNacgtn]', raw)
    return ''.join(letters)


def main() -> int:
    default_path = Path(__file__).with_name('data.txt')
    data_path = Path(sys.argv[1]) if len(sys.argv) > 1 else default_path
    print('Reading nucleotides from:', data_path)

    genome = load_sequence(data_path)
    n = len(genome)
    if n == 0:
        print('No nucleotide letters found.', file=sys.stderr)
        return 2

    print(f'Genome length (ACGT/N letters only): {n}\n')
    freqs = frecuencia(genome)
    counts = Counter(genome.upper())
    print('Nucleotide counts and frequencies:')
    for base in sorted(freqs):
        print(f"{base}: {counts[base]} ({freqs[base]:.6f})")

    print(f"\nSum of reported frequencies: {sum(freqs.values()):.6f}")
    
    # Print the result dictionary for automated testing (last line)
    print(freqs)
    
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
