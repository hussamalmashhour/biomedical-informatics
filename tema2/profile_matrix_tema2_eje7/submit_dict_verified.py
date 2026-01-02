#!/usr/bin/env python3
"""Submit with explicit dictionary format."""

from profile_matrix import read_motifs, profile
import sys
sys.path.insert(0, 'd:\\Biomedical Informatics')
from config import build_test_url

motifs = read_motifs('nfkbMotifs_16seqs.txt')
result = profile(motifs, Laplace=True)

print("Result dictionary:")
print(f"Type: {type(result)}")
print(f"Keys: {list(result.keys())}")
print(f"Length: {len(result)}")
print(f"A[0] = {result['A'][0]}")
print()
print(result)

# Double check the structure
print("\n" + "=" * 70)
print("VERIFICATION")
print("=" * 70)
print(f"Is dict? {isinstance(result, dict)}")
print(f"Has 4 keys? {len(result) == 4}")
print(f"Has A,C,G,T? {set(result.keys()) == {'A', 'C', 'G', 'T'}}")
print(f"A[0] == 0.15? {result['A'][0] == 0.15}")
print(f"All values are lists? {all(isinstance(v, list) for v in result.values())}")

url = build_test_url(2, 7, result)
print("\n" + "=" * 70)
print("SUBMISSION URL (DICT FORMAT)")
print("=" * 70)
print(url)

print("\n" + "=" * 70)
print("ALTERNATIVE: Manual URL construction")
print("=" * 70)
# Try building URL manually with explicit dict format
import urllib.parse
response_str = str(result)
encoded = urllib.parse.quote(response_str)
manual_url = f"https://cpg3.der.usal.es/eval/test?session=2&exercise=7&response={encoded}&id=Z2256773H"
print(manual_url)
