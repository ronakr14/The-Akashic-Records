String Matching
1. fuzzywuzzy - https://github.com/seatgeek/fuzzywuzzy.git - fuzzy string matching
2. rapidfuzz - https://github.com/rapidfuzz/RapidFuzz.git - High-performance fuzzy string matching
3. Jellyfish - https://github.com/jamesturk/jellyfish.git - phonetic matching
4. thefuzz - https://github.com/seatgeek/thefuzz.git - fuzzy string matching

Web Application
1. Chainlit - chat-based UIs for LLM apps
2. Streamlit - data apps and dashboards
3. Gradio - Dashboard with minimal code

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

LLM Optimization
BitNet-Run **ultra-efficient 1-bit/low-bit LLMs** on edge or low-resource hardware
GGUF Quantization - better for **practical, widely-supported quantization**
KVCache = Speed up LLM inference by caching past key/value states for efficient token-by-token generation
Attention Mechanism - Focus model on relevant parts of input sequences to improve NLP, vision, and multimodal tasks using Attention Mechanisms.
RNN - Sequential data modeling (time series, speech, NLP) where temporal dependencies 
Transformers - State‑of‑the‑art **NLP and multimodal model library**
Pytorch Lightning - Structure and scale PyTorch training with clean, modular cod
DSPY - Programmatic optimization of LLM pipelines 



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
