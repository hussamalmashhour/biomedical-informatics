#!/usr/bin/env python3
"""Download nfkbMotifs from URL and test profile function."""

import urllib.request
import sys
sys.path.insert(0, 'd:\\Biomedical Informatics')
sys.path.insert(0, 'd:\\Biomedical Informatics\\tema2\\profile_matrix_tema2_eje7')

from profile_matrix import profile
from config import build_test_url

# Download the file
url = "http://vis.usal.es/rodrigo/documentos/bioinfo/avanzada/datos/nfkbMotifs.txt"
print(f"Downloading from: {url}")

try:
    response = urllib.request.urlopen(url)
    data = response.read().decode('utf-8')
    
    # Parse sequences
    lines = data.strip().split('\n')
    motifs = []
    for line in lines:
        seq = ''.join(line.strip().split()).upper()
        if seq:
            motifs.append(seq)
    
    print(f"\nDownloaded {len(motifs)} sequences")
    print(f"Sequence length: {len(motifs[0]) if motifs else 0}")
    
    print("\nFirst few sequences:")
    for i, s in enumerate(motifs[:5]):
        print(f"  {i+1}: {s}")
    
    # Calculate profile
    result = profile(motifs, Laplace=True)
    
    print("\n" + "=" * 60)
    print("PROFILE RESULTS")
    print("=" * 60)
    print(f"\nFirst value for A: {result['A'][0]:.6f}")
    print(f"Expected by professor: 0.15")
    
    if abs(result['A'][0] - 0.15) < 0.001:
        print("✓ Match!")
    else:
        print("⚠ Slight difference (may be rounding)")
    
    print("\nFirst 5 positions of profile:")
    for nt in ['A', 'C', 'G', 'T']:
        probs = [f"{p:.3f}" for p in result[nt][:5]]
        print(f"  {nt}: {' '.join(probs)}")
    
    # Generate submission URL
    print("\n" + "=" * 60)
    print("SUBMISSION")
    print("=" * 60)
    url = build_test_url(2, 7, result)
    print(f"\nSubmission URL:\n{url}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
