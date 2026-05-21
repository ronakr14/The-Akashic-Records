---
id: q4aeuc6zkjdwdhv1z6gl58x
title: Example
desc: ''
updated: 1756135320120
created: 1756135313075
---

# 🏗️ End-to-End MLflow Workflow (Tabular ML Example)

---

## **Step 0: Setup**

```bash
pip install mlflow scikit-learn pandas
mlflow ui  # Starts MLflow UI at http://localhost:5000
```

* MLflow UI will let you track experiments, metrics, artifacts, and models.

---

## **Step 1: Load & Prepare Data**

```python
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load dataset
data = load_breast_cancer()
X, y = data.data, data.target

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
```

---

## **Step 2: Train & Log Experiment with MLflow**

```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Start MLflow run
with mlflow.start_run() as run:
    
    # Define model
    n_estimators = 100
    clf = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
    
    # Train
    clf.fit(X_train, y_train)
    
    # Predict
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    
    # Log parameters, metrics, model
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_metric("accuracy", acc)
    mlflow.sklearn.log_model(clf, "random_forest_model")
    
    print(f"Run ID: {run.info.run_id} | Accuracy: {acc}")
```

✅ Now this experiment is **logged in MLflow UI**

* You can compare multiple runs by changing `n_estimators`, max depth, etc.
* Artifacts (models, plots, confusion matrices) are stored automatically.

---

## **Step 3: Model Registry (Versioning & Staging)**

```python
# Register the model
model_uri = f"runs:/{run.info.run_id}/random_forest_model"
model_details = mlflow.register_model(model_uri, "BreastCancerRF")

print(f"Registered model name: {model_details.name}, version: {model_details.version}")
```

* Once registered, you can move the model through stages: `Staging → Production`
* MLflow allows **approvals, annotations, and deployment tracking**

---

## **Step 4: Load Model from Registry for Deployment**

```python
# Load production model
loaded_model = mlflow.sklearn.load_model("models:/BreastCancerRF/Production")

# Make predictions
preds = loaded_model.predict(X_test)
print("Accuracy from production model:", accuracy_score(y_test, preds))
```

✅ This simulates **deployment inference**, where your model is now **serving predictions**.

---

## **Step 5: Optional – Convert Workflow for a CNN**

* Replace **RandomForestClassifier** with a CNN model (PyTorch or TensorFlow)
* Log hyperparameters: learning rate, batch size, epochs
* Log metrics: training/validation loss, accuracy, confusion matrix, sample predictions
* Log artifacts: model checkpoints, plots, sample images
* Deploy via MLflow Model serving (`mlflow models serve`) or export to cloud endpoint

💡 Notes:

* For CNNs, preprocessing steps include image resizing, augmentation, normalization.
* Training loop is similar: forward pass → compute loss → backward pass → update weights → log metrics.
* MLflow can handle **both classic ML and deep learning seamlessly**.

---

## **Step 6: Serve Model as REST API (Optional)**

```bash
mlflow models serve -m "models:/BreastCancerRF/Production" -p 1234
```

* Your model is now available via `http://localhost:1234/invocations`
* Send JSON payloads → get predictions in real-time

---

## ⚡ TL;DR Workflow

1. **Data** → Load & preprocess
2. **Training** → Train model & compute metrics
3. **MLflow Tracking** → Log parameters, metrics, artifacts, and model
4. **Model Registry** → Versioning, staging, approvals
5. **Deployment** → Load model from registry → real-time or batch inference

✅ With this workflow, you can manage **classic ML, CNNs, or even Transformers** in production without losing track of experiments.

---
