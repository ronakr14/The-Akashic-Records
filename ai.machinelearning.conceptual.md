---
id: g5s6ah4l5bc2vsbtobmgiiu
title: Conceptual
desc: ''
updated: 1756134750919
created: 1756134743180
---

# 🧠 Machine Learning Conceptual Map

---

## **1. Problem Types (First Fork in the Road)**

* **Supervised Learning** (labels exist → prediction tasks)

  * **Regression** → predict continuous values (house price, demand forecasting).
  * **Classification** → predict discrete labels (spam vs not spam, fraud vs legit).

* **Unsupervised Learning** (no labels → structure discovery)

  * **Clustering** → group similar items (customer segmentation).
  * **Dimensionality Reduction** → compress data, remove noise (PCA).

* **Semi-Supervised Learning**

  * Few labels + lots of unlabeled data (medical imaging).

* **Reinforcement Learning**

  * Learn by trial & error with rewards (games, robotics).

---

## **2. Core Algorithm Families**

### 🔹 **Linear Models** (simple, interpretable)

* Regression (Linear, Logistic).
* Pros: easy, fast, explainable.
* Cons: weak with complex data.

---

### 🔹 **Trees & Ensembles** (the workhorses of tabular data)

* Decision Trees → simple but overfit.
* Random Forest → bagging (stability, robustness).
* Gradient Boosting (XGBoost, LightGBM, CatBoost) → boosting (state-of-the-art for tabular).
* Pros: handle non-linearities, great real-world performance.
* Cons: black-boxy, tuning needed.

---

### 🔹 **Support Vector Machines (SVMs)** (geometry-driven)

* Max-margin classifiers.
* Kernels for non-linear separation.
* Pros: great in high-dim small data.
* Cons: slow on large datasets.

---

### 🔹 **Clustering & Unsupervised**

* k-Means → simple, centroid-based.
* Hierarchical clustering → tree of clusters.
* Gaussian Mixture Models (GMMs) → probabilistic clustering.
* PCA → compress + rotate data.
* t-SNE/UMAP → visualize complex data.

---

### 🔹 **Anomaly Detection**

* Isolation Forest → isolate outliers fast.
* One-Class SVM → frontier around normal points.
* Autoencoders → reconstruction error for anomalies.

---

### 🔹 **Time Series (Classic)**

* ARIMA/SARIMA → linear forecasting with trend + seasonality.
* Prophet → business-friendly forecasting.
* Feature engineering + XGBoost → often the production winner.

---

### 🔹 **Probabilistic & Bayesian**

* Hidden Markov Models (HMMs).
* Naive Bayes.
* Bayesian optimization for hyperparameter tuning.

---

## **3. Cross-Cutting Concerns**

* **Feature Engineering** → scaling, encoding, feature selection, feature crosses.
* **Validation** → train/test splits, cross-validation, learning curves.
* **Imbalanced Data Handling** → SMOTE, class weights.
* **Evaluation Metrics** → accuracy, precision/recall, ROC, RMSE, MAE.

---

## **4. Evolutionary Trajectory**

* **Old School Stats** → Linear/Logistic Regression, ARIMA.
* **Classical ML Boom** → Trees, Ensembles, SVMs, PCA, clustering.
* **Deep Learning Era** → Neural nets, CNNs, RNNs, Transformers.
* **Hybrid AI** → Combine ML + DL + domain-specific heuristics (modern production systems).

---

# ⚡ Visual Mental Map (Words Only)

Think of it like a **map of roads branching out**:

* Start at the root: **Do I have labels?**

  * **Yes → Supervised** → regression, classification → linear, trees, boosting, SVMs.
  * **No → Unsupervised** → clustering, dimensionality reduction.
  * **Few labels → Semi-supervised**.
  * **Sequential/interactive → Reinforcement/Time Series**.

On the side, always running parallel:
👉 Feature engineering, validation, metrics, anomaly detection.

---

# 🏆 TL;DR

Machine Learning = toolbox 🧰.

* **Linear models** = rulers (simple, interpretable).
* **Trees/Ensembles** = Swiss Army knife (flexible, strong on tabular data).
* **SVMs** = scalpel (precise, margin-based, works best on smaller high-dim data).
* **Unsupervised methods** = magnifying glass (see hidden patterns).
* **Anomaly detection** = metal detector (find rare weird stuff).
* **Time series** = clock (predict what happens next).

---

