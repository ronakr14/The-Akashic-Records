# Challenge Pack 1

# 🐳 Docker Interview Prep – High-Level Scenarios & Killer Answers

* * *

## 🎯 1. **Explain Docker Image Layering and Caching Strategy**

**Scenario**:
You’ve got a 7-layer Dockerfile. Small change in layer 3. What happens?

**Expected Insight**:

- Docker uses **layered filesystem** (AUFS/OverlayFS).
- Changing layer 3 invalidates cache for 3 → N.
- Best practice: Order layers from **least to most frequently changed**.

> **Bonus**: Multistage builds help to isolate build-time bloat from runtime.

* * *

## 🎯 2. **Dockerfile Optimization Scenario**

**Scenario**:
You're handed a 1GB image. Team wants it &lt;100MB.

**Ideal Answer**:

- Use **Alpine** or `python:3.11-slim` base.
- Consolidate `RUN` commands into one to reduce layers.
- Use `.dockerignore` to exclude unnecessary files.
- Remove dev tools after build step.

> Use `docker build --squash` for extra credit.

* * *

## 🎯 3. **Image Security**

**Scenario**:
How do you secure a Docker image before pushing to production?

**Checklist**:

- Use only **official images** or trusted registries.
- Regularly **scan** using tools like `docker scan`, Trivy, or Snyk.
- Set minimal Linux users (`USER appuser`).
- Drop root privileges inside containers.
- Use **multi-stage builds** to separate compile time dependencies.

* * *

## 🎯 4. **Health Checks and Recovery**

**Scenario**:
Your Flask container occasionally fails silently. How to detect and recover?

**Answer**:

- Add `HEALTHCHECK` to Dockerfile:

  ```dockerfile
  HEALTHCHECK CMD curl -f http://localhost:5000/health || exit 1
  ```
- Or use Compose:

  ```yaml
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
    interval: 30s
    retries: 3
  ```
- Use orchestrators (e.g., Docker Swarm/K8s) to auto-restart failed containers.

* * *

## 🎯 5. **Networking Troubleshooting**

**Scenario**:
A multi-container app has API connection failures between services.

**Diagnosis Flow**:

- Confirm they're in the same `docker network` (check with `docker network inspect`).
- Use service **names**, not `localhost` or IP.
- Check port **exposure vs binding**.
- Try `docker exec curl` from one container to another.

> Compose’s `depends_on` does not wait for readiness — use healthchecks + retry logic.

* * *

## 🎯 6. **Data Persistence Pitfall**

**Scenario**:
App works fine locally, but data is lost between container restarts in staging.

**Root Cause**:

- Likely using **bind mount** or no mount at all.
- Correct fix: use **named volumes** in Compose or CLI:

  ```yaml
  volumes:
    - db_data:/var/lib/postgresql/data
  ```

* * *

## 🎯 7. **Legacy App Containerization**

**Scenario**:
You're asked to containerize a 2000s-era app with hardcoded paths, config files, and root access.

**Solution Strategy**:

- Use volume mounts to simulate file locations.
- Inject config with `--env`, `.env`, or mounted config files.
- Add a custom non-root user in Dockerfile if needed.
- Consider wrapping legacy code in a minimal Flask or FastAPI API layer.

* * *

## 🎯 8. **Multi-Stage Builds**

**Scenario**:
You need to build a Go app but ship only the binary.

**Approach**:

```dockerfile
FROM golang:1.20 AS builder
WORKDIR /app
COPY . .
RUN go build -o myapp

FROM alpine
COPY --from=builder /app/myapp /usr/bin/myapp
ENTRYPOINT ["myapp"]
```

> This reduces image size **drastically**.

* * *

## 🎯 9. **Deployment Strategy Question**

**Scenario**:
What are pros/cons of deploying with `docker-compose` vs. `Docker Swarm` vs. `Kubernetes`?

**Answer**:

| Tech             | Pros                                        | Cons                                 |
| ---------------- | ------------------------------------------- | ------------------------------------ |
| `docker-compose` | Easy local setup                            | No scaling, no fault tolerance       |
| `Docker Swarm`   | Built into Docker, easy setup               | Limited ecosystem, less used         |
| `K8s`            | Industry standard, autoscaling, secret mgmt | Heavy setup, overkill for small apps |

* * *

## 🎯 10. **CI/CD with Docker**

**Scenario**:
Build & deploy a container every time code is pushed to GitHub.

**Answer**:

- GitHub Actions workflow:

  ```yaml
  steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-docker@v2
    - run: docker build -t user/app:${{ github.sha }} .
    - run: docker push user/app:${{ github.sha }}
  ```
- Separate staging and prod branches with distinct Docker tags.

* * *

## 🚀 Bonus Questions

- What is the difference between an image and a container?
- What happens under the hood when you run `docker run`?
- How do you deal with Docker logs in production?
- What’s the difference between `CMD` and `ENTRYPOINT`?
- How do you share data between containers?