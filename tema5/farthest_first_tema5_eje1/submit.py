#!/usr/bin/env python3
"""
Submission script for Exercise 1 - Farthest First Clustering
Generates the submission URL with the computed centroids.
"""

import numpy as np
import os
import sys

# Add parent directory to path to import config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
import config


def load_centroids():
    """Load the computed centroids from the results."""
    centroids_file = os.path.join(os.path.dirname(__file__), 'centroids.npy')
    
    if not os.path.exists(centroids_file):
        print("❌ Centroids not found!")
        print("Please run farthest_first.py first to compute the results.")
        return None
    
    centroids = np.load(centroids_file)
    print(f"✓ Loaded centroids with shape: {centroids.shape}")
    return centroids


def format_centroids_for_submission(centroids):
    """
    Format centroids as nested list for API submission.
    
    The API expects format like: [[val1,val2,...],[val1,val2,...],...]
    Numbers should be rounded to 2 decimal places based on the exercise output.
    """
    # Convert to nested list and round to 2 decimals
    formatted = []
    for centroid in centroids:
        # Round each value to 2 decimal places and convert to plain float
        rounded_centroid = [round(float(val), 2) for val in centroid]
        formatted.append(rounded_centroid)
    
    return formatted


def build_submission_url(centroids):
    """Build the submission URL for the farthestFirst exercise."""
    # Get exercise info from config
    session, exercise, description = config.get_exercise_info("farthest_first_tema5_eje1")
    
    # Format centroids
    response = format_centroids_for_submission(centroids)
    
    # Build URL using config helper
    url = config.build_test_url(session, exercise, response)
    
    return url


def display_submission_info(centroids):
    """Display the submission information in a clear format."""
    print("\n" + "=" * 70)
    print("EXERCISE 1 - FARTHEST FIRST CLUSTERING")
    print("=" * 70)
    
    print("\nExercise Parameters:")
    print("  - Session: 5")
    print("  - Exercise: 1")
    print("  - E: dm matrix (229 genes × 7 timepoints)")
    print("  - k: 3")
    print("  - init: [-0.23, -0.09, -0.27, 0.2, 0.56, 1.52, 2.64]")
    
    print("\n" + "-" * 70)
    print("COMPUTED CENTROIDS")
    print("-" * 70)
    
    timepoints = ['0 hr', '9.5 hr', '11.5 hr', '13.5 hr', '15.5 hr', '18.5 hr', '20.5 hr']
    
    for i, centroid in enumerate(centroids):
        print(f"\nCentroid {i + 1}:")
        for t, val in zip(timepoints, centroid):
            print(f"  {t:8s}: {val:7.2f}")
    
    print("\n" + "-" * 70)
    print("SUBMISSION FORMAT")
    print("-" * 70)
    
    formatted = format_centroids_for_submission(centroids)
    print("\nResponse (as nested list):")
    print(formatted)
    
    # Show formatted string
    response_str = str(formatted)
    print(f"\nFormatted string:\n{response_str}")


def main():
    print("=" * 70)
    print("FARTHEST FIRST - SUBMISSION GENERATOR")
    print("=" * 70)
    
    # Load centroids
    centroids = load_centroids()
    if centroids is None:
        return
    
    # Display submission info
    display_submission_info(centroids)
    
    # Build submission URL
    url = build_submission_url(centroids)
    
    print("\n" + "=" * 70)
    print("SUBMISSION URL")
    print("=" * 70)
    print(f"\n{url}")
    
    print("\n" + "=" * 70)
    print("INSTRUCTIONS")
    print("=" * 70)
    print("""
1. Copy the URL above
2. Paste it in your browser
3. Check the response from the evaluation system
4. If correct: ✓ Points awarded!
5. If incorrect: Review the output format and try again

Note: The centroids are returned by the farthestFirst algorithm when applied to:
  - dm matrix (dgenes from Exercise 0)
  - k = 3 clusters
  - init = first dgene's expression pattern
    """)
    
    # Also save to file
    output_file = os.path.join(os.path.dirname(__file__), 'submission_url.txt')
    with open(output_file, 'w') as f:
        f.write("Exercise 1 - Farthest First Clustering\n")
        f.write("=" * 70 + "\n\n")
        f.write("Submission URL:\n")
        f.write(url + "\n\n")
        f.write("Centroids:\n")
        formatted = format_centroids_for_submission(centroids)
        for i, centroid in enumerate(formatted):
            f.write(f"Centroid {i+1}: {centroid}\n")
    
    print(f"\n✓ URL also saved to: {output_file}")


if __name__ == "__main__":
    main()
