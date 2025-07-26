---
id: aoay6jzbqc8vbh503rz86a6
title: Ansible
desc: ''
updated: 1753518000707
created: 1753517994961
---
tags: [master, ansible, automation, devops, configuration-management, infrastructure-as-code]

---

## 📌 Topic Overview

**Ansible** is an open-source, agentless **automation tool** for configuration management, application deployment, and infrastructure orchestration. Built in Python and using **YAML-based playbooks**, Ansible enables **Idempotent** system state enforcement — meaning you declare what a system should look like, and Ansible ensures it gets there without side effects.

> TL;DR: Ansible is your remote control for managing thousands of machines with human-readable instructions.

It's popular for **DevOps**, **CI/CD**, and **multi-cloud** environments because of its simplicity, SSH-based model, and minimal dependencies.

---

## 🚀 80/20 Roadmap

| Stage | Concept                      | Why It Matters                                                        |
|-------|------------------------------|------------------------------------------------------------------------|
| 1️⃣    | Ansible Architecture         | Understand inventory, modules, plugins, and execution flow            |
| 2️⃣    | Inventory Management         | Define hosts and groups to run tasks on                               |
| 3️⃣    | Ad-hoc Commands              | Run one-off commands for testing and debugging                        |
| 4️⃣    | Playbooks & Tasks            | YAML-based automation instructions – the heart of Ansible             |
| 5️⃣    | Roles & Reuse                | Organize playbooks into reusable, modular units                       |
| 6️⃣    | Variables & Templating       | Make your automation dynamic using `vars`, `group_vars`, and Jinja2   |
| 7️⃣    | Handlers, Tags & Conditions | Control task execution flow                                           |
| 8️⃣    | Ansible Vault                | Secure secrets and credentials in playbooks                           |
| 9️⃣    | Ansible Galaxy               | Reuse community-contributed roles                                     |

---

## 🛠️ Practical Tasks

- ✅ Install Ansible (`pip install ansible`)  
- ✅ Create an inventory file with multiple servers  
- ✅ Run ad-hoc commands: `ansible all -m ping`  
- ✅ Write a basic playbook to install NGINX  
- ✅ Use `when:` conditions and `tags` to control task runs  
- ✅ Secure variables with `ansible-vault`  
- ✅ Use roles to organize a multi-service deployment  
- ✅ Pull and use roles from [Ansible Galaxy](https://galaxy.ansible.com)

---

## 🧾 Cheat Sheets

### ▶️ Inventory (INI format)

```ini
[web]
web01 ansible_host=192.168.1.10
web02 ansible_host=192.168.1.11

[db]
db01 ansible_host=192.168.1.20 ansible_user=ubuntu
````

---

### ▶️ Basic Playbook

```yaml
- name: Install and start NGINX
  hosts: web
  become: yes
  tasks:
    - name: Install NGINX
      apt:
        name: nginx
        state: present

    - name: Start NGINX
      service:
        name: nginx
        state: started
```

---

### ▶️ Ad-hoc Command

```bash
ansible all -i inventory.ini -m ping
ansible web -m apt -a "name=nginx state=latest" --become
```

---

## 🎯 Progressive Challenges

| Level           | Challenge                                                                          |
| --------------- | ---------------------------------------------------------------------------------- |
| 🥉 Beginner     | Write a playbook to install a web server on a single host                          |
| 🥈 Intermediate | Use roles to install and configure NGINX + UFW across multiple hosts               |
| 🥇 Advanced     | Implement Ansible Vault to encrypt secrets in playbooks                            |
| 🏆 Expert       | Use dynamic inventory (e.g., AWS EC2) and integrate with Jenkins or GitHub Actions |

---

## 🎙️ Interview Q\&A

* **Q:** What is Ansible and how does it differ from Puppet or Chef?
* **Q:** Explain how Ansible ensures idempotency.
* **Q:** What is the purpose of roles in Ansible?
* **Q:** How would you secure secrets in Ansible?
* **Q:** What’s the difference between a task, a play, and a playbook?

---

## 🛣️ Next Tech Stack Recommendations

* **Terraform** — Infrastructure provisioning (IAC) paired with Ansible for configuration
* **Packer** — Image baking + Ansible for VM provisioning
* **Jenkins / GitHub Actions** — Trigger playbooks via CI pipelines
* **Molecule** — Test Ansible roles with local or Docker test suites
* **Ansible Tower (AWX)** — Web UI and API-driven Ansible control
* **Vault by HashiCorp** — Advanced secrets management

---

## 🔍 Mental Model

> “Think of Ansible as a programmable SSH orchestrator that scales from one server to thousands — without ever installing an agent.”

* ✅ Push-based model — Control from a central machine
* ✅ YAML = Human-readable infra recipes
* ✅ Modular design: Each task is a self-contained unit of automation
* ✅ Idempotent: It won’t redo work unnecessarily
* ✅ Extensible: Modules and plugins for everything from EC2 to Kubernetes
