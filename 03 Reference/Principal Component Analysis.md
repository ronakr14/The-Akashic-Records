---
id: ht7mh1pahcx7hb84fedb7t3
title: Principalcomponentanalysis
desc: ''
updated: 1756134629018
created: 1756134621823
---

# 🔻 PCA (Principal Component Analysis) – Math & Geometry Intuition

---

## 🔹 The Problem

High-dimensional data is messy:

* Think of a dataset with 100 features (columns).
* Some are redundant (highly correlated).
* Some add noise.
* We want to **reduce dimensions** but still keep most of the “information.”

---

## 🔹 The Trick

PCA finds **new axes (directions) in feature space** that:

1. Capture the maximum variance (spread of data).
2. Are orthogonal (uncorrelated).

👉 Instead of describing data with old features, we describe it with **Principal Components** (PCs).

---

## 🔹 Step 1: Center the Data

Subtract the mean of each feature → move dataset to origin.

* Important because PCA cares about variance, not absolute values.

---

## 🔹 Step 2: Find Covariance Matrix

Covariance tells us how features move together.

$$
Cov(X) = \frac{1}{n-1} X^T X
$$

* Large covariance between two features = they carry redundant info.
* Example: “Height” and “Arm Length” → highly correlated.

---

## 🔹 Step 3: Eigenvectors & Eigenvalues

This is where linear algebra enters like a rockstar 🎸.

* Eigenvectors = **directions** of maximum variance.
* Eigenvalues = **how much variance** is captured in that direction.

We sort eigenvectors by eigenvalues:

* PC1 (1st component) → captures most variance.
* PC2 → next most variance, orthogonal to PC1.
* … and so on.

---

## 🔹 Step 4: Project Data

We take original data and project it onto top k eigenvectors.

$$
Z = X W_k
$$

Where:

* $X$ = centered data.
* $W_k$ = top k eigenvectors.
* $Z$ = reduced representation.

---

## 🔹 Intuition with Example

Imagine a 2D dataset (points scattered in an elongated ellipse).

* The biggest spread is along the ellipse’s major axis.
* PCA rotates the axes → aligns PC1 with that major axis, PC2 with the minor axis.
* If PC2 doesn’t carry much variance, we can drop it → dataset reduced from 2D → 1D while still preserving structure.

👉 In higher dimensions, PCA does the same but with linear algebra instead of eyeballs.

---

## 🔹 Variance Retained

We choose number of components k by checking **explained variance ratio**:

* Example: PC1 explains 70%, PC2 explains 20%, PC3 explains 5%.
* Using just first 2 PCs → 90% variance retained.

---

# 🏆 Real-World Applications of PCA

* **Data Compression** → reduce features without losing much information.
* **Visualization** → reducing 100D word embeddings into 2D for plotting.
* **Noise Filtering** → small-variance PCs often capture noise.
* **Finance** → analyze correlated stocks by reducing them into a few PCs (market vs. sector trends).
* **Image Compression** → represent images with fewer components.

---

# ⚡ Quick Visual Analogy

* Imagine 100 CCTV cameras filming the same event from slightly different angles.
* PCA says: “Most of what’s happening can be captured by just 2–3 best cameras (directions). Let’s drop the redundant ones.”

---

# 🔑 Related Dimensionality Reduction Methods

* **t-SNE / UMAP** → non-linear, great for visualization (cluster discovery).
* **Autoencoders (Deep Learning)** → neural nets learn compressed representations.
* PCA is linear & algebraic, t-SNE/UMAP are more about non-linear manifolds.

---



# Principal Component Analysis

Best use case:  
Dimensionality reduction for high-dimensional data (feature compression, noise reduction, visualization) using Principal Component Analysis.

Alternative: — t-SNE if you need better cluster visualization for complex, nonlinear structures
