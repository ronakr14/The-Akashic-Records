---
id: 9ubfvuhfr79qszjx5aic4um
title: Selfhelp
desc: ''
updated: 1755668863128
created: 1755668836186
---

tags: #python #debugging #vscode #remote-debugging #devtools

---

## 📌 Topic Overview

`debugpy` is the official debugger for Python used by **VS Code** and other IDEs.
It supports local, remote, and multi-process debugging with breakpoints, variable inspection, call stacks, and hot reloading.

Think of it as the "bridge" between your Python runtime and your IDE’s debug UI.

---

## 🎯 80/20 Roadmap

* **20% Concepts to Learn → 80% Productivity**

  * Install & run `debugpy`
  * Attach debugger locally (`--listen`)
  * Remote debugging (`--wait-for-client`)
  * Breakpoints & watch variables
  * Debugging async code & multiprocessing

---

## 🛠️ Practical Tasks

* Install:

  ```bash
  pip install debugpy
  ```
* Run script with debug server:

  ```bash
  python -m debugpy --listen 5678 myscript.py
  ```
* Pause until client attaches:

  ```bash
  python -m debugpy --listen 0.0.0.0:5678 --wait-for-client app.py
  ```
* Add programmatic breakpoint:

  ```python
  import debugpy
  debugpy.breakpoint()
  print("Execution paused here for inspection")
  ```
* VS Code `launch.json` example:

  ```json
  {
    "name": "Python: Remote Attach",
    "type": "python",
    "request": "attach",
    "connect": {
      "host": "localhost",
      "port": 5678
    }
  }
  ```

---

## 📑 Cheat Sheets

* **Start Debug Server:** `python -m debugpy --listen 5678 script.py`
* **Wait for VS Code client:** add `--wait-for-client`
* **Inline Breakpoint:** `debugpy.breakpoint()`
* **Check if debugger attached:**

  ```python
  if debugpy.is_client_connected():
      print("Debugger attached")
  ```
* **Attach config:** Always set `"justMyCode": false` in VS Code to debug third-party libs.

---

## 🚀 Progressive Challenges

1. Debug a local script with breakpoints.
2. Run Flask/Django with `debugpy` and hot-reload debugging.
3. Attach to a long-running background job on a remote server.
4. Debug async coroutines with breakpoints inside `async def`.
5. Debug multiple processes (child processes spawned).

---

## 🎤 Interview Q\&A

**Q1: What’s the difference between `pdb` and `debugpy`?**
A: `pdb` is CLI-based, `debugpy` integrates with IDEs (VS Code, PyCharm) for richer debugging, remote support, and async debugging.

**Q2: How do you attach VS Code to a remote Python process?**
A: Run `python -m debugpy --listen 0.0.0.0:5678 --wait-for-client app.py`, then in VS Code use `"request": "attach"` with host/port.

**Q3: Can `debugpy` debug async tasks?**
A: Yes, breakpoints inside async functions are fully supported.

**Q4: How do you ensure security with remote debugging?**
A: Bind to `127.0.0.1` locally or tunnel via SSH. Never expose `0.0.0.0:5678` without a firewall.

---

## 🧭 Next Tech Stack Recommendation

Once comfortable with `debugpy`, move to:

* **VS Code Advanced Debugging** → conditional breakpoints, data breakpoints.
* **pytest + debugpy** → test debugging.
* **PyCharm Remote Debugging** → alternative ecosystem.
* **Production Observability** → Sentry, Datadog tracing.

---

