#!/usr/bin/env python3
"""Test and generate submission URL for IBWT (Exercise 3)."""

import sys
import os

# Import config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from config import STUDENT_ID, build_test_url

# Import ibwt function
sys.path.insert(0, os.path.dirname(__file__))
from ibwt import ibwt

# Import bwt for verification
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'bwt_tema4_eje2'))
from bwt import bwt


def simple_bwt(text):
    """Simple BWT for verification."""
    if text.count('$') != 1 or not text.endswith('$'):
        raise ValueError("Text must end with exactly one '$'")
    
    n = len(text)
    rotations = [text[i:] + text[:i] for i in range(n)]
    rotations.sort()
    return ''.join(rot[-1] for rot in rotations)


def main():
    print("=" * 70)
    print("EXERCISE 3: IBWT (Inverse BWT) - Submission Test")
    print("=" * 70)
    
    # Test with the exercise example first
    print("\n" + "-" * 50)
    print("Test 1: Example from exercise")
    print("-" * 50)
    
    example_bwt = "ard$rcaaaabb"
    example_result = ibwt(example_bwt)
    example_expected = "abracadabra$"
    
    print(f"BWT input: '{example_bwt}'")
    print(f"Reconstructed: '{example_result}'")
    print(f"Expected:      '{example_expected}'")
    
    if example_result == example_expected:
        print("✓ PASS: Example works correctly!")
    else:
        print("✗ FAIL: Example mismatch")
    
    # Verify by computing BWT
    bwt_check = simple_bwt(example_result)
    print(f"\nVerification: bwt('{example_result}') = '{bwt_check}'")
    if bwt_check == example_bwt:
        print("✓ PASS: Round-trip successful!")
    else:
        print(f"✗ FAIL: Expected '{example_bwt}'")
    
    # Test with the test case
    print("\n" + "=" * 70)
    print("Test 2: Test case for submission")
    print("=" * 70)
    
    test_bwt = "enwvpeoseu$llt"
    
    print(f"\nBWT input: '{test_bwt}'")
    print(f"Length: {len(test_bwt)}")
    
    # Compute IBWT
    result = ibwt(test_bwt)
    
    print(f"\nReconstructed: '{result}'")
    print(f"Length: {len(result)}")
    
    # Verify properties
    print("\n" + "-" * 50)
    print("Verification:")
    
    if len(result) == len(test_bwt):
        print(f"✓ Same length: {len(result)}")
    else:
        print(f"✗ Wrong length: {len(result)} ≠ {len(test_bwt)}")
    
    if result.endswith('$'):
        print("✓ Ends with '$'")
    else:
        print("✗ Does not end with '$'")
    
    if result.count('$') == 1:
        print("✓ Contains exactly one '$'")
    else:
        print(f"✗ Contains {result.count('$')} '$' characters")
    
    # Verify by computing BWT again
    bwt_verify = simple_bwt(result)
    print(f"\nRound-trip verification:")
    print(f"  original → BWT: '{test_bwt}'")
    print(f"  BWT → IBWT:     '{result}'")
    print(f"  IBWT → BWT:     '{bwt_verify}'")
    
    if bwt_verify == test_bwt:
        print("✓ PASS: Perfect round-trip! IBWT is correct.")
    else:
        print(f"✗ FAIL: Expected '{test_bwt}'")
    
    # Show character composition
    print("\n" + "-" * 50)
    print("Character composition:")
    from collections import Counter
    counter_bwt = Counter(test_bwt)
    counter_result = Counter(result)
    
    print(f"BWT:    {dict(sorted(counter_bwt.items()))}")
    print(f"Result: {dict(sorted(counter_result.items()))}")
    
    if counter_bwt == counter_result:
        print("✓ Same character multiset (as expected)")
    else:
        print("✗ Different characters")
    
    # Save to file
    out_path = os.path.join(os.path.dirname(__file__), 'original_text.txt')
    with open(out_path, 'w') as f:
        f.write(result)
    print(f"\n✓ Saved reconstructed text to: {out_path}")
    
    # Generate submission URL
    print("\n" + "=" * 70)
    print("SUBMISSION URL")
    print("=" * 70)
    
    # Response is the reconstructed text as a string
    response = result
    url = build_test_url(session=4, exercise=3, response=response, student_id=STUDENT_ID)
    
    print(f"\nIBWT of '{test_bwt}':")
    print(f"  Result: '{response}'")
    print(f"\nSubmission URL:")
    print(url)
    
    print("\n" + "=" * 70)
    print("KEY ALGORITHM POINTS:")
    print("=" * 70)
    print("""
1. INVERSE BWT reconstructs original text from BWT
2. Uses LAST-FIRST PROPERTY:
   - i-th occurrence of character X in FIRST column
   - Corresponds to i-th occurrence of X in LAST column

3. Algorithm:
   a. L = transformada (last column)
   b. F = sorted(L) (first column)
   c. Compute occurrence numbers for each position
   d. Create mapping from (char, occurrence) → row in F
   e. Start at row where F has '$'
   f. Follow LF mapping n times, collecting characters
   g. Reverse the collected string

4. Example: 'ard$rcaaaabb' → 'abracadabra$'
   - L = 'ard$rcaaaabb', F = '$aaaaabbcdrr'
   - Start at F[0] = '$'
   - Follow: $ → a → r → b → a → d → a → c → a → r → b → a → $
   - Collect and reverse to get 'abracadabra$'

5. Test case: 'enwvpeoseu$llt' → 'twelveplusone$'
   - Verified by round-trip: BWT → IBWT → BWT

Properties:
- IBWT has same length as BWT
- IBWT has same characters as BWT (permutation)
- IBWT always ends with '$'
- BWT(IBWT(x)) = x (perfect round-trip)
    """)
    
    # Additional tests
    print("\n" + "=" * 70)
    print("Additional verification with known examples:")
    print("=" * 70)
    
    test_cases = [
        ("smnpbnnaaaaa$a", "panamabananas$"),
        ("ard$rcaaaabb", "abracadabra$"),
        ("C$AB", "ABC$"),
    ]
    
    print("\nKnown BWT → Expected IBWT:")
    all_correct = True
    for bwt_in, expected_out in test_cases:
        result_test = ibwt(bwt_in)
        match = "✓" if result_test == expected_out else "✗"
        print(f"  {match} '{bwt_in}' → '{result_test}' {'(expected: ' + expected_out + ')' if result_test != expected_out else ''}")
        if result_test != expected_out:
            all_correct = False
    
    if all_correct:
        print("\n✓ All verification tests passed!")
    else:
        print("\n⚠️  Some verification tests failed")


if __name__ == "__main__":
    main()
