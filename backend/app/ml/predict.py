import sys
import os
import joblib
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import config
from app.ml.preprocessing import normalize_microbe


_model = None
_scaler = None
_feature_names = None
_drug_names = None
_microbe_columns = None
_thresholds = None
_model_cache = {}


def _load():
    global _model, _scaler, _feature_names, _drug_names, _microbe_columns, _thresholds
    if _model is None:
        _model = joblib.load(os.path.join(config.DATA_MODELS, "multi_rf_model.pkl"))
        _scaler = joblib.load(os.path.join(config.DATA_MODELS, "scaler.pkl"))
        _feature_names = joblib.load(os.path.join(config.DATA_MODELS, "feature_names.pkl"))
        _drug_names = joblib.load(os.path.join(config.DATA_MODELS, "drug_names.pkl"))
        mc_path = os.path.join(config.DATA_MODELS, "microbe_columns.pkl")
        _microbe_columns = joblib.load(mc_path) if os.path.exists(mc_path) else []
        thresh_path = os.path.join(config.DATA_MODELS, "best_thresholds.pkl")
        _thresholds = joblib.load(thresh_path) if os.path.exists(thresh_path) else None


def _load_model(model_key):
    if model_key not in _model_cache:
        path = os.path.join(config.DATA_MODELS, f"{model_key}_model.pkl")
        if not os.path.exists(path):
            return None, None
        _model_cache[model_key] = joblib.load(path)
    thresh_path = os.path.join(config.DATA_MODELS, f"{model_key}_thresholds.pkl")
    thresholds = joblib.load(thresh_path) if os.path.exists(thresh_path) else None
    _load()
    return _model_cache[model_key], thresholds


def _build_features(age, gender, diabetes, hypertension, hospital_before,
                    infection_freq, microbe_name=""):
    _load()
    raw = np.array([[age, infection_freq]])
    scaled = _scaler.transform(raw)
    s_age = scaled[0][0]
    s_inf = scaled[0][1]

    # Base features
    base = [s_age, gender, diabetes, hypertension, hospital_before, s_inf]

    # Microbe one-hot
    normalized = normalize_microbe(microbe_name) if microbe_name else "Other"
    microbe_vec = []
    for col in _microbe_columns:
        microbe_type = col.replace("microbe_", "")
        microbe_vec.append(1.0 if microbe_type == normalized else 0.0)

    # Engineered features (must match train_all_models.py)
    engineered = [
        s_age * diabetes,
        s_age * hypertension,
        s_age * hospital_before,
        s_age * s_inf,
        s_inf * hospital_before,
        s_inf * diabetes,
        diabetes * hypertension,
        diabetes * hospital_before,
        hypertension * hospital_before,
        diabetes + hypertension + hospital_before,  # comorbidity
        s_age * 0.25 + s_inf * 0.25 + (diabetes + hypertension + hospital_before) * 0.5,  # risk
        s_age ** 2,
        s_inf ** 2,
    ]

    return np.array([base + microbe_vec + engineered])


def _run_prediction(model, features, thresholds=None):
    _load()

    if thresholds is not None:
        # Use optimized thresholds
        results = []
        for i, estimator in enumerate(model.estimators_):
            try:
                proba = estimator.predict_proba(features)[0]
                if len(proba) > 1:
                    prob_r = proba[1]
                    pred = 1 if prob_r >= thresholds[i] else 0
                else:
                    pred = int(estimator.predict(features)[0])
                    prob_r = 1.0 if pred == 1 else 0.0
            except AttributeError:
                pred = int(estimator.predict(features)[0])
                prob_r = 1.0 if pred == 1 else 0.0

            drug = _drug_names[i]
            display = config.DRUG_DISPLAY_NAMES.get(drug, drug)
            result_label = "R" if pred == 1 else "S"
            confidence = prob_r if result_label == "R" else 1 - prob_r
            results.append({
                "drug_code": drug,
                "drug_name": display,
                "result": result_label,
                "confidence": round(confidence * 100, 1),
            })
    else:
        predictions = model.predict(features)[0]
        results = []
        for i, estimator in enumerate(model.estimators_):
            try:
                proba = estimator.predict_proba(features)[0]
                prob_r = proba[1] if len(proba) > 1 else (1.0 if predictions[i] == 1 else 0.0)
            except AttributeError:
                prob_r = 1.0 if predictions[i] == 1 else 0.0

            drug = _drug_names[i]
            display = config.DRUG_DISPLAY_NAMES.get(drug, drug)
            result_label = "R" if predictions[i] == 1 else "S"
            confidence = prob_r if result_label == "R" else 1 - prob_r
            results.append({
                "drug_code": drug,
                "drug_name": display,
                "result": result_label,
                "confidence": round(confidence * 100, 1),
            })

    results.sort(key=lambda x: x["confidence"], reverse=True)
    sensitive = [r for r in results if r["result"] == "S"]
    resistant = [r for r in results if r["result"] == "R"]
    best_drug = sensitive[0] if sensitive else None

    return {
        "all_drugs": results,
        "best_drug": best_drug,
        "sensitive": sensitive,
        "resistant": resistant,
    }


def predict_all_drugs(age, gender, diabetes, hypertension,
                      hospital_before, infection_freq, microbe_name=""):
    _load()
    features = _build_features(age, gender, diabetes, hypertension,
                               hospital_before, infection_freq, microbe_name)
    return _run_prediction(_model, features, _thresholds)


def predict_with_model(model_key, age, gender, diabetes, hypertension,
                       hospital_before, infection_freq, microbe_name=""):
    model, thresholds = _load_model(model_key)
    if model is None:
        return {"error": f"Model '{model_key}' not found"}
    features = _build_features(age, gender, diabetes, hypertension,
                               hospital_before, infection_freq, microbe_name)
    result = _run_prediction(model, features, thresholds)
    result["model_used"] = model_key
    return result
