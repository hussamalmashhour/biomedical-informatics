#!/usr/bin/env python3
from functions import functions

test_genes = ['YPR184W', 'YLR312C', 'YML054C', 'YBR116C', 'YKL187C', 
              'YLR267W', 'YEL012W', 'YOL084W', 'YJL045W', 'YJR095W']

result = functions(test_genes)

print(f"\nTotal input genes: {len(test_genes)}")
print(f"Total genes with entries: {len(result)}")
print("\nGenes found:")
for gene in test_genes:
    found = False
    for sgd_id, terms in result.items():
        # Check if this gene is associated with this SGD ID
        # We need to cross-reference somehow
        pass

print("\nAll SGD IDs in result:")
for sgd_id in sorted(result.keys()):
    print(f"  {sgd_id}: {result[sgd_id]}")
