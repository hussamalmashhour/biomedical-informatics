#!/usr/bin/env python3
"""Submission test for Exercise 2 - Contigs."""

import sys
import os

# Add parent directory to path for config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from contigs import contigs, read_kmers
from config import build_test_url

def main():
    """Run test and generate submission."""
    folder = os.path.dirname(__file__)
    kmers_path = os.path.join(folder, '10mers.txt')
    
    print("=" * 70)
    print("EXERCISE 2: Contigs")
    print("=" * 70)
    
    # Load k-mers
    kmers = read_kmers(kmers_path)
    k = len(kmers[0])
    
    print(f"\nInput:")
    print(f"  File: 10mers.txt")
    print(f"  Number of k-mers: {len(kmers)}")
    print(f"  K-mer length: {k}")
    
    # Find contigs
    print("\nFinding contigs...")
    result = contigs(kmers)
    
    print(f"\nContigs found: {len(result)}")
    
    if result:
        lengths = sorted([len(c) for c in result])
        
        print(f"\nContig details:")
        for i, contig in enumerate(result):
            print(f"  {i+1}. Length {len(contig):3d}: {contig[:60]}{'...' if len(contig) > 60 else ''}")
        
        print(f"\nStatistics:")
        print(f"  Lengths: {lengths}")
        print(f"  Total length: {sum(lengths)} bp")
        
        # Save to file
        output_path = os.path.join(folder, 'contigs.txt')
        with open(output_path, 'w') as f:
            for c in result:
                f.write(c + "\n")
        print(f"\nSaved to: {output_path}")
        
        # Format response - the exercise asks for a list of contigs
        print(f"\nResponse format: List of {len(result)} contigs")
        
        # Generate submission URL
        url = build_test_url(session=3, exercise=2, response=result)
        
        print("\n" + "=" * 70)
        print("SUBMISSION URL:")
        print(url)
        print("=" * 70)
        
        # Additional info
        print(f"\nAnswer:")
        print(f"  Number of contigs: {len(result)}")
        print(f"  Lengths: {lengths}")

if __name__ == '__main__':
    main()
