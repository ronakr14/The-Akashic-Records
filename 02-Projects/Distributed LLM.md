---
domain: ai
subdomain: distributed-inference
note_type: project
source_type: web
status: draft
level: advanced
---
# AI Summary

Home-lab plan for running one LLM split across several consumer laptops on a LAN using llama.cpp's RPC backend (host + `rpc-server` workers, GGUF models, tensor splitting, worker-side tensor cache). Covers network/firewall setup, a staged 8B → 70B scale-up with TTFT / tokens-per-second measurement at each step, and the key tradeoff: distributed inference (model doesn't fit) vs model replicas behind a gateway (throughput for parallel agents). Not started — pending actual laptop specs.

Related: [[LLM Serving & Inference]] · [[Distributed Llama]] · [[CrowdLlama]] · [[Hugging Face Accelerate]] · [[Distributed System]] · [[_AI MOC]]

---

# Setup guide (captured AI conversation)

Yes. Let's do the **first option properly: one LLM split across multiple laptops over your LAN**.

For a cheap/local setup, I recommend starting with **llama.cpp + its RPC backend**. It is open source, works with GGUF models, and its RPC mechanism is specifically intended to expose compute devices on other machines to a main llama.cpp process. The current RPC implementation can also cache large tensors locally on workers, and Linux systems with suitable RDMA hardware can use RDMA instead of TCP. ([GitHub](https://github.com/crc-org/llama.cpp/blob/main/tools/rpc/README.md "llama.cpp/tools/rpc/README.md at main · crc-org/llama.cpp · GitHub"))

The important caveat: **this is not magic pooled RAM**. You're distributing model computation across machines, and the network becomes part of your inference engine.

---

# 1. What we're building

Let's say you have:

```text
Laptop A
16 GB RAM
Intel/AMD CPU
2 GB GPU

Laptop B
16 GB RAM
Intel/AMD CPU
2 GB GPU

Laptop C
16 GB RAM
Intel/AMD CPU
2 GB GPU
```

We'll turn them into:

```text
                    LAN
                     │
                     │
              ┌──────▼──────┐
              │   Laptop A  │
              │    HOST     │
              │             │
              │ llama.cpp   │
              │ + RPC       │
              └──────┬──────┘
                     │
          ┌──────────┴──────────┐
          │                     │
          ▼                     ▼
 ┌────────────────┐     ┌────────────────┐
 │    Laptop B    │     │    Laptop C    │
 │     WORKER     │     │     WORKER     │
 │                │     │                │
 │ ggml-rpc-server│     │ ggml-rpc-server│
 │                │     │                │
 │ CPU/GPU        │     │ CPU/GPU        │
 └────────────────┘     └────────────────┘
```

The application talks only to Laptop A:

```text
Python
   │
   ▼
OpenAI-compatible llama.cpp server
   │
   ▼
Distributed model
   │
   ├── Laptop A
   ├── Laptop B
   └── Laptop C
```

That's the architecture I'd use.

---

# 2. First understand what is actually being distributed

Suppose you have:

```text
Llama 3.x 70B Q4
```

A rough model-weight requirement might be around:

```text
70B × ~4 bits
≈ 35 GB
```

plus quantization metadata, runtime memory, KV cache, buffers, etc.

A single:

```text
16 GB laptop
```

isn't going to comfortably host the whole thing.

But:

```text
Laptop A → 16 GB
Laptop B → 16 GB
Laptop C → 16 GB
```

gives the distributed system enough aggregate memory to potentially accommodate the model.

**However:**

```text
16 + 16 + 16 ≠ one 48 GB computer
```

The machines communicate over the network.

That's the fundamental tradeoff.

---

# 3. Use Ethernet if possible

This is probably the most important hardware recommendation.

Prefer:

```text
Laptop A
   │
   ├── 1 GbE
   │
Switch
   │
   ├── 1 GbE
   │
Laptop B
   │
   └── 1 GbE
       Laptop C
```

rather than:

```text
Laptop A ))))
          Wi-Fi
              ((( Laptop B
```

For experimentation, Wi-Fi can work.

For serious distributed inference:

**Ethernet.**

If you have 2.5GbE, even better.

---

# 4. Decide which laptop is the host

Pick the strongest machine.

For example:

```text
Laptop A
32 GB RAM
RTX 3050

Laptop B
16 GB RAM
integrated graphics

Laptop C
16 GB RAM
integrated graphics
```

I'd make A:

```text
HOST
```

and B/C:

```text
WORKERS
```

The host runs:

```text
llama.cpp
```

Workers run:

```text
ggml-rpc-server
```

The current llama.cpp RPC documentation explicitly supports exposing CUDA devices through `ggml-rpc-server`; the host is built with `GGML_RPC=ON`. ([GitHub](https://github.com/ggml-org/llama.cpp/blob/master/tools/rpc/README.md "llama.cpp/tools/rpc/README.md at master · ggml-org/llama.cpp · GitHub"))

---

# 5. Operating system

For your first experiment, I'd strongly recommend:

### Option A — Linux

Best choice.

Ubuntu 24.04 would be my pick.

```text
Laptop A → Ubuntu
Laptop B → Ubuntu
Laptop C → Ubuntu
```

### Option B — Windows

Also possible.

Since you're comfortable with Windows/Python, this is perfectly viable, but Linux will generally make the networking/build/debugging experience cleaner.

llama.cpp officially documents Windows builds through Visual Studio/CMake, and Linux builds through CMake. ([GitHub](https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md "llama.cpp/docs/build.md at master · ggml-org/llama.cpp · GitHub"))

### My recommendation

If the laptops are currently Windows:

**Don't wipe them immediately.**

Use:

```text
Windows
   │
   └── WSL2 Ubuntu
```

for the first prototype.

Once it works, you can decide whether a dedicated Linux installation is worthwhile.

---

# 6. Install llama.cpp

On the host:

```bash
git clone https://github.com/ggml-org/llama.cpp.git
cd llama.cpp
```

Build the basic CPU version:

```bash
cmake -B build
cmake --build build --config Release -j
```

llama.cpp's current build documentation uses CMake and supports backend-specific builds such as CUDA, Vulkan, etc. ([GitHub](https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md "llama.cpp/docs/build.md at master · ggml-org/llama.cpp · GitHub"))

You'll end up with binaries under something similar to:

```text
build/bin/
```

depending on platform/generator.

---

# 7. Build the RPC worker

This is where things get interesting.

On **Laptop B**:

```bash
git clone https://github.com/ggml-org/llama.cpp.git
cd llama.cpp
```

Build with RPC enabled:

```bash
cmake -B build \
    -DGGML_RPC=ON
```

Then:

```bash
cmake --build build --config Release -j
```

Do the same on Laptop C.

If your worker has an NVIDIA GPU, you can build CUDA + RPC:

```bash
cmake -B build \
    -DGGML_CUDA=ON \
    -DGGML_RPC=ON

cmake --build build --config Release -j
```

The llama.cpp RPC documentation gives this CUDA + RPC build pattern directly. ([GitHub](https://github.com/ggml-org/llama.cpp/blob/master/tools/rpc/README.md "llama.cpp/tools/rpc/README.md at master · ggml-org/llama.cpp · GitHub"))

---

# 8. Start the RPC server

On Laptop B:

```bash
./build/bin/ggml-rpc-server
```

You'll get something conceptually like:

```text
Starting RPC server
endpoint : 0.0.0.0:50052

Devices:
CPU: ...
```

For CUDA:

```text
Devices:

CUDA0:
NVIDIA ...
```

The RPC server listens on port:

```text
50052
```

by default in the current documentation. ([GitHub](https://github.com/ggml-org/llama.cpp/blob/master/tools/rpc/README.md "llama.cpp/tools/rpc/README.md at master · ggml-org/llama.cpp · GitHub"))

---

# 9. Find the worker's IP

On Laptop B:

```bash
ip addr
```

or:

```bash
hostname -I
```

Suppose:

```text
Laptop B = 192.168.1.102
```

Laptop C:

```text
192.168.1.103
```

Laptop A:

```text
192.168.1.101
```

So:

```text
HOST
192.168.1.101

WORKER
192.168.1.102:50052

WORKER
192.168.1.103:50052
```

---

# 10. Test network connectivity

From Laptop A:

```bash
ping 192.168.1.102
```

Then:

```bash
ping 192.168.1.103
```

You want:

```text
64 bytes from 192.168.1.102
64 bytes from 192.168.1.102
64 bytes from 192.168.1.102
```

Then test the RPC port:

```bash
nc -zv 192.168.1.102 50052
```

You want something like:

```text
Connection to 192.168.1.102 50052 port [tcp/*] succeeded
```

If this doesn't work, **don't proceed to the LLM yet**.

Fix networking first.

---

# 11. Firewall

This is a very common place to waste an afternoon.

On Linux, allow TCP:

```text
50052
```

For example with UFW:

```bash
sudo ufw allow from 192.168.1.0/24 to any port 50052 proto tcp
```

Obviously change the subnet to match your LAN.

Do **not** expose this RPC port to the public internet.

Your architecture should be:

```text
Internet
   X
   │
Router
   │
Private LAN
   │
   ├── Host
   ├── Worker
   └── Worker
```

not:

```text
Internet
   │
   ▼
RPC server
```

---

# 12. Enable RPC on the host

Now Laptop A needs an RPC-enabled llama.cpp build.

```bash
cmake -B build \
    -DGGML_RPC=ON

cmake --build build --config Release -j
```

If the host itself has an NVIDIA GPU:

```bash
cmake -B build \
    -DGGML_CUDA=ON \
    -DGGML_RPC=ON

cmake --build build --config Release -j
```

---

# 13. Download a GGUF model

Don't start with a 70B monster.

Seriously.

Start small.

I'd use something around:

```text
7B–14B
```

first.

Then:

```text
32B
```

Then potentially:

```text
70B+
```

The model needs to be in **GGUF** format for llama.cpp.

For example:

```text
model.gguf
```

Place it on the host.

For a first test:

```text
7B/8B Q4
```

is ideal.

You're testing the distributed infrastructure, not trying to win a benchmark on day one.

---

# 14. Start with ONE worker

Don't immediately configure:

```text
A → B → C → D → E
```

Start:

```text
A
│
└── B
```

Run RPC server on B:

```bash
./build/bin/ggml-rpc-server
```

Then configure A to use:

```text
192.168.1.102:50052
```

The RPC backend supports specifying RPC endpoints and can split tensor data across devices; the documentation also supports `--tensor-split` to control the proportions. ([GitHub](https://github.com/crc-org/llama.cpp/blob/main/tools/rpc/README.md "llama.cpp/tools/rpc/README.md at main · crc-org/llama.cpp · GitHub"))

---

# 15. Then add Laptop C

Once:

```text
A ↔ B
```

works:

```text
A
├── B
└── C
```

Worker B:

```text
192.168.1.102:50052
```

Worker C:

```text
192.168.1.103:50052
```

Now your distributed compute pool looks like:

```text
                 HOST
                  A
                  │
       ┌──────────┴──────────┐
       │                     │
       ▼                     ▼
      B:50052              C:50052
       │                     │
       ▼                     ▼
     CPU/GPU               CPU/GPU
```

---

# 16. Tensor splitting

This is one of the most important concepts.

Suppose you have:

```text
Host GPU
4 GB

Worker GPU
8 GB
```

You don't necessarily want:

```text
50%
50%
```

because the memory capacities aren't equal.

You might want something closer to:

```text
4 : 8
```

or:

```text
1 : 2
```

So:

```text
Host
33%

Worker
67%
```

llama.cpp exposes `--tensor-split` for specifying proportions across devices. ([GitHub](https://github.com/crc-org/llama.cpp/blob/main/tools/rpc/README.md "llama.cpp/tools/rpc/README.md at main · crc-org/llama.cpp · GitHub"))

The exact optimal split depends on the model, backend, memory available and whether you're using CPU/GPU combinations.

Don't blindly use equal splits.

---

# 17. Local cache

This is a feature you absolutely want.

The RPC server can maintain a local cache of large tensors.

Enable it with:

```bash
ggml-rpc-server -c
```

The documentation says the default cache is under:

```text
~/.cache/llama.cpp/rpc
```

and can be changed through `LLAMA_CACHE`. ([GitHub](https://github.com/crc-org/llama.cpp/blob/main/tools/rpc/README.md "llama.cpp/tools/rpc/README.md at main · crc-org/llama.cpp · GitHub"))

Why this matters:

Without caching:

```text
Host
 │
 ├── transfer tensor
 ├── transfer tensor
 ├── transfer tensor
 └── transfer tensor
```

again and again.

With caching:

```text
First run

Host ───────► Worker
              │
              ▼
            cache

Future runs

Host ───────► cached tensors
```

Much better.

---

# 18. The performance reality

This is where I want to kill a common misconception.

Suppose:

```text
Laptop A
16 GB

Laptop B
16 GB
```

You might think:

```text
32 GB
```

therefore:

```text
large model
+
fast inference
```

No.

You actually have:

```text
             ┌──────────────┐
             │ Laptop A     │
             │ compute      │
             └──────┬───────┘
                    │
                network
                    │
             ┌──────▼───────┐
             │ Laptop B     │
             │ compute      │
             └──────────────┘
```

Every synchronization crossing the network costs time.

Therefore:

```text
More memory
       ≠
More tokens/sec
```

The distributed architecture is mainly useful because:

> **The model fits when it otherwise wouldn't.**

That's the killer feature.

---

# 19. CPU vs GPU

Your 2 GB GPUs are unlikely to be transformative for large models.

You might actually find:

```text
CPU + large RAM
```

more useful than:

```text
2 GB GPU
```

for the first distributed experiment.

For example:

```text
Laptop A
16 GB RAM
CPU

Laptop B
16 GB RAM
CPU

Laptop C
16 GB RAM
CPU
```

can be more straightforward than trying to construct some Frankenstein:

```text
2 GB NVIDIA
+
2 GB AMD
+
Intel iGPU
+
CPU
```

Backend compatibility matters.

llama.cpp supports multiple hardware backends, including CUDA and Vulkan, but you need to build/use the appropriate backend for each machine. ([GitHub](https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md "llama.cpp/docs/build.md at master · ggml-org/llama.cpp · GitHub"))

---

# 20. Your first realistic experiment

I'd do this.

### Machine A

```text
16 GB RAM
CPU
```

### Machine B

```text
16 GB RAM
CPU
```

### Network

```text
1 Gb Ethernet
```

### Model

```text
8B Q4 GGUF
```

Then:

```text
A
│
│ RPC
▼
B
```

First prove:

```text
A can use B
```

Then:

```text
A
├── B
└── C
```

Then try:

```text
14B
```

Then:

```text
32B
```

Then see where the wheels come off.

That's the useful experiment.

---

# 21. Measure everything

Since you're a data engineer, don't just eyeball it.

Build a small benchmark:

```text
model
backend
workers
network
context
prompt_tokens
output_tokens
TTFT
tokens/sec
RAM
CPU
GPU
network bandwidth
```

Something like:

|Configuration|Model|Workers|tok/s|RAM|
|---|---|--:|--:|--:|
|Single|8B Q4|1|?|?|
|Distributed|8B Q4|2|?|?|
|Distributed|14B Q4|2|?|?|
|Distributed|32B Q4|3|?|?|

Then you get actual engineering data rather than Reddit folklore.

---

# 22. The really interesting part: expose it as an API

Once inference works, don't make every application talk directly to the CLI.

Run the llama.cpp server on Laptop A.

Conceptually:

```text
                    ┌───────────────┐
                    │ Python Agent  │
                    └───────┬───────┘
                            │
                    OpenAI-compatible
                            │
                            ▼
                    ┌───────────────┐
                    │ Laptop A      │
                    │ LLM API       │
                    └───────┬───────┘
                            │
                  distributed inference
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
           Laptop B      Laptop C      Laptop D
```

Now:

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://192.168.1.101:8080/v1",
    api_key="local"
)

response = client.chat.completions.create(
    model="local-model",
    messages=[
        {"role": "user", "content": "Explain Delta Lake."}
    ]
)
```

Your entire LAN becomes a private inference endpoint.

That's where this starts becoming genuinely useful.

---

# 23. Add your agent stack

Then you can plug:

```text
                 ┌───────────────┐
                 │   n8n         │
                 └───────┬───────┘
                         │
                 ┌───────▼───────┐
                 │ Local AI API  │
                 └───────┬───────┘
                         │
               ┌─────────▼─────────┐
               │ Distributed LLM   │
               └─────────┬─────────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
        Laptop          Laptop         Laptop
          A               B              C
```

Then:

```text
Python
LangGraph
n8n
RAG
Obsidian
your PKM
local agents
```

can all consume the same local model.

That's a much more interesting architecture than "I installed an LLM on three laptops."

---

# 24. One thing I'd change from my previous answer

I'd **not** jump directly to a 70B model.

I'd build this progression:

```text
STEP 1
──────
8B
A → B

        ↓

STEP 2
──────
8B
A → B → C

        ↓

STEP 3
──────
14B
A → B → C

        ↓

STEP 4
──────
32B
A → B → C

        ↓

STEP 5
──────
70B
A → B → C → D
```

At every stage measure:

```text
Does it fit?
Does it run?
TTFT?
tokens/sec?
RAM?
CPU?
GPU?
network?
```

That gives you a real understanding of distributed inference.

---

# 25. A potentially better architecture for your hardware

There's an important wrinkle.

If all your laptops are roughly:

```text
16 GB RAM
2 GB GPU
```

I wouldn't necessarily use them to create one giant distributed model.

I'd consider **two modes**:

### Mode A — Distributed inference

```text
A + B + C
       ↓
     32B/70B
```

Use when the model doesn't fit.

### Mode B — Model replicas

```text
       Gateway
       /  |  \
      /   |   \
     A    B    C
     │    │    │
    8B   8B   8B
```

Use when you want multiple agents/requests simultaneously.

This can be **much faster**.

For example:

```text
Agent 1 → A
Agent 2 → B
Agent 3 → C
```

instead of:

```text
Agent 1
   ↓
A → B → C
```

for every request.

---

# 26. The architecture I'd ultimately build

For your interests, I'd make the home cluster look like:

```text
                         ┌──────────────┐
                         │    Client    │
                         │ Python/n8n   │
                         │ Obsidian     │
                         └──────┬───────┘
                                │
                                ▼
                    ┌────────────────────┐
                    │    AI Gateway      │
                    │ OpenAI compatible  │
                    └─────────┬──────────┘
                              │
                   ┌──────────┴──────────┐
                   │                     │
                   ▼                     ▼
             ┌───────────┐        ┌─────────────┐
             │ Small LLM │        │ Large LLM    │
             │ Replica   │        │ Distributed  │
             └─────┬─────┘        └──────┬──────┘
                   │                     │
              ┌────┴────┐         ┌─────┼─────┐
              ▼         ▼         ▼     ▼     ▼
             A          B         A     B     C
```

Then add:

```text
Prometheus
    ↓
metrics
    ↓
Grafana
```

and measure:

```text
tokens/sec
TTFT
CPU
RAM
GPU
network
model
request
agent
```

Now you've basically built a tiny **distributed AI inference platform**.

And frankly, that's a much better learning project for someone moving toward **Senior Data Engineer → Architect** than merely running Ollama locally.

---

## Before we actually implement it

Send me the specs of the laptops in this format:

```text
Laptop 1
CPU:
RAM:
GPU:
GPU VRAM:
OS:
Ethernet:

Laptop 2
CPU:
RAM:
GPU:
GPU VRAM:
OS:
Ethernet:

Laptop 3
...
```

You can get the information on Windows with:

```powershell
Get-CimInstance Win32_Processor |
Select-Object Name

Get-CimInstance Win32_ComputerSystem |
Select-Object TotalPhysicalMemory

Get-CimInstance Win32_VideoController |
Select-Object Name,AdapterRAM
```

Then I can give you a **machine-specific implementation**, including the exact llama.cpp build commands, RPC configuration, model size/quantization to start with, network topology, firewall rules, and benchmark plan rather than making you blindly experiment. ([GitHub](https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md "llama.cpp/docs/build.md at master · ggml-org/llama.cpp · GitHub"))