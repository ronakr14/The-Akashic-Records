---
id: 7a1wpmd46rw5aoxao31i7ow
title: Anomalydetectio
desc: ''
updated: 1756134694687
created: 1756134683355
---

# 🔍 Anomaly Detection (Outlier Detection)

### 🔹 The Problem

* Data often has **rare, abnormal cases**:

  * Fraudulent transactions
  * Machine sensor failures
  * Cyber attacks
* Challenge: **labels are scarce** (you don’t always know what anomalies look like).

---

### 🔹 Main Approaches

1. **Statistical Methods**

   * Assume “normal” data follows some distribution.
   * Flag points far from mean/median.
   * Example: z-score (>3 std devs away = anomaly).
   * Weakness: doesn’t work well if data isn’t nicely Gaussian.

2. **Distance-Based**

   * Idea: anomalies are far from neighbors.
   * **kNN-based anomaly detection** → compute distance to nearest neighbors, if it’s too large → anomaly.

3. **Isolation Forest (IForest)** 🌲

   * Randomly splits data into trees.
   * Normal points require more splits to isolate.
   * Anomalies get isolated quickly.
   * Lightweight and works well in high dimensions.

4. **One-Class SVM**

   * Learns a frontier around “normal” data.
   * Anything outside = anomaly.
   * Good for text, network intrusion detection.

5. **Autoencoders (DL sneak peek)**

   * Train a neural net to reconstruct input.
   * If reconstruction error is high → anomaly.
   * Used in image/video anomalies (e.g., CCTV defect detection).

---

### 🔹 Real-World Use Cases

* **Banking** → Fraud detection (IForest/XGBoost hybrid).
* **Manufacturing** → Detect faulty machine sensor readings.
* **Cybersecurity** → Detect intrusion attempts from unusual log patterns.

---

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

---

### 🔹 Advanced (Transition to DL)

* **RNN/LSTM/GRU** → capture sequential dependencies.
* **Temporal CNNs** → fast sequence modeling.
* **Transformers (Time-Series)** → newer models for long-range dependencies.

---

### 🔹 Real-World Use Cases

* **Retail** → Forecast demand to optimize inventory.
* **Finance** → Predict credit risk or stock price trends.
* **IT/DevOps** → Detect anomalies in server metrics (latency, error rates).
* **Energy** → Forecast electricity load, renewable generation.

---

# ⚡ TL;DR

* **Anomaly Detection** → Find the weird kids in the dataset.

  * Tools: Isolation Forest, One-Class SVM, Autoencoders.
* **Time Series** → Predict what happens next in ordered data.

  * Tools: ARIMA/SARIMA, Prophet, Feature-engineered XGBoost.

Both of these are **still used a ton in industry** because deep learning often needs way more data than you’ll realistically have.



### 2. **Anomaly Detection**

Useful when labels are scarce or imbalance is huge.

* **Isolation Forest** → isolates anomalies by random splits.
* **One-Class SVM** → learns a frontier around “normal” points.
* Applications: fraud detection, intrusion detection, predictive maintenance.