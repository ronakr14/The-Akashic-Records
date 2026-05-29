#ai #model #training #deep-learning
Image and spatial data processing ([[classification]], [[detection]], [[segmentation]]) using Convolutional Neural Networks.

Alternative: — [[Vision Transformers]] if you need state-of-the-art performance and scalability on large datasets


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

