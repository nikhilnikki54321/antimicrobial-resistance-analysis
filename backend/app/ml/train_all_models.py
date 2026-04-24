"""
Train 8 models + SHAP for AMR Prediction.

Models:
1. Random Forest
2. XGBoost
3. LightGBM
4. CatBoost
5. Extra Trees
6. MLP Neural Network
7. SVM (Support Vector Machine)
8. FT-Transformer + BiLSTM (hybrid deep learning)
+ SHAP explainability on best model
"""

import sys
import os
import json
import time
import joblib
import warnings
import numpy as np

warnings.filterwarnings("ignore")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from imblearn.over_sampling import SMOTE
import config
from app.ml.preprocessing import load_and_clean
from app.ml.ft_bilstm_model import FTBiLSTMWrapper


MODEL_CONFIGS = {
    "random_forest": {
        "name": "Random Forest",
        "estimator": RandomForestClassifier(
            n_estimators=300, class_weight="balanced_subsample",
            max_depth=20, min_samples_split=3, min_samples_leaf=2,
            max_features="sqrt", random_state=42, n_jobs=-1,
        ),
        "use_smote": False,
        "multi_output": True,
    },
    "xgboost": {
        "name": "XGBoost",
        "estimator": XGBClassifier(
            n_estimators=200, max_depth=8, learning_rate=0.08,
            subsample=0.8, colsample_bytree=0.8,
            scale_pos_weight=3.0, random_state=42,
            use_label_encoder=False, verbosity=0, n_jobs=-1,
        ),
        "use_smote": False,
        "multi_output": True,
    },
    "lightgbm": {
        "name": "LightGBM",
        "estimator": LGBMClassifier(
            n_estimators=200, max_depth=10, learning_rate=0.08,
            subsample=0.8, colsample_bytree=0.8,
            is_unbalance=True, random_state=42,
            verbose=-1, n_jobs=-1,
        ),
        "use_smote": False,
        "multi_output": True,
    },
    "catboost": {
        "name": "CatBoost",
        "estimator": CatBoostClassifier(
            iterations=200, depth=8, learning_rate=0.08,
            auto_class_weights="Balanced",
            random_state=42, verbose=0,
        ),
        "use_smote": False,
        "multi_output": True,
    },
    "extra_trees": {
        "name": "Extra Trees",
        "estimator": ExtraTreesClassifier(
            n_estimators=300, class_weight="balanced_subsample",
            max_depth=20, min_samples_split=3, min_samples_leaf=2,
            max_features="sqrt", random_state=42, n_jobs=-1,
        ),
        "use_smote": False,
        "multi_output": True,
    },
    "mlp": {
        "name": "MLP Neural Network",
        "estimator": MLPClassifier(
            hidden_layer_sizes=(256, 128, 64),
            activation="relu", max_iter=500,
            early_stopping=True, validation_fraction=0.1,
            random_state=42, verbose=False,
        ),
        "use_smote": True,
        "multi_output": True,
    },
    "svm": {
        "name": "SVM (Support Vector Machine)",
        "estimator": SVC(
            kernel="rbf", C=10.0, gamma="scale",
            class_weight="balanced", probability=True,
            cache_size=500, random_state=42,
        ),
        "use_smote": False,
        "multi_output": True,
    },
}


def add_feature_engineering(X, n_base_features=6):
    age = X[:, 0:1]
    diabetes = X[:, 2:3]
    hypertension = X[:, 3:4]
    hospital = X[:, 4:5]
    infection = X[:, 5:6]

    engineered = np.hstack([
        age * diabetes,
        age * hypertension,
        age * hospital,
        age * infection,
        infection * hospital,
        infection * diabetes,
        diabetes * hypertension,
        diabetes * hospital,
        hypertension * hospital,
        diabetes + hypertension + hospital,
        age * 0.25 + infection * 0.25 + (diabetes + hypertension + hospital) * 0.5,
        age ** 2,
        infection ** 2,
    ])

    return np.hstack([X, engineered])


def apply_smote(X_train, y_train):
    smote = SMOTE(random_state=42, k_neighbors=3)
    combined = (y_train.sum(axis=1) > y_train.shape[1] * 0.3).astype(int)
    try:
        X_res, _ = smote.fit_resample(X_train, combined)
        from sklearn.neighbors import KNeighborsClassifier as KNC
        knn = KNC(n_neighbors=1, n_jobs=-1)
        knn.fit(X_train, y_train)
        y_res = knn.predict(X_res)
        return X_res, y_res
    except Exception:
        return X_train, y_train


def optimize_thresholds(model, X_val, y_val, is_multi_output=True):
    n_drugs = y_val.shape[1]
    thresholds = np.full(n_drugs, 0.5)

    for i in range(n_drugs):
        if is_multi_output:
            estimator = model.estimators_[i]
        else:
            estimator = model

        try:
            if is_multi_output:
                probas = estimator.predict_proba(X_val)
            else:
                probas_all = estimator.predict_proba(X_val)
                probas = np.column_stack([1 - probas_all[:, i], probas_all[:, i]])

            if probas.shape[1] < 2:
                continue
            prob_r = probas[:, 1]
        except (AttributeError, IndexError):
            continue

        best_f1 = 0
        best_t = 0.5
        for t in np.arange(0.2, 0.8, 0.05):
            preds = (prob_r >= t).astype(int)
            f1 = f1_score(y_val[:, i], preds, zero_division=0)
            if f1 > best_f1:
                best_f1 = f1
                best_t = t
        thresholds[i] = best_t

    return thresholds


def predict_with_thresholds(model, X, thresholds, is_multi_output=True):
    n_drugs = len(thresholds)
    preds = np.zeros((X.shape[0], n_drugs), dtype=int)

    for i in range(n_drugs):
        if is_multi_output:
            estimator = model.estimators_[i]
        else:
            estimator = model

        try:
            if is_multi_output:
                probas = estimator.predict_proba(X)
            else:
                probas_all = estimator.predict_proba(X)
                probas = np.column_stack([1 - probas_all[:, i], probas_all[:, i]])

            if probas.shape[1] >= 2:
                preds[:, i] = (probas[:, 1] >= thresholds[i]).astype(int)
            else:
                preds[:, i] = estimator.predict(X)
        except (AttributeError, IndexError):
            if is_multi_output:
                preds[:, i] = estimator.predict(X)
            else:
                preds[:, i] = model.predict(X)[:, i]

    return preds


def compute_metrics(y_true, y_pred, drug_names):
    per_drug = {}
    for i, drug in enumerate(drug_names):
        per_drug[drug] = {
            "accuracy": round(accuracy_score(y_true[:, i], y_pred[:, i]) * 100, 2),
            "f1": round(f1_score(y_true[:, i], y_pred[:, i], zero_division=0) * 100, 2),
            "precision": round(precision_score(y_true[:, i], y_pred[:, i], zero_division=0) * 100, 2),
            "recall": round(recall_score(y_true[:, i], y_pred[:, i], zero_division=0) * 100, 2),
        }

    overall = {
        "accuracy": round(np.mean([v["accuracy"] for v in per_drug.values()]), 2),
        "f1": round(np.mean([v["f1"] for v in per_drug.values()]), 2),
        "precision": round(np.mean([v["precision"] for v in per_drug.values()]), 2),
        "recall": round(np.mean([v["recall"] for v in per_drug.values()]), 2),
    }

    return overall, per_drug


def run_shap(best_model, X_test, feature_names, drug_names):
    """Run SHAP on best model and save results."""
    import shap
    print("\nRunning SHAP explainability...")

    shap_results = {}
    sample = X_test[:200]

    try:
        if hasattr(best_model, "estimators_"):
            for i, (est, drug) in enumerate(zip(best_model.estimators_, drug_names)):
                explainer = shap.TreeExplainer(est)
                shap_values = explainer.shap_values(sample)
                if isinstance(shap_values, list):
                    sv = shap_values[1] if len(shap_values) > 1 else shap_values[0]
                else:
                    sv = shap_values

                importance = np.abs(sv).mean(axis=0).tolist()
                top_features = sorted(
                    zip(feature_names[:len(importance)], importance),
                    key=lambda x: x[1], reverse=True
                )[:10]
                shap_results[drug] = [
                    {"feature": f, "importance": round(imp, 4)}
                    for f, imp in top_features
                ]
            print(f"  SHAP computed for {len(drug_names)} drugs")
        else:
            print("  SHAP: model type not supported for TreeExplainer, skipping")
    except Exception as e:
        print(f"  SHAP failed: {e}")

    return shap_results


def train_all():
    print("Loading and cleaning data...")
    X, y, feature_names, drug_names, scaler, microbe_cols = load_and_clean()
    n_base = len(feature_names)
    print(f"Dataset: {X.shape[0]} samples, {n_base} features "
          f"(incl. {len(microbe_cols)} microbe one-hot), {y.shape[1]} drugs")

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

    X_trainval, X_test, y_trainval, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_trainval, y_trainval, test_size=0.15, random_state=42
    )
    print(f"Train: {X_train.shape[0]}, Val: {X_val.shape[0]}, Test: {X_test.shape[0]}")

    print("Preparing SMOTE data...")
    X_train_sm, y_train_sm = apply_smote(X_train, y_train)
    print(f"SMOTE: {X_train_sm.shape[0]} samples\n")

    os.makedirs(config.DATA_MODELS, exist_ok=True)
    joblib.dump(scaler, os.path.join(config.DATA_MODELS, "scaler.pkl"))
    joblib.dump(all_feature_names, os.path.join(config.DATA_MODELS, "feature_names.pkl"))
    joblib.dump(drug_names, os.path.join(config.DATA_MODELS, "drug_names.pkl"))
    joblib.dump(microbe_cols, os.path.join(config.DATA_MODELS, "microbe_columns.pkl"))

    comparison = {}

    # --- Helper to train one sklearn model ---
    def train_one_model(model_key, model_cfg):
        name = model_cfg["name"]
        use_smote = model_cfg["use_smote"]

        train_X = X_train_sm if use_smote else X_train
        train_y = y_train_sm if use_smote else y_train

        start = time.time()
        model = MultiOutputClassifier(model_cfg["estimator"])
        model.fit(train_X, train_y)
        train_time = round(time.time() - start, 2)

        thresholds = optimize_thresholds(model, X_val, y_val)

        start = time.time()
        y_pred = predict_with_thresholds(model, X_test, thresholds)
        predict_time = round(time.time() - start, 4)

        overall, per_drug = compute_metrics(y_test, y_pred, drug_names)

        joblib.dump(model, os.path.join(config.DATA_MODELS, f"{model_key}_model.pkl"))
        joblib.dump(thresholds, os.path.join(config.DATA_MODELS, f"{model_key}_thresholds.pkl"))

        return model_key, {
            "name": name,
            "overall": overall,
            "per_drug": per_drug,
            "train_time_sec": train_time,
            "predict_time_sec": predict_time,
        }

    # --- Helper to train FT-BiLSTM ---
    def train_ft_bilstm():
        start = time.time()
        ft_model = FTBiLSTMWrapper(
            n_features=X_train.shape[1],
            n_drugs=y_train.shape[1],
            epochs=40,
            lr=0.001,
            batch_size=128,
        )
        ft_model.fit(X_train, y_train)
        train_time = round(time.time() - start, 2)

        ft_thresholds = ft_model.optimize_thresholds(X_val, y_val)

        start = time.time()
        y_pred_ft = ft_model.predict(X_test)
        predict_time = round(time.time() - start, 4)

        overall_ft, per_drug_ft = compute_metrics(y_test, y_pred_ft, drug_names)

        joblib.dump(ft_model, os.path.join(config.DATA_MODELS, "ft_bilstm_model.pkl"))
        joblib.dump(ft_thresholds, os.path.join(config.DATA_MODELS, "ft_bilstm_thresholds.pkl"))

        return "ft_bilstm", {
            "name": "FT-Transformer + BiLSTM",
            "overall": overall_ft,
            "per_drug": per_drug_ft,
            "train_time_sec": train_time,
            "predict_time_sec": predict_time,
        }

    # --- Train ALL models in parallel ---
    from concurrent.futures import ThreadPoolExecutor, as_completed

    total_start = time.time()
    print("Training 8 models in parallel...")
    print(f"  7 sklearn models + 1 FT-Transformer+BiLSTM")
    print()

    futures = {}
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Submit all 6 sklearn models
        for model_key, model_cfg in MODEL_CONFIGS.items():
            future = executor.submit(train_one_model, model_key, model_cfg)
            futures[future] = model_cfg["name"]

        # Submit FT-BiLSTM
        ft_future = executor.submit(train_ft_bilstm)
        futures[ft_future] = "FT-Transformer + BiLSTM"

        # Collect results as they finish
        for future in as_completed(futures):
            name = futures[future]
            try:
                key, result = future.result()
                comparison[key] = result
                o = result["overall"]
                print(f"  Done: {name:<28} F1={o['f1']}%  Acc={o['accuracy']}%  Time={result['train_time_sec']}s")
            except Exception as e:
                print(f"  FAILED: {name} - {e}")

    total_time = round(time.time() - total_start, 1)
    print(f"\nAll 8 models trained in {total_time}s (parallel)\n")

    # --- Find best model ---
    best_key = max(comparison, key=lambda k: comparison[k]["overall"]["f1"])
    comparison["_best_model"] = best_key

    print(f"\n{'='*60}")
    print(f"BEST MODEL: {comparison[best_key]['name']}")
    print(f"  F1:       {comparison[best_key]['overall']['f1']}%")
    print(f"  Accuracy: {comparison[best_key]['overall']['accuracy']}%")
    print(f"{'='*60}")

    # Save best as default
    if best_key == "ft_bilstm":
        joblib.dump(ft_model, os.path.join(config.DATA_MODELS, "multi_rf_model.pkl"))
        joblib.dump(ft_thresholds, os.path.join(config.DATA_MODELS, "best_thresholds.pkl"))
    else:
        best_model = joblib.load(os.path.join(config.DATA_MODELS, f"{best_key}_model.pkl"))
        best_thresh = joblib.load(os.path.join(config.DATA_MODELS, f"{best_key}_thresholds.pkl"))
        joblib.dump(best_model, os.path.join(config.DATA_MODELS, "multi_rf_model.pkl"))
        joblib.dump(best_thresh, os.path.join(config.DATA_MODELS, "best_thresholds.pkl"))

    # --- Run SHAP on best sklearn model ---
    best_sklearn_key = max(
        [k for k in comparison if k != "ft_bilstm" and not k.startswith("_")],
        key=lambda k: comparison[k]["overall"]["f1"]
    )
    best_sklearn_model = joblib.load(
        os.path.join(config.DATA_MODELS, f"{best_sklearn_key}_model.pkl")
    )
    shap_results = run_shap(best_sklearn_model, X_test, all_feature_names, drug_names)
    comparison["_shap"] = shap_results

    # Save comparison
    report_path = os.path.join(config.DATA_MODELS, "model_comparison.json")
    with open(report_path, "w") as f:
        json.dump(comparison, f, indent=2)
    print(f"\nComparison saved to {report_path}")

    return comparison


if __name__ == "__main__":
    train_all()
