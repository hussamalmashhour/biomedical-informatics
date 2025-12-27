#!/usr/bin/env python3
"""Test allMutations with E. coli oriC sequence."""

from allMutations import allMutations

# Read E. coli sequence
path = 'E-coli.txt'
with open(path, 'r') as f:
    text = f.read()

# Clean sequence
lines = [ln.strip() for ln in text.splitlines() if not ln.startswith('>')]
seq = ''.join(lines).upper()
seq = ''.join(ch for ch in seq if ch in 'ACGT')

# Use 500 bp window starting at minSkew position
mins_start = 3923620
window_seq = seq[mins_start:mins_start + 500]

# Test with k=9, d=3
k = 9
d = 3
result = allMutations(window_seq, k, d)

print(f'E. coli oriC window test:')
print(f'Window start: {mins_start}')
print(f'Window length: {len(window_seq)}')
print(f'k={k}, d={d}')
print(f'Result: {result}')
print(f'Type: {type(result)}')
