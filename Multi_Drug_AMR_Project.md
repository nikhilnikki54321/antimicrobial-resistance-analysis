# 🧬 Multi-Drug AMR Prediction System

## 📌 Problem Statement
Predict resistance (**S / R**) for **multiple drugs for a single microbe**.

---

## ✅ Approach 1: Multi-Label Prediction (Recommended)

Each drug is treated as a separate output.

### Example Dataset

| Microbe | Drug_A | Drug_B | Drug_C |
|--------|--------|--------|--------|
| E.coli | S      | R      | S      |

---

## 🔧 Implementation

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv("Bacteria_dataset_Multiresictance.csv")

# Convert S/R → 0/1
df.replace({'S': 0, 'R': 1}, inplace=True)

X = df.drop(['Drug_A','Drug_B','Drug_C'], axis=1)
y = df[['Drug_A','Drug_B','Drug_C']]

X_train, X_test, y_train, y_test = train_test_split(X, y)

model = MultiOutputClassifier(RandomForestClassifier())
model.fit(X_train, y_train)

pred = model.predict(X_test)
```

---

## 🎯 Output

Drug-wise predictions:
- Drug_A → S
- Drug_B → R
- Drug_C → S

---

## 🌐 Flask UI (Multi-Drug Input)

### HTML Form

```html
<form method="POST" action="/predict">
    <input type="text" name="feature1" placeholder="Feature 1"><br>

    <label>Select Drugs:</label><br>
    <input type="checkbox" name="drugs" value="Drug_A"> Drug A<br>
    <input type="checkbox" name="drugs" value="Drug_B"> Drug B<br>
    <input type="checkbox" name="drugs" value="Drug_C"> Drug C<br>

    <button type="submit">Predict</button>
</form>
```

---

### Flask Backend

```python
@app.route("/predict", methods=["POST"])
def predict():
    selected_drugs = request.form.getlist("drugs")

    input_vector = [0]*len(all_drugs)

    for d in selected_drugs:
        idx = all_drugs.index(d)
        input_vector[idx] = 1

    pred = model.predict([input_vector])

    result = {}
    for i, drug in enumerate(all_drugs):
        result[drug] = "R" if pred[0][i] == 1 else "S"

    return result
```

---

## 🧠 FT-Transformer (Multi-Output)

```python
import rtdl

model = rtdl.FTTransformer.make_default(
    n_num_features=X.shape[1],
    d_out=len(y.columns)
)
```

---

## 📊 Advanced Feature

### Best Drug Selection

```python
best_drug = min(result, key=lambda x: result[x])
```

---

## 🏁 Final Output Types

### Option 1
- Drug A → S  
- Drug B → R  

### Option 2
- Best Drug → Drug A  

---

## 🚀 Conclusion
- Supports multiple drugs per microbe  
- Uses ML + DL models  
- Deployable via Flask UI  
