#!/usr/bin/env python3
"""Gene Annotations Parser (Tema 5 - Ejercicio 5).

Implements the annotations function that parses a GFF file and extracts
gene information for a list of yeast gene names (systematic IDs).

The GFF (Generic Feature Format) file contains 9 tab-delimited columns:
1. seqname - Chromosome/sequence name
2. source - Program that generated the feature
3. feature - Feature type (ORF, transposon_end, etc.)
4. start - Start coordinate
5. end - End coordinate
6. score - Score value (. for ungapped, integer for gapped)
7. strand - Direction (+ or -)
8. frame - Reading frame (0, 1, or 2)
9. attributes - Semicolon-separated key-value pairs (ID, Name, SGD, dbxref, Note, etc.)

Complexity: O(n + m) where n = input IDs, m = GFF file lines.
"""

import os
import json


def parse_attributes(attr_string):
    """Parse the 9th field (attributes) of GFF into key-value pairs.
    
    Example:
        'ID=YER065C;Name=ICL1;SGD=S000000867;dbxref=SGD:S000000867;Note=...'
        → {'ID': 'YER065C', 'Name': 'ICL1', 'SGD': 'S000000867', ...}
    
    Args:
        attr_string: semicolon-separated key=value pairs
    
    Returns:
        dict of parsed attributes
    """
    attrs = {}
    for pair in attr_string.strip().split(';'):
        if '=' in pair:
            key, value = pair.split('=', 1)
            attrs[key] = value
        elif pair.strip():
            # Handle malformed pairs
            attrs[pair.strip()] = ''
    return attrs


def annotations(ids, gff_file='saccharomyces_cerevisiae_R64-2-1_20150113.gff'):
    """Extract annotation details for a list of yeast gene names.
    
    Args:
        ids: list or array of systematic gene names (e.g., ['YER065C', 'YPR184W'])
        gff_file: path to GFF annotation file (default: local SGD R64-2-1)
    
    Returns:
        dict mapping each input gene name to its annotation details:
        {
            'YER065C': {
                'start': '285241',
                'end': '286914',
                'name': 'ICL1',
                'id': 'S000000867'
            }
        }
    """
    # Convert to set for O(1) lookup
    id_set = set(ids) if not isinstance(ids, set) else ids
    
    # Dictionary to store results
    results = {gene_id: None for gene_id in ids}
    
    # Resolve file path
    if not os.path.isabs(gff_file):
        gff_file = os.path.join(os.path.dirname(__file__), gff_file)
    
    if not os.path.exists(gff_file):
        print(f"Error: GFF file not found: {gff_file}")
        return results
    
    # Parse GFF file
    with open(gff_file, 'r') as f:
        for line in f:
            # Skip comments
            if line.startswith('#'):
                continue
            
            # Skip empty lines
            line = line.rstrip('\n')
            if not line:
                continue
            
            # Parse tab-delimited fields
            fields = line.split('\t')
            if len(fields) < 9:
                continue
            
            seqname, source, feature, start, end, score, strand, frame, attributes = fields[:9]
            
            # Parse attributes
            attrs = parse_attributes(attributes)
            
            # Check if this is one of the genes we're looking for
            # Match by ID (systematic name) and feature type 'gene'
            gene_id = attrs.get('ID', '')
            if gene_id in id_set and feature == 'gene' and results[gene_id] is None:
                # Extract annotation details
                # Priority: gene field, then Name field, then ID
                name = attrs.get('gene', attrs.get('Name', gene_id))
                
                # Extract SGD ID from dbxref field (format: "SGD:S000000867")
                dbxref = attrs.get('dbxref', '')
                sgd_id = ''
                if 'SGD:' in dbxref:
                    sgd_id = dbxref.split('SGD:')[1].split(',')[0]
                
                results[gene_id] = {
                    'start': start,
                    'end': end,
                    'name': name,
                    'id': sgd_id
                }
    
    # Remove entries for genes not found
    results = {k: v for k, v in results.items() if v is not None}
    
    return results


def main():
    # Test case 1: Single gene
    print("=" * 70)
    print("Gene Annotations Parser - UPGMA GFF Parser")
    print("=" * 70)
    
    print("\nTest Case 1: Single gene")
    print("-" * 70)
    ids1 = ['YER065C']
    result1 = annotations(ids1)
    print(f"Input IDs: {ids1}")
    print(f"Output: {json.dumps(result1, indent=2)}")
    
    expected1 = {
        'YER065C': {
            'start': '285241',
            'end': '286914',
            'name': 'ICL1',
            'id': 'S000000867'
        }
    }
    # Check start, end, name, id match
    if 'YER065C' in result1:
        expected_vals = expected1['YER065C']
        actual_vals = result1['YER065C']
        start_match = actual_vals['start'] == expected_vals['start']
        end_match = actual_vals['end'] == expected_vals['end']
        name_match = actual_vals['name'] == expected_vals['name']
        id_match = actual_vals['id'] == expected_vals['id']
        
        if start_match and end_match and name_match and id_match:
            print("✓ Test Case 1 PASSED\n")
        else:
            print(f"✗ Test Case 1 FAILED")
            print(f"  Expected: {expected_vals}")
            print(f"  Actual: {actual_vals}\n")
    
    # Test case 2: Multiple genes
    print("Test Case 2: Multiple genes")
    print("-" * 70)
    ids2 = ['YPR184W', 'YLR312C', 'YML054C', 'YBR116C', 'YKL187C',
            'YLR267W', 'YEL012W', 'YOL084W', 'YJL045W', 'YJR095W']
    result2 = annotations(ids2)
    print(f"Input IDs: {len(ids2)} genes")
    print(f"Found: {len(result2)} genes\n")
    
    for gene_id in sorted(result2.keys()):
        info = result2[gene_id]
        print(f"  {gene_id}: {info['name']} ({info['id']})")
    
    if len(result2) == 10:
        print("\n✓ Test Case 2 PASSED\n")
    else:
        print(f"\n✗ Test Case 2 FAILED: Expected 10 genes, found {len(result2)}\n")
    
    # Write results to JSON
    out_path = os.path.join(os.path.dirname(__file__), 'annotations_results.json')
    
    # Combine all results
    all_results = {
        'test_case_1_single_gene': result1,
        'test_case_2_multiple_genes': result2,
        'total_genes_found': len(result2)
    }
    
    with open(out_path, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"Results written to {out_path}")


if __name__ == '__main__':
    main()
