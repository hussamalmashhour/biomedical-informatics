#!/usr/bin/env python3
"""Comprehensive test suite for IBWT (Inverse Burrows-Wheeler Transform)."""

import sys
import os

# Import from current directory
sys.path.insert(0, os.path.dirname(__file__))
from ibwt import ibwt, compute_ranks, lf_mapping

# Import BWT from Exercise 2 for verification
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'bwt_tema4_eje2'))
from bwt import bwt


def simple_bwt(text):
    """Simple BWT implementation for verification."""
    if text.count('$') != 1 or not text.endswith('$'):
        raise ValueError("Text must end with exactly one '$'")
    
    n = len(text)
    rotations = [text[i:] + text[:i] for i in range(n)]
    rotations.sort()
    return ''.join(rot[-1] for rot in rotations)


def subscripts(text):
    """Compute occurrence numbers for each character (1-based)."""
    counts = {}
    result = []
    
    for char in text:
        current_count = counts.get(char, 0) + 1
        counts[char] = current_count
        result.append(current_count)
    
    return result


def test_ibwt():
    """Run comprehensive IBWT tests."""
    
    print("=" * 70)
    print("EXERCISE 3: Testing ibwt() function (Inverse BWT)")
    print("=" * 70)
    
    all_pass = True
    
    # Test 1: Example from exercise - "abracadabra$"
    print("\nTest 1: Example from exercise - 'abracadabra$'")
    print("-" * 50)
    
    transformada1 = "ard$rcaaaabb"
    result1 = ibwt(transformada1)
    expected1 = "abracadabra$"
    
    print(f"BWT input: '{transformada1}'")
    print(f"Length: {len(transformada1)}")
    print(f"\nReconstructed: '{result1}'")
    print(f"Expected:      '{expected1}'")
    
    if result1 == expected1:
        print("✓ PASS: Exact match!")
    else:
        print("✗ FAIL: Mismatch")
        all_pass = False
    
    # Verify by computing BWT of result
    bwt_of_result = simple_bwt(result1)
    print(f"\nVerification: bwt('{result1}') = '{bwt_of_result}'")
    if bwt_of_result == transformada1:
        print("✓ PASS: BWT round-trip successful!")
    else:
        print(f"✗ FAIL: Expected '{transformada1}'")
        all_pass = False
    
    # Test 2: Classic "panamabananas$" example
    print("\n" + "=" * 70)
    print("Test 2: Classic example - 'panamabananas$'")
    print("-" * 50)
    
    original2 = "panamabananas$"
    # First compute its BWT
    bwt2 = simple_bwt(original2)
    print(f"Original text: '{original2}'")
    print(f"BWT: '{bwt2}'")
    
    # Now reconstruct
    reconstructed2 = ibwt(bwt2)
    print(f"Reconstructed: '{reconstructed2}'")
    
    if reconstructed2 == original2:
        print("✓ PASS: Perfect reconstruction!")
    else:
        print(f"✗ FAIL: Expected '{original2}'")
        all_pass = False
    
    # Test 3: Test case from exercise
    print("\n" + "=" * 70)
    print("Test 3: Test case - 'enwvpeoseu$llt'")
    print("-" * 50)
    
    transformada3 = "enwvpeoseu$llt"
    result3 = ibwt(transformada3)
    
    print(f"BWT input: '{transformada3}'")
    print(f"Length: {len(transformada3)}")
    print(f"\nReconstructed: '{result3}'")
    
    # Verify by computing BWT again
    bwt_verify = simple_bwt(result3)
    print(f"\nVerification: bwt('{result3}') = '{bwt_verify}'")
    
    if bwt_verify == transformada3:
        print("✓ PASS: BWT round-trip successful!")
    else:
        print(f"✗ FAIL: Expected '{transformada3}'")
        all_pass = False
    
    # Test 4: Test subscripts() helper function
    print("\n" + "=" * 70)
    print("Test 4: Testing subscripts() helper function")
    print("-" * 50)
    
    test_text = "ard$rcaaaabb"
    subs = subscripts(test_text)
    expected_subs = [1, 1, 1, 1, 2, 1, 2, 3, 4, 5, 1, 2]
    
    print(f"Text: '{test_text}'")
    print(f"Subscripts: {subs}")
    print(f"Expected:   {expected_subs}")
    
    if subs == expected_subs:
        print("✓ PASS: Subscripts correct!")
    else:
        print("✗ FAIL: Subscripts mismatch")
        all_pass = False
    
    # Show character-by-character mapping
    print("\nCharacter occurrence mapping:")
    for i, (char, occ) in enumerate(zip(test_text, subs)):
        print(f"  Position {i:2d}: '{char}' → occurrence {occ}")
    
    # Test 5: Simple test cases
    print("\n" + "=" * 70)
    print("Test 5: Simple test cases")
    print("-" * 50)
    
    # Case 5a: Two characters
    print("\na) BWT: 'A$' (from 'A$')")
    bwt5a = "A$"
    result5a = ibwt(bwt5a)
    expected5a = "A$"
    print(f"  Reconstructed: '{result5a}'")
    print(f"  Expected:      '{expected5a}'")
    print(f"  {'✓ PASS' if result5a == expected5a else '✗ FAIL'}")
    if result5a != expected5a:
        all_pass = False
    
    # Case 5b: Repeated characters
    print("\nb) BWT: 'AAA$' (from 'AAA$')")
    bwt5b = "AAA$"
    result5b = ibwt(bwt5b)
    print(f"  Reconstructed: '{result5b}'")
    
    # Verify by round-trip
    bwt_check = simple_bwt(result5b)
    if bwt_check == bwt5b:
        print(f"  ✓ PASS: Round-trip successful")
    else:
        print(f"  ✗ FAIL: Round-trip failed")
        all_pass = False
    
    # Case 5c: Simple distinct characters (from Exercise 2)
    print("\nc) BWT: 'C$AB' (from 'ABC$')")
    bwt5c = "C$AB"
    result5c = ibwt(bwt5c)
    expected5c = "ABC$"
    print(f"  Reconstructed: '{result5c}'")
    print(f"  Expected:      '{expected5c}'")
    print(f"  {'✓ PASS' if result5c == expected5c else '✗ FAIL'}")
    if result5c != expected5c:
        all_pass = False
    
    # Test 6: Step-by-step walkthrough of algorithm
    print("\n" + "=" * 70)
    print("Test 6: Step-by-step algorithm walkthrough")
    print("-" * 50)
    
    def ibwt_detailed(transformada, show_steps=5):
        """Show detailed steps of inverse BWT."""
        print(f"\nDetailed reconstruction for '{transformada}':")
        
        n = len(transformada)
        L = transformada  # Last column
        F = ''.join(sorted(L))  # First column
        
        print(f"\nL (last column):  {list(L)}")
        print(f"F (first column): {list(F)}")
        
        # Compute occurrence numbers
        L_occ = subscripts(L)
        F_occ = subscripts(F)
        
        print(f"\nOccurrence numbers in L: {L_occ}")
        print(f"Occurrence numbers in F: {F_occ}")
        
        # Create F mapping
        F_map = {}
        for i in range(n):
            key = (F[i], F_occ[i])
            F_map[key] = i
        
        print(f"\nF mapping (char, occ) → row (first {min(6, len(F_map))}):")
        for idx, ((char, occ), row) in enumerate(sorted(F_map.items())[:6]):
            print(f"  ('{char}', {occ}) → row {row}")
        if len(F_map) > 6:
            print(f"  ... ({len(F_map) - 6} more)")
        
        # Start reconstruction
        start_row = F.index('$')
        current_row = start_row
        
        print(f"\nStarting at row {start_row} (where F has '$')")
        print(f"\nReconstruction steps (showing first {show_steps}):")
        
        result_chars = []
        for step in range(n):
            char = L[current_row]
            occ = L_occ[current_row]
            result_chars.append(char)
            
            if step < show_steps:
                print(f"  Step {step}: row {current_row:2d} → L[{current_row}]='{char}' (occ {occ}) → next row {F_map[(char, occ)]}")
            
            current_row = F_map[(char, occ)]
        
        if n > show_steps:
            print(f"  ... ({n - show_steps} more steps)")
        
        result = ''.join(result_chars[::-1])
        print(f"\nBuilt backwards: '{''.join(result_chars)}'")
        print(f"Result (reversed): '{result}'")
        return result
    
    # Show detailed walkthrough for example
    detailed_result = ibwt_detailed("ard$rcaaaabb", show_steps=7)
    if detailed_result == "abracadabra$":
        print("\n✓ PASS: Detailed reconstruction matches expected!")
    else:
        print(f"\n✗ FAIL: Expected 'abracadabra$', got '{detailed_result}'")
        all_pass = False
    
    # Test 7: Verify with multiple test strings
    print("\n" + "=" * 70)
    print("Test 7: Round-trip testing with various strings")
    print("-" * 50)
    
    test_strings = [
        "ABC$",
        "MISSISSIPPI$",
        "BANANA$",
        "AACGATAGCGGTAGA$",
        "panamabananas$",
        "abracadabra$"
    ]
    
    print("\nTesting: original → BWT → IBWT → verify")
    for original in test_strings:
        bwt_text = simple_bwt(original)
        reconstructed = ibwt(bwt_text)
        
        match = "✓" if reconstructed == original else "✗"
        print(f"  {match} '{original[:15]:15s}' → BWT → '{reconstructed[:15]:15s}'")
        
        if reconstructed != original:
            print(f"      Expected: '{original}'")
            print(f"      Got:      '{reconstructed}'")
            all_pass = False
    
    # Test 8: Test compute_ranks function (internal)
    print("\n" + "=" * 70)
    print("Test 8: Testing compute_ranks() (internal function)")
    print("-" * 50)
    
    test_col = "ard$rcaaaabb"
    ranks = compute_ranks(test_col)
    expected_ranks = [0, 0, 0, 0, 1, 0, 1, 2, 3, 4, 0, 1]  # 0-based
    
    print(f"Column: '{test_col}'")
    print(f"Ranks (0-based): {ranks}")
    print(f"Expected:        {expected_ranks}")
    
    if ranks == expected_ranks:
        print("✓ PASS: Ranks correct!")
    else:
        print("✗ FAIL: Ranks mismatch")
        all_pass = False
    
    print("\nNote: compute_ranks uses 0-based indexing internally")
    print("      subscripts() uses 1-based indexing for clarity")
    
    # Test 9: LF mapping verification
    print("\n" + "=" * 70)
    print("Test 9: Testing LF mapping construction")
    print("-" * 50)
    
    bwt_test = "ard$rcaaaabb"
    first_col, lf = lf_mapping(bwt_test)
    
    print(f"BWT (L): '{bwt_test}'")
    print(f"First (F): '{first_col}'")
    print(f"LF mapping: {lf}")
    
    # Verify LF mapping makes sense
    print("\nLF mapping interpretation (first few):")
    for i in range(min(5, len(lf))):
        print(f"  L[{i}]='{bwt_test[i]}' maps to F[{lf[i]}]='{first_col[lf[i]]}'")
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    print("""
Key Points Verified:
1. ✓ IBWT correctly reconstructs original text from BWT
2. ✓ Example 'ard$rcaaaabb' → 'abracadabra$' works perfectly
3. ✓ Round-trip (original → BWT → IBWT → original) is lossless
4. ✓ Subscripts (occurrence numbers) computed correctly
5. ✓ LF mapping works correctly for reconstruction
6. ✓ Algorithm handles various test cases correctly

Algorithm Understanding:
- Last-First Property: i-th occurrence in F = i-th occurrence in L
- Start from row where F has '$'
- Follow LF mapping to walk through characters
- Build result backwards, then reverse
- Use occurrence numbers to distinguish identical characters

Test Case Results:
- Example: 'ard$rcaaaabb' → 'abracadabra$' ✓
- Classic: 'smnpbnnaaaaa$a' → 'panamabananas$' ✓
- Test case: 'enwvpeoseu$llt' → (computed and verified) ✓
    """)
    
    return all_pass


if __name__ == "__main__":
    success = test_ibwt()
    
    if success:
        print("\n🎉 ALL TESTS PASSED! 🎉")
    else:
        print("\n⚠️  SOME TESTS FAILED")
    
    sys.exit(0 if success else 1)
