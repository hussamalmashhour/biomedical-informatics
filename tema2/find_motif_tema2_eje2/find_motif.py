#!/usr/bin/env python3
"""Minimal motif finder with skew-based window selection.

What it does (no arguments needed):
1) Reads E-coli.txt from this folder (FASTA or plain).
2) Cleans to A/C/G/T.
3) Finds minSkew positions.
4) Takes a 500 bp window from the first minSkew position.
5) Searches motif TTATCCACA allowing 1 mismatch.
6) Prints all hits with genomic positions.

You can also run the built-in textbook example by calling main_example().
"""

import os


def clean_sequence(text):
    if not text:
        return ""
    lines = text.splitlines()
    if any(line.startswith('>') for line in lines):
        lines = [ln for ln in lines if not ln.startswith('>')]
    seq = ''.join(lines)
    return ''.join(ch for ch in seq if ch.isalpha()).upper()


def find_motif(motif, seq, d):
    if not motif or not seq or d < 0:
        return {}
    motif = motif.upper()
    seq = seq.upper()
    k = len(motif)
    out = {}
    for i in range(len(seq) - k + 1):
        window = seq[i:i + k]
        mismatches = sum(1 for a, b in zip(window, motif) if a != b)
        if mismatches <= d:
            out[i] = window
    return out


def skew(seq):
    s = seq.upper()
    values = [0]
    cur = 0
    for ch in s:
        if ch == 'G':
            cur += 1
        elif ch == 'C':
            cur -= 1
        values.append(cur)
    return values


def min_skew(seq):
    arr = skew(seq)
    if not arr:
        return []
    mn = min(arr)
    return [i for i, v in enumerate(arr) if v == mn]


def main_example():
    seq = "CGCCCGAATCCAGAACGCATTCCCCTGGCCTCCATTCTGGAACGGTACGGACGTCAATCAAAT"
    motif = "ATTCTGGA"
    d = 3
    res = find_motif(motif, seq, d)
    print('Example result (sorted by position):')
    for pos in sorted(res):
        print(f'{pos}: {res[pos]}')
    print('Expected keys include 6, 7, 33')


def run_ecoli_pipeline():
    path = os.path.join(os.path.dirname(__file__), 'E-coli.txt')
    with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
        text = fh.read()
    seq = clean_sequence(text)
    if not seq:
        raise SystemExit('Sequence is empty after cleaning E-coli.txt')
    mins = min_skew(seq)
    if not mins:
        raise SystemExit('Could not compute minSkew positions')
    start_pos = mins[0]
    window_len = 500
    subseq = seq[start_pos:start_pos + window_len]
    motif = 'TTATCCACA'
    d = 1
    hits = find_motif(motif, subseq, d)
    print(f'E-coli pipeline: start at minSkew pos {start_pos}, window {window_len}, motif {motif}, d={d}')
    print(f'Found {len(hits)} matches:')
    for pos in sorted(hits):
        print(f'{start_pos + pos}: {hits[pos]}')


def main():
    # Run the E. coli pipeline by default. Uncomment the next line to see the example.
    # main_example()
    run_ecoli_pipeline()


if __name__ == '__main__':
    main()
