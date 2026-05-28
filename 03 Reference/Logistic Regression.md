---
id: ppbwa1bi2k8j6kb3z3cey9s
title: Logisticregression Decisiontrees
desc: ''
updated: 1756134518901
created: 1756134455864
---

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

# 🌳 Decision Trees – Math Intuition

### 🔹 The Problem

We want a model that predicts outcomes by asking **a sequence of yes/no questions**.

---

### 🔹 The Trick

Trees split data by feature thresholds to make groups as “pure” as possible.

Example: Loan Approval

```
IF income > 80K → Approve
ELSE IF credit_score > 700 → Approve
ELSE → Reject
```

---

### 🔹 How the Splits Are Chosen

At each node, the algorithm asks: **“Which feature split reduces uncertainty the most?”**

Uncertainty = how mixed the classes are.

Metrics used:

* **Gini Impurity**:

$$
Gini = 1 - \sum p_i^2
$$

(where $p_i$ = proportion of class i in the node)

* **Entropy (Information Gain)**:

$$
Entropy = -\sum p_i \log(p_i)
$$

👉 Lower impurity/entropy = purer groups.

---

### 🔹 Growing the Tree

1. Start with all data at the root.
2. Pick the feature & threshold that gives max information gain.
3. Split into branches.
4. Repeat until stopping conditions (depth limit, min samples, purity reached).

---

### 🔹 Predictions

* For regression → predict mean of values in the leaf.
* For classification → predict majority class in the leaf.

---

### 🔹 Intuition

Decision Trees are just **a greedy algorithm** trying to cut the dataset into pure buckets step by step.

---

### 🏆 Why Decision Trees Are Awesome

* Interpretable (“if-else” rules).
* Handle non-linear relationships naturally.
* Work with both numerical and categorical data.

But:

* High variance → can overfit easily.
* That’s why we combine them (Random Forest, Gradient Boosting).

---

# 🔑 Logistic Regression vs Decision Trees

| Feature                 | Logistic Regression        | Decision Tree               |
| ----------------------- | -------------------------- | --------------------------- |
| Interpretability        | Coefficients show impact   | Rules are intuitive         |
| Handles Non-Linearity   | No (needs transformations) | Yes                         |
| Overfitting Risk        | Low (with regularization)  | High                        |
| Feature Scaling Needed? | Yes                        | No                          |
| Common Uses             | Finance, healthcare, text  | Risk models, churn, tabular |

---

