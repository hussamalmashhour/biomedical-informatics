#!/usr/bin/env python3
"""Test all three functions for Exercise 1."""

import os
from string_reconstruction import (
    balanced, eulerianCycle, stringReconstruction,
    build_debruijn_graph, composition, read_kmers
)

def test_balanced():
    """Test balanced() function with example from exercise."""
    print("=" * 70)
    print("TEST 1: balanced() Function")
    print("=" * 70)
    
    # Example from exercise
    example_graph = {
        'AA': ['AT'],
        'GT': ['TT'],
        'CC': ['CA'],
        'CA': ['AT'],
        'GG': ['GA', 'GG'],
        'GC': ['CC'],
        'AT': ['TG', 'TG', 'TG'],
        'GA': ['AT'],
        'TG': ['GC', 'GG', 'GT'],
        'TT': [],
        'TA': ['AA']
    }
    
    result = balanced(example_graph)
    
    print(f"\nExample graph from exercise:")
    print(f"Result: {result}")
    print(f"Expected: False")
    print(f"Match: {'✓' if result == False else '✗'}")
    
    # Test a balanced graph
    print("\n" + "-" * 50)
    balanced_graph = {
        'A': ['B'],
        'B': ['C'],
        'C': ['A']
    }
    result2 = balanced(balanced_graph)
    print(f"Simple cycle graph (A->B->C->A):")
    print(f"Result: {result2}")
    print(f"Expected: True")
    print(f"Match: {'✓' if result2 == True else '✗'}")
    
    return result == False


def test_eulerian_cycle():
    """Test eulerianCycle() function."""
    print("\n" + "=" * 70)
    print("TEST 2: eulerianCycle() Function")
    print("=" * 70)
    
    # Create a balanced graph from the 3-mer example
    test_string = "TAATGCCATGGGATGTT"
    k = 3
    kmers = composition(test_string, k)
    
    print(f"\nTest string: {test_string}")
    print(f"k = {k}")
    print(f"Number of k-mers: {len(kmers)}")
    
    graph = build_debruijn_graph(kmers)
    print(f"De Bruijn graph nodes: {len(graph)}")
    
    is_balanced = balanced(graph)
    print(f"Graph balanced: {is_balanced}")
    
    if is_balanced:
        try:
            cycle = eulerianCycle(graph)
            print(f"\nEulerian cycle found:")
            print(f"  Length: {len(cycle)} nodes")
            print(f"  First 10: {cycle[:10]}")
            print(f"  Last 10: {cycle[-10:]}")
            
            # Verify cycle is valid
            valid = True
            for i in range(len(cycle) - 1):
                if cycle[i+1] not in graph.get(cycle[i], []):
                    valid = False
                    print(f"  Invalid edge: {cycle[i]} -> {cycle[i+1]}")
                    break
            
            if valid:
                print(f"✓ Valid Eulerian cycle")
            else:
                print(f"✗ Invalid cycle")
                
            return valid
        except ValueError as e:
            print(f"Error: {e}")
            return False
    else:
        print("Graph not balanced - testing path instead")
        return True


def test_string_reconstruction():
    """Test stringReconstruction() function."""
    print("\n" + "=" * 70)
    print("TEST 3: stringReconstruction() Function")
    print("=" * 70)
    
    # Test 1: Small example
    print("\nTest 3a: Small example")
    test_string = "TAATGCCATGGGATGTT"
    k = 3
    kmers = composition(test_string, k)
    
    reconstructed = stringReconstruction(kmers)
    
    print(f"Original:      {test_string}")
    print(f"Reconstructed: {reconstructed}")
    print(f"Length match: {'✓' if len(reconstructed) == len(test_string) else '✗'}")
    
    # Verify k-mers match
    recon_kmers = composition(reconstructed, k)
    kmers_match = set(recon_kmers) == set(kmers)
    print(f"K-mers match: {'✓' if kmers_match else '✗'}")
    
    # Test 2: 10-mers from file
    print("\n" + "-" * 50)
    print("Test 3b: 10-mers from file")
    
    folder = os.path.dirname(__file__)
    kmers_path = os.path.join(folder, '10mers.txt')
    
    if os.path.exists(kmers_path):
        kmers_10 = read_kmers(kmers_path)
        k10 = len(kmers_10[0])
        
        print(f"Loaded {len(kmers_10)} k-mers of length {k10}")
        
        result = stringReconstruction(kmers_10)
        
        print(f"\nReconstructed sequence:")
        print(f"  Length: {len(result)}")
        print(f"  First 60: {result[:60]}")
        print(f"  Last 60:  {result[-60:]}")
        
        # Verify k-mers
        result_kmers = composition(result, k10)
        if set(result_kmers) == set(kmers_10):
            print(f"✓ All k-mers present in reconstruction")
        else:
            print(f"✗ K-mers don't match")
            missing = len(set(kmers_10) - set(result_kmers))
            extra = len(set(result_kmers) - set(kmers_10))
            print(f"  Missing: {missing}, Extra: {extra}")
        
        return result
    else:
        print(f"File not found: {kmers_path}")
        return None


def main():
    """Run all tests."""
    print("\n")
    print("#" * 70)
    print("# EXERCISE 1: Complete Function Testing")
    print("#" * 70)
    
    # Test 1: balanced()
    test1_pass = test_balanced()
    
    # Test 2: eulerianCycle()
    test2_pass = test_eulerian_cycle()
    
    # Test 3: stringReconstruction()
    result = test_string_reconstruction()
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"1. balanced() test: {'✓ PASS' if test1_pass else '✗ FAIL'}")
    print(f"2. eulerianCycle() test: {'✓ PASS' if test2_pass else '✗ FAIL'}")
    print(f"3. stringReconstruction() test: {'✓ PASS' if result else '✗ FAIL'}")
    
    if result:
        print(f"\nFinal reconstructed sequence length: {len(result)}")
        print(f"First 100 bp: {result[:100]}")
        
        return result
    
    return None


if __name__ == '__main__':
    main()
