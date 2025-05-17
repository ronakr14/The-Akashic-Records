---
id: n040gz6s1ywx855a7oorpmz
title: Venv
desc: ''
updated: 1747466993761
created: 1747466742692
---

Creating a virtual environment in Python is like giving your project its own private sandbox—no package chaos, no version drama, just clean, isolated bliss. Here's how you do it, step-by-step:

---

#tag.python.environment.venv.quicknotes

## 🐍 Step-by-Step: Create a Virtual Environment in Python

---

### ✅ 1. Check Your Python Version

Make sure Python is installed:

```bash
python --version
# or
python3 --version
```

You need Python 3.3+ for `venv`.

---

### 🛠️ 2. Create the Virtual Environment

In your project folder:

```bash
python -m venv venv
```

This creates a folder named `venv` (you can name it anything) that contains a copy of Python + pip.

> 💡 Naming convention tip: Use `.venv` or `env` to keep it hidden-ish or project-specific like `venv-mkdocs`.

---

### ▶️ 3. Activate the Virtual Environment

#### **Windows (cmd.exe)**:

```cmd
venv\Scripts\activate
```

#### **Windows (PowerShell)**:

```powershell
.\venv\Scripts\Activate.ps1
```

#### **macOS/Linux**:

```bash
source venv/bin/activate
```

You’ll know it’s activated when you see `(venv)` in your terminal prompt.

---

### 📦 4. Install Packages

Now you’re working in isolation. Go ahead:

```bash
pip install mkdocs mkdocs-material
```

---

### 💾 5. Freeze Your Dependencies

For reproducibility:

```bash
pip freeze > requirements.txt
```

Others can replicate your environment with:

```bash
pip install -r requirements.txt
```

---

### ❌ 6. Deactivate When Done

Just:

```bash
deactivate
```

Back to global Python—no mess.

---

## 🔄 Quick One-Liner (for automation nerds)

```bash
python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

Perfect for bootstrapping a project.