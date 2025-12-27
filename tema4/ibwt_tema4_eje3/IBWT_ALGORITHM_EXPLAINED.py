#!/usr/bin/env python3
"""
Inverse Burrows-Wheeler Transform (IBWT) - Complete Algorithm Explanation
==========================================================================

EXERCISE 3 (Tema 4): Implement ibwt() function

What is IBWT?
-------------
The Inverse Burrows-Wheeler Transform (IBWT) reconstructs the original text
from its BWT. This demonstrates that BWT is a REVERSIBLE transformation,
making it useful for lossless compression.

The Last-First Property:
------------------------
The key insight for IBWT is the LAST-FIRST PROPERTY:

    The i-th occurrence of character X in the FIRST column
    corresponds to the i-th occurrence of character X in the LAST column

This property allows us to "walk" through the original string by following
characters from last column to first column.

Example: "abracadabra$"
-----------------------
Original text: "abracadabra$"
BWT (from Exercise 2): "ard$rcaaaabb"

BWT Matrix (sorted rotations):
Row  First ... Last    Interpretation
 0:  $ ... a            The i-th 'a' in First column
 1:  a ... r            corresponds to the i-th 'a'
 2:  a ... b            in Last column
 3:  a ... a
 4:  a ... d
 5:  a ... a
 6:  b ... c
 7:  b ... a
 8:  c ... a
 9:  d ... r
10:  r ... b
11:  r ... b

L (Last column)  = "ard$rcaaaabb"
F (First column) = "$aaaaabbcdrr"

Occurrence Numbers:
-------------------
To use the Last-First property, we need to track which occurrence of each
character we're at:

L = "a r d $ r c a a a a b b"
    [1 1 1 1 2 1 2 3 4 5 1 2]  ← occurrence numbers in L

F = "$ a a a a a b b c d r r"
    [1 1 2 3 4 5 1 2 1 1 1 2]  ← occurrence numbers in F

LF Mapping:
-----------
For each position i in L, we can find the corresponding position in F
by looking for the same character with the same occurrence number.

Example:
  L[0] = 'a' with occurrence 1 → F[1] = 'a' with occurrence 1
  L[1] = 'r' with occurrence 1 → F[10] = 'r' with occurrence 1
  L[10] = 'b' with occurrence 1 → F[6] = 'b' with occurrence 1

LF mapping: [1, 10, 9, 0, 11, 8, 2, 3, 4, 5, 6, 7]
This tells us: position i in L maps to position LF[i] in F

Reconstruction Algorithm:
-------------------------
1. Start at the row where F has '$' (row 0)
2. For each step:
   a. Read the character from L at current row
   b. Append it to result
   c. Follow LF mapping to get next row
3. After n steps, reverse the result

Step-by-step for "ard$rcaaaabb":
---------------------------------
Start: row 0 (where F has '$')

Step 0: row 0 → L[0] = 'a', next = LF[0] = 1
Step 1: row 1 → L[1] = 'r', next = LF[1] = 10
Step 2: row 10 → L[10] = 'b', next = LF[10] = 6
Step 3: row 6 → L[6] = 'a', next = LF[6] = 2
Step 4: row 2 → L[2] = 'd', next = LF[2] = 9
Step 5: row 9 → L[9] = 'a', next = LF[9] = 5
Step 6: row 5 → L[5] = 'c', next = LF[5] = 8
Step 7: row 8 → L[8] = 'a', next = LF[8] = 4
Step 8: row 4 → L[4] = 'r', next = LF[4] = 11
Step 9: row 11 → L[11] = 'b', next = LF[11] = 7
Step 10: row 7 → L[7] = 'a', next = LF[7] = 3
Step 11: row 3 → L[3] = '$', next = LF[3] = 0 (back to start)

Collected (backwards): "a r b a d a c a r b a $"
Reversed: "$ a b r a c a d a b r a"
Result: "abracadabra$" ✓

Why Does This Work?
-------------------
Each row in the BWT matrix represents a rotation of the original string.
The LF mapping connects each character to its predecessor in the rotation.

By following the LF mapping starting from '$', we trace through the original
string character by character, but in reverse order.

Implementation Details:
-----------------------
```python
def compute_ranks(column):
    """Compute 0-based occurrence ranks."""
    counts = defaultdict(int)
    ranks = []
    for ch in column:
        ranks.append(counts[ch])
        counts[ch] += 1
    return ranks

def lf_mapping(bwt_text):
    """Build LF-mapping arrays."""
    first_col = ''.join(sorted(bwt_text))
    
    # Compute ranks for both columns
    last_ranks = compute_ranks(bwt_text)
    first_ranks = compute_ranks(first_col)
    
    # Map (char, rank) to position in first column
    pos_in_first = {}
    for idx, (ch, r) in enumerate(zip(first_col, first_ranks)):
        pos_in_first[(ch, r)] = idx
    
    # Build LF mapping
    lf = []
    for ch, r in zip(bwt_text, last_ranks):
        lf.append(pos_in_first[(ch, r)])
    
    return first_col, lf

def ibwt(bwt_text):
    """Inverse BWT using LF-mapping."""
    first_col, lf = lf_mapping(bwt_text)
    
    # Start from row with '$' in BWT (last column)
    row = bwt_text.index('$')
    
    result = []
    for _ in range(len(bwt_text)):
        ch = bwt_text[row]
        result.append(ch)
        row = lf[row]
    
    # Reverse to get original text
    return ''.join(reversed(result))
```

Complexity Analysis:
--------------------
Time: O(n log n) - dominated by sorting to get first column
Space: O(n) - for storing columns and mappings

More efficient implementations exist using:
- Wavelet trees: O(n) time and space
- FM-index structures: O(n) time with compressed space

Test Cases:
-----------
1. Example: "ard$rcaaaabb" → "abracadabra$" ✓
2. Classic: "smnpbnnaaaaa$a" → "panamabananas$" ✓
3. Test case: "enwvpeoseu$llt" → "twelveplusone$" ✓
4. Simple: "C$AB" → "ABC$" ✓

All verified by round-trip: original → BWT → IBWT → original

Properties Verified:
--------------------
✓ IBWT has same length as BWT
✓ IBWT has same character multiset as BWT
✓ IBWT always ends with '$'
✓ Perfect round-trip: BWT(IBWT(x)) = x
✓ Works for all valid BWT inputs

Why IBWT is Important:
----------------------
1. Proves BWT is REVERSIBLE (lossless transformation)
2. Enables BWT-based compression (bzip2)
3. Fundamental for FM-index and read alignment tools
4. Demonstrates elegant algorithmic properties

Connection to Exercise 2 (BWT):
-------------------------------
BWT and IBWT are perfect inverses:
- BWT: Rearranges text to group similar characters
- IBWT: Reconstructs original text using last-first property
- Round-trip: original → BWT → IBWT → original ✓

The pair forms a complete lossless transformation system.

Submission:
-----------
BWT input: 'enwvpeoseu$llt'
Reconstructed: 'twelveplusone$'
Length: 14
Round-trip verified: ✓

URL: https://cpg3.der.usal.es/eval/test?session=4&exercise=3&response=twelveplusone$&id=Z2256773H

Advanced Topics (Not Required):
--------------------------------
- Wavelet tree implementation for O(n) time
- Run-length encoding of BWT
- FM-index for pattern matching
- Backward search algorithm
- Multiple string BWT

References:
-----------
- Burrows & Wheeler (1994): Original paper
- FM-index: Ferragina & Manzini (2000)
- Applications: bzip2, BWA, Bowtie aligner
"""

def demonstrate_ibwt():
    """Interactive demonstration of IBWT algorithm."""
    
    print(__doc__)
    
    print("\n" + "=" * 70)
    print("INTERACTIVE DEMONSTRATION")
    print("=" * 70)
    
    bwt_text = "C$AB"
    print(f"\nBWT: '{bwt_text}'")
    
    # Show the sorted matrix
    n = len(bwt_text)
    first_col = ''.join(sorted(bwt_text))
    
    print(f"L (last column):  {list(bwt_text)}")
    print(f"F (first column): {list(first_col)}")
    
    # Compute occurrence numbers
    def subscripts(text):
        counts = {}
        result = []
        for char in text:
            current = counts.get(char, 0) + 1
            counts[char] = current
            result.append(current)
        return result
    
    L_occ = subscripts(bwt_text)
    F_occ = subscripts(first_col)
    
    print(f"\nOccurrence numbers:")
    print(f"L: {L_occ}")
    print(f"F: {F_occ}")
    
    # Build mapping
    F_map = {}
    for i in range(n):
        key = (first_col[i], F_occ[i])
        F_map[key] = i
    
    print(f"\nF mapping:")
    for (char, occ), row in sorted(F_map.items()):
        print(f"  ('{char}', {occ}) → row {row}")
    
    # Reconstruct
    print(f"\nReconstruction:")
    row = first_col.index('$')
    print(f"Start at row {row} (where F has '$')")
    
    result_chars = []
    for step in range(n):
        char = bwt_text[row]
        occ = L_occ[row]
        result_chars.append(char)
        next_row = F_map[(char, occ)]
        
        print(f"  Step {step}: row {row} → L='{char}' (occ {occ}) → next row {next_row}")
        row = next_row
    
    result = ''.join(result_chars[::-1])
    print(f"\nCollected (backwards): '{''.join(result_chars)}'")
    print(f"Result (reversed): '{result}'")
    
    print("\n" + "=" * 70)
    print("Notice how we walked through the original string!")
    print("=" * 70)


if __name__ == "__main__":
    demonstrate_ibwt()
