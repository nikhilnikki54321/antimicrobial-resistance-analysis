import sys
import os
import joblib

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import config
from app.ml.preprocessing import load_and_clean


def train_and_save():
    print("Loading and cleaning data...")
    X, y, feature_names, drug_names, scaler = load_and_clean()
    print(f"Dataset: {X.shape[0]} samples, {X.shape[1]} features, {y.shape[1]} drugs")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"Train: {X_train.shape[0]}, Test: {X_test.shape[0]}")

    print("\nTraining MultiOutput RandomForest...")
    model = MultiOutputClassifier(
        RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("\n" + "=" * 60)
    print("PER-DRUG CLASSIFICATION REPORTS")
    print("=" * 60)
    for i, drug in enumerate(drug_names):
        print(f"\n--- {drug} ({config.DRUG_DISPLAY_NAMES.get(drug, drug)}) ---")
        print(classification_report(
            y_test[:, i], y_pred[:, i],
            target_names=["S (Sensitive)", "R (Resistant)"],
            zero_division=0
        ))

    os.makedirs(config.DATA_MODELS, exist_ok=True)
    joblib.dump(model, os.path.join(config.DATA_MODELS, "multi_rf_model.pkl"))
    joblib.dump(scaler, os.path.join(config.DATA_MODELS, "scaler.pkl"))
    joblib.dump(feature_names, os.path.join(config.DATA_MODELS, "feature_names.pkl"))
    joblib.dump(drug_names, os.path.join(config.DATA_MODELS, "drug_names.pkl"))

    print("\n" + "=" * 60)
    print(f"Model saved to {config.DATA_MODELS}")
    print("Files: multi_rf_model.pkl, scaler.pkl, feature_names.pkl, drug_names.pkl")
    return model, scaler


if __name__ == "__main__":
    train_and_save()
