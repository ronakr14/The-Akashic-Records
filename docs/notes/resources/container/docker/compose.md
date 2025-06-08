# Compose

# 🧩 Docker Compose Mastery: The 80/20 Playbook

> Learn Compose not as a config file, but as a **deployment weapon**.

* * *

## 🔥 Phase 1: The Must-Know Concepts

Focus on mastering these _power levers_:

| Topic                | 20% That Matters                           |
| -------------------- | ------------------------------------------ |
| Multi-container apps | Compose = instant orchestration            |
| `depends_on`         | Set app startup order (but not readiness!) |
| Volumes              | Mount code/data across restarts            |
| Networks             | Internal container DNS, avoids `localhost` |
| Service configs      | `build`, `image`, `environment`, `command` |
| Deploy override      | Use `.env` + `docker-compose.override.yml` |

* * *

## 🧪 Phase 2: Hands-On Tactical Challenges

Each challenge teaches _multiple core Compose skills_.

### ✅ `compose.01.basic-two-service`

**Goal**: Connect a Node.js API to Postgres

```yaml
version: "3.8"
services:
  api:
    build: .
    ports:
      - "3000:3000"
    depends_on:
      - db
    environment:
      - DB_HOST=db
      - DB_PORT=5432

  db:
    image: postgres:14
    environment:
      POSTGRES_PASSWORD: secret
```

* * *

### 🧩 `compose.02.bind-mount-dev-sync`

**Goal**: Sync local code changes into container

```yaml
volumes:
  - .:/usr/src/app
```

Great for local dev with hot-reload. Use with Node, Flask, Django, etc.

* * *

### 🔐 `compose.03.env-secrets-config`

**Goal**: Inject secrets securely using `.env`

```env
POSTGRES_PASSWORD=topsecret
```

```yaml
env_file:
  - .env
```

Pro move: Use Git-ignored `.env` and inject config only at runtime.

* * *

### 🚀 `compose.04.override-strategy`

**Goal**: Use multiple Compose files for env-specific setup

```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up
```

Use this to change DBs, images, or configs between dev/prod.

* * *

## 🧠 Phase 3: Mental Models

- **Services ≠ Containers** — think of each service as a “role” that spawns containers.
- **Networks are magic** — every service can reach the other by its name, like `api` or `redis`.
- **Docker Compose is declarative** — it reconciles the state on your behalf.
- **Use Compose for everything** — local dev, CI/CD, smoke testing, even infra bootstrap.

* * *

## ⚡️ Phase 4: Production-Ready Practices (Condensed)

### 📁 Project Layout Template

```
project/
├── docker-compose.yml
├── docker-compose.override.yml
├── .env
├── api/
│   ├── Dockerfile
│   └── ...
└── db/
```

### 💡 Secrets Management

Use `env_file`, GitHub Actions secrets, or Vault for sensitive values.

* * *

### ⚙️ Deployment Command Pattern

```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

🔥 Pro tip: Always `--build` on first prod deploy or after config change.

* * *

## 📜 Phase 5: Cheat Commands You Must Memorize

```bash
docker-compose up -d         # Start everything
docker-compose down          # Stop & clean up
docker-compose build         # Build images
docker-compose logs -f       # Real-time logs
docker-compose exec app bash # Shell into container
docker-compose ps            # Check running services
```

* * *

## 📌 Tags

- \#docker-compose
- \#learning/80-20
- \#devops
- \#workflow

```

```