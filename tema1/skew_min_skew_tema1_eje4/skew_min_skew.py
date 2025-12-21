#!/usr/bin/env python3
"""
Compute GC content, skew, and minSkew positions for DNA sequences using local files only.

Implements:
 - GCcontent(path): average GC fraction across all sequences in a FASTA file (local path)
 - skew(seq): returns a list of integer skew values starting from 0; length = len(seq)+1
 - minSkew(seq): returns list of positions (indices into the skew list) where skew is minimal
 - plot_skew(seq, title=None): plot skew array using matplotlib

Only local input paths are accepted. FASTA headers (lines starting with '>') are ignored
and ambiguous nucleotides are skipped for GC content. For skew, non A/C/G/T letters are
ignored when building the sequence.

Usage (local file only):
    python "d:\\Biomedical Informatics\\skew_min_skew_tema1_eje4\\skew_min_skew.py" <path> [--plot]
"""
from __future__ import annotations
import sys
import re
import argparse
import os
from typing import List


def read_fasta_sequences_from_text(text: str) -> List[str]:
    """Parse FASTA-formatted text and return list of sequence strings."""
    lines = text.splitlines()
    seqs: List[str] = []
    current: List[str] = []
    for line in lines:
        if line.startswith('>'):
            if current:
                seqs.append(''.join(current))
                current = []
            continue
        letters = ''.join(re.findall(r'[A-Za-z]', line))
        if letters:
            current.append(letters)
    if current:
        seqs.append(''.join(current))
    # If no headers were found, treat the entire cleaned text as a single sequence
    if not any(ln.startswith('>') for ln in lines):
        joined = ''.join(seqs)
        return [joined] if joined else []
    return seqs


def GCcontent(path: str) -> float:
    """Compute average GC fraction across all sequences in a local FASTA file."""
    with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
        text = fh.read()
    seqs = read_fasta_sequences_from_text(text)
    if not seqs:
        return 0.0
    fractions: List[float] = []
    for seq in seqs:
        filtered = ''.join(re.findall(r'[ACGTacgt]', seq))
        s = filtered.upper()
        g = s.count('G')
        c = s.count('C')
        a = s.count('A')
        t = s.count('T')
        denom = a + c + g + t
        if denom == 0:
            continue
        fractions.append((g + c) / denom)
    return sum(fractions) / len(fractions) if fractions else 0.0


def skew(seq: str) -> List[int]:
    """Return skew array for seq. Start at 0, then for each base: +1 if G, -1 if C, else 0 change."""
    s = seq.upper()
    values: List[int] = [0]
    cur = 0
    for ch in s:
        if ch == 'G':
            cur += 1
        elif ch == 'C':
            cur -= 1
        # else A/T/N/other: no change
        values.append(cur)
    return values


def minSkew(seq: str) -> List[int]:
    """Return list of positions (indices in skew array) where skew is minimal."""
    arr = skew(seq)
    if not arr:
        return []
    mn = min(arr)
    return [i for i, v in enumerate(arr) if v == mn]


def fetch_sequence_from_path(path: str) -> str:
    """Read text from local path and return sequence string keeping only A/C/G/T letters."""
    with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
        raw = fh.read()
    lines = [ln for ln in raw.splitlines() if not ln.startswith('>')]
    joined = ''.join(lines)
    seq_letters = ''.join(re.findall(r'[ACGTacgt]', joined))
    return seq_letters


def plot_skew(seq: str, title: str | None = None) -> None:
    """Plot skew array for the given sequence using matplotlib."""
    try:
        import matplotlib.pyplot as plt  # type: ignore
    except ImportError as exc:
        raise RuntimeError('matplotlib is required for plotting skew') from exc
    arr = skew(seq)
    positions = list(range(len(arr)))
    plt.figure(figsize=(10, 4))
    plt.plot(positions, arr, linewidth=1)
    plt.xlabel('Position')
    plt.ylabel('Skew')
    plt.title(title or 'Skew plot')
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.show()


def main(argv=None) -> int:
    argv = argv or sys.argv[1:]
    parser = argparse.ArgumentParser(description='Compute GC content, skew, and minSkew for a DNA sequence file (local only).')
    parser.add_argument('path', help='Local path to FASTA/plain sequence file')
    parser.add_argument('--plot', action='store_true', help='Plot skew using matplotlib (if installed)')
    args = parser.parse_args(argv)

    path = args.path
    print('Reading sequence from:', path)
    seq = fetch_sequence_from_path(path)
    n = len(seq)
    print(f'Sequence length (A/C/G/T only): {n}')
    if n == 0:
        print('No sequence letters found.', file=sys.stderr)
        return 2
    # Report GC content for the same file
    gc_val = GCcontent(path)
    print(f'Average GC fraction (0..1): {gc_val:.6f}')
    print(f'Average GC percentage: {gc_val*100:.4f}%')
    arr = skew(seq)
    mins = minSkew(seq)
    # Print some context: minimal skew value and positions
    minval = min(arr)
    print(f'Minimal skew value: {minval}')
    print('Positions with minimal skew (0-based indices):')
    print(' '.join(map(str, mins)))
    print('\nPositions with minimal skew (1-based positions):')
    print(' '.join(str(i + 1) for i in mins))
    # Optionally print first 100 skew values for inspection
    print('\nFirst 100 skew values (index: value):')
    for i, v in enumerate(arr[:100]):
        print(f'{i}: {v}', end='; ')
    print()
    if args.plot:
        try:
            plot_skew(seq, title=f"Skew plot for {os.path.basename(path) or path}")
        except RuntimeError as exc:
            print(f'Plotting skipped: {exc}', file=sys.stderr)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
