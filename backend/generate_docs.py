import json
import os

with open(r"c:\Users\chaitu_123\Downloads\AMR\AMR\backend\data\models\model_comparison.json") as f:
    data = json.load(f)

md = "# Model Evaluation Matrices\n\nThis document contains the detailed evaluation matrices (Accuracy, F1, Precision, Recall) for every drug class across every trained model.\n\n"
for m in [k for k in data.keys() if not k.startswith("_")]:
    md += f"## {data[m]['name']}\n\n| Drug | Accuracy (%) | F1-Score (%) | Precision (%) | Recall (%) |\n|---|---|---|---|---|\n"
    for drug, metrics in data[m]["per_drug"].items():
        md += f"| {drug} | {metrics['accuracy']:.2f} | {metrics['f1']:.2f} | {metrics['precision']:.2f} | {metrics['recall']:.2f} |\n"
    md += "\n"

os.makedirs(r"c:\Users\chaitu_123\Downloads\AMR\AMR\docs", exist_ok=True)
with open(r"c:\Users\chaitu_123\Downloads\AMR\AMR\docs\evaluation_matrices.md", "w", encoding="utf-8") as f:
    f.write(md)
    
print("Docs generated!")
