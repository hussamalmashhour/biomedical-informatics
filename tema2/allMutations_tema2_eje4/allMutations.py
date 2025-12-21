#!/usr/bin/env python3
"""Count unique k-mers including all mutations within d mismatches.

The allMutations function extracts all k-mers from a sequence and then
generates all possible mutations for each k-mer (up to d mismatches).
It returns the count of unique k-mers across all mutations.

Usage:
    python allMutations.py
    
    Runs built-in test examples and tests on FASTA files.
"""

import os
from mutations import mutationsEqualOrLess


def read_fasta_sequences(path):
    """Read sequences from a FASTA file."""
    sequences = []
    current_header = None
    current_seq = []
    
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if current_seq:
                    sequences.append({
                        'header': current_header,
                        'sequence': ''.join(current_seq).upper()
                    })
                current_header = line[1:]
                current_seq = []
            else:
                current_seq.append(line)
        
        if current_seq:
            sequences.append({
                'header': current_header,
                'sequence': ''.join(current_seq).upper()
            })
    
    return sequences


def allMutations(seq, k, d):
    """Count unique k-mers in seq including all mutations with up to d mismatches.
    
    Args:
        seq: DNA sequence string
        k: k-mer length
        d: maximum allowed mismatches per k-mer
    
    Returns:
        Number of unique k-mers (including all mutations).
    
    Example:
        seq = "ACGTACGT"
        k = 3
        d = 1
        Result: total unique 3-mers within 1 mismatch from any 3-mer in seq
    """
    letters = "ACGT"
    unique_kmers = set()
    
    # Extract all k-mers from the sequence
    for i in range(len(seq) - k + 1):
        kmer = seq[i:i + k].upper()
        
        # Generate all mutations (including the original) up to d mismatches
        mutated_kmers = mutationsEqualOrLess(kmer, letters, d)
        
        # Add all mutations to the set
        unique_kmers.update(mutated_kmers)
    
    return len(unique_kmers)


def test_examples():
    """Test allMutations with example cases."""
    print('--- Test Examples ---\n')
    
    # Example 1: Simple case
    seq1 = "ACGTACGT"
    k1 = 3
    d1 = 0
    result1 = allMutations(seq1, k1, d1)
    print(f'Test 1: seq={seq1}, k={k1}, d={d1}')
    print(f'Result: {result1}')
    print(f'Expected: 6 (unique 3-mers: ACG, CGT, GTA, TAC, ACG, CGT -> 6 unique)')
    
    # Example 2: With 1 mismatch
    seq2 = "AC"
    k2 = 2
    d2 = 1
    result2 = allMutations(seq2, k2, d2)
    print(f'\nTest 2: seq={seq2}, k={k2}, d={d2}')
    print(f'Result: {result2}')
    # Original: AC
    # Mutations (1 mismatch): CC, GC, TC, AA, AG, AT
    # Total: AC, CC, GC, TC, AA, AG, AT = 7
    print(f'Expected: ~15 (AC and all 1-mismatch variants)')
    
    # Example 3: Longer sequence with mutations
    seq3 = "AAAA"
    k3 = 2
    d3 = 1
    result3 = allMutations(seq3, k3, d3)
    print(f'\nTest 3: seq={seq3}, k={k3}, d={d3}')
    print(f'Result: {result3}')
    print(f'Expected: All 2-mers within 1 mismatch of AA and variations')
    
    print()


def main():
    test_examples()
    
    # More realistic example
    print('--- Realistic Example ---')
    seq = "ATCGATCGATCG"
    k = 3
    d = 1
    result = allMutations(seq, k, d)
    print(f'Sequence: {seq}')
    print(f'k={k}, d={d}')
    print(f'Unique k-mers (including mutations): {result}')
    
    # Test with FASTA file
    fasta_path = os.path.join(os.path.dirname(__file__), 'mitDNAprimates.fasta')
    if os.path.exists(fasta_path):
        print('\n--- Test with mitDNAprimates.fasta ---\n')
        sequences = read_fasta_sequences(fasta_path)
        
        k = 9
        d = 1
        
        for seq_data in sequences:
            header = seq_data['header']
            seq = seq_data['sequence']
            result = allMutations(seq, k, d)
            print(f'{header}:')
            print(f'  Sequence length: {len(seq)} bp')
            print(f'  Unique {k}-mers (d={d}): {result}')
            print()


if __name__ == '__main__':
    main()
