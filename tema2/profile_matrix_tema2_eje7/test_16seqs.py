#!/usr/bin/env python3
"""Test with 16 sequences."""

from profile_matrix import read_motifs, profile
import sys
sys.path.insert(0, 'd:\\Biomedical Informatics')
from config import build_test_url

motifs = read_motifs('nfkbMotifs_16seqs.txt')
print(f'Number of sequences: {len(motifs)}')

result = profile(motifs, Laplace=True)
print(f'Dictionary length: {len(result)}')
print(f'A[0] = {result["A"][0]:.6f}')
print(f'Expected: 0.15')

if abs(result["A"][0] - 0.15) < 0.001:
    print('\n✓✓✓ PERFECT MATCH!')
else:
    print(f'\n✗ Not matching. Difference: {abs(result["A"][0] - 0.15):.6f}')

print('\nFull result:')
print(result)

print('\n' + '=' * 70)
print('SUBMISSION URL')
print('=' * 70)
url = build_test_url(2, 7, result)
print(url)
