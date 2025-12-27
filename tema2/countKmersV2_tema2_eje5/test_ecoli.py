#!/usr/bin/env python3
"""Test countKmersV2 with E. coli oriC sequence."""

from countKmersV2 import countKmersV2

# Read E. coli sequence
path = 'E-coli.txt'
with open(path, 'r') as f:
    text = f.read()

# Clean sequence
lines = [ln.strip() for ln in text.splitlines() if not ln.startswith('>')]
seq = ''.join(lines).upper()
seq = ''.join(ch for ch in seq if ch in 'ACGT')

# Use 500 bp window starting at minSkew position (from exercise 1.4)
mins_start = 3923620
window_seq = seq[mins_start:mins_start + 500]

# Test with k=9, d=1, n=4 (as mentioned in exercise)
k = 9
d = 1
n = 4
result = countKmersV2(window_seq, d, k, n)

print(f'E. coli oriC window test:')
print(f'Window start: {mins_start}')
print(f'Window length: {len(window_seq)}')
print(f'k={k}, d={d}, n={n}')
print(f'Result: {len(result)} k-mers found')
print(f'Type: {type(result)}')
print()
print('Top 20 k-mers by frequency:')
sorted_kmers = sorted(result.items(), key=lambda x: (-x[1], x[0]))
for kmer, count in sorted_kmers[:20]:
    print(f'  {kmer}: {count}')

print()
print(f'Full result dictionary for submission:')
print(result)
