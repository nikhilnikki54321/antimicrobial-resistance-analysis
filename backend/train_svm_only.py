"""
Train ONLY the SVM model and add it to existing model_comparison.json.
All other models are already trained — this avoids retraining them.
"""

import sys
import os
import json
import time
import joblib
import warnings
import numpy as np

warnings.filterwarnings("ignore")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from imblearn.over_sampling import SMOTE

import config
from app.ml.preprocessing import load_and_clean
from app.ml.train_all_models import add_feature_engineering, optimize_thresholds, predict_with_thresholds


def train_svm():
    print("=" * 60)
    print("Training SVM (Support Vector Machine) for AMR Prediction")
    print("=" * 60)

    # --- Load and prepare data (same pipeline as train_all) ---
    print("\nLoading and cleaning data...")
    X, y, feature_names, drug_names, scaler, microbe_cols = load_and_clean()
    n_base = len(feature_names)
    print(f"Dataset: {X.shape[0]} samples, {n_base} features, {y.shape[1]} drugs")

    print("Adding engineered features...")
    X = X.astype(np.float32)
    X = add_feature_engineering(X, n_base_features=6)
    X = X.astype(np.float32)
    y = y.astype(np.float32)

    eng_names = [
        "age_x_diabetes", "age_x_hypertension", "age_x_hospital",
        "age_x_infection", "infection_x_hospital", "infection_x_diabetes",
        "diabetes_x_hypertension", "diabetes_x_hospital", "hypertension_x_hospital",
        "comorbidity_count", "risk_score", "age_squared", "infection_squared",
    ]
    all_feature_names = feature_names + eng_names
    print(f"Enhanced: {X.shape[1]} total features")

    # --- Same split as train_all (same random_state) ---
    X_trainval, X_test, y_trainval, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_trainval, y_trainval, test_size=0.15, random_state=42
    )
    print(f"Train: {X_train.shape[0]}, Val: {X_val.shape[0]}, Test: {X_test.shape[0]}")

    # --- Train SVM ---
    print("\nTraining SVM (kernel=rbf, C=10, class_weight=balanced, probability=True)...")
    print("  This may take a few minutes due to probability calibration...")

    svm_estimator = SVC(
        kernel="rbf", C=10.0, gamma="scale",
        class_weight="balanced", probability=True,
        cache_size=200, random_state=42,
    )

    start = time.time()
    model = MultiOutputClassifier(svm_estimator, n_jobs=2)
    model.fit(X_train, y_train)
    train_time = round(time.time() - start, 2)
    print(f"  Training completed in {train_time}s")

    # --- Optimize thresholds ---
    print("  Optimizing per-drug thresholds...")
    thresholds = optimize_thresholds(model, X_val, y_val)

    # --- Evaluate ---
    start = time.time()
    y_pred = predict_with_thresholds(model, X_test, thresholds)
    predict_time = round(time.time() - start, 4)

    per_drug = {}
    for i, drug in enumerate(drug_names):
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

    # --- Save model and thresholds ---
    os.makedirs(config.DATA_MODELS, exist_ok=True)
    joblib.dump(model, os.path.join(config.DATA_MODELS, "svm_model.pkl"))
    joblib.dump(thresholds, os.path.join(config.DATA_MODELS, "svm_thresholds.pkl"))
    print(f"  Saved: svm_model.pkl, svm_thresholds.pkl")

    # --- Update model_comparison.json ---
    report_path = os.path.join(config.DATA_MODELS, "model_comparison.json")
    if os.path.exists(report_path):
        with open(report_path, "r") as f:
            comparison = json.load(f)
    else:
        comparison = {}

    comparison["svm"] = {
        "name": "SVM (Support Vector Machine)",
        "overall": overall,
        "per_drug": per_drug,
        "train_time_sec": train_time,
        "predict_time_sec": predict_time,
    }

    # Recalculate best model
    model_keys = [k for k in comparison if not k.startswith("_")]
    best_key = max(model_keys, key=lambda k: comparison[k]["overall"]["f1"])
    comparison["_best_model"] = best_key

    with open(report_path, "w") as f:
        json.dump(comparison, f, indent=2)
    print(f"  Updated: model_comparison.json")

    # --- Print results ---
    print(f"\n{'='*60}")
    print(f"SVM RESULTS:")
    print(f"  Accuracy:  {overall['accuracy']}%")
    print(f"  F1 Score:  {overall['f1']}%")
    print(f"  Precision: {overall['precision']}%")
    print(f"  Recall:    {overall['recall']}%")
    print(f"  Train time:   {train_time}s")
    print(f"  Predict time: {predict_time}s")
    print(f"\nBest overall model: {comparison[best_key]['name']} (F1={comparison[best_key]['overall']['f1']}%)")
    print(f"{'='*60}")

    # --- Per-drug breakdown ---
    print(f"\nPer-drug breakdown:")
    print(f"  {'Drug':<25} {'Acc':>6} {'F1':>6} {'Prec':>6} {'Rec':>6}")
    print(f"  {'-'*25} {'-'*6} {'-'*6} {'-'*6} {'-'*6}")
    for drug, m in per_drug.items():
        print(f"  {drug:<25} {m['accuracy']:>5.1f}% {m['f1']:>5.1f}% {m['precision']:>5.1f}% {m['recall']:>5.1f}%")

    print(f"\nDone! SVM is now available in the model comparison page.")
    return comparison


if __name__ == "__main__":
    train_svm()
