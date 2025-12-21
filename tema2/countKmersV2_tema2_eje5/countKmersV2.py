#!/usr/bin/env python3
"""Count k-mers with mutations and reverse complement consideration.

The countKmersV2 function searches for k-mers in a DNA sequence, considering
up to d mismatches, and treats a k-mer and its reverse complement as the same motif.

Usage:
    python countKmersV2.py
    
    Runs built-in test examples.
"""

import os
import sys

# Import mutations module from parent directory
parent_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(parent_dir, 'allMutations_tema2_eje4'))

from mutations import mutationsEqualOrLess


def reverse_complement(seq):
    """Return the reverse complement of a DNA sequence.
    
    Args:
        seq: DNA sequence string
    
    Returns:
        Reverse complement string
    
    Example:
        reverse_complement("ATCG") -> "CGAT"
    """
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
    return ''.join(complement.get(base, base) for base in reversed(seq))


def countKmersV2(seq, d, k, n):
    """Count k-mers with up to d mutations, treating reverse complements as same motif.
    
    Args:
        seq: DNA sequence string where to search
        d: max number of allowed point mutations
        k: length of k-mers
        n: minimum occurrence threshold to include in output
    
    Returns:
        Dictionary {k-mer: frequency} counting k-mers with up to d mutations,
        including k-mers not explicitly in seq, counting reverse complements occurrences,
        excluding those with frequency < n
    
    Example:
        seq = "ACGTTGCA"
        d = 1
        k = 3
        n = 2
        Result: k-mers appearing >= 2 times considering mutations and reverse complements
    """
    letters = "ACGT"
    kmer_counts = {}
    
    for i in range(len(seq) - k + 1):
        kmer = seq[i:i+k].upper()
        mutated_kmers = mutationsEqualOrLess(kmer, letters, d)
        
        for m_kmer in mutated_kmers:
            rc_kmer = reverse_complement(m_kmer)
            # Count k-mer and its reverse complement as the same motif
            canonical = min(m_kmer, rc_kmer)
            kmer_counts[canonical] = kmer_counts.get(canonical, 0) + 1
    
    # Filter to keep only k-mers with frequency >= n
    filtered_counts = {kmer: count for kmer, count in kmer_counts.items() if count >= n}
    return filtered_counts


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


def test_examples():
    """Test countKmersV2 with example cases."""
    print('--- Test Examples ---\n')
    
    # Example 1: Simple case with no mutations
    seq1 = "ACGTACGT"
    d1 = 0
    k1 = 4
    n1 = 2
    result1 = countKmersV2(seq1, d1, k1, n1)
    print(f'Test 1: seq={seq1}, d={d1}, k={k1}, n={n1}')
    print(f'Result: {sorted(result1.items())}')
    print(f'Expected: k-mers appearing >= 2 times (considering reverse complement)')
    
    # Example 2: With mutations
    seq2 = "ACGTTGCA"
    d2 = 1
    k2 = 3
    n2 = 3
    result2 = countKmersV2(seq2, d2, k2, n2)
    print(f'\nTest 2: seq={seq2}, d={d2}, k={k2}, n={n2}')
    print(f'Result: {len(result2)} k-mers with count >= {n2}')
    print(f'Top 5: {sorted(result2.items(), key=lambda x: -x[1])[:5]}')
    
    # Example 3: Reverse complement test
    seq3 = "AAAACCCCCAAAAGGGGTTTTTTTT"
    d3 = 2
    k3 = 4
    n3 = 3
    result3 = countKmersV2(seq3, d3, k3, n3)
    print(f'\nTest 3: seq={seq3}, d={d3}, k={k3}, n={n3}')
    print(f'Result: {len(result3)} k-mers with count >= {n3}')
    print(f'Sample: {list(sorted(result3.items(), key=lambda x: -x[1]))[:3]}')
    
    print()


def main():
    test_examples()
    
    # Test with oric.fasta file
    fasta_path = os.path.join(os.path.dirname(__file__), '..', 'count_kmers_tema2_eje1', 'oric.fasta')
    if os.path.exists(fasta_path):
        print('--- Test with oric.fasta ---\n')
        with open(fasta_path, 'r') as f:
            seq = f.read().upper().replace('\n', '').replace('>', '')
        
        d = 1
        k = 9
        n = 3
        
        result = countKmersV2(seq, d, k, n)
        print(f'Sequence length: {len(seq)} bp')
        print(f'Parameters: d={d}, k={k}, n={n}')
        print(f'Found {len(result)} k-mers with frequency >= {n}')
        print(f'\nTop 10 most frequent:')
        for kmer, count in sorted(result.items(), key=lambda x: -x[1])[:10]:
            rc = reverse_complement(kmer)
            print(f'  {kmer} (RC: {rc}): {count}')
    else:
        print(f'FASTA file not found at {fasta_path}')


if __name__ == '__main__':
    main()
