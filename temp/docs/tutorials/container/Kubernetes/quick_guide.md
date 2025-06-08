# Kubernetes Tutorial

## Overview

Kubernetes is an open-source platform designed to automate deploying, scaling, and operating application containers. It orchestrates containerized applications across a cluster of machines, providing tools for managing containerized applications.

## Key Concepts

### 1. Cluster

A Kubernetes cluster consists of a set of nodes that run containerized applications. Each cluster has a master node and worker nodes.

### 2. Pod

A Pod is the smallest deployable unit in Kubernetes. It can contain one or more containers that share the same network namespace and storage.

### 3. Deployment

A Deployment manages a set of identical Pods, ensuring that the specified number of Pods are running and available.

### 4. Service

A Service exposes a set of Pods as a network service. It provides load balancing and service discovery.

### 5. Namespace

Namespaces provide a mechanism for isolating groups of resources within a single cluster.

## Basic Commands

### 1. `kubectl version`

Check the version of `kubectl` and the Kubernetes cluster.

```sh
kubectl version
```

### 2. `kubectl get nodes`

List all nodes in the cluster.

```sh
kubectl get nodes
```

#### Example

```sh
NAME          STATUS   ROLES    AGE   VERSION
node1          Ready    master   10d   v1.21.0
node2          Ready    <none>   10d   v1.21.0
```

### 3. `kubectl get pods`

List all Pods in the current namespace.

```sh
kubectl get pods
```

#### Example

```sh
NAME                     READY   STATUS    RESTARTS   AGE
nginx-deployment-7fb8d6b9b-8qj7g   1/1     Running   0          5m
```

### 4. `kubectl create`

Create a resource from a file or from stdin.

```sh
kubectl create -f resource.yaml
```

#### Example

Create a Pod from a YAML file:

```sh
kubectl create -f pod.yaml
```

### 5. `kubectl apply`

Apply a configuration change to a resource.

```sh
kubectl apply -f resource.yaml
```

#### Example

Update a Deployment with a new configuration:

```sh
kubectl apply -f deployment.yaml
```

### 6. `kubectl delete`

Delete a resource.

```sh
kubectl delete -f resource.yaml
```

#### Example

Delete a Pod:

```sh
kubectl delete pod nginx-deployment-7fb8d6b9b-8qj7g
```

### 7. `kubectl describe`

Show detailed information about a resource.

```sh
kubectl describe pod pod_name
```

#### Example

```sh
kubectl describe pod nginx-deployment-7fb8d6b9b-8qj7g
```

### 8. `kubectl logs`

Print the logs for a container in a Pod.

```sh
kubectl logs pod_name
```

#### Example

```sh
kubectl logs nginx-deployment-7fb8d6b9b-8qj7g
```

## Example YAML Files

### Pod Definition

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
  - name: my-container
    image: nginx
    ports:
    - containerPort: 80
```

### Deployment Definition

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx
        ports:
        - containerPort: 80
```

### Service Definition

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  selector:
    app: nginx
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: LoadBalancer
```

## Namespaces

Namespaces help you organize resources in a cluster.

### Create a Namespace

```sh
kubectl create namespace my-namespace
```

### List Namespaces

```sh
kubectl get namespaces
```

### Use a Namespace

```sh
kubectl config set-context --current --namespace=my-namespace
```

## Summary

This tutorial introduces fundamental Kubernetes concepts and commands. Kubernetes simplifies container orchestration and management, making it easier to deploy and scale applications. For more detailed information, refer to the [official Kubernetes documentation](https://kubernetes.io/docs/home/).