#!/usr/bin/env python3
"""
Compute average GC content across sequences in a FASTA file.

Implements function `GCcontent(path)` which accepts a local FASTA file path.
We ignore rare/ambiguous nucleotides (N, R, Y, etc.) when computing
per-sequence GC fractions: denominator is only A+T+C+G counts. The function
returns the average GC fraction across all sequences in the file (a float
between 0 and 1).

Usage (local file only):
    python "d:\\Biomedical Informatics\\gccontent_tema1_eje3\\gccontent.py" <path>
"""
from __future__ import annotations
import sys
import re
from typing import List


def gc_fraction_of_sequence(seq: str) -> float:
    """Return GC fraction for a single sequence string.

    Only counts A,C,G,T towards the denominator. Ignores other letters.
    If no A/C/G/T present, returns 0.0.
    """
    s = seq.upper()
    g = s.count('G')
    c = s.count('C')
    a = s.count('A')
    t = s.count('T')
    denom = a + t + g + c
    if denom == 0:
        return 0.0
    return (g + c) / denom


def read_fasta_sequences_from_text(text: str) -> List[str]:
    """Parse FASTA-formatted text and return list of sequences (strings).

    If the input has no FASTA headers, the whole text is treated as a single
    sequence (after joining lines and keeping only letters).
    """
    lines = text.splitlines()
    seqs: List[str] = []
    current = []
    has_header = False
    for line in lines:
        if line.startswith('>'):
            has_header = True
            if current:
                seqs.append(''.join(current))
                current = []
            continue
        # keep only letters (we'll filter to A/C/G/T/N later if needed)
        stripped = ''.join(re.findall(r'[A-Za-z]', line))
        if stripped:
            current.append(stripped)
    if current:
        seqs.append(''.join(current))
    if not has_header:
        # If there were no headers, treat entire joined text as single sequence
        if seqs:
            joined = ''.join(seqs)
            return [joined]
        else:
            return []
    return seqs


def fetch_text_from_path(path: str) -> str:
    """Return text content from a local file path."""
    with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
        return fh.read()


def GCcontent(path: str) -> float:
    """Compute average GC fraction across all sequences in FASTA at `path`.

    Returns a float fraction between 0 and 1 (average of per-sequence GC
    fractions). If no sequences found, returns 0.0.
    """
    text = fetch_text_from_path(path)
    seqs = read_fasta_sequences_from_text(text)
    if not seqs:
        return 0.0
    fractions = []
    for s in seqs:
        # keep only A/C/G/T letters for GC calculation
        filtered = ''.join(re.findall(r'[ACGTacgt]', s))
        frac = gc_fraction_of_sequence(filtered)
        fractions.append(frac)
    if not fractions:
        return 0.0
    return sum(fractions) / len(fractions)


def main(argv=None) -> int:
    argv = argv or sys.argv[1:]
    if not argv:
        print('Usage: gccontent.py <path_or_url_to_fasta>')
        return 2
    path = argv[0]
    print('Computing average GC content for:', path)
    val = GCcontent(path)
    print('Average GC fraction (0..1):', val)
    print('Average GC percentage:', f'{val*100:.6f}%')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
