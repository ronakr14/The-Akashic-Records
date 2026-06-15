Interpretable rule-based modeling for classification/regression on structured data with clear decision paths using Decision Trees.

Alternative: — [[Random Forest]] if you need better accuracy and generalization by reducing overfitting


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

