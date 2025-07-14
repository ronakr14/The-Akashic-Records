---
id: htc4o4ss3x2klof0yvq2dc6
title: Cheatsheets
desc: ''
updated: 1752506756278
created: 1752506753399
---

## 🧾 Cheat Sheets

* **PyTorch Training Loop**:

```python
for epoch in range(epochs):
    for inputs, labels in dataloader:
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
```

* **CNN Layer Example**:

```python
nn.Conv2d(3, 16, kernel_size=3, stride=1, padding=1)
nn.ReLU()
nn.MaxPool2d(2)
```

* **Transformer Quick Build (Hugging Face)**:

```python
from transformers import BertForSequenceClassification, Trainer
model = BertForSequenceClassification.from_pretrained("bert-base-uncased")
trainer = Trainer(model=model, ...)
trainer.train()
```

* **Model Serving via TorchServe**:

```bash
torch-model-archiver --model-name resnet50 --version 1.0 --serialized-file model.pth --handler image_classifier
torchserve --start --ncs --model-store model_store --models resnet50=resnet50.mar
```
