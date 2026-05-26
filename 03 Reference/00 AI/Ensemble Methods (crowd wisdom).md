
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