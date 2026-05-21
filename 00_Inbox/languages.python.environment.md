---
id: hp0cjdhhiuyy93rfx2gytc7
title: Environment
desc: ''
updated: 1755789998811
created: 1755789992684
---

# 🐍 Python Virtual Environments + Pip – Cheat Sheet

---

## 🔹 Virtual Environments (`venv`)

```bash
# Create a virtual environment
python -m venv venv

# Activate
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux

# Deactivate
deactivate
```

👉 Tips:

* Keep `venv/` in project root but **add to `.gitignore`**
* Custom prompt:

```bash
python -m venv --prompt myproj venv
```

---

## 🔹 Pip Basics

```bash
pip install requests            # Install latest
pip install requests==2.31.0    # Specific version
pip install requests>=2.0,<3    # Version range

pip uninstall requests          # Remove
pip list                        # Show installed packages
pip show requests               # Show details
```

---

## 🔹 Requirements Management

```bash
pip freeze > requirements.txt   # Save dependencies
pip install -r requirements.txt # Install from file
```

👉 Best Practice:

* Pin versions (`package==x.y.z`) for reproducibility
* Separate files:

```
requirements.txt
dev-requirements.txt
```

---

## 🔹 Upgrades & Checks

```bash
pip install --upgrade requests   # Upgrade package
pip list --outdated              # See outdated
python -m pip install --upgrade pip   # Upgrade pip
```

---

## 🔹 Useful Tricks

```bash
pip search flask      # Search PyPI (deprecated in some versions)
pip check             # Verify dependency integrity
pip freeze --exclude-editable > requirements.txt  # Only top-level deps
```

**Editable Installs (for local dev)**

```bash
pip install -e .
```

---

## 🔹 Project Layout (with venv)

```
my_project/
├── venv/                # Virtual environment
├── src/
│   ├── __init__.py
│   └── main.py
├── requirements.txt
└── README.md
```

---

## 🔹 Beyond Pip

* **Poetry** → modern dep mgmt, packaging (`pyproject.toml`)
* **Pipenv** → manages `Pipfile` + virtualenv
* **Conda** → environments + data science deps

---

✅ **Quick Rules of Thumb**

* 1 project = 1 venv
* Always `pip freeze` after adding/upgrading deps
* Never commit `venv/`
* Use `pip install -e .` for local dev packages
* Upgrade pip regularly

---

⚡That’s your one-page reference for **dependency control** in Python.
