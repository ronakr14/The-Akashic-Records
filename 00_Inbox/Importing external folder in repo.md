---
title: "Importing external folder in repo"
source: "https://chatgpt.com/c/6a0b2b87-b6e4-83a3-9b85-9234146469f2"
author:
published:
created: 2026-05-26
description: "ChatGPT conversation with 2 messages"
tags:
  - "clippings"
---
**You said**

I have a folder outside of current repo but under main repo. I want to import that in current repo file, help

---

**ChatGPT said**

You’re basically trying to “reach outside your sandbox,” which Python doesn’t love by default. There are a few clean ways to do it depending on how serious/long-term this setup is. I’ll walk you through the options—from quick hack to production-grade.

---

## 🧠 First, clarify your structure (assumption)

Something like:

```
main-repo/
│
├── shared_lib/        ← you want to import this
│   └── utils.py
│
├── project-a/         ← current repo/code you're running
│   └── app.py
```

And inside `app.py`, you want:

```python
from shared_lib.utils import something
```

---

## 🚫 Option 1: Dirty hack (works, but don’t marry it)

Modify `sys.path` at runtime:

```python
import sys
import os

sys.path.append(os.path.abspath("../shared_lib"))

from utils import something
```

**Reality check:**

- Works instantly ✅
- Breaks in CI, Docker, teammates' machines ❌
- Smells like “I’ll fix it later” tech debt

Use this only if you're debugging or prototyping.

---

## ⚙️ Option 2: Use PYTHONPATH (better, still manual)

Set environment variable:

### On Windows (PowerShell):

```powershell
$env:PYTHONPATH=".."
python app.py
```

Or permanent:

```powershell
setx PYTHONPATH ".."
```

Now Python knows about `main-repo/`, so this works:

```python
from shared_lib.utils import something
```

**Tradeoff:**

- Cleaner than sys.path
- Still environment-dependent (can drift across machines)

---

## 🧱 Option 3: Turn shared folder into a proper package (recommended)

Make `shared_lib` a real Python package:

```
shared_lib/
├── pyproject.toml
└── shared_lib/
    └── utils.py
```

Then install it locally.

### If you're using Poetry (which you are):

From `project-a`:

```bash
poetry add ../shared_lib
```

Or if it's not structured yet:

```bash
poetry add --path ../shared_lib
```

Now you can cleanly do:

```python
from shared_lib.utils import something
```

**This is the adult version:**

- Reproducible ✅
- Works in CI/CD ✅
- Scales with team ✅

---

## 🧬 Option 4: Monorepo-style (best for long-term architecture)

If this “shared\_lib” is reused across multiple projects, treat your repo like a monorepo:

- Each module = independent package
- Use editable installs (`poetry add --path ...`)
- Optional: version them internally

This aligns with how big orgs structure internal tooling.

---

## 🧠 My take (no fluff)

If this is:

- **Quick experiment** → use `sys.path`
- **Your actual workflow** → use Poetry local package
- **Scaling across multiple repos/services** → go monorepo or internal package registry

Anything else is just delaying pain.

---

## ⚡ Bonus: If it's a GitHub repo

You can do:

```bash
poetry add git+https://github.com/your-org/shared_lib.git
```

---

If you want, share your exact folder structure and I’ll give you a zero-friction setup (including `pyproject.toml` scaffolding).