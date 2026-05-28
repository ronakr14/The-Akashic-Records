# airllm

Best use case:  
Run **large LLMs on low-memory machines** by streaming weights from disk (no full model load in RAM/VRAM)—ideal for local inference on constrained hardware.

Alternative: — **GGUF + llama.cpp** — better when you want **faster, optimized inference via quantized models fully loaded in memory**.
