#!/usr/bin/env python3
"""BWMatching (Tema 4 - Ejercicio 4)."""

from collections import defaultdict

def validate_text(text):
    if text.count('$') != 1 or not text.endswith('$'):
        raise ValueError("Text must contain exactly one sentinel '$' at the end.")

def read_fasta_first_sequence(path):
    seq = []
    in_first_sequence = False
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('>'):
                if in_first_sequence:
                    break
                in_first_sequence = True
                continue
            if in_first_sequence:
                seq.append(line)
    return ''.join(seq)

def rotations(text):
    return [text[i:] + text[:i] for i in range(len(text))]


def bwt(text):
    validate_text(text)
    rots = rotations(text)
    rots.sort()
    return ''.join(r[-1] for r in rots)


def compute_ranks(column):
    counts = defaultdict(int)
    ranks = []
    for ch in column:
        ranks.append(counts[ch])
        counts[ch] += 1
    return ranks


def build_first_to_last(last_col):
    first_col = ''.join(sorted(last_col))
    last_ranks = compute_ranks(last_col)
    first_ranks = compute_ranks(first_col)

    pos_in_first = {}
    for idx, (ch, r) in enumerate(zip(first_col, first_ranks)):
        pos_in_first[(ch, r)] = idx

    lf = [pos_in_first[(ch, r)] for ch, r in zip(last_col, last_ranks)]
    return lf


def bwMatching(lastColumn, firstToLast, pattern):
    top = 0
    bottom = len(lastColumn) - 1
    p = list(pattern)

    while top <= bottom:
        if p:
            symbol = p.pop()
            window = lastColumn[top:bottom + 1]
            if symbol not in window:
                return []
            first = top + window.index(symbol)
            last = bottom - window[::-1].index(symbol)
            top = firstToLast[first]
            bottom = firstToLast[last]
        else:
            return list(range(top, bottom + 1))
    return []

def run_example(text, pattern):
    last_col = bwt(text)
    lf = build_first_to_last(last_col)
    rows = bwMatching(last_col, lf, pattern)
    return last_col, lf, rows


def main():
    results = []
    folder = os.path.dirname(__file__)
    
    text = "panamabananas$"
    pattern = "ana"
    last_col, lf, rows = run_example(text, pattern)
    results.append((pattern, rows))
    
    oric_path = os.path.join(folder, 'oric.txt')
    if os.path.exists(oric_path):
        seq = read_fasta_first_sequence(oric_path) + '$'
        pattern2 = "cgga"
        last_col2 = bwt(seq)
        lf2 = build_first_to_last(last_col2)
        rows2 = bwMatching(last_col2, lf2, pattern2)
        results.append((pattern2, rows2))
    

if __name__ == '__main__':
    main()
