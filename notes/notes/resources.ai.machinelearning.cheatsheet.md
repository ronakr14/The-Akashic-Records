---
id: rih0vkqnyh34e6pdqp8byei
title: Cheatsheet
desc: ''
updated: 1752506586449
created: 1752506585841
---

## 🧾 Cheat Sheets

* **Scikit-Learn Pipeline**:

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('clf', RandomForestClassifier())
])

pipeline.fit(X_train, y_train)
predictions = pipeline.predict(X_test)
```

* **Evaluation Metrics Quick Guide**:
  \| Task             | Metric             |
  \|------------------|--------------------|
  \| Classification   | Accuracy, Precision, Recall, F1 |
  \| Imbalanced Data  | ROC AUC, Precision-Recall Curve |
  \| Regression       | MAE, RMSE, R² |

* **Model Serving (FastAPI)**:

```python
from fastapi import FastAPI
import joblib

app = FastAPI()
model = joblib.load("model.pkl")

@app.post("/predict/")
async def predict(data: dict):
    X = pd.DataFrame([data])
    pred = model.predict(X)[0]
    return {"prediction": pred}
```

* **MLflow Quick Start**:

```bash
mlflow ui
mlflow run .
mlflow models serve -m runs:/<run-id>/model
```
