#!/usr/bin/env python3
"""Greedy Motif Search (Tema 2 - Exercise 10).

Functions
---------
- score(Dna): compute motif score
- profile(Dna, Laplace=True): build profile with optional smoothing
- Pr(profile, motif): probability of a motif under the profile
- mostProbableKmer(profile, text, k): find k-mer with highest probability
- greedyMotifSearch(dna, k): greedy motif search algorithm
- read_sequences(path): read DNA sequences from file (one per line)

Algorithm
---------
Greedy Motif Search:
1. Initialize bestMotifs as the first k-mer of each sequence
2. For each k-mer in the first sequence:
   a. Set motifs[0] to this k-mer
   b. For i = 1 to t-1:
      - Build profile from motifs[0:i] (Laplace-smoothed)
      - Find most probable k-mer in dna[i]
      - Add to motifs
   c. If score(motifs) < score(bestMotifs), update bestMotifs
3. Return bestMotifs
"""

import os
from collections import Counter, defaultdict


def clean_line(line):
    """Strip whitespace and return uppercase DNA without spaces."""
    return ''.join(line.strip().split()).upper()


def read_sequences(path):
    """Read DNA sequences from file (one per line), ignoring empty lines."""
    sequences = []
    with open(path, 'r') as f:
        for raw in f:
            seq = clean_line(raw)
            if not seq:
                continue
            sequences.append(seq)
    return sequences


def score(Dna):
    """Compute motif score (sum of non-consensus frequencies per column)."""
    if not Dna:
        return 0

    t = len(Dna)
    n = len(Dna[0])

    total = 0
    for i in range(n):
        column = [dna[i] for dna in Dna]
        counts = Counter(column)
        max_freq = max(counts.values())
        total += t - max_freq
    return total


def profile(Dna, Laplace=True):
    """Build a profile matrix with optional Laplace smoothing."""
    if not Dna:
        return {b: [] for b in "ACGT"}

    t = len(Dna)
    n = len(Dna[0])

    # Validate equal lengths
    for s in Dna:
        if len(s) != n:
            raise ValueError("All strings must have equal length")

    add = 1 if Laplace else 0
    denom = t + 4 * add

    profile_dict = {b: [] for b in "ACGT"}

    for i in range(n):
        counts = defaultdict(int)
        # Initialize with Laplace pseudo-counts if needed
        if add:
            for b in "ACGT":
                counts[b] = add
        for s in Dna:
            counts[s[i]] += 1
        for b in "ACGT":
            profile_dict[b].append(counts[b] / denom)

    return profile_dict


def Pr(profile, motif):
    """Compute probability of motif given profile."""
    prob = 1.0
    for i, base in enumerate(motif):
        prob *= profile[base][i]
    return prob


def mostProbableKmer(profile, text, k):
    """Return the k-mer in text with highest probability under profile."""
    best_kmer = text[:k]
    best_prob = Pr(profile, best_kmer)

    for i in range(1, len(text) - k + 1):
        kmer = text[i:i + k]
        p = Pr(profile, kmer)
        if p > best_prob:
            best_prob = p
            best_kmer = kmer
    return best_kmer


def greedyMotifSearch(dna, k):
    """Greedy motif search algorithm.
    
    Args:
        dna: list of t DNA strings
        k: motif length
    
    Returns:
        List of t motifs (k-mers) with minimum score.
    """
    t = len(dna)
    n = len(dna[0])
    
    # Initialize bestMotifs with first k-mer from each sequence
    bestMotifs = [dna[i][:k] for i in range(t)]
    bestScore = score(bestMotifs)

    # Iterate over all k-mers in the first sequence
    for i in range(n - k + 1):
        motifs = [dna[0][i:i + k]]  # Start with k-mer from first sequence

        # For each subsequent sequence
        for j in range(1, t):
            # Build profile from motifs found so far (Laplace-smoothed)
            prof = profile(motifs, Laplace=True)
            # Find most probable k-mer in dna[j]
            kmer = mostProbableKmer(prof, dna[j], k)
            motifs.append(kmer)

        # Check if this set of motifs is better
        cur_score = score(motifs)
        if cur_score < bestScore:
            bestScore = cur_score
            bestMotifs = motifs

    return bestMotifs


def test_example():
    """Run the provided example test."""
    dna = ['GGCGTTCAGGCA', 'AAGAATCAGTCA', 'CAAGGAGTTCGC',
           'CACGTCAATCAC', 'CAATAATATTCG']
    k = 3
    result = greedyMotifSearch(dna, k)
    print('Test Example (k=3):')
    print(f'Expected: [\'TTC\', \'ATC\', \'TTC\', \'ATC\', \'TTC\']')
    print(f'Result:   {result}')
    print(f'Score:    {score(result)}\n')


def test_seqs4mut():
    """Test with seqs4mut.txt (k=15)."""
    folder = os.path.dirname(__file__)
    path = os.path.join(folder, 'seqs4mut.txt')
    if os.path.exists(path):
        sequences = read_sequences(path)
        k = 15
        result = greedyMotifSearch(sequences, k)
        print(f'Test seqs4mut.txt (k={k}):')
        print(f'Number of sequences: {len(sequences)}')
        print(f'Sequence length: {len(sequences[0])} bp')
        print(f'Motif length: {k} bp')
        print(f'Motifs found:')
        for i, motif in enumerate(result):
            print(f'  {i}: {motif}')
        print(f'Score: {score(result)}\n')
    else:
        print(f'File not found: {path}\n')


def main():
    test_example()
    test_seqs4mut()


if __name__ == '__main__':
    main()
