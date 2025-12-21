# Complementaria (reverse-complement) example

This small Python script downloads the Vibrio cholerae genome (plain text) from
the provided URL, extracts the 20 nucleotides in the center of the genome
(ignoring non-ACGT/N characters), and prints that 20-nt sequence and its
reverse-complement using the `complementaria(seq)` function.

Run:

```powershell
python "d:\\Biomedical Informatics\\complementaria.py"
```

Output:
- Genome length (ACGT/N letters only)
- Center 20-nt sequence
- Reverse complement of that sequence

The function mapping is A<->T and C<->G. Case is preserved (upper->upper, lower->lower).
