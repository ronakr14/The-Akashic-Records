---
id: j7uwjalvba8pv9mh5yjdav2
title: Tips Trick
desc: ''
updated: 1756120149640
created: 1756120128481
---

### 1. Minimize Layers

* Combine multiple `RUN` commands into one.
* Clean up temp files (`rm -rf /var/lib/apt/lists/*`).
* Fewer layers = smaller, faster images.

### 2. Use `.dockerignore`

* Prevent unnecessary files (`.git`, `node_modules`, logs) from being copied.
* Speeds up builds and reduces image size.

### 3. Multi-Stage Builds

* Use a **builder stage** (Node, Maven, Go, etc.) to compile.
* Copy only the final output into a **production stage** (e.g., Nginx).
* Strips out build tools and dev dependencies → lean, secure images.

### 4. Pin Image Versions

* Avoid `latest` tags.
* Use pinned versions like `python:3.11.6-slim` for stability and reproducibility.
* Choose minimal variants (slim, alpine) but test for compatibility.

### 5. Add `HEALTHCHECK`

* Define a health endpoint or process check.
* Example:

  ```dockerfile
  HEALTHCHECK --interval=30s --timeout=10s \
    CMD curl -f http://localhost:8080/health || exit 1
  ```
* Lets Docker (and orchestrators like Kubernetes) detect failures and restart containers automatically.

---
