#!/usr/bin/env python3
"""GO (Gene Ontology) Annotation Parser (Tema 5 - Ejercicio 6).

Implements the functions parser that reads GO OBO and GAF files to extract
Biological Process annotations for yeast genes.

File formats:
- OBO (Open Biomedical Ontology): Contains GO term definitions with IDs and names
  Format: [Term] blocks with id: and name: fields
- GAF (Gene Association File): Tab-delimited with 17 columns:
  1. DB (always SGD)
  2. DB_Object_ID (SGD systematic ID)
  3. DB_Object_Symbol (gene name)
  4. Qualifier (enables, involved_in, etc.)
  5. GO_ID (e.g., GO:0015968)
  6. DB:Reference (publication)
  7. Evidence_Code (IMP, IDA, TAS, IEA, etc.)
  8. With/From (supporting info)
  9. Aspect (P=Biological Process, F=Function, C=Component)
  10-17. Additional fields

Filtering:
- Aspect must be 'P' (Biological Process)
- Evidence Code must NOT be 'IEA' (exclude electronic annotations)
- Gene symbol must match input ids list

Output: Dict mapping SGD IDs → set of GO term names
"""

import os
import json


def parse_obo(go_obo_file):
    """Parse OBO file to extract GO ID → term name mapping.
    
    The OBO format is structured as follows:
    [Term]
    id: GO:0006995
    name: cellular respiration
    namespace: biological_process
    ...
    
    Args:
        go_obo_file: path to go.obo file
    
    Returns:
        dict mapping GO IDs (e.g., 'GO:0015968') to term names (e.g., 'glyoxylate cycle')
    """
    go_map = {}
    
    if not os.path.exists(go_obo_file):
        print(f"Warning: OBO file not found: {go_obo_file}")
        return go_map
    
    current_id = None
    with open(go_obo_file, 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            
            # Extract GO ID
            if line.startswith('id:'):
                current_id = line.split('id:')[1].strip()
            
            # Extract name for the current term
            elif line.startswith('name:') and current_id:
                name = line.split('name:')[1].strip()
                go_map[current_id] = name
    
    return go_map


def parse_gaf(gaf_file, ids, go_map):
    """Parse GAF file to extract gene → GO term annotations.
    
    Filters for:
    - Gene symbols matching input ids
    - Aspect = 'P' (Biological Process)
    - Evidence Code != 'IEA' (exclude electronic annotations)
    
    GAF format (17 tab-delimited columns):
    1. DB
    2. DB_Object_ID (SGD ID like S000000867)
    3. DB_Object_Symbol (gene name like YER065C)
    4. Qualifier
    5. GO_ID (like GO:0015968)
    6. DB:Reference
    7. Evidence_Code (IMP, IDA, TAS, IEA, etc.)
    8. With/From
    9. Aspect (P, F, or C)
    10. DB_Object_Name
    11-17. Additional fields
    
    Args:
        gaf_file: path to GAF file
        ids: set/list of gene symbols to lookup
        go_map: dict mapping GO IDs to term names
    
    Returns:
        dict mapping SGD IDs to sets of GO term names
    """
    # Convert to set for O(1) lookup
    id_set = set(ids) if not isinstance(ids, set) else ids
    
    # Results dict: SGD ID → set of GO term names
    results = {}
    
    if not os.path.exists(gaf_file):
        print(f"Warning: GAF file not found: {gaf_file}")
        return results
    
    with open(gaf_file, 'r') as f:
        for line in f:
            # Skip comment lines
            if line.startswith('!'):
                continue
            
            line = line.rstrip('\n')
            if not line:
                continue
            
            # Parse 17-column GAF format
            fields = line.split('\t')
            if len(fields) < 9:
                continue
            
            # Extract key fields
            db = fields[0]
            sgd_id = fields[1]
            gene_symbol = fields[2]
            go_id = fields[4]
            evidence_code = fields[6]
            aspect = fields[8]
            
            # Filter: only Biological Process (P), exclude electronic annotations (IEA)
            if aspect != 'P' or evidence_code == 'IEA':
                continue
            
            # Filter: gene symbol must be in input list
            if gene_symbol not in id_set:
                continue
            
            # Lookup GO term name
            if go_id not in go_map:
                print(f"Warning: GO ID not found: {go_id}")
                continue
            
            go_name = go_map[go_id]
            
            # Add to results
            if sgd_id not in results:
                results[sgd_id] = set()
            
            results[sgd_id].add(go_name)
    
    return results


def functions(ids, go_obo_file='go.obo', gaf_file='gene_association.sgd'):
    """Extract Biological Process annotations for genes.
    
    Orchestrates parsing of OBO and GAF files to return GO annotations.
    
    Args:
        ids: list/array of gene symbols (e.g., ['YER065C', 'YPR184W'])
        go_obo_file: path to GO OBO file (default: local go.obo)
        gaf_file: path to Gene Association File (default: local gene_association.sgd)
    
    Returns:
        dict mapping SGD IDs to sets of Biological Process term names
        Example: {'S000000867': {'glyoxylate cycle', 'metabolic process'}}
    """
    # Resolve file paths
    if not os.path.isabs(go_obo_file):
        go_obo_file = os.path.join(os.path.dirname(__file__), go_obo_file)
    if not os.path.isabs(gaf_file):
        gaf_file = os.path.join(os.path.dirname(__file__), gaf_file)
    
    # Parse OBO file
    print(f"Parsing OBO file: {os.path.basename(go_obo_file)}...")
    go_map = parse_obo(go_obo_file)
    print(f"  Found {len(go_map)} GO terms\n")
    
    # Parse GAF file
    print(f"Parsing GAF file: {os.path.basename(gaf_file)}...")
    results = parse_gaf(gaf_file, ids, go_map)
    print(f"  Found annotations for {len(results)} genes\n")
    
    return results


def main():
    print("=" * 70)
    print("GO Annotation Parser - Biological Process Extractor")
    print("=" * 70)
    
    # Test case 1: Single gene
    print("\nTest Case 1: Single gene (YER065C)")
    print("-" * 70)
    ids1 = ['YER065C']
    result1 = functions(ids1)
    
    print(f"Input genes: {ids1}")
    print("Output:")
    for sgd_id in sorted(result1.keys()):
        terms = sorted(result1[sgd_id])
        print(f"  {sgd_id}: {terms}")
    
    # Check expected result
    if 'S000000867' in result1 and 'glyoxylate cycle' in result1['S000000867']:
        print("✓ Test Case 1 PASSED\n")
    else:
        print("✗ Test Case 1 FAILED - Expected 'glyoxylate cycle' in S000000867\n")
    
    # Test case 2: Multiple genes
    print("Test Case 2: Multiple genes")
    print("-" * 70)
    ids2 = ['YPR184W', 'YLR312C', 'YML054C', 'YBR116C', 'YKL187C',
            'YLR267W', 'YEL012W', 'YOL084W', 'YJL045W', 'YJR095W']
    result2 = functions(ids2)
    
    print(f"Input genes: {len(ids2)} genes")
    print("Output:")
    for sgd_id in sorted(result2.keys()):
        terms = sorted(result2[sgd_id])
        print(f"  {sgd_id}: {terms}")
    
    if len(result2) > 0:
        print("\n✓ Test Case 2 PASSED\n")
    else:
        print("\n✗ Test Case 2 FAILED\n")
    
    # Write results to JSON
    out_path = os.path.join(os.path.dirname(__file__), 'go_annotations.json')
    
    # Convert sets to lists for JSON serialization
    result1_json = {k: sorted(list(v)) for k, v in result1.items()}
    result2_json = {k: sorted(list(v)) for k, v in result2.items()}
    
    output = {
        'test_case_1_single_gene': result1_json,
        'test_case_2_multiple_genes': result2_json,
        'summary': {
            'genes_with_annotations': len(result2),
            'total_unique_terms': len(set().union(*result2.values()))
        }
    }
    
    with open(out_path, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"Results written to {out_path}")


if __name__ == '__main__':
    main()
