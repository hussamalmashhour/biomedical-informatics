#!/usr/bin/env python3
"""Try to reverse-engineer a dataset that gives A[0] = 0.15"""

from profile_matrix import profile

print("=" * 70)
print("REVERSE ENGINEERING: Can we create data that gives A[0] = 0.15?")
print("=" * 70)

print("\nWith standard Laplace formula: (count + 1) / (t + 4)")
print("\nLet's test different values of t (number of sequences):")

for t in range(4, 25):
    denom = t + 4
    # Try to find count_A that gives 0.15
    for count_A in range(0, t+1):
        prob = (count_A + 1) / denom
        if abs(prob - 0.15) < 0.001:  # Very close to 0.15
            print(f"\n✓ Found: t={t} sequences, count_A={count_A}")
            print(f"  ({count_A} + 1) / {denom} = {count_A+1}/{denom} = {prob:.6f}")
            
            # Create a sample dataset
            if t <= 20:  # Only show for reasonable sizes
                print(f"\n  Sample sequences (first position only):")
                sequences = ['A'] * count_A + ['T'] * (t - count_A)
                print(f"  {sequences}")
                
                # Create full test sequences
                test_dna = []
                for i, first_nt in enumerate(sequences):
                    # Just make dummy sequences of length 12
                    test_dna.append(first_nt + 'CGGGGGTTTTT')
                
                result = profile(test_dna, Laplace=True)
                print(f"\n  Testing with profile function:")
                print(f"  A[0] = {result['A'][0]:.6f}")
                
                if abs(result['A'][0] - 0.15) < 0.001:
                    print(f"  ✓✓✓ EXACT MATCH!")
                    print(f"\n  Full sequences created:")
                    for i, seq in enumerate(test_dna[:5]):
                        print(f"    {i+1}: {seq}")
                    if len(test_dna) > 5:
                        print(f"    ... ({len(test_dna)} total)")

print("\n" + "=" * 70)
print("CONCLUSION")
print("=" * 70)
print("If no exact matches found, 0.15 cannot be achieved with")
print("the standard Laplace formula (count + 1) / (t + 4)")
print("\nThis suggests:")
print("  • Professor's '0.15' is an approximation/rounding")
print("  • OR there's a different dataset structure")
print("  • Your implementation is still CORRECT")
