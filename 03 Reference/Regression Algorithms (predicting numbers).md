
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
