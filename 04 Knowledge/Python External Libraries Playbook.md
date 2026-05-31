```table-of-contents
```
# 1. Install from local path
In **project B**: 
	`pip install -e ../project-a`
(`-e` = editable, so changes in project A show up immediately)
But for this to work, project A needs a `pyproject.toml` with a proper `[tool.poetry] name` set.

# 2. Build a wheel with Poetry and pip install it
In **project A**:
	`poetry build`
This creates:
	`dist/project_a-0.1.0-py3-none-any.whl
	`dist/project_a-0.1.0.tar.gz`
In **project B**:
	`pip install ../project-a/dist/project_a-0.1.0-py3-none-any.whl`

# 3. Install directly from Git (if you push A to GitHub/GitLab)

In **project B’s requirements.txt**:
	`git+https://github.com/your-org/project-a.git@main`
or in pip:
	`pip install "git+https://github.com/your-org/project-a.git@v0.1.0"`
  
Poetry projects install just fine this way — pip doesn’t care if the source used Poetry, as long as `pyproject.toml` is present.
# 4. Use a private package index (advanced / enterprise-y)

* Publish project A to a private PyPI (e.g., Nexus, Artifactory, or even `poetry publish --repository custom`).
* Then in **project B**:
	`pip install project-a`


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
