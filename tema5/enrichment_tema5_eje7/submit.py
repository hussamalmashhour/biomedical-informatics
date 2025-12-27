#!/usr/bin/env python3
"""Generate submission URL for Exercise 7 - Gene Set Enrichment Analysis."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from config import STUDENT_ID, API_BASE_URL
from enrichment import enrichment, load_dgenes


def generate_submission_url():
    """Generate submission URL for Exercise 7."""
    
    # Test case from exercise requirements
    print("Running enrichment() with test data...")
    print("=" * 70)
    
    # Load dgenes from file
    dgenes_file = os.path.join(os.path.dirname(__file__), 'dgenes.txt')
    dgenes = load_dgenes(dgenes_file)
    
    print(f"Loaded dgenes: {len(dgenes)} genes")
    
    # GO:0006066 genes (alcohol metabolic process)
    goids = {'S000000056', 'S000000080', 'S000000702', 'S000000826', 'S000004937'}
    
    print(f"GO:0006066 genes: {len(goids)} genes")
    print(f"Genes: {sorted(goids)}")
    
    # Universe size
    n = 6034
    print(f"Universe size (n): {n}")
    
    # Run enrichment
    p_value, contingency, odds_ratio = enrichment(dgenes, goids, n)
    
    print(f"\nResults:")
    print(f"  Contingency Table: {contingency}")
    print(f"  Odds Ratio: {odds_ratio:.6f}")
    print(f"  P-value: {p_value:.6f}")
    
    # Generate submission URL
    # The response should be just the p-value
    url = f"{API_BASE_URL}/test?session=5&exercise=7&response={p_value}&id={STUDENT_ID}"
    
    print(f"\n{'=' * 70}")
    print("SUBMISSION URL:")
    print('=' * 70)
    print(url)
    print('=' * 70)
    
    # Save to file
    output_file = os.path.join(os.path.dirname(__file__), 'submission_url.txt')
    with open(output_file, 'w') as f:
        f.write(url)
    
    print(f"\nURL saved to: {output_file}")
    
    return url


if __name__ == '__main__':
    generate_submission_url()
