#!/usr/bin/env python3
"""Test and generate submission URL for BWMatching (Exercise 4)."""

import sys
import os

# Import config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from config import STUDENT_ID, build_test_url

# Import functions
sys.path.insert(0, os.path.dirname(__file__))
from bwmatching import read_fasta_first_sequence, bwt, build_first_to_last, bwMatching


def main():
    print("=" * 70)
    print("EXERCISE 4: BWMatching - Final Submission Test")
    print("=" * 70)
    
    # ========================================================================
    # TEST 1: Example from exercise (to verify algorithm)
    # ========================================================================
    print("\n" + "=" * 70)
    print("TEST 1: Example from exercise")
    print("=" * 70)
    
    text_example = "panamabananas$"
    pattern_example = "ana"
    
    print(f"Text: '{text_example}'")
    print(f"Pattern: '{pattern_example}'")
    
    # Build BWT and mapping
    last_col = bwt(text_example)
    first_to_last = build_first_to_last(last_col)
    result_example = bwMatching(last_col, first_to_last, pattern_example)
    
    print(f"BWT (last column): '{last_col}'")
    print(f"First-to-last mapping: {first_to_last}")
    print(f"\nResult: {result_example}")
    print(f"Expected: [3, 4, 5]")
    
    if result_example == [3, 4, 5]:
        print("✓ CORRECT - Algorithm works as expected!")
    else:
        print("✗ INCORRECT - Algorithm has a bug!")
    
    # Show the BWT matrix for verification
    print("\nBWT Matrix (sorted rotations):")
    rotations = [text_example[i:] + text_example[:i] for i in range(len(text_example))]
    rotations.sort()
    for i, rot in enumerate(rotations):
        marker = " ← MATCH" if i in result_example else ""
        print(f"  Row {i:2d}: {rot}{marker}")
    
    # ========================================================================
    # TEST 2: Test case - oriC Vibrio cholerae with pattern "cgga"
    # ========================================================================
    print("\n" + "=" * 70)
    print("TEST 2: Test case - oricVC$ with pattern 'cgga'")
    print("=" * 70)
    
    # Read Vibrio cholerae oriC sequence
    oric_path = os.path.join(os.path.dirname(__file__), 'oric.txt')
    seq_vc = read_fasta_first_sequence(oric_path)
    
    print(f"Loaded sequence from: {oric_path}")
    print(f"Sequence name: Vibrio cholerae oriC")
    print(f"Sequence length: {len(seq_vc)} bp")
    print(f"First 60 chars: {seq_vc[:60]}")
    print(f"Last 60 chars:  {seq_vc[-60:]}")
    
    # Verify case
    has_lower = any(c.islower() for c in seq_vc)
    has_upper = any(c.isupper() for c in seq_vc)
    print(f"\nSequence case: {'lowercase' if has_lower else 'uppercase'}")
    
    # Test with pattern "cgga" (as specified in exercise)
    text_test = seq_vc + "$"
    pattern_test = "cgga"
    
    print(f"\nText: oricVC$ (Vibrio cholerae oriC + $)")
    print(f"Text length (with $): {len(text_test)}")
    print(f"Pattern: '{pattern_test}'")
    
    # Build BWT and search
    last_col_test = bwt(text_test)
    first_to_last_test = build_first_to_last(last_col_test)
    result_test = bwMatching(last_col_test, first_to_last_test, pattern_test)
    
    print(f"\nBWT row indices: {result_test}")
    print(f"Number of matches: {len(result_test)}")
    
    # Verify with naive search
    print("\n" + "-" * 70)
    print("Verification with naive search:")
    
    naive_matches = []
    for i in range(len(seq_vc) - len(pattern_test) + 1):
        if seq_vc[i:i+len(pattern_test)] == pattern_test:
            naive_matches.append(i)
    
    print(f"Naive search found {len(naive_matches)} matches at positions: {naive_matches}")
    
    if len(result_test) == len(naive_matches):
        print(f"✓ Match count agrees: {len(result_test)} matches")
    else:
        print(f"✗ Match count differs: BWMatching={len(result_test)}, Naive={len(naive_matches)}")
    
    # Show actual pattern occurrences
    print("\nPattern occurrences in text:")
    for pos in naive_matches[:5]:  # Show first 5
        context_start = max(0, pos - 10)
        context_end = min(len(seq_vc), pos + len(pattern_test) + 10)
        context = seq_vc[context_start:context_end]
        marker_pos = pos - context_start
        print(f"  Position {pos}: ...{context}...")
        print(f"  {' ' * (marker_pos + 15)}{'^' * len(pattern_test)}")
    
    # ========================================================================
    # SUBMISSION URL
    # ========================================================================
    print("\n" + "=" * 70)
    print("SUBMISSION URL")
    print("=" * 70)
    
    # The answer is the BWT row indices
    response = result_test
    url = build_test_url(session=4, exercise=4, response=response, student_id=STUDENT_ID)
    
    print(f"\nText: oricVC$ (Vibrio cholerae oriC)")
    print(f"Pattern: '{pattern_test}'")
    print(f"Result (BWT row indices): {response}")
    print(f"Number of matches: {len(response)}")
    print(f"\nSubmission URL:")
    print(url)
    
    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("\n" + "=" * 70)
    print("ALGORITHM SUMMARY")
    print("=" * 70)
    print("""
BWMatching Algorithm (Backward Search):
1. Start with last character of pattern
2. Find all rows in last column with that character
3. Use first-to-last mapping to find corresponding rows in first column
4. Repeat with previous character of pattern
5. When pattern exhausted, return row indices

Example: text="panamabananas$", pattern="ana"
- Start with 'a' (last char): rows 1-6 in first column have 'a'
- Filter by 'n' (middle char): rows 9-11 in last column have 'n'
- Use LF-mapping: map to rows 3-5 in first column
- Filter by 'a' (first char): rows 3-5 already start with 'a'
- Result: [3, 4, 5] ✓

Key Properties:
- Returns row indices in BWT matrix (not text positions)
- Rows are where pattern starts in sorted rotations
- Uses only first column (sorted) and last column (BWT)
- Uses first-to-last mapping to navigate between columns
- Time complexity: O(m × n) where m=pattern length, n=text length

Test Case Result:
- Text: Vibrio cholerae oriC (1080 bp) + $
- Pattern: "cgga" (lowercase)
- Result: """ + str(response) + """
- Matches: """ + str(len(response)) + """ occurrences
""")
    
    # Save results
    out_path = os.path.join(os.path.dirname(__file__), 'bwmatching_results.txt')
    with open(out_path, 'w') as f:
        f.write(f"Pattern: {pattern_test}\n")
        f.write(f"Rows: {result_test}\n\n")
        f.write(f"Pattern: {pattern_example}\n")
        f.write(f"Rows: {result_example}\n")
    
    print(f"\n✓ Results saved to: {out_path}")


if __name__ == '__main__':
    main()
