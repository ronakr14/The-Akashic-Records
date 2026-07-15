```table-of-contents
```
---

## 1. Data Engineering & ETL (DataFrames, Batch, Pipelines)

**DataFrame & Tabular Processing**
- Pandas - De-facto Python DataFrame library for structured data wrangling.
- Polars - Faster, Arrow-backed DataFrame engine for high-throughput ETL.
- Dask - Parallel pandas-like API to scale workloads across cores/clusters.
- PySpark - Distributed DataFrame engine for large-scale ETL on Spark.
- Koalas - Pandas API on Spark (now part of PySpark 3.2+).
- Vaex - Out-of-core DataFrame for billion-row tabular data.
- Swifter - One-line pandas operation accelerator via Dask/Vegeta.
- Modin - Drop-in pandas replacement that scales via Dask/Ray.
- PyJanitor - Clean, readable pandas pipelines (clean names, dedupe, etc.).
- NumExpr - Vectorized math backend for fast pandas/numpy expressions.
- OpenPyxl - Read/write Excel `.xlsx` files from Python.

**Stream & Real-Time Processing**
- Kafka - Distributed event-streaming backbone for high-throughput pipelines.
- Redpanda - Kafka-compatible streaming with lower latency, simpler ops.
- Pulsar - Multi-tenant messaging with geo-replication and tiered storage.
- Flink - Stateful, low-latency stream processing with exactly-once semantics.
- Spark Structured Streaming - Micro-batch streaming tightly integrated with Spark batch/ML.
- RisingWave - Cloud-native streaming database for real-time analytics.

**ETL Orchestration & Workflow Engines**
- Airflow - DAG-based workflow scheduler for batch ETL pipelines.
- Dagster - Asset-aware data orchestrator with strong typing/testing.
- Prefect - Modern Pythonic workflow orchestration with retries + UI.
- Luigi - Long-running batch pipelines with dependency chaining.
- DAG Factory - Programmatically build Airflow DAGs from YAML/Python config.
- Kedro - Opinionated ML/data pipelines with project templates + catalog.
- n8n - Visual workflow automation connecting APIs, DBs, AI services.
- Zapier - No-code automation across SaaS apps (consumer/prosumer).
- Make (implied) - Visual no-code automation platform.
- SSIS - Microsoft SQL Server Integration Services for ETL.
- Data Factory - Managed cloud ETL/ELT orchestration (Azure).
- Argo (implied) - Kubernetes-native workflow engine for batch jobs.

**File Watching & Process Scheduling**
- Watchdog - Filesystem event monitor for hot-reload pipelines.
- Watchfiles - Fast Rust-backed file watcher for dev servers.
- Schedule - Simple in-process job scheduler for periodic Python tasks.
- Schedulezen - Cron-style human-friendly scheduling DSL.
- Crontab - OS-level scheduled task automation.
- Cron Job - Recurring task automation via system cron.
- APScheduler - In-process advanced scheduler for Python services.

**Migration & Schema Management**
- Alembic - Versioned SQLAlchemy schema migrations.
- Flyway - SQL-first, language-agnostic schema migrations for CI/CD.
- Data Migration - General term for moving data between systems.

---

## 2. Databases, Warehouses & Storage

**Cloud Data Warehouses**
- Snowflake - Cloud-native columnar warehouse for scalable analytics.
- BigQuery - Serverless petabyte-scale SQL warehouse on GCP.
- Databricks - Lakehouse platform combining warehouse + Spark + ML.
- Redshift (implied) - AWS columnar warehouse.
- SQL Server - Microsoft enterprise RDBMS + analytics.
- Oracle - Enterprise RDBMS for OLTP + warehousing workloads.
- Postgres - Open-source advanced RDBMS with rich extension ecosystem.
- SQLite - Embedded zero-config SQL database.

**NoSQL & Specialized Stores**
- DynamoDB - AWS managed key-value/document NoSQL.
- MongoDB - Document-oriented NoSQL for flexible JSON schemas.
- InfluxDB - Time-series database for metrics/IoT workloads.
- Oracle - Enterprise RDBMS with strong consistency/transaction model.

**Vector Databases (cross-ref §9)**
- FAISS CPU - Local high-perf similarity search over dense vectors.
- Milvus - Distributed vector DB for billion-scale AI workloads.
- Weaviate - Vector DB with built-in vectorization modules for RAG.
- Pinecone - Fully managed vector DB for production semantic search.
- Qdrant - High-perf vector DB with rich filtering for production RAG.
- ChromaDB - Lightweight in-memory/embedded vector DB for prototypes.
- Postgres PgVector - Postgres extension for vector similarity search.
- Elasticsearch - Distributed search engine with vector + BM25 retrieval.

**Caching & KV Stores**
- Redis - In-memory KV store for cache, sessions, pub/sub.
- Valkey - Open-source Redis fork, ultra-low-latency KV.
- Memcached - Distributed in-memory object cache.
- DiskCache - Persistent disk-backed cache for Python apps.

**Analytical & Embedded Engines**
- DuckDB - Embedded OLAP database, "SQLite for analytics."
- DataFusion - Rust-based query engine with Python bindings.
- DBT Core - SQL transformation framework with versioned models.

**SQL Tooling & ORM**
- SQLAlchemy - Mature Python SQL toolkit + ORM.
- SQLModel - Type-safe ORM combining Pydantic + SQLAlchemy.
- SQLGlot - Pure-Python SQL parser/transpiler across dialects.
- PyPika - Fluent SQL query builder for Python.
- SQLSoup - Legacy SQLAlchemy legacy mapping helper.
- sql - General structured query language for relational data.
- Spark SQL - Distributed SQL engine on top of Spark.
- NoSQL - General non-relational database category.

---

## 3. Data Quality, Validation, Lineage & Observability

**Data Quality & Validation**
- Great Expectations - Define + test data expectations in pipelines.
- Pandera - Lightweight dataframe/schema validation for pandas/polars.
- Pydantic - Type-driven runtime validation for Python data.
- PydanticAI - Pydantic-based structured/type-safe LLM apps.
- Deequ - Spark-scale data quality checks (AWS).
- Cleanlab - Label-cleaning + data quality ML library.
- Python Protocols - Structural typing for interfaces.
- Abstract Base Classes - Enforce interface contracts via inheritance.
- Beartype - Runtime type-checker decorator for any Python function.

**Data Observability & Drift**
- Monte Carlo - Commercial data observability platform.
- Evidently - ML/data drift + model performance monitoring.
- WhyLabs - Data/ML observability with whylogs profiling.
- Cleanlab - Label noise detection + dataset QA.
- LakeWatch - Real-time data lake observability + monitoring.
- Lakekeeper - Lightweight Iceberg-focused catalog/governance.
- Unity Catalog - Enterprise lakehouse governance + lineage.

**Model & Experiment Tracking**
- MLflow - End-to-end ML lifecycle: tracking, registry, deploy.
- ML Metadata - Track artifacts/lineage across ML pipelines.
- Weights & Biases - Experiment tracking, sweeps, model registry.
- TensorBoard - Real-time training metric visualization.
- DAGsHub - Git-for-data-science + experiment tracking.
- DVC (Data Version Control) - Git-based versioning for datasets/models.

---

## 4. Data Visualization & BI

**Python Visualization Libraries**
- Matplotlib - Foundational static plotting library.
- Plotly - Interactive declarative charts (browser-rendered).
- Dash - Plotly-powered Python dashboard web framework.
- Seaborn (implied) - High-level statistical plotting on matplotlib.

**JavaScript Visualization**
- D3 - Low-level JS library for fully custom interactive viz.

**BI Platforms**
- Apache Superset - Enterprise OSS BI + dashboards.
- Metabase - Lightweight BI for non-technical users.
- PowerBI - Microsoft BI with strong Excel integration.

**Diagramming**
- Mermaid - Markdown-style text-to-diagram renderer.

---

## 5. ML & Deep Learning Foundations

**Core Frameworks**
- PyTorch - Flexible dynamic-graph deep learning framework.
- TensorFlow - End-to-end static + dynamic graph ML platform.
- Keras - High-level NN API for rapid prototyping.
- JAX - High-perf numerical computing + auto-differentiation.
- AutoGrad - Reverse-mode autodiff for custom optimization.

**Distributed & Scalable Training**
- Ray - Distributed compute framework for Python ML workloads.
- Ray Tune - Scalable distributed hyperparameter search.
- PyTorch Lightning - Structured PyTorch training at scale.
- Accelerate - HF lightweight wrapper for distributed PyTorch.
- DeepSpeed - Microsoft library for large-model training/inference.
- FSDP - Shard params/grads across GPUs for huge models.
- Horovod (implied) - Uber's distributed training framework.
- Scalable & Distributed Training - General category for multi-GPU/cluster training.

**Hyperparameter & AutoML**
- Optuna - Efficient Bayesian hyperparameter search.
- Keras Tuner - Hyperparameter tuning for Keras models.
- Lazy Predict - Quickly benchmark many sklearn models on a dataset.
- AutoML - General category: auto model selection + FE + tuning.
- AutoGluon - Multi-modal AutoML (tabular/text/image) end-to-end.
- H2O.ai AutoML - Enterprise AutoML with explainability.

**Tabular / Gradient Boosting**
- XGBoost - High-perf gradient boosting for tabular data.
- LightGBM - Fast gradient boosting for very large datasets.
- CatBoost - High-accuracy boosting with native categorical handling.
- scikit-learn - Foundational ML library: classical algorithms + pipelines.

**Classical & Specialized Models**
- Decision Trees - Interpretable tree-based learners.
- Random Forest - Bagged trees for tabular robustness.
- Ensemble Methods (Bagging/Boosting/Stacking) - Combine many weak learners.
- Gradient Boosting - Sequential boosting framework category.
- Support Vector Machines - Kernel methods for high-dim classification.
- Linear Regression - Baseline continuous-target predictor.
- Logistic Regression - Baseline binary classifier.
- K-means - Classic centroid-based clustering.
- PCA - Linear dimensionality reduction.
- Probabilistic Models & Bayesian ML - Bayesian inference frameworks.
- Hidden Markov Models - Sequential probabilistic models.

**Neural Architectures**
- Transformers - Attention-based SOTA NLP/multimodal models.
- RNN - Recurrent nets for sequential data.
- LSTM - Long short-term memory recurrent units.
- Attention Mechanism - Focus on relevant input parts (transformer core).
- Seq2Seq Architecture - Encoder-decoder sequence models.
- Feedforward Neural Networks - Basic fully-connected NNs.
- CNN - Convolutional networks for images/signal.
- Capsule Networks - Routing-based image representation learning.
- Graph Neural Networks - NN for graph-structured data.
- Vision Transformers - Transformer applied to image patches.
- Mamba - State-space model for long-sequence modeling.
- Diffusion Models - Iterative denoising generative models.
- AutoEncoders - Self-supervised reconstruction networks.
- Variational Autoencoders - Probabilistic generative encoders.
- Generative Models - General category for generative architectures.
- Dynamic Computation Graphs - Conditional computation in graphs.

**Learning Paradigms**
- Supervised Learning - Labeled classification/regression.
- Unsupervised Learning - Pattern discovery without labels.
- Semi-Supervised & Weak Supervision - Combine labeled + unlabeled/noisy labels.
- Reinforcement Learning - Agent learns from reward signals.
- Transfer Learning - Reuse pretrained representations on new tasks.
- Pretrained Models - Models pre-trained on large corpora.

**Recommendation Systems**
- Recommendations - Personalized ranking systems category.
- Collaborative Filtering - User/item interaction-based ranking.
- Content-Based Filtering - Item feature-based ranking.

**Specialized ML Domains**
- Anomaly Detection - Identify outliers/fraud/rare events.
- Time Series Models - Forecasting + temporal modeling.
- Explainability & Interpretability - Model reasoning transparency category.
- SHAP - Game-theoretic feature attribution.
- LIME - Local interpretable model-agnostic explanations.
- InterpretML - Microsoft's explainable ML toolkit.
- Feature Engineering - Transform raw inputs into model-ready features.

**Production Serving & Deployment**
- BentoML - Standardized model packaging + serving.
- Ray Serve - Scalable low-latency model serving.
- Seldon - Kubernetes-native ML deployment.
- KServe - Serverless Kubernetes inference.
- TensorFlow Extended (TFX) - End-to-end TF production pipelines.
- TensorFlow Hub - Repository of pretrained TF models.
- TensorRT - NVIDIA high-perf inference optimizer.
- Open Neural Network Exchange (ONNX) - Portable model format.
- Diffusers - Hugging Face diffusion model library.
- TorchVision - Pretrained vision models + transforms.
- TorchAudio - Audio models + I/O for PyTorch.
- MLxtend - Companion library with extra ML utilities.

---

## 6. LLM Frameworks, Models & Inference

**Local LLM Runtimes & Quantization**
- Ollama - Simple CLI for running local LLMs.
- LM Studio - Desktop GUI for local LLM experimentation.
- llama.cpp - CPU/GPU local LLM via GGUF quantization.
- Oobabooga - Local web GUI for open-source LLMs (text-generation-webui).
- AirLLM - Run huge LLMs on low-RAM via disk-streamed weights.
- vLLM - High-throughput serving with PagedAttention.
- OpenLLM - Standardized packaging + serving for open-source LLMs.
- Text Generation Interface (TGI) - HF production LLM serving.
- BitNet - 1-bit LLMs for edge/low-resource hardware.
- GGUF Quantization - Standardized quantization for local LLM weights.
- Bits & Bytes - 8-bit/4-bit optimizers for memory-efficient training.
- KV Cache - Cache past keys/values to speed token generation.
- Paged Attention - Memory-efficient attention via paging.
- llmfit - Hardware-aware local LLM size recommender.
- Unsloth - Fast QLoRA fine-tuning for LLMs.

**LLM Models**
- Mistral - Open-weight high-perf inference-optimized LLMs.
- OpenAI / ChatGPT - Top-tier managed reasoning + chat models.
- Claude - Long-context reasoning + document-heavy workflows.
- Gemini - Multimodal reasoning over text/code/image/video.
- Llama 3 - Open-source flexible foundation model.
- Nemotron - NVIDIA enterprise-grade LLM family.
- GLM-5 - Open-source frontier agentic + reasoning LLM.
- Kimi - Long-context Chinese LLM from Moonshot.
- IBM Granite-Docling - IBM docling-oriented Granite family.

**LLM Frameworks & Training**
- Hugging Face Transformers - Load/fine-tune SOTA NLP/vision models.
- PEFT - Parameter-efficient fine-tuning (LoRA/QLoRA).
- TRL (Transformer RL) - RLHF/DPO/PPO fine-tuning for LLMs.
- Transformers (general) - SOTA NLP/multimodal model category.

**Optimization Tooling**
- DSPy - Programmatic optimization of LLM pipelines.
- Instructor - Structured outputs from LLMs via Pydantic.

---

## 7. GenAI Pipelines: RAG, Agents, Chunking, Embeddings

**LLM Orchestration Frameworks**
- LangChain - Chain tools, prompts, retrievers + integrations.
- LlamaIndex - Ingestion + indexing + retrieval for RAG.
- Haystack - Production RAG pipelines (deepset).
- Haystack Agents - Agent workflows on Haystack.
- Semantic Kernel - Enterprise-grade AI orchestration (.NET/Python).
- LiteLLM - Unified interface to 100+ LLM providers.
- LangSmith - LangChain debugging/observability platform.
- LangWatch - LLM observability + evaluation.
- Logfire - Pydantic-based observability for LLM apps.
- Instructor - Structured LLM outputs via Pydantic schemas.

**Agent Frameworks**
- LangGraph - Stateful, deterministic multi-agent orchestration.
- AutoGen - Conversational multi-agent framework (Microsoft).
- CrewAI - Role-based collaborative LLM agent teams.
- LangChain Agents - ReAct/agent executors in LangChain.
- AutoGPT - Autonomous goal-driven agent loops.
- AgentGPT - Cloud-hosted autonomous agents.
- DeerFlow - Long-horizon multi-step AI workflow coordinator.
- Eigent - Local-first multi-agent desktop platform.
- OpenAI Swarm - Lightweight OpenAI agent handoff framework.
- Claw Agents / Claw Router - Custom agent routing infra.
- Agentic RAG - LLM-driven dynamic retrieval pipelines.
- AI Agents - General category for autonomous LLM agents.

**Multi-Agent Platforms**
- Multi Agent Systems - General multi-agent architecture category.
- OpenDevin - Autonomous software engineer agent.
- Devin - End-to-end autonomous software engineer (Cognition).

**RAG Systems & Platforms**
- Classic RAG - Retrieve-then-generate baseline pipeline.
- Graph RAG - Graph-structured retrieval over knowledge graphs.
- RAGFlow - End-to-end RAG pipeline platform.
- Anything LLM - Self-hosted chat-with-docs workspace.
- Dify.AI - OSS LLMOps + agentic workflow builder.
- Flowise AI - Visual drag-drop LLM workflow builder.
- Deepset Cloud - Managed Haystack cloud platform.
- PageIndex - Long-document RAG via hierarchical indexing.
- Recursive-llm - Recursive reasoning over chunked docs.

**Chunking & Text Splitters**
- Agentic Chunking - LLM-driven adaptive chunking.
- Static Chunking - Fixed-size token-aware chunking.
- Text Splitter - Generic chunking utilities.
- Chunkr - Document-aware intelligent chunking.
- Sentence Transformers - Embedding-based semantic chunking.

**Embeddings**
- OpenAI Embeddings - High-quality managed embeddings.
- Gemini Embeddings - Google's embedding models.
- Sentence Transformers - Open-source embedding model library.

**Document Parsing & Ingestion**
- LlamaParse - LLM-optimized PDF/document parser.
- MarkitDown - Convert documents → Markdown.
- PyPDF2 - Pure-Python PDF reader/writer.
- PyPDFium2 - PDFium-backed PDF rendering.
- PDFPlumber - Extract text/tables from PDFs.
- PDF.js - JS-based PDF renderer (browser).
- Dots.OCR - Vision-LLM OCR for complex layouts.
- Unstructured (implied) - General doc parsing library.
- IBM Granite-Docling - Doc-conversion Granite family.

**Prompting & Prompt Tools**
- Promptify - Generate structured NLP prompts.
- Natural Language Interactions - General NL interface category.
- Prompt Engineering - General practice category.
- paged attention (cross-ref §6) - Memory-efficient attention inference.

**Retrieval / Search (AI-flavored)**
- Tavily - LLM-optimized web search API.
- Serp API - Programmatic Google search results.
- Phind - Developer-focused AI search engine.
- Perplexity - Answer-engine search + citation.
- Hunter Alpha - AI-powered prospecting/search.

---

## 8. NLP, Speech & Text Processing

**Core NLP Libraries**
- spaCy - Industrial-strength NLP (tokenization, NER, deps).
- NLTK (implied) - Foundational NLP teaching/research library.
- TextBlob - Simple NLP API (sentiment, POS, translation).
- Textacy - Higher-level spaCy patterns + corpus utilities.
- Flashtext - Fast keyword/regex replacement at scale.
- langdetect - Language detection from text.
- PySBD - Sentence boundary disambiguation.
- CleanText - Normalize noisy web/social text.
- UniDecode - Unicode transliteration/normalization.
- BM25 - Classic lexical retrieval ranking function.

**Tokenization**
- Tiktoken - OpenAI's fast BPE tokenizer.
- Tokenization - General text → token process.

**String Matching & Distance**
- FuzzyWuzzy - Fuzzy string matching (Levenshtein).
- RapidFuzz - High-perf C-backed fuzzy matching.
- Jellyfish - Phonetic + string distance algorithms.
- thefuzz - Modern maintained fork of fuzzywuzzy.
- textdistance - Compute 30+ string distance metrics.

**Speech & Audio**
- Chatterbox - TTS/voice synthesis library.
- LuxTTS - Open-source text-to-speech system.
- PyTTSx3 - Cross-platform TTS wrapper.
- Torchaudio - PyTorch audio I/O + transforms.
- SpeechMA - Speech models + audio processing.

**OCR & Vision**
- PyTesseract - Tesseract OCR Python wrapper.

**Localization & Translation**
- Argostranslate (implied) - Offline translation library.

---

## 9. Search, Retrieval & Vector Stores
(Cross-references §2 vector DBs and §7 RAG.)

- Elastic Search - Distributed search engine (BM25 + vectors).
- FAISS CPU - Local vector similarity search.
- Milvus - Distributed vector DB for AI scale.
- Weaviate - Vector DB with built-in vectorization.
- Pinecone - Managed vector DB for production RAG.
- Qdrant - Vector DB with rich payload filtering.
- ChromaDB - Lightweight embedded vector DB.
- PgVector - Postgres vector similarity extension.
- Semantic Search - Meaning-based search paradigm.
- BM25 - Lexical baseline retriever.
- Lexical Search (implied) - Keyword-based search.

---

## 10. Web Frameworks & API Development

**Python Web Frameworks**
- Django - Full-stack batteries-included web framework.
- Flask - Lightweight WSGI microframework.
- FastAPI - Async-first, type-driven API framework.
- Litestar - Modern ASGI framework with DI + plugins.
- Robyn - Rust-accelerated async Python web framework.
- Hug - API framework with type annotations (implied).

**LLM/AI App UI Frameworks**
- Streamlit - Data apps + dashboards in pure Python.
- Gradio - Minimal-code ML model demo UIs.
- Chainlit - Chat-style UIs for LLM apps.
- Taipy - Data-driven full-stack Python web apps.
- NiceGUI - Browser-based UI from Python callbacks.
- Flet - Flutter-style cross-platform Python UIs.
- PyScript - Python in the browser via Pyodide.
- PyWebView - Native window wrapper around web content.

**Desktop GUI Frameworks**
- PySide6 - Qt for Python (LGPL).
- Toga - Native cross-platform Python GUI toolkit.
- CustomTkinter - Modern themed Tkinter widgets.
- PyGUI - Lightweight native GUI library.
- EEL - Electron-style HTML/CSS/JS Python desktop apps.

**Frontend (non-Python)**
- JavaScript - Browser + full-stack web language.
- TypeScript - Typed superset of JS.
- React JS - Component-based frontend library.
- Next.js - Full-stack React framework.
- Node.js - JS server-side runtime.

**Static Site Generators & Docs**
- Hugo - Go-based ultra-fast static site generator.
- MkDocs - Python static site generator for project docs.
- MkDocs Material - Modern theme for MkDocs.
- GitHub Pages - Static hosting on GitHub.
- Netlify - JAMstack hosting + CI/CD.
- Vercel - Frontend cloud + edge functions.
- Fumadocs - Modern docs framework for Next.js.

**Serverless & Edge**
- Cloudflare - Global edge + CDN + security platform.
- Surge.sh - Simple static deploy CLI.
- Zappa - Deploy WSGI Python apps to AWS Lambda.
- Nitric - Cloud-agnostic serverless framework.

**API Tooling**
- Postman - Collaborative API testing + collections.
- Hoppscotch - Lightweight browser-based API client.
- Insomnia - Lightweight REST/GraphQL client.

**ASGI/WSGI Servers**
- Uvicorn - Lightning-fast ASGI server.

---

## 11. Web Scraping & Browser Automation

**Browser Automation**
- Selenium - Full browser automation + testing.
- Playwright - Reliable modern browser automation.
- MechanicalSoup - Simple HTTP + form automation.
- Helium - Higher-level readable Selenium wrapper.
- Pyautogui - Desktop GUI automation (cross-app).

**HTTP & Async Clients**
- httpx - Modern async HTTP client (requests-compatible).
- HttpCore - Low-level async HTTP transport.
- curl-cffi - Browser-TLS-fingerprint HTTP client (anti-bot).
- Fire - Auto-generate CLI from any Python object.
- Invoke - Pythonic task execution tool.

**Web Crawling for AI**
- Crawl4AI - LLM-pipeline-optimized crawler.
- Scrapling - Adaptive scraper with auto-fallback.
- BeautifulSoup (implied) - HTML/XML parsing library.
- lxml (implied) - Fast XML/HTML parser.

**Tunneling & Proxies**
- Ngrok - Public tunnel to local services.
- LocalToNet - Free local tunnel alternative.
- LocalXpose - Public URL tunneling service.

---

## 12. Security, Cryptography & Identity

**Password Hashing**
- bcrypt - Adaptive password hashing.
- argon2-cffi - Memory-hard password hashing (modern).
- Passlib - Unified password hashing interface.

**General Cryptography**
- cryptography - Modern crypto primitives (Fernet, RSA, TLS).
- PyCryptodome - Low-level crypto algorithms.
- PyOpenSSL - SSL/TLS + certificate handling.

**Tokens & Identity**
- PyJWT - Compact JWT encode/decode.
- python-jose - Broader JOSE (JWT/JWS/JWE) support.
- itsdangerous - Signed + timestamped data (Flask).

**Secrets Management**
- hvac - HashiCorp Vault client.
- secrets - Stdlib secure random + token mgmt.
- python-dotenv - Load `.env` into env vars.

**Obfuscation & Protection**
- PyArmor - Python bytecode obfuscation + licensing.

**SSH & Secure Channels**
- Paramiko - SSH2 protocol pure-Python client.

**Static Analysis / SAST**
- Bandit - Security linting for Python code.

**Misc Security**
- Ethical Hacking - General penetration-testing category.
- pywhat - Identify strings (emails, hashes, crypto).

---

## 13. DevOps, CI/CD & Infrastructure

**CI/CD Platforms**
- Jenkins - Self-hosted CI/CD pipelines.
- GitHub Actions - Repo-native CI/CD on GitHub.
- GitLab - End-to-end DevOps platform with built-in CI.
- Concourse (implied) - Pipeline-as-code CI/CD.

**Containers & Orchestration**
- Docker (implied) - Container runtime.
- Kubernetes (implied) - Container orchestration.
- Helm - Kubernetes package manager.
- Kubeflow Pipelines - K8s-native ML pipelines.
- Container Service - Managed container orchestration.

**Infrastructure as Code**
- Terraform - Multi-cloud IaC declarative provisioning.
- Ansible - Agentless config mgmt + orchestration.
- Pulumi (implied) - Code-based IaC.

**PaaS / Hosting Platforms**
- Heroku - Simple git-push app deployment.
- Railway - Zero-config app + DB hosting.
- Render - Managed web services + static sites.
- Fly.io - Global edge app deployment.
- InfinityFree - Free PHP/static hosting.
- Coolify - Self-hosted Heroku alternative.
- Digital Ocean - Simple VPS + app platform hosting.

**Edge & Serverless**
- Cloud Run - GCP managed serverless containers.
- AWS Lambda (implied) - AWS serverless functions.
- Cloudflare Workers (implied) - Edge serverless.

**Monitoring & Observability (Infra)**
- Prometheus - Metrics + alerting (Pull model).
- Grafana - Metrics dashboards + alerting UI.
- Grafana Cloud - Hosted Grafana + Prometheus stack.
- Loki - Cost-efficient log aggregation (label-based).
- Containers & Observations - K8s observability category.

**Cost & FinOps**
- Cost Attribution Engine - Tag/chargeback cloud spend.

**Project / Work Management**
- Jira - Agile issue + project tracking.
- Confluence - Team wiki + structured docs.
- Notion - Flexible team workspace.
- Linear (implied) - Modern issue tracker.
- Trello (implied) - Kanban boards.

---

## 14. Cloud Platforms & Deployment

**Hyperscalers**
- AWS - Broadest cloud ecosystem (default for scale).
- GCP - Strong for data + AI/ML workloads.
- Microsoft Azure - Enterprise + Microsoft stack.
- Oracle Cloud - Oracle/ERP workloads.

**Specialized Cloud**
- Cloudflare - Edge + CDN + security.
- IBM Cloud - Hybrid + enterprise (implied).
- Digital Ocean - Simple, affordable VPS + PaaS.

**Managed ML Platforms**
- Vertex AI - GCP end-to-end ML platform.
- SageMaker - AWS end-to-end ML platform.
- Azure ML - Azure ML lifecycle platform.

---

## 15. AI Coding Agents & IDEs

**AI Coding Assistants (IDE plugins)**
- GitHub Copilot - Real-time inline code completion.
- Cursor - AI-first multi-file code editor.
- Continue - Open-source AI coding extension.
- Windsurf - AI-native agentic IDE.
- Codeium - Free multi-IDE AI completion.
- Tabnine - AI completion across languages/IDEs.
- Claude Code - Agentic coding in your terminal/repo.
- Gemini Code Assistant - Google Cloud-integrated coding AI.
- Amazon CodeWhisperer - AWS-optimized coding AI.
- Sourcegraph Cody - Repo-aware code intelligence.
- Phind - Developer AI search pair-programmer.
- Perplexity - AI answer engine for devs.
- OpenCode - Lightweight open-source coding AI.

**Autonomous Coding Agents**
- Devin - End-to-end autonomous SWE agent.
- Cline - Autonomous coding agent in VSCode.
- OpenDevin - Open-source autonomous SWE agent.

**IDEs & Editors**
- VSCode - Lightweight extensible code editor.
- JetBrains - Deep-language-intelligence IDEs.
- VSCode Debug - Built-in debugger for VSCode.

**AI CLI Tools**
- Gemini CLI - Google's AI from the terminal.
- OpenAI Codex CLI - Codex agent in CLI.
- HKUDS CLI-Anything - Turn any function into a CLI.
- CLI Anything - General "make it a CLI" pattern.

**Personal Memory / Context**
- Claude Mem - Persistent memory layer for Claude.

---

## 16. Testing & QA

**Test Frameworks**
- Pytest - Scalable unit/integration tests with fixtures.
- Unittest - Stdlib structured testing framework.
- Robot Framework - Keyword-driven test automation.

**Browser/UI Testing**
- Selenium - Cross-browser UI test automation.
- Playwright - Reliable modern browser testing.

**Property-Based Testing**
- Hypothesis (implied) - Property-based testing for Python.

**Load/Performance Testing**
- Locust (implied) - Python load testing.

**Code Quality**
- Bandit - Security-focused linting.

---

## 17. Logging, Observability & Monitoring

**Python Logging**
- Logger - Stdlib logging framework.
- Loguru - Drop-in simple + colorful logging.
- StructLog - Structured context-rich logging.

**Log Aggregation**
- Loki - Grafana-stack log aggregation.
- ELK (implied) - Elasticsearch/Logstash/Kibana.

**APM & Tracing**
- Logfire - Pydantic-based tracing + logs.
- PyInstrument - Low-overhead Python profiler.
- Tracemalloc - Stdlib memory allocation tracing.
- OpenTelemetry (implied) - Vendor-neutral tracing.

**ML-Specific Observability**
- Evidently - ML drift + model performance tracking.
- LangSmith - LLM tracing + debugging.
- LangWatch - LLM observability + evaluation.
- WhyLabs - ML/data observability.

---

## 18. Workflow Orchestration & Automation
(Cross-ref §1 ETL pipelines, §7 AI workflows.)

- Airflow - Batch ETL DAG scheduler.
- Dagster - Asset-aware orchestration.
- Prefect - Pythonic workflow orchestration.
- Luigi - Long-running batch pipelines.
- n8n - Visual workflow automation.
- Zapier - No-code SaaS automation.
- Make - Visual no-code automation platform.
- Apache Beam (implied) - Unified batch+stream SDK.

---

## 19. Messaging, Queues & Streaming
(Cross-ref §1 stream processing.)

- Kafka - Distributed event streaming.
- Redpanda - Kafka-compatible low-latency streaming.
- Pulsar - Tiered-storage messaging + streaming.
- RabbitMQ - AMQP message broker.
- Celery - Distributed Python task queue.
- Dramatiq - High-perf Python task queue.
- RQ (Redis Queue) - Redis-backed Python job queue.
- APScheduler - In-process job scheduling.

---

## 20. Email & Notifications

- SendGrid - High-volume transactional + marketing email.
- Resend - Developer-first transactional email API.
- Postmark - Reliable transactional email delivery.
- Mailgun - Email API for devs (transactional + bulk).
- Postal - Self-hosted email delivery server.
- sender - Lightweight transactional email service.
- Notifypy - Cross-platform desktop notifications.

---

## 21. CLI, Scripting & Process Automation

**CLI Frameworks**
- Click - Composable Python CLI framework.
- Fire - Auto-CLI from any Python object.
- Typer (implied) - Type-driven CLI builder.
- HKUDS CLI-Anything - Turn any function into a CLI.
- CLI Anything - General pattern of exposing functions as CLIs.

**Shell & Subprocess**
- Plumbum - Shell-like Pythonic subprocess.
- Subprocess - Stdlib process control.
- Delegator - Simple subprocess wrapper.
- Invoke - Pythonic task runner (like Make/Rake).
- Paramiko - SSH-based remote task execution.
- BASH - Unix shell for system automation.
- SH - POSIX shell scripting.

**Scripting Languages**
- Python - Default backend/data/AI language.
- JavaScript - Browser + Node scripting.
- TypeScript - Typed JS for scale.
- Scala - JVM functional + OO language.

**TUI & Output**
- Rich - Beautiful terminal output + progress bars.
- Textual - TUI framework built on Rich.
- tqdm - Fast progress bars for loops.
- Yaspin - Spinner utility for CLIs.
- Humanize - Human-readable formatting (dates, sizes).

---

## 22. Python Packaging & Environment

- Poetry - Dependency + packaging with lockfile.
- Pip-Tools - Minimal pinning + resolution tooling.
- UV - Rust-based ultra-fast pip replacement.
- Conda - Cross-language env + package manager.
- Pipenv (implied) - App-level env + dep manager.
- Pyenv (implied) - Python version manager.
- python-dotenv - Load `.env` files.
- Pip (implied) - Default Python installer.

---

## 23. Version Control, Collaboration & Project Management

**Version Control Systems**
- Git - Distributed version control (implied).
- DVC (Data Version Control) - Git for datasets + models.
- Git LFS - Large file storage extension for Git.
- GitPython - Pythonic Git repository access.

**Hosting Platforms**
- GitHub - Centralized Git hosting + collaboration.
- GitLab - DevOps + Git hosting platform.
- Bitbucket - Git hosting tied to Atlassian.

**Spec-Driven Development**
- GitHub Speckit - Spec-first GitHub development.

**Project / Knowledge Management**
- Jira - Issue tracking + agile boards.
- Confluence - Team documentation wiki.
- Notion - Flexible team workspace + docs.

---

## 24. Concurrency, Async & GPU

**Async & Concurrency**
- Async - Stdlib asyncio framework.
- Uvicorn - ASGI server (async Python).
- Threading - Stdlib OS threads.
- Multiprocessing - Stdlib process parallelism.
- Joblib - Easy parallelism for Python (esp. sklearn).
- concurrent.futures (implied) - High-level pool executors.

**GPU & Accelerators**
- CUDA - NVIDIA GPU compute platform.
- TensorRT - NVIDIA inference optimizer.

**Distributed Compute**
- Dask - Parallel pandas-like compute.
- Ray - Distributed Python compute framework.

---

## 25. Type Safety, Validation & Utilities

**Type System & Validation**
- Pydantic - Runtime data validation via type hints.
- PydanticAI - LLM-app variant of Pydantic.
- Beartype - Drop-in runtime type checker.
- Python Protocols - Structural subtyping.
- Abstract Base Classes - Explicit interface base classes.
- Python Named Tuples - Lightweight typed tuples.
- Dataclasses (implied) - Stdlib class boilerplate reducer.
- TypedDict (implied) - Dict shape typing.

**Functional & Metaprogramming**
- Functools - Stdlib functional helpers (lru_cache, reduce).
- Wrapt - Function/method decoration utilities.
- AST - Python abstract syntax tree manipulation.
- DeepDiff - Deep comparison of Python objects.

**Serialization & Data Formats**
- OrJSON - Fast JSON (encode/decode).
- YARL - Yet another URL library (immutable URLs).
- OpenPyxl - Excel xlsx I/O.

**General Utilities**
- Humanize - Human-readable values.
- Arrow - Cleaner datetime API.
- Pendulum (implied) - Drop-in datetime replacement.
- TQDM - Progress bars.
- Yaspin - Terminal spinners.
- defaultdict - Stdlib dict-with-default.
- debugpy - Remote debugging for Python.

**Filesystem & Config**
- PyFilesystem2 - Unified filesystem abstraction.
- Hydra - Composable config management.
- python-dotenv - `.env` loader.
- Fire - Object → CLI.

---

## 26. Configuration, Secrets & Environment

- Hydra - Composable YAML-based config framework.
- python-dotenv - `.env` → env vars.
- hvac - HashiCorp Vault client.
- secrets - Stdlib secure secrets generator.
- Dynaconf (implied) - Layered settings management.
- ConfigArgParse (implied) - CLI + file + env config.

---

## 27. Audio, Video & Media

**Video Encoding**
- Zencoder - Cloud video transcoding API.
- AWS Elemental MediaConvert - AWS video transcoding service.

**Audio / Speech**
- LuxTTS - TTS model system.
- PyTTSx3 - Cross-platform TTS wrapper.
- Torchaudio - PyTorch audio toolkit.
- Chatterbox - TTS/voice library.
- SpeechMA - Speech model processing.

**Vision**
- TorchVision - PyTorch vision models + transforms.
- Diffusers - Diffusion model library (HF).
- Vision Transformers - ViT category.

---

## 28. Networking, Tunnels & Protocols

- httpx - Async HTTP client.
- HttpCore - Low-level async HTTP transport.
- Paramiko - SSH2 client.
- Ngrok - Public tunnel to localhost.
- LocalToNet - Free local tunnel.
- LocalXpose - Public URL tunnel.
- curl-cffi - TLS-fingerprint HTTP client.
- Model Context Protocol (MCP) - Standardized LLM tool-use protocol.
- FastMCP - Fast Model Context Protocol server framework.
- PageIndex - Long-doc hierarchical indexing protocol.

---

## 29. Data Structures, Math & Scientific Computing

**Numerical**
- NumPy - Foundational N-dimensional arrays.
- NumExpr - Fast array expression evaluator.
- SciPy (implied) - Scientific computing algorithms.
- SymPy (implied) - Symbolic mathematics.

**Statistics & Probabilistic**
- Probabilistic Models & Bayesian ML - Bayesian frameworks category.
- Statsmodels (implied) - Statistical models + tests.
- PCA - Dimensionality reduction.
- Hidden Markov Models - Probabilistic sequences.

**Data Structures**
- defaultdict - Dict with factory default.
- Named Tuples - Lightweight record types.
- Frozen sets (implied) - Immutable sets.

---

## 30. Documentation & Static Sites

(Cross-ref §10 for tools.)

- Hugo - Go static site generator.
- MkDocs - Python static docs generator.
- MkDocs Material - Material theme for MkDocs.
- GitHub Pages - GitHub static hosting.
- Netlify - JAMstack hosting + CI.
- Vercel - Frontend cloud platform.
- Surge.sh - Static deploy CLI.
- Fumadocs - Next.js docs framework.
- Mermaid - Text-to-diagrams in markdown.
- Confluence - Wiki + structured docs.
- Notion - Flexible docs + workspace.
- MkDocs (implied - cross-listed) - Python docs site.

---

## 31. Specialized Domains & AI Concepts
(Concepts grouped here that are not single tools.)

**AI Paradigms**
- Artificial Intelligence - General AI category.
- Generative AI - Generative model category.
- Machine Learning - General ML category.
- Deep Learning - Deep NN category.
- Neural Networks - General NN category.

**Reasoning & Architecture**
- Embeddings - Dense vector representations.
- Transfer Learning - Reuse pretrained models.
- Reinforcement Learning - Agent + reward learning.
- Unsupervised Learning - No-label pattern discovery.
- Semi-Supervised & Weak Supervision - Combined supervision.
- Supervised Learning - Labeled prediction.
- Pretrained Models - Off-the-shelf trained models.

**Generative**
- Diffusion Models - Iterative denoising generation.
- Variational Autoencoders - Probabilistic encoders.
- AutoEncoders - Reconstruction networks.
- Generative Models - Generative architecture category.

**Retrieval & Reasoning**
- RAG Systems - Retrieval-augmented generation category.
- Classic RAG - Standard retrieve-then-generate.
- Graph RAG - Graph-structured retrieval.
- Agentic RAG - Adaptive agent-driven retrieval.

**Misc Concepts**
- Clustering - Group similar items (category).
- Capsule Networks - Capsule routing vision nets.
- CNN - Convolutional networks.
- RNN - Recurrent networks.
- LSTM - Long short-term memory nets.
- Graph Neural Networks - GNN category.
- Vision Transformers - ViT category.
- Mamba - SSM long-sequence models.
- Seq2Seq Architecture - Encoder-decoder sequences.
- Dynamic Computation Graphs - Conditional compute graphs.
- Paged Attention - Memory-efficient attention.
- KV Cache - Past-token cache for inference.
- Interpretability - Model explainability category.

**Blockchain / Web3**
- Blockchain - Distributed ledger category.

**Other Specialized**
- Critical Chain Project Management - Project mgmt methodology.
- Bandit (cross-ref §12) - Security linter.
- Cleanlab (cross-ref §3) - Label cleaning.
- Cleantext (cross-ref §8) - Text normalization.
- Cleanlab - Same.

---

## 32. Cross-cutting Tools & Misc

**Repetitive/Do-Not-Put-Anywhere-Else**

- Fire - Object → CLI (cross-ref §21).
- HKUDS CLI-Anything - Function → CLI.
- CLI Anything - Generic CLI pattern.
- Manifest - Likely manifest-format tool (ambiguous).
- PageIndex - Doc hierarchical indexing (cross-ref §7/§28).
- Recursive-llm - Recursive LLM reasoning.
- PageIndex - Long-doc tree indexing.
- Recursive-llm - Recursive chunking + reasoning.
- LoRA - Parameter-efficient fine-tuning (implied via PEFT).
- LangChain Agents - ReAct agents in LangChain.
- Langduse - Ambiguous/unknown — likely typo or niche tool.
- langduse - Same as above.
- OpenShell - Open interpreter shell (implied).
- openjarvis - Ambiguous; possibly Jarvis assistant variant.
- cleanlab - Cross-ref §3.
- whisper (implied) - OpenAI speech-to-text.
- recursivellm / recursive-llm - Recursive LLM pipeline tool.
- Reflect - Python reflection (implied).
- reflex - Web framework built on Pynecone (implied).
- reflex - Pythonic web app framework.
- Reflex - Modern Python web framework.

**Hardware/Embedding/Protocols**
- Embeddings (cross-ref §7) - Dense vector representations.
- MCP (Model Context Protocol) - LLM tool protocol.
- FastMCP - Fast MCP server framework.
- Fabric - AI-augmented human framework (implied).
- lakeFS (implied) - Git-like ops for data lakes.
- schedule (cross-ref §1) - Python job scheduling.
- sklego - scikit-learn extra LEGO-style components.
- skops - scikit-learn model serialization.
- Risingwave (cross-ref §1) - Streaming DB.
- River - Online streaming ML library.
- River - Python online ML library.
- Pebble (implied) - Threading + process pools.

**Workflow / Productivity Tools**
- Schedule / Schedulezen (cross-ref §1) - Job schedulers.
- Reflex (cross-ref §10) - Python web framework.
- River (cross-ref §5) - Online ML.
- skops / sklego - scikit-learn extensions.
- DeepDiff (cross-ref §25) - Deep object diffing.
- Fabric (cross-ref §21) - SSH/bash framework.
- skops - sklearn serialization.
- sklego - sklearn extras.
- lakehouse (cross-ref §3/§14) - Combined lake+warehouse.
- lakehouse - General term.

**Visualization / Output**
- Textual - TUI framework.
- Rich - Terminal formatting.
- tqdm - Progress bars.
- yaspin - Spinners.
- humanize - Human-readable values.

**Lightweight Frameworks / Misc Tools**
- Rocketry (implied) - Modern Python scheduling.
- APScheduler - In-process scheduler.
- Schedule - Stdlib-style scheduler.
- Schedulezen - Cron-style scheduler.
- DAG factory - Build Airflow DAGs.
- DAGsHub - DataScience git hosting.
- DVC (Data Version Control) - Git for data.
- River - Online ML.
- RisingWave - Streaming DB.

---

## 33. Drop / Likely Typos or Redundant Entries

These appeared in source with no link/description or seem miscategorized:

- `langduse` - Likely typo for `langfuse` (LLM observability). → If so, §17.
- `parsebench` - Likely parsing benchmark tool, niche.
- `influx DB` - Already covered as InfluxDB (§2).
- `pprisma` - Likely typo for `prisma` (JS ORM).
- `picoclaw` - Likely joke/internal tool, no context.
- `slm.sh` - Possibly a small LLM hosting service.
- `textual` (cross-ref §21) - Covered.
- `chatterbox` (cross-ref §8) - Covered.
- `langduse` - See above.
- `Parsebench` - Benchmarking for parsers.
- `Influx DB` - InfluxDB.
- `pingyy` - Likely typo for `pinggy` (tunneling) — §11.
- `localtonet` - §11.
- `OpenAI Cortex` - Ambiguous; possibly OpenAI internal tool.
- `OpenAI Swarm` - §7.
- `paperclip` - Likely typo for `PaperClip` or unrelated.
- `Capsule Networks` - §5/§31.
- `pandas` - §1.
- `pandas` (duplicate entry in source) - §1.
- `minimax.io` - Anthropic's framework name (in source) — cross-ref §15.
- `cycle` - Generic concept; no specific tool.
- `cyclegan` (implied) - Image-to-image translation.
- `ci/cd` - §13.
- `cli anything` - §15/§21.
- `cleantext` - §8.
- `cleanlab` - §3.
- `cluster computing` - §24 (distributed compute).
- `clustering` - §5/§31.
- `critical chain project management` - §31.
- `customtkinter` - §10.
- `dagster` - §1.
- `dbT core` - §2 DBT.
- `DBT core` - §2.
- `decision trees` - §5.
- `deep learning` - §31.
- `deepdiff` - §25.
- `deepset cloud` - §7.
- `defaultdict` - §25.
- `diffusion models` - §5/§31.
- `distributed systems` - §24.
- `django` - §10.
- `duckdb` - §2.
- `dynamic computation graphs` - §5/§31.
- `eigent` - §7.
- `elastic search` - §9.
- `embeddings` - §7.
- `explainability & interpretability` - §5.
- `feature engineering` - §5.
- `feedforward neural networks` - §5.
- `flowise ai` - §7.
- `generative ai` - §31.
- `gflownet (implied)` - Generative flow networks; absent.
- `github pages` - §10/§13.
- `gnn` - §5 (Graph Neural Networks).
- `gradient boosting` - §5.
- `graph rag` - §7.
- `haystack agents` - §7.
- `helm` - §13.
- `hkuds cli-anything` - §15/§21.
- `httpcore` - §10.
- `httpx` - §10.
- `hunter alpha` - §7.
- `humanize` - §25.
- `hydra` - §26.
- `infinityfree` - §13.
- `instructor` - §6/§7.
- `interpretml` - §5.
- `invoke` - §11.
- `jira` - §13.
- `joblib` - §24.
- `k-means` - §5.
- `kedro` - §1.
- `keras tuner` - §5.
- `kimi` - §6.
- `kubeflow pipelines` - §13.
- `lakehouse (cross-ref §2)` - Lakehouse architecture.
- `lakekeeper` - §3.
- `langchain agents` - §7.
- `langdetect` - §8.
- `langflow` - §7 (LangFlow visual builder).
- `langfuse` - Likely intended for `langduse` (§17).
- `langsmith` - §7.
- `langwatch` - §7.
- `lazy predict` - §5.
- `lime` - §5.
- `linear regression` - §5.
- `litellm` - §7.
- `litestar` - §10.
- `llamaparse` - §7.
- `llm-checker` - LLM evaluation utility.
- `localtonet` - §11.
- `localxpose` - §11.
- `logfire` - §17.
- `logistic regression` - §5.
- `long short term memory` (LSTM) - §5.
- `ltx-2` - Likely a video/LLM model, ambiguous.
- `luigi` - §1.
- `luxtts` - §27.
- `machine learning` - §31.
- `mamba` - §5.
- `markitdown` - §7.
- `mermaid` - §4.
- `minimax.io` - See note above; cross-ref §15/§6.
- `mkdocs` / `mkdocs material` - §10.
- `ml algorithms` - §5/§31.
- `ml metadata` - §3.
- `mlflow` - §3/§5.
- `mlxtend` - §5.
- `model context protocol` - §7/§28.
- `mongodb` - §2.
- `multi agent systems` - §7.
- `multiprocessing` - §24.
- `n8n` - §1.
- `natural language interactions` - §7.
- `netlify` - §10.
- `neural networks` - §31.
- `nextjs` - §10.
- `ngrok` - §11.
- `nhost` - BaaS platform (covered conceptually under §10 backend).
- `nicegui` - §10.
- `nitric` - §10.
- `nodejs` - §10.
- `nosql` - §2.
- `notifypy` - §20.
- `numexpr` - §1/§25.
- `numpy` - §25/§29.
- `open neural network exchange` - §5.
- `openai codex cli` - §15.
- `openai cortex` - §15 (ambiguous).
- `openai swarm` - §7.
- `opencode` - §15.
- `openpyxl` - §1.
- `openrouter` - LLM API router (covered implicitly §6/§7).
- `openwebui` - Self-hosted LLM UI (covered implicitly §10).
- `oracle` - §2/§14.
- `orjson` - §25.
- `paged attention` - §6.
- `pageindex` - §7/§28.
- `pandera` - §3.
- `paramiko` - §12/§21.
- `pdf js` - §7.
- `pdf plumber` - §7.
- `peft` - §6.
- `perplexity` - §7.
- `phind` - §7.
- `playwright` - §11.
- `postgres` - §2.
- `powerbi` - §4.
- `prefect` - §1.
- `pca` - §5/§29.
- `pprisma` - Likely typo for `prisma`.
- `probabilistic models & bayesian ml` - §5/§31.
- `prometheus` - §17.
- `pyarmor` - §12.
- `pyautogui` - §11.
- `pydantic` - §25.
- `pyfilesystem2` - §25.
- `pygui` - §10.
- `pyinstrument` - §17.
- `pyjanitor` - §1.
- `pypdf2` - §7.
- `pypdfium2` - §7.
- `pypika` - §2.
- `pysbd` - §8.
- `pyscript` - §10.
- `pyside6` - §10.
- `pytesseract` - §8.
- `python dotenv` - §22/§26.
- `python named tuples` - §25.
- `python-jose` - §12.
- `pyttsx3` - §27.
- `pywebview` - §10.
- `pywhat` - §12.
- `rag systems` - §7.
- `random forest` - §5.
- `ray` / `ray serve` - §5/§6.
- `react js` - §10.
- `recursive-llm` - §7.
- `reflex` - §10/§32.
- `reinforcement learning` - §31.
- `replit` - Cloud IDE/hosting (§13).
- `rich` - §25.
- `risingwave` - §1.
- `river` - §32.
- `robocorp` - RPA framework (§32 niche).
- `robyn` - §10.
- `sarvam ai` - Indian-language LLM platform (implied §6).
- `scala` - §21/§32.
- `scalable & distributed training` - §5.
- `schedule` / `schedulezen` - §1.
- `scikit-learn` - §5.
- `scrapling` - §11.
- `secrets` - §26.
- `secure` - §12 (general).
- `semantic search` - §9.
- `seq2seq architecture` - §5.
- `serp api` - §7.
- `sh` - §21.
- `shap` - §5.
- `sklego` - §32.
- `skops` - §32.
- `slim.sh` - Shell tool, ambiguous.
- `spacy` - §8.
- `speechma` - §8/§27.
- `sql server` - §2.
- `sql alchemy` - §2.
- `sqlglot` - §2.
- `sqlite` - §2.
- `sqlmodel` - §2.
- `ssis` - §1.
- `sqlsoup` - §2.
- `superclaude` - Niche AI assistant (§15).
- `surge.sh` - §10/§13.
- `swifter` - §1.
- `tabnine` - §15.
- `tavily` - §7.
- `telethon` - Telegram client library (§32 niche).
- `temp oral.io` (likely `temporal.io`) - Workflow engine (§1/§18).
- `tensorflow extended` - §5.
- `tensorflow hub` - §5.
- `tensors` - §29 (general).
- `terraform` - §13.
- `text distance` - §8.
- `text generation interface` - §6.
- `textacy` - §8.
- `textblob` - §8.
- `textual` - §25/§32.
- `threading` - §24.
- `tiktoken` - §8.
- `time series models` - §5.
- `toga` - §10.
- `tokenization` - §8.
- `torchaudio` - §27.
- `torch vision` - §27.
- `tqdm` - §25.
- `tracemalloc` - §17.
- `transfer learning` - §5/§31.
- `tree based models` - §5.
- `pretrained models` - §5/§31.
- `ui-tars` - Computer-use AI agent (§7/§32).
- `unidecode` - §8.
- `unsloth` - §6.
- `unsupervised learning` - §5/§31.
- `uv` - §22.
- `uvicorn` - §10/§24.
- `vaex` - §1.
- `variational autoencoders` - §5.
- `vercel` - §10/§13.
- `vision transformers` - §5/§27.
- `vscode debug` - §15.
- `watchdog` / `watchfiles` - §1.
- `wrapt` - §25.
- `xlwings` - Excel-Python interop (§1).
- `yarl` - §25.
- `yaspin` - §25.
- `zapier` - §1/§18.
- `zappa` - §10.

---

## Quick Reference: Cross-Reference Hot Spots

- **Vector DBs**: §2 ↔ §7 ↔ §9.
- **LLM orchestration**: §6 ↔ §7 ↔ §15 (Coding agents that are LLM-driven).
- **Observability**: §3 (data) ↔ §17 (infra) ↔ §7 (LLM-specific).
- **Distributed compute**: §1 (Dask/Spark) ↔ §5 (Ray) ↔ §24.
- **Workflow engines**: §1 (Airflow/Dagster/Prefect) ↔ §18 ↔ §13 (CI/CD).
- **Streaming**: §1 ↔ §19.
- **Document parsing**: §7 ↔ §8.
- **AI Coding**: §15 spans IDEs, assistants, agents, CLI.
- **Quantization/optimization**: §6 (LLM) ↔ §5 (general).
- **Security**: §12 ↔ §13 (network/infra) ↔ §17 (audit).