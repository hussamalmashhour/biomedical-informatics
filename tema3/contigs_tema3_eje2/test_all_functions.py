#!/usr/bin/env python3
"""Test contigs() function with example and file data."""

import os
from contigs import contigs, build_debruijn_graph, compute_degrees, read_kmers

def composition(text, k):
    """Generate all k-mers from a string."""
    return [text[i:i+k] for i in range(len(text) - k + 1)]

def test_example():
    """Test with example from exercise."""
    print("=" * 70)
    print("TEST 1: Example from Exercise")
    print("=" * 70)
    
    test_string = "TAATGCCATGGGATGTT"
    k = 3
    test_kmers = composition(test_string, k)
    
    print(f"\nOriginal string: {test_string}")
    print(f"k = {k}")
    print(f"Number of k-mers: {len(test_kmers)}")
    print(f"K-mers: {test_kmers}")
    
    result = contigs(test_kmers)
    
    # Expected contigs from exercise
    expected = ['TAAT', 'ATG', 'ATG', 'ATG', 'TGTT', 'TGG', 'GGG', 'GGAT', 'TGCCAT']
    
    print(f"\nContigs found ({len(result)}):")
    for i, contig in enumerate(sorted(result)):
        print(f"  {i+1:2d}. {contig:10s} (length {len(contig)})")
    
    print(f"\nExpected contigs ({len(expected)}):")
    for i, contig in enumerate(sorted(expected)):
        print(f"  {i+1:2d}. {contig:10s} (length {len(contig)})")
    
    # Compare
    result_set = set(result)
    expected_set = set(expected)
    
    match = result_set == expected_set
    print(f"\nExact match: {'✓' if match else '✗'}")
    
    if not match:
        missing = expected_set - result_set
        extra = result_set - expected_set
        if missing:
            print(f"  Missing: {missing}")
        if extra:
            print(f"  Extra: {extra}")
    
    return match


def test_simple_cases():
    """Test simple edge cases."""
    print("\n" + "=" * 70)
    print("TEST 2: Simple Cases")
    print("=" * 70)
    
    # Test 2a: Linear chain
    print("\n2a. Linear chain (no branching)")
    linear_kmers = ["ABC", "BCD", "CDE", "DEF"]
    linear_result = contigs(linear_kmers)
    
    print(f"K-mers: {linear_kmers}")
    print(f"Contigs: {linear_result}")
    print(f"Expected: ['ABCDEF'] (single contig)")
    print(f"Match: {'✓' if len(linear_result) == 1 and linear_result[0] == 'ABCDEF' else '✗'}")
    
    # Test 2b: Simple branching
    print("\n2b. Branching")
    branch_kmers = ["AB", "BC", "AD", "DC"]
    branch_result = contigs(branch_kmers)
    
    print(f"K-mers: {branch_kmers}")
    print(f"Contigs: {sorted(branch_result)}")
    print(f"Expected: 4 contigs (each edge is a contig)")


def test_10mers():
    """Test with 10-mers file."""
    print("\n" + "=" * 70)
    print("TEST 3: 10-mers Data File")
    print("=" * 70)
    
    folder = os.path.dirname(__file__)
    kmers_path = os.path.join(folder, '10mers.txt')
    
    if not os.path.exists(kmers_path):
        print(f"File not found: {kmers_path}")
        return None, None
    
    kmers = read_kmers(kmers_path)
    k = len(kmers[0])
    
    print(f"\nLoaded {len(kmers)} k-mers of length {k}")
    
    result = contigs(kmers)
    
    print(f"\nContigs found: {len(result)}")
    
    if result:
        lengths = sorted([len(c) for c in result])
        print(f"Lengths (sorted): {lengths}")
        
        print(f"\nStatistics:")
        print(f"  Shortest: {min(lengths)} bp")
        print(f"  Longest:  {max(lengths)} bp")
        print(f"  Average:  {sum(lengths)/len(lengths):.1f} bp")
        print(f"  Total:    {sum(lengths)} bp")
        
        print(f"\nContigs details:")
        for i, contig in enumerate(result):
            preview = contig[:60] + "..." if len(contig) > 60 else contig
            print(f"  {i+1}. Length {len(contig):3d}: {preview}")
    
    return len(result), lengths if result else []


def analyze_graph():
    """Analyze the de Bruijn graph structure."""
    print("\n" + "=" * 70)
    print("GRAPH ANALYSIS")
    print("=" * 70)
    
    folder = os.path.dirname(__file__)
    kmers_path = os.path.join(folder, '10mers.txt')
    
    if not os.path.exists(kmers_path):
        return
    
    kmers = read_kmers(kmers_path)
    graph = build_debruijn_graph(kmers)
    indegree, outdegree = compute_degrees(graph)
    
    print(f"\nGraph statistics:")
    print(f"  Total nodes: {len(set(indegree) | set(outdegree))}")
    print(f"  Nodes with edges: {len(graph)}")
    
    # Count nodes by degree type
    balanced = 0
    branching_in = 0
    branching_out = 0
    both_branching = 0
    
    for node in set(indegree) | set(outdegree):
        ind = indegree[node]
        outd = outdegree[node]
        
        if ind == 1 and outd == 1:
            balanced += 1
        elif ind != 1 and outd != 1:
            both_branching += 1
        elif ind != 1:
            branching_in += 1
        elif outd != 1:
            branching_out += 1
    
    print(f"\nNode degree distribution:")
    print(f"  Balanced (in=1, out=1): {balanced}")
    print(f"  In-branching (in≠1):    {branching_in}")
    print(f"  Out-branching (out≠1):  {branching_out}")
    print(f"  Both branching:         {both_branching}")
    
    # Show some branching nodes
    print(f"\nSample branching nodes (first 10):")
    count = 0
    for node in sorted(graph.keys()):
        if indegree[node] != 1 or outdegree[node] != 1:
            print(f"  {node}: in={indegree[node]}, out={outdegree[node]}, neighbors={graph[node][:3]}...")
            count += 1
            if count >= 10:
                break


def main():
    """Run all tests."""
    print("\n")
    print("#" * 70)
    print("# EXERCISE 2: Contigs Testing")
    print("#" * 70)
    
    # Test 1: Example
    test1_pass = test_example()
    
    # Test 2: Simple cases
    test_simple_cases()
    
    # Test 3: 10-mers
    num_contigs, lengths = test_10mers()
    
    # Test 4: Graph analysis
    analyze_graph()
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"1. Example test: {'✓ PASS' if test1_pass else '✗ FAIL'}")
    print(f"2. 10-mers test: {'✓ PASS' if num_contigs else '✗ FAIL'}")
    
    if num_contigs:
        print(f"\nAnswer for Exercise 2:")
        print(f"  Number of contigs: {num_contigs}")
        print(f"  Contig lengths: {lengths}")
        
        return num_contigs, lengths
    
    return None, None


if __name__ == '__main__':
    main()
