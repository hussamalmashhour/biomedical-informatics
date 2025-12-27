#!/usr/bin/env python3
"""Test and generate submission URL for First Occurrence (Exercise 5)."""

import sys
import os

# Import config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from config import STUDENT_ID, build_test_url

# Import first occurrence functions
sys.path.insert(0, os.path.dirname(__file__))
from first_occurrence import firstOccurrence, computeAllFirstOccurrences


def main():
    print("=" * 70)
    print("EXERCISE 5: First Occurrence - Submission Test")
    print("=" * 70)
    
    # Test case from exercise
    text = "$aaaaaabmnnps"
    symbol = "n"
    
    print(f"\nTest case:")
    print(f"Text: '{text}'")
    print(f"Symbol: '{symbol}'")
    
    # Show text with indices
    print(f"\nText with indices:")
    print("Indices: " + " ".join(f"{i:2d}" for i in range(len(text))))
    print("Chars:   " + " ".join(f" {c}" for c in text))
    
    # Compute first occurrence
    result = firstOccurrence(symbol, text)
    
    print(f"\nFirst occurrence of '{symbol}': {result}")
    print(f"Verification: text[{result}] = '{text[result]}'")
    
    # Verify it's correct
    if text[result] == symbol:
        print("✓ Correct position")
    else:
        print(f"✗ Wrong position - text[{result}] = '{text[result]}' ≠ '{symbol}'")
    
    # Check no earlier occurrence
    earlier = text[:result].find(symbol)
    if earlier == -1:
        print(f"✓ No earlier occurrence of '{symbol}'")
    else:
        print(f"✗ Earlier occurrence at position {earlier}")
    
    # Also compute all first occurrences as requested in test case
    print("\n" + "-" * 50)
    print("All first occurrences (test case requirement):")
    
    all_first = computeAllFirstOccurrences(text)
    
    for sym, pos in sorted(all_first.items()):
        print(f"  '{sym}': {pos}")
    
    # This is the C(symbol) array for BWT!
    print("\n" + "-" * 50)
    print("Understanding the result:")
    print(f"These first occurrences form the C(symbol) array for BWT matching.")
    print(f"C[symbol] = first occurrence of symbol in sorted text")
    print(f"Used in LF-mapping: LF(i, symbol) = C[symbol] + Occ(symbol, i-1)")
    
    # Generate submission URLs
    print("\n" + "=" * 70)
    print("SUBMISSION URLS")
    print("=" * 70)
    
    # Format 1: Submit single first occurrence (9 for 'n')
    print("\nFormat 1: First occurrence of 'n' only")
    response1 = result
    url1 = build_test_url(session=4, exercise=5, response=response1, student_id=STUDENT_ID)
    print(f"Response: {response1}")
    print(f"URL: {url1}")
    
    # Format 2: Submit all first occurrences as dictionary
    print("\nFormat 2: All first occurrences as dictionary")
    response2 = all_first
    url2 = build_test_url(session=4, exercise=5, response=response2, student_id=STUDENT_ID)
    print(f"Response: {response2}")
    print(f"URL: {url2}")
    
    # Format 3: Submit as list of positions (ordered by symbol)
    print("\nFormat 3: All first occurrences as list")
    response3 = [pos for sym, pos in sorted(all_first.items())]
    url3 = build_test_url(session=4, exercise=5, response=response3, student_id=STUDENT_ID)
    print(f"Response: {response3}")
    print(f"URL: {url3}")
    
    # Most likely format based on exercise description
    print("\n" + "=" * 70)
    print("RECOMMENDED SUBMISSION")
    print("=" * 70)
    print("\nBased on exercise description: 'apply to ALL symbols'")
    print("Most likely expected format: Dictionary or list of all first occurrences")
    print("\nRecommended URL (Format 2 - Dictionary):")
    print(url2)
    
    print("\n" + "=" * 70)
    print("KEY ALGORITHM POINTS:")
    print("=" * 70)
    print("""
1. firstOccurrence(symbol, text) finds first index where symbol appears
2. Exercise hint: "trivial en python usando la función index para str"
3. Implementation: return text.index(symbol) or text.find(symbol)
4. Test case: Apply to ALL symbols in '$aaaaaabmnnps'

Example: '$aaaaaabmnnps'
- '$' first at 0
- 'a' first at 1
- 'b' first at 7
- 'm' first at 8
- 'n' first at 9  ← answer for single symbol 'n'
- 'p' first at 11
- 's' first at 12

Relation to BWT:
- Text is SORTED (like first column of BWT matrix)
- First occurrence = C[symbol] in LF-mapping
- C[symbol] = count of symbols lexicographically < symbol
- Used in backward search: top = C[symbol] + Occ(symbol, top-1)
""")
    
    # Save results
    out_path = os.path.join(os.path.dirname(__file__), 'first_occurrences.txt')
    with open(out_path, 'w') as f:
        f.write(f"Text: {text}\n")
        f.write(f"Symbol: {symbol}\n")
        f.write(f"First occurrence: {result}\n")
        f.write("All first occurrences:\n")
        for sym, pos in sorted(all_first.items()):
            f.write(f"{sym}: {pos}\n")
    
    print(f"\n✓ Results saved to: {out_path}")


if __name__ == '__main__':
    main()
