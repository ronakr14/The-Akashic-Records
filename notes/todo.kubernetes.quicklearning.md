---
id: v80fcke5juz2enssnz2znbl
title: Kubernetes Quicklearning
desc: ''
updated: 1747580268002
created: 1747580228734
---

## 🧩 Kubernetes Challenge Series: "Conquer K8s"

### 🎮 Game Mechanics

* **Mode**: Solo Quests 🧙 + Team Raids 👥
* **Tools**: Minikube / Kind (local), Play with K8s (online), kubeadm for advanced
* **Level Up**: Pass criteria → Git commit proof → Badge/unlock next tier
* **Bonus XP**: Finish under time limit or with least YAML

---

## 🟢 **Level 1: KUBIE CADET** (Easy)

### 1. `kubie-init`

**Goal**: Spin up a local Kubernetes cluster.

* ✅ Task: Use Minikube or Kind to start a cluster.
* ✅ Verify: `kubectl get nodes` returns Ready.

---

### 2. `deploy-n-go`

**Goal**: Deploy your first app.

* ✅ Task: Create Deployment for nginx with 2 replicas.
* ✅ Verify: Pods running, exposed via ClusterIP service.

---

### 3. `secret-agent`

**Goal**: Use ConfigMap + Secret like a spy.

* ✅ Task: Create app that reads config from a ConfigMap + credentials from Secret.
* ✅ Bonus XP: Use environment variable + mounted secret file.

---

### 4. `health-check`

**Goal**: Add readiness/liveness probes to your app.

* ✅ Verify: Pod restarts when unhealthy.

---

### 5. `kube-cleanup`

**Goal**: Delete everything you made — but cleanly.

* ✅ Task: Create namespace `playground`; deploy all resources there and nuke it at once.

---

## 🟡 **Level 2: POD PROFESSIONAL** (Intermediate)

### 6. `scale-up`

**Goal**: Enable autoscaling.

* ✅ Task: Add HorizontalPodAutoscaler to nginx; simulate load with `siege`.
* ✅ Bonus XP: Set custom CPU threshold.

---

### 7. `pvc-warrior`

**Goal**: Attach persistent storage to a pod.

* ✅ Task: Deploy a pod with a PVC using `hostPath` or dynamic provisioning.
* ✅ Bonus XP: Store logs or SQLite data.

---

### 8. `RBAC-me-not`

**Goal**: Create a user with limited permissions.

* ✅ Task: Add ServiceAccount that can only get pods.
* ✅ Bonus XP: Try and fail to list secrets using that account.

---

### 9. `net-bender`

**Goal**: Block all traffic between pods except whitelisted ones.

* ✅ Task: Implement NetworkPolicy to only allow frontend to talk to backend.

---

### 10. `blue-green-zebra`

**Goal**: Blue-green deployment.

* ✅ Task: Set up two deployments behind one service, switch over cleanly.
* ✅ Bonus XP: Automate using `kubectl rollout`.

---

## 🔴 **Level 3: CLUSTER COMMANDER** (Expert)

### 11. `chaos-fighter`

**Goal**: Survive a pod failure storm.

* ✅ Task: Install Litmus or Kube-monkey and inject failures.
* ✅ Bonus XP: Implement a recovery strategy.

---

### 12. `multi-zone-me`

**Goal**: Design for fault tolerance.

* ✅ Task: Use node labels + affinity/anti-affinity to spread pods.
* ✅ Bonus XP: Enforce across multiple availability zones.

---

### 13. `metrics-mage`

**Goal**: Monitor with Prometheus + Grafana.

* ✅ Task: Install monitoring stack via Helm.
* ✅ Bonus XP: Create custom alert rule.

---

### 14. `GitOps-hero`

**Goal**: Automate deployments via GitOps.

* ✅ Task: Install ArgoCD and sync a repo.
* ✅ Bonus XP: Auto-promote based on Git tag.

---

### 15. `CI/CD overlord`

**Goal**: Integrate Jenkins with Kubernetes.

* ✅ Task: Build & deploy a container from code to pod using Jenkins pipeline.
* ✅ Bonus XP: Use `kaniko` to build without Docker daemon.

---

## 🏆 Bonus Round: **"THE FINAL BOSS — FULL K8S STACK"**

**Mission**: Deploy a production-grade stack:

* Ingress Controller
* TLS + Cert-Manager
* Stateful DB with PVC
* App with HPA
* RBAC rules
* GitOps pipeline

Deliver it. Demo it. Own it.

---
