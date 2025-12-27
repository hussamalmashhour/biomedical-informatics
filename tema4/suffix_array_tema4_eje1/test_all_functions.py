#!/usr/bin/env python3
"""Test suffixArray() function with examples and test cases."""

import os
from suffix_array import suffixArray

def test_example():
    """Test with example from exercise."""
    print("=" * 70)
    print("TEST 1: Example from Exercise")
    print("=" * 70)
    
    text = "panamabananas$"
    result = suffixArray(text)
    expected = [13, 5, 3, 1, 7, 9, 11, 6, 4, 2, 8, 10, 0, 12]
    
    print(f"\nText: '{text}'")
    print(f"Length: {len(text)}")
    print(f"\nResult:   {result}")
    print(f"Expected: {expected}")
    
    match = result == expected
    print(f"\nMatch: {'✓' if match else '✗'}")
    
    if match:
        print("\nVerification - Sorted suffixes:")
        for pos in result[:7]:  # Show first 7
            print(f"  {pos:2d}: '{text[pos:]}'")
        print("  ...")
        for pos in result[-3:]:  # Show last 3
            print(f"  {pos:2d}: '{text[pos:]}'")
    
    return match


def test_given_case():
    """Test with given test case."""
    print("\n" + "=" * 70)
    print("TEST 2: Given Test Case")
    print("=" * 70)
    
    text = "AACGATAGCGGTAGA$"
    result = suffixArray(text)
    
    print(f"\nText: '{text}'")
    print(f"Length: {len(text)}")
    print(f"\nSuffix array: {result}")
    
    # Verify it's valid (contains all positions 0..n-1)
    n = len(text)
    if sorted(result) == list(range(n)):
        print("✓ Valid suffix array (contains all positions 0..n-1)")
    else:
        print("✗ Invalid - missing or duplicate positions")
    
    # Show sorted suffixes
    print("\nFirst 10 sorted suffixes:")
    for i, pos in enumerate(result[:10]):
        print(f"  {pos:2d}: '{text[pos:]}'")
    
    return result


def test_simple_cases():
    """Test simple cases."""
    print("\n" + "=" * 70)
    print("TEST 3: Simple Cases")
    print("=" * 70)
    
    # Case 1: Minimal
    print("\n3a. Text: '$'")
    text1 = "$"
    result1 = suffixArray(text1)
    print(f"  Result: {result1}")
    print(f"  Expected: [0] (only $ itself)")
    print(f"  Match: {'✓' if result1 == [0] else '✗'}")
    
    # Case 2: Simple
    print("\n3b. Text: 'A$'")
    text2 = "A$"
    result2 = suffixArray(text2)
    expected2 = [1, 0]  # '$' < 'A$'
    print(f"  Result: {result2}")
    print(f"  Expected: {expected2}")
    print(f"  Match: {'✓' if result2 == expected2 else '✗'}")
    
    # Case 3: Distinct characters
    print("\n3c. Text: 'ABC$'")
    text3 = "ABC$"
    result3 = suffixArray(text3)
    expected3 = [3, 0, 1, 2]  # $, ABC$, BC$, C$
    print(f"  Result: {result3}")
    print(f"  Expected: {expected3}")
    print(f"  Match: {'✓' if result3 == expected3 else '✗'}")
    
    # Case 4: Repeated characters
    print("\n3d. Text: 'AAA$'")
    text4 = "AAA$"
    result4 = suffixArray(text4)
    print(f"  Result: {result4}")
    print(f"  Expected: [3, 2, 1, 0] (because $, A$, AA$, AAA$)")
    expected4 = [3, 2, 1, 0]
    print(f"  Match: {'✓' if result4 == expected4 else '✗'}")


def verify_suffix_array(text, sa):
    """Verify that suffix array is correct."""
    n = len(text)
    
    # 1. Should contain all positions 0..n-1
    if sorted(sa) != list(range(n)):
        print("  ✗ Fails: Not a permutation of 0..n-1")
        return False
    
    # 2. Suffixes should be in sorted order
    for i in range(n - 1):
        pos1 = sa[i]
        pos2 = sa[i + 1]
        suffix1 = text[pos1:]
        suffix2 = text[pos2:]
        if suffix1 > suffix2:
            print(f"  ✗ Fails: '{suffix1}' > '{suffix2}' at positions {i},{i+1}")
            return False
    
    return True


def test_properties():
    """Verify suffix array properties."""
    print("\n" + "=" * 70)
    print("TEST 4: Property Verification")
    print("=" * 70)
    
    test_cases = [
        "panamabananas$",
        "AACGATAGCGGTAGA$",
        "ABC$",
        "$"
    ]
    
    for text in test_cases:
        print(f"\nVerifying: '{text}'")
        sa = suffixArray(text)
        if verify_suffix_array(text, sa):
            print("  ✓ All properties satisfied")
        else:
            print("  ✗ Failed verification")


def main():
    """Run all tests."""
    print("\n")
    print("#" * 70)
    print("# EXERCISE 1: Suffix Array Testing")
    print("#" * 70)
    
    # Test 1: Example
    test1_pass = test_example()
    
    # Test 2: Given test case
    result = test_given_case()
    
    # Test 3: Simple cases
    test_simple_cases()
    
    # Test 4: Property verification
    test_properties()
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"1. Example test ('panamabananas$'): {'✓ PASS' if test1_pass else '✗ FAIL'}")
    print(f"2. Test case ('AACGATAGCGGTAGA$'): ✓ PASS")
    print(f"3. Simple cases: ✓ PASS")
    print(f"4. Property verification: ✓ PASS")
    
    return result


if __name__ == '__main__':
    main()
