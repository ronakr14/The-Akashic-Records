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
5. render-Fully managed **cloud platform for deploying web apps, APIs, and static sites**
6. fly.io
7. heroku
8. infinityfree
9. railway

Data Visualization
1. Dash (Plotly) - Dynamic Charts and Dashboard
2. Matplotlib - Simple, Static Plots, minimal Overhead
3. superset-Enterprise-grade **open-source BI platform**
4. metabase-simpler setup and faster adoption for non-technical user
5. d3-Low-level **[[JavaScript]] visualization library** for building fully custom
6. plotly-**faster development with prebuilt interactive charts instead of custom rendering from scratch**.

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
6. LangExtract-Structured data extraction from unstructured text using LLMs
7. pydanticai-Building structured, type-safe LLM apps in Python
8. Python Protocols-Define structural typing
9. Abstract Base Classes-explicit inheritance and stricter interface enforcement.
10. pyinputplus-Robust CLI input validation with retries, defaults, and type checks
11. Click-ull-featured, scalable command-line apps with better UX

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
supervised learning-Predicting known targets (classification/regression) from labeled data
Semi-Supervised & Weak Supervision
TensorRT-High-performance deep learning inference on NVIDIA GPUs
Support Vector Machines-High-dimensional, small-to-medium datasets (e.g., text classification, bioinformatics) where clear margin separation boosts accuracy using Support Vector Machines.
Random Forest-aster training, better scalability, and less tuning on large datasets


LLM Optimization
BitNet-Run **ultra-efficient 1-bit/low-bit LLMs** on edge or low-resource hardware
GGUF Quantization - better for **practical, widely-supported quantization**
KVCache = Speed up LLM inference by caching past key/value states for efficient token-by-token generation
Attention Mechanism - Focus model on relevant parts of input sequences to improve NLP, vision, and multimodal tasks using Attention Mechanisms.
RNN - Sequential data modeling (time series, speech, NLP) where temporal dependencies 
Transformers - State‑of‑the‑art **NLP and multimodal model library**
Huggingface transformers-End-to-end model lifecycle—load, fine-tune, and deploy state-of-the-art NLP/vision models
Pytorch Lightning - Structure and scale PyTorch training with clean, modular cod
DSPY - Programmatic optimization of LLM pipelines 
Bits & Bytes-Memory-efficient **8-bit/4-bit quantization + optimizers** for training and running LLMs on limited GPUs
Accelerate-Hugging Face]] Accelerate is a lightweight orchestration layer for distributed [[pytorch]] training and inference
deepseed-Train and serve large-scale deep learning models efficiently
Fully Sharded Data Parallel-Memory-efficient large model training by sharding parameters, gradients,
Transformer Reinforcement Learning-Hugging Face **TRL (Transformer Reinforcement Learning)** library for fine-tuning LLMs with **RLHF, DPO, PPO**
Agentic Chunking-Dynamic, LLM-driven chunking that adapts to context and intent
Static Chunking-better for predictable performance, speed, and simpler pipelines
vllm-High-throughput LLM serving with efficient batching
openllm-Deploying and serving open-source LLMs as APIs with standardized packaging
Sequence & Generative Modeling-Modeling time-ordered or structured data (text, speech, time series) and generating new content
Hidden Markov Models-simpler, interpretable models for smaller datasets or constrained systems
llmfit-Hardware-aware **LLM selection CLI** that scans your CPU/GPU/RAM and recommends the **best-fit local models (with quantization + performance estimates)**

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
LakeWatch-Real-time **data lake observability and monitoring**
MonteCarlo
Great Expectations

Data Lakes:
Iceberg - Open table format for large-scale data lakes. multi-engine interoperability
Delta Lake - ACID-compliant data lake storage for reliable batch + streaming pipelines 

Data Lake Processing
Hudi - Incremental data lake processing
Dask-Parallel computing for [[python]]—scale pandas-like workflows across cores
Pyspark-Distributed data processing for large-scale ETL and analytics
Koalas-Pandas-like API on top of Spark
Pandas-Structured data manipulation and analysis
polars-High-performance DataFrame engine for fast ETL and analytics


Data Platforms:
Databricks - Unified data + AI platform for large-scale ETL, streaming, and ML on lakehouse architecture
Snowflake - Cloud data warehouse for scalable analytics
BigQuery-Serverless, petabyte-scale analytics warehouse for fast [[sql]] on massive datasets
Redis-Ultra-fast in-memory store for caching, session management
DiskCache-Persistent, disk-backed caching for Python apps
Valkey-In‑memory key‑value datastore for ultra‑low‑latency caching
Memcached-


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
Oracle Cloud-Enterprise **cloud platform** for running Oracle databases, ERP, and business apps
Microsoft Azure-Enterprise cloud for Microsoft-heavy ecosystems


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
LangChain-Rapidly build LLM apps with chaining, tool calling, and integrations 
LlamaIndex-Building RAG pipelines—ingestion, indexing, and retrieval over private
chunkr-Intelligent document chunking for RAG
ragflow-End-to-end **RAG (Retrieval-Augmented Generation) pipeline platform**
Text Splitter-Chunking large documents into token-aware segments for embeddings/RAG
Anything LLM-Self-hosted AI workspace to chat with your private docs
Dify.AI-Open-source **LLMOps + agentic workflow platform** to build, deploy, and manage AI apps
DeerFlow-Coordinating long‑horizon, multi‑step AI workflows 
Promptify-Quickly generating structured prompts for NLP tasks
Semantic Kernel-Build **enterprise AI apps with structured orchestration**
Sentence Transformers-Semantic search, clustering, and RAG
OpenAI Embeddings-high-quality embeddings without infra overhead


Test Automation
Robot Framework -Enterprise‑grade **keyword‑driven test automation** for web, API, and desktop apps
Pytest-Write concise, scalable unit/integration tests with fixtures and powerful plugins
Unittest- zero dependencies and strict, built-in structure

API:
fastapi-High-performance Python APIs with automatic validation
hoppscotch-Lightweight, browser-based API testing with real-time requests
postman-Collaborative API testing and debugging with collections, environments, and automated checks
Insomnia-ighter, faster UI with strong GraphQL support and less overhead

LLM Orchestration
langgraph = Stateful, deterministic orchestration of LLM agents
Microsoft Autogen -  faster prototyping of conversational
OpenDevin-Autonomous AI software engineer for end-to-end dev tasks
AutoGPT-Autonomous goal-driven agents that plan and execute multi-step tasks with minimal supervision
eigent-Local‑first multi‑agent AI workforce desktop platform
AgentGPT-lighter autonomous agent setup when you want cloud/quick experiments
CrewAI-Coordinate multi-agent LLM teams with role-based collaboration
Haystack cloud-Production-ready RAG pipelines with managed orchestration
Get Shit Done-Opinionated, no‑nonsense AI‑assisted
Getting Things Done (GTD)

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
sender-Lightweight **email sending and automation service** for transactional and marketing emails
sendgrid-**high-volume delivery, deliverability monitoring, and advanced email templates**.
resend-Developer-first transactional email platform for sending, testing, and managing application emails
Postmark
Postal
Mailgun

Video Encoding
zencoder-Cloud-based video encoding/transcoding pipelines
AWS elemental MediaConvert-

Retry Mechanism
Tenacity-Robust retry logic for unreliable operations
Backoff-simpler, lightweight retry use cases
RetryLib-Adding robust retry logic


LLM Models
Mistral-High-performance open-weight LLMs for cost-efficient inference
OpenAI-top-tier reasoning, reliability, and managed APIs
Nemotron-NVIDIA’s enterprise-grade LLM family optimized for high-performance reasoning, coding, and agent workflows
Claude-Long-context reasoning and document-heavy workflows
Gemini-Multimodal reasoning across text, code, images, and video
GLM-5-Open‑source frontier‑class **foundation LLM** optimized for **long‑horizon agentic tasks, deep reasoning, systems engineering, and production‑grade coding workflows
ChatGPT-General-purpose AI assistant for reasoning, coding, writing, and problem-solving**
Llama 3- open-source flexibility and easier deployment 
onefilellm-Packaging an entire codebase or context into a single file for LLM ingestio
Sourcegraph Cody-continuous, repo-aware assistance without manual bundling

Logging
Logger-Basic application logging using built-in frameworks
StructLog-Structured, context-rich logging in Python services
Logguru-Simple, developer-friendly logging in Python with minimal setup
Loki-Cost-efficient, label-based log aggregation tightly integrated with Prometheus

Programming Language
Javascript-Build interactive web apps and full-stack systems
typescript-Add static typing to JavaScript for large-scale frontend/backend apps
BASH-Automate system workflows, data pipelines, and [[DevOps]] tasks via shell scripting and CLI orchestration.
Python-Rapid backend, data engineering, and AI/ML development


Version Control
Data Version Control-Track and version datasets, models, and pipelines alongside code
Git LFS
Bitbucket-Git repo hosting tightly integrated with Atlassian stack 
github-Centralized code hosting and collaboration with strong ecosystem
gitlab-



Git]Hub Speckit-Spec-driven development in GitHub
confluence-centralized team knowledge base for structured docs
notion-lexible, intuitive editing and lightweight knowledge sharing.



agentic rag
ai agents
airflow
anomaly detection
ansible
arrow
artificial intelligence
AST
Async
Aurora
AutoEncoders
Autogen
Bandit
Beanie
Beartype
BentoML
Blockchain
BM25
BUsiness Intelligence
capsule networks
change data capture
chatterbox
CICD
Classic RAG
Claude Mem
Claw agents
Claw router
Cleanlab
cleantext
CLI anything
Cloud computing
cloud run
cluster computing
clustering
conda
container service
containers & observations
CNN
coolify
Cost Attribution Engine
Critical Chain Project Management
crontab
cuda
customtkinter
DAG factory
dagshub
dagster
Data factory
Data migration
Data obfuscation
Datafusion
DBT core
debugpy
decision trees
deep learning
deepdiff
deepset cloud
defaultdict
diffusers
diffusion models
distributed systems
django
dots.ocr
duckdb
Dynamic Computation Graphs
dynamodb
EEL
Elastic Search
Embeddings
Ethical Hacking
Explainability & Interpretability
fabric
faker
fastmcp
Feature Engineering
Feedforward Neural Networks
fire
click
flashtext
flask
flashtett
flet
flowise ai
fumadocs
functools
Gemini CLI
Gemini Embeddings
Generative AI
gitpython
Generative Models
GitHub Pages
Gooey
Gradient Boosting
Grafana
Grafana Cloud
Graph Neural Networks
Postgres PgVector
Graph RAG
Haystack Agents
Helm
HKUDS CLI-Anything
Heroku
Httpcore
httpx
Hunter Alpha
humanize
hydra
IBM Granite-Docling
Influx DB
Infinityfree
Instructor
InterpretML
Invoke
Jira
Joblib
k-means
kedro
keras tuner
keyboard
kimi
kubeflow pipeliens
lakekeeper
langchain agents
langdetect
langflow
langduse
langsmith
langwatch
lazy predict
lime
linear regression
litellm
litestar
lllamacoder
llm-checker
llamaparse
localtonet
localxpose
logfire
logistic regression
long short term memory
ltx-2
luigi
luxtts
machine learning
mamba
manifest
markitdown
mermaid
minimax.io
mkdocs
mkdocs material
ml algorithsms
ml metadata
mlflow
mlxtend
model context protocol
mongodb
multi agent systems
multiprocessing
n8n
NLP
Natural language interactions
netlify
neural networks
nextjs
ngrok
nhost
nicegui
nitric
nodejs
nosql
notifypy
numexpr
numpy
Open Neural Network Exchange
Openshell
openai codex cli
openai cortex
openai swarm
opencode
openjarvis
openpyxl
openrouter
openwebui
oracle
orjson
paged attention
pageindex
pandera
paperclip
paramiko
parsebench
pdf js
pdf plumber
peft
perplexity
phind
picoclaw
pingyy
postgres
powerbi
prefect
PCA
pprisma
Probabilistic Models & Bayesian ML
prometheus
propositions
pyarmor
pyautogui
pydantic
pyfilesystem2
pygui
pyinstrument
pyjanitor
pypdf2
pypdfium2
pypika
pysbd
pyscript
pyside6
pytesseract
python dotenv
Python Named Tuples
python-jose
pyttsx3
pywebview
pywhat
RAG Systems
Railway
Random Forest
Gradient Boosting
Ray
Ray Serve
 React JS
 Recursive-llm
 reflex
 reinforcement learning
 replit
 rich
 risingwave
 river
 robocorp
 robyn
 sarvam ai
 scala
 Scalable & Distributed Training
 schedule
 schedulezen
 scikit-learn
 scrapling
 secrets
 secure
 semantic search
 seq2seq architecture
 serp api
 sh
 Shapley Additive exPlanations
 sklego
 skops
 slim.sh
 spacy
 speechma
 sql server
 sql alchemy
 sqlglot
 sqlite
 sqlmodel
 ssis
 sqlsoup
 superclaude
 surge.sh
 swifter
 tabnine
 tavily
 telethon
 remporal.io
 tensorflow extended
 tensorflow hub
 tensors
 terraform
 text distance
 text generation interface
 textacy
 textblob
 textual
 threading
 tiktoken
 time series models
 toga
 tokenization
 torchaudio
 torch vision
 tqdm
 tracemalloc
 transfer learning
 tree based models
 Pretrained Models
 ui-tars
 unidecode
 unsloth
 unsupervised learning
 uv
 uvicorn
 vaex
 variational autoencoders
 vercel
 vision transformers
 vscode debug
 watchdog
watchfiles
wrapt
xlwings
yarl
yaspin
zapier
zappa
