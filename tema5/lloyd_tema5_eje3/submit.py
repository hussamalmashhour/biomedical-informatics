#!/usr/bin/env python3
"""
Submission script for Exercise 3 - Lloyd's Algorithm (K-means)
Generates the submission URL with the computed cluster assignments.
"""

import numpy as np
import os
import sys

# Add parent directory to path to import config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
import config

# Import the lloyd function
from lloyd import lloyd


def run_test_case():
    """Run the test case from the exercise."""
    print("=" * 70)
    print("EXERCISE 3 - LLOYD'S ALGORITHM (K-MEANS)")
    print("=" * 70)
    
    # Test case from exercise
    points = np.array([
        [3, 20], [4, 22], [5, 23], [3, 18], [4, 21], [5, 24],
        [21, 10], [22, 12], [23, 13], [21, 8], [20, 11], [24, 13],
        [11, 2], [12, 1], [13, 3], [15, 4], [11, 3], [14, 2]
    ], dtype=float)
    
    k = 3
    convergence = 0.1
    iterations = 100
    initCenters = np.array([[3, 20], [24, 13], [14, 2]], dtype=float)
    
    print("\nTest Case Parameters:")
    print(f"  Points shape: {points.shape}")
    print(f"  k (clusters): {k}")
    print(f"  convergence: {convergence}")
    print(f"  iterations: {iterations}")
    print(f"\nInitial Centers:")
    for i, center in enumerate(initCenters):
        print(f"    Center {i}: {center}")
    
    print("\n" + "-" * 70)
    print("Running Lloyd's Algorithm...")
    print("-" * 70 + "\n")
    
    # Run lloyd algorithm
    labels, final_centers = lloyd(points, k, convergence, iterations, initCenters=initCenters)
    
    print("-" * 70)
    print("RESULTS")
    print("-" * 70)
    
    print(f"\nFinal Centers:")
    for i, center in enumerate(final_centers):
        print(f"  Cluster {i}: {center}")
    
    print(f"\nCluster Assignments (labels):")
    print(f"  {labels}")
    
    # Show cluster sizes
    print(f"\nCluster Sizes:")
    for i in range(k):
        count = np.sum(labels == i)
        print(f"  Cluster {i}: {count} points")
    
    # Show which points belong to each cluster
    print(f"\nPoints in Each Cluster:")
    for i in range(k):
        cluster_points = points[labels == i]
        print(f"\n  Cluster {i} ({len(cluster_points)} points):")
        for j, point in enumerate(cluster_points):
            print(f"    {point}")
    
    return labels


def format_labels_for_submission(labels):
    """
    Format cluster labels as list for API submission.
    
    The API expects format like: [0,0,1,2,0,1,...]
    """
    # Convert to list of integers
    return [int(label) for label in labels]


def build_submission_url(labels):
    """Build the submission URL for the Lloyd exercise."""
    # Get exercise info from config
    session, exercise, description = config.get_exercise_info("lloyd_tema5_eje3")
    
    # Format labels
    response = format_labels_for_submission(labels)
    
    # Build URL using config helper
    url = config.build_test_url(session, exercise, response)
    
    return url


def main():
    print("=" * 70)
    print("LLOYD'S ALGORITHM - SUBMISSION GENERATOR")
    print("=" * 70)
    
    # Run test case
    labels = run_test_case()
    
    # Build submission URL
    url = build_submission_url(labels)
    
    print("\n" + "=" * 70)
    print("SUBMISSION FORMAT")
    print("=" * 70)
    
    formatted_labels = format_labels_for_submission(labels)
    print(f"\nCluster assignments (as list):")
    print(formatted_labels)
    
    print("\n" + "=" * 70)
    print("SUBMISSION URL")
    print("=" * 70)
    print(f"\n{url}")
    
    print("\n" + "=" * 70)
    print("EXPLANATION")
    print("=" * 70)
    print("""
Lloyd's Algorithm (K-means Clustering):

1. Initialize k centroids (given as initCenters in test case)
2. Repeat until convergence:
   a. Assign each point to nearest centroid
   b. Recompute centroids as mean of assigned points
   c. Check if average centroid movement < convergence threshold
3. Return cluster assignments for each point

Convergence Criterion:
  - Average movement of centroids between iterations
  - If avg_movement <= 0.1, algorithm stops
  - Maximum 100 iterations

Output:
  - Array of cluster indices [0, 1, 2, ...] for each point
  - Each index indicates which cluster the point belongs to

Note: The output depends on initialization!
  - Random initialization → different results each time
  - Fixed initCenters → deterministic result
    """)
    
    # Save to file
    output_file = os.path.join(os.path.dirname(__file__), 'submission_url.txt')
    with open(output_file, 'w') as f:
        f.write("Exercise 3 - Lloyd's Algorithm (K-means)\n")
        f.write("=" * 70 + "\n\n")
        f.write("Submission URL:\n")
        f.write(url + "\n\n")
        f.write(f"Cluster assignments:\n{formatted_labels}\n")
    
    print(f"\n✓ URL also saved to: {output_file}")


if __name__ == "__main__":
    main()
