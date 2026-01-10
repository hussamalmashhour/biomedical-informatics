#!/usr/bin/env python3
"""Custom examples for find_motif"""

from find_motif import find_motif

# Example 1: Finding "ACGT" with different mismatch levels
print("=" * 60)
print("EXAMPLE 1: Finding ACGT with varying mismatches")
print("=" * 60)

seq1 = "AAAAACGTTTTTGCGTAAAAATGTCCCC"
motif1 = "ACGT"

print(f"Sequence: {seq1}")
print(f"Motif:    {motif1}")
print()

for d in [0, 1, 2]:
    hits = find_motif(motif1, seq1, d)
    print(f"d={d} (exact={d==0}): Found {len(hits)} matches")
    for pos in sorted(hits):
        match = hits[pos]
        mismatches = sum(1 for a, b in zip(match, motif1) if a != b)
        print(f"  Position {pos:2d}: {match} ({mismatches} mismatches)")
    print()

# Example 2: Finding DnaA box pattern
print("=" * 60)
print("EXAMPLE 2: Finding DnaA box variants")
print("=" * 60)

seq2 = "ATGATCAAGATGATCAAGATGATCAAG"
motif2 = "ATGATCAAG"

print(f"Sequence: {seq2}")
print(f"Motif:    {motif2} (9-mer DnaA box)")
print()

hits = find_motif(motif2, seq2, d=1)
print(f"With d=1: Found {len(hits)} matches")
for pos in sorted(hits):
    match = hits[pos]
    mismatches = sum(1 for a, b in zip(match, motif2) if a != b)
    marker = "✓ EXACT" if mismatches == 0 else f"✗ {mismatches} diff"
    print(f"  Position {pos:2d}: {match} [{marker}]")

# Example 3: No matches
print("\n" + "=" * 60)
print("EXAMPLE 3: When nothing matches")
print("=" * 60)

seq3 = "AAAAAAAAAA"
motif3 = "GCGCGC"

hits = find_motif(motif3, seq3, d=1)
print(f"Searching for {motif3} in {seq3} with d=1")
print(f"Result: {len(hits)} matches (too many mismatches)")
