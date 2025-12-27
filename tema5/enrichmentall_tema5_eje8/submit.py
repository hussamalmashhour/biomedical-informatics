#!/usr/bin/env python3
"""Generate submission URL for Exercise 8 - Comprehensive Enrichment Analysis."""

import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from config import STUDENT_ID, API_BASE_URL
from enrichmentall import load_genes, enrichmentAll


def generate_submission_url():
    """Generate submission URL for Exercise 8."""
    
    # Load gene lists
    print("Loading gene lists...")
    ugenes = load_genes('ugenes.txt')
    random_genes = load_genes('randomGenes.txt')
    
    print(f"  ugenes: {len(ugenes)} genes")
    print(f"  randomGenes: {len(random_genes)} genes\n")
    
    # Test case from exercise requirements
    print("="*70)
    print("TEST CASE: randomGenes enrichment")
    print("="*70)
    print("Parameters: a=0.01, min=5, max=500, type='P'\n")
    
    # Run enrichmentAll
    result = enrichmentAll(ugenes, random_genes, 0.01, 5, 500, 'P')
    
    print(f"Enriched terms: {len(result)}\n")
    
    if result:
        print("Top 5 enriched GO terms:")
        for i, term in enumerate(result[:5], 1):
            print(f"  {i}. {term['name']}")
            print(f"     p-value: {term['pval']:.2e}, ngis: {term['ngis']}/{term['ngo']}\n")
    else:
        print("No significant enrichment found\n")
    
    # The response should be the list of enriched terms
    # Convert to proper format for submission
    response_str = json.dumps(result, separators=(',', ':'))
    
    # Generate submission URL
    url = f"{API_BASE_URL}/test?session=5&exercise=8&response={response_str}&id={STUDENT_ID}"
    
    print("="*70)
    print("SUBMISSION URL:")
    print("="*70)
    print(url[:200] + "..." if len(url) > 200 else url)
    print("="*70)
    
    # Save to file
    output_file = os.path.join(os.path.dirname(__file__), 'submission_url.txt')
    with open(output_file, 'w') as f:
        f.write(url)
    
    print(f"\nURL saved to: {output_file}")
    
    # Also save results as JSON for reference
    results_file = os.path.join(os.path.dirname(__file__), 'submission_results.json')
    with open(results_file, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"Results saved to: {results_file}")
    
    return url


if __name__ == '__main__':
    generate_submission_url()
