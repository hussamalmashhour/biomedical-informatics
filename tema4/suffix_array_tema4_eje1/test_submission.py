#!/usr/bin/env python3
"""Submission test for Exercise 1 - Suffix Array."""

import sys
import os

# Add parent directory to path for config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from suffix_array import suffixArray
from config import build_test_url

def main():
    """Run test and generate submission."""
    # Test case from exercise
    text = "AACGATAGCGGTAGA$"
    
    print("=" * 70)
    print("EXERCISE 1: Suffix Array")
    print("=" * 70)
    
    print(f"\nInput:")
    print(f"  Text: '{text}'")
    print(f"  Length: {len(text)}")
    
    # Compute suffix array
    print("\nComputing suffix array...")
    result = suffixArray(text)
    
    print(f"\nSuffix array: {result}")
    print(f"  Length: {len(result)}")
    
    # Verify
    n = len(text)
    if sorted(result) == list(range(n)):
        print("  ✓ Valid (contains all positions 0..n-1)")
    
    # Show sorted suffixes
    print(f"\nSorted suffixes (first 10):")
    for i, pos in enumerate(result[:10]):
        suffix = text[pos:]
        preview = suffix if len(suffix) <= 20 else suffix[:20] + "..."
        print(f"  {i+1:2d}. Position {pos:2d}: '{preview}'")
    
    # Save to file
    folder = os.path.dirname(__file__)
    output_path = os.path.join(folder, 'suffix_array.txt')
    with open(output_path, 'w') as f:
        f.write(' '.join(map(str, result)))
    print(f"\nSaved to: {output_path}")
    
    # Format response
    print(f"\nResponse format: {result}")
    
    # Generate submission URL
    url = build_test_url(session=4, exercise=1, response=result)
    
    print("\n" + "=" * 70)
    print("SUBMISSION URL:")
    print(url)
    print("=" * 70)
    
    # Additional info
    print(f"\nNote: Suffix array for '{text}'")
    print(f"  First element: {result[0]} (position of '$')")
    print(f"  Last element: {result[-1]} (position of last suffix lexicographically)")

if __name__ == '__main__':
    main()
