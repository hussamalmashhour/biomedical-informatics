#!/usr/bin/env python3
"""
Submission script for Exercise 5 - Gene Annotations
Generates the submission URL with gene annotations for the test case.
"""

import json
import os
import sys

# Add parent directory to path to import config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
import config

# Import the annotations function
from annotations import annotations


def run_test_case():
    """Run the test case from the exercise."""
    print("=" * 70)
    print("EXERCISE 5 - GENE ANNOTATIONS")
    print("=" * 70)
    
    # Test case from exercise
    ids = ['YPR184W', 'YLR312C', 'YML054C', 'YBR116C', 'YKL187C',
           'YLR267W', 'YEL012W', 'YOL084W', 'YJL045W', 'YJR095W']
    
    print(f"\nTest Case:")
    print(f"  Input genes: {len(ids)}")
    print(f"  IDs: {ids}")
    
    print(f"\nParsing GFF file...")
    result = annotations(ids)
    
    print(f"\nResults:")
    print("-" * 70)
    
    if len(result) == 0:
        print("ERROR: No genes found!")
        return None
    
    print(f"Found annotations for {len(result)} genes:\n")
    
    for gene_id in sorted(result.keys()):
        info = result[gene_id]
        print(f"  {gene_id}:")
        print(f"    name: {info['name']}")
        print(f"    id: {info['id']}")
        print(f"    start: {info['start']}")
        print(f"    end: {info['end']}")
        print()
    
    return result


def format_annotations_for_submission(result):
    """
    Format annotations dictionary for API submission.
    
    The API expects nested dictionaries with string values.
    Format: {'YER065C': {'start': '285241', 'end': '286914', 'name': 'ICL1', 'id': 'S000000867'}}
    """
    formatted = {}
    for gene_id, info in result.items():
        # Only include the required fields: start, end, name, id
        formatted[gene_id] = {
            'start': str(info['start']),
            'end': str(info['end']),
            'name': str(info['name']),
            'id': str(info['id'])
        }
    
    return formatted


def build_submission_url(result):
    """Build the submission URL for the annotations exercise."""
    # Get exercise info from config
    session, exercise, description = config.get_exercise_info("annotations_tema5_eje5")
    
    # Format result
    response = format_annotations_for_submission(result)
    
    # Build URL using config helper
    url = config.build_test_url(session, exercise, response)
    
    return url


def main():
    print("=" * 70)
    print("GENE ANNOTATIONS - SUBMISSION GENERATOR")
    print("=" * 70)
    
    # Run test case
    result = run_test_case()
    
    if result is None:
        return
    
    # Build submission URL
    url = build_submission_url(result)
    
    print("\n" + "=" * 70)
    print("SUBMISSION FORMAT")
    print("=" * 70)
    
    formatted_result = format_annotations_for_submission(result)
    print(f"\nAnnotations dictionary (simplified):")
    for gene_id in sorted(formatted_result.keys())[:3]:  # Show first 3
        info = formatted_result[gene_id]
        print(f"  '{gene_id}': {info}")
    print(f"  ... ({len(formatted_result)} genes total)")
    
    print("\n" + "=" * 70)
    print("SUBMISSION URL")
    print("=" * 70)
    print(f"\n{url}")
    
    print("\n" + "=" * 70)
    print("EXPLANATION")
    print("=" * 70)
    print("""
Gene Annotations Parser:

1. Input: List of yeast gene systematic names (e.g., YER065C)
2. Parse GFF file (SGD R64-2-1 version from 2015)
3. Extract for each gene:
   - start: Gene start coordinate
   - end: Gene end coordinate
   - name: Gene common name (from 'Name=' or 'gene=' field)
   - id: SGD database ID (from 'SGD=' field)
4. Return dictionary mapping gene IDs to their annotations

GFF Format:
  - Tab-delimited file with 9 columns
  - Column 9 contains attributes: ID=...; Name=...; SGD=...; etc.
  - Example: ID=YER065C;Name=ICL1;SGD=S000000867;...

Example Output:
  {'YER065C': {'start': '285241', 'end': '286914', 'name': 'ICL1', 'id': 'S000000867'}}

Data Source:
  - Saccharomyces Genome Database (SGD)
  - R64-2-1 version (January 2015)
  - File: saccharomyces_cerevisiae_R64-2-1_20150113.gff
    """)
    
    # Save to file
    output_file = os.path.join(os.path.dirname(__file__), 'submission_url.txt')
    with open(output_file, 'w') as f:
        f.write("Exercise 5 - Gene Annotations\n")
        f.write("=" * 70 + "\n\n")
        f.write("Submission URL:\n")
        f.write(url + "\n\n")
        f.write(f"Annotations for {len(result)} genes:\n")
        for gene_id in sorted(result.keys()):
            info = result[gene_id]
            f.write(f"  {gene_id}: {info['name']} ({info['id']})\n")
    
    print(f"\nOK URL also saved to: {output_file}")


if __name__ == "__main__":
    main()
