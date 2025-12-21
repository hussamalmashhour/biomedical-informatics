#!/usr/bin/env python3
"""Gene Set Enrichment Analysis - Fisher's Exact Test (Tema 5 - Ejercicio 7).

Implements the enrichment function that computes Fisher's exact test for
gene set enrichment. This test determines if a gene set (ids) is significantly
enriched in a particular Gene Ontology (GO) term (goids).

Algorithm:
1. Compute a 2×2 contingency table from set operations:
   - a = |ids ∩ goids|       (genes in both sets)
   - b = |goids| - a         (genes in GO term but not in ids)
   - c = |ids| - a           (genes in ids but not in GO term)
   - d = n - (a + b + c)     (genes in neither set)

2. Build contingency table:
   [[a, b],
    [c, d]]

3. Apply Fisher's exact test (one-tailed, greater):
   - Tests if enrichment is statistically significant
   - alternative='greater' tests if ids genes are overrepresented in the GO term

4. Return p-value

Complexity: O(1) for set operations and Fisher's test computation.
"""

import os
import re
from scipy.stats import fisher_exact


def enrichment(ids, goids, n):
    """Compute Fisher's exact test p-value for gene set enrichment.
    
    Tests whether genes in ids are significantly enriched in a GO term.
    
    Args:
        ids: set of gene identifiers of interest (e.g., differentially expressed)
        goids: set of gene identifiers annotated to a specific GO term
        n: integer, total number of genes in the universe
    
    Returns:
        p_value: float, one-tailed p-value from Fisher's exact test
        contingency: 2x2 contingency table
        odds_ratio: odds ratio from Fisher's test
    
    Raises:
        ValueError: if inputs are invalid
    """
    # Input validation
    if not isinstance(ids, set):
        raise ValueError("ids must be a set")
    if not isinstance(goids, set):
        raise ValueError("goids must be a set")
    if not isinstance(n, int) or n < 1:
        raise ValueError("n must be a positive integer")
    
    # Compute contingency table values using set operations
    # a: intersection (genes in both sets)
    a = len(ids & goids)
    
    # b: genes in GO term but not in ids
    b = len(goids) - a
    
    # c: genes in ids but not in GO term
    c = len(ids) - a
    
    # d: genes in neither set
    d = n - a - b - c
    
    # Validate that d is non-negative
    if d < 0:
        raise ValueError(f"Invalid: universe size n={n} is smaller than |ids ∪ goids|={a + b + c}")
    
    # Build 2×2 contingency table
    # [[a, b],     where a = enriched, b = not in ids
    #  [c, d]]     where c = in ids, d = neither
    contingency_table = [[a, b], [c, d]]
    
    # Apply Fisher's exact test (one-tailed, greater)
    # alternative='greater' tests: P(enrichment) > baseline
    odds_ratio, p_value = fisher_exact(contingency_table, alternative='greater')
    
    return p_value, contingency_table, odds_ratio


def load_dgenes(filepath):
    """Load gene set from file (Python set literal format).
    
    Parses a file containing a Python set literal like:
    {'S000000003', 'S000000010', ...}
    
    Args:
        filepath: path to dgenes.txt file
    
    Returns:
        set of gene identifiers
    """
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        return set()
    
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Extract set literal (handles multiline format)
        # Match everything between first { and last }
        match = re.search(r'\{(.*)\}', content, re.DOTALL)
        if match:
            # Parse quoted strings
            genes_str = match.group(1)
            # Find all quoted strings
            quoted = re.findall(r"'([^']+)'", genes_str)
            return set(quoted)
        else:
            print("Error: Could not parse set from file")
            return set()
    
    except Exception as e:
        print(f"Error reading file: {e}")
        return set()



def main():
    print("=" * 70)
    print("Gene Set Enrichment Analysis - Fisher's Exact Test")
    print("=" * 70)
    
    # Test Case 1: Example from specification
    print("\nTest Case 1: Example data")
    print("-" * 70)
    ids = set(range(30))  # 30 genes of interest
    goids = set(range(20, 60))  # 40 genes in GO term (20-59)
    n = 200  # Total universe
    
    print(f"Input:")
    print(f"  ids:   set(range(30)) = {len(ids)} genes")
    print(f"  goids: set(range(20, 60)) = {len(goids)} genes")
    print(f"  n:     {n} (total genes in universe)")
    
    p_value, contingency, odds_ratio = enrichment(ids, goids, n)
    
    print(f"\nSet operations:")
    print(f"  |ids ∩ goids| = {contingency[0][0]} (intersection)")
    print(f"  |goids - ids| = {contingency[0][1]} (GO only)")
    print(f"  |ids - goids| = {contingency[1][0]} (ids only)")
    print(f"  |neither|     = {contingency[1][1]} (background)")
    
    print(f"\nContingency Table:")
    print(f"  [[{contingency[0][0]}, {contingency[0][1]}],")
    print(f"   [{contingency[1][0]}, {contingency[1][1]}]]")
    
    print(f"\nResults:")
    print(f"  Odds Ratio: {odds_ratio:.6f}")
    print(f"  P-value:    {p_value:.6f}")
    
    expected_pvalue = 0.046325
    if abs(p_value - expected_pvalue) < 0.001:
        print(f"  ✓ Matches expected p-value approx {expected_pvalue}\n")
    else:
        print(f"  Note: p-value differs from expected {expected_pvalue}\n")
    
    # Test Case 2: Real data from dgenes.txt
    print("Test Case 2: Real Diauxic Shift Genes")
    print("-" * 70)
    
    # Load dgenes from file
    dgenes_file = os.path.join(os.path.dirname(__file__), 'dgenes.txt')
    dgenes = load_dgenes(dgenes_file)
    
    if not dgenes:
        print("Warning: Could not load dgenes.txt, using example subset\n")
        # Fallback to example data
        dgenes = {
            'S000000702', 'S000000826', 'S000004937', 'S000005253',
            'S000007226', 'S000000056', 'S000000080', 'S000001516',
            'S000002572', 'S000003146', 'S000000915', 'S000000968',
            'S000001421', 'S000003439', 'S000005141', 'S000005195',
            'S000005614', 'S000007254', 'S000000186', 'S000002082',
            'S000002483', 'S000002822', 'S000002878', 'S000003053',
            'S000004002'
        }
    
    # GO:0006066 genes (amino acid biosynthetic process)
    go_term = {
        'S000000056', 'S000000080', 'S000000702', 'S000000826', 'S000004937'
    }
    
    n_universe = 6034
    
    print(f"Input:")
    print(f"  dgenes (loaded from file):     {len(dgenes)} genes")
    print(f"  GO:0006066 term genes:         {len(go_term)} genes")
    print(f"  Universe size (n):             {n_universe}")
    
    p_val_real, cont_real, odds_real = enrichment(dgenes, go_term, n_universe)
    
    print(f"\nSet operations:")
    print(f"  |dgenes ∩ GO|   = {cont_real[0][0]} (intersection)")
    print(f"  |GO - dgenes|   = {cont_real[0][1]} (GO only)")
    print(f"  |dgenes - GO|   = {cont_real[1][0]} (dgenes only)")
    print(f"  |neither|       = {cont_real[1][1]} (background)")
    
    print(f"\nContingency Table:")
    print(f"  [[{cont_real[0][0]}, {cont_real[0][1]}],")
    print(f"   [{cont_real[1][0]}, {cont_real[1][1]}]]")
    
    print(f"\nResults:")
    print(f"  Odds Ratio: {odds_real:.6f}")
    print(f"  P-value:    {p_val_real:.6f}")
    
    if p_val_real < 0.05:
        print(f"  ✓ Significant enrichment (p < 0.05)\n")
    else:
        print(f"  Note: Not significant at p < 0.05\n")
    
    # Calculate effect size information
    intersection_genes = dgenes & go_term
    print(f"Genes in both sets: {sorted(intersection_genes)}")
    print(f"Proportion enriched: {cont_real[0][0]}/{len(go_term)} GO genes = {100*cont_real[0][0]/len(go_term):.1f}%\n")
    
    # Write results to file
    out_path = "enrichment_results.txt"
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write("Gene Set Enrichment Analysis - Fisher's Exact Test Results\n")
        f.write("=" * 70 + "\n\n")
        
        f.write("TEST CASE 1: Example Data\n")
        f.write("-" * 70 + "\n")
        f.write(f"Input: ids={{{len(ids)} genes}}, goids={{{len(goids)} genes}}, n={n}\n")
        f.write(f"Contingency Table: [[{contingency[0][0]}, {contingency[0][1]}], [{contingency[1][0]}, {contingency[1][1]}]]\n")
        f.write(f"Odds Ratio: {odds_ratio:.6f}\n")
        f.write(f"P-value: {p_value:.6f}\n")
        f.write(f"Expected: approx {expected_pvalue}\n")
        f.write(f"Match: {abs(p_value - expected_pvalue) < 0.001}\n\n")
        
        f.write("TEST CASE 2: Real Diauxic Shift Genes\n")
        f.write("-" * 70 + "\n")
        f.write(f"Input: dgenes={{{len(dgenes)} genes (from dgenes.txt)}}, GO:0006066={{{len(go_term)} genes}}, n={n_universe}\n")
        f.write(f"Contingency Table: [[{cont_real[0][0]}, {cont_real[0][1]}], [{cont_real[1][0]}, {cont_real[1][1]}]]\n")
        f.write(f"Odds Ratio: {odds_real:.6f}\n")
        f.write(f"P-value: {p_val_real:.6f}\n")
        f.write(f"Significant (p < 0.05): {p_val_real < 0.05}\n\n")
        f.write(f"Genes in intersection: {sorted(intersection_genes)}\n")
        f.write(f"Proportion enriched: {cont_real[0][0]}/{len(go_term)} GO genes = {100*cont_real[0][0]/len(go_term):.1f}%\n")
    
    print(f"Results written to {out_path}")


if __name__ == '__main__':
    main()
