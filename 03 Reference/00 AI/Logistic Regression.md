---
id: ppbwa1bi2k8j6kb3z3cey9s
title: Logisticregression Decisiontrees
desc: ''
updated: 1756134518901
created: 1756134455864
---
# Logistic Regression

Best use case:  
Binary classification with interpretable coefficients (fraud detection, churn prediction) on structured data using Logistic Regression.

Alternative: — [[Random Forest]] if you need better performance on nonlinear relationships without heavy feature engineering

# 🧮 Logistic Regression – Math Intuition

### 🔹 The Problem

We want to predict a **binary outcome** (yes/no, spam/not spam, fraud/not fraud).

Linear regression doesn’t work because it can predict values like **-0.8** or **1.2** for probabilities 🤦. We need outputs between 0 and 1.

---

### 🔹 The Trick: Sigmoid Function

We take a linear combination of inputs, then squash it into the \[0,1] range with the **sigmoid**:

$$
p = \frac{1}{1 + e^{-(w_0 + w_1x_1 + w_2x_2 + ... + w_nx_n)}}
$$

Where:

* $p$ = probability (e.g., fraud = 0.8)
* $w_i$ = learned weights
* $x_i$ = features (transaction amount, location, etc.)

👉 Think: **linear regression, but curved into probability space**.

---

### 🔹 Decision Rule

* If $p > 0.5$ → predict class 1.
* Else → predict class 0.

---

### 🔹 Training (Maximum Likelihood)

Instead of minimizing squared error, logistic regression maximizes the probability of predicting the correct class.

Loss function = **Log Loss (Cross-Entropy)**:

$$
L = - \sum \big[ y \cdot \log(p) + (1-y) \cdot \log(1-p) \big]
$$

Gradient Descent updates the weights so that probabilities get closer to true labels.

---

### 🔹 Intuition

* Each feature weight $w_i$ tells you how strongly that feature pushes the probability toward class 1 or 0.
* Example:

  * If "transaction amount > \$5000" has a high positive weight → it strongly increases fraud probability.

---

### 🏆 Why Logistic Regression Still Rules

* Simple, interpretable, fast.
* Great for **finance, healthcare, and tabular data**.
* Baseline for almost every classification task.
* But: can’t handle non-linear boundaries well.

---
