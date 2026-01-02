#!/usr/bin/env python3
"""Generate submission with full precision."""

from profile_matrix import read_motifs, profile
import sys
sys.path.insert(0, 'd:\\Biomedical Informatics')
from config import build_test_url

motifs = read_motifs('nfkbMotifs_16seqs.txt')
result = profile(motifs, Laplace=True)

print("Result with FULL precision (no rounding):")
print(result)
print(f"\nA[0] = {result['A'][0]}")
print(f"Dictionary length: {len(result)}")

# Check the exact values
print("\nFirst value analysis:")
print(f"  A[0] = {result['A'][0]} (expected 0.15)")
print(f"  3/20 = {3/20}")
print(f"  Match: {result['A'][0] == 0.15}")

url = build_test_url(2, 7, result)
print("\n" + "=" * 70)
print("SUBMISSION URL (FULL PRECISION)")
print("=" * 70)
print(url)
