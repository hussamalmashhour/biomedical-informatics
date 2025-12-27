#!/usr/bin/env python3
"""
Visualization script for Farthest First clustering results.
Creates simple text-based visualizations of expression patterns.
"""

import numpy as np
import os


def load_results():
    """Load clustering results."""
    # Load centroids
    centroids_file = os.path.join(os.path.dirname(__file__), 'centroids.npy')
    
    if not os.path.exists(centroids_file):
        print("❌ Results not found. Please run farthest_first.py first.")
        return None
    
    centroids = np.load(centroids_file)
    print(f"✓ Loaded {len(centroids)} centroids")
    return centroids


def plot_ascii_pattern(values, label, width=60):
    """Create ASCII plot of expression pattern."""
    print(f"\n{label}")
    print("-" * width)
    
    # Normalize to 0-width range for plotting
    min_val = min(values)
    max_val = max(values)
    range_val = max_val - min_val
    
    if range_val == 0:
        range_val = 1
    
    timepoints = ['0h', '9.5h', '11.5h', '13.5h', '15.5h', '18.5h', '20.5h']
    
    for i, (t, val) in enumerate(zip(timepoints, values)):
        # Calculate bar length
        normalized = (val - min_val) / range_val
        bar_len = int(normalized * (width - 20))
        
        # Choose character based on value
        if val > 2.3:
            char = '█'  # Strong up
        elif val > 0.5:
            char = '▓'  # Moderate up
        elif val > -0.5:
            char = '░'  # Neutral
        elif val > -2.3:
            char = '▒'  # Moderate down
        else:
            char = '▓'  # Strong down
        
        bar = char * bar_len
        print(f"{t:7s} {val:6.2f} |{bar}")
    
    print(f"\nRange: [{min_val:.2f}, {max_val:.2f}]")
    print(f"Mean: {np.mean(values):.2f}")
    print(f"Std: {np.std(values):.2f}")


def compare_centroids(centroids):
    """Compare all centroids side by side."""
    print("\n" + "=" * 70)
    print("CENTROID COMPARISON")
    print("=" * 70)
    
    timepoints = ['0h', '9.5h', '11.5h', '13.5h', '15.5h', '18.5h', '20.5h']
    
    print(f"\n{'Time':7s} ", end="")
    for i in range(len(centroids)):
        print(f"| Cent{i+1:1d}  ", end="")
    print()
    print("-" * 50)
    
    for t_idx, t in enumerate(timepoints):
        print(f"{t:7s} ", end="")
        for centroid in centroids:
            val = centroid[t_idx]
            print(f"| {val:5.2f} ", end="")
        print()


def analyze_distances(centroids):
    """Analyze distances between centroids."""
    print("\n" + "=" * 70)
    print("INTER-CENTROID DISTANCES")
    print("=" * 70)
    
    n = len(centroids)
    print("\nEuclidean distances:")
    print("     ", end="")
    for i in range(n):
        print(f"Cent{i+1:1d}  ", end="")
    print()
    
    for i in range(n):
        print(f"Cent{i+1}: ", end="")
        for j in range(n):
            dist = np.linalg.norm(centroids[i] - centroids[j])
            print(f"{dist:6.2f} ", end="")
        print()
    
    # Find most separated pair
    max_dist = 0
    max_pair = (0, 0)
    for i in range(n):
        for j in range(i+1, n):
            dist = np.linalg.norm(centroids[i] - centroids[j])
            if dist > max_dist:
                max_dist = dist
                max_pair = (i, j)
    
    print(f"\n✓ Most separated: Centroid {max_pair[0]+1} and {max_pair[1]+1}")
    print(f"  Distance: {max_dist:.2f}")


def classify_pattern(centroid):
    """Classify the expression pattern."""
    early = np.mean(centroid[:3])
    late = np.mean(centroid[4:])
    change = late - early
    
    max_val = np.max(np.abs(centroid))
    max_idx = np.argmax(np.abs(centroid))
    
    timepoints = ['0h', '9.5h', '11.5h', '13.5h', '15.5h', '18.5h', '20.5h']
    
    classification = {
        'early_mean': early,
        'late_mean': late,
        'change': change,
        'max_abs': max_val,
        'max_time': timepoints[max_idx],
        'pattern': ''
    }
    
    if change > 1.5:
        classification['pattern'] = "LATE INDUCTION"
    elif change < -1.5:
        classification['pattern'] = "LATE REPRESSION"
    elif max_val > 3:
        classification['pattern'] = "STRONG INDUCTION"
    elif max_val < -3:
        classification['pattern'] = "STRONG REPRESSION"
    else:
        classification['pattern'] = "MODERATE/STABLE"
    
    return classification


def main():
    print("=" * 70)
    print("FARTHEST FIRST CLUSTERING - VISUALIZATION")
    print("=" * 70)
    
    # Load results
    centroids = load_results()
    if centroids is None:
        return
    
    # Plot each centroid
    for i, centroid in enumerate(centroids):
        plot_ascii_pattern(centroid, f"CENTROID {i+1}")
        
        # Classify pattern
        classification = classify_pattern(centroid)
        print(f"\nPattern: {classification['pattern']}")
        print(f"Early phase (0-11.5h): {classification['early_mean']:.2f}")
        print(f"Late phase (15.5-20.5h): {classification['late_mean']:.2f}")
        print(f"Change: {classification['change']:.2f} log2 fc")
        print(f"Peak: {classification['max_abs']:.2f} at {classification['max_time']}")
    
    # Compare centroids
    compare_centroids(centroids)
    
    # Analyze distances
    analyze_distances(centroids)
    
    # Summary
    print("\n" + "=" * 70)
    print("BIOLOGICAL INTERPRETATION")
    print("=" * 70)
    print("""
The 3 centroids represent distinct expression patterns during diauxic shift:

CENTROID 1 (Late Induction):
  - Genes gradually induced as glucose depletes
  - Likely involved in: respiratory metabolism, mitochondrial function
  - Examples: genes for TCA cycle, oxidative phosphorylation

CENTROID 2 (Late Repression):
  - Genes repressed when switching to respiration
  - Likely involved in: fermentative metabolism, growth
  - Examples: glycolytic genes, ribosomal proteins

CENTROID 3 (Strong/Peak Induction):
  - Genes with strongest induction response
  - Likely involved in: stress response, metabolic reorganization
  - Examples: heat shock proteins, alternative carbon source metabolism

These patterns reflect the metabolic shift from fermentation (glucose)
to respiration (ethanol) as cells adapt to nutrient depletion.
    """)
    
    print("=" * 70)


if __name__ == "__main__":
    main()
