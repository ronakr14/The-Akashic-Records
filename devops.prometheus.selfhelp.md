---
id: dw0vffv3s9q5darcejo15ib
title: Selfhelp
desc: ''
updated: 1753517973317
created: 1753517967882
---
tags: [master, prometheus, monitoring, observability, devops, metrics]

---

## 📌 Topic Overview

**Prometheus** is a powerful open-source **metrics-based monitoring and alerting system** originally built at SoundCloud. It scrapes metrics from configured endpoints, stores time-series data, and lets you query it via a flexible language called **PromQL**.

It's the beating heart of modern observability stacks and the default monitoring solution in **Kubernetes environments**, often paired with **Grafana** for visualization.

> Think of Prometheus as the “metrics time machine” — it records everything and answers "what happened, when, and how much?"

---

## 🚀 80/20 Roadmap

| Stage | Concept                        | Why It Matters                                                   |
|-------|--------------------------------|------------------------------------------------------------------|
| 1️⃣    | Prometheus Architecture        | Understand core components: TSDB, exporters, scraper, alertmanager |
| 2️⃣    | Exporters                      | Metrics exposure for apps and systems (e.g., Node Exporter)      |
| 3️⃣    | Prometheus Configuration      | `prometheus.yml` file with scrape jobs and targets               |
| 4️⃣    | PromQL                         | Query language to analyze and aggregate time-series data         |
| 5️⃣    | Alerting Rules & Alertmanager | Trigger automated alerts with conditions and receivers           |
| 6️⃣    | Service Discovery (K8s etc.)  | Dynamic target registration for scalable environments            |
| 7️⃣    | Grafana Integration            | Turn metrics into dashboards                                     |

---

## 🛠️ Practical Tasks

- ✅ Install Prometheus using Docker or a binary  
- ✅ Use Node Exporter to expose system-level metrics  
- ✅ Write basic `prometheus.yml` with custom scrape intervals  
- ✅ Query CPU usage with PromQL: `rate(node_cpu_seconds_total[5m])`  
- ✅ Create alerting rules for high memory usage  
- ✅ Connect Prometheus to Alertmanager with email/Slack integration  
- ✅ Visualize metrics in Grafana  

---

## 🧾 Cheat Sheets

### ▶️ Prometheus Configuration (Minimal)

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: "node"
    static_configs:
      - targets: ["localhost:9100"]
````

### ▶️ Common PromQL Queries

```sql
# CPU usage per core
rate(node_cpu_seconds_total{mode!="idle"}[1m])

# Memory usage
node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes

# Disk space
node_filesystem_free_bytes / node_filesystem_size_bytes
```

---

### ▶️ Alerting Rule

```yaml
groups:
  - name: example-alerts
    rules:
      - alert: HighCPUUsage
        expr: avg(rate(node_cpu_seconds_total{mode="user"}[5m])) > 0.85
        for: 1m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage on instance"
```

---

## 🎯 Progressive Challenges

| Level           | Challenge                                                                 |
| --------------- | ------------------------------------------------------------------------- |
| 🥉 Beginner     | Scrape metrics from your local system with Node Exporter                  |
| 🥈 Intermediate | Write PromQL queries to monitor disk, memory, and CPU trends              |
| 🥇 Advanced     | Configure Alertmanager with email and Slack notifications                 |
| 🏆 Expert       | Use Kubernetes service discovery to auto-scrape pods in a dynamic cluster |

---

## 🎙️ Interview Q\&A

* **Q:** What is Prometheus and how does it differ from traditional monitoring tools?
* **Q:** What is an exporter in Prometheus?
* **Q:** How does Prometheus achieve high availability and scalability?
* **Q:** Can you explain a real-world PromQL query you wrote and used?
* **Q:** How does Prometheus integrate with Grafana and Alertmanager?

---

## 🛣️ Next Tech Stack Recommendations

* **Grafana** — Rich dashboards and alert visualizations
* **Thanos** — Long-term storage and global view for Prometheus
* **VictoriaMetrics** — High-performance alternative TSDB
* **Loki** — Logs companion to Prometheus metrics
* **Alertmanager** — Core alert delivery and grouping system
* **OpenMetrics / OTEL Collector** — For standardized observability pipelines
* **Kube-prometheus-stack** — Helm stack for full Kubernetes observability setup

---

## 🔍 Mental Model

> “Prometheus treats your system like a living organism — constantly measuring vitals (metrics), analyzing health (queries), and calling for help (alerts) when things go sideways.”

* ✅ Pull-based model: Prometheus asks, exporters answer
* ✅ Time-series everything: All data is stored with a timestamp
* ✅ Ephemeral-safe: Works great with dynamic, containerized environments
* ✅ Declarative config: You control what gets scraped and when
