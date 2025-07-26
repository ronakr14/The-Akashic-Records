---
id: p97ut7qjoonbvd4pc8m4vb4
title: Grafana
desc: ''
updated: 1753517771322
created: 1753517766199
---
tags: [master, grafana, observability, dashboards, metrics, monitoring]

---

## 📌 Topic Overview

**Grafana** is an open-source **observability and dashboard platform** used for visualizing metrics, logs, and traces. It's the go-to solution for developers, SREs, and DevOps engineers to create beautiful dashboards and monitor everything from server health to application performance.

> Think of it as the **command center** for your systems—if something blinks red, Grafana's how you know.

It integrates with **Prometheus**, **Loki**, **InfluxDB**, **Elasticsearch**, and many more data sources, and provides **alerting, templating, and plugin support**.

---

## 🚀 80/20 Roadmap

| Stage | Concept                    | Why It Matters                                                |
|-------|----------------------------|----------------------------------------------------------------|
| 1️⃣    | Data sources (Prometheus, Loki) | Without this, Grafana is just a blank canvas                  |
| 2️⃣    | Panels & Visualizations   | Convert raw data into human-friendly insights                  |
| 3️⃣    | Dashboards & Variables    | Reusable, dynamic dashboards for every environment             |
| 4️⃣    | Alerts & Notifications    | Proactive monitoring via Slack, Email, PagerDuty, etc.         |
| 5️⃣    | Permissions & Teams       | Secure multi-tenant access to dashboards                       |
| 6️⃣    | Plugins & Extensibility   | Integrate custom charts, tools, or even data sources           |
| 7️⃣    | JSON Model / API usage    | Automate dashboard provisioning and deployment                 |

---

## 🛠️ Practical Tasks

- ✅ Connect Prometheus as a data source  
- ✅ Create a system-level dashboard showing CPU, memory, and disk  
- ✅ Add templating variables to switch between services/nodes  
- ✅ Set alerting thresholds with Slack integration  
- ✅ Export and import dashboards using JSON  
- ✅ Install community plugins (e.g., for Gantt, heatmap, etc.)  
- ✅ Use Grafana CLI to manage datasources and dashboards  

---

## 🧾 Cheat Sheets

### ▶️ Connecting Prometheus as a Data Source

1. **Settings → Data Sources → Add data source**
2. Choose **Prometheus**
3. URL: `http://<prometheus-server>:9090`
4. Click **Save & Test**

---

### ▶️ Creating a Dashboard Panel

1. New Dashboard → **Add Panel**
2. Select **data source**
3. Enter a PromQL query like:
   ```promql
   rate(http_requests_total[5m])
````

4. Choose visualization type (Graph, Table, Gauge, etc.)
5. Save panel and dashboard

---

### ▶️ Example Templating Variable

```bash
Label values query:
label_values(instance)
```

Use in PromQL:

```promql
rate(http_requests_total{instance=~"$instance"}[5m])
```

---

### ▶️ CLI Commands

```bash
grafana-cli plugins install <plugin-id>
systemctl restart grafana-server
```

---

## 🎯 Progressive Challenges

| Level           | Challenge                                                      |
| --------------- | -------------------------------------------------------------- |
| 🥉 Beginner     | Create a CPU + memory + disk dashboard from Prometheus         |
| 🥈 Intermediate | Add templating to make dashboards environment-aware            |
| 🥇 Advanced     | Trigger alerts based on error rates with PagerDuty integration |
| 🏆 Expert       | Automate dashboard deployment using Grafana API or Terraform   |

---

## 🎙️ Interview Q\&A

* **Q:** What is Grafana used for in observability?
* **Q:** How do you set up alerting in Grafana?
* **Q:** How does Grafana compare with Kibana or Datadog?
* **Q:** Can you explain templating in dashboards?
* **Q:** How would you manage dashboards across environments?

---

## 🛣️ Next Tech Stack Recommendations

* **Prometheus** — Ideal metrics backend for Grafana
* **Loki** — Log aggregation designed to complement Prometheus
* **Tempo** — For distributed tracing visualization
* **Grafana Cloud** — Managed SaaS version with extra features
* **InfluxDB / Elasticsearch** — Alternative data sources
* **Terraform Provider Grafana** — For infrastructure-as-code dashboard provisioning
* **K6 + Grafana** — Performance testing and results visualization

---

## 🔍 Mental Model

> “Grafana turns firehose telemetry into meaningful visual alerts. It’s the **lens on top of your metrics stack**.”

* ✅ Decouples visualization from metric collection
* ✅ Focuses on readability, customization, and alerts
* ✅ Not a log processor or metrics collector by itself—just the renderer
