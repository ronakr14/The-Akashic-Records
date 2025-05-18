---
id: ohuystool12eg60hkdisyub
title: Quicklearn
desc: ''
updated: 1747574333891
created: 1747574309933
---

# ☸️ Kubernetes 80/20 Mastery Plan

> The average path takes months. We’re not average.

This plan skips the bloated certifications and hand-holding. Instead, it delivers *the 20% of knowledge* that unlocks *80% of real-world Kubernetes mastery* — **fast, hands-on, tactical**.

---

## 🔥 Phase 1: Core 80/20 Concepts — Learn These First

| 🔧 Concept         | 🧠 What You Need to Know                          |
|-------------------|---------------------------------------------------|
| **Pod**           | Smallest deployable unit in K8s. Runs 1+ containers. |
| **Deployment**    | Maintains a desired pod count; handles rollout.     |
| **Service**       | Exposes pods to the cluster/world.                 |
| **ConfigMap**     | Injects non-secret config into pods.               |
| **Secret**        | Injects secure values (base64 encoded).            |
| **Volume**        | Attaches persistent or ephemeral storage.          |
| **Namespace**     | Logical separation between resources.              |
| **kubectl**       | The CLI swiss army knife of K8s.                   |
| **Manifest files**| Declarative YAML defining infrastructure.          |
| **Port-forwarding**| The “dev mode” way to test services.              |

⚠️ Learn `kubectl explain <resource>` — it's the built-in YAML doc tool.

---

## 🧪 Phase 2: Challenge-Based Learning (Gamified)

### ✅ `k8s.01.hello-k8s`
- Launch a `Deployment` of Nginx (3 replicas)
- Expose via `Service` on port 80
- Verify via `kubectl port-forward`

### ✅ `k8s.02.config-secret-env`
- Create a `ConfigMap` and `Secret`
- Mount them into pods as env vars
- Deploy a dummy app that echoes env vars

### ✅ `k8s.03.rolling-deploy`
- Update the image of an app with `Deployment`
- Use `kubectl rollout status`
- Practice rollback

### ✅ `k8s.04.pvc-storage-lab`
- Deploy a pod with a `PersistentVolumeClaim`
- Bind to a dynamic volume (e.g., local-path)
- Write and persist a file

### ✅ `k8s.05.namespace-multitenant`
- Create 2 namespaces: `dev`, `prod`
- Deploy identical apps in both
- Access and manage separately via `-n`

---

## 🧠 Phase 3: Mental Models You Must Grok

- **Everything is declarative**: YAML is king.
- **K8s is a state machine**: You define *what*, K8s handles *how*.
- **Controllers = robots**: Deployments, StatefulSets, DaemonSets → automate workloads.
- **The control plane is sacred**: Don’t mess with `kube-system` unless you know kung fu.

---

## 🚀 Phase 4: Expand to Full Understanding

### 🔁 Complete Understanding Topics

| Area                    | Why It Matters                                       |
|-------------------------|------------------------------------------------------|
| **StatefulSets**        | Required for DBs and apps needing sticky IDs        |
| **DaemonSets**          | One pod per node — log collectors, agents, etc.     |
| **Jobs / CronJobs**     | One-off and scheduled tasks                         |
| **Ingress + IngressController** | HTTP routing and path-based routing         |
| **RBAC**                | Security via Roles and Bindings                     |
| **Helm**                | Templating system for complex deployments           |
| **Horizontal Pod Autoscaler** | Scales based on CPU/memory/metrics            |
| **Custom Resource Definitions (CRDs)** | Extend K8s with your own resources   |
| **Networking (CNI)**    | Container-level IP management and routing           |
| **Service Mesh (Istio/Linkerd)** | Advanced traffic shaping & observability  |
| **Kustomize**           | Native overlay system for K8s manifests             |

---

## 🛠️ Phase 5: Cheatsheet for Daily Ops

```bash
# List everything
kubectl get all -n <namespace>

# Pod logs
kubectl logs <pod-name> -f

# SSH into container
kubectl exec -it <pod-name> -- /bin/bash

# Apply manifest
kubectl apply -f <file>.yaml

# Port forward for local testing
kubectl port-forward svc/<service-name> 8080:80

# Rollout control
kubectl rollout status deployment/<name>
kubectl rollout undo deployment/<name>

# Describe resource
kubectl describe <pod/deployment/service> <name>

# YAML help
kubectl explain deployment.spec.template
````

---

## 🧠 Bonus: GitHub Repo Structure for Practice

```
k8s-labs/
├── 01-hello-k8s/
│   └── deployment.yaml
├── 02-config-secret/
│   └── ...
├── 03-rolling-update/
├── 04-persistent-volumes/
├── 05-namespaces/
└── README.md
```

---

## 📌 Tags

* \#kubernetes
* \#learning/80-20
* \#devops
* \#infrastructure
* \#learning-path

```
