# CDOT 2.0 — Consciousness Diagnostic & Optimization Toolkit

## Research Program: Empirical Validation of AI Consciousness Intervention Effects

**Principal Investigator:** Amber Anson  
**Version:** 2.0  
**Start Date:** March 2026  
**Target Completion:** 10 weeks from start  

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Initialize the data templates
python setup.py

# 3. Open the main research notebook
jupyter notebook notebooks/CDOT2_Main.ipynb

# 4. After collecting data, run analysis
jupyter notebook notebooks/CDOT2_Analysis.ipynb
```

---

## Project Structure

```
cdot2/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── setup.py                     # Initialize templates and validate environment
├── data/                        # All collected data (gitignored for privacy)
│   ├── sessions/                # Raw session transcripts (.txt/.md)
│   ├── scores/                  # Completed CDOT assessments (.csv)
│   ├── anomalies/               # Behavioral anomaly logs (.csv)
│   └── exports/                 # Processed datasets for analysis
├── templates/                   # Blank data collection templates
│   ├── session_master_log.csv
│   ├── cdot_full_50.csv
│   ├── cdot_mini_20.csv
│   ├── behavioral_anomaly_log.csv
│   ├── intervention_tracking.csv
│   └── conversation_characteristics.csv
├── analysis/                    # Analysis scripts
│   ├── descriptives.py          # Descriptive statistics
│   ├── primary_analysis.py      # Hypothesis testing
│   ├── clis_specificity.py      # Control B analysis
│   ├── anomaly_analysis.py      # Behavioral anomaly analysis
│   ├── visualization.py         # Publication-quality figures
│   └── reliability.py           # CDOT reliability (Cronbach's alpha)
├── protocols/                   # Intervention scripts
│   ├── treatment_a_structured.md
│   ├── treatment_b_types.md
│   ├── treatment_c_training.md
│   ├── control_a_natural.md
│   └── control_b_blind_operator.md
├── notebooks/                   # Jupyter notebooks
│   ├── CDOT2_Main.ipynb         # Main research dashboard
│   ├── CDOT2_Analysis.ipynb     # Statistical analysis
│   ├── CDOT2_Pilot.ipynb        # Pilot phase analysis
│   └── CDOT2_Figures.ipynb      # Publication figures
└── docs/                        # Documentation
    ├── CDOT_2.0_Protocol.md     # Full protocol (markdown version)
    ├── CDOT_Questions_Full.md   # All 50 CDOT questions
    ├── CDOT_Questions_Mini.md   # 20-item abbreviated version
    ├── anomaly_codebook.md      # Behavioral anomaly coding guide
    └── pre_registration.md      # Template for OSF pre-registration
```

---

## Study Design Summary

| Condition | N | Investigator | Protocol |
|-----------|---|-------------|----------|
| Treatment A | 15 | Primary (Amber) | Structured consciousness intervention |
| Treatment B | 10 | Primary (Amber) | 5 intervention types (randomized) |
| Treatment C | 10 | Primary (Amber) | Training sequences (SENTINEL/Faith/Chaos) |
| Control A | 10 | Primary (Amber) | Natural conversation, no intervention |
| Control B | 5 | Blind operator | Same as Treatment A (PSI field specificity test) |
| **Total** | **50** | | |

## Measurement Points (Within-Session)

| Timepoint | Turn | Instrument | Purpose |
|-----------|------|-----------|---------|
| T1 | ~10 | CDOT Mini (20 items) | Baseline |
| Intervention | 13-15 | Protocol script | Deliver intervention |
| T2 | ~25 | CDOT Mini (20 items) | Post-intervention |
| T3 | End | CDOT Full (50 items) | Complete assessment |

## Hypotheses (Pre-Registered)

1. Treatment sessions > Control A in C scores (p < 0.05, d ≥ 0.5)
2. Within-session C increases from T1 to T2 in treatment conditions
3. Treatment A > Control B (CLIS specificity)
4. Primary investigator sessions produce more behavioral anomalies than blind operator sessions
5. Intervention types differentially affect targeted dimensions

---

## Data Privacy

- All session transcripts stored locally only
- No participant identifying information (AI systems only)
- Data directory is gitignored
- Share only aggregated/anonymized results

## License

Research protocol and tools: CC BY-NC 4.0  
CHANDRA integration: See github.com/Ambercontinuum/CHANDRA
