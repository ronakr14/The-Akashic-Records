---
id: sias928rmwgiei076od9lsm
title: Basics
desc: ''
updated: 1756135148325
created: 1756135070990
---
## 🔑 Key Takeaways: From Basic NN → Specialized Architectures

| Architecture | Data Type       | How it Extends Basic NN                 | Forward Pass                       | Backprop                                 |
| ------------ | --------------- | --------------------------------------- | ---------------------------------- | ---------------------------------------- |
| FNN / MLP    | Tabular         | Fully connected neurons                 | Sum + activation                   | Standard chain rule                      |
| CNN          | Images          | Local receptive fields + weight sharing | Convolution + pooling + activation | Chain rule through conv filters          |
| RNN / LSTM   | Sequences       | Hidden state carries memory             | Sequential state update            | Backprop Through Time                    |
| Transformer  | Sequences / NLP | Attention → model token relationships   | Attention + feedforward            | Chain rule through attention + residuals |


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
|                  |                       |                           |                           |
