#ai #machine-learning #model-training
Identify rare or unexpected patterns in data (fraud, sensor faults, intrusion detection) using Anomaly Detection.

Alternative:  
1. [[Classification]] if you have labeled anomalies and need higher accuracy with supervised training

### 🔹 Main Approaches

1. **[[Statistical Methods]]**

   * Assume “normal” data follows some distribution.
   * Flag points far from mean/median.
   * Example: z-score (>3 std devs away = anomaly).
   * Weakness: doesn’t work well if data isn’t nicely Gaussian.

1. **[[Distance-Based]]**

   * Idea: anomalies are far from neighbors.
   * **[[kNN]]-based anomaly detection** → compute distance to nearest neighbors, if it’s too large → anomaly.

1. **[[Isolation Forest]] (IForest)** 🌲

   * Randomly splits data into trees.
   * Normal points require more splits to isolate.
   * Anomalies get isolated quickly.
   * Lightweight and works well in high dimensions.

1. **[[One-Class SVM]]**

   * Learns a frontier around “normal” data.
   * Anything outside = anomaly.
   * Good for text, network intrusion detection.

1. **[[Autoencoders]] (DL sneak peek)**

   * Train a neural net to reconstruct input.
   * If reconstruction error is high → anomaly.
   * Used in image/video anomalies (e.g., CCTV defect detection).