import json
import os
import pandas as pd

def load_evaluation_matrices():
    """
    Loads and prints the evaluation matrices for every model trained.
    Includes the SHAP feature importance metric matrices.
    """
    json_path = os.path.join(os.path.dirname(__file__), "..", "backend", "data", "models", "model_comparison.json")
    
    if not os.path.exists(json_path):
        print(f"Error: Could not find model_comparison.json at {json_path}")
        return

    with open(json_path, "r") as f:
        data = json.load(f)

    # 1. Print Standard Evaluation Metrics
    for model_key, model_data in data.items():
        if model_key.startswith("_"):
            continue
            
        print(f"\n{'='*60}")
        print(f"Model: {model_data['name']}")
        print(f"{'='*60}")
        
        per_drug = model_data.get("per_drug", {})
        if not per_drug:
            print("No per-drug metrics available.")
            continue
            
        df = pd.DataFrame(per_drug).T
        df = df[['accuracy', 'f1', 'precision', 'recall']]
        df.index.name = 'Drug'
        
        print(df.to_markdown())
        print("\n")

    # 2. Print SHAP Evaluation Matrices
    if "_shap" in data:
        print(f"\n{'='*60}")
        print(f"SHAP Feature Importance Matrices (Best Model)")
        print(f"{'='*60}")
        
        for drug_name, shap_features in data["_shap"].items():
            print(f"\n--- SHAP Feature Importances for {drug_name} ---")
            df_shap = pd.DataFrame(shap_features)
            df_shap.index = df_shap.index + 1
            df_shap.index.name = 'Rank'
            print(df_shap.to_markdown())
            print("\n")

if __name__ == "__main__":
    load_evaluation_matrices()
