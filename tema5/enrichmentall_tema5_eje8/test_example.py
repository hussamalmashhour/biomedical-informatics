#!/usr/bin/env python3
"""Test enrichmentAll with example data."""
from enrichmentall import load_genes, enrichmentAll

# Load gene lists
c3 = load_genes('c3genes.txt')
ugenes = load_genes('ugenes.txt')

print(f'c3genes: {len(c3)} genes')
print(f'ugenes: {len(ugenes)} genes')

# Example test from exercise
print("\n" + "="*70)
print("EXAMPLE TEST")
print("="*70)
print("Parameters: a=10e-20, min=5, max=500, type='P'")
print()

result = enrichmentAll(ugenes, c3, 10e-20, 5, 500, 'P')

print(f"\nTotal enriched terms: {len(result)}")

if result:
    print("\nTop result:")
    print(f"  name: {result[0]['name']}")
    print(f"  pval: {result[0]['pval']}")
    print(f"  ngis: {result[0]['ngis']}")
    print(f"  ngo: {result[0]['ngo']}")
    
    print("\nExpected:")
    print("  name: cytoplasmic translation")
    print("  pval: 8.43491843768445e-26")
    print("  ngis: 45")
    print("  ngo: 170")
    
    # Check if matches
    if result[0]['name'] == 'cytoplasmic translation':
        print("\n✓ Name matches!")
    if result[0]['ngis'] == 45:
        print("✓ ngis matches!")
    if result[0]['ngo'] == 170:
        print("✓ ngo matches!")
    if abs(result[0]['pval'] - 8.43491843768445e-26) < 1e-30:
        print("✓ pval matches!")
else:
    print("No results found!")
