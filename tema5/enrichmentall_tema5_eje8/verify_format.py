#!/usr/bin/env python3
"""Final verification of output format."""
from enrichmentall import load_genes, enrichmentAll

# Example test
print("EXAMPLE TEST - Verifying output format")
print("="*70)

c3 = load_genes('c3genes.txt')
ugenes = load_genes('ugenes.txt')

result = enrichmentAll(ugenes, c3, 10e-20, 5, 500, 'P')

print(f"Number of results: {len(result)}")
print()

if result:
    print("First result:")
    print(f"  Type: {type(result[0])}")
    print(f"  Keys: {sorted(result[0].keys())}")
    print(f"  Values:")
    for key in ['name', 'pval', 'ngis', 'ngo']:
        print(f"    {key}: {result[0][key]} (type: {type(result[0][key]).__name__})")

print("\nExpected format:")
print("  [{'name': str, 'pval': float, 'ngis': int, 'ngo': int}]")

print("\nOur format:")
print(f"  [{{'name': {type(result[0]['name']).__name__}, 'pval': {type(result[0]['pval']).__name__}, 'ngis': {type(result[0]['ngis']).__name__}, 'ngo': {type(result[0]['ngo']).__name__}}}]")

print("\n✓ Format matches!" if all(k in result[0] for k in ['name', 'pval', 'ngis', 'ngo']) else "✗ Format error!")

# Test case
print("\n" + "="*70)
print("TEST CASE - randomGenes")
print("="*70)
random_genes = load_genes('randomGenes.txt')
result_test = enrichmentAll(ugenes, random_genes, 0.01, 5, 500, 'P')

print(f"Number of enriched terms: {len(result_test)}")
if result_test:
    print("\nAll enriched terms:")
    for i, term in enumerate(result_test, 1):
        print(f"  {i}. {term['name']}: p={term['pval']:.4e}, ngis={term['ngis']}, ngo={term['ngo']}")
