# Docker Quicklearning

Buckle up. Here’s your **Docker Challenge Series**, designed like a _video game campaign_ with three tiers:
🟢 **Easy** (Get battle-ready), 🟡 **Intermediate** (Real ops), 🔴 **Expert** (Welcome to the Thunderdome).

Each challenge has:

- 🎯 **Mission** – What to do
- 🎓 **Skill Unlocked** – What you gain
- 🛠️ **Tool Focus** – Commands/concepts in play
- 🚨 **Constraints** – Because difficulty is a feature

## [#tag.todo.docker](/tags/tag/todo/docker.md)

## 🟢 EASY MODE (Levels 1–5) — _"Learn the Weapon"_

### **Level 1: Hello Container**

🎯 Run a container that echoes “Hello from Docker!” and exits.
🎓 Learn image execution flow.
🛠️ `docker run`, `--rm`, `alpine`, `echo`
🚨 Must use an official Alpine image only.

* * *

### **Level 2: Build Your First Image**

🎯 Create a Dockerfile for a Python script that prints current time.
🎓 Understand build layers and base images.
🛠️ `FROM`, `RUN`, `COPY`, `CMD`
🚨 Image must be under 100MB.

* * *

### **Level 3: Host a Web App**

🎯 Serve a Flask “Hello World” app using Docker.
🎓 Learn port mapping & exposing services.
🛠️ `-p`, `WORKDIR`, Flask
🚨 App must be accessible at `http://localhost:5000`.

* * *

### **Level 4: Persist the Apocalypse**

🎯 Run a Postgres container with volume-mounted data.
🎓 Grasp persistent storage.
🛠️ `-v`, `docker volume`, `/var/lib/postgresql/data`
🚨 Restart the container without losing your data.

* * *

### **Level 5: Shell Fu**

🎯 Launch a Bash shell inside a running container.
🎓 Master container introspection.
🛠️ `exec`, `ps`, `env`, `top`
🚨 Must install a tool (e.g. curl) inside the running container.

* * *

## 🟡 INTERMEDIATE MODE (Levels 6–10) — _"Command the Battlefield"_

### **Level 6: Compose Yourself**

🎯 Use Docker Compose to orchestrate a Flask app and Postgres DB.
🎓 Master multi-container orchestration.
🛠️ `docker-compose`, `depends_on`, `networks`, `.env`
🚨 DB must persist data and app must auto-connect at boot.

* * *

### **Level 7: Container Health**

🎯 Add a healthcheck to your Dockerized Flask API.
🎓 Learn container lifecycle monitoring.
🛠️ `HEALTHCHECK`, `curl`, `CMD`
🚨 Restart the app only if healthcheck fails 3 times.

* * *

### **Level 8: Slim It Down**

🎯 Refactor your image using Alpine or multistage builds.
🎓 Reduce image size and optimize build caching.
🛠️ `python:3.11-alpine`, `COPY`, `RUN`, `--no-cache`
🚨 Final image must be under 50MB.

* * *

### **Level 9: Secrets & Lies**

🎯 Inject a secret API key into your container without baking it into the image.
🎓 Environment variable security.
🛠️ `--env`, `.env`, `docker-compose secrets`
🚨 No hard-coded secrets allowed.

* * *

### **Level 10: Tag You’re It**

🎯 Tag, push, and pull your image to/from Docker Hub.
🎓 Learn image lifecycle and remote registries.
🛠️ `docker tag`, `push`, `pull`, `login`
🚨 Image must be named using a proper namespace and versioning (`user/app:1.0.0`).

* * *

## 🔴 EXPERT MODE (Levels 11–15) — _"Master the Matrix"_

### **Level 11: CI/CD Triggered Container Build**

🎯 Write a GitHub Actions workflow that builds and pushes your Docker image on every commit.
🎓 CI-driven Docker automation.
🛠️ `actions/setup-docker`, GitHub Actions YAML, `docker login`
🚨 Must build for staging and production with different ENV configs.

* * *

### **Level 12: Reverse Proxy With NGINX**

🎯 Set up an NGINX container to reverse proxy to your Flask app.
🎓 Real-world multi-container networking.
🛠️ `nginx.conf`, `proxy_pass`, `docker network`
🚨 App must be accessible via NGINX on port 80.

* * *

### **Level 13: Zombie Cleanup**

🎯 Your disk is full of dangling containers, images, volumes. Write a cleanup script.
🎓 Docker system hygiene.
🛠️ `docker system prune`, `volume prune`, `rmi`, `rm`
🚨 Must only delete unused resources (no nuking active containers).

* * *

### **Level 14: Build Your Own Base Image**

🎯 Create a Docker image with Python + curl + vim pre-installed as a reusable base.
🎓 Internal image development.
🛠️ `FROM`, `apt`, `LABEL`, `ENTRYPOINT`
🚨 Image must be versioned and include metadata.

* * *

### **Level 15: Multi-Arch Container Build**

🎯 Build and push an image that runs on both ARM64 and x86_64.
🎓 Architect for edge cases + cross-platform support.
🛠️ `buildx`, `qemu`, `--platform`
🚨 Final image must run on a Raspberry Pi and your x86 laptop.

* * *

## 🏆 Bonus Level: Container Gladiator Arena

🎯 Join a container war. Compete with others to:

- Deploy fastest
- Debug mystery container crash
- Minimize image size
- Optimize build time

🎓 All the above skills… **battle-tested**.