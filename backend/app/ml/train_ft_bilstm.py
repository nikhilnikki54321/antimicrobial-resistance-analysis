"""
Train FT-Transformer + BiLSTM model standalone.
Run this AFTER train_all_models.py (uses same data split).
"""

import sys
import os
import json
import time
import joblib
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
import config
from app.ml.preprocessing import load_and_clean
from app.ml.ft_bilstm_model import FTBiLSTMWrapper


def add_feature_engineering(X):
    age = X[:, 0:1]; diabetes = X[:, 2:3]; hypertension = X[:, 3:4]
    hospital = X[:, 4:5]; infection = X[:, 5:6]
    eng = np.hstack([
        age*diabetes, age*hypertension, age*hospital, age*infection,
        infection*hospital, infection*diabetes, diabetes*hypertension,
        diabetes*hospital, hypertension*hospital,
        diabetes+hypertension+hospital,
        age*0.25 + infection*0.25 + (diabetes+hypertension+hospital)*0.5,
        age**2, infection**2,
    ])
    return np.hstack([X, eng])


def train():
    print("Loading data...")
    X, y, feat, drugs, scaler, mcols = load_and_clean()
    X = X.astype(np.float32)
    X = add_feature_engineering(X)
    X = X.astype(np.float32)
    y = y.astype(np.float32)
    print(f"Dataset: {X.shape[0]} samples, {X.shape[1]} features, {y.shape[1]} drugs")

    X_trainval, X_test, y_trainval, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(X_trainval, y_trainval, test_size=0.15, random_state=42)
    print(f"Train: {X_train.shape[0]}, Val: {X_val.shape[0]}, Test: {X_test.shape[0]}")

    print(f"\nTraining FT-Transformer + BiLSTM (40 epochs)...\n")
    start = time.time()

    model = FTBiLSTMWrapper(
        n_features=X_train.shape[1],
        n_drugs=y_train.shape[1],
        epochs=40,
        lr=0.001,
        batch_size=128,
    )
    model.fit(X_train, y_train)
    train_time = round(time.time() - start, 2)

    print("\nOptimizing per-drug thresholds...")
    thresholds = model.optimize_thresholds(X_val, y_val)
    print(f"Thresholds: {[round(t, 2) for t in thresholds]}")

    y_pred = model.predict(X_test)

    per_drug = {}
    for i, drug in enumerate(drugs):
        per_drug[drug] = {
            "accuracy": round(accuracy_score(y_test[:, i], y_pred[:, i]) * 100, 2),
            "f1": round(f1_score(y_test[:, i], y_pred[:, i], zero_division=0) * 100, 2),
            "precision": round(precision_score(y_test[:, i], y_pred[:, i], zero_division=0) * 100, 2),
            "recall": round(recall_score(y_test[:, i], y_pred[:, i], zero_division=0) * 100, 2),
        }

    overall = {
        "accuracy": round(np.mean([v["accuracy"] for v in per_drug.values()]), 2),
        "f1": round(np.mean([v["f1"] for v in per_drug.values()]), 2),
        "precision": round(np.mean([v["precision"] for v in per_drug.values()]), 2),
        "recall": round(np.mean([v["recall"] for v in per_drug.values()]), 2),
    }

    print(f"\n{'='*50}")
    print(f"FT-Transformer + BiLSTM Results")
    print(f"{'='*50}")
    print(f"  Accuracy:  {overall['accuracy']}%")
    print(f"  F1 Score:  {overall['f1']}%")
    print(f"  Precision: {overall['precision']}%")
    print(f"  Recall:    {overall['recall']}%")
    print(f"  Train time: {train_time}s")

    joblib.dump(model, os.path.join(config.DATA_MODELS, "ft_bilstm_model.pkl"))
    joblib.dump(thresholds, os.path.join(config.DATA_MODELS, "ft_bilstm_thresholds.pkl"))
    print(f"\nModel saved.")

    report_path = os.path.join(config.DATA_MODELS, "model_comparison.json")
    if os.path.exists(report_path):
        with open(report_path, "r") as f:
            comparison = json.load(f)
    else:
        comparison = {}

    comparison["ft_bilstm"] = {
        "name": "FT-Transformer + BiLSTM",
        "overall": overall,
        "per_drug": per_drug,
        "train_time_sec": train_time,
        "predict_time_sec": 0,
    }

    best_key = max(
        [k for k in comparison if not k.startswith("_")],
        key=lambda k: comparison[k]["overall"]["f1"]
    )
    comparison["_best_model"] = best_key

    with open(report_path, "w") as f:
        json.dump(comparison, f, indent=2)

    print(f"Comparison updated. Best: {comparison[best_key]['name']} (F1: {comparison[best_key]['overall']['f1']}%)")


if __name__ == "__main__":
    train()
