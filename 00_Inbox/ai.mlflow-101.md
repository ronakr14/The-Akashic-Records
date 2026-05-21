---
id: 8mxjddxozr6fkfu7sxreuzr
title: Mlflow 101
desc: ''
updated: 1756135284074
created: 1756135275697
---

# 🧠 MLflow 101 – Managing ML/DL Experiments & Pipelines

---

## 1️⃣ **What is MLflow?**

MLflow is an **open-source platform** for managing the **end-to-end ML lifecycle**. Think of it as your:

* Experiment tracker
* Model version control system
* Deployment manager

All in one place.

It has **four main components**:

---

## 2️⃣ **MLflow Components**

| Component          | Purpose                                         | How it Helps                                          |
| ------------------ | ----------------------------------------------- | ----------------------------------------------------- |
| **Tracking**       | Log experiments, parameters, metrics, artifacts | Compare models, tune hyperparameters, keep history    |
| **Projects**       | Package code & dependencies                     | Reproducible ML projects, shareable across teams      |
| **Models**         | Save and version models in a standard format    | Deploy anywhere: REST API, cloud, batch               |
| **Model Registry** | Centralized model store                         | Versioning, staging, production management, approvals |

💡 Analogy:

* Tracking = your notebook with experiments
* Projects = your containerized code
* Models = your artifacts ready for deployment
* Registry = your “production shelf” for models

---

## 3️⃣ **MLflow Tracking in Action**

Typical ML workflow:

1. Train a model:

```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier

with mlflow.start_run():
    clf = RandomForestClassifier(n_estimators=100)
    clf.fit(X_train, y_train)
    
    # Log parameters
    mlflow.log_param("n_estimators", 100)
    
    # Log metrics
    accuracy = clf.score(X_test, y_test)
    mlflow.log_metric("accuracy", accuracy)
    
    # Log model
    mlflow.sklearn.log_model(clf, "rf_model")
```

* Every run is **tracked automatically** in MLflow UI
* Compare multiple runs → choose the best model easily

---

## 4️⃣ **MLflow Projects**

* Package ML code in a **standard format** (`MLproject` file)
* Define:

  * Conda / pip environment
  * Entry points (scripts)

```yaml
name: my_project
conda_env: conda.yaml
entry_points:
  main:
    parameters:
      n_estimators: {type: int, default: 100}
    command: "python train.py --n_estimators {n_estimators}"
```

💡 Benefit: reproducible experiments and **team collaboration**

---

## 5️⃣ **MLflow Models & Registry**

* Once trained, models can be **saved in a standard format**:

  * `mlflow.sklearn`, `mlflow.tensorflow`, `mlflow.pytorch`
* Deploy to:

  * REST API via MLflow server
  * Cloud / batch predictions
* Registry allows:

  * Version control
  * Stage management (`Staging`, `Production`)
  * Annotations & approval workflows

---

## 6️⃣ **Why MLflow Matters in Production**

* **Experiment reproducibility** → no more “it worked on my machine”
* **Centralized model tracking** → easier audits and team collaboration
* **Seamless deployment** → move from notebook → production REST endpoint
* **Supports all frameworks** → scikit-learn, TensorFlow, PyTorch, XGBoost

---

## 7️⃣ **Integration with DL Pipelines**

* Use MLflow to **track hyperparameters, losses, metrics** in CNN, RNN, Transformer training
* Log **artifacts**: checkpoints, images, embeddings, plots
* Compare models visually in the UI → pick the best for deployment

💡 Example:

* Train ResNet for image classification → log: learning rate, batch size, epochs, accuracy, confusion matrix, model weights
* Later, switch to EfficientNet → easily compare performance

---

## ⚡ TL;DR

* MLflow = **tracking + packaging + versioning + deployment**
* It **bridges research → production**, so your ML/DL experiments don’t die in Jupyter notebooks
* Works for **classic ML, deep learning, and hybrid pipelines**

---
