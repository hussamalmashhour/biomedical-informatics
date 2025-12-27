#!/usr/bin/env python3
from first_occurrence import firstOccurrence

text = "$aaaaaabmnnps"
symbols = sorted(set(text))

print("Text:", text)
print("Symbols:", symbols)

# Using map as professor suggests
result = list(map(lambda s: firstOccurrence(s, text), symbols))
print("Result (using map):", result)
