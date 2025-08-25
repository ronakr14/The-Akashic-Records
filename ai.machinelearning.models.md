---
id: la1wcsfkgdpme31l10q1yn0
title: Models
desc: ''
updated: 1756134342881
created: 1756134336539
---

# 🧰 Core Machine Learning Algorithms (Detailed but digestible)

---

## 🔹 1. **Regression Algorithms (predicting numbers)**

Goal → predict **continuous values**.
Examples: house prices, temperature, stock prices.

* **Linear Regression**

  * Fits a straight line: $y = mx + c$.
  * Works if data is linearly correlated.
  * Weakness: breaks when relationships are non-linear.

* **Polynomial Regression**

  * Extends linear regression with non-linear curves.
  * Risk: easily overfits if degree is too high.

* **Regularized Regression**

  * Adds penalties to avoid overfitting.
  * **Ridge (L2 penalty)** → shrinks coefficients smoothly.
  * **Lasso (L1 penalty)** → can shrink some coefficients to zero (feature selection).
  * **ElasticNet** → combo of both.

👉 Think of regression as the “Excel line of best fit,” but smarter.

---

## 🔹 2. **Classification Algorithms (predicting categories)**

Goal → predict **discrete labels**.
Examples: spam vs. not spam, churn vs. retain, fraud vs. legit.

* **Logistic Regression**

  * Despite the name, it’s for classification.
  * Outputs probabilities using the **sigmoid function**.
  * Great baseline algorithm.

* **k-Nearest Neighbors (kNN)**

  * “Birds of a feather flock together.”
  * Classifies based on the majority label of nearest data points.
  * Simple, but slow on large datasets.

* **Naive Bayes**

  * Based on Bayes’ Theorem.
  * “Naive” because it assumes features are independent.
  * Works shockingly well for **text classification** (spam filters, sentiment).

* **Support Vector Machines (SVM)**

  * Finds the **best hyperplane** to separate classes.
  * Uses **kernel trick** to handle non-linear data.
  * Powerful, but doesn’t scale well to massive datasets.

---

## 🔹 3. **Decision Trees**

Goal → split data into decision rules like a flowchart.

* Intuitive and interpretable.
* Example:

  ```
  IF income > 80K AND credit_score > 700 → Approve loan
  ELSE → Reject
  ```
* Weakness: can overfit (memorize training data).

---

## 🔹 4. **Ensemble Methods (crowd wisdom)**

Instead of relying on one weak model, combine many to build a strong predictor.

* **Bagging (Bootstrap Aggregating)**

  * Train multiple models on random subsets of data.
  * Average predictions (for regression) or majority vote (for classification).
  * Example: **Random Forest** (many decision trees).

* **Boosting**

  * Train models sequentially, each focusing on fixing errors of the previous.
  * Examples:

    * **AdaBoost** → assigns weights to misclassified data points.
    * **Gradient Boosting Machines (GBM)** → optimizes with gradient descent.
    * **XGBoost / LightGBM / CatBoost** → faster, more efficient, state-of-the-art for tabular data.

* **Stacking**

  * Train multiple models and then feed their outputs into a “meta-model.”
  * Example: logistic regression combining predictions from RF + SVM + XGBoost.

👉 In Kaggle competitions, **Boosting + Ensembles = gold medal recipe**.

---

## 🔹 5. **Clustering (unsupervised)**

Goal → group similar items without labels.

* **k-Means Clustering**

  * Divides data into $k$ clusters by minimizing distances to cluster centroids.
  * Simple but needs $k$ predefined.

* **Hierarchical Clustering**

  * Builds a tree of clusters (dendrogram).
  * Useful when you don’t know the number of clusters.

* **DBSCAN**

  * Groups based on density.
  * Great for arbitrary shapes, and can detect noise/outliers.

---

## 🔹 6. **Dimensionality Reduction**

When you’ve got **too many features**, reduce them while preserving structure.

* **PCA (Principal Component Analysis)** → projects data into fewer dimensions.
* **t-SNE / UMAP** → used for visualization of high-dimensional data.

---

## 🔹 7. **Recommendation Systems**

Special beast, but super important in industry.

* **Collaborative Filtering** → “users who liked X also liked Y.”
* **Content-Based Filtering** → based on item features (e.g., movie genres).
* **Hybrid Systems** → combine both.

---

# ⚖️ When to Use What?

* Predicting numbers → **Regression**
* Predicting categories → **Classification**
* Finding patterns/groups → **Clustering**
* Reducing noise/complexity → **Dimensionality Reduction**
* Tabular data with complex patterns → **Ensembles (XGBoost/LightGBM)**
* Text data → **Naive Bayes, Logistic Regression, Transformers (later)**
* Images → **Deep Learning (later)**

---
