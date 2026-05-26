---
title: "Poetry custom package install"
source: "https://chatgpt.com/c/6a0ae0c4-3808-8323-8c5d-8f40f7c018e5"
author:
published:
created: 2026-05-26
description: "ChatGPT conversation with 2 messages"
tags:
  - "clippings"
---
**You said**

I am using a poetry package manager. I need to install custom packages in it, how that can be done? I have one at local and other on github

---

**ChatGPT said**

Short answer: Poetry handles both cleanly—but you have to be explicit about *where* the package lives and *how* it should be resolved. Think of it as dependency sourcing strategy: local path vs remote VCS.

Let’s break it down like an engineer, not a tutorial bot.

---

## 🧩 1. Installing a local package

You’ve got a package sitting somewhere on your machine—Poetry can treat it as a first-class dependency.

### 👉 Option A: Add via CLI (recommended)

```bash
poetry add ../my-local-package
```

### 👉 Option B: Edit pyproject.toml manually

```toml
[tool.poetry.dependencies]
my-local-package = { path = "../my-local-package" }
```

---

### ⚙️ Advanced knobs (this is where it gets interesting)

- **Editable mode (like pip -e)** → live changes reflect instantly:
```toml
my-local-package = { path = "../my-local-package", develop = true }
```
- **Relative vs absolute paths**
	- Relative → portable (good for repos)
		- Absolute → brittle (avoid unless necessary)

---

### ⚠️ Reality check

If your local package:

- doesn’t have a `pyproject.toml` → expect pain
- has conflicting dependencies → Poetry will complain loudly (good thing)

---

## 🌐 2. Installing from GitHub

Now we move to VCS dependencies—Poetry plays nicely with Git.

### 👉 Option A: CLI

```bash
poetry add git+https://github.com/username/repo.git
```

---

### 👉 Option B: pyproject.toml

```toml
[tool.poetry.dependencies]
my-package = { git = "https://github.com/username/repo.git" }
```

---

### 🔧 Pin it properly (don’t YOLO latest)

You *should* lock to a branch, tag, or commit:

```toml
my-package = { git = "https://github.com/username/repo.git", branch = "main" }
```

or

```toml
my-package = { git = "https://github.com/username/repo.git", tag = "v1.2.0" }
```

or (best for reproducibility 👇)

```toml
my-package = { git = "https://github.com/username/repo.git", rev = "a1b2c3d" }
```

---

### 🔐 Private repos?

Use SSH:

```toml
my-package = { git = "git@github.com:username/repo.git" }
```

Make sure your SSH keys are set up, or Poetry will just fail silently and ruin your day.

---

## 🧠 Pro-level patterns (this is where teams mess up)

### 1\. Hybrid dev workflow

- Use local path during development
- Switch to Git tag for CI/CD

You can even script this swap if you're serious about automation.

---

### 2\. Monorepo setup

Poetry works surprisingly well:

```toml
package-a = { path = "packages/package-a", develop = true }
package-b = { path = "packages/package-b", develop = true }
```

---

### 3\. Dependency overrides (Poetry 1.2+)

If Git package has bad dependencies:

```toml
[tool.poetry.group.dev.dependencies]
problem-lib = { version = "1.2.3" }
```

---

## 🚨 Common pitfalls (learn from other people's scars)

- Mixing `pip install` with Poetry → don’t. Ever.
- Forgetting `poetry lock` after manual edits
- Using `branch = "main"` in production (risky, non-deterministic)
- Local paths breaking in CI (because that path doesn’t exist there)

---

## 🧭 My blunt recommendation

- Use **local path + develop=true** while building
- Tag releases → install via Git with `tag` or `rev`
- Never depend on floating branches in anything that matters

---

If you want, I can help you:

- design a **clean monorepo structure**
- or wire this into your **n8n / CI pipeline** so local → git → release becomes seamless

Just tell me your setup.