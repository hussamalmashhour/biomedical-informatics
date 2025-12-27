#!/usr/bin/env python3
"""Test submission for Exercise 10 - Greedy Motif Search."""

import sys
import os

# Add parent directory to path for config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from greedy_motif_search import greedyMotifSearch, read_sequences, score
from config import build_test_url

def main():
    """Run test and generate submission."""
    # Load sequences
    folder = os.path.dirname(__file__)
    path = os.path.join(folder, 'seqs4mut.txt')
    sequences = read_sequences(path)
    
    k = 15
    
    print("=" * 70)
    print("EXERCISE 10: Greedy Motif Search")
    print("=" * 70)
    
    print(f"\nInput:")
    print(f"  Number of sequences: {len(sequences)}")
    print(f"  Sequence length: {len(sequences[0])} bp")
    print(f"  Motif length k: {k}")
    
    # Run greedy motif search
    result = greedyMotifSearch(sequences, k)
    
    print(f"\nMotifs found:")
    for i, motif in enumerate(result):
        print(f"  Seq {i}: {motif}")
    
    motif_score = score(result)
    print(f"\nScore: {motif_score}")
    
    # Build consensus
    consensus = []
    for pos in range(k):
        counts = {'A': 0, 'C': 0, 'G': 0, 'T': 0}
        for motif in result:
            if pos < len(motif):
                counts[motif[pos]] += 1
        consensus.append(max(counts, key=counts.get))
    consensus_str = ''.join(consensus)
    
    print(f"Consensus: {consensus_str}")
    
    # Format response as list of motifs
    print(f"\nResponse format: {result}")
    
    # Generate submission URL
    url = build_test_url(session=2, exercise=10, response=result)
    
    print("\n" + "=" * 70)
    print("SUBMISSION URL:")
    print(url)
    print("=" * 70)

if __name__ == '__main__':
    main()
