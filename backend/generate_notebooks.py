import os
import nbformat
from nbformat.v4 import new_notebook, new_code_cell, new_markdown_cell

notebooks_dir = os.path.join("data", "notebooks")
os.makedirs(notebooks_dir, exist_ok=True)

models = ["random_forest", "xgboost", "lightgbm", "catboost", "extra_trees", "mlp", "svm", "ft_bilstm"]

setup_code = """import sys
import os
import joblib
import numpy as np
sys.path.insert(0, os.path.abspath("../.."))
sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath("."))
import config
from app.ml.preprocessing import load_and_clean
from app.ml.train_all_models import add_feature_engineering, predict_with_thresholds
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import shap
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = (8, 6)

print("Loading Data...")
X, y, feature_names, drug_names, scaler, microbe_cols = load_and_clean()
X = X.astype(np.float32)
X = add_feature_engineering(X)
X = X.astype(np.float32)
y = y.astype(np.float32)

all_feature_names = feature_names + [
    "age_x_diabetes", "age_x_hypertension", "age_x_hospital",
    "age_x_infection", "infection_x_hospital", "infection_x_diabetes",
    "diabetes_x_hypertension", "diabetes_x_hospital", "hypertension_x_hospital",
    "comorbidity_count", "risk_score", "age_squared", "infection_squared"
]

X_trainval, X_test, y_trainval, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_trainval, y_trainval, test_size=0.15, random_state=42)
print("Data Loaded Successfully.")
"""

for m in models:
    nb = new_notebook()
    
    nb.cells.append(new_markdown_cell(f"# Evaluation Report: {m.upper()}"))
    nb.cells.append(new_markdown_cell(f"This notebook loads the trained `{m}` model, evaluates it on the test dataset, and generates SHAP explainability visualisations."))
    nb.cells.append(new_code_cell(setup_code))
    
    eval_code = f"""print("Evaluating {m.upper()} Model...")
model_path = os.path.join(config.DATA_MODELS, "{m}_model.pkl")
thresh_path = os.path.join(config.DATA_MODELS, "{m}_thresholds.pkl")

if os.path.exists(model_path):
    model = joblib.load(model_path)
    thresholds = joblib.load(thresh_path)
    
    y_pred = predict_with_thresholds(model, X_test, thresholds)
    
    print("\\n### Classification Report ###\\n")
    report = classification_report(y_test, y_pred, target_names=drug_names, zero_division=0)
    print(report)
else:
    print(f"Model file for {m} not found at {{model_path}}")
"""
    nb.cells.append(new_code_cell(eval_code))
    
    shap_code = f"""import warnings
warnings.filterwarnings('ignore')

if "{m}" not in ["mlp", "svm", "ft_bilstm"]:
    print("\\n### SHAP Evaluation Matrix ###\\n")
    try:
        sample = X_test[:200]
        # Generate SHAP for a few top drugs to prevent enormous notebooks
        for i, (est, drug) in enumerate(zip(model.estimators_[:5], drug_names[:5])):
            print(f"\\n--- SHAP Feature Importance for {{drug}} ---")
            explainer = shap.TreeExplainer(est)
            shap_values = explainer.shap_values(sample)
            if isinstance(shap_values, list):
                sv = shap_values[1] if len(shap_values) > 1 else shap_values[0]
            else:
                sv = shap_values
                
            plt.figure(figsize=(10, 6))
            shap.summary_plot(sv, sample, feature_names=all_feature_names, show=False)
            plt.tight_layout()
            plt.show()
    except Exception as e:
        print("SHAP Computation failed:", e)
else:
    print("\\n### SHAP TreeExplainer Not Supported ###")
    print("Linear/Neural models are omitted from SHAP TreeExplainability in this automated pipeline.")
"""
    nb.cells.append(new_code_cell(shap_code))
    
    nb_path = os.path.join(notebooks_dir, f"{m}_evaluation.ipynb")
    with open(nb_path, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)
        
print("All notebook templates generated successfully in data/notebooks/")
