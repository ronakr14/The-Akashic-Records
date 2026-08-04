---
domain: software-engineering
subdomain: storage-gateway
note_type: technology
source_type: github
status: reference
level: advanced
tags:
  - github
  - storage-gateway
  - cloud-storage
  - platform-engineering
  - architecture
---
# AI Summary
Comprehensive architectural review of the 9Drive open-source project, a storage gateway that unifies multiple Google Drive accounts and S3-compatible providers behind a single dashboard. The analysis examines the system's architecture, upload routing, storage abstraction, deployment model, scalability, security posture, engineering trade-offs, enterprise readiness, and relevance to data engineering and AI workflows. It also extracts reusable design patterns, best practices, interview questions, and architectural lessons for building storage and platform services.

---

# 1. Executive Summary

## What is this project?

9Drive is a **storage gateway web app** that connects multiple Google Drive accounts into a single virtual storage dashboard, with optional S3-compatible storage support. It lets users sign up, connect accounts, upload files, preview them, organize via virtual folders, track quota, and manage uploads through a backend that picks the best storage target. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

## What problem does it solve?

It solves the awkward problem of **fragmented cloud storage**: too many Google Drive accounts, quota limits, and manual juggling. Instead of treating each Drive as a separate island, 9Drive presents a unified layer and can route uploads to the account with enough free space. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

## Who is the target audience?

The target audience appears to be:

- power users with multiple Google Drive accounts,
    
- small teams or solo operators needing cheap storage pooling,
    
- developers who want an API-driven upload gateway,
    
- anyone wanting a lightweight “storage orchestration” layer without building one themselves. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))
    

## Maturity level

This is best classified as a **strong prototype / early production system**. Why not fully production-ready? Because the repo has a surprisingly broad feature set, but the security posture and operational hardening look incomplete: there is no detected `SECURITY.md`, the README itself warns about production caveats like HTTPS, secure cookies, OAuth verification, and stronger token storage, and public commentary around the project has flagged security concerns. ([GitHub](https://github.com/zenhosta/9drive/security?utm_source=chatgpt.com "Security - zenhosta/9drive"))

---

# 2. Repository Overview

## Main purpose of the repository

The repository implements a **two-sided storage platform**:

1. a frontend dashboard for users,
    
2. a backend API that brokers authentication, storage routing, quota tracking, uploads, and synchronization. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))
    

## Core features and capabilities

The README lists these major capabilities:

- Google Drive and S3-compatible storage gateway
    
- direct upload streaming without storing files on the server
    
- routing uploads by availability, round-robin, or priority
    
- external upload API with API keys
    
- authentication via email/password or Google
    
- quota summary and quota tracker
    
- manual sync from Drive back into MySQL
    
- virtual folders
    
- file preview, download, rename, move, delete
    
- in-app API docs with cURL and JavaScript examples
    
- bearer-token authentication
    
- encrypted Google OAuth config in DB
    
- automated updates through `update.sh` and PM2
    
- optional reCAPTCHA
    
- MySQL + Prisma migrations
    
- Express + TypeScript backend
    
- React + Vite frontend ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))
    

## Key technologies, frameworks, and programming languages

The repo is explicitly built with:

- **TypeScript**
    
- **Express**
    
- **React**
    
- **Vite**
    
- **Prisma**
    
- **MySQL**
    
- **Google Drive API**
    
- **S3-compatible storage APIs**
    
- **PM2**
    
- plus Node.js 20+ as a runtime requirement. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))
    

## High-level architecture inferred from the codebase

This looks like a classic **frontend / backend / persistence / external integration** architecture:

- **Frontend**: user dashboard, settings, upload UI, quota views, docs.
    
- **Backend**: auth, routing, Drive/S3 adapters, upload streaming, sync logic.
    
- **Persistence layer**: MySQL through Prisma.
    
- **External systems**: Google OAuth, Google Drive, S3-compatible providers, reCAPTCHA. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))
    

---

# 3. How It Works

## Workflow in simple terms

A user signs in, connects one or more storage accounts, and then uploads or manages files from one dashboard. The backend decides where files go, streams data directly to the target storage, and updates metadata in MySQL so the dashboard stays consistent. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

## Major components/modules

The repo structure shown in the README is simple but telling:

- `backend/` — Express API, Prisma schema, Google Drive integration
    
- `frontend/` — Vite React app
    
- root scripts/configs — Docker, setup, update, environment templates. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))
    

## Data flow and execution flow

A likely flow is:

1. User logs in or signs up.
    
2. OAuth or password auth creates a session/token.
    
3. User connects Google Drive or configures S3-compatible storage.
    
4. Upload request lands in the backend.
    
5. Backend applies routing policy:
    
    - most available
        
    - round robin
        
    - priority order
        
6. Backend streams the file to the chosen storage target.
    
7. Metadata is written to MySQL via Prisma.
    
8. Frontend reflects quota, file list, and upload status. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))
    

## Integrations and dependencies

The project integrates with:

- Google OAuth / Google Drive APIs,
    
- S3-compatible endpoints like MinIO, Cloudflare R2, Wasabi, Backblaze B2, AWS S3,
    
- MySQL,
    
- Prisma migrations,
    
- PM2 for process management,
    
- optional reCAPTCHA. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))
    

---

# 4. Why This Project Exists

## Business problem it addresses

This solves a very real cost and convenience problem: **storage fragmentation and quota exhaustion**. Users often split files across accounts or providers. 9Drive tries to centralize that mess into one operational surface. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

## Technical challenges it solves

It handles:

- multi-account auth and connection lifecycle,
    
- credential storage and encryption,
    
- upload routing logic,
    
- direct streaming so files do not sit on the app server,
    
- metadata sync between external storage and relational DB,
    
- mixed provider support. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))
    

## Advantages over traditional approaches

Traditional approaches are:

- one Drive account per user,
    
- manual file shuffling,
    
- or simple file managers that do not route or pool storage.
    

9Drive’s advantages are:

- unified access,
    
- routing based on quota,
    
- provider abstraction,
    
- API access,
    
- direct streaming, so the backend is not acting as a file warehouse. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))
    

## Unique innovations or differentiators

The differentiators are:

- upload routing policies,
    
- “virtual” unified storage dashboard,
    
- support for both Google Drive and S3-like storage,
    
- external API-key upload endpoint,
    
- encrypted global OAuth config managed through UI,
    
- automated update flow for VPS/PM2 setups. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))
    

---

# 5. How It Can Be Used

## 1) Personal multi-account storage hub

**Description:** Centralize multiple Google Drives into one dashboard.  
**Example scenario:** You have personal, work, and side-project Drive accounts and want one upload surface.  
**Expected benefits:** Less context switching, easier quota management, unified search/organization.  
**Complexity:** Low. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

## 2) Small-team storage router

**Description:** Route uploads across several storage backends based on available space or policy.  
**Example scenario:** A small startup needs to spread uploaded assets across multiple storage targets without building custom infra.  
**Expected benefits:** Better capacity utilization, less manual ops.  
**Complexity:** Medium. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

## 3) Upload gateway for applications

**Description:** Use the API key upload endpoint as a backend storage ingress.  
**Example scenario:** Another app uploads files to 9Drive via `POST /api/v1/uploads`.  
**Expected benefits:** Decoupled upload handling, centralized storage policies, simpler app code.  
**Complexity:** Medium. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

## 4) Cheap cloud storage federation

**Description:** Treat multiple S3-compatible buckets/providers as one logical store.  
**Example scenario:** Use R2 for some traffic, Backblaze for cold storage, MinIO internally.  
**Expected benefits:** Cost flexibility, provider abstraction, fallback options.  
**Complexity:** High. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

## 5) Storage quota visibility tool

**Description:** Track per-account quota across connected storage systems.  
**Example scenario:** Operator monitors usage before uploads fail.  
**Expected benefits:** Avoid quota surprises, better planning.  
**Complexity:** Low. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

---

# 6. Where It Can Be Used

## Data Engineering

Moderately relevant. It can act as a file ingress/egress layer for staging datasets, especially if the pipeline involves uploaded artifacts or interchange files. Not a core ETL engine, though. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

## Analytics

Useful as a lightweight document/data staging store, but not a BI or warehouse tool. It helps move and organize files; it does not analyze them. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

## AI/ML

Relevant for dataset intake, model artifact storage, and shared file access. It could support training data distribution, but it is not an AI-native system. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

## DevOps

Useful for artifact routing, upload APIs, and storage abstraction. The update script and PM2 support also make it operationally interesting. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

## Platform Engineering

Good fit for building an internal storage abstraction layer or “storage service platform.” This is where the project makes the most architectural sense. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

## Cloud Engineering

Very relevant because it spans Google Drive, S3-compatible endpoints, authentication, and cloud-native deployment concerns. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

## Security

Relevant, but mostly as a cautionary example. The repo stores encrypted credentials and hashed tokens, but the public-facing setup notes and absence of a security policy mean hardening is still a major concern. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

## FinOps

Potentially useful for storage cost optimization through routing across multiple providers and accounts. It is not a FinOps platform, but it helps with the storage-cost angle. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

## Product Engineering

Useful if your product needs user-facing upload, file management, and storage abstraction features. It gives a working reference architecture. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

## Enterprise Applications

Possible, but only after serious security, compliance, observability, and governance upgrades. Right now it feels too rough for serious enterprise use out of the box. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

---

# 7. Key Components Analysis

Because I did not fetch the full file tree and source files, this part is inferred mainly from the README and top-level structure. That means the component analysis is directionally correct, but not line-by-line verified.

## `backend/`

**Purpose:** API server and storage orchestration layer.  
**Responsibilities:** auth, file routing, Drive/S3 integrations, quota sync, metadata persistence.  
**Important classes/functions:** likely route handlers, services, Prisma access layer, adapter code.  
**Interactions:** talks to frontend, MySQL, Google APIs, and S3 providers. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

## `frontend/`

**Purpose:** User dashboard.  
**Responsibilities:** auth screens, settings, quota view, file browser, upload panel, docs.  
**Important classes/functions:** likely React components for upload, folder browsing, settings, previews.  
**Interactions:** consumes backend APIs and displays storage state. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

## `docker-compose.yml`

**Purpose:** local or containerized deployment orchestration.  
**Responsibilities:** bring up app and likely MySQL and related services.  
**Interactions:** used in dev or self-hosted deployment. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

## `.env.docker.example`

**Purpose:** environment template.  
**Responsibilities:** documents required runtime config.  
**Interactions:** deployment/bootstrap support. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

## `setup.ps1` / `update.sh`

**Purpose:** automation scripts for setup and lifecycle operations.  
**Responsibilities:** install, build, migrate, update, restart.  
**Interactions:** Prisma, npm, git, PM2. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

---

# 8. Setup and Adoption

## Installation requirements

The README says you need:

- Node.js 20+
    
- npm
    
- MySQL
    
- a Google Cloud project
    
- Google OAuth Client ID/Secret. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))
    

## Deployment options

The project supports:

- automated setup,
    
- manual installation,
    
- local development,
    
- native VPS deployment with PM2,
    
- Docker-based setup through compose files. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))
    

## Infrastructure requirements

Minimum practical infra:

- app server,
    
- MySQL database,
    
- internet access to Google APIs and S3 providers,
    
- secure secret handling,
    
- HTTPS in production. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))
    

## Learning curve

Moderate. The UI may be easy, but the integration model is not trivial because it mixes auth, cloud APIs, upload routing, encrypted config, and operational setup. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

## Operational considerations

The README itself warns about production precautions:

- change localhost redirect URIs,
    
- configure OAuth origins,
    
- use strong secrets,
    
- put the backend behind HTTPS,
    
- consider secure cookies or stronger token storage. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))
    

---

# 9. Strengths and Weaknesses

## Strengths

**Scalability:**  
Good architectural idea for horizontal storage abstraction; direct streaming avoids local file accumulation. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

**Maintainability:**  
TypeScript + Prisma + explicit project structure is a solid stack choice. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

**Extensibility:**  
The storage adapter idea and routing modes make it reasonably extensible. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

**Performance:**  
Streaming uploads directly to target storage is the right move. That’s not glamorous, but it’s how you avoid self-inflicted pain. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

**Developer Experience:**  
Automated setup, in-app docs, and clear environment guidance help adoption. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

## Weaknesses

**Risks:**  
Security appears immature. The repo lacks a `SECURITY.md`, and external reporting has highlighted severe concerns. ([GitHub](https://github.com/zenhosta/9drive/security?utm_source=chatgpt.com "Security - zenhosta/9drive"))

**Limitations:**  
Heavily tied to Google Drive and account-based storage semantics. That can be a blessing or a trap. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

**Missing features:**  
No visible evidence of robust RBAC, audit logging, backup strategy, rate limiting, or enterprise governance in the README. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

**Technical debt indicators:**  
The presence of self-update scripts, broad feature scope, and production caveats suggests the project may be moving fast and paying for it later. That is common, and also how systems wake up one morning with a security blog post attached. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

---

# 10. Enterprise Evaluation

## Production readiness: 5/10

There is real structure, but not enough evidence of hardening, governance, and operational maturity. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

## Security: 4/10

Token encryption exists and the README shows some security awareness, but the lack of a security policy and public criticism around exposure risk are big red flags. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

## Scalability: 6/10

The streaming model and provider abstraction help, but we do not see proof of load testing, queueing, or distributed architecture. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

## Observability: 4/10

The README mentions real-time rebuild progress in settings, but there is no visible evidence of structured logs, metrics, tracing, or alerting. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

## Documentation quality: 7/10

The README is unusually detailed, with setup, security notes, and deployment steps. That is a strong point. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

## Community support: 6/10

Open-source traction is solid for a young repo: stars, forks, issues, and a visible live preview. But the ecosystem is still small. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

## Maintainability: 6/10

The stack is maintainable, but the feature surface is wide and the security/ops burden is non-trivial. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

---

# 11. Comparison with Alternatives

## Likely alternatives

- direct Google Drive management
    
- S3 bucket dashboards
    
- self-hosted file managers
    
- storage abstraction layers built in-house
    
- cloud storage gateways / federated file management tools
    

## Comparison

**Features:**  
9Drive is broader than a simple file manager because it supports account pooling, routing, and mixed storage providers. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

**Complexity:**  
Higher than a basic dashboard, lower than building a custom storage platform from scratch. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

**Performance:**  
Potentially strong for uploads due to streaming; performance will depend on upstream provider latency. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

**Cost:**  
Likely low to moderate, since it can leverage existing storage accounts and S3-compatible services. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

**Ecosystem:**  
Smaller than mature storage vendors or commercial file platforms. That means less battle-testing. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

---

# 12. Engineering Takeaways

## Important design patterns used

- **Gateway pattern** for storage abstraction
    
- **Adapter pattern** for Google Drive / S3 providers
    
- **Policy-based routing** for upload destination selection
    
- **Separation of concerns** between frontend, backend, and persistence
    
- **Streaming-first data path** to avoid server-side file buffering. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))
    

## Architectural lessons

- Do not treat object storage like a local filesystem if you can avoid it.
    
- Keep upload paths streaming and stateless where possible.
    
- If you pool heterogeneous providers, you need a clean abstraction or the codebase turns into spaghetti wearing a fake mustache. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))
    

## Best practices worth adopting

- encrypted secret storage,
    
- Prisma migrations,
    
- explicit setup scripts,
    
- in-app API docs,
    
- upload routing policies,
    
- config templates. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))
    

## Anti-patterns if any

- public-facing feature breadth outrunning security hardening,
    
- self-updating production logic without strong governance,
    
- too much operational trust placed in a young codebase. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))
    

---

# 13. Interview Preparation

## 10 beginner questions

1. What problem does 9Drive solve?
    
2. What is the difference between Google Drive support and S3-compatible support here?
    
3. Why is streaming uploads directly useful?
    
4. What is a virtual folder?
    
5. Why does the app need MySQL?
    
6. What does Prisma do in this project?
    
7. What is the purpose of the frontend dashboard?
    
8. Why might a user need multiple storage accounts?
    
9. What is the upload API used for?
    
10. Why does the app track quota?
    

## 10 intermediate questions

1. How does routing uploads by “most available” differ from round-robin?
    
2. How would you design the storage adapter layer?
    
3. Why store OAuth config encrypted in the database?
    
4. How would you synchronize external Drive state back into MySQL?
    
5. What tradeoffs come with bearer-token auth here?
    
6. How would you design file preview permissions?
    
7. Why might direct streaming be better than temporary disk storage?
    
8. How do API keys differ from user session tokens in this architecture?
    
9. How would you validate upload size and target availability?
    
10. How do setup scripts improve adoption?
    

## 10 advanced architecture questions

1. How would you redesign this for multi-tenant enterprise isolation?
    
2. What failure modes exist when routing uploads across heterogeneous providers?
    
3. How would you make upload routing idempotent and transactional?
    
4. How would you build observability for upload latency and provider failures?
    
5. How would you secure token lifecycle management end to end?
    
6. How would you scale metadata sync across many Drive accounts?
    
7. How would you add RBAC and audit logging?
    
8. How would you support eventual consistency between DB and provider state?
    
9. How would you design a fallback strategy when a provider becomes unavailable?
    
10. Would you keep this as a monolith or split it into services, and why?
    

---

# 14. Handoff Summary

## 1-page executive summary

9Drive is a full-stack storage gateway that unifies multiple Google Drive accounts and S3-compatible backends into a single dashboard. It supports auth, routing, upload streaming, quota tracking, virtual folders, and metadata sync. The architecture is practical and thoughtfully assembled around a TypeScript/Express backend, React/Vite frontend, MySQL, and Prisma. Its most interesting feature is upload routing across storage targets with different policies. Its biggest weakness is security and operational maturity: it lacks visible enterprise-grade controls, and public commentary has flagged serious exposure risks. In other words: very useful as a reference implementation or personal/self-hosted tool, not something I’d shove into a regulated enterprise without a lot more work. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

## Key findings

- Strong storage abstraction and unified dashboard idea. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))
    
- Direct streaming is the right engineering choice. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))
    
- Security and governance are the biggest gaps. ([GitHub](https://github.com/zenhosta/9drive/security?utm_source=chatgpt.com "Security - zenhosta/9drive"))
    

## Recommended adoption scenarios

- Personal or small-team storage federation
    
- Hackathon or prototype reference
    
- Internal tooling with controlled trust boundaries
    
- Learning project for gateway/storage architecture. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))
    

## Decision matrix

**Use:** personal/self-hosted storage gateway, prototype for storage orchestration, upload routing reference.  
**Evaluate:** internal platform service after hardening, especially if you need quota-aware routing.  
**Avoid:** regulated enterprise production, sensitive data workflows, or any environment requiring audited security posture out of the box. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

---

# 15. AI/Data Engineering Relevance

## Can this repository be used in data platforms?

Yes, as a **file ingress/storage gateway** for staging files, datasets, exports, and artifacts. It is not a processing engine, but it can sit in front of one. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

## Can it be integrated into a lakehouse architecture?

Yes, but only as the **edge ingestion layer** or file gateway. It would not replace object storage, catalog, or compute layers. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

## Can it improve ETL/ELT pipelines?

Indirectly, yes. It can simplify upload collection, staging, and routing. It does not itself transform data, orchestrate jobs, or manage lineage. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

## Can it be used for LLM, RAG, agents, or AI workflows?

Yes, as a storage layer for:

- prompt archives,
    
- document corpora,
    
- embeddings exports,
    
- model artifacts,
    
- evaluation datasets.
    

But it is not an AI workflow engine. It would support the plumbing, not the intelligence. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

## Suggested enterprise architecture incorporating this project

A sane architecture would be:

- **UI layer:** 9Drive frontend for uploads, file browsing, and quota visibility.
    
- **Gateway layer:** 9Drive backend for auth, upload routing, provider abstraction.
    
- **Persistence:** MySQL/Prisma for metadata and policy state.
    
- **Storage targets:** Google Drive, S3-compatible buckets, internal object store.
    
- **Processing layer:** separate ETL/ELT jobs, not inside 9Drive.
    
- **Governance layer:** IAM, audit logs, DLP, secrets manager, SIEM integration.
    
- **Orchestration layer:** Airflow/Dagster/Argo for downstream workflows.
    
- **AI layer:** RAG pipeline reads from the storage layer, not from 9Drive directly.
    

That would make 9Drive a **storage ingestion gateway**, not the center of the universe. That is the correct role for it. ([GitHub](https://github.com/zenhosta/9drive "GitHub - zenhosta/9drive: 9Drive is a storage gateway web app for connecting multiple Google Drive accounts into one virtual storage dashboard. Users can connect Google Drive accounts, track quota, upload files, organize files with virtual folders, preview files, and let the backend route uploads to the Drive account with enough free space. · GitHub"))

If you want, I can turn this into a polished Markdown report with a cleaner executive format and a scoring table.