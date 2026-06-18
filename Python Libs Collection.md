String Matching
1. fuzzywuzzy - https://github.com/seatgeek/fuzzywuzzy.git - fuzzy string matching
2. rapidfuzz - https://github.com/rapidfuzz/RapidFuzz.git - High-performance fuzzy string matching
3. Jellyfish - https://github.com/jamesturk/jellyfish.git - phonetic matching
4. thefuzz - https://github.com/seatgeek/thefuzz.git - fuzzy string matching

Web Application
1. Chainlit - chat-based UIs for LLM apps
2. Streamlit - data apps and dashboards
3. Gradio - Dashboard with minimal code
4. Taipy-Rapidly building data-driven Python web apps

Data Visualization
1. Dash (Plotly) - Dynamic Charts and Dashboard
2. Matplotlib - Simple, Static Plots, minimal Overhead

Web Interactions
1. Mechanical Soup - Automate simple web interactions
2. Selenium - Automate real browser interactions for testing or scraping JS-heavy, dynamic websites
3. Playwright - Reliable end-to-end browser automation
4. curl-cffi - Bypass anti-bot protections (e.g., [[cloudflare]]) with browser-like HTTP requests 
5. crawl4ai - AI-optimized web crawling for LLM pipelines
6. helium - Simplify Selenium-based web automation with a higher-level, readable API

Security & Hashing
1. argon2-cffi - Memory-hard password hashing
2. Passlib - Secure password hashing
3. bcrypt - 
4. hvac - programmatic secrets management 
5. pyjwt-Lightweight JWT encode/decode for stateless authentication
6. python-jose-broader JOSE support 
7. itsdangerous-Signing and timestamping data
8. pyopenssl-Low-level SSL/TLS handling and certificate management in Python
9. cryptography-Secure data protection (encryption, hashing, key exchange) for APIs, 
10. pycryptodome-Implement custom cryptographic operations 

ML Model Serving
1. Ray Serve - Scalable, low-latency model serving for Python ML workloads
2. Seldon - Kubernetes-native deployments
3. Kserve - Kubernetes-native model serving for scalable, serverless inference

Validation Framework
1. Great Expectations - Data quality **validation framework** to define, test, and monitor expectations on datasets in ETL/ELT pipelines
2. Monte Carlo
3. Evidently - **ML/data drift monitoring and model performance tracking** alongside data validation
4. Deegu - Spark-heavy environments needing scalable, code-first validation at large scale
5. WhyLabs - 

Shell Scripting via Python
Plumbum - Shell-like scripting in Python with clean subprocess handling
Subprocess - zero dependencies and full control over process execution
Delegator - Simple subprocess management with clean API

Vector DB
FAISS CPU - Local, high-performance vector similarity search on CPUs
Milvus - High-scale vector database for AI workloads
Weaviate - Vector database for semantic search and RAG
Pinecone - Fully managed vector database for production-grade semantic search/RAG
Qdrant - High-performance vector database for production RAG/semantic search
ChromaDB - Lightweight local [[Vector Database]] for embedding

Static web pages
Hugo


Machine Learning Optimization
Optuna - Efficient hyperparameter optimization
Ray Tune - large-scale, distributed tuning across clusters
Keras Tuner - Hyperparameter tuning for Keras models
AutoML - Automate model selection, [[Feature Engineering]], and hyperparameter
AutoGluon - End-to-end [[automl]] for tabular, text, and image data
H2O.ai AutoML - enterprise-ready tooling with strong model explainability and deployment options
Azure ML - Enterprise ML lifecycle on Microsoft stack
Vertex AI - End-to-end ML platform on Google Cloud
SageMaker - End-to-end ML platform on AWS
AutoGrad-Automatic differentiation for computing gradients in custom models and optimization loops
JAX-High-performance numerical computing and ML research with auto-diff 
Pytorch-Flexible **deep learning framework** for building, training, and deploying custom neural networks
Tensorflow-End-to-end ML platform for building, training, and deploying models at scale
Keras-Rapid prototyping of deep learning models with simple
Recommendations-Personalized content/product ranking
Collaborative filtering-simpler baseline with minimal feature engineering
Content based filtering- based on item features
XGBOost-High-performance gradient boosting for structured/tabular data
LightGBM-High-performance gradient boosting for large-scale tabular data
CatBoost-High-accuracy tabular modeling with strong handling of categorical features
Ensemble Methods-
	Bagging
	Boosting
	Stacking-
tensorboard-Real-time visualization of training metrics 
Weights & Biases

LLM Optimization
BitNet-Run **ultra-efficient 1-bit/low-bit LLMs** on edge or low-resource hardware
GGUF Quantization - better for **practical, widely-supported quantization**
KVCache = Speed up LLM inference by caching past key/value states for efficient token-by-token generation
Attention Mechanism - Focus model on relevant parts of input sequences to improve NLP, vision, and multimodal tasks using Attention Mechanisms.
RNN - Sequential data modeling (time series, speech, NLP) where temporal dependencies 
Transformers - State‑of‑the‑art **NLP and multimodal model library**
Pytorch Lightning - Structure and scale PyTorch training with clean, modular cod
DSPY - Programmatic optimization of LLM pipelines 
Bits & Bytes-Memory-efficient **8-bit/4-bit quantization + optimizers** for training and running LLMs on limited GPUs
Accelerate-Hugging Face]] Accelerate is a lightweight orchestration layer for distributed [[pytorch]] training and inference
deepseed-Train and serve large-scale deep learning models efficiently
Fully Sharded Data Parallel-Memory-efficient large model training by sharding parameters, gradients,
Transformer Reinforcement Learning-Hugging Face **TRL (Transformer Reinforcement Learning)** library for fine-tuning LLMs with **RLHF, DPO, PPO**
Agentic Chunking-Dynamic, LLM-driven chunking that adapts to context and intent
Static Chunking-better for predictable performance, speed, and simpler pipelines

Python Package Manager:
Poetry - Dependency management + packaging with lockfile reproducibility
Pip tools - minimal tooling and more control 
UV

AI Coding Agent
Opencode - Lightweight open-source code
Continue - Open-source AI coding assistant in your IDE
Cursor -AI-first code editor for rapid multi-file edit in your IDE
Cline - Autonomous coding agent
Devin - End-to-end autonomous software engineer
Windsurf - AI-native IDE for agentic coding
Github Copilot - Real-time code autocomplete and inline suggestions
Gemini Code Assistant - AI coding assistant tightly integrated with Google Cloud
Codeium - Free, fast AI code completion and chat across IDEs
Claude Code - Agentic coding in your repo
Amazon Code Whisperer - AI code assistant optimized for [Amazon Web Services](Amazon%20Web%20Services.md)
VSCODE-Lightweight, extensible code editor
JetBrains-deep language intelligence, refactoring, and enterprise-grade development



Data Lake Catalog Layer
lakekeeper - Lightweight data lake governance/catalog layer (Iceberg-focused)
Unity Catalog - enterprise-grade governance, lineage, and multi-workspace control

Data Lakes:
Iceberg - Open table format for large-scale data lakes. multi-engine interoperability
Delta Lake - ACID-compliant data lake storage for reliable batch + streaming pipelines 

Data Lake Processing
Hudi - Incremental data lake processing

Data Platforms:
Databricks - Unified data + AI platform for large-scale ETL, streaming, and ML on lakehouse architecture
Snowflake - Cloud data warehouse for scalable analytics
BigQuery-Serverless, petabyte-scale analytics warehouse for fast [[sql]] on massive datasets

Backend as a service
Appwrite - Self-hosted backend-as-a-service
Supabase - Rapidly build full-stack apps with hosted Postgres, auth, storage, and realtime APIs
Firebase - Rapidly build and ship **mobile/web apps with real-time backend**
Big Data-Processing and analyzing massive, high-velocity datasets 



Cloud Compute Service
AWS - Default choice for building highly scalable, cloud-native systems with the widest service ecosystem
GCP - Building and scaling data-intensive, AI/ML-driven platforms
Cloudflare - Run **global edge apps + CDN + security** 
Digital Ocean - Simple, cost-effective cloud hosting


Query language for structuredata
sql - Core language for querying and transforming structured data
spark sql -  process massive datasets across clusters instead of single-node databases

Database Migration
alembic - Version-controlled database schema migrations for Python app
Flyway - language-agnostic, [[sql]]-first migrations with simpler CI/CD integration

Orchestration:
Jenkins - Automate complex CI/CD pipelines with full control
Github Actions - Repo-native CI/CD tightly integrated with GitHub for automating
Cron Job -Simple **scheduled task automation** for running scripts,
Gitlab - End-to-end DevOps platform

Test Automation
Robot Framework -Enterprise‑grade **keyword‑driven test automation** for web, API, and desktop apps

API:
High-performance Python APIs with automatic validation

LLM Orchestration
langgraph = Stateful, deterministic orchestration of LLM agents
Microsoft Autogen -  faster prototyping of conversational
OpenDevin-Autonomous AI software engineer for end-to-end dev tasks
AutoGPT-Autonomous goal-driven agents that plan and execute multi-step tasks with minimal supervision
eigent-Local‑first multi‑agent AI workforce desktop platform
AgentGPT-lighter autonomous agent setup when you want cloud/quick experiments
CrewAI-Coordinate multi-agent LLM teams with role-based collaboration
Haystack cloud-Production-ready RAG pipelines with managed orchestration

Local LLM GUI:
OobaBooga-Local GUI for running and experimenting with open-source LLMs
LM Studio-User-friendly desktop app to run and test local LLMs 
Ollama-Run and manage local LLMs with simple CLI/API
Llama.cpp - Run LLMs locally on CPU/GPU with low memory using quantized GGUF
AirLLM - Run **large LLMs on low-memory machines** by streaming weights from disk

Messaging Platform
Redpanda-Kafka-compatible streaming platform with lower latency and simpler op
Kafka-Real-time event streaming backbone
Pulsar-built-in multi-tenancy, geo-replication, and separation of storage/compute
Flink-Stateful stream processing for low-latency, exactly-once pipelines
Spark Structured Streaming-micro-batch simplicity and tighter integration with batch + ML workloads
Dramatiq-High-performance background task processing in Python
RabbitMQ
Celery-Background job processing and distributed task queues in [[python]] 
APScheduler-In-app job scheduling for Python services
Redis queue-Lightweight background job queue using Redis for fast, simple async task processing 

Video Encoding
zencoder-Cloud-based video encoding/transcoding pipelines
AWS elemental MediaConvert-

Retry Mechanism
Tenacity-Robust retry logic for unreliable operations
Backoff-simpler, lightweight retry use cases


LLM Models
Mistral-High-performance open-weight LLMs for cost-efficient inference
OpenAI-top-tier reasoning, reliability, and managed APIs
Nemotron-NVIDIA’s enterprise-grade LLM family optimized for high-performance reasoning, coding, and agent workflows
Claude-Long-context reasoning and document-heavy workflows
Gemini-Multimodal reasoning across text, code, images, and video
GLM-5-Open‑source frontier‑class **foundation LLM** optimized for **long‑horizon agentic tasks, deep reasoning, systems engineering, and production‑grade coding workflows
ChatGPT-General-purpose AI assistant for reasoning, coding, writing, and problem-solving**
Llama 3- open-source flexibility and easier deployment 

Logging
Logger-Basic application logging using built-in frameworks
StructLog-Structured, context-rich logging in Python services
Logguru-Simple, developer-friendly logging in Python with minimal setup
Loki-Cost-efficient, label-based log aggregation tightly integrated with Prometheus
