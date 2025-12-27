#!/usr/bin/env python3
"""Gibbs Sampler for Motif Search (Tema 2 - Exercise 11).

Algorithm (per instructions):
1) Initialize motifs by choosing a random k-mer from each DNA string.
2) bestMotifs = motifs.
3) Repeat N iterations:
   a) Pick a random index i.
   b) Remove motifs[i].
   c) Build a Laplace-smoothed profile from the remaining motifs.
   d) Compute probability of every k-mer in dna[i] using Pr(profile, kmer).
   e) Sample a k-mer proportionally to these probabilities.
   f) Insert the sampled k-mer back; update bestMotifs if score improves.

Uses only standard Python and previously defined helpers (score, profile, Pr).
"""

import os
import random
from collections import Counter, defaultdict

# ------------------------------
# Helpers
# ------------------------------

def clean_line(line):
    """Strip whitespace and return uppercase DNA without spaces."""
    return ''.join(line.strip().split()).upper()


def read_sequences(path):
    """Read DNA sequences from file (one per line), ignoring empty lines."""
    sequences = []
    with open(path, 'r') as f:
        for raw in f:
            seq = clean_line(raw)
            if seq:
                sequences.append(seq)
    return sequences


def score(Dna):
    """Compute motif score (sum of non-consensus counts per column)."""
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
    for s in Dna:
        if len(s) != n:
            raise ValueError("All strings must have equal length")

    add = 1 if Laplace else 0
    denom = t + 4 * add
    prof = {b: [] for b in "ACGT"}

    for i in range(n):
        counts = defaultdict(int)
        if add:
            for b in "ACGT":
                counts[b] = add
        for s in Dna:
            counts[s[i]] += 1
        for b in "ACGT":
            prof[b].append(counts[b] / denom)
    return prof


def Pr(prof, motif):
    """Compute probability of motif given profile."""
    prob = 1.0
    for i, base in enumerate(motif):
        prob *= prof[base][i]
    return prob


def consensus(motifs):
    """Return consensus string (alphabetical tie-break)."""
    if not motifs:
        return ""
    n = len(motifs[0])
    result = []
    for i in range(n):
        column = [m[i] for m in motifs]
        counts = Counter(column)
        best_base = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
        result.append(best_base)
    return ''.join(result)


def random_kmer(seq, k):
    """Pick a random k-mer from seq."""
    start = random.randint(0, len(seq) - k)
    return seq[start:start + k]


# ------------------------------
# Gibbs Sampler
# ------------------------------

def gibbsSampler_core(dna, k, N):
    """Run Gibbs sampling for motifs (returns list of motifs)."""
    t = len(dna)
    motifs = [random_kmer(seq, k) for seq in dna]
    bestMotifs = list(motifs)
    bestScore = score(bestMotifs)

    for _ in range(N):
        i = random.randrange(t)
        removed = motifs.pop(i)

        prof = profile(motifs, Laplace=True)

        seq = dna[i]
        kmers = []
        weights = []
        for start in range(len(seq) - k + 1):
            kmer = seq[start:start + k]
            kmers.append(kmer)
            weights.append(Pr(prof, kmer))

        # Sample according to weights (Laplace ensures weights > 0)
        chosen = random.choices(kmers, weights=weights, k=1)[0]
        motifs.insert(i, chosen)

        cur_score = score(motifs)
        if cur_score < bestScore:
            bestScore = cur_score
            bestMotifs = list(motifs)

    return bestMotifs


def gibbsSampler(dna, k, N, num_runs=50):
    """Run Gibbs sampling and return consensus sequence.
    
    Args:
        dna: list of DNA sequences
        k: motif length
        N: iterations per run
        num_runs: number of times to run algorithm
    
    Returns:
        Consensus sequence (string) of best motifs found.
    """
    best_motifs = None
    best_score = float('inf')
    
    for _ in range(num_runs):
        motifs = gibbsSampler_core(dna, k, N)
        sc = score(motifs)
        if sc < best_score:
            best_score = sc
            best_motifs = motifs
    
    # Return consensus string, not list
    return consensus(best_motifs)


def run_multiple(dna, k, N, runs):
    """Run gibbsSampler multiple times and return consensus with score."""
    best = None
    best_score = float('inf')
    for r in range(runs):
        motifs = gibbsSampler_core(dna, k, N)
        sc = score(motifs)
        if sc < best_score:
            best_score = sc
            best = motifs
    return consensus(best), best_score


# ------------------------------
# Main / Tests
# ------------------------------

def run_example(folder):
    """Example with k=7, N=100, 50 runs. Expects consensus GATTACA."""
    path = os.path.join(folder, 'secuencias.txt')
    if not os.path.exists(path):
        print(f"Example skipped: file not found {path}\n")
        return
    dna = read_sequences(path)
    k = 7
    N = 100
    runs = 50
    cons, sc = run_multiple(dna, k, N, runs)
    print("Example (secuencias.txt):")
    print(f"  k={k}, N={N}, runs={runs}")
    print(f"  Score: {sc}")
    print(f"  Consensus: {cons} (expected GATTACA)")
    print()


def run_test_secuencias2(folder):
    """Test with secuencias2.txt: k=8, N=100, runs=50."""
    path = os.path.join(folder, 'secuencias2.txt')
    if not os.path.exists(path):
        print(f"Test skipped: file not found {path}\n")
        return
    dna = read_sequences(path)
    k = 8
    N = 100
    runs = 50
    cons, sc = run_multiple(dna, k, N, runs)
    print("Test (secuencias2.txt):")
    print(f"  k={k}, N={N}, runs={runs}")
    print(f"  Score: {sc}")
    print(f"  Consensus: {cons}")
    print()


def main():
    folder = os.path.dirname(__file__)
    # Optional: set a seed for reproducibility; comment out for randomness
    # random.seed(0)
    run_example(folder)
    run_test_secuencias2(folder)


if __name__ == '__main__':
    main()
