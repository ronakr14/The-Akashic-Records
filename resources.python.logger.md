---
id: 72547uonpdyn2m1l6jbczwq
title: Logger
desc: ''
updated: 1753338638018
created: 1753338633018
---
tags: [master, logger]

## 📌 Topic Overview

**Logging** is:

* The practice of recording runtime information from applications for **debugging, monitoring, and auditing**.
* Essential for diagnosing issues, tracking application behavior, and maintaining observability in production systems.
* In Python, the built-in **`logging`** module provides a flexible framework for emitting log messages.
* Supports different **log levels** (DEBUG, INFO, WARNING, ERROR, CRITICAL) to categorize the severity of events.
* Enables output to various destinations: console, files, remote servers, or external log management systems.
* Facilitates formatting, filtering, and contextual information injection.
* Critical for compliance, security audits, and proactive alerting in production environments.

## 🚀 80/20 Roadmap

| Stage | Concept                                | Reason                                              |
| ----- | ------------------------------------ | ---------------------------------------------------|
| 1️⃣   | Basic logging setup                   | Capture logs in console or file                      |
| 2️⃣   | Log levels and severity               | Filter important vs verbose messages                 |
| 3️⃣   | Formatters and handlers               | Customize log output and destinations                |
| 4️⃣   | Logger hierarchy and naming           | Organize logs per module or component                |
| 5️⃣   | Contextual logging (extra, filters)   | Add dynamic info like user IDs, request IDs          |
| 6️⃣   | Rotating and timed file handlers      | Manage log file size and retention                    |
| 7️⃣   | Integration with monitoring systems   | Forward logs to ELK, Splunk, or cloud logging        |
| 8️⃣   | Structured logging (JSON, key-value)  | Enable machine-readable logs for analytics           |
| 9️⃣   | Exception and traceback logging       | Capture detailed error info for troubleshooting      |
| 🔟    | Performance considerations            | Minimize overhead and log safely in multithreaded apps |

---

## 🛠️ Practical Tasks

* ✅ Set up a basic logger that writes to console.
* ✅ Log messages at different severity levels.
* ✅ Configure logging to output to a file with timestamps.
* ✅ Create custom log formats including module name and line number.
* ✅ Use multiple handlers to log to console and file simultaneously.
* ✅ Implement rotating file handlers to archive logs after size/time limits.
* ✅ Add contextual information using `LoggerAdapter` or filters.
* ✅ Capture and log exceptions with tracebacks.
* ✅ Integrate logging with external log management services.
* ✅ Use structured JSON logging for modern observability stacks.

---

## 🧾 Cheat Sheets

### 🔹 Basic Logging Setup

```python
import logging

logging.basicConfig(level=logging.INFO)
logging.info("This is an info message")
logging.error("This is an error message")
````

### 🔹 Custom Logger with Handlers and Formatters

```python
logger = logging.getLogger("myapp")
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
file_handler = logging.FileHandler("app.log")

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

logger.debug("Debug message")
```

### 🔹 Rotating File Handler

```python
from logging.handlers import RotatingFileHandler

rotating_handler = RotatingFileHandler("app.log", maxBytes=1024*1024*5, backupCount=3)
rotating_handler.setFormatter(formatter)
logger.addHandler(rotating_handler)
```

### 🔹 Logging Exceptions with Traceback

```python
try:
    1 / 0
except ZeroDivisionError:
    logger.exception("An error occurred")
```

---

## 🎯 Progressive Challenges

| Level           | Task                                                          |
| --------------- | ------------------------------------------------------------- |
| 🥉 Easy         | Configure console and file logging with different levels      |
| 🥈 Intermediate | Implement rotating file handlers and log format customization |
| 🥇 Advanced     | Add contextual data and use LoggerAdapters                    |
| 🏆 Expert       | Integrate structured JSON logging and send logs remotely      |

---

## 🎙️ Interview Q\&A

* **Q:** What are the different log levels and when would you use them?
* **Q:** How do handlers and formatters work in Python logging?
* **Q:** What is the purpose of a LoggerAdapter?
* **Q:** How can you rotate logs and why is it important?
* **Q:** How do you capture exceptions in logs with tracebacks?
* **Q:** What is structured logging and why does it matter?
* **Q:** How would you ensure logging does not impact app performance?

---

## 🛣️ Next Tech Stack Recommendations

* **ELK Stack (Elasticsearch, Logstash, Kibana)** — Centralized log management and visualization.
* **Prometheus + Grafana** — For monitoring and alerting alongside logs.
* **Fluentd / Fluent Bit** — Log forwarding and aggregation agents.
* **Sentry / Rollbar** — Error tracking with detailed logging integration.
* **Loguru** — Python logging library with simpler syntax and more features.

---

## 🧠 Pro Tips

* Always log at appropriate levels to avoid noise.
* Use unique logger names per module for easier filtering.
* Avoid logging sensitive information such as passwords or tokens.
* Test your logging configuration in production-like environments.
* Use asynchronous logging if performance is critical.
* Structure logs when integrating with modern log analysis tools.

---

## 🧬 Tactical Philosophy

> **Logging is your application's memory — if you don’t log properly, you’re flying blind. Effective logging is about balance: enough detail to diagnose issues, but not so much you drown in noise.**

⚙️ Plan your log strategy as part of your app design.
🔐 Treat logs as sensitive data; secure and sanitize them.
📈 Continuously refine logging based on incident postmortems.
💣 Avoid blocking application flow due to logging overhead.
🤖 Automate log analysis to get ahead of problems, not just react.

---
