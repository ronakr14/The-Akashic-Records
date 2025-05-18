# Swarm

# 🐳 Docker Swarm Mastery: 80/20 Strategy

Swarm isn't Kubernetes — it’s **simpler**, faster to get into prod, and _grossly underrated_. This plan gives you **practical Swarm chops** using the 80/20 rule: focus on the 20% of commands, patterns, and pitfalls that show up in 80% of real-world ops.

* * *

## 🔥 Phase 1: The Core Five You Must Burn Into Muscle Memory

| Concept        | Command                                 | Mastery Notes                |
| -------------- | --------------------------------------- | ---------------------------- |
| Init swarm     | `docker swarm init`                     | Run on the manager node      |
| Join node      | `docker swarm join`                     | Workers join using token     |
| Deploy service | `docker service create ...`             | Deploy containerized app     |
| Scale service  | `docker service scale mysvc=5`          | Replicates container         |
| Update service | `docker service update --image new ...` | Zero-downtime rolling update |

💡 **Hack**: Always use a **docker-compose.yml** with `docker stack deploy -c docker-compose.yml mystack` once you understand `service create`.

* * *

## 🚧 Phase 2: Challenge-Driven Learning (Gamified)

| Challenge                       | Goal                                                      | Concept                                      |
| ------------------------------- | --------------------------------------------------------- | -------------------------------------------- |
| `swarm.01.init-local-lab`       | Set up a local 3-node swarm using Docker-in-Docker or VMs | `init`, `join`, overlay networks             |
| `swarm.02.simple-web-service`   | Deploy Nginx with 3 replicas                              | `service create`, scaling, `docker ps`       |
| `swarm.03.network-connectivity` | Deploy 2 services (web ↔ API) on custom overlay           | `network create`, `depends_on`, healthcheck  |
| `swarm.04.rolling-update`       | Update service without downtime                           | `service update`, `--update-delay`, rollback |
| `swarm.05.secret-management`    | Deploy a service that reads a secret                      | `docker secret`, `docker config`             |

* * *

## 🧠 Phase 3: Swarm Mental Models

- **Swarm is declarative**: you define state, Swarm keeps it running.
- **Swarm ≠ Kubernetes**: it’s simpler, but has **built-in routing mesh**, **load balancing**, and **TLS out-of-the-box**.
- **Service ≠ container**: Services are swarm-managed abstractions that **scale**, **self-heal**, and **roll out** intelligently.

* * *

## ⚔️ Phase 4: Tactical Edge Use Cases (Real DevOps Work)

### 🔄 Rolling Updates with Zero Downtime

```bash
docker service update --image myapi:v2 --update-parallelism 2 --update-delay 10s myapi
```

### 📡 Ingress Routing & Load Balancing

- Built-in routing mesh — every node can receive traffic for any service.
- Publish port only once: `-p 80:80` → swarm routes correctly across replicas.

### 🔐 Secrets & Configs

```bash
echo "supersecret" | docker secret create db_pass -
docker service create --secret db_pass ...
```

### 📈 Monitoring

Use `docker service ps <service>` and `docker node ls` for cluster health.

> Bonus: Plug in Prometheus/Grafana with `cadvisor` or `dockerd-exporter`.

* * *

## 🧪 Phase 5: Interview-Level Command Recall

> Memorize these like a mantra:

```bash
docker swarm init
docker swarm join-token worker
docker service create ...
docker service scale ...
docker stack deploy -c ...
docker secret create ...
docker service update ...
```

* * *

## 📦 Bonus: Swarm Quick Deploy Templates

Create a **Swarm-ready stack** in seconds with this `docker-compose.yml`:

```yaml
version: "3.8"
services:
  web:
    image: nginx
    ports:
      - "80:80"
    deploy:
      replicas: 3
      restart_policy:
        condition: on-failure
      update_config:
        parallelism: 2
        delay: 5s
```

Deploy with:

```bash
docker stack deploy -c docker-compose.yml mystack
```

* * *

## 🔁 Final Loop: Rehearse, Riff, Repeat

- Simulate failures: kill containers, unplug nodes, scale services mid-deploy.
- Explain aloud each command and why you'd use it.
- Rebuild the cluster weekly from scratch with bare minimum commands.

* * *

# 📌 Tags

- \#docker-swarm
- \#learning/80-20
- \#devops

```

```