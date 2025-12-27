#!/usr/bin/env python3
"""Test and generate submission URL for BWT (Exercise 2)."""

import sys
import os

# Import config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from config import STUDENT_ID, build_test_url

# Import bwt function
sys.path.insert(0, os.path.dirname(__file__))
from bwt import bwt


def main():
    print("=" * 70)
    print("EXERCISE 2: BWT (Burrows-Wheeler Transform) - Submission Test")
    print("=" * 70)
    
    # Test with the test case
    test_text = "AACGATAGCGGTAGA$"
    
    print(f"\nTest case text: '{test_text}'")
    print(f"Length: {len(test_text)}")
    
    # Compute BWT
    bwt_result = bwt(test_text)
    
    print(f"\nBWT (as list): {bwt_result}")
    print(f"BWT (as string): '{''.join(bwt_result)}'")
    print(f"Length: {len(bwt_result)}")
    
    # Verify properties
    print("\n" + "-" * 50)
    print("Verification:")
    
    if len(bwt_result) == len(test_text):
        print(f"✓ Correct length: {len(bwt_result)}")
    else:
        print(f"✗ Wrong length: {len(bwt_result)} ≠ {len(test_text)}")
    
    if sorted(bwt_result) == sorted(test_text):
        print("✓ Same character multiset as original")
    else:
        print("✗ Different characters from original")
    
    # Check that it's a valid BWT ($ should appear)
    if '$' in bwt_result:
        print(f"✓ Contains sentinel '$' at position {bwt_result.index('$')}")
    else:
        print("✗ Missing sentinel '$'")
    
    # Show first few characters of sorted rotations for verification
    print("\n" + "-" * 50)
    print("First 5 sorted rotations (verification):")
    n = len(test_text)
    rotations = [test_text[i:] + test_text[:i] for i in range(n)]
    rotations.sort()
    for i, rot in enumerate(rotations[:5]):
        print(f"  {i}: {rot} → last: '{rot[-1]}'")
    
    # Save to file
    out_path = os.path.join(os.path.dirname(__file__), 'bwt.txt')
    with open(out_path, 'w') as f:
        f.write(''.join(bwt_result))
    print(f"\n✓ Saved BWT to: {out_path}")
    
    # Generate submission URL
    print("\n" + "=" * 70)
    print("SUBMISSION URL")
    print("=" * 70)
    
    # Format response - BWT as a list for JSON
    response = bwt_result
    url = build_test_url(session=4, exercise=2, response=response, student_id=STUDENT_ID)
    
    print(f"\nBWT for '{test_text}':")
    print(f"  As list: {response}")
    print(f"  As string: '{''.join(response)}'")
    print(f"\nSubmission URL:")
    print(url)
    
    print("\n" + "=" * 70)
    print("KEY ALGORITHM POINTS:")
    print("=" * 70)
    print("""
1. BWT = Last column of sorted cyclic rotations matrix
2. Cyclic rotations: text[i:] + text[:i] for i in range(n)
3. Sort all rotations lexicographically
4. Extract last character from each sorted rotation
5. Alternative: BWT[i] = text[(SA[i]-1) % n] using suffix array

Example 'panamabananas$':
- 14 rotations starting with: $pan..., aban..., amab..., etc.
- Last column: ['s','m','n','p','b','n','n','a','a','a','a','a','$','a']
- As string: 'smnpbnnaaaaa$a'

Properties:
- BWT has same length as original text
- BWT has same characters (permutation)
- BWT groups similar characters together (good for compression)
- BWT is reversible (can reconstruct original text)
    """)


if __name__ == "__main__":
    main()
