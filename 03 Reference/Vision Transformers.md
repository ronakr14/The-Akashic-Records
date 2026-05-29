
* **Goal:** Process images using Transformer-style attention instead of convolutions.
* **How it works:**

  * Split image into patches → flatten → linear embedding
  * Add positional embeddings → preserve patch order
  * Feed through Transformer layers (self-attention + feedforward)
* **Why it matters:**

  * Captures long-range dependencies in images
  * Competitive with CNNs on large datasets


# Vision Transformers

Best use case:  
State-of-the-art image understanding (classification, detection, segmentation) using attention—strong for large-scale, high-accuracy vision tasks.

Alternative: — **CNNs (e.g., ResNet)** (better for smaller datasets and lower compute constraints)
