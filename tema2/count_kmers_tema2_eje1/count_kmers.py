#!/usr/bin/env python3
"""
count_kmers.py

Implements `countKmers(seq, k, n)` which returns a dictionary of k-mer counts
filtered to only k-mers that appear >= n times. Handles raw sequences and
FASTA-formatted text (ignores header lines starting with '>').

Includes a CLI to run the provided examples or any local FASTA file.

Usage (examples):
    python "d:\\Biomedical Informatics\\tema2\\count_kmers_tema2_eje1\\count_kmers.py"

Usage (custom file):
    python "d:\\Biomedical Informatics\\tema2\\count_kmers_tema2_eje1\\count_kmers.py" \
        --path "d:\\Biomedical Informatics\\tema2\\count_kmers_tema2_eje1\\oric.fasta" --k 9 --n 3
"""
import argparse
from collections import Counter
from typing import Dict


def _clean_sequence(text: str) -> str:
    """Return sequence letters from raw text or FASTA, upper-cased.

    If `text` contains FASTA header lines (starting with '>'), those lines
    are ignored and the remaining lines concatenated. Non-letter whitespace
    is removed.
    """
    if not text:
        return ""
    # If looks like FASTA (has header or newlines), process lines
    lines = text.splitlines()
    if any(line.startswith('>') for line in lines):
        # remove header lines
        seq_lines = [line.strip() for line in lines if not line.startswith('>')]
        seq = ''.join(seq_lines)
    else:
        # remove whitespace
        seq = ''.join(lines)
    # keep letters only and uppercase
    seq = ''.join(ch for ch in seq if ch.isalpha()).upper()
    return seq


def countKmers(seq: str, k: int, n: int) -> Dict[str, int]:
    """Count k-mers of length `k` in `seq` and return those with count >= n.

    Args:
        seq: input sequence (raw letters or FASTA text containing a header).
        k: k-mer length (must be > 0).
        n: minimum occurrences to include in output (n >= 1 typically).

    Returns:
        A dictionary mapping k-mer (uppercase) -> count (int) for counts >= n.
    """
    if k <= 0:
        return {}
    s = _clean_sequence(seq)
    L = len(s)
    if k > L:
        return {}
    counts = Counter()
    for i in range(0, L - k + 1):
        kmer = s[i:i + k]
        counts[kmer] += 1
    # filter
    return {kmer: cnt for kmer, cnt in counts.items() if cnt >= n}


# --- Test / CLI harness ---

_short_example_seq = "ACGTTGCATGTCGCATGATGCATGAGAGCT"
_vibrio_cholerae_fasta = ">oriC [Vibrio cholerae]\n" + (
    "atcaatgatcaacgtaagcttctaagcatgatcaaggtgctcacacagtttatccacaacctgagtggatgacatcaagataggtcgttgtatctccttcctctcgtactctcatgaccacggaaagatgatcaagagaggatgatttcttggccatatcgcaatgaatacttgtgacttgtgcttccaattgacatcttcagcgccatattgcgctggccaaggtgacggagcgggattacgaaagcatgatcatggctgttgttctgtttatcttgttttgactgagacttgttaggatagacggtttttcatcactgactagccaaagccttactctgcctgacatcgaccgtaaattgataatgaatttacatgcttccgcgacgatttacctcttgatcatcgatccgattgaagatcttcaattgttaattctcttgcctcgactcatagccatgatgagctcttgatcatgtttccttaaccctctattttttacggaagaatgatcaagctgctgctcttgatcatcgtttc"
)

_vibrio_thermotoga_fasta = ">oriC [Thermotoga petrophila]\n" + (
    "aactctatacctcctttttgtcgaatttgtgtgatttatagagaaaatcttattaactgaaactaaaatggtaggtttggtggtaggttttgtgtacattttgtagtatctgatttttaattacataccgtatattgtattaaattgacgaacaattgcatggaattgaatatatgcaaaacaaacctaccaccaaactctgtattgaccattttaggacaacttcagggtggtaggtttctgaagctctcatcaatagactattttagtctttacaaacaatattaccgttcagattcaagattctacaacgctgttttaatgggcgttgcagaaaacttaccacctaaaatccagtatccaagccgatttcagagaaacctaccacttacctaccacttacctaccacccgggtggtaagttgcagacattattaaaaacctcatcagaagcttgttcaaaaatttcaatactcgaaacctaccacctgcgtcccctattatttactactactaataatagcagtataattgatctga"
)


def _run_tests(default_path: str | None = None):
    if default_path:
        with open(default_path, 'r', encoding='utf-8', errors='ignore') as fh:
            file_text = fh.read()
        print(f'Running file: {default_path} (k=9, n=3)')
        res_file = countKmers(file_text, 9, 3)
        items = sorted(res_file.items(), key=lambda x: (-x[1], x[0]))
        print(f'Found {len(items)} k-mers with count >= 3. Top entries:')
        for kmer, cnt in items[:20]:
            print(f'{kmer}: {cnt}')
        print()

    print('Running short example (k=4, n=2)')
    res = countKmers(_short_example_seq, 4, 2)
    print('Result:', res)
    print('\nExpected (order may differ): {\'GCAT\': 3, \'ATGA\': 2, \'TGCA\': 2, \'CATG\': 3}')

    print('\nRunning Vibrio cholerae oriC (k=9, n=3)')
    res2 = countKmers(_vibrio_cholerae_fasta, 9, 3)
    items = sorted(res2.items(), key=lambda x: (-x[1], x[0]))
    print(f'Found {len(items)} k-mers with count >= 3. Top entries:')
    for kmer, cnt in items[:20]:
        print(f'{kmer}: {cnt}')


def _parse_args(argv=None):
    parser = argparse.ArgumentParser(description='Count k-mers in a DNA sequence (local FASTA/plain).')
    parser.add_argument('--path', help='Local path to FASTA/plain file to analyze')
    parser.add_argument('--k', type=int, default=9, help='k-mer length (default: 9)')
    parser.add_argument('--n', type=int, default=3, help='Minimum count threshold (default: 3)')
    return parser.parse_args(argv)


def _run_cli(argv=None):
    args = _parse_args(argv)
    if not args.path:
        _run_tests()
        return
    with open(args.path, 'r', encoding='utf-8', errors='ignore') as fh:
        text = fh.read()
    res = countKmers(text, args.k, args.n)
    items = sorted(res.items(), key=lambda x: (-x[1], x[0]))
    print(f'Analyzed file: {args.path}\nFound {len(items)} k-mers with count >= {args.n}. Top 20:')
    for kmer, cnt in items[:20]:
        print(f'{kmer}: {cnt}')


if __name__ == '__main__':
    _run_cli()
