High-accuracy modeling on tabular data by sequentially correcting errors (ranking, fraud, churn) using Gradient Boosting.

Alternative: — [[Random Forest]] if you need faster training and less sensitivity to hyperparameters


### 🔹 The Big Idea

Instead of training **one big model**, gradient boosting builds **a sequence of weak learners (usually shallow decision trees)**, each one fixing the mistakes of the last.

It’s like:

* Model 1: “I’ll make some predictions.”
* Model 2: “Cool, I’ll fix where you messed up.”
* Model 3: “I’ll fix both of your screwups.”
* … and so on.

At the end, you add them up = strong model.

---

### 🔹 Step 1: Define the Loss Function

Every supervised ML model needs a **loss function** to measure errors.

* Regression → Mean Squared Error (MSE).
* Classification → Log Loss (cross-entropy).

Say we’re doing regression:

$$
L(y, \hat{y}) = (y - \hat{y})^2
$$

Where:

* $y$ = true value
* $\hat{y}$ = prediction

---

### 🔹 Step 2: Start with a Weak Model

Start with a **simple guess**. In regression, a good first guess is the **mean of all target values**.

$$
\hat{y}_0 = \text{mean}(y)
$$

---

### 🔹 Step 3: Compute the Residuals

Residuals = the errors (what we still need to fix).

$$
r_i = y_i - \hat{y}_i
$$

Example:

* True house price = 500K
* Prediction = 450K
* Residual = +50K → “we under-predicted by 50K.”

---

### 🔹 Step 4: Fit a Tree on the Residuals

Train a **small decision tree** to predict those residuals.

* If residual is consistently positive in some region, tree learns to bump predictions up.
* If residual is negative, tree learns to pull predictions down.

This tree = a **correction model**.

---

### 🔹 Step 5: Update the Predictions

Now we update our prediction by adding the tree’s correction.

$$
\hat{y}_{new} = \hat{y}_{old} + \eta \cdot f(x)
$$

Where:

* $f(x)$ = new tree’s predictions (correction).
* $\eta$ = learning rate (controls step size).

---

### 🔹 Step 6: Repeat Until Convergence

Keep repeating:

1. Compute residuals (gradients).
2. Fit a new tree.
3. Update predictions.

Stop after N trees or when loss stops improving.

---

### 🔹 Why “Gradient” Boosting?

Because instead of just fitting on raw residuals, we use the **negative gradient of the loss function** as the target for the next tree.

* Residuals for squared error = same as gradients.
* For log loss (classification), gradients = probabilities vs. true labels.

That’s why GBM can optimize *any differentiable loss function*.

---

### 🔹 Visual Intuition

* Imagine throwing darts at a dartboard.
* First throw (weak model) lands far from bullseye.
* Each next throw (tree) doesn’t aim blindly—it corrects the error direction (gradient).
* After enough throws, you’re close to the bullseye (good predictions).

---

# 🏆 Why Gradient Boosting is a Beast

1. Handles **non-linearities** (trees split data flexibly).
2. Works with both regression & classification.
3. Less prone to overfitting than plain decision trees.
4. Tunable → learning rate, tree depth, number of trees.
5. With modern versions (XGBoost, LightGBM, CatBoost), it’s **fast and scalable**.

---

# ⚡ Real-World Example: Fraud Detection with GBM

* Dataset: millions of credit card transactions.
* First model: predicts average fraud probability (bad baseline).
* Residuals: captures subtle fraud patterns (e.g., weird time of purchase, unusual location).
* Each tree focuses on *hard-to-catch fraud cases*.
* Final model = ensemble of trees that detect fraud with **superhuman accuracy**.

---
