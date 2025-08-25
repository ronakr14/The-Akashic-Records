---
id: sias928rmwgiei076od9lsm
title: Basics
desc: ''
updated: 1756135148325
created: 1756135070990
---

# 🌉 From Basic NN to Specialized Deep Learning Architectures

---

## 1️⃣ CNNs (Convolutional Neural Networks) — Images & Spatial Data

**Problem with FNNs on images:**

* Flattening an image destroys spatial structure.
* A 224×224 RGB image = 150,528 inputs → huge, redundant, inefficient.

**The CNN Solution:**

* Replace fully connected neurons with **convolutional neurons**: each neuron looks at a small patch of the image (receptive field).
* **Filters/Kernels** slide across the image → detect local patterns (edges, textures).
* Stacking layers → detect higher-level features (shapes → objects).

**Forward Pass:**

1. Convolution → feature map
2. Activation (ReLU)
3. Pooling → downsample spatially
4. Repeat → final layers flatten → fully connected → prediction

**Backpropagation:**

* Still works via chain rule
* Gradients now flow through convolutions → update filters
* Network learns **which features are important in local patches**

**Intuition:**

* Neurons aren’t fully connected to all pixels, they specialize locally
* Weight sharing → fewer parameters, faster learning

---

## 2️⃣ RNNs (Recurrent Neural Networks) — Sequential Data

**Problem with FNNs on sequences:**

* Input must be fixed-length → can’t remember past context
* No notion of temporal order

**The RNN Solution:**

* Each neuron has **hidden state** that carries memory from previous time steps
* Forward pass:

  $$
  h_t = f(W_x x_t + W_h h_{t-1} + b)
  $$

  * $x_t$ = input at time t
  * $h_{t-1}$ = previous hidden state
  * f = activation (tanh/ReLU)

**Backpropagation:**

* **Backprop Through Time (BPTT)**
* Gradients flow along both layers and time steps
* Handles sequential dependencies

**Variants:**

* LSTM → solves vanishing gradient
* GRU → simpler, faster

**Intuition:**

* Neurons now **remember past information** → perfect for time-series, text, or speech

---

## 3️⃣ Transformers — Sequences with Attention

**Problem with RNNs:**

* Sequential → slow, cannot parallelize
* Hard to capture long-range dependencies

**The Transformer Solution:**

* Remove recurrence → use **attention mechanism**
* Forward pass:

  1. Encode input sequence into embeddings
  2. Compute attention: how much each token should “look at” other tokens

     $$
     \text{Attention}(Q,K,V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right) V
     $$
  3. Pass through feedforward layers
  4. Repeat in stacked layers

**Backpropagation:**

* Same principle: chain rule
* Gradients flow through attention, feedforward layers, and residual connections

**Intuition:**

* Neurons now “vote” about **relationships between all tokens**
* Captures long-range dependencies efficiently
* Basis for GPT, BERT, and modern NLP models

---

## 🔑 Key Takeaways: From Basic NN → Specialized Architectures

| Architecture | Data Type       | How it Extends Basic NN                 | Forward Pass                       | Backprop                                 |
| ------------ | --------------- | --------------------------------------- | ---------------------------------- | ---------------------------------------- |
| FNN / MLP    | Tabular         | Fully connected neurons                 | Sum + activation                   | Standard chain rule                      |
| CNN          | Images          | Local receptive fields + weight sharing | Convolution + pooling + activation | Chain rule through conv filters          |
| RNN / LSTM   | Sequences       | Hidden state carries memory             | Sequential state update            | Backprop Through Time                    |
| Transformer  | Sequences / NLP | Attention → model token relationships   | Attention + feedforward            | Chain rule through attention + residuals |

---

### ⚡ Mental Model

* Basic neuron = “weighted vote + activation”
* CNN neuron = “weighted vote on local patch”
* RNN neuron = “weighted vote + memory of past votes”
* Transformer neuron = “weighted vote with attention to all other neurons in the sequence”

Essentially, **the core NN machinery (weighted sum + activation + backprop) stays the same**, we just **change connectivity patterns and how neurons see the data**.

---

