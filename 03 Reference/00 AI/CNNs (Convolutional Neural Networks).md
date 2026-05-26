

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