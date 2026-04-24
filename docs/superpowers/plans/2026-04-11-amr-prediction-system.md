# Multi-Drug AMR Prediction System — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a full-stack AMR prediction system — Flask REST API (ML backend) + Next.js shadcn/ui frontend — that predicts antibiotic resistance (S/R) for all drugs against a microbe given patient clinical features.

**Architecture:** Flask backend exposes `/api/predict` and `/api/history` endpoints. ML pipeline uses `MultiOutputClassifier(RandomForestClassifier())` trained on 10,710 samples across 15 drugs. Next.js frontend with shadcn/ui provides a 3-step form (patient → microbe → auto-generated full report). Frontend calls Flask API via fetch.

**Tech Stack:** Python 3.9+, Flask, scikit-learn, pandas, numpy, joblib | Next.js 14+, React 18, TypeScript, Tailwind CSS, shadcn/ui, Recharts, Framer Motion

---

## Real Dataset Columns

Source: `Bacteria_dataset_Multiresictance.csv` (10,710 rows)

**Patient features:**
- `age/gender` — combined "37/F" format, needs splitting
- `Diabetes` — Yes/No/True/False mixed
- `Hypertension` — Yes/No
- `Hospital_before` — Yes/No
- `Infection_Freq` — float

**Microbe:**
- `Souches` — e.g. "S290 Escherichia coli" (ID + species name)

**15 Drug target columns (S/R):**
AMX/AMP, AMC, CZ, FOX, CTX/CRO, IPM, GEN, AN, Acide nalidixique, ofx, CIP, C, Co-trimoxazole, Furanes, colistine

**Drop columns:** ID, Name, Email, Address, Collection_Date, Notes

---

## File Structure

```
AMR/
├── backend/
│   ├── venv/                          (Python virtual environment)
│   ├── requirements.txt
│   ├── config.py                      (Flask config, CORS, paths)
│   ├── run.py                         (Flask entry point)
│   ├── app/
│   │   ├── __init__.py                (Flask app factory)
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── predict.py             (POST /api/predict)
│   │   │   └── history.py             (GET/POST /api/history)
│   │   ├── ml/
│   │   │   ├── __init__.py
│   │   │   ├── preprocessing.py       (clean, encode, scale dataset)
│   │   │   ├── train.py               (train + save models)
│   │   │   └── predict.py             (load model + run inference)
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── validators.py          (input validation)
│   ├── data/
│   │   ├── raw/                       (symlink or copy of CSV)
│   │   ├── processed/                 (cleaned CSV)
│   │   └── models/                    (saved .pkl files)
│   └── tests/
│       ├── __init__.py
│       ├── test_preprocessing.py
│       ├── test_predict.py
│       └── test_routes.py
│
├── frontend/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx                   (landing)
│   │   ├── predict/page.tsx
│   │   ├── result/page.tsx
│   │   └── history/page.tsx
│   ├── components/
│   │   ├── ui/                        (shadcn auto-generated)
│   │   ├── layout/
│   │   │   ├── navbar.tsx
│   │   │   └── theme-toggle.tsx
│   │   ├── landing/
│   │   │   ├── hero-section.tsx
│   │   │   └── how-it-works.tsx
│   │   ├── predict/
│   │   │   ├── step-indicator.tsx
│   │   │   ├── patient-form.tsx
│   │   │   └── microbe-form.tsx
│   │   └── result/
│   │       ├── best-drug-card.tsx
│   │       ├── avoid-card.tsx
│   │       ├── results-table.tsx
│   │       ├── resistance-chart.tsx
│   │       └── clinical-summary.tsx
│   ├── lib/
│   │   ├── utils.ts
│   │   ├── api.ts
│   │   └── types.ts
│   ├── package.json
│   ├── tailwind.config.ts
│   ├── components.json
│   └── tsconfig.json
│
├── docs/                              (existing spec files)
└── dev_logs/
```

---

## Task 1: Project Scaffolding — Backend venv + requirements

**Files:**
- Create: `backend/requirements.txt`
- Create: `backend/venv/` (virtual environment)

- [ ] **Step 1: Create backend directory and venv**

```bash
cd /Users/qgai/Desktop/AMR
mkdir -p backend
python3 -m venv backend/venv
```

- [ ] **Step 2: Create requirements.txt**

```
flask==3.1.1
flask-cors==5.0.1
pandas==2.2.3
numpy==1.26.4
scikit-learn==1.6.1
joblib==1.4.2
gunicorn==23.0.0
```

- [ ] **Step 3: Install requirements in venv**

```bash
source backend/venv/bin/activate
pip install -r backend/requirements.txt
```

Expected: All packages install successfully.

- [ ] **Step 4: Verify installs**

```bash
source backend/venv/bin/activate
python -c "import flask, pandas, sklearn; print('OK')"
```

Expected: prints `OK`

---

## Task 2: Project Scaffolding — Backend directory structure

**Files:**
- Create: all `__init__.py` files, `config.py`, `run.py`
- Create: `data/raw/`, `data/processed/`, `data/models/`

- [ ] **Step 1: Create all backend directories**

```bash
cd /Users/qgai/Desktop/AMR/backend
mkdir -p app/routes app/ml app/utils data/raw data/processed data/models tests
```

- [ ] **Step 2: Create __init__.py files**

Create empty `__init__.py` in: `app/`, `app/routes/`, `app/ml/`, `app/utils/`, `tests/`

- [ ] **Step 3: Create config.py**

```python
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_RAW = os.path.join(BASE_DIR, "data", "raw")
DATA_PROCESSED = os.path.join(BASE_DIR, "data", "processed")
DATA_MODELS = os.path.join(BASE_DIR, "data", "models")
RAW_CSV = os.path.join(DATA_RAW, "Bacteria_dataset_Multiresictance.csv")

DRUG_COLUMNS = [
    "AMX/AMP", "AMC", "CZ", "FOX", "CTX/CRO", "IPM",
    "GEN", "AN", "Acide nalidixique", "ofx", "CIP",
    "C", "Co-trimoxazole", "Furanes", "colistine"
]

DRUG_DISPLAY_NAMES = {
    "AMX/AMP": "Amoxicillin/Ampicillin",
    "AMC": "Amoxicillin-Clavulanate",
    "CZ": "Cefazolin",
    "FOX": "Cefoxitin",
    "CTX/CRO": "Cefotaxime/Ceftriaxone",
    "IPM": "Imipenem",
    "GEN": "Gentamicin",
    "AN": "Amikacin",
    "Acide nalidixique": "Nalidixic Acid",
    "ofx": "Ofloxacin",
    "CIP": "Ciprofloxacin",
    "C": "Chloramphenicol",
    "Co-trimoxazole": "Co-trimoxazole",
    "Furanes": "Nitrofurantoin",
    "colistine": "Colistin"
}

FEATURE_COLUMNS = ["age", "gender", "Diabetes", "Hypertension",
                   "Hospital_before", "Infection_Freq"]

DROP_COLUMNS = ["ID", "Name", "Email", "Address",
                "Collection_Date", "Notes", "Souches", "age/gender"]
```

- [ ] **Step 4: Create run.py**

```python
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
```

- [ ] **Step 5: Create app/__init__.py (Flask factory)**

```python
from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)

    from app.routes.predict import predict_bp
    from app.routes.history import history_bp

    app.register_blueprint(predict_bp, url_prefix="/api")
    app.register_blueprint(history_bp, url_prefix="/api")

    return app
```

- [ ] **Step 6: Copy raw CSV to data/raw/**

```bash
cp /Users/qgai/Desktop/AMR/Bacteria_dataset_Multiresictance.csv \
   /Users/qgai/Desktop/AMR/backend/data/raw/
```

---

## Task 3: Data Preprocessing Pipeline

**Files:**
- Create: `app/ml/preprocessing.py`
- Test: `tests/test_preprocessing.py`

- [ ] **Step 1: Write test_preprocessing.py**

```python
import pandas as pd
from app.ml.preprocessing import load_and_clean, split_age_gender, encode_targets


def test_split_age_gender():
    df = pd.DataFrame({"age/gender": ["37/F", "65/M", "29/F"]})
    result = split_age_gender(df)
    assert list(result["age"]) == [37, 65, 29]
    assert list(result["gender"]) == [0, 1, 0]


def test_encode_targets():
    df = pd.DataFrame({"Drug_A": ["S", "R", "S"], "Drug_B": ["R", "R", "S"]})
    result = encode_targets(df, ["Drug_A", "Drug_B"])
    assert list(result["Drug_A"]) == [0, 1, 0]
    assert list(result["Drug_B"]) == [1, 1, 0]


def test_load_and_clean_returns_X_y():
    X, y, feature_names, drug_names = load_and_clean()
    assert X.shape[0] > 0
    assert y.shape[0] == X.shape[0]
    assert len(drug_names) == 15
```

- [ ] **Step 2: Write preprocessing.py**

```python
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import config


def split_age_gender(df):
    parts = df["age/gender"].str.split("/", expand=True)
    df["age"] = pd.to_numeric(parts[0], errors="coerce")
    df["gender"] = parts[1].map({"M": 1, "F": 0, "m": 1, "f": 0})
    return df


def encode_targets(df, drug_columns):
    for col in drug_columns:
        df[col] = df[col].map({"S": 0, "R": 1, "s": 0, "r": 1})
    return df


def clean_boolean(df, col):
    df[col] = df[col].astype(str).str.strip().str.lower()
    df[col] = df[col].map({
        "yes": 1, "true": 1, "1": 1, "1.0": 1,
        "no": 0, "false": 0, "0": 0, "0.0": 0, "nan": 0
    }).fillna(0).astype(int)
    return df


def extract_microbe_name(souches_val):
    if pd.isna(souches_val):
        return "Unknown"
    parts = str(souches_val).strip().split(" ", 1)
    return parts[1] if len(parts) > 1 else parts[0]


def load_and_clean():
    df = pd.read_csv(config.RAW_CSV)

    df = split_age_gender(df)

    for col in ["Diabetes", "Hypertension", "Hospital_before"]:
        df = clean_boolean(df, col)

    df["Infection_Freq"] = pd.to_numeric(df["Infection_Freq"], errors="coerce").fillna(0)
    df["microbe"] = df["Souches"].apply(extract_microbe_name)

    df = encode_targets(df, config.DRUG_COLUMNS)

    df["age"] = df["age"].fillna(df["age"].median())
    df["gender"] = df["gender"].fillna(0)

    feature_cols = ["age", "gender", "Diabetes", "Hypertension",
                    "Hospital_before", "Infection_Freq"]
    X = df[feature_cols].copy()
    y = df[config.DRUG_COLUMNS].copy()

    y = y.dropna(how="any")
    X = X.loc[y.index]

    scaler = MinMaxScaler()
    X[["age", "Infection_Freq"]] = scaler.fit_transform(X[["age", "Infection_Freq"]])

    return X.values, y.values, feature_cols, config.DRUG_COLUMNS, scaler


def get_microbe_list():
    df = pd.read_csv(config.RAW_CSV)
    df["microbe"] = df["Souches"].apply(extract_microbe_name)
    return sorted(df["microbe"].dropna().unique().tolist())
```

- [ ] **Step 3: Run tests**

```bash
cd /Users/qgai/Desktop/AMR/backend
source venv/bin/activate
python -m pytest tests/test_preprocessing.py -v
```

Expected: All 3 tests pass.

---

## Task 4: Model Training Pipeline

**Files:**
- Create: `app/ml/train.py`
- Output: `data/models/multi_rf_model.pkl`, `data/models/scaler.pkl`

- [ ] **Step 1: Write train.py**

```python
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import config
from app.ml.preprocessing import load_and_clean


def train_and_save():
    X, y, feature_names, drug_names, scaler = load_and_clean()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = MultiOutputClassifier(
        RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    for i, drug in enumerate(drug_names):
        print(f"\n{drug}:")
        print(classification_report(
            y_test[:, i], y_pred[:, i],
            target_names=["S", "R"], zero_division=0
        ))

    os.makedirs(config.DATA_MODELS, exist_ok=True)
    joblib.dump(model, os.path.join(config.DATA_MODELS, "multi_rf_model.pkl"))
    joblib.dump(scaler, os.path.join(config.DATA_MODELS, "scaler.pkl"))
    joblib.dump(feature_names, os.path.join(config.DATA_MODELS, "feature_names.pkl"))
    joblib.dump(drug_names, os.path.join(config.DATA_MODELS, "drug_names.pkl"))

    print("\nModel saved to", config.DATA_MODELS)
    return model, scaler


if __name__ == "__main__":
    train_and_save()
```

- [ ] **Step 2: Run training**

```bash
cd /Users/qgai/Desktop/AMR/backend
source venv/bin/activate
python -m app.ml.train
```

Expected: prints per-drug classification reports, saves 4 .pkl files.

---

## Task 5: Prediction Inference Module

**Files:**
- Create: `app/ml/predict.py`
- Test: `tests/test_predict.py`

- [ ] **Step 1: Write predict.py**

```python
import joblib
import numpy as np
import os
import config


_model = None
_scaler = None
_feature_names = None
_drug_names = None


def _load():
    global _model, _scaler, _feature_names, _drug_names
    if _model is None:
        _model = joblib.load(os.path.join(config.DATA_MODELS, "multi_rf_model.pkl"))
        _scaler = joblib.load(os.path.join(config.DATA_MODELS, "scaler.pkl"))
        _feature_names = joblib.load(os.path.join(config.DATA_MODELS, "feature_names.pkl"))
        _drug_names = joblib.load(os.path.join(config.DATA_MODELS, "drug_names.pkl"))


def predict_all_drugs(age, gender, diabetes, hypertension,
                      hospital_before, infection_freq):
    _load()

    raw = np.array([[age, infection_freq]])
    scaled = _scaler.transform(raw)

    features = np.array([[
        scaled[0][0],
        gender,
        diabetes,
        hypertension,
        hospital_before,
        scaled[0][1]
    ]])

    predictions = _model.predict(features)[0]
    probabilities = []
    for i, estimator in enumerate(_model.estimators_):
        proba = estimator.predict_proba(features)[0]
        prob_resistant = proba[1] if len(proba) > 1 else proba[0]
        probabilities.append(float(prob_resistant))

    results = []
    for i, drug in enumerate(_drug_names):
        display = config.DRUG_DISPLAY_NAMES.get(drug, drug)
        result_label = "R" if predictions[i] == 1 else "S"
        confidence = probabilities[i] if result_label == "R" else 1 - probabilities[i]
        results.append({
            "drug_code": drug,
            "drug_name": display,
            "result": result_label,
            "confidence": round(confidence * 100, 1)
        })

    results.sort(key=lambda x: x["confidence"], reverse=True)

    sensitive = [r for r in results if r["result"] == "S"]
    resistant = [r for r in results if r["result"] == "R"]
    best_drug = sensitive[0] if sensitive else None

    return {
        "all_drugs": results,
        "best_drug": best_drug,
        "sensitive": sensitive,
        "resistant": resistant
    }
```

- [ ] **Step 2: Write test_predict.py**

```python
from app.ml.predict import predict_all_drugs


def test_predict_returns_all_15_drugs():
    result = predict_all_drugs(
        age=65, gender=1, diabetes=1,
        hypertension=1, hospital_before=0, infection_freq=2.0
    )
    assert len(result["all_drugs"]) == 15
    assert all(r["result"] in ("S", "R") for r in result["all_drugs"])
    assert all(0 <= r["confidence"] <= 100 for r in result["all_drugs"])


def test_predict_has_best_drug():
    result = predict_all_drugs(
        age=30, gender=0, diabetes=0,
        hypertension=0, hospital_before=0, infection_freq=0.0
    )
    if result["sensitive"]:
        assert result["best_drug"] is not None
        assert result["best_drug"]["result"] == "S"
```

- [ ] **Step 3: Run tests**

```bash
cd /Users/qgai/Desktop/AMR/backend
source venv/bin/activate
python -m pytest tests/test_predict.py -v
```

Expected: Both tests pass.

---

## Task 6: Flask API Routes

**Files:**
- Create: `app/routes/predict.py`
- Create: `app/routes/history.py`
- Create: `app/utils/validators.py`
- Test: `tests/test_routes.py`

- [ ] **Step 1: Write validators.py**

```python
def validate_predict_input(data):
    errors = []
    if "age" not in data or not isinstance(data["age"], (int, float)):
        errors.append("age is required and must be a number")
    elif not (0 <= data["age"] <= 120):
        errors.append("age must be between 0 and 120")

    if "gender" not in data or data["gender"] not in (0, 1):
        errors.append("gender is required (0=Female, 1=Male)")

    for field in ["diabetes", "hypertension", "hospital_before"]:
        if field in data and data[field] not in (0, 1):
            errors.append(f"{field} must be 0 or 1")

    return errors
```

- [ ] **Step 2: Write predict route**

```python
from flask import Blueprint, request, jsonify
from app.ml.predict import predict_all_drugs
from app.utils.validators import validate_predict_input

predict_bp = Blueprint("predict", __name__)


@predict_bp.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON body required"}), 400

    errors = validate_predict_input(data)
    if errors:
        return jsonify({"errors": errors}), 422

    result = predict_all_drugs(
        age=data["age"],
        gender=data["gender"],
        diabetes=data.get("diabetes", 0),
        hypertension=data.get("hypertension", 0),
        hospital_before=data.get("hospital_before", 0),
        infection_freq=data.get("infection_freq", 0.0)
    )

    return jsonify(result)
```

- [ ] **Step 3: Write history route**

```python
import json
import os
from datetime import datetime
from flask import Blueprint, request, jsonify

history_bp = Blueprint("history", __name__)

HISTORY_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "data", "history.json"
)


def _load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []


def _save_history(records):
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w") as f:
        json.dump(records, f, indent=2)


@history_bp.route("/history", methods=["GET"])
def get_history():
    records = _load_history()
    return jsonify(records)


@history_bp.route("/history", methods=["POST"])
def save_history():
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON body required"}), 400

    record = {
        "id": len(_load_history()) + 1,
        "timestamp": datetime.now().isoformat(),
        "input": data.get("input", {}),
        "result": data.get("result", {})
    }

    records = _load_history()
    records.insert(0, record)
    _save_history(records)

    return jsonify(record), 201
```

- [ ] **Step 4: Write test_routes.py**

```python
import json
from app import create_app


def test_predict_endpoint():
    app = create_app()
    client = app.test_client()

    resp = client.post("/api/predict", json={
        "age": 65, "gender": 1, "diabetes": 1,
        "hypertension": 1, "hospital_before": 0,
        "infection_freq": 2.0
    })
    assert resp.status_code == 200
    data = resp.get_json()
    assert "all_drugs" in data
    assert len(data["all_drugs"]) == 15


def test_predict_validation():
    app = create_app()
    client = app.test_client()

    resp = client.post("/api/predict", json={"age": -5, "gender": 3})
    assert resp.status_code == 422


def test_history_flow():
    app = create_app()
    client = app.test_client()

    resp = client.post("/api/history", json={
        "input": {"age": 65}, "result": {"best_drug": "IPM"}
    })
    assert resp.status_code == 201

    resp = client.get("/api/history")
    assert resp.status_code == 200
    assert len(resp.get_json()) >= 1
```

- [ ] **Step 5: Run all backend tests**

```bash
cd /Users/qgai/Desktop/AMR/backend
source venv/bin/activate
python -m pytest tests/ -v
```

Expected: All tests pass.

- [ ] **Step 6: Start Flask server and manual test**

```bash
cd /Users/qgai/Desktop/AMR/backend
source venv/bin/activate
python run.py
```

Test with curl:
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"age":65,"gender":1,"diabetes":1,"hypertension":1,"hospital_before":0,"infection_freq":2.0}'
```

Expected: JSON response with all_drugs, best_drug, sensitive, resistant arrays.

---

## Task 7: Frontend Scaffolding — Next.js + shadcn/ui

**Files:**
- Create: `frontend/` (entire Next.js project)

- [ ] **Step 1: Create Next.js project**

```bash
cd /Users/qgai/Desktop/AMR
npx create-next-app@latest frontend --typescript --tailwind --eslint --app --src=no --import-alias="@/*" --use-npm
```

- [ ] **Step 2: Initialize shadcn/ui**

```bash
cd /Users/qgai/Desktop/AMR/frontend
npx shadcn@latest init -d
```

- [ ] **Step 3: Install shadcn components**

```bash
cd /Users/qgai/Desktop/AMR/frontend
npx shadcn@latest add button card input label badge select switch radio-group checkbox separator tabs alert progress skeleton tooltip popover command navigation-menu sheet dropdown-menu table dialog sonner
```

- [ ] **Step 4: Install additional dependencies**

```bash
cd /Users/qgai/Desktop/AMR/frontend
npm install framer-motion lucide-react recharts next-themes
```

- [ ] **Step 5: Verify dev server starts**

```bash
cd /Users/qgai/Desktop/AMR/frontend
npm run dev
```

Expected: Next.js dev server on http://localhost:3000

---

## Task 8: Frontend — Layout + Navbar + Theme Toggle

**Files:**
- Modify: `app/layout.tsx`
- Create: `components/layout/navbar.tsx`
- Create: `components/layout/theme-toggle.tsx`
- Modify: `app/globals.css`

- [ ] **Step 1: Set up dark mode globals.css**

Update `app/globals.css` with shadcn dark/light CSS variables + dark mode as default.

- [ ] **Step 2: Create theme-toggle.tsx**

Button with Sun/Moon icon using `next-themes` `useTheme()`.

- [ ] **Step 3: Create navbar.tsx**

Sticky navbar with logo, nav links (Home, Predict, History, About), theme toggle. Uses shadcn NavigationMenu. Mobile: Sheet-based hamburger menu.

- [ ] **Step 4: Update layout.tsx**

Wrap with `ThemeProvider` from next-themes. Add Navbar, Toaster (sonner). Set `defaultTheme="dark"`.

---

## Task 9: Frontend — Landing Page

**Files:**
- Create: `components/landing/hero-section.tsx`
- Create: `components/landing/how-it-works.tsx`
- Modify: `app/page.tsx`

- [ ] **Step 1: Create hero-section.tsx**

Gradient heading "Multi-Drug AMR Prediction System", badge "ML + DL Powered", description text, two CTA buttons (Start Prediction → /predict, View History → /history).

- [ ] **Step 2: Create how-it-works.tsx**

3-column Card grid: Step 1 (Patient Info), Step 2 (Microbe Data), Step 3 (Full AMR Report). Each card with number, Lucide icon, title, description.

- [ ] **Step 3: Wire landing page**

`app/page.tsx` renders HeroSection + HowItWorks.

---

## Task 10: Frontend — Prediction Form (Patient + Microbe)

**Files:**
- Create: `components/predict/step-indicator.tsx`
- Create: `components/predict/patient-form.tsx`
- Create: `components/predict/microbe-form.tsx`
- Create: `lib/api.ts`
- Create: `lib/types.ts`
- Modify: `app/predict/page.tsx`

- [ ] **Step 1: Create types.ts**

```typescript
export interface PredictInput {
  age: number;
  gender: number;
  diabetes: number;
  hypertension: number;
  hospital_before: number;
  infection_freq: number;
}

export interface DrugResult {
  drug_code: string;
  drug_name: string;
  result: "S" | "R";
  confidence: number;
}

export interface PredictResponse {
  all_drugs: DrugResult[];
  best_drug: DrugResult | null;
  sensitive: DrugResult[];
  resistant: DrugResult[];
}
```

- [ ] **Step 2: Create api.ts**

```typescript
import { PredictInput, PredictResponse } from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000/api";

export async function predictAMR(input: PredictInput): Promise<PredictResponse> {
  const res = await fetch(`${API_BASE}/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input),
  });
  if (!res.ok) throw new Error("Prediction failed");
  return res.json();
}
```

- [ ] **Step 3: Create step-indicator.tsx**

3-step animated indicator with circles, connecting lines, labels. Props: `currentStep: 1 | 2 | 3`.

- [ ] **Step 4: Create patient-form.tsx**

Card with: Age (Input number), Gender (RadioGroup M/F), Hypertension (Switch), Diabetes (Switch), Hospital Before (Switch), Infection Frequency (Input number). "Continue" button.

- [ ] **Step 5: Create microbe-form.tsx**

Card with: genomic feature inputs, optional single-drug filter checkbox. "Generate Full AMR Report" button.

- [ ] **Step 6: Wire predict page**

`app/predict/page.tsx` — multi-step form with state, step transitions (Framer Motion), calls `predictAMR()` on submit, navigates to `/result` with data.

---

## Task 11: Frontend — Result Page (Full AMR Report)

**Files:**
- Create: `components/result/best-drug-card.tsx`
- Create: `components/result/avoid-card.tsx`
- Create: `components/result/results-table.tsx`
- Create: `components/result/resistance-chart.tsx`
- Create: `components/result/clinical-summary.tsx`
- Modify: `app/result/page.tsx`

- [ ] **Step 1: Create best-drug-card.tsx**

Card with amber left border, star icon, drug name (text-2xl), confidence %, "Also consider" secondary list.

- [ ] **Step 2: Create avoid-card.tsx**

Card with red left border, X icon, list of resistant drugs with percentages.

- [ ] **Step 3: Create results-table.tsx**

shadcn DataTable — columns: Drug Name, Result (Badge S green / R red), Confidence (Progress bar + %), Status (dot). Sortable by confidence.

- [ ] **Step 4: Create resistance-chart.tsx**

Recharts horizontal BarChart. Green bars for S, red for R. Sorted least → most resistant. Tooltip on hover.

- [ ] **Step 5: Create clinical-summary.tsx**

shadcn Alert — auto-generated text summarizing patient info, susceptible drugs, resistant drugs, recommendation.

- [ ] **Step 6: Wire result page**

`app/result/page.tsx` — reads prediction data from URL search params or state, renders all result components.

---

## Task 12: Frontend — History Page

**Files:**
- Create: `app/history/page.tsx`
- Update: `lib/api.ts` (add history fetch)

- [ ] **Step 1: Add history API functions to api.ts**

```typescript
export async function getHistory() {
  const res = await fetch(`${API_BASE}/history`);
  return res.json();
}

export async function saveHistory(input: PredictInput, result: PredictResponse) {
  const res = await fetch(`${API_BASE}/history`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ input, result }),
  });
  return res.json();
}
```

- [ ] **Step 2: Create history page**

Page with: heading, DataTable (Date, Patient summary badges, Microbe, Best Drug amber badge, View button), pagination.

---

## Task 13: Integration Testing & Dev Logs

- [ ] **Step 1: Start Flask backend**

```bash
cd /Users/qgai/Desktop/AMR/backend
source venv/bin/activate
python run.py
```

- [ ] **Step 2: Start Next.js frontend**

```bash
cd /Users/qgai/Desktop/AMR/frontend
npm run dev
```

- [ ] **Step 3: End-to-end test**

1. Open http://localhost:3000
2. Click "Start Prediction"
3. Fill patient info → Continue
4. Fill microbe data → Generate Report
5. Verify full AMR report with all 15 drugs
6. Verify best drug card, avoid card, chart, summary
7. Save to history
8. Check history page shows the record

- [ ] **Step 4: Create dev_logs directory and initial files**

```bash
mkdir -p /Users/qgai/Desktop/AMR/dev_logs
```

Create CHANGELOG.md, DEV_TRACKER.md, DECISION_LOG.md, DAILY_LOG.md with initial entries.
