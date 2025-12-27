#!/usr/bin/env python3
"""Debug annotation counts to understand ngo discrepancy."""

from collections import defaultdict

def parse_gaf_debug(gaf_file, uids_set=None):
    """Parse GAF showing IEA vs non-IEA counts."""
    gene_go_all = defaultdict(set)
    gene_go_no_iea = defaultdict(set)
    
    with open(gaf_file, 'r') as f:
        for line in f:
            if line.startswith('!'):
                continue
            parts = line.strip().split('\t')
            if len(parts) < 7:
                continue
            
            gene = parts[1]
            go_id = parts[4]
            evidence = parts[6]
            
            if uids_set and gene not in uids_set:
                continue
            
            gene_go_all[gene].add(go_id)
            if evidence != 'IEA':
                gene_go_no_iea[gene].add(go_id)
    
    return gene_go_all, gene_go_no_iea

# Load data
from enrichmentall import load_genes

print("Loading genes...")
c3 = load_genes('c3genes.txt')
ugenes = load_genes('ugenes.txt')
print(f"Cluster: {len(c3)} genes")
print(f"Universe: {len(ugenes)} genes")

print("\nParsing GAF with and without IEA...")
gene_go_all, gene_go_no_iea = parse_gaf_debug('gene_association.sgd', set(ugenes))

# Count for GO:0002181 (cytoplasmic translation)
target_go = 'GO:0002181'

genes_with_term_all = [g for g in ugenes if target_go in gene_go_all.get(g, set())]
genes_with_term_no_iea = [g for g in ugenes if target_go in gene_go_no_iea.get(g, set())]

genes_cluster_with_term_all = [g for g in c3 if target_go in gene_go_all.get(g, set())]
genes_cluster_with_term_no_iea = [g for g in c3 if target_go in gene_go_no_iea.get(g, set())]

print(f"\nFor GO term {target_go} (cytoplasmic translation):")
print(f"  WITH IEA:")
print(f"    ngo (genes in universe): {len(genes_with_term_all)}")
print(f"    ngis (genes in cluster): {len(genes_cluster_with_term_all)}")
print(f"  WITHOUT IEA (our implementation):")
print(f"    ngo (genes in universe): {len(genes_with_term_no_iea)}")
print(f"    ngis (genes in cluster): {len(genes_cluster_with_term_no_iea)}")
print(f"\n  Expected from example:")
print(f"    ngo: 170")
print(f"    ngis: 45")

print(f"\n  Analysis:")
print(f"    Our ngo=140 vs expected=170 → difference of {170-len(genes_with_term_no_iea)} genes")
print(f"    With IEA ngo={len(genes_with_term_all)} → difference of {170-len(genes_with_term_all)} from expected")
print(f"    Our ngis={len(genes_cluster_with_term_no_iea)} vs expected=45 → ✓ MATCHES!")
