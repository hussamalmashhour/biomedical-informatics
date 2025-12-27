#!/usr/bin/env python3
"""Test submission for Exercise 11 - Gibbs Sampler."""

import sys
import os

# Add parent directory to path for config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from gibbs_sampler import gibbsSampler, read_sequences
from config import build_test_url

def main():
    """Run test and generate submission."""
    # Load sequences
    folder = os.path.dirname(__file__)
    path = os.path.join(folder, 'secuencias2.txt')
    sequences = read_sequences(path)
    
    k = 8
    N = 100
    runs = 50
    
    print("=" * 70)
    print("EXERCISE 11: Gibbs Sampler")
    print("=" * 70)
    
    print(f"\nInput:")
    print(f"  Number of sequences: {len(sequences)}")
    print(f"  Motif length k: {k}")
    print(f"  Iterations per run N: {N}")
    print(f"  Number of runs: {runs}")
    
    print(f"\nRunning Gibbs Sampler {runs} times...")
    print("(This may take a moment...)")
    
    # Run and get consensus string (NOT list)
    consensus = gibbsSampler(sequences, k, N, num_runs=runs)
    
    print(f"\nConsensus sequence found: {consensus}")
    print(f"Type: {type(consensus).__name__} (should be 'str')")
    print(f"Length: {len(consensus)} bp")
    
    # Format response as consensus string
    print(f"\nResponse format: '{consensus}'")
    
    # Generate submission URL
    url = build_test_url(session=2, exercise=11, response=consensus)
    
    print("\n" + "=" * 70)
    print("SUBMISSION URL:")
    print(url)
    print("=" * 70)
    
    print(f"\nNote: Professor expects:")
    print(f"  - Response type: str (consensus sequence)")
    print(f"  - Target score: ~4")

if __name__ == '__main__':
    main()
