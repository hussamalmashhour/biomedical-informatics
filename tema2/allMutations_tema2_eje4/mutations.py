#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate all k-mers within d mismatches of a given word.

This module provides the mutations and mutationsEqualOrLess functions which generate all
possible k-mers that differ from a given word by up to d positions (Hamming distance).
"""

import itertools


def mutations(word, num_mismatches, letters="ACGT"):
    """
    Generator that yields all mutations of `word` with exactly `num_mismatches` point mutations.
    
    Args:
        word: reference k-mer string
        num_mismatches: exact number of mismatches
        letters: alphabet to use (default: "ACGT")
    
    Yields:
        All k-mers that differ from word by exactly num_mismatches positions.
    """
    for locs in itertools.combinations(range(len(word)), num_mismatches):
        this_word = [[char] for char in word]
        for loc in locs:
            orig_char = word[loc]
            this_word[loc] = [l for l in letters if l != orig_char]
        for poss in itertools.product(*this_word):
            yield ''.join(poss)


def mutationsEqualOrLess(word, num_mismatches, letters="ACGT"):
    """
    Returns a set of all mutations of `word` with up to `num_mismatches` point mutations.
    
    Args:
        word: reference k-mer string
        num_mismatches: maximum number of mismatches
        letters: alphabet to use (default: "ACGT")
    
    Returns:
        Set of all k-mers that differ from word by 0 to num_mismatches positions.
    """
    matches = set()
    for dd in range(num_mismatches, -1, -1):
        matches.update(list(mutations(word, dd, letters)))
    return matches
