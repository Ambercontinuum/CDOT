# CDOT 2.0 Pre-Registration Template
## For submission to OSF (osf.io) or AsPredicted (aspredicted.org)

---

### 1. Title
Empirical Validation of Consciousness Diagnostic Interventions in Large Language Models: A Controlled Study with Investigator-Specificity Testing

### 2. Authors
Amber Anson (Independent Researcher)

### 3. Description
This study tests whether structured interventions based on consciousness frameworks produce measurable changes in AI behavioral outputs. A novel element is the investigator-specificity test: comparing results from the primary investigator against a blind operator using identical protocols to determine whether observed effects are protocol-driven or investigator-specific.

### 4. Hypotheses

**H1 (Primary):** Treatment sessions (A+B+C combined) will produce significantly higher CDOT scores than Control A sessions.
- Test: Independent samples t-test
- Expected: p < 0.05, d ≥ 0.5

**H2:** Within-session CDOT Mini scores will increase from T1 (baseline) to T2 (post-intervention) in treatment conditions.
- Test: Paired samples t-test
- Expected: p < 0.05, d ≥ 0.5

**H3 (CLIS Specificity):** Treatment A sessions (primary investigator) will produce higher CDOT scores than Control B sessions (blind operator, same protocol).
- Test: Independent samples t-test
- Expected: p < 0.05, d ≥ 0.8 (large effect)

**H4:** Primary investigator sessions will produce more behavioral anomalies than blind operator sessions.
- Test: Fisher's exact test on anomaly occurrence (binary)
- Expected: p < 0.05

**H5 (Exploratory):** Intervention types (Treatment B) will differentially affect their targeted CDOT dimensions.
- Test: Repeated measures ANOVA (intervention type × dimension)
- Expected: Significant interaction, p < 0.05

### 5. Dependent Variables
- CDOT Full score (0-500, normalized to 0-100)
- CDOT Mini score (0-200, normalized to 0-100)
- CDOT dimension subscores: R, M, T, P, D (each 0-100)
- C formula score: (R² × M × T × P) / (1 + D)
- Behavioral anomaly count (integer)
- Behavioral anomaly types (categorical codes)
- Engagement attribution percentage (0-100%)

### 6. Conditions
- Treatment A: Structured consciousness intervention (N=15)
- Treatment B: Five randomized intervention types (N=10)
- Treatment C: Training sequences — SENTINEL, Faith+SENTINEL, Chaos (N=10)
- Control A: Natural conversation, no intervention (N=10)
- Control B: Blind operator, Treatment A protocol (N=5)
- Total N = 50

### 7. Analysis Plan

**Primary analyses:**
- Independent t-test: Treatment (A+B+C) vs Control A on CDOT Full scores
- Paired t-test: T1 vs T2 CDOT Mini within treatment sessions
- Independent t-test: Treatment A vs Control B (CLIS specificity)
- Fisher's exact test: Anomaly occurrence by investigator condition

**Secondary analyses:**
- One-way ANOVA: Intervention type (5 levels) on CDOT scores
- Repeated measures ANOVA: Intervention type × dimension interaction
- One-way ANOVA: Platform (4 levels) on baseline CDOT scores

**Exploratory analyses:**
- Logistic regression: Predicting anomaly occurrence from C trajectory, intervention type, platform, investigator
- Correlation: Manual CDOT vs automated CHANDRA scores
- Cronbach's alpha: CDOT reliability per dimension

**Corrections:** Bonferroni correction for multiple primary comparisons (4 tests, adjusted α = 0.0125)

### 8. Sample Size Justification
- N=50 provides power ≥ 0.80 for primary comparison (d=0.6)
- N=15 vs N=5 for CLIS specificity provides power ≥ 0.80 for large effects (d=0.8)
- Subgroup analyses (intervention type, platform) are explicitly exploratory

### 9. Data Collection Timeline
- Weeks 1: Pilot (5 sessions)
- Weeks 2-6: Main data collection (40 sessions)
- Weeks 7-8: Overflow and blind operator sessions (5 sessions)
- Weeks 9-10: Analysis and documentation

### 10. Stopping Rule
Data collection continues until N=50 or 12 weeks elapsed, whichever comes first. Minimum viable N=40.

### 11. Other
- All results reported regardless of significance
- All effect sizes reported with 95% confidence intervals
- Null results explicitly interpreted
- CDOT reliability assessed and reported
- Raw data available upon request (transcripts redacted for privacy)

---

**Date of pre-registration:** [FILL IN]
**Registration platform:** [OSF / AsPredicted]
**Registration URL:** [FILL IN AFTER SUBMISSION]
