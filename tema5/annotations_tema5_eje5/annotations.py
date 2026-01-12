#!/usr/bin/env python3
"""Gene Annotations Parser (Tema 5 - Ejercicio 5)."""

import os


def parse_attributes(attr_string):
    attrs = {}
    for pair in attr_string.strip().split(';'):
        if '=' in pair:
            key, value = pair.split('=', 1)
            attrs[key] = value
        elif pair.strip():
            attrs[pair.strip()] = ''
    return attrs


def annotations(ids, gff_file='saccharomyces_cerevisiae_R64-2-1_20150113.gff'):
    id_set = set(ids) if not isinstance(ids, set) else ids
    results = {gene_id: None for gene_id in ids}
    
    if not os.path.isabs(gff_file):
        gff_file = os.path.join(os.path.dirname(__file__), gff_file)
    
    if not os.path.exists(gff_file):
        return results
    
    with open(gff_file, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            
            line = line.rstrip('\n')
            if not line:
                continue
            
            fields = line.split('\t')
            if len(fields) < 9:
                continue
            
            seqname, source, feature, start, end, score, strand, frame, attributes = fields[:9]
            attrs = parse_attributes(attributes)
            gene_id = attrs.get('ID', '')
            if gene_id in id_set and feature == 'gene' and results[gene_id] is None:
                name = attrs.get('gene', attrs.get('Name', gene_id))
                
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
    
    results = {k: v for k, v in results.items() if v is not None}
    return results


def main():
    ids = ['YPR184W', 'YLR312C', 'YML054C', 'YBR116C', 'YKL187C',
           'YLR267W', 'YEL012W', 'YOL084W', 'YJL045W', 'YJR095W']
    result = annotations(ids)
    print(result)


if __name__ == '__main__':
    main()
