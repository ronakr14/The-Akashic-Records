---
id: oj5ccb7nn7yeh03eklxcyrc
title: Quicklearn
desc: ''
updated: 1747573431724
created: 1747571535169
---

#tag.resources.docker.quicknotes

## **Docker in Record Time: The Dirty 20% That Delivers**

This isn’t a beginner course. This is a **combat-ready plan** to get you from “what even is a container” to “I just containerized your mom’s lasagna recipe and deployed it to production.”

---

### **Phase 0: Set the Stage Like a Pro (30 min)**

1. **Install Docker Desktop** (or Docker Engine on Linux)

2. Test with:

   ```bash
   docker --version
   docker run hello-world
   ```

3. Skip Docker Swarm, Kubernetes, or Docker Compose for now. You’ll earn those later. First, **master the fundamentals** that let you build and ship.

---

### **Phase 1: Learn by Containerizing 3 Real Things**

No "hello-world" B.S. Here’s your **trifecta of brutal experience**:

| Project            | Containerized Version                 |
| ------------------ | ------------------------------------- |
| 1. A Flask API     | Containerize with custom Dockerfile   |
| 2. A PostgreSQL DB | Run official image, persistent volume |
| 3. A Web App       | Build + serve static files with Nginx |

You learn Docker by **forcing apps into boxes**.

---

### **Phase 2: The Core Docker Kung-Fu (90% of Power in 10 Commands)**

| Command                     | Use Case                             |
| --------------------------- | ------------------------------------ |
| `docker run`                | Start container from image           |
| `docker build`              | Build image from Dockerfile          |
| `docker ps -a`              | See running/stopped containers       |
| `docker exec -it <id> bash` | Shell into container                 |
| `docker logs <id>`          | Get container logs                   |
| `docker stop/rm <id>`       | Stop or delete container             |
| `docker images`             | See available images                 |
| `docker rmi <image>`        | Remove image                         |
| `docker volume`             | Persistent data                      |
| `docker network`            | Container-to-container communication |

**Drill daily with these. Live inside the terminal.**
Set yourself up with aliases or shell functions to burn them into muscle memory.

---

### **Phase 3: Create & Ship a Real Dockerfile (2 Days Max)**

Here’s a **minimal but mighty Dockerfile**:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

Then build and run:

```bash
docker build -t my-flask-api .
docker run -p 5000:5000 my-flask-api
```

This will teach you:

* `FROM`, `WORKDIR`, `COPY`, `RUN`, `CMD` – the *Dockerfile DNA*
* Port mapping (`-p`) – essential for exposing services
* Layer caching – why your builds get faster over time

---

### **Phase 4: Volume, Networks, and Persistence (1 Day)**

#### **Volumes** = data that survives container destruction.

```bash
docker volume create pgdata
docker run -v pgdata:/var/lib/postgresql/data postgres
```

#### **Networks** = let containers talk to each other like buddies.

```bash
docker network create backend
docker run --network backend --name db postgres
docker run --network backend --name app my-app
```

Stop pretending containers are isolated islands. **This is how microservices are born.**

---

### **Phase 5: Your Personal Docker Arsenal**

Create a **`.docker` folder in your projects** and standardize:

* `Dockerfile`
* `docker-compose.yml` *(once you’re ready)*
* `.dockerignore` *(like `.gitignore`, but for containers)*

Example `.dockerignore`:

```
__pycache__/
*.pyc
*.log
.env
```

---

### **Phase 6: Stop Writing Docs. Start Shipping**

Set up a 1-command deploy:

```bash
docker build -t my-web-app . && docker run -d -p 80:80 my-web-app
```

Or write a bash script:

```bash
#!/bin/bash
docker stop my-app && docker rm my-app
docker build -t my-app .
docker run -d --name my-app -p 8000:8000 my-app
```

Boom. Deployment magic, no Ansible, no Terraform. Just raw shell fu.

---

### **Phase 7: Bonus Moves When You’re Ready**

| Feature               | When to Learn | Why It Matters                     |
| --------------------- | ------------- | ---------------------------------- |
| `docker-compose`      | Day 5+        | Multi-container orchestration      |
| Docker Hub            | Day 3+        | Push/pull public or private images |
| `ENTRYPOINT` vs `CMD` | Day 4         | Fine-grained container control     |
| Alpine images         | Day 5+        | Smaller, faster images             |
| Docker context        | Day 6+        | Remote deploys, multi-env          |

---

### **The 20% Stack That Pays 80% Dividends**

| Concept               | Power Gained                            |
| --------------------- | --------------------------------------- |
| Build Dockerfile      | Containerize anything                   |
| `run`, `exec`, `logs` | Lifecycle mastery                       |
| Volumes               | Data that doesn’t vanish                |
| Networks              | Multi-container systems                 |
| Bash scripting        | Deploy pipelines without CI/CD overhead |
