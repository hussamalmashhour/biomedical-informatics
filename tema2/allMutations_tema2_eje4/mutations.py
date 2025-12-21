#!/usr/bin/env python3
"""Generate all k-mers within d mismatches of a given word.

This module provides the mutationsEqualOrLess function which generates all
possible k-mers that differ from a given word by up to d positions (Hamming distance).

Example:
    mutationsEqualOrLess("ACG", "ACGT", 1) -> {"ACG", "CCG", "GCG", "TCG", "AAG", "AGG", ...}
"""


def mutationsEqualOrLess(word, letters, num_mismatches):
    """Generate all k-mers within num_mismatches of word using given alphabet.
    
    Args:
        word: reference k-mer string
        letters: alphabet to use (e.g., "ACGT")
        num_mismatches: maximum Hamming distance (allowed mismatches)
    
    Returns:
        Set of all k-mers that differ from word by 0 to num_mismatches positions.
    """
    if num_mismatches == 0:
        return {word}
    
    if len(word) == 0:
        return set()
    
    # Remove first character and recursively generate mutations for the rest
    first_char = word[0]
    suffix = word[1:]
    
    # Get all mutations of the suffix
    suffix_mutations = mutationsEqualOrLess(suffix, letters, num_mismatches)
    
    result = set()
    
    # Option 1: Keep the first character (0 mismatches at position 0)
    for mut in suffix_mutations:
        result.add(first_char + mut)
    
    # Option 2: If we have mismatches left, try all other letters at position 0
    if num_mismatches > 0:
        for letter in letters:
            if letter != first_char:
                # Use 1 mismatch at position 0, then allow (num_mismatches - 1) for the rest
                suffix_mutations_reduced = mutationsEqualOrLess(
                    suffix, letters, num_mismatches - 1
                )
                for mut in suffix_mutations_reduced:
                    result.add(letter + mut)
    
    return result
