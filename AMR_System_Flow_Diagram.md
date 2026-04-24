# Multi-Drug AMR Prediction System — Complete Flow Diagram

---

## Problem Statement

Predict antibiotic resistance (**S** = Sensitive / **R** = Resistant) for **single or multiple drugs** against a microbe, using **patient clinical features** alongside microbe data.

---

## End-to-End System Flow

```
┌──────────────────────────────────────────────────────────────┐
│                     DATA COLLECTION                           │
│                                                               │
│  Source: Hospital labs, clinical records, genomic databases    │
│                                                               │
│  Patient Data:                                                │
│  ┌───────┐ ┌────────┐ ┌──────────────┐ ┌──────────┐          │
│  │  Age  │ │ Gender │ │ Hypertension │ │ Diabetes │          │
│  │ (int) │ │ (M/F)  │ │  (Yes/No)    │ │ (Yes/No) │          │
│  └───────┘ └────────┘ └──────────────┘ └──────────┘          │
│                                                               │
│  Microbe Data:                                                │
│  ┌─────────────────┐ ┌──────────────┐ ┌───────────────┐      │
│  │ Microbe Type    │ │ Genomic      │ │ Lab Culture   │      │
│  │ (E.coli, etc.)  │ │ Features     │ │ Features      │      │
│  └─────────────────┘ └──────────────┘ └───────────────┘      │
│                                                               │
│  Target Labels (per drug):                                    │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐                 │
│  │ Drug_A │ │ Drug_B │ │ Drug_C │ │ Drug_N │                 │
│  │ (S/R)  │ │ (S/R)  │ │ (S/R)  │ │ (S/R)  │                 │
│  └────────┘ └────────┘ └────────┘ └────────┘                 │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                     RAW DATASET STRUCTURE                      │
│                                                               │
│  CSV: Bacteria_dataset_Multiresistance.csv                    │
│                                                               │
│  ┌─────┬────────┬─────┬──────────┬───────┬───────┬───────┐   │
│  │ Age │ Gender │ HT  │ Diabetes │ Mic_1 │ Mic_2 │ ...   │   │
│  ├─────┼────────┼─────┼──────────┼───────┼───────┼───────┤   │
│  │ 65  │  M     │ Yes │  Yes     │ 0.82  │ 1.20  │ ...   │   │
│  │ 32  │  F     │ No  │  No      │ 0.45  │ 0.98  │ ...   │   │
│  │ 48  │  M     │ Yes │  No      │ 0.67  │ 1.05  │ ...   │   │
│  └─────┴────────┴─────┴──────────┴───────┴───────┴───────┘   │
│                                                               │
│  ┌────────┬────────┬────────┬────────┐                        │
│  │ Drug_A │ Drug_B │ Drug_C │ Drug_N │  ← Target columns     │
│  ├────────┼────────┼────────┼────────┤                        │
│  │   S    │   R    │   S    │   R    │                        │
│  │   S    │   S    │   R    │   S    │                        │
│  │   R    │   R    │   S    │   R    │                        │
│  └────────┴────────┴────────┴────────┘                        │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                      PREPROCESSING                            │
│                                                               │
│  Step 1: Encode Categorical Features                          │
│  ┌────────────────────────────────────────┐                   │
│  │ Gender:       M → 1,  F → 0           │                   │
│  │ Hypertension: Yes → 1, No → 0         │                   │
│  │ Diabetes:     Yes → 1, No → 0         │                   │
│  └────────────────────────────────────────┘                   │
│                                                               │
│  Step 2: Scale Continuous Features                            │
│  ┌────────────────────────────────────────┐                   │
│  │ Age → MinMaxScaler / StandardScaler    │                   │
│  │ Microbe features → Normalized          │                   │
│  └────────────────────────────────────────┘                   │
│                                                               │
│  Step 3: Encode Target Labels                                 │
│  ┌────────────────────────────────────────┐                   │
│  │ S → 0  (Sensitive)                     │                   │
│  │ R → 1  (Resistant)                     │                   │
│  └────────────────────────────────────────┘                   │
│                                                               │
│  Step 4: Handle Missing Values                                │
│  ┌────────────────────────────────────────┐                   │
│  │ NaN → impute (median/mode/KNN)         │                   │
│  └────────────────────────────────────────┘                   │
│                                                               │
│  Step 5: Train/Test Split                                     │
│  ┌────────────────────────────────────────┐                   │
│  │ X_train, X_test, y_train, y_test       │                   │
│  │ (80/20 or 70/30 split)                 │                   │
│  └────────────────────────────────────────┘                   │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                  FEATURE & TARGET MATRICES                     │
│                                                               │
│  Feature Matrix (X):                                          │
│  [Age, Gender, Hypertension, Diabetes,                        │
│   Microbe_feat_1, Microbe_feat_2, ..., Microbe_feat_N]       │
│                                                               │
│  Target Matrix (y):                                           │
│  ┌──────────────────────┐  ┌──────────────────────────────┐   │
│  │ Single Drug Mode:    │  │ Multi Drug Mode:             │   │
│  │ y = [Drug_A]         │  │ y = [Drug_A, Drug_B, Drug_C, │   │
│  │ shape: (n_samples,)  │  │      ..., Drug_N]            │   │
│  │                      │  │ shape: (n_samples, n_drugs)  │   │
│  └──────────────────────┘  └──────────────────────────────┘   │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                   USER SELECTS MODE                           │
│                                                               │
│          ┌─────────────────┐   ┌─────────────────┐            │
│          │  SINGLE DRUG    │   │  MULTI DRUG     │            │
│          │  MODE           │   │  MODE           │            │
│          │                 │   │                 │            │
│          │ Test resistance │   │ Screen multiple │            │
│          │ for ONE drug    │   │ drugs at once   │            │
│          └────────┬────────┘   └────────┬────────┘            │
└───────────────────┼─────────────────────┼────────────────────┘
                    │                     │
        ┌───────────┘                     └───────────┐
        │                                             │
        ▼                                             ▼
┌───────────────────────────┐   ┌──────────────────────────────┐
│    SINGLE DRUG PIPELINE   │   │    MULTI DRUG PIPELINE       │
│                           │   │                              │
│  Input:                   │   │  Input:                      │
│   Patient features        │   │   Patient features           │
│   + 1 drug selected       │   │   + N drugs selected         │
│                           │   │                              │
│  Model Options:           │   │  Model Options:              │
│  ┌──────────────────────┐ │   │  ┌────────────────────────┐  │
│  │ ML: RandomForest     │ │   │  │ ML: MultiOutput        │  │
│  │     Classifier       │ │   │  │     Classifier +       │  │
│  │                      │ │   │  │     RandomForest       │  │
│  │ Binary classification│ │   │  │                        │  │
│  │ .fit(X, y_single)    │ │   │  │ Multi-label            │  │
│  │ .predict() → 0 or 1  │ │   │  │ .fit(X, y_all)         │  │
│  └──────────────────────┘ │   │  │ .predict() → [0,1,0,..]│  │
│  ┌──────────────────────┐ │   │  └────────────────────────┘  │
│  │ DL: FT-Transformer   │ │   │  ┌────────────────────────┐  │
│  │     d_out = 1        │ │   │  │ DL: FT-Transformer     │  │
│  │                      │ │   │  │     d_out = n_drugs     │  │
│  │ Handles mixed        │ │   │  │                        │  │
│  │ numerical +          │ │   │  │ Learns cross-drug      │  │
│  │ categorical inputs   │ │   │  │ resistance correlation  │  │
│  └──────────────────────┘ │   │  │ patterns (MDR)         │  │
│                           │   │  └────────────────────────┘  │
│  Output:                  │   │                              │
│   Drug_A → S or R         │   │  Output:                     │
│   Confidence: 87%         │   │   Drug_A → S                 │
│                           │   │   Drug_B → R                 │
│  Use Case:                │   │   Drug_C → S                 │
│   Doctor testing one      │   │   Drug_N → R                 │
│   specific drug           │   │   + Best drug recommendation │
│                           │   │                              │
│  Advantage:               │   │  Use Case:                   │
│   Simpler, faster,        │   │   Lab screening all drugs    │
│   focused prediction      │   │   at once                    │
│                           │   │                              │
│                           │   │  Advantage:                  │
│                           │   │   Captures drug-drug          │
│                           │   │   correlation, finds best     │
│                           │   │   drug automatically          │
└─────────────┬─────────────┘   └──────────────┬───────────────┘
              │                                │
              └───────────────┬────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                    MODEL EVALUATION                            │
│                                                               │
│  Metrics (per drug):                                          │
│  ┌──────────────────────────────────────────────┐             │
│  │ Accuracy    — overall correct predictions     │             │
│  │ Precision   — of predicted R, how many are R  │             │
│  │ Recall      — of actual R, how many caught    │             │
│  │ F1-Score    — balance of precision & recall    │             │
│  │ AUC-ROC     — discrimination ability          │             │
│  │ Confusion Matrix — S/R breakdown              │             │
│  └──────────────────────────────────────────────┘             │
│                                                               │
│  Multi-Drug Additional Metrics:                               │
│  ┌──────────────────────────────────────────────┐             │
│  │ Hamming Loss   — fraction of wrong labels     │             │
│  │ Jaccard Score  — label overlap accuracy        │             │
│  │ Per-drug breakdown of all above metrics       │             │
│  └──────────────────────────────────────────────┘             │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                       FLASK WEB UI                            │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐   │
│  │                                                        │   │
│  │  ========== AMR Prediction System ==========           │   │
│  │                                                        │   │
│  │  --- Patient Information ---                           │   │
│  │  Age:            [__________]                          │   │
│  │  Gender:         (o) Male    (o) Female                │   │
│  │  Hypertension:   [x] Yes                               │   │
│  │  Diabetes:       [ ] No                                │   │
│  │                                                        │   │
│  │  --- Microbe Information ---                           │   │
│  │  Microbe Type:   [ E. coli        ▼ ]                  │   │
│  │  Feature 1:      [__________]                          │   │
│  │  Feature 2:      [__________]                          │   │
│  │  Feature N:      [__________]                          │   │
│  │                                                        │   │
│  │  --- Prediction Mode ---                               │   │
│  │  (o) Single Drug    (o) Multi Drug                     │   │
│  │                                                        │   │
│  │  --- If Single Drug Mode ---                           │   │
│  │  Select Drug:    [ Amoxicillin     ▼ ]                 │   │
│  │                                                        │   │
│  │  --- If Multi Drug Mode ---                            │   │
│  │  Select Drugs to Screen:                               │   │
│  │  [x] Amoxicillin                                       │   │
│  │  [x] Ciprofloxacin                                     │   │
│  │  [ ] Gentamicin                                        │   │
│  │  [x] Meropenem                                         │   │
│  │  [ ] Tetracycline                                      │   │
│  │  [x] Trimethoprim                                      │   │
│  │                                                        │   │
│  │              [ PREDICT ]                               │   │
│  │                                                        │   │
│  └────────────────────────────────────────────────────────┘   │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                     FLASK BACKEND                             │
│                                                               │
│  POST /predict                                                │
│  ┌──────────────────────────────────────────────────────┐     │
│  │ 1. Read form inputs (patient + microbe features)     │     │
│  │ 2. Detect mode (single / multi)                      │     │
│  │ 3. Preprocess inputs (encode, scale)                 │     │
│  │ 4. Load appropriate model                            │     │
│  │ 5. Run prediction                                    │     │
│  │ 6. Decode output (0 → S, 1 → R)                     │     │
│  │ 7. If multi → find best drug (lowest resistance)     │     │
│  │ 8. Return results as JSON / render template          │     │
│  └──────────────────────────────────────────────────────┘     │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                         OUTPUT                                │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐   │
│  │                                                        │   │
│  │  ========== SINGLE DRUG RESULT ==========              │   │
│  │                                                        │   │
│  │  Patient:  Male, Age 65, HT: Yes, DM: Yes             │   │
│  │  Microbe:  E. coli                                     │   │
│  │  Drug:     Amoxicillin                                 │   │
│  │                                                        │   │
│  │  Prediction:  R (Resistant)                            │   │
│  │  Confidence:  87%                                      │   │
│  │                                                        │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐   │
│  │                                                        │   │
│  │  ========== MULTI DRUG RESULT ==========               │   │
│  │                                                        │   │
│  │  Patient:  Male, Age 65, HT: Yes, DM: Yes             │   │
│  │  Microbe:  E. coli                                     │   │
│  │                                                        │   │
│  │  Drug-wise Predictions:                                │   │
│  │  ┌──────────────────┬────────────┬─────────────┐       │   │
│  │  │ Drug             │ Prediction │ Confidence  │       │   │
│  │  ├──────────────────┼────────────┼─────────────┤       │   │
│  │  │ Amoxicillin      │     S      │    92%      │       │   │
│  │  │ Ciprofloxacin    │     R      │    78%      │       │   │
│  │  │ Meropenem        │     S      │    95%      │       │   │
│  │  │ Trimethoprim     │     R      │    84%      │       │   │
│  │  └──────────────────┴────────────┴─────────────┘       │   │
│  │                                                        │   │
│  │  Best Drug Recommendation: Meropenem (95% sensitive)   │   │
│  │                                                        │   │
│  │  Clinical Summary:                                     │   │
│  │  "Patient (Male, 65, Hypertensive, Diabetic)           │   │
│  │   infected with E. coli.                               │   │
│  │   Recommend: Meropenem or Amoxicillin                  │   │
│  │   Avoid: Ciprofloxacin, Trimethoprim (Resistant)"      │   │
│  │                                                        │   │
│  └────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

---

## Why Patient Features Matter for AMR

```
┌──────────────────────────────────────────────────────────────┐
│              CLINICAL FEATURE IMPACT ON AMR                   │
│                                                               │
│  ┌────────────────┬─────────────────────────────────────┐     │
│  │ Feature        │ Impact on Resistance                │     │
│  ├────────────────┼─────────────────────────────────────┤     │
│  │ Age            │ Elderly → more prior antibiotic     │     │
│  │                │ exposure → higher resistance rates   │     │
│  ├────────────────┼─────────────────────────────────────┤     │
│  │ Gender         │ UTI resistance patterns differ      │     │
│  │                │ significantly between M/F           │     │
│  ├────────────────┼─────────────────────────────────────┤     │
│  │ Hypertension   │ Comorbidity affects drug metabolism │     │
│  │                │ and prior medication history        │     │
│  ├────────────────┼─────────────────────────────────────┤     │
│  │ Diabetes       │ Higher infection rates, more        │     │
│  │                │ antibiotic exposure → higher AMR    │     │
│  └────────────────┴─────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────┘
```

---

## Single Drug vs Multi Drug — Architecture Comparison

```
┌──────────────────────────────┐   ┌──────────────────────────────┐
│      SINGLE DRUG MODE        │   │       MULTI DRUG MODE        │
│                              │   │                              │
│  1 model per drug            │   │  1 model for all drugs       │
│                              │   │                              │
│  Model:                      │   │  Model:                      │
│   RandomForestClassifier()   │   │   MultiOutputClassifier(     │
│   .fit(X, y_single)          │   │     RandomForestClassifier() │
│   .predict() → 0 or 1       │   │   )                          │
│                              │   │   .fit(X, y_all)             │
│  OR                          │   │   .predict() → [0,1,0,1,...]│
│                              │   │                              │
│   FT-Transformer             │   │  OR                          │
│   d_out = 1                  │   │                              │
│                              │   │   FT-Transformer             │
│                              │   │   d_out = n_drugs            │
│  ────────────────────────    │   │                              │
│  Pros:                       │   │  ────────────────────────    │
│  + Simpler                   │   │  Pros:                       │
│  + Faster inference          │   │  + Captures cross-drug       │
│  + Easier to debug           │   │    resistance patterns       │
│                              │   │  + One model serves all      │
│  Cons:                       │   │  + Finds best drug auto      │
│  - No cross-drug insight     │   │                              │
│  - N models to maintain      │   │  Cons:                       │
│  - Cannot recommend best     │   │  - Heavier training          │
│    drug                      │   │  - Needs all drug labels     │
└──────────────────────────────┘   └──────────────────────────────┘
```

---

## Implementation Code Reference

### Preprocessing

```python
import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split

df = pd.read_csv("Bacteria_dataset_Multiresistance.csv")

# Encode categorical features
df['Gender'] = df['Gender'].map({'M': 1, 'F': 0})
df['Hypertension'] = df['Hypertension'].map({'Yes': 1, 'No': 0})
df['Diabetes'] = df['Diabetes'].map({'Yes': 1, 'No': 0})

# Scale continuous features
scaler = MinMaxScaler()
df['Age'] = scaler.fit_transform(df[['Age']])

# Encode drug targets
drug_columns = ['Drug_A', 'Drug_B', 'Drug_C']
df[drug_columns] = df[drug_columns].replace({'S': 0, 'R': 1})

# Split features and targets
X = df.drop(drug_columns, axis=1)
y = df[drug_columns]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
```

### Single Drug Model

```python
from sklearn.ensemble import RandomForestClassifier

# Train one model for Drug_A
model_single = RandomForestClassifier()
model_single.fit(X_train, y_train['Drug_A'])

pred_single = model_single.predict(X_test)
# Output: 0 or 1 (S or R) for Drug_A only
```

### Multi Drug Model

```python
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier

model_multi = MultiOutputClassifier(RandomForestClassifier())
model_multi.fit(X_train, y_train)

pred_multi = model_multi.predict(X_test)
# Output: [[0,1,0], [1,0,1], ...] for all drugs
```

### FT-Transformer (Deep Learning)

```python
import rtdl

# Single drug
model_dl_single = rtdl.FTTransformer.make_default(
    n_num_features=X.shape[1],
    d_out=1
)

# Multi drug
model_dl_multi = rtdl.FTTransformer.make_default(
    n_num_features=X.shape[1],
    d_out=len(drug_columns)
)
```

### Best Drug Selection (Multi Drug Mode)

```python
best_drug = min(result, key=lambda x: result[x])
# Returns the drug with lowest resistance (most sensitive)
```

### Flask Backend

```python
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    # Read patient features
    age = float(request.form["age"])
    gender = 1 if request.form["gender"] == "M" else 0
    ht = 1 if request.form.get("hypertension") else 0
    diabetes = 1 if request.form.get("diabetes") else 0
    microbe_features = [float(request.form[f"feat_{i}"]) for i in range(N_FEATURES)]

    input_vector = [age, gender, ht, diabetes] + microbe_features
    mode = request.form["mode"]

    if mode == "single":
        drug = request.form["drug"]
        model = single_models[drug]
        pred = model.predict([input_vector])
        result = {drug: "R" if pred[0] == 1 else "S"}

    elif mode == "multi":
        selected_drugs = request.form.getlist("drugs")
        pred = multi_model.predict([input_vector])
        result = {}
        for i, drug in enumerate(all_drugs):
            if drug in selected_drugs:
                result[drug] = "R" if pred[0][i] == 1 else "S"
        best_drug = min(result, key=lambda x: result[x])
        result["best_drug"] = best_drug

    return render_template("result.html", result=result, mode=mode)
```

### HTML Form

```html
<form method="POST" action="/predict">
    <h3>Patient Information</h3>
    <input type="number" name="age" placeholder="Age"><br>
    <label>Gender:</label>
    <input type="radio" name="gender" value="M"> Male
    <input type="radio" name="gender" value="F"> Female<br>
    <input type="checkbox" name="hypertension"> Hypertension<br>
    <input type="checkbox" name="diabetes"> Diabetes<br>

    <h3>Microbe Features</h3>
    <input type="text" name="feat_0" placeholder="Feature 1"><br>
    <input type="text" name="feat_1" placeholder="Feature 2"><br>

    <h3>Prediction Mode</h3>
    <input type="radio" name="mode" value="single"> Single Drug
    <input type="radio" name="mode" value="multi"> Multi Drug<br>

    <h3>Single Drug Selection</h3>
    <select name="drug">
        <option value="Drug_A">Amoxicillin</option>
        <option value="Drug_B">Ciprofloxacin</option>
        <option value="Drug_C">Meropenem</option>
    </select><br>

    <h3>Multi Drug Selection</h3>
    <input type="checkbox" name="drugs" value="Drug_A"> Amoxicillin<br>
    <input type="checkbox" name="drugs" value="Drug_B"> Ciprofloxacin<br>
    <input type="checkbox" name="drugs" value="Drug_C"> Meropenem<br>

    <button type="submit">Predict</button>
</form>
```

---

## Technology Stack

```
┌──────────────────────────────────────────────────────────────┐
│                     TECH STACK                                │
│                                                               │
│  ┌─────────────┐  ┌───────────────┐  ┌─────────────────┐     │
│  │  Frontend    │  │  Backend      │  │  ML/DL Models   │     │
│  │  HTML/CSS    │  │  Flask        │  │  scikit-learn   │     │
│  │  JavaScript  │  │  Python       │  │  rtdl (FT-T)    │     │
│  │  Bootstrap   │  │  REST API     │  │  PyTorch        │     │
│  └─────────────┘  └───────────────┘  └─────────────────┘     │
│                                                               │
│  ┌─────────────┐  ┌───────────────┐  ┌─────────────────┐     │
│  │  Data       │  │  Preprocessing│  │  Evaluation     │     │
│  │  pandas     │  │  sklearn      │  │  sklearn metrics│     │
│  │  numpy      │  │  LabelEncoder │  │  confusion_mx   │     │
│  │  CSV files  │  │  MinMaxScaler │  │  AUC-ROC        │     │
│  └─────────────┘  └───────────────┘  └─────────────────┘     │
└──────────────────────────────────────────────────────────────┘
```

---

## Summary

```
┌──────────────────────────────────────────────────────────────┐
│                     SYSTEM SUMMARY                            │
│                                                               │
│  Input:    Patient (Age, Gender, HT, Diabetes)               │
│            + Microbe features                                 │
│                                                               │
│  Modes:    Single Drug → S/R for one drug                     │
│            Multi Drug  → S/R for N drugs + best drug          │
│                                                               │
│  Models:   ML → RandomForest (Single & MultiOutput)           │
│            DL → FT-Transformer (handles mixed features)       │
│                                                               │
│  Deploy:   Flask web app with mode toggle                     │
│                                                               │
│  Output:   Per-drug S/R prediction                            │
│            Confidence scores                                  │
│            Best drug recommendation (multi mode)              │
│            Clinical summary                                   │
└──────────────────────────────────────────────────────────────┘
```
