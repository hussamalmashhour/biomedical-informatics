#!/usr/bin/env python3
"""Try with lowercase keys."""

from profile_matrix import read_motifs, profile
import sys
sys.path.insert(0, 'd:\\Biomedical Informatics')
from config import build_test_url

motifs = read_motifs('nfkbMotifs_16seqs.txt')
result = profile(motifs, Laplace=True)

# Convert to lowercase keys
result_lowercase = {
    'a': result['A'],
    'c': result['C'],
    'g': result['G'],
    't': result['T']
}

print("Result with LOWERCASE keys:")
print(result_lowercase)
print(f"\nKeys: {list(result_lowercase.keys())}")
print(f"a[0] = {result_lowercase['a'][0]}")

url = build_test_url(2, 7, result_lowercase)
print("\n" + "=" * 70)
print("SUBMISSION URL (lowercase keys)")
print("=" * 70)
print(url)
