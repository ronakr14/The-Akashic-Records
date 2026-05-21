---
id: 7ncui10gj8mvc682x40dcqn
title: Additional
desc: ''
updated: 1756134653486
created: 1756134647223
---

# 🧰 Remaining Key Concepts in ML Before Deep Learning

### 1. **Feature Engineering & Data Processing**

Not a single algorithm, but a **core ML skill**:

* Handling missing values.
* Encoding categorical variables (one-hot, embeddings, target encoding).
* Scaling numerical features (StandardScaler, MinMax).
* Feature crosses (e.g., Age × Income).
* Feature selection (Lasso, mutual information).

⚡ In tabular ML, *feature engineering matters more than the algorithm.*

---

### 2. **Anomaly Detection**

Useful when labels are scarce or imbalance is huge.

* **Isolation Forest** → isolates anomalies by random splits.
* **One-Class SVM** → learns a frontier around “normal” points.
* Applications: fraud detection, intrusion detection, predictive maintenance.

---

### 3. **Time-Series Models (Classic)**

Deep learning dominates now, but these still rule in industry:

* **ARIMA/SARIMA** → statistical models for forecasting (stock prices, sales).
* **Prophet (Facebook)** → easy time-series forecasting with seasonality/holidays.
* **Lag features + XGBoost** → often outperforms RNNs in production.

---

### 4. **Probabilistic Models & Bayesian ML**

* **Gaussian Mixture Models (GMMs)** → clustering with soft assignments.
* **Hidden Markov Models (HMMs)** → sequence modeling (speech, POS tagging, before RNNs took over).
* **Bayesian Networks** → represent probabilistic dependencies.
* **Bayesian Optimization** → used for hyperparameter tuning.

---

### 5. **Semi-Supervised & Weak Supervision**

* Often you have **lots of unlabeled data, few labels**.
* Algorithms: self-training, label propagation.
* Real-world: medical imaging (labels are expensive).

---

### 6. **Evaluation & Validation Tricks**

* **Cross-validation (k-fold)** → robust way to evaluate models.
* **Handling imbalanced data** → SMOTE (synthetic minority oversampling), weighted loss functions.
* **Learning curves** → to diagnose under/overfitting.

---

# 🏆 TL;DR — What’s Left in Classic ML?

* Core algorithms: ✅ (regression, trees, ensembles, SVMs, clustering, PCA).
* Extra flavors still worth knowing:

  * **Anomaly detection**
  * **Time series**
  * **Probabilistic models**
  * **Feature engineering** (the secret sauce in production ML)

---
