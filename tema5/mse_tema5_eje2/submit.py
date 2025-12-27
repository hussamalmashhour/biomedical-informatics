#!/usr/bin/env python3
"""
Submission script for Exercise 2 - Mean Squared Error (MSE)
Generates the submission URL with the computed MSE result.
"""

import numpy as np
import os
import sys

# Add parent directory to path to import config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
import config

# Import the mse function
from mse import mse


def run_test_case():
    """Run the test case from the exercise."""
    print("=" * 70)
    print("EXERCISE 2 - MSE (Mean Squared Error)")
    print("=" * 70)
    
    # Test case from exercise
    points = np.array([
        [3, 20], [4, 22], [5, 23], [3, 18], [4, 21], [5, 24],
        [21, 10], [22, 12], [23, 13], [21, 8], [20, 11], [24, 13],
        [11, 2], [12, 1], [13, 3], [15, 4], [11, 3], [14, 2]
    ], dtype=float)
    
    centers = np.array([[3, 20], [24, 13], [14, 2]], dtype=float)
    
    print("\nTest Case:")
    print(f"  Points shape: {points.shape}")
    print(f"  Centers shape: {centers.shape}")
    print(f"\nPoints (first 5):")
    for i in range(min(5, len(points))):
        print(f"    {points[i]}")
    print("    ...")
    
    print(f"\nCenters:")
    for i, center in enumerate(centers):
        print(f"    Center {i+1}: {center}")
    
    # Compute MSE
    result = mse(points, centers)
    
    print(f"\n" + "-" * 70)
    print(f"RESULT: {result:.2f}")
    print("-" * 70)
    
    return result


def build_submission_url(result):
    """Build the submission URL for the MSE exercise."""
    # Get exercise info from config
    session, exercise, description = config.get_exercise_info("mse_tema5_eje2")
    
    # Round to 2 decimal places
    formatted_result = round(result, 2)
    
    # Build URL using config helper
    url = config.build_test_url(session, exercise, formatted_result)
    
    return url


def main():
    print("=" * 70)
    print("MSE - SUBMISSION GENERATOR")
    print("=" * 70)
    
    # Run test case
    result = run_test_case()
    
    # Build submission URL
    url = build_submission_url(result)
    
    print("\n" + "=" * 70)
    print("SUBMISSION URL")
    print("=" * 70)
    print(f"\n{url}")
    
    print("\n" + "=" * 70)
    print("EXPLANATION")
    print("=" * 70)
    print("""
Mean Squared Error (MSE) measures clustering quality:

1. For each point, find the nearest center
2. Compute squared distance to that nearest center
3. Return the average of all squared distances

Formula:
  MSE = (1/n) × Σ min_c ||point_i - center_c||²

Lower MSE = better clustering (points closer to their centers)

In this test case:
  - 18 points in 2D space
  - 3 cluster centers
  - Each point assigned to nearest center
  - Average squared distance: {:.2f}
    """.format(result))
    
    # Save to file
    output_file = os.path.join(os.path.dirname(__file__), 'submission_url.txt')
    with open(output_file, 'w') as f:
        f.write("Exercise 2 - Mean Squared Error (MSE)\n")
        f.write("=" * 70 + "\n\n")
        f.write("Submission URL:\n")
        f.write(url + "\n\n")
        f.write(f"Result: {result:.2f}\n")
    
    print(f"\n✓ URL also saved to: {output_file}")


if __name__ == "__main__":
    main()
