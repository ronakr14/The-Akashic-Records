---
id: dof856iz9ct6iwy6szrm8x5
title: Actions
desc: ''
updated: 1753336841175
created: 1753336835412
---
tags: [master, github-actions]

## 📌 Topic Overview

**GitHub Actions** is:

* A **CI/CD and automation platform** natively integrated into GitHub repositories.
* Enables automation of workflows based on repository events like push, pull request, issue creation, and more.
* Uses **YAML-based workflow files** stored inside the repository (`.github/workflows/`).
* Supports **jobs** that run on GitHub-hosted runners or self-hosted runners.
* Integrates with GitHub ecosystem deeply — enabling seamless build, test, deploy, and automation pipelines.
* Features include:
  * Matrix builds for parallel testing.
  * Secrets management.
  * Marketplace of reusable actions.
  * Easy-to-use syntax for defining dependencies and conditions.
  * Native support for containers, Docker, and cloud deployments.

## 🚀 80/20 Roadmap

| Stage | Concept                              | Reason                                            |
| ----- | ---------------------------------- | -------------------------------------------------|
| 1️⃣   | Basic workflow setup and triggers  | Automate builds on push, PR, schedule, or manual |
| 2️⃣   | Jobs, steps, and actions            | Define granular tasks inside workflows            |
| 3️⃣   | Using marketplace actions           | Reuse community actions to save time              |
| 4️⃣   | Matrix builds                      | Run jobs in parallel with different OS/versions  |
| 5️⃣   | Secrets and environment variables   | Securely manage credentials and config             |
| 6️⃣   | Conditional execution and workflows | Control flow with `if` and workflow dispatch       |
| 7️⃣   | Self-hosted runners                 | Extend runner capacity and custom environments     |
| 8️⃣   | Deployments and environment protection | Automate deploys with environment approvals       |
| 9️⃣   | Artifact and caching strategies     | Speed up builds and preserve outputs                |
| 🔟    | Integration with cloud providers    | Deploy to AWS, Azure, GCP, Kubernetes, etc.        |

---

## 🛠️ Practical Tasks

* ✅ Create a basic workflow triggered on push to main branch.
* ✅ Define multiple jobs with sequential and parallel execution.
* ✅ Use official marketplace actions (checkout, setup-python, etc.).
* ✅ Configure matrix builds for testing multiple Python versions.
* ✅ Store and access secrets securely within workflows.
* ✅ Add conditional steps based on branch or event type.
* ✅ Upload and download artifacts between jobs.
* ✅ Implement caching to speed up dependencies installation.
* ✅ Configure self-hosted runners for specialized build environments.
* ✅ Deploy an application to a cloud service (AWS/GCP/Azure).

---

## 🧾 Cheat Sheets

### 🔹 Simple Workflow Example (`.github/workflows/ci.yml`)

```yaml
name: CI Pipeline

on:
  push:
    branches:
      - main
  pull_request:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest
````

### 🔹 Matrix Build Example

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10]
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -r requirements.txt
      - run: pytest
```

### 🔹 Caching Dependencies

```yaml
- name: Cache pip
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

---

## 🎯 Progressive Challenges

| Level           | Task                                                              |
| --------------- | ----------------------------------------------------------------- |
| 🥉 Easy         | Create a workflow that runs tests on every push                   |
| 🥈 Intermediate | Implement matrix builds for multiple OS and Python versions       |
| 🥇 Advanced     | Add caching and artifact uploads to speed up build pipelines      |
| 🏆 Expert       | Build a deploy pipeline with environment protection and approvals |

---

## 🎙️ Interview Q\&A

* **Q:** What are GitHub Actions and how do they integrate with GitHub?
* **Q:** Explain the difference between jobs and steps in a workflow.
* **Q:** How does matrix strategy improve CI pipelines?
* **Q:** How do you manage secrets securely in workflows?
* **Q:** What are self-hosted runners and when should you use them?
* **Q:** How can you cache dependencies to optimize build times?
* **Q:** Describe how to trigger workflows on pull requests and scheduled events.

---

## 🛣️ Next Tech Stack Recommendations

* **Docker** — Containerize builds and deploy pipelines.
* **Terraform / Pulumi** — Infrastructure as Code for managing runner environments.
* **HashiCorp Vault** — Advanced secrets management integrated with workflows.
* **AWS / Azure / GCP CLI** — For deploying apps via Actions.
* **Octopus Deploy / ArgoCD** — Complement GitHub Actions for advanced CD.

---

## 🧠 Pro Tips

* Use reusable workflows to DRY up common CI/CD tasks.
* Keep workflows small and focused; split complex pipelines.
* Encrypt sensitive data and never commit secrets in repos.
* Leverage the marketplace but vet third-party actions carefully.
* Use artifacts to persist build outputs between jobs.
* Monitor workflow run times and optimize slow steps regularly.

---

## 🧬 Tactical Philosophy

> **GitHub Actions turns your repo into a powerful automation engine. The closer your CI/CD is to your codebase, the faster and safer your software delivery becomes.**

⚙️ Keep automation declarative, versioned, and transparent.
🔐 Prioritize security and secrets hygiene.
📈 Continuously optimize for speed and reliability.
💣 Use native GitHub events to build reactive workflows.
🤖 Embrace reusable actions and workflows to scale automation.

---
