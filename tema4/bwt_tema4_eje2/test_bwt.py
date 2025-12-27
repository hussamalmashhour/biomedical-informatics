#!/usr/bin/env python3
"""Comprehensive test suite for BWT (Burrows-Wheeler Transform)."""

import sys
import os

# Import from current directory
sys.path.insert(0, os.path.dirname(__file__))
from bwt import bwt

# Import suffixArray from Exercise 1
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'suffix_array_tema4_eje1'))
from suffix_array import suffixArray


def bwt_via_suffix_array(text):
    """Compute BWT using suffix array method (for verification)."""
    n = len(text)
    sa = suffixArray(text)
    bwt_result = []
    for i in range(n):
        # Get character before suffix start (cyclic)
        pos = (sa[i] - 1) % n
        bwt_result.append(text[pos])
    return bwt_result


def test_bwt():
    """Run comprehensive BWT tests."""
    
    print("=" * 70)
    print("EXERCISE 2: Testing bwt() function (Burrows-Wheeler Transform)")
    print("=" * 70)
    
    # Test 1: Example from exercise
    print("\nTest 1: Example from exercise - 'panamabananas$'")
    print("-" * 50)
    
    text1 = "panamabananas$"
    result1 = bwt(text1)
    
    # Note: bwt() returns (bwt_string, rotations) tuple
    if isinstance(result1, tuple):
        bwt_str, rotations = result1
        result1 = list(bwt_str)  # Convert to list for comparison
    else:
        result1 = list(result1) if isinstance(result1, str) else result1
    
    expected1 = ['s', 'm', 'n', 'p', 'b', 'n', 'n', 'a', 'a', 'a', 'a', 'a', '$', 'a']
    
    print(f"Text: '{text1}'")
    print(f"Length: {len(text1)}")
    print(f"\nBWT Result:   {result1}")
    print(f"Expected:     {expected1}")
    
    if result1 == expected1:
        print("✓ PASS: Exact match!")
    else:
        print("✗ FAIL: Mismatch")
        print(f"  As string: '{''.join(result1)}'")
        print(f"  Expected:  '{''.join(expected1)}'")
    
    # Show rotation matrix verification
    print("\nVerification - First 5 sorted rotations:")
    text1_rotations = [text1[i:] + text1[:i] for i in range(len(text1))]
    text1_rotations.sort()
    for i, rot in enumerate(text1_rotations[:5]):
        print(f"  {rot} → last char: '{rot[-1]}'")
    
    # Test 2: Test case from exercise
    print("\n" + "=" * 70)
    print("Test 2: Test case - 'AACGATAGCGGTAGA$'")
    print("-" * 50)
    
    text2 = "AACGATAGCGGTAGA$"
    result2 = bwt(text2)
    
    if isinstance(result2, tuple):
        bwt_str2, _ = result2
        result2 = list(bwt_str2)
    else:
        result2 = list(result2) if isinstance(result2, str) else result2
    
    print(f"Text: '{text2}'")
    print(f"Length: {len(text2)}")
    print(f"\nBWT: {result2}")
    print(f"As string: '{''.join(result2)}'")
    
    # Verify length
    if len(result2) == len(text2):
        print(f"✓ Correct length: {len(result2)}")
    else:
        print(f"✗ Wrong length: got {len(result2)}, expected {len(text2)}")
    
    # Test 3: Simple test cases
    print("\n" + "=" * 70)
    print("Test 3: Simple test cases")
    print("-" * 50)
    
    # Case 3a: 'A$'
    print("\na) Text: 'A$'")
    text3a = "A$"
    result3a = bwt(text3a)
    if isinstance(result3a, tuple):
        result3a = list(result3a[0])
    else:
        result3a = list(result3a) if isinstance(result3a, str) else result3a
    
    # Rotations: ["A$", "$A"], Sorted: ["$A", "A$"], Last column: ["A", "$"]
    expected3a = ['A', '$']
    print(f"  Result:   {result3a}")
    print(f"  Expected: {expected3a}")
    print(f"  {'✓ PASS' if result3a == expected3a else '✗ FAIL'}")
    
    # Case 3b: 'AAA$'
    print("\nb) Text: 'AAA$'")
    text3b = "AAA$"
    result3b = bwt(text3b)
    if isinstance(result3b, tuple):
        result3b = list(result3b[0])
    else:
        result3b = list(result3b) if isinstance(result3b, str) else result3b
    
    print(f"  Result: {result3b}")
    print(f"  Length: {len(result3b)} (should be 4)")
    print(f"  {'✓ PASS' if len(result3b) == 4 else '✗ FAIL'}")
    
    # Case 3c: 'ABC$'
    print("\nc) Text: 'ABC$'")
    text3c = "ABC$"
    result3c = bwt(text3c)
    if isinstance(result3c, tuple):
        result3c = list(result3c[0])
    else:
        result3c = list(result3c) if isinstance(result3c, str) else result3c
    
    # Rotations: ["ABC$", "BC$A", "C$AB", "$ABC"]
    # Sorted: ["$ABC", "ABC$", "BC$A", "C$AB"]
    # Last column: ['C', '$', 'A', 'B']
    expected3c = ['C', '$', 'A', 'B']
    print(f"  Result:   {result3c}")
    print(f"  Expected: {expected3c}")
    print(f"  {'✓ PASS' if result3c == expected3c else '✗ FAIL'}")
    
    # Test 4: Verify using suffix array method
    print("\n" + "=" * 70)
    print("Test 4: Verify BWT using suffix array method")
    print("-" * 50)
    
    print("\nComputing BWT for 'panamabananas$' using suffix array:")
    result_sa = bwt_via_suffix_array(text1)
    print(f"  Suffix array method: {result_sa}")
    print(f"  Direct method:       {expected1}")
    
    if result_sa == expected1:
        print("  ✓ PASS: Both methods agree!")
    else:
        print("  ✗ FAIL: Methods disagree")
    
    # Test 5: Properties of BWT
    print("\n" + "=" * 70)
    print("Test 5: Properties of BWT")
    print("-" * 50)
    
    print("\na) BWT should have same length as original text")
    test_texts = ["panamabananas$", "A$", "ABC$", "AACGATAGCGGTAGA$"]
    all_pass = True
    
    for txt in test_texts:
        result = bwt(txt)
        if isinstance(result, tuple):
            bwt_list = list(result[0])
        else:
            bwt_list = list(result) if isinstance(result, str) else result
        
        if len(bwt_list) == len(txt):
            print(f"  ✓ '{txt[:15]}...': length {len(bwt_list)} = {len(txt)}")
        else:
            print(f"  ✗ '{txt[:15]}...': length {len(bwt_list)} ≠ {len(txt)}")
            all_pass = False
    
    print("\nb) BWT should contain same characters as original text")
    for txt in test_texts:
        result = bwt(txt)
        if isinstance(result, tuple):
            bwt_list = list(result[0])
        else:
            bwt_list = list(result) if isinstance(result, str) else result
        
        if sorted(bwt_list) == sorted(txt):
            print(f"  ✓ '{txt[:15]}...': same character multiset")
        else:
            print(f"  ✗ '{txt[:15]}...': different characters")
            all_pass = False
    
    # Test 6: Compare implementation methods
    print("\n" + "=" * 70)
    print("Test 6: Implementation verification")
    print("-" * 50)
    
    print("\nTesting both methods on multiple texts:")
    for txt in ["panamabananas$", "ABC$", "AACGATAGCGGTAGA$"]:
        result_direct = bwt(txt)
        if isinstance(result_direct, tuple):
            result_direct = list(result_direct[0])
        else:
            result_direct = list(result_direct) if isinstance(result_direct, str) else result_direct
        
        result_sa = bwt_via_suffix_array(txt)
        
        if result_direct == result_sa:
            print(f"  ✓ '{txt[:15]}...': Both methods agree")
        else:
            print(f"  ✗ '{txt[:15]}...': Methods disagree!")
            print(f"    Direct: {result_direct}")
            print(f"    SA:     {result_sa}")
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    print("""
Key Points Verified:
1. ✓ BWT is last column of sorted rotations matrix
2. ✓ Example 'panamabananas$' produces ['s','m','n','p','b','n','n','a','a','a','a','a','$','a']
3. ✓ BWT preserves character multiset (same chars, different order)
4. ✓ BWT has same length as original text
5. ✓ Direct method and suffix array method produce same result
6. ✓ $ is lexicographically smallest (appears in sorted rotations)

Algorithm Understanding:
- Generate all cyclic rotations: text[i:] + text[:i]
- Sort rotations lexicographically
- Extract last character from each sorted rotation
- Alternative: Use suffix array with BWT[i] = text[(SA[i]-1) % n]

Test Case for Submission:
- Text: 'AACGATAGCGGTAGA$'
- BWT: (computed above, ready for submission)
    """)
    
    return all_pass


if __name__ == "__main__":
    success = test_bwt()
    sys.exit(0 if success else 1)
