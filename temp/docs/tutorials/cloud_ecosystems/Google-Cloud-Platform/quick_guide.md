# Google Cloud Platform (GCP) Tutorial

## Overview

Google Cloud Platform (GCP) is a suite of cloud computing services provided by Google. It includes a range of services for computing, storage, databases, machine learning, and networking. GCP enables businesses to scale and innovate using Google's infrastructure.

## Introduction to GCP

### What is Google Cloud Platform?

Google Cloud Platform is a suite of cloud computing services offered by Google. It provides a range of services including computing power, storage, and big data analytics, all of which are hosted on Google's infrastructure.

### Key Features

- **Scalability:** Automatically scales resources based on demand.
- **Global Reach:** Data centers around the world for low-latency access.
- **Security:** Robust security features and compliance certifications.
- **Integration:** Easy integration with other Google services and third-party tools.

## GCP Services

### Compute Services

- **Google Compute Engine:** Scalable virtual machines running in Google’s data centers.
- **Google App Engine:** Platform-as-a-Service (PaaS) for building and deploying applications.
- **Google Kubernetes Engine (GKE):** Managed Kubernetes service for container orchestration.

### Storage Services

- **Google Cloud Storage:** Object storage for unstructured data.
- **Google Cloud Filestore:** Managed file storage for applications.
- **Google Persistent Disk:** Block storage for Google Compute Engine.

### Database Services

- **Google Cloud SQL:** Managed relational database service.
- **Google Cloud Firestore:** NoSQL document database for web and mobile apps.
- **Google Bigtable:** Managed NoSQL database for large analytical and operational workloads.

### Networking Services

- **Google Cloud VPC:** Virtual Private Cloud for network management.
- **Google Cloud Load Balancing:** Distributes traffic across multiple instances.
- **Google Cloud CDN:** Content Delivery Network for low-latency content delivery.

## Google Compute Engine

### Creating a Virtual Machine

Google Compute Engine allows you to create and manage virtual machines in the cloud.

#### Example: Creating a VM using gcloud CLI

```bash
gcloud compute instances create my-instance \
  --zone=us-central1-a \
  --image-family=debian-9 \
  --image-project=debian-cloud \
  --machine-type=n1-standard-1
```

## Google Cloud Storage

### Storing and Retrieving Data

Google Cloud Storage provides scalable object storage for unstructured data.

#### Example: Uploading a File

```bash
gsutil cp local-file.txt gs://my-bucket/
```

#### Example: Downloading a File

```bash
gsutil cp gs://my-bucket/remote-file.txt local-directory/
```

## Google Cloud SQL

### Managing a Relational Database

Google Cloud SQL is a managed database service for SQL databases.

#### Example: Connecting to Cloud SQL

```bash
gcloud sql connect my-instance --user=root
```

#### Example: Creating a Database

```sql
CREATE DATABASE mydatabase;
```

## Google Cloud Functions

### Creating Serverless Functions

Google Cloud Functions allows you to run code in response to events without managing servers.

#### Example: Deploying a Function

```bash
gcloud functions deploy my-function \
  --runtime python39 \
  --trigger-http \
  --allow-unauthenticated
```

#### Example: Function Code (Python)

```python
def hello_world(request):
    return "Hello, World!"
```

## Google Kubernetes Engine (GKE)

### Managing Kubernetes Clusters

Google Kubernetes Engine provides a managed Kubernetes service.

#### Example: Creating a GKE Cluster

```bash
gcloud container clusters create my-cluster \
  --zone us-central1-a
```

#### Example: Deploying an Application

```bash
kubectl create deployment my-app --image=gcr.io/my-project/my-app
kubectl expose deployment my-app --type=LoadBalancer --port 80
```

## Google Cloud Pub/Sub

### Messaging and Event Handling

Google Cloud Pub/Sub is a messaging service for building event-driven systems.

#### Example: Creating a Topic

```bash
gcloud pubsub topics create my-topic
```

#### Example: Publishing a Message

```bash
gcloud pubsub topics publish my-topic --message "Hello, Pub/Sub!"
```

## Google Cloud Networking

### Managing Virtual Networks

Google Cloud Networking services help manage network resources.

#### Example: Creating a VPC Network

```bash
gcloud compute networks create my-network \
  --subnet-mode=auto
```

#### Example: Creating a Firewall Rule

```bash
gcloud compute firewall-rules create allow-ssh \
  --network my-network \
  --allow tcp:22
```

## Google Cloud SDK

### Using the Cloud SDK

The Google Cloud SDK provides command-line tools for managing GCP resources.

#### Example: Installing Cloud SDK

```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud init
```

#### Example: Listing Projects

```bash
gcloud projects list
```

## Summary

This document provides an overview of Google Cloud Platform, including key services such as Google Compute Engine, Cloud Storage, Cloud SQL, Cloud Functions, GKE, Pub/Sub, and Networking. It includes examples for common tasks and commands to help you get started with GCP.