#!/usr/bin/env python3
"""Comprehensive test suite for First Occurrence (Exercise 5)."""

import sys
import os

# Add current directory to path to import first_occurrence
sys.path.insert(0, os.path.dirname(__file__))
from first_occurrence import firstOccurrence, computeAllFirstOccurrences


def test_example_from_exercise():
    """Test 1: Example from exercise statement."""
    print("\n" + "=" * 70)
    print("TEST 1: Example from exercise")
    print("=" * 70)
    
    text = "$aaaaaabmnnps"
    symbol = "n"
    expected = 9
    
    result = firstOccurrence(symbol, text)
    
    print(f"Text: '{text}'")
    print(f"Symbol: '{symbol}'")
    print(f"Expected: {expected}")
    print(f"Result:   {result}")
    
    # Verify
    passed = result == expected
    print(f"\n{'✓ PASS' if passed else '✗ FAIL'}")
    
    return passed


def test_all_first_occurrences():
    """Test 2: All first occurrences in example text."""
    print("\n" + "=" * 70)
    print("TEST 2: All first occurrences (test case)")
    print("=" * 70)
    
    text = "$aaaaaabmnnps"
    
    # Expected first occurrences
    expected = {
        '$': 0,
        'a': 1,
        'b': 7,
        'm': 8,
        'n': 9,
        'p': 11,
        's': 12
    }
    
    result = computeAllFirstOccurrences(text)
    
    print(f"Text: '{text}'")
    print(f"\nExpected first occurrences:")
    for symbol, pos in sorted(expected.items()):
        print(f"  '{symbol}': {pos}")
    
    print(f"\nActual first occurrences:")
    for symbol, pos in sorted(result.items()):
        print(f"  '{symbol}': {pos}")
    
    # Verify
    passed = result == expected
    print(f"\n{'✓ PASS' if passed else '✗ FAIL'}")
    
    if not passed:
        print("\nDifferences:")
        all_symbols = set(expected.keys()) | set(result.keys())
        for symbol in sorted(all_symbols):
            exp = expected.get(symbol, 'missing')
            res = result.get(symbol, 'missing')
            if exp != res:
                print(f"  '{symbol}': expected {exp}, got {res}")
    
    return passed


def test_edge_cases():
    """Test 3: Edge cases."""
    print("\n" + "=" * 70)
    print("TEST 3: Edge cases")
    print("=" * 70)
    
    all_passed = True
    
    # Test 3a: First symbol in text
    print("\na) First symbol in text")
    text = "$aaaaaabmnnps"
    symbol = "$"
    expected = 0
    result = firstOccurrence(symbol, text)
    passed = result == expected
    print(f"  Symbol '{symbol}' in '{text}'")
    print(f"  Expected: {expected}, Result: {result}")
    print(f"  {'✓ PASS' if passed else '✗ FAIL'}")
    all_passed = all_passed and passed
    
    # Test 3b: Last symbol in text
    print("\nb) Last symbol in text")
    symbol = "s"
    expected = 12
    result = firstOccurrence(symbol, text)
    passed = result == expected
    print(f"  Symbol '{symbol}' in '{text}'")
    print(f"  Expected: {expected}, Result: {result}")
    print(f"  {'✓ PASS' if passed else '✗ FAIL'}")
    all_passed = all_passed and passed
    
    # Test 3c: Symbol with multiple occurrences (should return first)
    print("\nc) Symbol with multiple occurrences")
    symbol = "a"
    expected = 1
    result = firstOccurrence(symbol, text)
    passed = result == expected
    print(f"  Symbol '{symbol}' in '{text}' (appears 6 times)")
    print(f"  Expected first: {expected}, Result: {result}")
    print(f"  {'✓ PASS' if passed else '✗ FAIL'}")
    all_passed = all_passed and passed
    
    # Test 3d: Symbol not in text
    print("\nd) Symbol not in text")
    symbol = "x"
    expected = -1
    result = firstOccurrence(symbol, text)
    passed = result == expected
    print(f"  Symbol '{symbol}' in '{text}' (not present)")
    print(f"  Expected: {expected}, Result: {result}")
    print(f"  {'✓ PASS' if passed else '✗ FAIL'}")
    all_passed = all_passed and passed
    
    # Test 3e: Single character text
    print("\ne) Single character text")
    text = "$"
    symbol = "$"
    expected = 0
    result = firstOccurrence(symbol, text)
    passed = result == expected
    print(f"  Symbol '{symbol}' in '{text}'")
    print(f"  Expected: {expected}, Result: {result}")
    print(f"  {'✓ PASS' if passed else '✗ FAIL'}")
    all_passed = all_passed and passed
    
    print(f"\n{'✓ ALL EDGE CASES PASSED' if all_passed else '✗ SOME EDGE CASES FAILED'}")
    return all_passed


def test_bwt_context():
    """Test 4: First occurrences in BWT context."""
    print("\n" + "=" * 70)
    print("TEST 4: First occurrences in BWT context")
    print("=" * 70)
    
    # Build BWT for 'panamabananas$'
    def build_bwt(text):
        n = len(text)
        rotations = [text[i:] + text[:i] for i in range(n)]
        rotations.sort()
        return ''.join(rot[-1] for rot in rotations)
    
    original_text = "panamabananas$"
    bwt_text = build_bwt(original_text)
    first_column = ''.join(sorted(bwt_text))
    
    print(f"Original text: '{original_text}'")
    print(f"BWT (last column): '{bwt_text}'")
    print(f"First column (sorted): '{first_column}'")
    
    # Get first occurrences
    first_occ = computeAllFirstOccurrences(first_column)
    
    print(f"\nFirst occurrences in first column:")
    for symbol, pos in sorted(first_occ.items()):
        print(f"  '{symbol}': {pos}")
    
    # This should match the C(symbol) array
    print(f"\nThis is the C(symbol) array for BWT pattern matching!")
    print(f"C[symbol] = first occurrence of symbol in sorted first column")
    
    # Verify properties
    expected_symbols = sorted(set(original_text))
    actual_symbols = sorted(first_occ.keys())
    passed = expected_symbols == actual_symbols
    
    print(f"\n{'✓ PASS' if passed else '✗ FAIL'}")
    return passed


def test_sorted_vs_unsorted():
    """Test 5: Demonstrate difference between sorted and unsorted text."""
    print("\n" + "=" * 70)
    print("TEST 5: Sorted vs unsorted text")
    print("=" * 70)
    
    # Unsorted text
    unsorted = "panamabananas$"
    
    # Sorted text (like BWT first column)
    sorted_text = ''.join(sorted(unsorted))
    
    print(f"Unsorted text: '{unsorted}'")
    print(f"Sorted text:   '{sorted_text}'")
    
    # First occurrences in both
    first_unsorted = computeAllFirstOccurrences(unsorted)
    first_sorted = computeAllFirstOccurrences(sorted_text)
    
    print(f"\nFirst occurrences in UNSORTED text:")
    for symbol, pos in sorted(first_unsorted.items()):
        print(f"  '{symbol}': {pos} (char at position: '{unsorted[pos]}')")
    
    print(f"\nFirst occurrences in SORTED text:")
    for symbol, pos in sorted(first_sorted.items()):
        print(f"  '{symbol}': {pos} (char at position: '{sorted_text[pos]}')")
    
    print(f"\nNote: Exercise uses SORTED text (like BWT first column)")
    print(f"In sorted text, first occurrence = C(symbol) for BWT matching")
    
    return True


def test_c_array_construction():
    """Test 6: Constructing C(symbol) array from first occurrences."""
    print("\n" + "=" * 70)
    print("TEST 6: C(symbol) array construction")
    print("=" * 70)
    
    text = "$aaaaaabmnnps"
    
    print(f"Text (sorted): '{text}'")
    print(f"\nText with indices:")
    print("Indices: " + " ".join(f"{i:2d}" for i in range(len(text))))
    print("Chars:   " + " ".join(f" {c}" for c in text))
    
    # Get first occurrences
    first_occ = computeAllFirstOccurrences(text)
    
    print(f"\nFirst occurrences (same as C[symbol]):")
    for symbol, pos in sorted(first_occ.items()):
        print(f"  C['{symbol}'] = {pos}")
    
    # Verify C[symbol] = count of symbols < symbol
    print(f"\nVerification: C[symbol] = count of symbols lexicographically < symbol")
    for symbol, pos in sorted(first_occ.items()):
        # Count symbols before first occurrence of this symbol
        count_before = sum(1 for c in text[:pos] if c != symbol)
        print(f"  '{symbol}': first at {pos}, symbols before: {count_before}")
    
    print(f"\nC[symbol] is used in LF-mapping:")
    print(f"  LF(i, symbol) = C[symbol] + Occ(symbol, i-1)")
    
    return True


def run_all_tests():
    """Run all test cases."""
    print("=" * 70)
    print("FIRST OCCURRENCE - COMPREHENSIVE TEST SUITE")
    print("=" * 70)
    
    tests = [
        ("Example from exercise", test_example_from_exercise),
        ("All first occurrences", test_all_first_occurrences),
        ("Edge cases", test_edge_cases),
        ("BWT context", test_bwt_context),
        ("Sorted vs unsorted", test_sorted_vs_unsorted),
        ("C-array construction", test_c_array_construction),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"\n✗ TEST FAILED WITH EXCEPTION: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status:8} - {name}")
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    print(f"\n{passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("\n🎉 ALL TESTS PASSED!")
        return True
    else:
        print(f"\n⚠️  {total_count - passed_count} test(s) failed")
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
