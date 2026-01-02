#!/usr/bin/env python3
"""Try submitting as list of lists."""

from profile_matrix import read_motifs, profile
import sys
sys.path.insert(0, 'd:\\Biomedical Informatics')
from config import build_test_url

motifs = read_motifs('nfkbMotifs_16seqs.txt')
result_dict = profile(motifs, Laplace=True)

# Convert to list of lists [A_row, C_row, G_row, T_row]
result_list = [result_dict['A'], result_dict['C'], result_dict['G'], result_dict['T']]

print("Submitting as LIST OF LISTS format:")
print("[[A_values], [C_values], [G_values], [T_values]]")
print(f"\nFirst values: A={result_list[0][0]}, C={result_list[1][0]}, G={result_list[2][0]}, T={result_list[3][0]}")
print(f"A[0] = {result_list[0][0]} (expected 0.15) ✓")

url = build_test_url(2, 7, result_list)
print("\n" + "=" * 70)
print("SUBMISSION URL (LIST FORMAT)")
print("=" * 70)
print(url)
