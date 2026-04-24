# AMR Prediction System — UI Flow Diagrams & Development Logs

---

# PART 1: UI FLOW DIAGRAMS

---

## UI Screen Navigation Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER OPENS APP                               │
│                     http://localhost:5000                         │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      SCREEN 1: LANDING PAGE                          │
│                                                                      │
│  ┌───────────────────────────────────────────────────────────────┐   │
│  │  NAVBAR:  [Home (active)]  [Predict]  [History]  [About]     │   │
│  ├───────────────────────────────────────────────────────────────┤   │
│  │                                                               │   │
│  │  ╔═══════════════════════════════════════════════════════════╗│   │
│  │  ║              HERO SECTION (full width banner)             ║│   │
│  │  ║                                                           ║│   │
│  │  ║     Multi-Drug AMR Prediction System                      ║│   │
│  │  ║     ════════════════════════════════                       ║│   │
│  │  ║                                                           ║│   │
│  │  ║     Predict antibiotic resistance (Sensitive / Resistant) ║│   │
│  │  ║     for multiple drugs against a single microbe —         ║│   │
│  │  ║     powered by Machine Learning & Deep Learning.          ║│   │
│  │  ║                                                           ║│   │
│  │  ║     [ Start Prediction ]      [ View History ]            ║│   │
│  │  ║                                                           ║│   │
│  │  ╚═══════════════════════════════════════════════════════════╝│   │
│  │                                                               │   │
│  │  ─────────────────────────────────────────────────────────    │   │
│  │                                                               │   │
│  │  SECTION: Problem Statement                                   │   │
│  │  ┌───────────────────────────────────────────────────────┐    │   │
│  │  │                                                       │    │   │
│  │  │  Antimicrobial Resistance (AMR) is a growing global   │    │   │
│  │  │  health threat. When bacteria become resistant to     │    │   │
│  │  │  antibiotics, infections become harder to treat.      │    │   │
│  │  │                                                       │    │   │
│  │  │  This system predicts whether a microbe is:           │    │   │
│  │  │                                                       │    │   │
│  │  │    S (Sensitive)  → Drug WILL work against microbe    │    │   │
│  │  │    R (Resistant)  → Drug will NOT work, avoid it      │    │   │
│  │  │                                                       │    │   │
│  │  │  for single or multiple drugs at once.                │    │   │
│  │  │                                                       │    │   │
│  │  └───────────────────────────────────────────────────────┘    │   │
│  │                                                               │   │
│  │  ─────────────────────────────────────────────────────────    │   │
│  │                                                               │   │
│  │  SECTION: How It Works (Step-by-step visual)                  │   │
│  │  ┌───────────────────────────────────────────────────────┐    │   │
│  │  │                                                       │    │   │
│  │  │   STEP 1            STEP 2            STEP 3          │    │   │
│  │  │  ┌────────┐       ┌────────┐        ┌────────────┐   │    │   │
│  │  │  │ Enter  │  ───► │ Select │  ───►  │ Auto-Gen   │   │    │   │
│  │  │  │Patient │       │Microbe │        │ Full Report│   │    │   │
│  │  │  │  Info  │       │+ Data  │        │ ALL Drugs  │   │    │   │
│  │  │  └────────┘       └────────┘        └────────────┘   │    │   │
│  │  │      │                │                  │            │    │   │
│  │  │  Age, Gender,    Microbe type       System auto-     │    │   │
│  │  │  Hypertension,   + Genomic/Lab      predicts S/R     │    │   │
│  │  │  Diabetes         features          for EVERY drug   │    │   │
│  │  │                                     against this     │    │   │
│  │  │                      │              microbe          │    │   │
│  │  │                      ▼                               │    │   │
│  │  │               RESULT                                  │    │   │
│  │  │              ┌────────────────┐                        │    │   │
│  │  │              │ Full AMR Report│                        │    │   │
│  │  │              │ ALL drugs S/R  │                        │    │   │
│  │  │              │ + best drug    │                        │    │   │
│  │  │              │ + avoid list   │                        │    │   │
│  │  │              └────────────────┘                        │    │   │
│  │  │                                                       │    │   │
│  │  └───────────────────────────────────────────────────────┘    │   │
│  │                                                               │   │
│  │  ─────────────────────────────────────────────────────────    │   │
│  │                                                               │   │
│  │  SECTION: How Prediction Works                                │   │
│  │  ┌───────────────────────────────────────────────────────┐    │   │
│  │  │                                                       │    │   │
│  │  │  DEFAULT: Full Report on ALL Drugs (Auto-Generated)   │    │   │
│  │  │  ─────────────────────────────────────────────────    │    │   │
│  │  │                                                       │    │   │
│  │  │  When you select a microbe, the system                │    │   │
│  │  │  AUTOMATICALLY generates a full resistance            │    │   │
│  │  │  report for EVERY drug in the database                │    │   │
│  │  │  against that microbe. No need to pick drugs.         │    │   │
│  │  │                                                       │    │   │
│  │  │  ┌─────────────────────────────────────────────┐      │    │   │
│  │  │  │  Select microbe: E. coli                    │      │    │   │
│  │  │  │           │                                 │      │    │   │
│  │  │  │           ▼  (auto-generates)               │      │    │   │
│  │  │  │                                             │      │    │   │
│  │  │  │  Drug_A (Amoxicillin)    → S  92%           │      │    │   │
│  │  │  │  Drug_B (Ciprofloxacin)  → R  78%           │      │    │   │
│  │  │  │  Drug_C (Meropenem)      → S  95%           │      │    │   │
│  │  │  │  Drug_D (Gentamicin)     → S  88%           │      │    │   │
│  │  │  │  Drug_E (Tetracycline)   → R  81%           │      │    │   │
│  │  │  │  Drug_F (Trimethoprim)   → R  84%           │      │    │   │
│  │  │  │  ... (all drugs in DB)                      │      │    │   │
│  │  │  │                                             │      │    │   │
│  │  │  │  BEST → Meropenem (95%)                     │      │    │   │
│  │  │  │  AVOID → Ciprofloxacin, Tetracycline,       │      │    │   │
│  │  │  │          Trimethoprim                        │      │    │   │
│  │  │  └─────────────────────────────────────────────┘      │    │   │
│  │  │                                                       │    │   │
│  │  └───────────────────────────────────────────────────────┘    │   │
│  │                                                               │   │
│  │  ┌──────────────────────────┐  ┌──────────────────────────┐   │   │
│  │  │                          │  │                          │   │   │
│  │  │  FULL REPORT (Default)   │  │  SINGLE DRUG (Optional)  │   │   │
│  │  │  ──────────────────      │  │  ─────────────────       │   │   │
│  │  │                          │  │                          │   │   │
│  │  │  Select microbe → auto   │  │  Filter the full report  │   │   │
│  │  │  screens ALL drugs.      │  │  to focus on ONE drug.   │   │   │
│  │  │                          │  │                          │   │   │
│  │  │  Output:                 │  │  Output:                 │   │   │
│  │  │  Complete S/R table      │  │  Drug_A → S or R         │   │   │
│  │  │  for every drug.         │  │  with detailed info.     │   │   │
│  │  │                          │  │                          │   │   │
│  │  │  Includes:               │  │  Use when:               │   │   │
│  │  │  - Per drug S/R          │  │  Doctor already knows    │   │   │
│  │  │  - Best drug pick        │  │  which drug to check.    │   │   │
│  │  │  - Avoid list            │  │                          │   │   │
│  │  │  - Clinical summary      │  │  Model:                  │   │   │
│  │  │                          │  │  Binary Classifier       │   │   │
│  │  │  Model:                  │  │  (per drug)              │   │   │
│  │  │  Multi-Label Classifier  │  │                          │   │   │
│  │  │  (all drugs at once)     │  │                          │   │   │
│  │  │                          │  │                          │   │   │
│  │  │  [ Start Full Report ]   │  │  [ Try Single Drug ]     │   │   │
│  │  │                          │  │                          │   │   │
│  │  └──────────────────────────┘  └──────────────────────────┘   │   │
│  │                                                               │   │
│  │  ─────────────────────────────────────────────────────────    │   │
│  │                                                               │   │
│  │  SECTION: What Inputs Does It Need?                           │   │
│  │  ┌───────────────────────────────────────────────────────┐    │   │
│  │  │                                                       │    │   │
│  │  │  Patient Clinical Data:                               │    │   │
│  │  │  ┌──────────┐ ┌────────┐ ┌──────────────┐ ┌────────┐ │    │   │
│  │  │  │   Age    │ │ Gender │ │ Hypertension │ │Diabetes│ │    │   │
│  │  │  │  (years) │ │ (M/F)  │ │  (Yes/No)    │ │(Yes/No)│ │    │   │
│  │  │  └──────────┘ └────────┘ └──────────────┘ └────────┘ │    │   │
│  │  │                                                       │    │   │
│  │  │  Why patient data matters:                            │    │   │
│  │  │  • Age → Elderly have more prior antibiotic exposure  │    │   │
│  │  │  • Gender → UTI resistance differs between M/F       │    │   │
│  │  │  • Hypertension → affects drug metabolism history     │    │   │
│  │  │  • Diabetes → higher infection & antibiotic exposure  │    │   │
│  │  │                                                       │    │   │
│  │  │  Microbe Data:                                        │    │   │
│  │  │  ┌──────────────┐ ┌──────────────────────────────┐    │    │   │
│  │  │  │ Microbe Type │ │ Genomic / Lab Culture        │    │    │   │
│  │  │  │ (E.coli,     │ │ Features (MIC, zone          │    │    │   │
│  │  │  │  S.aureus,   │ │ diameter, gene markers, etc.)│    │    │   │
│  │  │  │  K.pneumo..) │ │                              │    │    │   │
│  │  │  └──────────────┘ └──────────────────────────────┘    │    │   │
│  │  │                                                       │    │   │
│  │  └───────────────────────────────────────────────────────┘    │   │
│  │                                                               │   │
│  │  ─────────────────────────────────────────────────────────    │   │
│  │                                                               │   │
│  │  SECTION: Models Under the Hood                               │   │
│  │  ┌───────────────────────────────────────────────────────┐    │   │
│  │  │                                                       │    │   │
│  │  │  ┌─────────────────────────────────────────────────┐  │    │   │
│  │  │  │  ML: Random Forest (scikit-learn)               │  │    │   │
│  │  │  │  ─────────────────────────────────              │  │    │   │
│  │  │  │  • Single: RandomForestClassifier()             │  │    │   │
│  │  │  │  • Multi:  MultiOutputClassifier(               │  │    │   │
│  │  │  │              RandomForestClassifier()            │  │    │   │
│  │  │  │            )                                    │  │    │   │
│  │  │  │  • Each drug treated as separate output label   │  │    │   │
│  │  │  │  • Robust, interpretable, fast training         │  │    │   │
│  │  │  └─────────────────────────────────────────────────┘  │    │   │
│  │  │                                                       │    │   │
│  │  │  ┌─────────────────────────────────────────────────┐  │    │   │
│  │  │  │  DL: FT-Transformer (rtdl / PyTorch)            │  │    │   │
│  │  │  │  ─────────────────────────────────              │  │    │   │
│  │  │  │  • Handles mixed numerical + categorical inputs │  │    │   │
│  │  │  │  • Single: d_out = 1                            │  │    │   │
│  │  │  │  • Multi:  d_out = number_of_drugs              │  │    │   │
│  │  │  │  • Learns complex cross-drug resistance         │  │    │   │
│  │  │  │    correlation patterns (MDR)                   │  │    │   │
│  │  │  │  • Higher accuracy on large datasets            │  │    │   │
│  │  │  └─────────────────────────────────────────────────┘  │    │   │
│  │  │                                                       │    │   │
│  │  └───────────────────────────────────────────────────────┘    │   │
│  │                                                               │   │
│  │  ─────────────────────────────────────────────────────────    │   │
│  │                                                               │   │
│  │  SECTION: What You Get (Output Types)                         │   │
│  │  ┌───────────────────────────────────────────────────────┐    │   │
│  │  │                                                       │    │   │
│  │  │  OUTPUT OPTION 1: Per-Drug Prediction                 │    │   │
│  │  │  ┌─────────────────────────────────────────────────┐  │    │   │
│  │  │  │  Drug_A (Amoxicillin)   → S (Sensitive)  92%   │  │    │   │
│  │  │  │  Drug_B (Ciprofloxacin) → R (Resistant)  78%   │  │    │   │
│  │  │  │  Drug_C (Meropenem)     → S (Sensitive)  95%   │  │    │   │
│  │  │  └─────────────────────────────────────────────────┘  │    │   │
│  │  │                                                       │    │   │
│  │  │  OUTPUT OPTION 2: Best Drug Recommendation            │    │   │
│  │  │  ┌─────────────────────────────────────────────────┐  │    │   │
│  │  │  │  Best Drug → Meropenem (95% sensitive)          │  │    │   │
│  │  │  │  Also safe → Amoxicillin (92%)                  │  │    │   │
│  │  │  │  Avoid     → Ciprofloxacin (resistant)          │  │    │   │
│  │  │  └─────────────────────────────────────────────────┘  │    │   │
│  │  │                                                       │    │   │
│  │  │  OUTPUT OPTION 3: Clinical Summary                    │    │   │
│  │  │  ┌─────────────────────────────────────────────────┐  │    │   │
│  │  │  │  "Patient (Male, 65, Hypertensive, Diabetic)    │  │    │   │
│  │  │  │   infected with E. coli.                        │  │    │   │
│  │  │  │   Recommend: Meropenem.                         │  │    │   │
│  │  │  │   Avoid: Ciprofloxacin."                        │  │    │   │
│  │  │  └─────────────────────────────────────────────────┘  │    │   │
│  │  │                                                       │    │   │
│  │  └───────────────────────────────────────────────────────┘    │   │
│  │                                                               │   │
│  │  ─────────────────────────────────────────────────────────    │   │
│  │                                                               │   │
│  │  SECTION: Example Dataset (How the data looks)                │   │
│  │  ┌───────────────────────────────────────────────────────┐    │   │
│  │  │                                                       │    │   │
│  │  │  Each row = one microbe sample + patient info:        │    │   │
│  │  │                                                       │    │   │
│  │  │  ┌─────┬──────┬─────┬─────┬───────┬──────┬──────┐    │    │   │
│  │  │  │ Age │Gender│ HT  │ DM  │Microbe│Drug_A│Drug_B│    │    │   │
│  │  │  ├─────┼──────┼─────┼─────┼───────┼──────┼──────┤    │    │   │
│  │  │  │ 65  │  M   │ Yes │ Yes │ E.coli│  S   │  R   │    │    │   │
│  │  │  │ 32  │  F   │ No  │ No  │ E.coli│  S   │  S   │    │    │   │
│  │  │  │ 48  │  M   │ Yes │ No  │S.aureus│ R   │  R   │    │    │   │
│  │  │  └─────┴──────┴─────┴─────┴───────┴──────┴──────┘    │    │   │
│  │  │                                                       │    │   │
│  │  │  S = Sensitive (drug works)                           │    │   │
│  │  │  R = Resistant (drug fails)                           │    │   │
│  │  │                                                       │    │   │
│  │  └───────────────────────────────────────────────────────┘    │   │
│  │                                                               │   │
│  │  ─────────────────────────────────────────────────────────    │   │
│  │                                                               │   │
│  │  SECTION: Technology Stack                                    │   │
│  │  ┌───────────────────────────────────────────────────────┐    │   │
│  │  │                                                       │    │   │
│  │  │  ┌───────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐  │    │   │
│  │  │  │  Python   │ │  Flask   │ │ sklearn  │ │ PyTorch│  │    │   │
│  │  │  │  Backend  │ │  Web UI  │ │ ML Models│ │ DL/FTT │  │    │   │
│  │  │  └───────────┘ └──────────┘ └──────────┘ └────────┘  │    │   │
│  │  │  ┌───────────┐ ┌──────────┐ ┌──────────┐             │    │   │
│  │  │  │  pandas   │ │  numpy   │ │  rtdl    │             │    │   │
│  │  │  │  Data I/O │ │  Compute │ │  FT-Trans│             │    │   │
│  │  │  └───────────┘ └──────────┘ └──────────┘             │    │   │
│  │  │                                                       │    │   │
│  │  └───────────────────────────────────────────────────────┘    │   │
│  │                                                               │   │
│  │  ─────────────────────────────────────────────────────────    │   │
│  │                                                               │   │
│  │  SECTION: Call to Action (bottom of landing page)             │   │
│  │  ┌───────────────────────────────────────────────────────┐    │   │
│  │  │                                                       │    │   │
│  │  │    Supports multiple drugs per microbe                │    │   │
│  │  │    Uses ML (Random Forest) + DL (FT-Transformer)      │    │   │
│  │  │    Patient-aware predictions (age, gender, HT, DM)    │    │   │
│  │  │    Deployable via Flask web interface                  │    │   │
│  │  │                                                       │    │   │
│  │  │    ┌──────────────────┐  ┌──────────────────────┐     │    │   │
│  │  │    │ Start Prediction │  │   View Past Results  │     │    │   │
│  │  │    │  (go to form)    │  │   (go to history)    │     │    │   │
│  │  │    └──────────────────┘  └──────────────────────┘     │    │   │
│  │  │                                                       │    │   │
│  │  └───────────────────────────────────────────────────────┘    │   │
│  │                                                               │   │
│  │  FOOTER:                                                      │   │
│  │  ┌───────────────────────────────────────────────────────┐    │   │
│  │  │  AMR Prediction System | Multi-Drug Resistance Tool   │    │   │
│  │  │  Built with Python, Flask, scikit-learn, PyTorch      │    │   │
│  │  └───────────────────────────────────────────────────────┘    │   │
│  │                                                               │   │
│  └───────────────────────────────────────────────────────────────┘   │
└──────────────────┬───────────────────────┬──────────────────────────┘
                   │                       │
          Click "Start"            Click "History"
                   │                       │
                   ▼                       ▼
          SCREEN 2: INPUT           SCREEN 6: HISTORY
                   │
                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                  SCREEN 2: INPUT FORM                             │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │  NAVBAR:  [Home]  [Predict]  [History]  [About]           │   │
│  ├───────────────────────────────────────────────────────────┤   │
│  │                                                           │   │
│  │  STEP INDICATOR:                                          │   │
│  │  [1. Patient Info] ──── [2. Microbe Data] ──── [3. Full AMR Report]
│  │    (active)               (next)                (auto-generated)
│  │                                                           │   │
│  │  ═══════════════════════════════════════════════════════   │   │
│  │                                                           │   │
│  │  SECTION A: Patient Information                           │   │
│  │  ┌─────────────────────────────────────────────────────┐  │   │
│  │  │                                                     │  │   │
│  │  │  Age:              [    65    ]                      │  │   │
│  │  │                    └─ slider or number input         │  │   │
│  │  │                                                     │  │   │
│  │  │  Gender:           (o) Male    ( ) Female            │  │   │
│  │  │                                                     │  │   │
│  │  │  Hypertension:     [Toggle ON ████░░ ]              │  │   │
│  │  │                                                     │  │   │
│  │  │  Diabetes:         [Toggle OFF ░░░░██ ]             │  │   │
│  │  │                                                     │  │   │
│  │  └─────────────────────────────────────────────────────┘  │   │
│  │                                                           │   │
│  │                              [ Next → ]                   │   │
│  └───────────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                    Click "Next"
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                  SCREEN 2B: MICROBE INPUT                        │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │                                                           │   │
│  │  STEP INDICATOR:                                          │   │
│  │  [1. Patient Info] ──── [2. Microbe Data] ──── [3. Full AMR Report]
│  │    (done ✓)               (active)              (auto-generated)
│  │                                                           │   │
│  │  ═══════════════════════════════════════════════════════   │   │
│  │                                                           │   │
│  │  SECTION B: Microbe Information                           │   │
│  │  ┌─────────────────────────────────────────────────────┐  │   │
│  │  │                                                     │  │   │
│  │  │  Microbe Type:     [ E. coli              ▼ ]       │  │   │
│  │  │                    ├── E. coli                       │  │   │
│  │  │                    ├── K. pneumoniae                 │  │   │
│  │  │                    ├── S. aureus                     │  │   │
│  │  │                    ├── P. aeruginosa                 │  │   │
│  │  │                    └── A. baumannii                  │  │   │
│  │  │                                                     │  │   │
│  │  │  --- Genomic / Lab Features ---                     │  │   │
│  │  │                                                     │  │   │
│  │  │  Feature 1 (MIC):    [  0.82  ]                     │  │   │
│  │  │  Feature 2 (Zone):   [  1.20  ]                     │  │   │
│  │  │  Feature 3 (Gene):   [  0.45  ]                     │  │   │
│  │  │  Feature N:          [  ....  ]                     │  │   │
│  │  │                                                     │  │   │
│  │  │  [ + Add More Features ]                            │  │   │
│  │  │                                                     │  │   │
│  │  │  ┌─────────────────────────────────────────────┐    │  │   │
│  │  │  │  NOTE: Once you submit, the system will     │    │  │   │
│  │  │  │  automatically test this microbe against    │    │  │   │
│  │  │  │  ALL drugs in the database and generate a   │    │  │   │
│  │  │  │  complete resistance report.                │    │  │   │
│  │  │  └─────────────────────────────────────────────┘    │  │   │
│  │  │                                                     │  │   │
│  │  │  Optional: Filter to single drug instead            │  │   │
│  │  │  [ ] Check to test only one drug:                   │  │   │
│  │  │       [ Amoxicillin          ▼ ]                    │  │   │
│  │  │                                                     │  │   │
│  │  └─────────────────────────────────────────────────────┘  │   │
│  │                                                           │   │
│  │          [ ← Back ]  [ Generate Full AMR Report → ]       │   │
│  └───────────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                    Click "Generate Full AMR Report"
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                  SCREEN 3: LOADING STATE                         │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │                                                           │   │
│  │                                                           │   │
│  │              Analyzing Resistance Patterns...              │   │
│  │                                                           │   │
│  │                   ╭──────────╮                             │   │
│  │                   │  ◠ ◡ ◠   │  ← animated spinner        │   │
│  │                   ╰──────────╯                             │   │
│  │                                                           │   │
│  │              Processing: E. coli sample                    │   │
│  │              Patient: Male, 65, HT+, DM-                  │   │
│  │              Screening ALL drugs in database...            │   │
│  │                                                           │   │
│  │              ████████████░░░░░░░░  60%                     │   │
│  │                                                           │   │
│  └───────────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                    Prediction complete
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│              SCREEN 4A: SINGLE DRUG RESULT (if filtered)         │
│              (shown only when user opted for single drug filter)  │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │                                                           │   │
│  │  STEP INDICATOR:                                          │   │
│  │  [1. Patient Info] ──── [2. Microbe Data] ──── [3. Report]│   │
│  │    (done ✓)               (done ✓)              (result)  │   │
│  │                                                           │   │
│  │  ═══════════════════════════════════════════════════════   │   │
│  │                                                           │   │
│  │  RESULT: Single Drug Prediction                           │   │
│  │  ┌─────────────────────────────────────────────────────┐  │   │
│  │  │                                                     │  │   │
│  │  │  Patient Summary                                    │  │   │
│  │  │  ┌───────────────────────────────────────────────┐  │  │   │
│  │  │  │ Age: 65 | Gender: Male | HT: Yes | DM: No   │  │  │   │
│  │  │  │ Microbe: E. coli                              │  │  │   │
│  │  │  └───────────────────────────────────────────────┘  │  │   │
│  │  │                                                     │  │   │
│  │  │  Drug Tested: Amoxicillin                           │  │   │
│  │  │                                                     │  │   │
│  │  │  ┌─────────────────────────────────────────┐        │  │   │
│  │  │  │                                         │        │  │   │
│  │  │  │       ██████████████████████             │        │  │   │
│  │  │  │       █   RESISTANT (R)    █             │        │  │   │
│  │  │  │       █   Confidence: 87%  █             │        │  │   │
│  │  │  │       ██████████████████████             │        │  │   │
│  │  │  │       (red colored badge)               │        │  │   │
│  │  │  │                                         │        │  │   │
│  │  │  │  Confidence Bar:                        │        │  │   │
│  │  │  │  ████████████████████░░░░  87%          │        │  │   │
│  │  │  │                                         │        │  │   │
│  │  │  └─────────────────────────────────────────┘        │  │   │
│  │  │                                                     │  │   │
│  │  │  Note: This microbe shows resistance to             │  │   │
│  │  │  Amoxicillin. Consider alternative antibiotics.     │  │   │
│  │  │                                                     │  │   │
│  │  │  [ See Full Report for ALL Drugs → ]                │  │   │
│  │  │                                                     │  │   │
│  │  └─────────────────────────────────────────────────────┘  │   │
│  │                                                           │   │
│  │  [ ← New Prediction ]  [ Full Report ]  [ Download ]     │   │
│  │                                                           │   │
│  └───────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│              SCREEN 4B: FULL AMR REPORT (DEFAULT)                │
│              (auto-generated for ALL drugs against the microbe)  │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │                                                           │   │
│  │  STEP INDICATOR:                                          │   │
│  │  [1. Patient Info] ──── [2. Microbe Data] ──── [3. Report]│   │
│  │    (done ✓)               (done ✓)              (result)  │   │
│  │                                                           │   │
│  │  ═══════════════════════════════════════════════════════   │   │
│  │                                                           │   │
│  │  RESULT: Full AMR Report — ALL Drugs Screened             │   │
│  │  ┌─────────────────────────────────────────────────────┐  │   │
│  │  │                                                     │  │   │
│  │  │  Patient Summary                                    │  │   │
│  │  │  ┌───────────────────────────────────────────────┐  │  │   │
│  │  │  │ Age: 65 | Gender: Male | HT: Yes | DM: No   │  │  │   │
│  │  │  │ Microbe: E. coli                              │  │  │   │
│  │  │  └───────────────────────────────────────────────┘  │  │   │
│  │  │                                                     │  │   │
│  │  │  Drug-wise Results (ALL drugs auto-screened):        │  │   │
│  │  │  ┌───────────────┬──────────┬────────┬──────────┐   │  │   │
│  │  │  │ Drug          │ Result   │ Conf.  │ Status   │   │  │   │
│  │  │  ├───────────────┼──────────┼────────┼──────────┤   │  │   │
│  │  │  │ Amoxicillin   │   S      │  92%   │ [green]  │   │  │   │
│  │  │  │ Ciprofloxacin │   R      │  78%   │ [red]    │   │  │   │
│  │  │  │ Gentamicin    │   S      │  88%   │ [green]  │   │  │   │
│  │  │  │ Meropenem     │   S      │  95%   │ [green]  │   │  │   │
│  │  │  │ Tetracycline  │   R      │  81%   │ [red]    │   │  │   │
│  │  │  │ Trimethoprim  │   R      │  84%   │ [red]    │   │  │   │
│  │  │  │ ... (every drug in DB)                       │   │  │   │
│  │  │  └───────────────┴──────────┴────────┴──────────┘   │  │   │
│  │  │                                                     │  │   │
│  │  │  ┌─────────────────────────────────────────────┐    │  │   │
│  │  │  │  BEST DRUG RECOMMENDATION                   │    │  │   │
│  │  │  │  ─────────────────────────                  │    │  │   │
│  │  │  │                                             │    │  │   │
│  │  │  │  ★ Meropenem (95% confidence - Sensitive)   │    │  │   │
│  │  │  │    Also consider: Amoxicillin (92%)         │    │  │   │
│  │  │  │                                             │    │  │   │
│  │  │  │  Avoid:                                     │    │  │   │
│  │  │  │  ✗ Trimethoprim (84% Resistant)             │    │  │   │
│  │  │  │  ✗ Ciprofloxacin (78% Resistant)            │    │  │   │
│  │  │  └─────────────────────────────────────────────┘    │  │   │
│  │  │                                                     │  │   │
│  │  │  ┌─────────────────────────────────────────────┐    │  │   │
│  │  │  │  VISUAL: Resistance Bar Chart               │    │  │   │
│  │  │  │                                             │    │  │   │
│  │  │  │  Meropenem     █░░░░░░░░░░░░░  5% (S)      │    │  │   │
│  │  │  │  Amoxicillin   ██░░░░░░░░░░░░  8% (S)      │    │  │   │
│  │  │  │  Gentamicin    ██░░░░░░░░░░░░ 12% (S)      │    │  │   │
│  │  │  │  Ciprofloxacin ██████████░░░░  78% (R)      │    │  │   │
│  │  │  │  Tetracycline  ██████████░░░░  81% (R)      │    │  │   │
│  │  │  │  Trimethoprim  ███████████░░░  84% (R)      │    │  │   │
│  │  │  │  (sorted: least → most resistant)           │    │  │   │
│  │  │  │                                             │    │  │   │
│  │  │  │  ← Less Resistant    More Resistant →       │    │  │   │
│  │  │  └─────────────────────────────────────────────┘    │  │   │
│  │  │                                                     │  │   │
│  │  │  ┌─────────────────────────────────────────────┐    │  │   │
│  │  │  │  CLINICAL SUMMARY (auto-generated)           │    │  │   │
│  │  │  │  ─────────────────────────────────           │    │  │   │
│  │  │  │  "Patient (Male, 65, Hypertensive)           │    │  │   │
│  │  │  │   infected with E. coli.                     │    │  │   │
│  │  │  │                                              │    │  │   │
│  │  │  │   SUSCEPTIBLE (safe to use):                 │    │  │   │
│  │  │  │   - Meropenem (95%), Amoxicillin (92%),      │    │  │   │
│  │  │  │     Gentamicin (88%)                         │    │  │   │
│  │  │  │                                              │    │  │   │
│  │  │  │   RESISTANT (avoid):                         │    │  │   │
│  │  │  │   - Trimethoprim (84%), Tetracycline (81%),  │    │  │   │
│  │  │  │     Ciprofloxacin (78%)                      │    │  │   │
│  │  │  │                                              │    │  │   │
│  │  │  │   RECOMMENDATION: Meropenem (best match)"    │    │  │   │
│  │  │  └─────────────────────────────────────────────┘    │  │   │
│  │  │                                                     │  │   │
│  │  └─────────────────────────────────────────────────────┘  │   │
│  │                                                           │   │
│  │  [ ← New Prediction ]  [ Download PDF ]  [ Save to History ] │
│  │                                                           │   │
│  └───────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## UI Screen Navigation Map

```
                        ┌──────────────┐
                        │   LANDING    │
                        │    PAGE      │
                        │ (full info)  │
                        └──────┬───────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
                ▼              ▼              ▼
          ┌──────────┐  ┌──────────┐  ┌──────────┐
          │ PREDICT  │  │ HISTORY  │  │  ABOUT   │
          │  (form)  │  │  (logs)  │  │  (info)  │
          └────┬─────┘  └──────────┘  └──────────┘
               │
    ┌──────────┴──────────┐
    │                     │
    ▼                     ▼
┌──────────┐       ┌───────────┐
│ STEP 1:  │       │  STEP 2:  │
│ PATIENT  │──────►│  MICROBE  │
│ INFO     │       │  DATA     │
└──────────┘       └─────┬─────┘
                         │
              Click "Generate Full AMR Report"
                         │
                         ▼
                   ┌──────────┐
                   │ LOADING  │
                   │  STATE   │
                   └────┬─────┘
                        │
               ┌────────┴────────┐
               │                 │
               ▼                 ▼
    ┌────────────────┐  ┌────────────────┐
    │ FULL AMR       │  │ SINGLE DRUG   │
    │ REPORT         │  │ RESULT        │
    │ (DEFAULT)      │  │ (if filtered) │
    │                │  │               │
    │ ALL drugs S/R  │  │ 1 drug S/R    │
    │ + best drug    │  │ + link to     │
    │ + avoid list   │  │   full report │
    │ + clinical sum │  │               │
    └───────┬────────┘  └──────┬────────┘
            │                  │
            └────────┬─────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
  ┌──────────┐ ┌──────────┐ ┌──────────┐
  │   NEW    │ │ DOWNLOAD │ │  SAVE TO │
  │ PREDICT  │ │   PDF    │ │ HISTORY  │
  └──────────┘ └──────────┘ └──────────┘
```

---

## Design System — shadcn/ui Inspired

```
┌──────────────────────────────────────────────────────────────────┐
│                    DESIGN PHILOSOPHY                               │
│                                                                   │
│  Reference: shadcn/ui + Radix UI + Tailwind CSS                   │
│                                                                   │
│  Principles:                                                      │
│  • Minimal, clean, no visual clutter                              │
│  • Subtle borders, not heavy boxes                                │
│  • Generous whitespace — let content breathe                      │
│  • Dark mode by default, light mode toggle                        │
│  • Micro-interactions: hover states, focus rings, transitions     │
│  • Typography-driven hierarchy, not color-driven                  │
│  • Cards with subtle shadows, rounded-lg corners                  │
│  • Muted backgrounds, high-contrast text                          │
│                                                                   │
│  NOT Bootstrap. NOT Material UI. NOT generic HTML.                │
│  Think: Linear, Vercel Dashboard, Stripe Dashboard.               │
└──────────────────────────────────────────────────────────────────┘
```

---

## Tech Stack for UI (shadcn-quality)

```
┌──────────────────────────────────────────────────────────────────┐
│                    FRONTEND STACK                                  │
│                                                                   │
│  Framework:     Next.js 14+ (App Router) OR React + Vite          │
│  Styling:       Tailwind CSS v4                                   │
│  Components:    shadcn/ui (built on Radix UI primitives)          │
│  Icons:         Lucide React                                      │
│  Charts:        Recharts (shadcn/ui chart wrappers)               │
│  Animations:    Framer Motion (page transitions, micro-anims)     │
│  Dark Mode:     next-themes (class-based toggle)                  │
│  Forms:         React Hook Form + Zod validation                  │
│  Tables:        @tanstack/react-table (shadcn DataTable)          │
│  Toasts:        sonner (shadcn toast)                             │
│  State:         Zustand or React Context                          │
│                                                                   │
│  Backend API:   Flask (Python) → REST endpoints                   │
│  Frontend calls Flask API via fetch / axios                       │
└──────────────────────────────────────────────────────────────────┘
```

---

## Color System (shadcn/ui tokens)

```
┌──────────────────────────────────────────────────────────────────┐
│                    COLOR TOKENS                                    │
│                                                                   │
│  Base (Dark Mode Default):                                        │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │  --background:     hsl(0 0% 3.9%)      ← near black       │   │
│  │  --foreground:     hsl(0 0% 98%)       ← near white text  │   │
│  │  --card:           hsl(0 0% 3.9%)      ← card bg          │   │
│  │  --card-foreground:hsl(0 0% 98%)       ← card text        │   │
│  │  --muted:          hsl(0 0% 14.9%)     ← subtle bg        │   │
│  │  --muted-foreground:hsl(0 0% 63.9%)    ← secondary text   │   │
│  │  --border:         hsl(0 0% 14.9%)     ← subtle lines     │   │
│  │  --ring:           hsl(0 0% 83.1%)     ← focus rings      │   │
│  └────────────────────────────────────────────────────────────┘   │
│                                                                   │
│  Base (Light Mode):                                               │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │  --background:     hsl(0 0% 100%)      ← white            │   │
│  │  --foreground:     hsl(0 0% 3.9%)      ← near black text  │   │
│  │  --card:           hsl(0 0% 100%)      ← white cards      │   │
│  │  --muted:          hsl(0 0% 96.1%)     ← light grey bg    │   │
│  │  --border:         hsl(0 0% 89.8%)     ← light borders    │   │
│  └────────────────────────────────────────────────────────────┘   │
│                                                                   │
│  AMR-Specific Semantic Colors:                                    │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │                                                            │   │
│  │  SENSITIVE (S):                                            │   │
│  │    --sensitive:     hsl(142 76% 36%)    ← emerald-600      │   │
│  │    --sensitive-bg:  hsl(142 76% 36% / 0.1)  ← subtle bg   │   │
│  │    Badge: text-emerald-500 bg-emerald-500/10               │   │
│  │    border-emerald-500/20 rounded-full px-2.5 py-0.5       │   │
│  │    Display: "Susceptible" with dot indicator               │   │
│  │                                                            │   │
│  │  RESISTANT (R):                                            │   │
│  │    --resistant:     hsl(0 84% 60%)      ← red-500         │   │
│  │    --resistant-bg:  hsl(0 84% 60% / 0.1)    ← subtle bg   │   │
│  │    Badge: text-red-500 bg-red-500/10                       │   │
│  │    border-red-500/20 rounded-full px-2.5 py-0.5           │   │
│  │    Display: "Resistant" with dot indicator                 │   │
│  │                                                            │   │
│  │  BEST DRUG:                                                │   │
│  │    --best:          hsl(47 96% 53%)     ← amber-400       │   │
│  │    Badge: text-amber-400 bg-amber-400/10                   │   │
│  │    border-amber-400/20 with star icon                      │   │
│  │                                                            │   │
│  │  WARNING (Low Confidence):                                 │   │
│  │    --warning:       hsl(25 95% 53%)     ← orange-500      │   │
│  │    Badge: text-orange-500 bg-orange-500/10                 │   │
│  │                                                            │   │
│  │  UNCERTAIN:                                                │   │
│  │    text-muted-foreground bg-muted                          │   │
│  │    with disclaimer tooltip                                 │   │
│  │                                                            │   │
│  └────────────────────────────────────────────────────────────┘   │
│                                                                   │
│  Confidence Thresholds:                                           │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │  90-100%  → emerald badge, solid progress bar              │   │
│  │  70-89%   → emerald/red badge (based on S/R), normal bar  │   │
│  │  50-69%   → orange warning badge + tooltip explanation     │   │
│  │  < 50%    → muted grey badge + "Low confidence" disclaimer │   │
│  └────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

---

## Typography System

```
┌──────────────────────────────────────────────────────────────────┐
│                    TYPOGRAPHY                                      │
│                                                                   │
│  Font:  Inter (or Geist Sans — used by Vercel/shadcn)             │
│  Mono:  JetBrains Mono (for data values, percentages)             │
│                                                                   │
│  Scale (Tailwind classes):                                        │
│  ┌──────────────────────────────────────────────────────────┐     │
│  │  Hero heading:    text-4xl font-bold tracking-tight      │     │
│  │  Page heading:    text-3xl font-semibold tracking-tight  │     │
│  │  Section heading: text-xl font-semibold                  │     │
│  │  Card title:      text-lg font-medium                    │     │
│  │  Body:            text-sm text-muted-foreground          │     │
│  │  Label:           text-sm font-medium                    │     │
│  │  Data value:      text-2xl font-mono font-bold           │     │
│  │  Badge:           text-xs font-medium                    │     │
│  │  Caption:         text-xs text-muted-foreground          │     │
│  └──────────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────────┘
```

---

## shadcn/ui Component Mapping

```
┌──────────────────────────────────────────────────────────────────┐
│               COMPONENT TREE (shadcn/ui)                          │
│                                                                   │
│  App (next-themes ThemeProvider)                                   │
│  ├── Layout                                                       │
│  │   ├── Navbar (sticky, border-b, backdrop-blur)                 │
│  │   │   ├── Logo (font-bold tracking-tight)                      │
│  │   │   ├── NavigationMenu (shadcn)                              │
│  │   │   │   ├── NavigationMenuItem → /                           │
│  │   │   │   ├── NavigationMenuItem → /predict                    │
│  │   │   │   ├── NavigationMenuItem → /history                    │
│  │   │   │   └── NavigationMenuItem → /about                      │
│  │   │   ├── ThemeToggle (Sun/Moon icon Button)                   │
│  │   │   └── MobileSheet (Sheet + hamburger for mobile)           │
│  │   │                                                            │
│  │   └── main (max-w-6xl mx-auto px-4)                            │
│  │                                                                │
│  ├── LandingPage (/)                                              │
│  │   ├── HeroSection (gradient text, large heading)               │
│  │   │   ├── Badge ("ML + DL Powered")                            │
│  │   │   ├── h1 (text-4xl gradient)                               │
│  │   │   ├── p (text-muted-foreground max-w-2xl)                  │
│  │   │   └── ButtonGroup                                          │
│  │   │       ├── Button (variant="default") → /predict            │
│  │   │       └── Button (variant="outline") → /history            │
│  │   │                                                            │
│  │   ├── HowItWorksSection                                       │
│  │   │   └── 3x Card (shadcn) in grid                            │
│  │   │       ├── Card: Step 1 — Patient Info (icon + desc)        │
│  │   │       ├── Card: Step 2 — Microbe Data (icon + desc)        │
│  │   │       └── Card: Step 3 — Full AMR Report (icon + desc)     │
│  │   │                                                            │
│  │   ├── PredictionModesSection                                   │
│  │   │   ├── Card: Full Report (default, highlighted border)      │
│  │   │   └── Card: Single Drug (muted, optional)                  │
│  │   │                                                            │
│  │   ├── InputFeaturesSection                                     │
│  │   │   ├── Card: Patient features (icons per feature)           │
│  │   │   └── Card: Microbe features                               │
│  │   │                                                            │
│  │   ├── ModelsSection                                            │
│  │   │   ├── Card: Random Forest (with Badge "ML")                │
│  │   │   └── Card: FT-Transformer (with Badge "DL")              │
│  │   │                                                            │
│  │   ├── OutputSection                                            │
│  │   │   └── Tabs (shadcn)                                        │
│  │   │       ├── TabsTrigger: "Per-Drug"                          │
│  │   │       ├── TabsTrigger: "Best Drug"                         │
│  │   │       └── TabsTrigger: "Clinical Summary"                  │
│  │   │                                                            │
│  │   ├── DatasetPreviewSection                                    │
│  │   │   └── DataTable (shadcn, @tanstack/react-table)            │
│  │   │                                                            │
│  │   ├── TechStackSection                                         │
│  │   │   └── Grid of Badge components (Python, Flask, etc.)       │
│  │   │                                                            │
│  │   └── CTASection                                               │
│  │       ├── Button (primary) → /predict                          │
│  │       └── Button (outline) → /history                          │
│  │                                                                │
│  ├── PredictPage (/predict)                                       │
│  │   ├── StepIndicator (custom, animated connecting lines)        │
│  │   │   ├── Step 1: Patient Info (Circle + Label)                │
│  │   │   ├── Step 2: Microbe Data (Circle + Label)                │
│  │   │   └── Step 3: Full AMR Report (Circle + Label)             │
│  │   │                                                            │
│  │   ├── Step1: PatientInfoCard (shadcn Card)                     │
│  │   │   ├── CardHeader ("Patient Information")                   │
│  │   │   ├── CardContent                                          │
│  │   │   │   ├── Input (shadcn) → Age (type="number")            │
│  │   │   │   ├── RadioGroup (shadcn) → Gender (M/F)              │
│  │   │   │   ├── Switch (shadcn) → Hypertension                  │
│  │   │   │   └── Switch (shadcn) → Diabetes                      │
│  │   │   └── CardFooter                                           │
│  │   │       └── Button "Continue" (variant="default")            │
│  │   │                                                            │
│  │   ├── Step2: MicrobeDataCard (shadcn Card)                     │
│  │   │   ├── CardHeader ("Microbe Information")                   │
│  │   │   ├── CardContent                                          │
│  │   │   │   ├── Select (shadcn Combobox) → Microbe type          │
│  │   │   │   │   with search/filter (Popover + Command)           │
│  │   │   │   ├── InputGroup → Genomic features                    │
│  │   │   │   │   ├── Input (Label: "MIC Value")                   │
│  │   │   │   │   ├── Input (Label: "Zone Diameter")               │
│  │   │   │   │   └── Button (variant="ghost") "+ Add Feature"     │
│  │   │   │   ├── Separator (shadcn)                               │
│  │   │   │   ├── Checkbox (shadcn) "Filter to single drug"       │
│  │   │   │   └── Select → Drug dropdown (if checked)              │
│  │   │   └── CardFooter                                           │
│  │   │       ├── Button "Back" (variant="outline")                │
│  │   │       └── Button "Generate Report" (variant="default")     │
│  │   │                                                            │
│  │   └── LoadingState (AnimatePresence + Framer Motion)           │
│  │       ├── Skeleton loaders (shadcn Skeleton)                   │
│  │       ├── Progress bar (shadcn Progress, animated)             │
│  │       └── Muted status text                                    │
│  │                                                                │
│  ├── ResultPage (/result)                                         │
│  │   ├── PatientSummaryCard (shadcn Card, muted bg)               │
│  │   │   └── Grid: Age | Gender | HT | DM | Microbe (Badges)     │
│  │   │                                                            │
│  │   ├── FullReportView (default)                                 │
│  │   │   ├── BestDrugCard (Card with amber-400 border-l-4)       │
│  │   │   │   ├── Star icon + Drug name + Confidence               │
│  │   │   │   └── "Also consider:" secondary recommendations      │
│  │   │   │                                                        │
│  │   │   ├── AvoidCard (Card with red-500 border-l-4)            │
│  │   │   │   └── List of resistant drugs with X icons             │
│  │   │   │                                                        │
│  │   │   ├── DataTable (shadcn, sortable columns)                 │
│  │   │   │   ├── Column: Drug Name                                │
│  │   │   │   ├── Column: Result (Badge — S green / R red)         │
│  │   │   │   ├── Column: Confidence (Progress bar + %)            │
│  │   │   │   └── Column: Status (dot indicator)                   │
│  │   │   │                                                        │
│  │   │   ├── ResistanceChart (Recharts BarChart, horizontal)      │
│  │   │   │   └── Sorted bars: green (S) → red (R)                │
│  │   │   │                                                        │
│  │   │   └── ClinicalSummaryCard (Card, prose formatting)         │
│  │   │       └── Alert (shadcn) with clinical recommendation      │
│  │   │                                                            │
│  │   ├── SingleDrugView (if filtered)                             │
│  │   │   ├── Large Badge (S or R, centered)                       │
│  │   │   ├── Confidence ring (radial progress)                    │
│  │   │   └── Button → "See Full Report"                           │
│  │   │                                                            │
│  │   └── ActionBar (sticky bottom or card footer)                 │
│  │       ├── Button "New Prediction" (variant="outline")          │
│  │       ├── Button "Download PDF" (variant="outline", icon)      │
│  │       └── Button "Save to History" (variant="default")         │
│  │                                                                │
│  ├── HistoryPage (/history)                                       │
│  │   ├── PageHeader ("Prediction History")                        │
│  │   ├── FilterBar                                                │
│  │   │   ├── Input (search icon) → search                         │
│  │   │   ├── DateRangePicker (shadcn Calendar + Popover)          │
│  │   │   └── Select → filter by result type                       │
│  │   ├── DataTable (shadcn, @tanstack/react-table)                │
│  │   │   ├── Column: # (row number)                               │
│  │   │   ├── Column: Date                                         │
│  │   │   ├── Column: Patient (badges for conditions)              │
│  │   │   ├── Column: Microbe                                      │
│  │   │   ├── Column: Drugs Screened (count badge)                 │
│  │   │   ├── Column: Best Drug (amber badge)                      │
│  │   │   └── Column: Actions (Button → View)                      │
│  │   ├── Pagination (shadcn)                                      │
│  │   └── ExportDropdown (DropdownMenu → CSV, PDF)                 │
│  │                                                                │
│  └── Footer (border-t, muted text, centered)                      │
└──────────────────────────────────────────────────────────────────┘
```

---

## shadcn/ui Component Catalog (what to install)

```
┌──────────────────────────────────────────────────────────────────┐
│              SHADCN COMPONENTS TO INSTALL                          │
│                                                                   │
│  npx shadcn@latest init                                           │
│                                                                   │
│  Core:                                                            │
│  npx shadcn@latest add button card input label badge              │
│  npx shadcn@latest add select switch radio-group checkbox         │
│  npx shadcn@latest add separator tabs alert progress              │
│  npx shadcn@latest add skeleton tooltip popover                   │
│                                                                   │
│  Navigation:                                                      │
│  npx shadcn@latest add navigation-menu sheet                      │
│  npx shadcn@latest add dropdown-menu command                      │
│                                                                   │
│  Data:                                                            │
│  npx shadcn@latest add table data-table                           │
│  npx shadcn@latest add chart (Recharts wrapper)                   │
│  npx shadcn@latest add calendar                                   │
│                                                                   │
│  Feedback:                                                        │
│  npx shadcn@latest add sonner (toast)                             │
│  npx shadcn@latest add dialog                                     │
│                                                                   │
│  Additional:                                                      │
│  npm install framer-motion lucide-react next-themes               │
│  npm install @tanstack/react-table recharts                       │
│  npm install react-hook-form @hookform/resolvers zod              │
└──────────────────────────────────────────────────────────────────┘
```

---

## Detailed Screen Wireframes (shadcn style)

### Landing Page — Hero Section

```
┌──────────────────────────────────────────────────────────────────┐
│ DARK MODE (default)                                 [Sun icon]   │
│                                                                  │
│ ┌────────────────────────────────────────────────────────────┐   │
│ │ bg-background border-b border-border backdrop-blur-md      │   │
│ │                                                            │   │
│ │  AMR Predict    Home   Predict   History   About    [🌙]   │   │
│ │  ──────────     ────   ───────   ───────   ─────          │   │
│ │  (font-bold)    (text-muted-foreground, hover:text-fg)    │   │
│ └────────────────────────────────────────────────────────────┘   │
│                                                                  │
│              ┌─────────────────────────────────┐                 │
│              │ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │                 │
│              │ ░  badge: "ML + DL Powered"   ░ │                 │
│              │ ░  (text-xs border rounded-full)░ │                │
│              │ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │                 │
│              │                                 │                 │
│              │  Multi-Drug AMR                 │                 │
│              │  Prediction System              │                 │
│              │  ─────────────────              │                 │
│              │  (text-4xl font-bold             │                 │
│              │   tracking-tight                 │                 │
│              │   bg-gradient-to-r               │                 │
│              │   from-white to-zinc-400         │                 │
│              │   bg-clip-text                   │                 │
│              │   text-transparent)              │                 │
│              │                                 │                 │
│              │  Predict antibiotic resistance  │                 │
│              │  for every drug against a       │                 │
│              │  microbe — powered by ML & DL.  │                 │
│              │  (text-muted-foreground          │                 │
│              │   text-lg max-w-2xl mx-auto)     │                 │
│              │                                 │                 │
│              │  ┌──────────────┐ ┌───────────┐ │                 │
│              │  │▓▓ Start     ▓▓│ │ History   │ │                 │
│              │  │▓▓ Prediction▓▓│ │ (outline) │ │                 │
│              │  │▓▓ (primary) ▓▓│ │ (ghost    │ │                 │
│              │  │▓▓           ▓▓│ │  border)  │ │                 │
│              │  └──────────────┘ └───────────┘ │                 │
│              │                                 │                 │
│              └─────────────────────────────────┘                 │
│                       (text-center)                              │
│                                                                  │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  │
│  (Separator — subtle border-b)                                   │
└──────────────────────────────────────────────────────────────────┘
```

### Landing Page — How It Works Cards

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                   │
│  How It Works                                                     │
│  (text-2xl font-semibold tracking-tight)                          │
│                                                                   │
│  ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐  │
│  │ Card (shadcn)    │ │ Card (shadcn)    │ │ Card (shadcn)    │  │
│  │ border-border    │ │ border-border    │ │ border-border    │  │
│  │ bg-card          │ │ bg-card          │ │ bg-card          │  │
│  │ rounded-xl       │ │ rounded-xl       │ │ rounded-xl       │  │
│  │ hover:border-    │ │ hover:border-    │ │ hover:border-    │  │
│  │  ring/50         │ │  ring/50         │ │  ring/50         │  │
│  │ transition-all   │ │ transition-all   │ │ transition-all   │  │
│  │                  │ │                  │ │                  │  │
│  │  ┌────┐          │ │  ┌────┐          │ │  ┌────┐          │  │
│  │  │ 01 │          │ │  │ 02 │          │ │  │ 03 │          │  │
│  │  └────┘          │ │  └────┘          │ │  └────┘          │  │
│  │  (text-4xl       │ │  (text-4xl       │ │  (text-4xl       │  │
│  │   font-bold      │ │   font-bold      │ │   font-bold      │  │
│  │   text-muted)    │ │   text-muted)    │ │   text-muted)    │  │
│  │                  │ │                  │ │                  │  │
│  │  [User icon]     │ │  [Bug icon]      │ │  [FileText icon] │  │
│  │                  │ │                  │ │                  │  │
│  │  Patient Info    │ │  Microbe Data    │ │  Full AMR Report │  │
│  │  (font-medium)   │ │  (font-medium)   │ │  (font-medium)   │  │
│  │                  │ │                  │ │                  │  │
│  │  Enter age,      │ │  Select microbe  │ │  Auto-generated  │  │
│  │  gender, HT,     │ │  type & genomic  │ │  S/R for ALL     │  │
│  │  diabetes.       │ │  lab features.   │ │  drugs + best    │  │
│  │  (text-sm        │ │  (text-sm        │ │  recommendation. │  │
│  │   text-muted-fg) │ │   text-muted-fg) │ │  (text-sm        │  │
│  │                  │ │                  │ │   text-muted-fg) │  │
│  └──────────────────┘ └──────────────────┘ └──────────────────┘  │
│       (grid grid-cols-3 gap-6)                                    │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

### Predict Page — Patient Form (shadcn Card)

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                   │
│  Step Indicator (custom):                                         │
│  ┌──────────────────────────────────────────────────────────┐     │
│  │                                                          │     │
│  │   (●)─────────────( )─────────────( )                    │     │
│  │    1                2               3                    │     │
│  │  Patient          Microbe        Report                  │     │
│  │  (text-xs)        (text-xs        (text-xs               │     │
│  │  (text-fg)         text-muted)     text-muted)           │     │
│  │                                                          │     │
│  │  ● = bg-primary rounded-full w-8 h-8                     │     │
│  │  ○ = border-muted rounded-full w-8 h-8                   │     │
│  │  line = h-[2px] bg-muted (animated fill on progress)     │     │
│  │                                                          │     │
│  └──────────────────────────────────────────────────────────┘     │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐     │
│  │ Card (max-w-2xl mx-auto)                                 │     │
│  │ rounded-xl border-border bg-card shadow-sm               │     │
│  │                                                          │     │
│  │ ┌────────────────────────────────────────────────────┐   │     │
│  │ │ CardHeader                                         │   │     │
│  │ │  Patient Information                               │   │     │
│  │ │  (text-xl font-semibold)                           │   │     │
│  │ │  Enter the patient's clinical details.             │   │     │
│  │ │  (text-sm text-muted-foreground)                   │   │     │
│  │ └────────────────────────────────────────────────────┘   │     │
│  │                                                          │     │
│  │ ┌────────────────────────────────────────────────────┐   │     │
│  │ │ CardContent (space-y-6)                            │   │     │
│  │ │                                                    │   │     │
│  │ │  Age                                               │   │     │
│  │ │  (Label — text-sm font-medium)                     │   │     │
│  │ │  ┌────────────────────────────────────────┐        │   │     │
│  │ │  │ 65                                     │        │   │     │
│  │ │  └────────────────────────────────────────┘        │   │     │
│  │ │  (Input — h-10 rounded-md border-border            │   │     │
│  │ │   bg-background px-3 text-sm                       │   │     │
│  │ │   focus:ring-2 focus:ring-ring)                    │   │     │
│  │ │                                                    │   │     │
│  │ │  Gender                                            │   │     │
│  │ │  (Label)                                           │   │     │
│  │ │  ┌─────────────────┐ ┌──────────────────┐          │   │     │
│  │ │  │ (●) Male        │ │ ( ) Female       │          │   │     │
│  │ │  └─────────────────┘ └──────────────────┘          │   │     │
│  │ │  (RadioGroup — flex gap-4, RadioGroupItem           │   │     │
│  │ │   border-primary, checked:bg-primary)              │   │     │
│  │ │                                                    │   │     │
│  │ │  ┌─────────────────────────────────────┐           │   │     │
│  │ │  │ Hypertension           [━━━━●░░░]   │           │   │     │
│  │ │  │ (Label)                (Switch ON)   │           │   │     │
│  │ │  │                        bg-primary    │           │   │     │
│  │ │  └─────────────────────────────────────┘           │   │     │
│  │ │  (flex items-center justify-between)               │   │     │
│  │ │                                                    │   │     │
│  │ │  ┌─────────────────────────────────────┐           │   │     │
│  │ │  │ Diabetes               [░░░░░●━━━]  │           │   │     │
│  │ │  │ (Label)                (Switch OFF)  │           │   │     │
│  │ │  │                        bg-muted      │           │   │     │
│  │ │  └─────────────────────────────────────┘           │   │     │
│  │ │                                                    │   │     │
│  │ └────────────────────────────────────────────────────┘   │     │
│  │                                                          │     │
│  │ ┌────────────────────────────────────────────────────┐   │     │
│  │ │ CardFooter (flex justify-end)                      │   │     │
│  │ │                                                    │   │     │
│  │ │                            ┌──────────────────┐    │   │     │
│  │ │                            │ Continue →       │    │   │     │
│  │ │                            │ (Button default) │    │   │     │
│  │ │                            │ bg-primary       │    │   │     │
│  │ │                            │ text-primary-fg  │    │   │     │
│  │ │                            │ rounded-md h-10  │    │   │     │
│  │ │                            └──────────────────┘    │   │     │
│  │ └────────────────────────────────────────────────────┘   │     │
│  │                                                          │     │
│  └──────────────────────────────────────────────────────────┘     │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

### Result Page — Full AMR Report (shadcn Cards + DataTable)

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐     │
│  │ Patient Summary (Card — bg-muted/50 border-border)       │     │
│  │ rounded-xl p-4                                           │     │
│  │                                                          │     │
│  │  ┌──────┐ ┌──────┐ ┌─────────────┐ ┌──────────┐ ┌─────┐│     │
│  │  │Age:65│ │Male  │ │Hypertension │ │Diabetes: │ │E.coli│     │
│  │  │Badge │ │Badge │ │   Yes       │ │   No     │ │Badge ││     │
│  │  │muted │ │muted │ │  Badge red  │ │Badge grey│ │accent││     │
│  │  └──────┘ └──────┘ └─────────────┘ └──────────┘ └─────┘│     │
│  └──────────────────────────────────────────────────────────┘     │
│                                                                   │
│  ┌─────────────────────────────┐ ┌────────────────────────────┐  │
│  │ Card (border-l-4            │ │ Card (border-l-4           │  │
│  │  border-l-amber-400)       │ │  border-l-red-500)         │  │
│  │                             │ │                            │  │
│  │  ★ Best Drug                │ │  ✗ Avoid                   │  │
│  │  (text-amber-400)           │ │  (text-red-500)            │  │
│  │                             │ │                            │  │
│  │  Meropenem                  │ │  Trimethoprim (84%)        │  │
│  │  (text-2xl font-bold)       │ │  Tetracycline (81%)        │  │
│  │  95% confidence             │ │  Ciprofloxacin (78%)       │  │
│  │  (text-muted-foreground)    │ │  (text-sm text-muted-fg)   │  │
│  │                             │ │                            │  │
│  │  Also: Amoxicillin (92%),   │ │                            │  │
│  │  Gentamicin (88%)           │ │                            │  │
│  │  (text-sm text-muted-fg)    │ │                            │  │
│  └─────────────────────────────┘ └────────────────────────────┘  │
│       (grid grid-cols-2 gap-4)                                    │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐     │
│  │ DataTable (shadcn — @tanstack/react-table)               │     │
│  │ rounded-xl border-border                                 │     │
│  │                                                          │     │
│  │ ┌──────────────┬──────────┬──────────────┬────────────┐  │     │
│  │ │ Drug ↕       │ Result ↕ │ Confidence ↕ │ Status     │  │     │
│  │ │ (sortable)   │(sortable)│ (sortable)   │            │  │     │
│  │ ├──────────────┼──────────┼──────────────┼────────────┤  │     │
│  │ │              │ ┌──────┐ │              │            │  │     │
│  │ │ Meropenem    │ │● S   │ │ ██████████░ 95%│ ● green │  │     │
│  │ │              │ │green │ │              │            │  │     │
│  │ │              │ │badge │ │ (Progress    │            │  │     │
│  │ │              │ └──────┘ │  component)  │            │  │     │
│  │ ├──────────────┼──────────┼──────────────┼────────────┤  │     │
│  │ │ Amoxicillin  │ │● S   │ │ █████████░░ 92%│ ● green │  │     │
│  │ ├──────────────┼──────────┼──────────────┼────────────┤  │     │
│  │ │ Gentamicin   │ │● S   │ │ ████████░░░ 88%│ ● green │  │     │
│  │ ├──────────────┼──────────┼──────────────┼────────────┤  │     │
│  │ │ Trimethoprim │ │● R   │ │ ████████░░░ 84%│ ● red   │  │     │
│  │ │              │ │red   │ │              │            │  │     │
│  │ │              │ │badge │ │              │            │  │     │
│  │ ├──────────────┼──────────┼──────────────┼────────────┤  │     │
│  │ │ Tetracycline │ │● R   │ │ ████████░░░ 81%│ ● red   │  │     │
│  │ ├──────────────┼──────────┼──────────────┼────────────┤  │     │
│  │ │ Ciprofloxacin│ │● R   │ │ ███████░░░░ 78%│ ● red   │  │     │
│  │ └──────────────┴──────────┴──────────────┴────────────┘  │     │
│  │                                                          │     │
│  │  (hover:bg-muted/50 on rows, transition-colors)          │     │
│  │  (sorted by confidence desc by default)                  │     │
│  └──────────────────────────────────────────────────────────┘     │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐     │
│  │ Resistance Chart (Recharts — horizontal BarChart)        │     │
│  │ Card rounded-xl p-6                                      │     │
│  │                                                          │     │
│  │  Resistance Profile                                      │     │
│  │  (CardTitle)                                             │     │
│  │                                                          │     │
│  │  Meropenem     ██                              5%  (S)   │     │
│  │  Amoxicillin   ███                             8%  (S)   │     │
│  │  Gentamicin    ████                           12%  (S)   │     │
│  │  Ciprofloxacin █████████████████████           78%  (R)  │     │
│  │  Tetracycline  ██████████████████████          81%  (R)  │     │
│  │  Trimethoprim  ██████████████████████░         84%  (R)  │     │
│  │                                                          │     │
│  │  (bars: emerald-500 for S, red-500 for R)                │     │
│  │  (bg-muted rounded-full for track)                       │     │
│  │  (tooltip on hover with exact %)                         │     │
│  │                                                          │     │
│  │  ← Susceptible              Resistant →                  │     │
│  │  (text-xs text-muted-foreground)                         │     │
│  └──────────────────────────────────────────────────────────┘     │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐     │
│  │ Clinical Summary (Alert — shadcn)                        │     │
│  │ border-border rounded-xl                                 │     │
│  │                                                          │     │
│  │  [FileText icon]  Clinical Recommendation                │     │
│  │                                                          │     │
│  │  Patient (Male, 65, Hypertensive) infected with          │     │
│  │  E. coli.                                                │     │
│  │                                                          │     │
│  │  Susceptible: Meropenem (95%), Amoxicillin (92%),        │     │
│  │  Gentamicin (88%)                                        │     │
│  │                                                          │     │
│  │  Resistant: Trimethoprim (84%), Tetracycline (81%),      │     │
│  │  Ciprofloxacin (78%)                                     │     │
│  │                                                          │     │
│  │  Recommendation: Meropenem                               │     │
│  │  (text-sm, prose styling)                                │     │
│  └──────────────────────────────────────────────────────────┘     │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐     │
│  │ Action Bar (flex justify-between items-center p-4)       │     │
│  │                                                          │     │
│  │  ┌────────────┐  ┌──────────────┐  ┌─────────────────┐  │     │
│  │  │ ← New      │  │ ↓ Download   │  │ ▓▓ Save to    ▓▓│  │     │
│  │  │ Prediction │  │   PDF        │  │ ▓▓ History    ▓▓│  │     │
│  │  │ (outline)  │  │ (outline)    │  │ ▓▓ (primary)  ▓▓│  │     │
│  │  └────────────┘  └──────────────┘  └─────────────────┘  │     │
│  └──────────────────────────────────────────────────────────┘     │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

### History Page (shadcn DataTable)

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                   │
│  Prediction History                                               │
│  (text-3xl font-semibold tracking-tight)                          │
│  Browse and export past AMR predictions.                          │
│  (text-muted-foreground)                                          │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐     │
│  │ FilterBar (flex gap-4 items-center)                      │     │
│  │                                                          │     │
│  │ ┌─────────────────────────┐ ┌────────────────┐ ┌──────┐ │     │
│  │ │ 🔍 Search patients,     │ │ 📅 Date range  │ │All ▼ │ │     │
│  │ │    microbes, drugs...   │ │ (Calendar      │ │result│ │     │
│  │ │ (Input with icon)       │ │  Popover)      │ │Select│ │     │
│  │ └─────────────────────────┘ └────────────────┘ └──────┘ │     │
│  └──────────────────────────────────────────────────────────┘     │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐     │
│  │ DataTable (rounded-xl border-border)                     │     │
│  │                                                          │     │
│  │ ┌────┬──────────┬──────────┬─────────┬────────┬────────┐ │     │
│  │ │ #  │ Date     │ Patient  │ Microbe │Best    │Actions │ │     │
│  │ │    │          │          │         │Drug    │        │ │     │
│  │ ├────┼──────────┼──────────┼─────────┼────────┼────────┤ │     │
│  │ │001 │ Apr 11   │ M, 65   │ E.coli  │Meropen.│ [View] │ │     │
│  │ │    │ (muted)  │ [HT]    │ (Badge) │(amber  │(Button │ │     │
│  │ │    │          │ (Badge)  │         │ badge) │ ghost) │ │     │
│  │ ├────┼──────────┼──────────┼─────────┼────────┼────────┤ │     │
│  │ │002 │ Apr 10   │ F, 32   │ S.aureus│Amox.   │ [View] │ │     │
│  │ ├────┼──────────┼──────────┼─────────┼────────┼────────┤ │     │
│  │ │003 │ Apr 09   │ M, 48   │ K.pneum.│Genta.  │ [View] │ │     │
│  │ │    │          │ [DM]    │         │        │        │ │     │
│  │ ├────┼──────────┼──────────┼─────────┼────────┼────────┤ │     │
│  │ │004 │ Apr 08   │ F, 55   │ E.coli  │Cipro.  │ [View] │ │     │
│  │ │    │          │ [HT]    │         │        │        │ │     │
│  │ └────┴──────────┴──────────┴─────────┴────────┴────────┘ │     │
│  │                                                          │     │
│  │  (hover:bg-muted/50 transition-colors on rows)           │     │
│  │  (column headers: text-muted-foreground text-xs)         │     │
│  └──────────────────────────────────────────────────────────┘     │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐     │
│  │ Footer (flex justify-between items-center)               │     │
│  │                                                          │     │
│  │  Showing 4 of 127       ┌─────────────────────────────┐  │     │
│  │  (text-sm text-muted)   │ ← 1  2  3  ...  13  →      │  │     │
│  │                         │ (Pagination — shadcn)       │  │     │
│  │                         └─────────────────────────────┘  │     │
│  │                                                          │     │
│  │  ┌──────────────────────┐                                │     │
│  │  │ ↓ Export ▼           │  (DropdownMenu)                │     │
│  │  │   ├── Export CSV     │                                │     │
│  │  │   └── Export PDF     │                                │     │
│  │  └──────────────────────┘                                │     │
│  └──────────────────────────────────────────────────────────┘     │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

---

## Responsive Layout (Tailwind breakpoints)

```
┌──────────────────────────────────────────────────────────────────┐
│                   DESKTOP (lg: > 1024px)                          │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐     │
│  │ Navbar: flex items-center justify-between px-6           │     │
│  │ [Logo]  [NavigationMenu horizontal]  [ThemeToggle]       │     │
│  ├──────────────────────────────────────────────────────────┤     │
│  │                                                          │     │
│  │ max-w-6xl mx-auto px-6                                   │     │
│  │                                                          │     │
│  │ Landing: grid grid-cols-3 gap-6 (How It Works cards)     │     │
│  │ Predict: max-w-2xl mx-auto (centered card)               │     │
│  │ Result:  grid grid-cols-2 gap-4 (Best + Avoid side by)   │     │
│  │          DataTable full width below                       │     │
│  │ History: DataTable full width                             │     │
│  │                                                          │     │
│  └──────────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────────┘

┌───────────────────────────────┐
│    TABLET (md: 768-1024px)    │
│                               │
│  Landing: grid-cols-2         │
│  (3rd card wraps below)       │
│  Result: grid-cols-1          │
│  (Best card, then Avoid card) │
│  DataTable: horizontal scroll │
└───────────────────────────────┘

┌──────────────────────────┐
│  MOBILE (< 768px)        │
│                          │
│  Navbar → Sheet (hamburger│
│  icon + slide-out menu)   │
│                          │
│  Landing: grid-cols-1     │
│  Cards: full width stack  │
│  Result: single column    │
│  Table: card-view or      │
│   horizontal scroll       │
│                          │
│  All Cards: rounded-lg    │
│  (slightly less radius)   │
│                          │
│  Buttons: w-full on       │
│  mobile (full width)      │
└──────────────────────────┘
```

---

## Micro-Interactions & Animations

```
┌──────────────────────────────────────────────────────────────────┐
│                    ANIMATIONS (Framer Motion)                      │
│                                                                   │
│  Page Transitions:                                                │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │  AnimatePresence mode="wait"                               │   │
│  │  initial={{ opacity: 0, y: 20 }}                           │   │
│  │  animate={{ opacity: 1, y: 0 }}                            │   │
│  │  exit={{ opacity: 0, y: -20 }}                             │   │
│  │  transition={{ duration: 0.2, ease: "easeInOut" }}         │   │
│  └────────────────────────────────────────────────────────────┘   │
│                                                                   │
│  Step Transitions (Predict form):                                 │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │  Step 1 → Step 2: slide left + fade                        │   │
│  │  Step 2 → Step 1: slide right + fade (back)                │   │
│  │  Indicator line: animated width fill (spring)               │   │
│  └────────────────────────────────────────────────────────────┘   │
│                                                                   │
│  Loading → Result:                                                │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │  Skeleton → content: staggered fade-in per card             │   │
│  │  Cards: initial={{ opacity:0, scale:0.95 }}                │   │
│  │  animate: staggerChildren: 0.1                             │   │
│  │  Progress bar: animated value with spring                  │   │
│  └────────────────────────────────────────────────────────────┘   │
│                                                                   │
│  Hover & Focus:                                                   │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │  Buttons:  transition-colors duration-150                  │   │
│  │  Cards:    hover:border-ring/50 transition-all             │   │
│  │  Table rows: hover:bg-muted/50 transition-colors           │   │
│  │  Inputs:   focus-visible:ring-2 ring-ring ring-offset-2    │   │
│  │  Switch:   checked:bg-primary transition-colors (200ms)    │   │
│  │  Badge:    no animation (static, crisp)                    │   │
│  └────────────────────────────────────────────────────────────┘   │
│                                                                   │
│  Chart:                                                           │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │  Bars: animate from width 0 → actual, staggered 50ms       │   │
│  │  Tooltip: fade in on hover (opacity transition)            │   │
│  └────────────────────────────────────────────────────────────┘   │
│                                                                   │
│  Toast (sonner):                                                  │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │  "Report saved to history" → slide up from bottom-right    │   │
│  │  "PDF downloaded" → slide up from bottom-right             │   │
│  │  Auto-dismiss after 3s                                     │   │
│  └────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

---

---

# PART 2: STRUCTURED DEVELOPMENT LOGS

---

## Project Directory Structure

```
AMR/
├── docs/
│   ├── Multi_Drug_AMR_Project.md          ← Original project spec
│   ├── AMR_System_Flow_Diagram.md         ← System flow diagrams
│   └── AMR_UI_Flow_And_Dev_Logs.md        ← This file (UI + Dev logs)
│
├── dev_logs/
│   ├── CHANGELOG.md                       ← Version history
│   ├── DEV_TRACKER.md                     ← Phase-wise progress tracker
│   ├── BUG_LOG.md                         ← Bug tracking
│   ├── DECISION_LOG.md                    ← Architecture decisions record
│   └── DAILY_LOG.md                       ← Daily development notes
│
│  ══════════════════════════════════════
│  BACKEND (Flask API — Python)
│  ══════════════════════════════════════
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── app.py                         ← Flask main app
│   │   ├── routes/
│   │   │   ├── predict.py                 ← POST /api/predict
│   │   │   └── history.py                 ← GET/POST /api/history
│   │   ├── ml/
│   │   │   ├── single_drug_model.py       ← Single drug pipeline
│   │   │   ├── multi_drug_model.py        ← Multi drug pipeline
│   │   │   └── preprocessing.py           ← Shared preprocessing
│   │   └── utils/
│   │       ├── validators.py              ← Input validation
│   │       └── pdf_export.py              ← PDF report generation
│   ├── data/
│   │   ├── raw/
│   │   │   └── Bacteria_dataset_Multiresistance.csv
│   │   ├── processed/
│   │   │   └── cleaned_dataset.csv
│   │   └── models/
│   │       ├── single_rf_drugA.pkl
│   │       ├── single_rf_drugB.pkl
│   │       ├── multi_rf_model.pkl
│   │       └── scaler.pkl
│   ├── tests/
│   │   ├── test_preprocessing.py
│   │   ├── test_single_model.py
│   │   ├── test_multi_model.py
│   │   └── test_routes.py
│   ├── requirements.txt
│   ├── config.py
│   └── run.py
│
│  ══════════════════════════════════════
│  FRONTEND (Next.js + shadcn/ui)
│  ══════════════════════════════════════
│
├── frontend/
│   ├── app/                               ← Next.js App Router
│   │   ├── layout.tsx                     ← Root layout + ThemeProvider
│   │   ├── page.tsx                       ← Landing page (/)
│   │   ├── predict/
│   │   │   └── page.tsx                   ← Prediction form (/predict)
│   │   ├── result/
│   │   │   └── page.tsx                   ← AMR report (/result)
│   │   ├── history/
│   │   │   └── page.tsx                   ← Prediction history (/history)
│   │   ├── about/
│   │   │   └── page.tsx                   ← About page (/about)
│   │   └── globals.css                    ← Tailwind + shadcn CSS vars
│   │
│   ├── components/
│   │   ├── ui/                            ← shadcn/ui components (auto-gen)
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── input.tsx
│   │   │   ├── label.tsx
│   │   │   ├── badge.tsx
│   │   │   ├── select.tsx
│   │   │   ├── switch.tsx
│   │   │   ├── radio-group.tsx
│   │   │   ├── checkbox.tsx
│   │   │   ├── separator.tsx
│   │   │   ├── tabs.tsx
│   │   │   ├── alert.tsx
│   │   │   ├── progress.tsx
│   │   │   ├── skeleton.tsx
│   │   │   ├── tooltip.tsx
│   │   │   ├── popover.tsx
│   │   │   ├── command.tsx
│   │   │   ├── navigation-menu.tsx
│   │   │   ├── sheet.tsx
│   │   │   ├── dropdown-menu.tsx
│   │   │   ├── table.tsx
│   │   │   ├── data-table.tsx
│   │   │   ├── chart.tsx
│   │   │   ├── calendar.tsx
│   │   │   ├── dialog.tsx
│   │   │   ├── pagination.tsx
│   │   │   └── sonner.tsx
│   │   │
│   │   ├── layout/                        ← Layout components
│   │   │   ├── navbar.tsx                 ← Sticky nav + theme toggle
│   │   │   ├── mobile-nav.tsx             ← Sheet-based mobile menu
│   │   │   ├── footer.tsx                 ← Minimal footer
│   │   │   └── theme-toggle.tsx           ← Sun/Moon toggle button
│   │   │
│   │   ├── landing/                       ← Landing page sections
│   │   │   ├── hero-section.tsx           ← Gradient heading + CTAs
│   │   │   ├── how-it-works.tsx           ← 3-step card grid
│   │   │   ├── prediction-modes.tsx       ← Full report vs single drug
│   │   │   ├── input-features.tsx         ← Patient + microbe features
│   │   │   ├── models-section.tsx         ← RF + FT-Transformer cards
│   │   │   ├── output-section.tsx         ← Tabs: per-drug/best/summary
│   │   │   ├── dataset-preview.tsx        ← Sample data table
│   │   │   └── tech-stack.tsx             ← Badge grid
│   │   │
│   │   ├── predict/                       ← Prediction form components
│   │   │   ├── step-indicator.tsx         ← Animated 3-step progress
│   │   │   ├── patient-form.tsx           ← Age, gender, HT, diabetes
│   │   │   ├── microbe-form.tsx           ← Combobox + feature inputs
│   │   │   └── loading-state.tsx          ← Skeleton + progress bar
│   │   │
│   │   └── result/                        ← Result page components
│   │       ├── patient-summary.tsx        ← Badge row card
│   │       ├── best-drug-card.tsx         ← Amber border-l highlight
│   │       ├── avoid-card.tsx             ← Red border-l warning
│   │       ├── results-table.tsx          ← Sortable DataTable
│   │       ├── resistance-chart.tsx       ← Recharts horizontal bar
│   │       ├── clinical-summary.tsx       ← Alert with recommendation
│   │       ├── single-drug-result.tsx     ← Large badge + confidence
│   │       └── action-bar.tsx             ← New/Download/Save buttons
│   │
│   ├── lib/
│   │   ├── utils.ts                       ← cn() helper (shadcn)
│   │   ├── api.ts                         ← Flask API fetch functions
│   │   └── schemas.ts                     ← Zod validation schemas
│   │
│   ├── hooks/
│   │   ├── use-prediction.ts              ← Prediction state management
│   │   └── use-history.ts                 ← History fetch + pagination
│   │
│   ├── types/
│   │   └── index.ts                       ← TypeScript interfaces
│   │
│   ├── components.json                    ← shadcn/ui config
│   ├── tailwind.config.ts                 ← Tailwind + shadcn theme
│   ├── next.config.ts                     ← Next.js config
│   ├── tsconfig.json
│   └── package.json
│
└── README.md
```

---

## DEV_TRACKER.md — Phase-wise Progress

```
# AMR Development Tracker

## Phase 1: Data & Preprocessing
──────────────────────────────────────────────────────
| Task                          | Status      | Date       | Owner   | Notes                    |
|-------------------------------|-------------|------------|---------|--------------------------|
| Collect raw dataset           | [ ]         |            |         |                          |
| EDA & data profiling          | [ ]         |            |         |                          |
| Handle missing values         | [ ]         |            |         |                          |
| Encode categorical (Gender,   | [ ]         |            |         |                          |
|   HT, Diabetes)               |             |            |         |                          |
| Scale continuous (Age, feats) | [ ]         |            |         |                          |
| Encode targets (S→0, R→1)    | [ ]         |            |         |                          |
| Train/test split              | [ ]         |            |         |                          |
| Save processed dataset        | [ ]         |            |         |                          |

## Phase 2: Model Training
──────────────────────────────────────────────────────
| Task                          | Status      | Date       | Owner   | Notes                    |
|-------------------------------|-------------|------------|---------|--------------------------|
| Single drug RF model          | [ ]         |            |         |                          |
| Multi drug RF model           | [ ]         |            |         |                          |
| FT-Transformer (single)      | [ ]         |            |         |                          |
| FT-Transformer (multi)       | [ ]         |            |         |                          |
| Model evaluation metrics      | [ ]         |            |         |                          |
| Model comparison report       | [ ]         |            |         |                          |
| Save best models (.pkl)       | [ ]         |            |         |                          |

## Phase 3: Flask Backend
──────────────────────────────────────────────────────
| Task                          | Status      | Date       | Owner   | Notes                    |
|-------------------------------|-------------|------------|---------|--------------------------|
| Flask app setup               | [ ]         |            |         |                          |
| /predict endpoint (single)    | [ ]         |            |         |                          |
| /predict endpoint (multi)     | [ ]         |            |         |                          |
| /history endpoint             | [ ]         |            |         |                          |
| Input validation              | [ ]         |            |         |                          |
| Error handling                | [ ]         |            |         |                          |
| Best drug logic               | [ ]         |            |         |                          |

## Phase 4: Frontend UI
──────────────────────────────────────────────────────
| Task                          | Status      | Date       | Owner   | Notes                    |
|-------------------------------|-------------|------------|---------|--------------------------|
| Landing page                  | [ ]         |            |         |                          |
| Step indicator component      | [ ]         |            |         |                          |
| Patient info form             | [ ]         |            |         |                          |
| Microbe info form             | [ ]         |            |         |                          |
| Drug selection (single/multi) | [ ]         |            |         |                          |
| Loading screen                | [ ]         |            |         |                          |
| Single drug result page       | [ ]         |            |         |                          |
| Multi drug result page        | [ ]         |            |         |                          |
| Resistance bar chart          | [ ]         |            |         |                          |
| History page                  | [ ]         |            |         |                          |
| Responsive design             | [ ]         |            |         |                          |
| PDF export                    | [ ]         |            |         |                          |

## Phase 5: Testing & Deployment
──────────────────────────────────────────────────────
| Task                          | Status      | Date       | Owner   | Notes                    |
|-------------------------------|-------------|------------|---------|--------------------------|
| Unit tests (preprocessing)    | [ ]         |            |         |                          |
| Unit tests (models)           | [ ]         |            |         |                          |
| Integration tests (routes)    | [ ]         |            |         |                          |
| UI testing                    | [ ]         |            |         |                          |
| Performance testing           | [ ]         |            |         |                          |
| Deploy (local / cloud)        | [ ]         |            |         |                          |
```

---

## CHANGELOG.md — Version History

```
# Changelog — AMR Prediction System

## Format
[version] - YYYY-MM-DD
### Added / Changed / Fixed / Removed

──────────────────────────────────────────────────────

## [0.1.0] - YYYY-MM-DD (Phase 1: Data Ready)
### Added
- Raw dataset loaded and profiled
- Preprocessing pipeline (encode, scale, split)
- Processed dataset saved

──────────────────────────────────────────────────────

## [0.2.0] - YYYY-MM-DD (Phase 2: Models Trained)
### Added
- Single drug RandomForest classifier
- Multi drug MultiOutputClassifier
- Model evaluation metrics
- Saved .pkl model files

──────────────────────────────────────────────────────

## [0.3.0] - YYYY-MM-DD (Phase 3: Backend Ready)
### Added
- Flask app with /predict and /history routes
- Single and multi drug prediction endpoints
- Input validation and error handling
- Best drug recommendation logic

──────────────────────────────────────────────────────

## [0.4.0] - YYYY-MM-DD (Phase 4: UI Complete)
### Added
- Multi-step input form with step indicator
- Single drug result page
- Multi drug result page with bar chart
- History page with search/filter
- Responsive design

──────────────────────────────────────────────────────

## [1.0.0] - YYYY-MM-DD (Phase 5: Release)
### Added
- Full test coverage
- PDF export
- Deployed to production
```

---

## BUG_LOG.md — Bug Tracking

```
# Bug Log — AMR Prediction System

## Format
| BUG-ID | Date | Severity | Description | Root Cause | Fix | Status |

## Severity Levels
- P0: System crash / wrong prediction
- P1: Feature broken but workaround exists
- P2: UI issue / minor logic error
- P3: Cosmetic / nice-to-have fix

──────────────────────────────────────────────────────

| BUG-ID  | Date       | Sev | Description              | Root Cause         | Fix              | Status    |
|---------|------------|-----|--------------------------|--------------------|------------------|-----------|
| BUG-001 |            | P0  |                          |                    |                  | [ ] Open  |
| BUG-002 |            | P1  |                          |                    |                  | [ ] Open  |
| BUG-003 |            | P2  |                          |                    |                  | [ ] Open  |
```

---

## DECISION_LOG.md — Architecture Decisions

```
# Decision Log — AMR Prediction System

## Format
DEC-XXX: Title
- Date:
- Context: (why this decision came up)
- Decision: (what was decided)
- Alternatives considered: (what else was on the table)
- Consequences: (trade-offs accepted)

──────────────────────────────────────────────────────

### DEC-001: Use Multi-Output Classifier over separate models
- Date: 2026-04-10
- Context: Need to predict S/R for multiple drugs simultaneously
- Decision: Use sklearn MultiOutputClassifier wrapping RandomForest
- Alternatives: Train separate binary classifier per drug
- Consequences: One model to maintain, captures cross-drug patterns,
  but requires all drug labels during training

### DEC-002: Include patient clinical features as model inputs
- Date: 2026-04-10
- Context: Age, gender, HT, diabetes affect resistance patterns
- Decision: Include patient features alongside microbe features
- Alternatives: Use only microbe/genomic features
- Consequences: Better predictions, requires clinical data collection,
  model becomes patient-aware not just microbe-aware

### DEC-003: Support both single-drug and multi-drug modes
- Date: 2026-04-10
- Context: Different clinical scenarios need different outputs
- Decision: Build dual-mode system with shared preprocessing
- Alternatives: Multi-drug only (simpler codebase)
- Consequences: More flexible, slightly more code to maintain,
  covers both focused testing and broad screening use cases

### DEC-004: Flask over FastAPI for web framework
- Date:
- Context:
- Decision:
- Alternatives:
- Consequences:
```

---

## DAILY_LOG.md — Daily Dev Notes

```
# Daily Development Log

## Format
### YYYY-MM-DD
- What was done:
- Blockers:
- Tomorrow:

──────────────────────────────────────────────────────

### 2026-04-10
- What was done:
  - Created project spec (Multi_Drug_AMR_Project.md)
  - Designed system flow diagram (AMR_System_Flow_Diagram.md)
  - Designed UI flow + dev log structure (AMR_UI_Flow_And_Dev_Logs.md)
  - Decided on dual-mode (single + multi drug) architecture
  - Added patient features (age, gender, HT, diabetes) to design
- Blockers:
  - None
- Tomorrow:
  - Set up project directory structure
  - Begin Phase 1: Data preprocessing pipeline
```

---

## How to Use These Logs

```
┌──────────────────────────────────────────────────────────────┐
│                  LOG USAGE GUIDE                              │
│                                                               │
│  ┌─────────────────┬──────────────────────────────────────┐   │
│  │ Log File        │ When to Update                       │   │
│  ├─────────────────┼──────────────────────────────────────┤   │
│  │ DEV_TRACKER.md  │ Mark [ ] → [x] when task complete    │   │
│  │                 │ Add new tasks as they emerge          │   │
│  ├─────────────────┼──────────────────────────────────────┤   │
│  │ CHANGELOG.md    │ After each phase completion           │   │
│  │                 │ After any release or milestone        │   │
│  ├─────────────────┼──────────────────────────────────────┤   │
│  │ BUG_LOG.md      │ When a bug is found                  │   │
│  │                 │ When a bug is fixed                   │   │
│  ├─────────────────┼──────────────────────────────────────┤   │
│  │ DECISION_LOG.md │ When an architecture choice is made  │   │
│  │                 │ When a trade-off is accepted          │   │
│  ├─────────────────┼──────────────────────────────────────┤   │
│  │ DAILY_LOG.md    │ End of each working session          │   │
│  │                 │ Start of next session (plan)          │   │
│  └─────────────────┴──────────────────────────────────────┘   │
│                                                               │
│  Traceability Chain:                                          │
│  DAILY_LOG → links to → DEV_TRACKER tasks                     │
│  DEV_TRACKER → links to → CHANGELOG versions                  │
│  BUG_LOG → links to → fixes in CHANGELOG                      │
│  DECISION_LOG → explains → why code is structured this way    │
└──────────────────────────────────────────────────────────────┘
```
