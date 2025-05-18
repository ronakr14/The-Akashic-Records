# Challenge Pack 1

# 🐳 Docker Swarm Interview Prep: High-Level Scenarios

> Designed to assess architectural thinking, swarm-level ops knowledge, and production-hardened patterns.

* * *

## 🔥 Scenario 1: High Availability Deployment

**Q:** How would you design a highly available microservice architecture using Docker Swarm?

**✅ Expected Response:**

- Use **3+ manager nodes** for Raft consensus quorum.
- Deploy services with `--replicas=n` for redundancy.
- Use **Docker Swarm overlay network** to enable internal service discovery.
- Attach **external load balancer (e.g., HAProxy, Traefik)** to balance ingress.
- Configure **health checks** and `restart_policy` for self-healing.
- Bind persistent services to **named volumes** with storage drivers.

> Bonus: Mention **manager node failure tolerance** & **`drain` mode** for maintenance.

* * *

## 🔥 Scenario 2: Rolling Update Gone Wrong

**Q:** A rolling update of a service caused a crash loop in all replicas. How do you recover?

**✅ Expected Response:**

- Use `docker service rollback <service>` to revert to the last stable version.
- Investigate rollout failure using `docker service ps <service> --no-trunc`.
- Use `update_config` to control **delay**, **parallelism**, and **failure_action** (e.g., pause).
- Run updates with `--update-monitor` for time-bound rollback triggers.

> Bonus: Propose CI validation and staging pipeline using Swarm for canary deployments.

* * *

## 🔥 Scenario 3: Secret Management in Swarm

**Q:** How do you securely handle credentials and secrets in Swarm?

**✅ Expected Response:**

- Use `docker secret create` to inject secrets.
- Attach secrets in service definition under `--secret` or in `docker-compose.yml`.
- Secrets are mounted as **read-only tmpfs** inside the container (`/run/secrets/`).
- Only services explicitly granted access can see them.
- Secrets never touch disk or get exposed via `ENV`.

> Bonus: Discuss rotating secrets using `docker secret rm` + rolling update.

* * *

## 🔥 Scenario 4: Inter-service Networking

**Q:** How does Docker Swarm handle networking between services?

**✅ Expected Response:**

- Each Swarm service gets a DNS name via **internal DNS**.
- Swarm creates **overlay networks** spanning all nodes.
- Services on the same overlay network can talk using `http://service-name`.
- Use `--network` flag to attach services to networks.
- Supports **multi-networked containers** for security boundaries (e.g., frontend + backend net split).

> Bonus: Discuss `attachable` networks for legacy container interop.

* * *

## 🔥 Scenario 5: Swarm vs Kubernetes (Trade-offs)

**Q:** Why would you choose Swarm over Kubernetes, and what are the trade-offs?

**✅ Expected Response:**

- **Pros**:
  - Simpler setup & learning curve.
  - Native in Docker engine — no extra binaries.
  - Fast to deploy and scale small/medium projects.

- **Cons**:
  - Lacks advanced features like CRDs, service mesh, and mature autoscaling.
  - Weaker community support and ecosystem.
  - Docker Swarm is semi-maintained, Kubernetes dominates enterprise infra.

> Bonus: “Swarm is to orchestration what SQLite is to databases — simple, elegant, limited.”

* * *

## 🔥 Scenario 6: Persistent Storage in Swarm

**Q:** How do you persist data across service restarts in Swarm?

**✅ Expected Response:**

- Use **named volumes** (`docker volume create`) and bind them to services.
- Prefer **external volume drivers** (like `local-persist`, `nfs`, `rexray`, or CSI-compatible) for cluster-wide persistence.
- Bind volumes in `docker-compose.yml` or CLI using `--mount` or `--volume`.

> Bonus: Highlight that data must be accessible from _any node_ the task might land on.

* * *

## 🔥 Scenario 7: Troubleshooting a Broken Service

**Q:** A service isn’t responding. What’s your debugging process?

**✅ Expected Response:**

- Run `docker service ps <name>` to check status, failures, and logs.
- Inspect logs via `docker service logs <name>` or individual tasks.
- Check task/node scheduling issues (`docker node ls`, `docker node inspect`).
- Validate container health and exit codes.
- Use `docker inspect` to review volumes, secrets, envs.

> Bonus: Use `drain` mode to isolate node issues without impacting the cluster.

* * *

## 📌 Tags

- [#docker](/tags/docker.md)
- [#docker-swarm](/tags/docker-swarm.md)
- [#interview-prep](/tags/interview-prep.md)
- [#high-level](/tags/high-level.md)
- [#devops](/tags/devops.md)

```

```