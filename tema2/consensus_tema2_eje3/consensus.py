#!/usr/bin/env python3
"""Compute consensus sequence from aligned DNA sequences.

The consensus sequence shows the most frequent base at each position.
Ties are broken alphabetically (A < C < G < T).
Invalid/missing positions use '*' as wildcard.

Consensus strength is visualized with case:
  - UPPERCASE: base appears in >50% of sequences (strong)
  - lowercase: base appears in <=50% of sequences (weak)

Usage:
    python consensus.py
    
    Reads mitDNAprimates.fasta from local directory and computes consensus.
"""

import os
from collections import Counter


def consensus(seqs, show_strength=True):
    """Compute consensus sequence from aligned DNA sequences.
    
    Args:
        seqs: list of DNA sequence strings (all must be same length).
        show_strength: if True, use case to reflect consensus strength
                       (uppercase >50%, lowercase <=50%).
    
    Returns:
        Consensus sequence as string. Use '*' for positions with no valid bases.
    
    Raises:
        ValueError: if sequences have different lengths.
    """
    if not seqs:
        return ""
    
    # Validate all sequences are the same length
    first_len = len(seqs[0])
    if not all(len(seq) == first_len for seq in seqs):
        raise ValueError(f"All sequences must be the same length. Got lengths: {[len(seq) for seq in seqs]}")
    
    length = first_len
    result = []
    for i in range(length):
        column = [seq[i].upper() for seq in seqs]
        counts = Counter(nuc for nuc in column if nuc in "ACGT")
        if not counts:
            result.append('*')
            continue
        
        max_count = max(counts.values())
        max_bases = sorted([base for base, count in counts.items() if count == max_count])
        consensus_base = max_bases[0]
        
        # Calculate strength: frequency of consensus base
        freq = max_count / len(column)
        
        # Apply case based on strength if requested
        if show_strength:
            if freq > 0.5:
                result.append(consensus_base.upper())
            else:
                result.append(consensus_base.lower())
        else:
            result.append(consensus_base.upper())
    
    return "".join(result)


def clean_sequence(text):
    """Extract sequence from raw or FASTA text."""
    if not text:
        return ""
    lines = text.splitlines()
    if any(line.startswith('>') for line in lines):
        lines = [ln for ln in lines if not ln.startswith('>')]
    seq = ''.join(lines)
    return ''.join(ch for ch in seq if ch.isalpha()).upper()


def read_fasta_sequences(path):
    """Read all sequences from a FASTA file. Handle gaps ('-') as 'N'."""
    with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
        text = fh.read()
    sequences = []
    current_seq = []
    for line in text.splitlines():
        if line.startswith('>'):
            if current_seq:
                sequences.append(''.join(current_seq))
                current_seq = []
        else:
            # Keep A/C/G/T, convert gaps and unknowns to 'N'
            cleaned = ''.join(ch.upper() if ch in 'ACGT' else 'N' for ch in line if ch.isalpha() or ch == '-')
            if cleaned:
                current_seq.append(cleaned)
    if current_seq:
        sequences.append(''.join(current_seq))
    return sequences


def test_examples():
    """Test consensus with provided examples."""
    print('--- Test Examples ---')
    
    # Example 1: simple case with clear consensus
    test1 = ['ATTCTGGA', 'AATCCAGA', 'ATCCAGAA']
    try:
        result1 = consensus(test1, show_strength=False)
        print(f'Test 1: {test1}')
        print(f'Result: {result1}')
        print(f'Expected: ATTCAGGA or similar (most frequent bases per position)')
    except ValueError as e:
        print(f'Test 1 ERROR: {e}')
    
    # Example 2: with strength indicator
    test2 = ['ACGT', 'ACGT', 'AGGT']
    try:
        result2 = consensus(test2, show_strength=True)
        print(f'\nTest 2: {test2}')
        print(f'Result (with strength): {result2}')
        print('Expected: ACGT or similar (uppercase for >50%, lowercase for <=50%)')
    except ValueError as e:
        print(f'Test 2 ERROR: {e}')
    
    # Example 3: length mismatch (should raise error)
    test3 = ['ACGT', 'ACGTAA']
    print(f'\nTest 3 (length mismatch): {test3}')
    try:
        result3 = consensus(test3)
        print(f'Result: {result3}')
    except ValueError as e:
        print(f'Expected ERROR: {e}')
    
    print()


def main():
    # Read mitochondrial primate DNA sequences
    fasta_path = os.path.join(os.path.dirname(__file__), 'mitDNAprimates.fasta')
    seqs = read_fasta_sequences(fasta_path)
    if not seqs:
        print('No sequences found.')
        return
    print(f'Read {len(seqs)} sequences, each length {len(seqs[0])}')
    
    try:
        # Compute consensus with strength indicators
        result = consensus(seqs, show_strength=True)
    except ValueError as e:
        print(f'ERROR: {e}')
        return
    
    print(f'Consensus sequence length: {len(result)}')
    print(f'Consensus: {result[:100]}...')
    
    # Statistics
    wildcard_count = result.count('*')
    lowercase_count = sum(1 for ch in result if ch.islower())
    uppercase_count = sum(1 for ch in result if ch.isupper())
    
    print(f'Wildcard positions (*): {wildcard_count}')
    print(f'Strong consensus (uppercase): {uppercase_count}')
    print(f'Weak consensus (lowercase): {lowercase_count}')


if __name__ == '__main__':
    test_examples()
    main()
