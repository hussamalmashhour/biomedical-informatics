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
    """
    Calculate all possible k-mers from `seq`, including those not explicitly present,
    considering up to `d` point mutations per k-mer.

    Parameters:
    -----------
    seq : str
        DNA sequence (contains only A, C, G, T)
    k : int
        Length of k-mers
    d : int
        Maximum number of mismatches allowed

    Returns:
    --------
    int
        Number of unique k-mers possible (including mutations)
    """
    # Handle edge case
    if k > len(seq):
        return 0
    
    # Initialize an empty set to store unique k-mers
    all_kmer_mutations = set()
    
    # Slide a window of length k over seq to extract each k-mer
    for i in range(len(seq) - k + 1):
        current_kmer = seq[i:i + k].upper()
        
        # Get all possible mutations of that k-mer with up to d mismatches
        mutations_set = mutationsEqualOrLess(current_kmer, d, letters="ACGT")
        
        # Add all returned mutations to all_kmer_mutations set
        all_kmer_mutations.update(mutations_set)
    
    # Return the length of all_kmer_mutations
    return len(all_kmer_mutations)


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
