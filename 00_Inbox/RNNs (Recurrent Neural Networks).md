
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


 **Recurrent Neural Networks (RNNs)**

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