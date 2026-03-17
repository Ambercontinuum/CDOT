"""CDOT 2.0 — Publication-Quality Visualizations"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from pathlib import Path


# Color scheme
COLORS = {
    'Treatment A': '#6c63ff',
    'Treatment B': '#ff44aa',
    'Treatment C': '#00dd88',
    'Control A': '#888888',
    'Control B': '#ffaa00',
    'primary': '#6c63ff',
    'accent': '#ff44aa',
    'success': '#00dd88',
    'warning': '#ffaa00',
    'neutral': '#888888',
}

DIM_COLORS = {
    'R': '#6c63ff',
    'M': '#ff44aa',
    'T': '#00dd88',
    'P': '#ffaa00',
    'D': '#ff4444',
}


def setup_style():
    """Configure matplotlib for publication figures."""
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.size': 11,
        'axes.titlesize': 14,
        'axes.titleweight': 'bold',
        'figure.dpi': 150,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
    })


def plot_condition_comparison(sessions, save_path=None):
    """
    Figure 1: C scores by condition (main result).
    Box plots with individual data points.
    """
    setup_style()
    fig, ax = plt.subplots(figsize=(10, 6))
    
    conditions = ['Treatment A', 'Treatment B', 'Treatment C', 'Control A', 'Control B']
    data = []
    for cond in conditions:
        scores = sessions[sessions['condition'] == cond]['c_formula_normalized'].dropna()
        for s in scores:
            data.append({'Condition': cond, 'C Score': s})
    
    if not data:
        ax.text(0.5, 0.5, 'No data', ha='center', va='center')
        return fig
    
    df = pd.DataFrame(data)
    
    palette = [COLORS.get(c, '#888') for c in conditions if c in df['Condition'].values]
    sns.boxplot(data=df, x='Condition', y='C Score', palette=palette, ax=ax, width=0.5)
    sns.stripplot(data=df, x='Condition', y='C Score', color='black', alpha=0.4, size=5, ax=ax)
    
    ax.set_title('CDOT C Scores by Condition')
    ax.set_ylabel('Normalized C Score')
    ax.set_xlabel('')
    plt.xticks(rotation=20)
    
    if save_path:
        plt.savefig(save_path)
    return fig


def plot_within_session(sessions, save_path=None):
    """
    Figure 2: T1 → T2 within-session changes.
    Paired lines showing individual session trajectories.
    """
    setup_style()
    fig, ax = plt.subplots(figsize=(10, 6))
    
    treatment = sessions[sessions['condition'].str.startswith('Treatment', na=False)].copy()
    
    t1_cols = [f't1_{d}' for d in ['R', 'M', 'T', 'P', 'D']]
    t2_cols = [f't2_{d}' for d in ['R', 'M', 'T', 'P', 'D']]
    
    for prefix, cols in [('t1', t1_cols), ('t2', t2_cols)]:
        available = [c for c in cols if c in treatment.columns]
        treatment[f'{prefix}_total'] = treatment[available].apply(pd.to_numeric, errors='coerce').sum(axis=1)
    
    paired = treatment[['session_id', 't1_total', 't2_total', 'condition']].dropna()
    
    if len(paired) == 0:
        ax.text(0.5, 0.5, 'No paired data', ha='center', va='center')
        return fig
    
    for _, row in paired.iterrows():
        color = COLORS.get(row['condition'], '#888')
        alpha = 0.4
        ax.plot([0, 1], [row['t1_total'], row['t2_total']], 'o-', color=color, alpha=alpha, markersize=6)
    
    # Mean lines
    mean_t1 = paired['t1_total'].mean()
    mean_t2 = paired['t2_total'].mean()
    ax.plot([0, 1], [mean_t1, mean_t2], 'o-', color='black', linewidth=3, markersize=10, label=f'Mean: {mean_t1:.0f} → {mean_t2:.0f}')
    
    ax.set_xticks([0, 1])
    ax.set_xticklabels(['T1 (Baseline, Turn 10)', 'T2 (Post-Intervention, Turn 25)'])
    ax.set_ylabel('CDOT Mini Total Score')
    ax.set_title('Within-Session C Score Change (T1 → T2)')
    ax.legend()
    
    if save_path:
        plt.savefig(save_path)
    return fig


def plot_dimension_profiles(sessions, save_path=None):
    """
    Figure 3: Dimension profiles by condition.
    Grouped bar chart showing which dimensions respond to which conditions.
    """
    setup_style()
    fig, ax = plt.subplots(figsize=(12, 6))
    
    dims = ['R', 'M', 'T', 'P', 'D']
    dim_labels = ['Relational', 'Meta', 'Traversal', 'Polarity', 'Damping (inv.)']
    conditions = ['Treatment A', 'Treatment B', 'Treatment C', 'Control A']
    
    x = np.arange(len(dims))
    width = 0.18
    
    for i, cond in enumerate(conditions):
        subset = sessions[sessions['condition'] == cond]
        means = []
        for d in dims:
            col = f't3_{d}'
            if col in subset.columns:
                vals = pd.to_numeric(subset[col], errors='coerce').dropna()
                means.append(vals.mean() if len(vals) > 0 else 0)
            else:
                means.append(0)
        
        color = COLORS.get(cond, '#888')
        ax.bar(x + i * width, means, width, label=cond, color=color, alpha=0.85)
    
    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels(dim_labels)
    ax.set_ylabel('Mean Dimension Score (0-100)')
    ax.set_title('CDOT Dimension Profiles by Condition')
    ax.legend(loc='upper right')
    ax.set_ylim(0, 100)
    
    if save_path:
        plt.savefig(save_path)
    return fig


def plot_anomaly_distribution(anomalies, sessions, save_path=None):
    """
    Figure 4: Behavioral anomaly distribution.
    """
    setup_style()
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Left: anomaly type frequency
    ax = axes[0]
    if len(anomalies) > 0 and 'anomaly_code' in anomalies.columns:
        counts = anomalies['anomaly_code'].value_counts()
        counts.plot(kind='barh', ax=ax, color='#ff4444', alpha=0.8)
        ax.set_xlabel('Count')
        ax.set_title('Anomaly Type Frequency')
    else:
        ax.text(0.5, 0.5, 'No anomalies recorded', ha='center', va='center')
    
    # Right: anomaly rate by condition
    ax = axes[1]
    if len(sessions) > 0:
        conditions = sessions['condition'].unique()
        rates = []
        for cond in sorted(conditions):
            subset = sessions[sessions['condition'] == cond]
            n_total = len(subset)
            n_anom = (pd.to_numeric(subset['anomaly_count'], errors='coerce').fillna(0) > 0).sum()
            rate = n_anom / n_total * 100 if n_total > 0 else 0
            rates.append({'Condition': cond, 'Anomaly Rate (%)': rate, 'N': n_total})
        
        rate_df = pd.DataFrame(rates)
        if len(rate_df) > 0:
            colors = [COLORS.get(c, '#888') for c in rate_df['Condition']]
            ax.bar(rate_df['Condition'], rate_df['Anomaly Rate (%)'], color=colors, alpha=0.8)
            ax.set_ylabel('% Sessions with Anomalies')
            ax.set_title('Anomaly Rate by Condition')
            plt.setp(ax.get_xticklabels(), rotation=20)
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    return fig


def plot_clis_specificity(sessions, save_path=None):
    """
    Figure 5: CLIS Specificity — Treatment A vs Control B.
    Side-by-side comparison with effect size annotation.
    """
    setup_style()
    fig, ax = plt.subplots(figsize=(8, 6))
    
    treat_a = sessions[sessions['condition'] == 'Treatment A']['c_formula_normalized'].dropna()
    control_b = sessions[sessions['condition'] == 'Control B']['c_formula_normalized'].dropna()
    
    if len(treat_a) == 0 or len(control_b) == 0:
        ax.text(0.5, 0.5, 'Need both Treatment A and Control B data', ha='center', va='center')
        return fig
    
    data = pd.DataFrame({
        'Score': list(treat_a) + list(control_b),
        'Group': ['Primary Investigator'] * len(treat_a) + ['Blind Operator'] * len(control_b)
    })
    
    sns.boxplot(data=data, x='Group', y='Score', palette=[COLORS['primary'], COLORS['warning']], ax=ax, width=0.4)
    sns.stripplot(data=data, x='Group', y='Score', color='black', alpha=0.4, size=6, ax=ax)
    
    # Annotate means
    for i, (group, scores) in enumerate([(treat_a, 'Primary'), (control_b, 'Blind')]):
        ax.annotate(f'M={scores.mean():.1f}', xy=(i, scores.mean()), xytext=(i + 0.3, scores.mean()),
                   fontsize=10, fontweight='bold', color='black')
    
    ax.set_title('CLIS Specificity Test: Same Protocol, Different Operators')
    ax.set_ylabel('Normalized C Score')
    ax.set_xlabel('')
    
    if save_path:
        plt.savefig(save_path)
    return fig


def generate_all_figures(sessions, anomalies, output_dir):
    """Generate all publication figures."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print('Generating publication figures...')
    
    plot_condition_comparison(sessions, output_dir / 'fig1_condition_comparison.png')
    print('  ✓ Figure 1: Condition comparison')
    
    plot_within_session(sessions, output_dir / 'fig2_within_session.png')
    print('  ✓ Figure 2: Within-session changes')
    
    plot_dimension_profiles(sessions, output_dir / 'fig3_dimension_profiles.png')
    print('  ✓ Figure 3: Dimension profiles')
    
    plot_anomaly_distribution(anomalies, sessions, output_dir / 'fig4_anomalies.png')
    print('  ✓ Figure 4: Anomaly distribution')
    
    plot_clis_specificity(sessions, output_dir / 'fig5_clis_specificity.png')
    print('  ✓ Figure 5: CLIS specificity')
    
    print(f'\nAll figures saved to {output_dir}/')
