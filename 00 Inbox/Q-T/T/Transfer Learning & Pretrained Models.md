* **Why it matters:** Training large models from scratch is expensive.
* **Feature extraction:** Use pretrained layers as fixed feature generators.
* **Fine-tuning:** Retrain some/all layers on your domain-specific dataset.
* **Model distillation:** Compress large models into smaller, deployable versions.

**Practical:** HuggingFace Transformers for NLP, ResNet/EfficientNet for images.

# Transfer Learning & Pretrained Models

Best use case:  
Leverage pretrained models to fine-tune on small/medium datasets—cuts training time and boosts performance quickly.

Alternative: — **Training from scratch** (better when domain is highly unique or large proprietary data is available)
