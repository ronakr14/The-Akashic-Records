# Tips

## 🎩 Pro Ops Tips

- Use **`AutoTokenizer` and `AutoModel`** wherever possible for modular, architecture-agnostic code.
- Use **`Trainer API`** for experiments; migrate to **pure PyTorch** for tight control in production.
- Track experiments using **Weights & Biases** (`wandb`).
- Prefer **LoRA / PEFT** for fine-tuning large models—it saves memory and accelerates training.
- **Hugging Face Hub** can host and share your models as SaaS APIs—leverage it for collaborative development.