#!/usr/bin/env python3
"""Test countKmersV2 with the example from the exercise."""

from countKmersV2 import countKmersV2, reverse_complement

# Test case from exercise
print("=" * 60)
print("Test 1 - Example from exercise:")
print("=" * 60)

test_seq = "AACAAGCTGATAAACATTTAAAGAG"
k = 5
d = 1
n = 4

result = countKmersV2(test_seq, d, k, n)

print(f"Sequence: {test_seq}")
print(f"k={k}, d={d}, n={n}")
print(f"\nResult ({len(result)} k-mers):")
print(result)

# Expected output from exercise
expected = {
    'AAAAA': 4, 'CTTTT': 4, 'AACAG': 4, 'TTTAA': 5, 'TAAAA': 5,
    'TTAAT': 4, 'TTGAA': 4, 'GTTAA': 4, 'ATTAA': 4, 'TTCAA': 4,
    'TTAAC': 4, 'TTATA': 4, 'TTAAA': 5, 'TTTTA': 5, 'TATAA': 4,
    'CTGTT': 4, 'AAAAG': 4, 'TTTTT': 4
}

print(f"\nExpected ({len(expected)} k-mers):")
print(expected)

# Compare
print("\n" + "=" * 60)
print("Comparison:")
print("=" * 60)

all_kmers = sorted(set(result.keys()) | set(expected.keys()))
matches = 0
mismatches = 0

for kmer in all_kmers:
    exp = expected.get(kmer, 0)
    act = result.get(kmer, 0)
    match = "✓" if exp == act else "✗"
    if exp == act and exp > 0:
        matches += 1
    elif exp != act:
        mismatches += 1
        print(f"{kmer}: Expected={exp}, Actual={act} {match}")

print(f"\nMatches: {matches}")
print(f"Mismatches: {mismatches}")

if matches == len(expected) and len(result) == len(expected):
    print("\n✅ TEST PASSED!")
else:
    print("\n❌ TEST FAILED")
    print(f"Missing k-mers: {set(expected.keys()) - set(result.keys())}")
    print(f"Extra k-mers: {set(result.keys()) - set(expected.keys())}")

# Test reverse complement
print("\n" + "=" * 60)
print("Test 2 - Reverse complement check:")
print("=" * 60)
rc_seq = "ATCG"
rc_test = reverse_complement(rc_seq)
print(f"Original: {rc_seq}")
print(f"Reverse complement: {rc_test}")
print(f"Reverse complement of reverse complement: {reverse_complement(rc_test)}")
print(f"Should be back to original: {reverse_complement(rc_test) == rc_seq}")

# Test with simple sequence
print("\n" + "=" * 60)
print("Test 3 - Simple verification:")
print("=" * 60)
small_seq = "ATCGAT"
small_result = countKmersV2(small_seq, d=0, k=3, n=1)
print(f"Sequence: {small_seq}, k=3, d=0, n=1")
print(f"Result: {small_result}")
print(f"K-mers in sequence: ATC, TCG, CGA, GAT")
print(f"ATC RC=GAT (same), TCG RC=CGA (same)")
print(f"Expected: ATC(2), TCG(2) since we count RC together")
