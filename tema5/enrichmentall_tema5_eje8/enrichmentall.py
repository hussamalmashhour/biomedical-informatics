#!/usr/bin/env python3
"""Comprehensive Gene Set Enrichment Analysis (Tema 5 - Ejercicio 8).

Implements enrichmentAll function that performs GO term enrichment analysis
across all GO terms using the hypergeometric distribution test.

Algorithm:
1. Load gene lists from files (uids, gids)
2. Parse GO ontology (OBO) to build name mapping
3. Parse Gene Association File (GAF) to build gene-GO annotations
4. For each GO term of the specified type:
   - Filter by min/max annotation counts
   - Calculate hypergeometric p-value:
     N = total genes in universe
     M = genes annotated with this GO term
     n = genes in the cluster
     k = genes in cluster with this annotation
     p = P(X >= k) = 1 - hypergeom.cdf(k-1, N, M, n)
5. Filter by p-value threshold
6. Sort by p-value and return

Complexity: O(n * m) where n = number of GO terms, m = number of genes
"""

import os
import json
from collections import defaultdict
from scipy.stats import hypergeom


def load_genes(filepath):
    """Load gene list from file (one gene per line).
    
    Args:
        filepath: path to gene list file
    
    Returns:
        list of gene IDs
    """
    genes = []
    if not os.path.exists(filepath):
        print(f"Warning: File not found: {filepath}")
        return genes
    
    try:
        with open(filepath, 'r') as f:
            for line in f:
                gene_id = line.strip()
                if gene_id and not gene_id.startswith('#'):
                    genes.append(gene_id)
        return genes
    except Exception as e:
        print(f"Error reading file: {e}")
        return genes


def parse_obo(filepath):
    """Parse OBO file to extract GO ID → term name mapping.
    
    Args:
        filepath: path to OBO file
    
    Returns:
        dict {GO_ID: (name, namespace)}
    """
    go_map = {}
    
    if not os.path.exists(filepath):
        print(f"Warning: OBO file not found: {filepath}")
        return go_map
    
    current_id = None
    current_name = None
    current_namespace = None
    
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.rstrip('\n')
                
                if line.startswith('id:'):
                    current_id = line.split('id:')[1].strip()
                elif line.startswith('name:'):
                    current_name = line.split('name:')[1].strip()
                elif line.startswith('namespace:'):
                    current_namespace = line.split('namespace:')[1].strip()
                elif line.startswith('[Term]') and current_id:
                    # Save previous term
                    if current_name and current_namespace:
                        go_map[current_id] = (current_name, current_namespace)
                    current_id = None
                    current_name = None
                    current_namespace = None
            
            # Save last term
            if current_id and current_name and current_namespace:
                go_map[current_id] = (current_name, current_namespace)
        
        return go_map
    
    except Exception as e:
        print(f"Error parsing OBO: {e}")
        return go_map


def parse_gaf(filepath, uids_set, go_map):
    """Parse GAF file to build gene → GO annotations.
    
    Filters out IEA (electronic) annotations.
    
    Args:
        filepath: path to GAF file
        uids_set: set of all universe genes (for filtering)
        go_map: dict of valid GO terms
    
    Returns:
        dict {gene_id: set(GO_IDs)}
    """
    gene_go = defaultdict(set)
    go_genes = defaultdict(set)  # For counting
    
    if not os.path.exists(filepath):
        print(f"Warning: GAF file not found: {filepath}")
        return gene_go, go_genes
    
    try:
        with open(filepath, 'r') as f:
            for line in f:
                # Skip comments
                if line.startswith('!'):
                    continue
                
                line = line.rstrip('\n')
                if not line:
                    continue
                
                # Parse tab-delimited fields
                fields = line.split('\t')
                if len(fields) < 9:
                    continue
                
                gene_id = fields[1]
                go_id = fields[4]
                evidence_code = fields[6]
                aspect = fields[8]
                
                # Filter: only genes in universe, valid GO terms, non-IEA evidence
                if gene_id not in uids_set or go_id not in go_map or evidence_code == 'IEA':
                    continue
                
                gene_go[gene_id].add(go_id)
                go_genes[go_id].add(gene_id)
        
        return gene_go, go_genes
    
    except Exception as e:
        print(f"Error parsing GAF: {e}")
        return gene_go, defaultdict(set)


def enrichmentAll(uids, gids, a, min_count, max_count, go_type, 
                  obo_file='gene_ontology.obo', gaf_file='gene_association.gaf'):
    """Compute GO enrichment for all terms.
    
    Args:
        uids: list of all genes in experiment (universe)
        gids: list of genes in cluster/group of interest
        a: significance threshold (p-value)
        min_count: minimum GO term annotation count
        max_count: maximum GO term annotation count
        go_type: 'P' (Biological Process), 'C' (Cellular Component), 'F' (Molecular Function)
        obo_file: path to GO ontology file
        gaf_file: path to Gene Association File
    
    Returns:
        list of dicts sorted by p-value:
        [
            {'name': GO_term_name, 'pval': p_value, 'ngis': overlap_count, 'ngo': total_annotated},
            ...
        ]
    """
    # Resolve file paths
    if not os.path.isabs(obo_file):
        obo_file = os.path.join(os.path.dirname(__file__), obo_file)
    if not os.path.isabs(gaf_file):
        gaf_file = os.path.join(os.path.dirname(__file__), gaf_file)
    
    # Convert to sets for O(1) lookup
    uids_set = set(uids)
    gids_set = set(gids)
    
    N = len(uids_set)  # Total genes in universe
    n = len(gids_set)  # Genes in cluster
    
    # Parse GO files
    print(f"Parsing OBO file: {os.path.basename(obo_file)}...")
    go_map = parse_obo(obo_file)
    print(f"  Found {len(go_map)} GO terms\n")
    
    print(f"Parsing GAF file: {os.path.basename(gaf_file)}...")
    gene_go, go_genes = parse_gaf(gaf_file, uids_set, go_map)
    print(f"  Annotated {len(gene_go)} genes\n")
    
    # Compute enrichment for each GO term
    results = []
    
    for go_id, genes_with_go in go_genes.items():
        go_name, namespace = go_map[go_id]
        
        # Filter by GO type
        aspect_map = {'biological_process': 'P', 'cellular_component': 'C', 'molecular_function': 'F'}
        aspect = aspect_map.get(namespace, '?')
        
        if aspect != go_type:
            continue
        
        # Filter by annotation count
        M = len(genes_with_go)  # Total genes annotated with this term
        if not (min_count <= M <= max_count):
            continue
        
        # Count overlap
        k = len(gids_set & genes_with_go)  # Genes in both cluster and GO term
        
        # Calculate hypergeometric p-value
        # P(X >= k) where X ~ Hypergeom(N, M, n)
        # = 1 - P(X < k)
        # = 1 - P(X <= k-1)
        # = 1 - hypergeom.cdf(k-1, N, M, n)
        
        if k == 0:
            # No overlap, p-value is 1
            p_value = 1.0
        else:
            # Use survival function (1 - cdf)
            p_value = 1.0 - hypergeom.cdf(k - 1, N, M, n)
        
        # Filter by p-value threshold
        if p_value >= a:
            continue
        
        # Add to results
        results.append({
            'name': go_name,
            'pval': p_value,
            'ngis': k,
            'ngo': M
        })
    
    # Sort by p-value
    results.sort(key=lambda x: x['pval'])
    
    return results


def main():
    print("=" * 70)
    print("Comprehensive Gene Set Enrichment Analysis (Hypergeometric Test)")
    print("=" * 70)
    
    # Load gene lists
    print("\nLoading gene lists...")
    uids = load_genes('ugenes.txt')
    gids_c3 = load_genes('c3genes.txt')
    gids_random = load_genes('randomGenes.txt')
    
    print(f"  Universe (uids):     {len(uids)} genes")
    print(f"  Cluster 3 (c3):      {len(gids_c3)} genes")
    print(f"  Random genes:        {len(gids_random)} genes\n")
    
    # Test Case 1: Biological Process enrichment in Cluster 3
    print("Test Case 1: Cluster 3 - Biological Process Enrichment")
    print("-" * 70)
    
    a = 0.05  # p-value threshold
    min_count = 1
    max_count = 500
    go_type = 'P'
    
    print(f"Parameters: a={a}, min={min_count}, max={max_count}, type={go_type}\n")
    
    result_c3 = enrichmentAll(uids, gids_c3, a, min_count, max_count, go_type)
    
    print(f"Enriched terms: {len(result_c3)}\n")
    
    if result_c3:
        print("Top enriched GO terms (sorted by p-value):")
        for i, term in enumerate(result_c3[:10], 1):
            print(f"  {i}. {term['name']}")
            print(f"     p-value: {term['pval']:.2e}, overlap: {term['ngis']}/{term['ngo']}\n")
    else:
        print("No significant enrichment found\n")
    
    # Test Case 2: Cellular Component enrichment
    print("Test Case 2: Cluster 3 - Cellular Component Enrichment")
    print("-" * 70)
    
    go_type = 'C'
    print(f"Parameters: a={a}, min={min_count}, max={max_count}, type={go_type}\n")
    
    result_c3_cc = enrichmentAll(uids, gids_c3, a, min_count, max_count, go_type)
    
    print(f"Enriched terms: {len(result_c3_cc)}\n")
    
    if result_c3_cc:
        print("Top enriched GO terms (sorted by p-value):")
        for i, term in enumerate(result_c3_cc[:10], 1):
            print(f"  {i}. {term['name']}")
            print(f"     p-value: {term['pval']:.2e}, overlap: {term['ngis']}/{term['ngo']}\n")
    else:
        print("No significant enrichment found\n")
    
    # Test Case 3: Random genes (should show less enrichment)
    print("Test Case 3: Random Genes - Biological Process Enrichment")
    print("-" * 70)
    
    go_type = 'P'
    print(f"Parameters: a={a}, min={min_count}, max={max_count}, type={go_type}\n")
    
    result_random = enrichmentAll(uids, gids_random, a, min_count, max_count, go_type)
    
    print(f"Enriched terms: {len(result_random)}\n")
    
    # Write comprehensive results to file
    out_path = "enrichmentAll_results.json"
    output = {
        'parameters': {
            'p_value_threshold': a,
            'min_annotations': min_count,
            'max_annotations': max_count
        },
        'cluster_3_biological_process': result_c3,
        'cluster_3_cellular_component': result_c3_cc,
        'random_genes_biological_process': result_random,
        'summary': {
            'c3_bp_terms': len(result_c3),
            'c3_cc_terms': len(result_c3_cc),
            'random_bp_terms': len(result_random)
        }
    }
    
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)
    
    print(f"Results written to {out_path}\n")
    
    # Also write text summary
    txt_path = "enrichmentAll_results.txt"
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write("Comprehensive Gene Set Enrichment Analysis Results\n")
        f.write("=" * 70 + "\n\n")
        
        f.write("CLUSTER 3 - BIOLOGICAL PROCESS\n")
        f.write("-" * 70 + "\n")
        f.write(f"Enriched terms: {len(result_c3)}\n\n")
        for i, term in enumerate(result_c3, 1):
            f.write(f"{i}. {term['name']}\n")
            f.write(f"   p-value: {term['pval']:.6e}\n")
            f.write(f"   overlap: {term['ngis']}/{term['ngo']}\n\n")
        
        f.write("\nCLUSTER 3 - CELLULAR COMPONENT\n")
        f.write("-" * 70 + "\n")
        f.write(f"Enriched terms: {len(result_c3_cc)}\n\n")
        for i, term in enumerate(result_c3_cc, 1):
            f.write(f"{i}. {term['name']}\n")
            f.write(f"   p-value: {term['pval']:.6e}\n")
            f.write(f"   overlap: {term['ngis']}/{term['ngo']}\n\n")
        
        f.write("\nRANDOM GENES - BIOLOGICAL PROCESS\n")
        f.write("-" * 70 + "\n")
        f.write(f"Enriched terms: {len(result_random)}\n\n")
        for i, term in enumerate(result_random, 1):
            f.write(f"{i}. {term['name']}\n")
            f.write(f"   p-value: {term['pval']:.6e}\n")
            f.write(f"   overlap: {term['ngis']}/{term['ngo']}\n\n")
    
    print(f"Text summary written to {txt_path}")


if __name__ == '__main__':
    main()
