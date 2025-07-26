---
id: rkrr71htc8istglzh5gbz0j
title: Terraform
desc: ''
updated: 1753517789949
created: 1753517785089
---
tags: [master, terraform, infrastructure-as-code, devops, automation, provisioning]

---

## 📌 Topic Overview

**Terraform** is an open-source **Infrastructure as Code (IaC)** tool by HashiCorp that lets you define, provision, and manage cloud infrastructure using declarative configuration files. You describe *what* you want (not *how*), and Terraform takes care of creating or updating resources across AWS, Azure, GCP, Kubernetes, and more.

> Imagine `git` for your infrastructure — version-controlled, reviewable, and reproducible.

It enables **multi-cloud orchestration**, **DRY templates**, and **modular infrastructure**, making it a favorite in modern DevOps toolchains.

---

## 🚀 80/20 Roadmap

| Stage | Concept                      | Why It Matters                                                   |
|-------|------------------------------|------------------------------------------------------------------|
| 1️⃣    | Providers & Resources        | Core building blocks to talk to your cloud                        |
| 2️⃣    | Terraform CLI Commands       | Plan, apply, destroy — control infra from your terminal           |
| 3️⃣    | Variables & Outputs          | Parameterize configs, pass data between modules                   |
| 4️⃣    | Modules                      | Reusable components = DRY, modular, scalable infra                |
| 5️⃣    | State Management             | Track the real vs desired world; supports remote backends         |
| 6️⃣    | Terraform Cloud / Workspaces | Isolate environments, collaborate with teams                      |
| 7️⃣    | Provisioners & Lifecycle     | Handle special bootstrapping or execution ordering                |

---

## 🛠️ Practical Tasks

- ✅ Install Terraform and configure AWS provider  
- ✅ Write a `.tf` file to create an EC2 instance  
- ✅ Use `terraform plan`, `apply`, `destroy`  
- ✅ Pass variables via `terraform.tfvars`  
- ✅ Use `output` blocks to expose values like instance IP  
- ✅ Create and reuse modules for VPC and networking  
- ✅ Store state in S3 with DynamoDB locking  

---

## 🧾 Cheat Sheets

### ▶️ Basic Terraform File

```hcl
provider "aws" {
  region = "us-west-2"
}

resource "aws_instance" "example" {
  ami           = "ami-123456"
  instance_type = "t2.micro"
}
````

### ▶️ CLI Basics

```bash
terraform init       # initialize project
terraform validate   # check syntax
terraform plan       # preview changes
terraform apply      # create/update infra
terraform destroy    # tear down infra
```

---

### ▶️ Variables and Outputs

```hcl
# variables.tf
variable "instance_type" {
  default = "t2.micro"
}

# outputs.tf
output "instance_ip" {
  value = aws_instance.example.public_ip
}
```

---

### ▶️ Remote State Backend (S3)

```hcl
terraform {
  backend "s3" {
    bucket         = "my-tf-state-bucket"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
  }
}
```

---

## 🎯 Progressive Challenges

| Level           | Challenge                                                               |
| --------------- | ----------------------------------------------------------------------- |
| 🥉 Beginner     | Create an EC2 instance using a Terraform script                         |
| 🥈 Intermediate | Build VPC + subnets + security groups via a module                      |
| 🥇 Advanced     | Configure remote backend with S3 + DynamoDB locking                     |
| 🏆 Expert       | Use workspaces and modules to manage multi-env deployment (dev/staging) |

---

## 🎙️ Interview Q\&A

* **Q:** What is the purpose of `terraform plan`?
* **Q:** How do you manage state in Terraform, and why is it important?
* **Q:** What's the difference between `terraform apply` and `terraform destroy`?
* **Q:** How would you modularize infrastructure with Terraform?
* **Q:** Explain the benefits of remote state backends.

---

## 🛣️ Next Tech Stack Recommendations

* **Terragrunt** — Wrapper for managing complex Terraform configurations
* **Packer** — For building AMIs used in Terraform deployments
* **AWS CDK / Pulumi** — Code-first IaC alternatives
* **Atlantis** — GitOps-style Terraform execution via pull requests
* **Terraform Cloud** — Managed SaaS for team collaboration
* **Infracost** — Estimate costs of infra changes during PR reviews
* **OpenTofu** — Terraform fork for open-source-first IaC philosophy

---

## 🔍 Mental Model

> “Terraform is the *compiler* for your cloud. Write infra in code, and Terraform turns it into reality — idempotently, reproducibly, and predictably.”

* ✅ Think declarative: describe the end state
* ✅ Control the lifecycle via plan → apply → destroy
* ✅ Lock, version, and reuse infrastructure like code

