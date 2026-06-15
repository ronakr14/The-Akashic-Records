
### 3. **Time-Series Models (Classic)**

Deep learning dominates now, but these still rule in industry:

* **ARIMA/SARIMA** → statistical models for forecasting (stock prices, sales).
* **Prophet (Facebook)** → easy time-series forecasting with seasonality/holidays.
* **Lag features + XGBoost** → often outperforms RNNs in production.
# Time Series

Best use case:  
Forecasting and trend analysis over temporal data (e.g., demand prediction, anomaly detection in metrics/logs).

Alternative: — **XGBoost** (better when you can engineer lag features and want strong tabular performance without specialized TS models)

# ⏳ Time Series Models (Forecasting)

### 🔹 The Problem

* Predict future values based on historical trends.
* Examples: stock price forecasting, demand prediction, server load monitoring.

---

### 🔹 Classic Approaches

1. **ARIMA (AutoRegressive Integrated Moving Average)**

   * Combines:

     * **AR** → predict using past values.
     * **I** → difference data to remove trends.
     * **MA** → use past forecast errors.
   * Example: predict tomorrow’s stock price from past 7 days + error correction.
   * Weakness: assumes linear relationships.

2. **SARIMA (Seasonal ARIMA)**

   * Extends ARIMA with seasonality (e.g., daily, monthly patterns).
   * Example: energy demand (peaks every morning & evening).

3. **Facebook Prophet**

   * Designed for business time series.
   * Handles seasonality, holidays, trends automatically.
   * Very interpretable.
   * Widely used in BI dashboards (forecasting sales, revenue).

4. **Machine Learning on Time-Series**

   * Feature engineering: lag features, rolling averages, time-of-day.
   * Feed into XGBoost/Random Forest.
   * Often beats ARIMA in real-world noisy datasets.
