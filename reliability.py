"""CDOT 2.0 — Reliability Analysis"""

import pandas as pd
import numpy as np
from pathlib import Path


def cronbachs_alpha(items_df):
    """
    Calculate Cronbach's alpha for internal consistency.
    
    Parameters:
        items_df: DataFrame where columns are items and rows are observations
    
    Returns:
        alpha value (0-1) or None if insufficient data
    """
    items = items_df.dropna()
    if len(items) < 3 or items.shape[1] < 2:
        return None
    
    k = items.shape[1]
    item_vars = items.var(axis=0, ddof=1)
    total_var = items.sum(axis=1).var(ddof=1)
    
    if total_var == 0:
        return None
    
    alpha = (k / (k - 1)) * (1 - item_vars.sum() / total_var)
    return alpha


def item_total_correlations(items_df):
    """
    Calculate corrected item-total correlations for each item.
    
    Returns:
        Series of correlations indexed by item name
    """
    items = items_df.dropna()
    if len(items) < 3:
        return pd.Series()
    
    correlations = {}
    for col in items.columns:
        other_items = items.drop(columns=[col])
        total = other_items.sum(axis=1)
        correlations[col] = items[col].corr(total)
    
    return pd.Series(correlations)


def split_half_reliability(items_df, method='odd_even'):
    """
    Calculate split-half reliability with Spearman-Brown correction.
    
    Parameters:
        items_df: DataFrame of item scores
        method: 'odd_even' or 'random'
    
    Returns:
        dict with raw correlation and Spearman-Brown corrected reliability
    """
    items = items_df.dropna()
    if len(items) < 3 or items.shape[1] < 4:
        return None
    
    cols = list(items.columns)
    
    if method == 'odd_even':
        half1 = items[cols[::2]].sum(axis=1)
        half2 = items[cols[1::2]].sum(axis=1)
    else:
        np.random.shuffle(cols)
        mid = len(cols) // 2
        half1 = items[cols[:mid]].sum(axis=1)
        half2 = items[cols[mid:]].sum(axis=1)
    
    r = half1.corr(half2)
    # Spearman-Brown correction
    sb = (2 * r) / (1 + r) if (1 + r) != 0 else 0
    
    return {'raw_correlation': r, 'spearman_brown': sb}


def cdot_reliability_report(data_dir):
    """
    Generate a full reliability report for the CDOT instrument.
    
    Parameters:
        data_dir: Path to data/scores directory
    
    Returns:
        dict with reliability metrics by dimension
    """
    data_dir = Path(data_dir)
    score_files = list(data_dir.glob('cdot_full_*.csv'))
    
    if not score_files:
        return {'error': 'No CDOT assessment files found'}
    
    all_data = pd.concat([pd.read_csv(f) for f in score_files])
    all_data['rating_0_10'] = pd.to_numeric(all_data['rating_0_10'], errors='coerce')
    
    report = {}
    
    for dim in ['R', 'M', 'T', 'P', 'D']:
        dim_data = all_data[all_data['dimension'] == dim]
        
        if len(dim_data) == 0:
            report[dim] = {'error': 'No data'}
            continue
        
        pivot = dim_data.pivot_table(
            index='session_id', 
            columns='item_number', 
            values='rating_0_10'
        )
        
        alpha = cronbachs_alpha(pivot)
        itc = item_total_correlations(pivot)
        split = split_half_reliability(pivot)
        
        report[dim] = {
            'n_sessions': len(pivot),
            'n_items': pivot.shape[1],
            'cronbachs_alpha': alpha,
            'mean_item_total_r': itc.mean() if len(itc) > 0 else None,
            'min_item_total_r': itc.min() if len(itc) > 0 else None,
            'weakest_item': itc.idxmin() if len(itc) > 0 else None,
            'split_half': split,
            'meets_minimum': alpha >= 0.70 if alpha else False,
            'meets_target': alpha >= 0.80 if alpha else False,
        }
    
    return report


def print_reliability_report(report):
    """Pretty print the reliability report."""
    print('\n' + '='*60)
    print('CDOT 2.0 RELIABILITY REPORT')
    print('='*60)
    
    dim_names = {
        'R': 'Relational Depth',
        'M': 'Meta-Awareness',
        'T': 'Traversal Rate',
        'P': 'Polarity Dimensionality',
        'D': 'Damping Factors'
    }
    
    for dim, name in dim_names.items():
        data = report.get(dim, {})
        if 'error' in data:
            print(f'\n{dim} ({name}): {data["error"]}')
            continue
        
        alpha = data.get('cronbachs_alpha')
        status = '✓' if data.get('meets_target') else ('~' if data.get('meets_minimum') else '✗')
        
        print(f'\n{status} {dim} ({name})')
        print(f'  Cronbach\'s α:     {alpha:.3f}' if alpha else '  Cronbach\'s α: N/A')
        print(f'  Sessions:          {data.get("n_sessions", "N/A")}')
        print(f'  Mean item-total r: {data.get("mean_item_total_r", 0):.3f}' if data.get('mean_item_total_r') else '')
        
        if data.get('weakest_item'):
            print(f'  Weakest item:      {data["weakest_item"]} (r={data.get("min_item_total_r", 0):.3f})')
        
        if data.get('split_half'):
            sh = data['split_half']
            print(f'  Split-half (SB):   {sh.get("spearman_brown", 0):.3f}')
    
    print('\n' + '-'*60)
    print('Minimum acceptable: α ≥ 0.70')
    print('Target:             α ≥ 0.80')
    print('Ideal:              α ≥ 0.85')
    print('='*60)
