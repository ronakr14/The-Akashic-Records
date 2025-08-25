---
id: 70uxp5qbmjgkfb31owo7mx2
title: Branches
desc: ''
updated: 1756135020887
created: 1756135015237
---

# 🧠 Deep Learning Menu Card

---

## 1️⃣ **Feedforward Neural Networks (FNN / MLP)**

* **AKA:** Multilayer Perceptrons
* **Input → hidden layers → output** (fully connected).
* **Use Cases:**

  * Tabular data (when trees aren’t enough)
  * Simple regression/classification tasks
* **Pros:**

  * Universal function approximator
  * Simple to understand
* **Cons:**

  * Doesn’t exploit spatial/temporal structure
  * Overfits easily on small data

---

## 2️⃣ **Convolutional Neural Networks (CNNs)**

* **Designed for:** Grid-like data (images, videos)
* **Key Idea:** Convolutions detect **local patterns** → hierarchical features

  * Early layers → edges, textures
  * Mid layers → shapes
  * Deep layers → objects
* **Use Cases:**

  * Image classification, object detection, segmentation
  * Video analysis
  * Medical imaging
* **Pros:** Parameter-efficient, exploits spatial structure
* **Cons:** Needs lots of labeled data

---

## 3️⃣ **Recurrent Neural Networks (RNNs)**

* **Designed for:** Sequential data
* **Key Idea:** Hidden state carries memory of past inputs → good for sequences
* **Variants:**

  * LSTM (Long Short-Term Memory) → solves vanishing gradients
  * GRU (Gated Recurrent Unit) → simpler, faster
* **Use Cases:**

  * Time-series forecasting
  * Language modeling, speech recognition
* **Pros:** Handles variable-length sequences
* **Cons:** Slow to train on long sequences

---

## 4️⃣ **Transformers**

* **Revolutionary for:** NLP, now general-purpose
* **Key Idea:** Attention mechanism → model relationships between all elements in sequence simultaneously
* **Use Cases:**

  * Machine translation (Google Translate)
  * Text generation (GPT, BERT)
  * Vision Transformers (ViT) for images
* **Pros:** Parallelizable, handles long-range dependencies
* **Cons:** Requires massive data and compute

---

## 5️⃣ **Autoencoders**

* **Purpose:** Unsupervised representation learning / dimensionality reduction
* **Structure:** Encoder → compressed latent space → Decoder → reconstruct input
* **Use Cases:**

  * Anomaly detection
  * Image denoising
  * Feature compression
* **Pros:** Learns compact representations
* **Cons:** Not predictive by default (need tweaks for supervised tasks)

---

## 6️⃣ **Generative Models**

* **GANs (Generative Adversarial Networks):**

  * Generator vs Discriminator → create realistic synthetic data
  * Use Cases: Image synthesis, data augmentation, deepfakes
* **VAEs (Variational Autoencoders):**

  * Probabilistic latent space → generate new samples
  * Use Cases: Image generation, anomaly detection

---

## 7️⃣ **Reinforcement Learning + Deep RL**

* **Goal:** Learn policies via trial & error (reward maximization)
* **Key DL Component:** Neural networks approximate value functions or policies
* **Use Cases:**

  * Games (AlphaGo, OpenAI Five)
  * Robotics / autonomous vehicles
  * Recommendation / dynamic pricing
* **Pros:** Learns sequential decision-making
* **Cons:** Data inefficient, training can be unstable

---

## ⚡ Quick Comparison Table

| Branch           | Best For              | Strength                  | Weakness                  |
| ---------------- | --------------------- | ------------------------- | ------------------------- |
| FNN / MLP        | Tabular, simple tasks | Universal approx          | Ignores structure         |
| CNN              | Images, spatial data  | Local pattern recognition | Needs lots of data        |
| RNN / LSTM / GRU | Sequences             | Memory of past            | Slow, vanishing gradients |
| Transformer      | NLP, sequences        | Long-range dependencies   | Massive compute           |
| Autoencoder      | Compression, anomaly  | Learn latent features     | Not predictive            |
| GAN / VAE        | Data generation       | Creative synthesis        | Hard to train             |
| Deep RL          | Decision-making       | Learn complex policies    | Data & compute hungry     |

---

# 🔑 Takeaways

* **Structured tabular data → MLP / classic ML often enough**
* **Images → CNNs dominate**
* **Sequences → RNNs historically, Transformers now state-of-the-art**
* **Dimensionality / anomalies → Autoencoders**
* **Generative creativity → GANs/VAEs**
* **Games/agents → Deep RL**

---

