#!/usr/bin/env python3
"""
Burrows-Wheeler Transform (BWT) - Complete Algorithm Explanation
=================================================================

EXERCISE 2 (Tema 4): Implement bwt() function

What is BWT?
------------
The Burrows-Wheeler Transform (BWT) is a string transformation used in data
compression and bioinformatics. It rearranges a text to group similar characters
together, making it more compressible.

Algorithm:
----------
1. Generate all cyclic rotations of the text
2. Sort the rotations lexicographically
3. Take the LAST COLUMN of the sorted matrix

Example with "panamabananas$":
-------------------------------
Original text: "panamabananas$" (length 14)

Step 1: Generate all 14 cyclic rotations
    0: panamabananas$
    1: anamabananas$p
    2: namabananas$pa
    3: amabananas$pan
    ...
    13: $panamabanana

Step 2: Sort rotations lexicographically
    $ is smallest, so "$panamabanana" comes first
    Then "abananas$panam"
    Then "amabananas$pan"
    etc.

Sorted rotations:
    0:  $panamabananas  → last char: 's'
    1:  abananas$panam  → last char: 'm'
    2:  amabananas$pan  → last char: 'n'
    3:  anamabananas$p  → last char: 'p'
    4:  ananas$panamab  → last char: 'b'
    5:  anas$panamaban  → last char: 'n'
    6:  as$panamabanan  → last char: 'n'
    7:  bananas$panama  → last char: 'a'
    8:  mabananas$pana  → last char: 'a'
    9:  namabananas$pa  → last char: 'a'
    10: nanas$panamaba  → last char: 'a'
    11: nas$panamabana  → last char: 'a'
    12: panamabananas$  → last char: '$'
    13: s$panamabanana  → last char: 'a'

Step 3: Extract last column (BWT)
    BWT = ['s','m','n','p','b','n','n','a','a','a','a','a','$','a']
    As string: "smnpbnnaaaaa$a"

Key Properties:
---------------
1. BWT has same LENGTH as original text
2. BWT has same CHARACTERS as original (permutation)
3. BWT groups similar characters together (notice all 'a's clustered)
4. BWT is REVERSIBLE (can reconstruct original text from BWT)
5. '$' sentinel marks the original string's end position

Implementation Methods:
-----------------------

Method 1: Direct (used in our implementation)
    def bwt(text):
        n = len(text)
        rotations = [text[i:] + text[:i] for i in range(n)]
        rotations.sort()
        return [rot[-1] for rot in rotations]
    
    Time: O(n² log n) - sorting n strings of length n
    Space: O(n²) - storing all rotations

Method 2: Using Suffix Array (more efficient)
    def bwt(text):
        n = len(text)
        sa = suffixArray(text)  # From Exercise 1
        return [text[(sa[i] - 1) % n] for i in range(n)]
    
    Time: O(n log n) - suffix array construction + O(n) for BWT
    Space: O(n) - only suffix array needed

Relationship to Suffix Array:
------------------------------
BWT and suffix arrays are closely related:
- Suffix array contains starting positions of sorted suffixes
- BWT[i] = character BEFORE the suffix that starts at position SA[i]
- Formula: BWT[i] = text[(SA[i] - 1) % n]

Example:
    text = "panamabananas$"
    SA = [13, 5, 3, 1, 7, 9, 11, 6, 4, 2, 8, 10, 0, 12]
    
    BWT[0] = text[(13-1) % 14] = text[12] = 's'
    BWT[1] = text[(5-1) % 14] = text[4] = 'm'
    BWT[2] = text[(3-1) % 14] = text[2] = 'n'
    ...

Why is BWT Useful?
------------------
1. Data Compression:
   - Groups similar characters together
   - Makes text more compressible with RLE or entropy coding
   - Used in bzip2 compression algorithm

2. Bioinformatics:
   - Used in read alignment (BWA, Bowtie)
   - Efficient pattern matching
   - Memory-efficient genome indexing

3. Reversibility:
   - Can reconstruct original text from BWT
   - Only need BWT string (same size as original)
   - Demonstrates important property of lossless transformation

Inverse BWT (Preview of Exercise 3):
-------------------------------------
The BWT is reversible. Given BWT, we can reconstruct the original text.
This is the subject of Exercise 3 (ibwt).

Testing Strategy:
-----------------
1. Verify exact example: "panamabananas$" → ['s','m','n','p','b','n','n','a','a','a','a','a','$','a']
2. Test with test case: "AACGATAGCGGTAGA$"
3. Verify properties:
   - Same length as original
   - Same character multiset
   - Contains exactly one '$'
4. Compare direct method vs suffix array method
5. Test edge cases: single char, repeated chars, distinct chars

Test Results:
-------------
✓ All tests pass
✓ Example matches expected output exactly
✓ Both implementation methods produce identical results
✓ All BWT properties verified

Submission:
-----------
Text: 'AACGATAGCGGTAGA$'
BWT: ['A','G','$','A','T','T','G','A','G','A','C','A','C','G','G','A']
As string: 'AG$ATTGAGACACGGA'
Length: 16

URL: https://cpg3.der.usal.es/eval/test?session=4&exercise=2&response=['A','G','$','A','T','T','G','A','G','A','C','A','C','G','G','A']&id=Z2256773H

Complexity Analysis:
--------------------
Direct method:
- Generate rotations: O(n²) time and space (n strings of length n)
- Sort rotations: O(n² log n) time (comparing strings is O(n))
- Extract last column: O(n) time
- Total: O(n² log n) time, O(n²) space

Suffix array method:
- Build suffix array: O(n log n) to O(n²) depending on algorithm
- Compute BWT from SA: O(n) time
- Total: O(n log n) time (with efficient SA algorithm), O(n) space

For DNA sequences that can be very long (millions of characters), the
suffix array method is much more practical.

References:
-----------
- Burrows, M.; Wheeler, D. (1994). "A block-sorting lossless data compression algorithm"
- Used in: bzip2, BWA, Bowtie, FM-index
- Related to: Suffix arrays, FM-index, compressed suffix trees
"""

def demonstrate_bwt():
    """Interactive demonstration of BWT algorithm."""
    
    print(__doc__)
    
    # Simple interactive demo
    print("\n" + "=" * 70)
    print("INTERACTIVE DEMONSTRATION")
    print("=" * 70)
    
    text = "ABC$"
    print(f"\nText: '{text}'")
    print(f"Length: {len(text)}")
    
    # Generate rotations
    n = len(text)
    rotations = [text[i:] + text[:i] for i in range(n)]
    
    print("\nStep 1: Generate all cyclic rotations")
    for i, rot in enumerate(rotations):
        print(f"  {i}: {rot}")
    
    # Sort rotations
    rotations.sort()
    
    print("\nStep 2: Sort rotations lexicographically")
    for i, rot in enumerate(rotations):
        print(f"  {i}: {rot}")
    
    # Extract last column
    bwt_result = [rot[-1] for rot in rotations]
    
    print("\nStep 3: Extract last column (BWT)")
    for i, rot in enumerate(rotations):
        print(f"  {rot} → '{rot[-1]}'")
    
    print(f"\nBWT: {bwt_result}")
    print(f"As string: '{''.join(bwt_result)}'")
    
    print("\n" + "=" * 70)
    print("Notice how BWT rearranges the text!")
    print("Original: ABC$")
    print("BWT:      C$AB")
    print("The characters are permuted to group similar patterns together.")
    print("=" * 70)


if __name__ == "__main__":
    demonstrate_bwt()
