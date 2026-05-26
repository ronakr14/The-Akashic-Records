# 🧠 Neural Networks 101

A neural network is basically a **stack of function approximators**. At its core is the **artificial neuron**, inspired by the human brain.

---

## 1️⃣ The Artificial Neuron

* Inputs: $x_1, x_2, ..., x_n$
* Weights: $w_1, w_2, ..., w_n$ → tells importance of each input
* Bias: $b$ → allows shifting activation
* Activation function: $f(\cdot)$ → introduces non-linearity

**Equation:**

$$
y = f(w_1 x_1 + w_2 x_2 + ... + w_n x_n + b)
$$

💡 Intuition:

* Think of the neuron as **“weighted voting”** of its inputs.
* Activation = “should I fire or not?”

---

## 2️⃣ Activation Functions

Why not just use linear outputs?

* Without non-linearity → network collapses into a single linear function, no matter how deep.

Common activations:

| Function   | Equation                                | Intuition                                |
| ---------- | --------------------------------------- | ---------------------------------------- |
| Sigmoid    | $1 / (1 + e^{-x})$                      | Squashes to \[0,1], probabilistic output |
| Tanh       | $(e^x - e^{-x}) / (e^x + e^{-x})$       | \[-1,1], zero-centered                   |
| ReLU       | $max(0, x)$                             | Sparse activation, faster training       |
| Leaky ReLU | $x \text{ if } x>0 \text{ else } 0.01x$ | Avoids dead neurons                      |

💡 Rule of thumb:

* ReLU for hidden layers, Sigmoid for output if binary classification.

---

## 3️⃣ Forward Pass (Prediction)

1. Inputs → each neuron multiplies inputs by weights, adds bias.
2. Pass through activation → neuron “fires”
3. Outputs → feed to next layer
4. Repeat → until final layer produces predictions

💡 Intuition:

* Forward pass = **how the network transforms inputs into outputs**.

---

## 4️⃣ Loss Function

* Measures how far predictions $\hat{y}$ are from true labels $y$
* Common choices:

  * Regression → MSE: $(y - \hat{y})^2$
  * Classification → Cross-entropy

---

## 5️⃣ Backpropagation (Learning)

Goal: **update weights to reduce loss**

### Step 1: Compute Gradient

* Derivative of loss w\.r.t each weight → tells how changing that weight affects the loss

$$
\frac{\partial L}{\partial w} = ?
$$

* Done using **chain rule** from calculus

---

### Step 2: Weight Update (Gradient Descent)

$$
w := w - \eta \frac{\partial L}{\partial w}
$$

* $\eta$ = learning rate (step size)
* Repeat over all weights and all layers

💡 Intuition:

* Backprop = **blame assignment**

  * Which weights contributed to the error?
  * Adjust them slightly → next prediction is better

---

### Step 3: Iteration (Epochs)

* Forward pass → compute loss
* Backprop → adjust weights
* Repeat for many epochs until loss converges

---

## 6️⃣ Layers = Network Depth

* **Input layer** → raw features
* **Hidden layers** → feature extraction / representation learning
* **Output layer** → predictions

💡 Deeper networks = can learn **hierarchical features**

* Shallow → simple patterns
* Deep → complex patterns (edges → shapes → objects in images)

---

## 7️⃣ Intuition Example

Imagine predicting house price:

1. Input: size, location, bedrooms
2. Hidden layer: neurons detect patterns (e.g., “luxury location” or “big size”)
3. Next layer: combine features → “likely high price”
4. Output: predicted price

* Network “automatically learns” useful combinations of features instead of manual feature engineering

---

## ⚡ TL;DR – Neural Network Flow

1. **Neuron**: weighted sum + activation
2. **Forward Pass**: input → hidden layers → output
3. **Compute Loss**: compare prediction vs truth
4. **Backprop**: compute gradients → adjust weights
5. **Iterate**: until predictions are good

---

💡 **Rule of Thumb for Remembering Neural Nets:**

> “Forward = prediction, Backward = blame & adjust, Repeat until smart.”

---

