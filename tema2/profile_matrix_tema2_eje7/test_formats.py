#!/usr/bin/env python3
"""Test different output formats."""

from profile_matrix import read_motifs, profile
import sys
sys.path.insert(0, 'd:\\Biomedical Informatics')
from config import build_test_url

motifs = read_motifs('nfkbMotifs_16seqs.txt')
result = profile(motifs, Laplace=True)

print("=" * 70)
print("TESTING DIFFERENT FORMATS")
print("=" * 70)

print("\n1. Current format (dict with string keys):")
print(result)
print(f"   Keys: {list(result.keys())}")
print(f"   Type: {type(result)}")

print("\n2. Dict with sorted keys explicitly:")
sorted_result = {k: result[k] for k in sorted(result.keys())}
print(sorted_result)

print("\n3. As 2D list [[A row], [C row], [G row], [T row]]:")
list_format = [result['A'], result['C'], result['G'], result['T']]
print(list_format)

print("\n4. Maybe they want profile AS A LIST OF ROWS?")
# Like: [[A values], [C values], [G values], [T values]]
profile_list = [result[nt] for nt in 'ACGT']
print(profile_list)

print("\n5. Or as transposed? (columns as rows)")
n = len(result['A'])
transposed = []
for i in range(n):
    transposed.append([result['A'][i], result['C'][i], result['G'][i], result['T'][i]])
print(f"First 3 columns: {transposed[:3]}")

print("\n" + "=" * 70)
print("CHECKING URL FORMAT")
print("=" * 70)

# Check what format_response does
from config import format_response
print("\nFormat 1 (dict):")
print(format_response(result)[:200])

print("\nFormat 4 (list of lists):")
print(format_response(profile_list)[:200])
