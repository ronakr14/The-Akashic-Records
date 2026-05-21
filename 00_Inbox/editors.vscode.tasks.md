---
id: 90bl40wurjikrixxpxkq247
title: Tasks
desc: ''
updated: 1755671248551
created: 1755671232783
---

## 1️⃣ **Tasks in VS Code (`tasks.json`)**

VS Code can run shell commands, scripts, or builds automatically.

**Example: Auto-run Python linter + tests**

1. Create `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Lint & Test",
      "type": "shell",
      "command": "flake8 src/ && pytest tests/",
      "group": "build",
      "problemMatcher": []
    }
  ]
}
```

2. Press **Ctrl+Shift+B** (Win/Linux) or **Cmd+Shift+B** (Mac) → selects “Lint & Test” → runs automatically.

**You can chain anything:**

* Build scripts
* Docker commands
* Custom Python scripts

---

## 2️⃣ **Snippets for Repetitive Code**

* Snippets auto-expand boilerplate code.
* Example for a Python function snippet:

1. Go to **File → Preferences → User Snippets → Python**
2. Add:

```json
{
  "Print Function Template": {
    "prefix": "pfunc",
    "body": [
      "def ${1:function_name}(${2:args}):",
      "    \"\"\"$3\"\"\"",
      "    ${0:pass}"
    ],
    "description": "Function template with docstring"
  }
}
```

* Type `pfunc` → press **Tab** → expands into a ready-to-edit function skeleton.

---

## 3️⃣ **Macros via Extensions**

Extensions like **“Multi-command”** or **“Macros”** let you record or define sequences of actions.

**Example:**

* Record: open terminal → run `pytest` → focus editor
* Trigger with one shortcut → all steps run automatically

---

## 4️⃣ **Tasks + Keybindings**

Combine tasks with keyboard shortcuts:

1. Open `keybindings.json`:

```json
{
  "key": "ctrl+alt+t",
  "command": "workbench.action.tasks.runTask",
  "args": "Lint & Test"
}
```

2. Press **Ctrl+Alt+T** → your task runs instantly.

---

## 5️⃣ **Live Templates / Emmet (HTML, CSS, JS)**

* For HTML/CSS/JS: `ul>li*5` → Tab expands into a 5-item list.
* You can customize Emmet abbreviations to automate repetitive HTML/JS boilerplate.

---

## 6️⃣ **Git + Extensions Automation**

* Extensions like **GitLens** can automate blame, history lookup, or commit template insertion.
* Combine with tasks → e.g., auto-lint + auto-stage + auto-commit script.

---

## 7️⃣ **File Watchers**

* You can use extensions like **“Run on Save”**:

  * Every time you save `*.py`, run `black` or `pytest`.
* Or set up **VS Code tasks with `watcher` mode**: automatically rebuild or re-run scripts when files change.

---

### ⚡ Practical Example

1. Save Python files → auto-format with `black`.
2. Lint with `flake8`.
3. Run unit tests with `pytest`.
4. All with **one shortcut** or auto-trigger on save.

---
