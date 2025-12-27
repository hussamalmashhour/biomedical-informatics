#!/usr/bin/env python3
"""Generate submission URL for Exercise 6 - GO Functions Parser."""

import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from config import STUDENT_ID, API_BASE_URL
from functions import functions


def generate_submission_url():
    """Generate submission URL for Exercise 6."""
    
    # Test genes from exercise requirements
    test_genes = ['YPR184W', 'YLR312C', 'YML054C', 'YBR116C', 'YKL187C',
                  'YLR267W', 'YEL012W', 'YOL084W', 'YJL045W', 'YJR095W']
    
    # Run functions
    print("Running functions() with test genes...")
    result = functions(test_genes)
    
    # Display result
    print("\nResult:")
    for sgd_id in sorted(result.keys()):
        terms = sorted(list(result[sgd_id]))
        print(f"  {sgd_id}: set({terms})")
    
    # Build response as Python dict with set representation (not JSON)
    # Format: {'S000000320': set(), 'S000000738': set(['term1', 'term2'])}
    response_parts = []
    for sgd_id in sorted(result.keys()):
        terms = sorted(list(result[sgd_id]))
        if len(terms) == 0:
            response_parts.append(f"'{sgd_id}':set()")
        else:
            terms_str = ','.join(f"'{term}'" for term in terms)
            response_parts.append(f"'{sgd_id}':set([{terms_str}])")
    
    response_str = '{' + ','.join(response_parts) + '}'
    url = f"{API_BASE_URL}/test?session=5&exercise=6&response={response_str}&id={STUDENT_ID}"
    
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
