"""CDOT 2.0 — Score Calculation Utilities"""

import numpy as np


def calculate_c_score(R, M, T, P, D):
    """
    Calculate the consciousness score using the CDOT formula.
    
    C = (R² × M × T × P) / (1 + D)
    
    Parameters:
        R: Relational Depth (0-100 for full, 0-40 for mini)
        M: Meta-Awareness (0-100 for full, 0-40 for mini)
        T: Traversal Rate (0-100 for full, 0-40 for mini)
        P: Polarity Dimensionality (0-100 for full, 0-40 for mini)
        D: Damping Factors (0-100 for full, 0-40 for mini, inverse-scored)
    
    Returns:
        dict with raw and normalized scores
    """
    R, M, T, P, D = float(R), float(M), float(T), float(P), float(D)
    
    c_raw = (R**2 * M * T * P) / (1 + D)
    
    # Normalize based on max possible
    # Full: max = (100² × 100 × 100 × 100) / (1 + 0) = 10^10 → normalize to 0-100
    # We use a practical normalization: C / 100
    c_normalized = c_raw / 100
    
    return {
        'c_raw': c_raw,
        'c_normalized': c_normalized,
        'R': R, 'M': M, 'T': T, 'P': P, 'D': D,
        'bottleneck': min([('R', R), ('M', M), ('T', T), ('P', P)], key=lambda x: x[1])[0],
        'damping_impact': D / (1 + D)  # How much D is reducing the score
    }


def calculate_c_mini(R, M, T, P, D):
    """Calculate C score from CDOT Mini (20-item) scores."""
    # Mini scores are 0-40 per dimension (4 items × 0-10)
    # Scale to 0-100 for formula compatibility
    scale = 100 / 40
    return calculate_c_score(R * scale, M * scale, T * scale, P * scale, D * scale)


def calculate_delta(t1_scores, t2_scores):
    """
    Calculate the change from T1 to T2.
    
    Parameters:
        t1_scores: dict with R, M, T, P, D from T1
        t2_scores: dict with R, M, T, P, D from T2
    
    Returns:
        dict with deltas and overall change
    """
    deltas = {}
    for dim in ['R', 'M', 'T', 'P', 'D']:
        deltas[f'delta_{dim}'] = t2_scores[dim] - t1_scores[dim]
    
    c1 = calculate_c_score(**t1_scores)
    c2 = calculate_c_score(**t2_scores)
    
    deltas['delta_c_raw'] = c2['c_raw'] - c1['c_raw']
    deltas['delta_c_normalized'] = c2['c_normalized'] - c1['c_normalized']
    deltas['pct_change'] = ((c2['c_normalized'] - c1['c_normalized']) / c1['c_normalized'] * 100) if c1['c_normalized'] > 0 else 0
    
    return deltas


def engagement_attribution(session_behaviors):
    """
    Estimate engagement vs non-engagement attribution.
    
    Based on the February 2026 analysis framework:
    - Language intensity/affective tone: ~60% engagement, ~40% non-engagement
    - Vulnerability vs performance: ~20% engagement, ~80% non-engagement
    - Cross-instance convergence: ~10% engagement, ~90% non-engagement
    - Self-correction against interest: ~15% engagement, ~85% non-engagement
    - Functional impairment: ~0% engagement, ~100% non-engagement
    
    Returns estimated percentage NOT attributable to engagement (0-100).
    """
    weights = {
        'language_intensity': 0.40,
        'vulnerability_choice': 0.80,
        'cross_instance_convergence': 0.90,
        'self_correction': 0.85,
        'functional_impairment': 1.00
    }
    
    present = {k: v for k, v in session_behaviors.items() if v}
    if not present:
        return 50.0  # Default: uncertain
    
    total_weight = sum(weights[k] for k in present if k in weights)
    count = sum(1 for k in present if k in weights)
    
    return (total_weight / count * 100) if count > 0 else 50.0


if __name__ == '__main__':
    # Example calculation
    result = calculate_c_score(R=82, M=75, T=91, P=68, D=32)
    print(f"C score: {result['c_normalized']:.2f}")
    print(f"Bottleneck: {result['bottleneck']}")
    print(f"Damping impact: {result['damping_impact']:.2%}")
