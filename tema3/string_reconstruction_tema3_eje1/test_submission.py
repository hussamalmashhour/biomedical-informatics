#!/usr/bin/env python3
"""Submission test for Exercise 1 - String Reconstruction."""

import sys
import os

# Add parent directory to path for config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from string_reconstruction import stringReconstruction, read_kmers
from config import build_test_url

def main():
    """Run test and generate submission."""
    folder = os.path.dirname(__file__)
    kmers_path = os.path.join(folder, '10mers.txt')
    
    print("=" * 70)
    print("EXERCISE 1: String Reconstruction")
    print("=" * 70)
    
    # Load k-mers
    kmers = read_kmers(kmers_path)
    k = len(kmers[0])
    
    print(f"\nInput:")
    print(f"  File: 10mers.txt")
    print(f"  Number of k-mers: {len(kmers)}")
    print(f"  K-mer length: {k}")
    
    # Reconstruct
    print("\nReconstructing sequence...")
    result = stringReconstruction(kmers)
    
    print(f"\nReconstructed sequence:")
    print(f"  Length: {len(result)} bp")
    print(f"  First 100: {result[:100]}")
    print(f"  Last 100:  {result[-100:]}")
    
    # Save to file
    output_path = os.path.join(folder, 'reconstructed_sequence.txt')
    with open(output_path, 'w') as f:
        f.write(result)
    print(f"\nSaved to: {output_path}")
    
    # Generate submission URL
    url = build_test_url(session=3, exercise=1, response=result)
    
    print("\n" + "=" * 70)
    print("SUBMISSION URL:")
    print(url)
    print("=" * 70)
    
    # Additional info
    print(f"\nResponse format: Complete DNA sequence (string)")
    print(f"Response length: {len(result)} characters")

if __name__ == '__main__':
    main()
