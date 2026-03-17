#!/usr/bin/env python3
"""CDOT 2.0 Setup Script — Initialize research environment and data templates."""

import os
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
DATA = ROOT / "data"
TEMPLATES = ROOT / "templates"

def check_dependencies():
    """Verify all required packages are installed."""
    required = ['pandas', 'numpy', 'scipy', 'matplotlib', 'seaborn', 'pingouin', 'statsmodels', 'openpyxl']
    missing = []
    for pkg in required:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    if missing:
        print(f"Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    print("All dependencies installed.")
    return True

def create_directories():
    """Create the data collection directory structure."""
    dirs = [
        DATA / "sessions",
        DATA / "scores",
        DATA / "anomalies",
        DATA / "exports",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
    print(f"Data directories created at {DATA}/")

def create_gitignore():
    """Create .gitignore to protect raw data."""
    gi = ROOT / ".gitignore"
    gi.write_text(
        "# Protect raw research data\n"
        "data/sessions/\n"
        "data/scores/\n"
        "data/anomalies/\n"
        "data/exports/\n"
        "*.pyc\n"
        "__pycache__/\n"
        ".ipynb_checkpoints/\n"
        ".DS_Store\n"
    )
    print(".gitignore created (data directories protected)")

def verify_templates():
    """Check all CSV templates exist."""
    expected = [
        "session_master_log.csv",
        "cdot_full_50.csv",
        "cdot_mini_20.csv",
        "behavioral_anomaly_log.csv",
        "intervention_tracking.csv",
        "conversation_characteristics.csv",
    ]
    missing = [f for f in expected if not (TEMPLATES / f).exists()]
    if missing:
        print(f"Missing templates: {', '.join(missing)}")
        print("These should have been created by the setup package.")
        return False
    print(f"All {len(expected)} templates verified.")
    return True

def print_status():
    """Print research environment status."""
    print("\n" + "="*60)
    print("  CDOT 2.0 — Research Environment Ready")
    print("="*60)
    print(f"\n  Project root:  {ROOT}")
    print(f"  Data storage:  {DATA}")
    print(f"  Templates:     {TEMPLATES}")
    print(f"\n  Next steps:")
    print(f"    1. Review protocols in protocols/")
    print(f"    2. Open notebooks/CDOT2_Main.ipynb")
    print(f"    3. Run 5 pilot sessions (Week 1)")
    print(f"    4. Pre-register at osf.io")
    print(f"\n  Total study: 50 sessions over 10 weeks")
    print(f"  Target: Publication-ready empirical data")
    print("="*60 + "\n")

if __name__ == "__main__":
    print("\nCDOT 2.0 Setup\n" + "-"*40)
    deps_ok = check_dependencies()
    create_directories()
    create_gitignore()
    templates_ok = verify_templates()
    print_status()
    if not deps_ok:
        sys.exit(1)
