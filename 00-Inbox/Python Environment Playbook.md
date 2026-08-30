# AI Summary
A practical playbook for managing Python runtimes and isolated development environments on Windows and MSYS/bash. The note recommends `uv` as the primary tool for Python installation, virtual environments, dependency management, and project initialization, while also covering the Windows `py` launcher, built-in `venv`, and Poetry. It includes installation commands, activation workflows, dependency management, multi-version Python handling, best practices such as excluding virtual environments from version control, and a decision guide for selecting the appropriate tool based on different development scenarios.

---


Managing multiple Python versions and isolated environments. This note covers Windows + MSYS/bash workflows.

---

# Recommended Approach: `uv`

For this environment (Windows with bash/MSMS), **`uv`** is the recommended tool. It replaces `py` launcher, `venv`, and `poetry` with one fast Rust-based CLI.

```bash
# Install uv
powershell -ExecutionPolicy ByPass -c "irm https://.astral.sh/uv/install.ps1 | iex"

# Install a Python version
uv python install 3.13

# Create a virtual environment
uv venv .venv313

# Activate
source .venv313/Scripts/activate

# Install packages
uv pip install <package>

# Pin dependencies
uv pip freeze > requirements.txt
```

`uv` also supports:
- `uv init` / `uv add` (project scaffolding, replaces `poetry init`)
- `uv tool run` (one-off command execution)
- `uv python list` (list installed versions)

See: [[Python External Libraries Playbook]] for package recommendations.

---

# Multiple Python Runtimes (Windows `py` Launcher)

Windows ships a `py` launcher that manages multiple Python installations.

```bash
# List installed versions
py -0

# Install a specific version
py install 3.13

# Get executable path for a version
py -3.13 -c "import sys; print(sys.executable)"

# Set persistent environment variable (PowerShell)
setx PYTHON313 "<executable path>"
```

After setting environment variables, reference them in virtual environment creation:

```bash
py -3.13 -m venv .venv313
```

---

# Virtual Environments (`venv`)

Built into Python. Creates isolated package environments per project.

```bash
# Create
python -m venv .venv

# Activate (bash/MSYS)
source .venv/Scripts/activate

# Activate (PowerShell)
.venv/Scripts/Activate.ps1

# Deactivate
deactivate
```

Best practice: never commit `.venv/`. Add it to `.gitignore`.

---

# Poetry (Alternative)

Poetry provides dependency resolution + packaging. Slower than `uv` but mature.

```bash
# Install Poetry
pip install poetry

# Use a specific Python version
poetry env use $env:PYTHON314    # PowerShell
poetry env use $(py -3.14 -c "import sys; print(sys.executable)")  # bash

# Activate shell
poetry shell

# Install dependencies
poetry install
```

For frequent use, add a shell function:

```powershell
function poetry-use {
    param([string]$ver)
    $exe = (py -$ver -c "import sys; print(sys.executable)")
    poetry env use $exe
    poetry shell
}
```

Add to `$PROFILE` (find path with `echo $PROFILE`).

---

# Decision Guide

| Scenario | Tool |
|---|---|
| Starting fresh in this environment | `uv` |
| Simple script, need isolation fast | `uv venv` |
| Team already uses Poetry | `poetry` (or migrate to `uv`) |
| Need to test across many Python versions | `py` launcher + `uv python` |
| Corporate environment, no internet | `uv` with `--offline` or pre-installed system Python |

---

# See Also

- [[Python External Libraries Playbook]] — package recommendations
- [[Python Application Integrations]] — Python + service integrations
