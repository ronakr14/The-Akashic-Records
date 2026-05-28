
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