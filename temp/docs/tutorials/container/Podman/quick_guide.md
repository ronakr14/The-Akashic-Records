# Podman Tutorial

## Overview

Podman is an open-source container management tool designed to be a drop-in replacement for Docker. It allows you to manage containers and pods without requiring a daemon.

## Installing Podman

### On Linux

To install Podman on a Linux system, use the package manager specific to your distribution:

#### Debian/Ubuntu

```sh
sudo apt update
sudo apt install -y podman
```

#### Fedora

```sh
sudo dnf install -y podman
```

#### CentOS/RHEL

```sh
sudo yum install -y podman
```

### On macOS

To install Podman on macOS, you can use Homebrew:

```sh
brew install podman
```

### On Windows

To install Podman on Windows, you can use the Podman Windows installer available from the [Podman releases page](https://github.com/containers/podman/releases).

## Basic Podman Commands

### 1. `podman --version`

Check the installed Podman version.

```sh
podman --version
```

#### Example

```sh
podman version 4.0.0
```

### 2. `podman pull`

Download a container image from a registry.

```sh
podman pull image_name
```

#### Example

```sh
podman pull nginx
```

### 3. `podman images`

List all available container images on your system.

```sh
podman images
```

#### Example

```sh
REPOSITORY          TAG       IMAGE ID       CREATED       SIZE
nginx               latest    f6b22f3dfc8f   2 weeks ago   133MB
```

### 4. `podman rmi`

Remove a container image.

```sh
podman rmi image_name
```

#### Example

```sh
podman rmi nginx
```

### 5. `podman run`

Run a container from an image.

```sh
podman run [OPTIONS] image_name
```

#### Example

```sh
podman run -d -p 80:80 nginx
```

### 6. `podman ps`

List running containers.

```sh
podman ps
```

#### Example

```sh
CONTAINER ID  IMAGE     COMMAND                  CREATED         STATUS         PORTS                NAMES
abcd1234efgh  nginx     "nginx -g 'daemon of…"   10 minutes ago  Up 10 minutes  0.0.0.0:80->80/tcp   quizzical_hermann
```

### 7. `podman stop`

Stop a running container.

```sh
podman stop container_id
```

#### Example

```sh
podman stop abcd1234efgh
```

### 8. `podman rm`

Remove a stopped container.

```sh
podman rm container_id
```

#### Example

```sh
podman rm abcd1234efgh
```

### 9. `podman exec`

Execute a command inside a running container.

```sh
podman exec -it container_id command
```

#### Example

```sh
podman exec -it abcd1234efgh /bin/bash
```

## Working with Pods

A Pod is a group of one or more containers that share the same network namespace.

### 1. `podman pod create`

Create a new pod.

```sh
podman pod create --name pod_name
```

#### Example

```sh
podman pod create --name my-pod
```

### 2. `podman pod ps`

List all pods.

```sh
podman pod ps
```

#### Example

```sh
POD ID        NAME    STATUS    CREATED         INFRA ID
abcd1234efgh  my-pod  Running   10 minutes ago  efgh5678ijkl
```

### 3. `podman pod stop`

Stop a running pod.

```sh
podman pod stop pod_name
```

#### Example

```sh
podman pod stop my-pod
```

### 4. `podman pod rm`

Remove a pod.

```sh
podman pod rm pod_name
```

#### Example

```sh
podman pod rm my-pod
```

## Example YAML Files

### Container Definition

Podman does not use YAML files natively for container definitions. Instead, you use `podman run` commands or create Podman-compatible configuration files manually.

### Pod Definition

Podman supports Kubernetes YAML files for defining pods.

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

To apply the YAML configuration, use:

```sh
podman play kube pod.yaml
```

## Summary

This tutorial introduces fundamental Podman commands and concepts. Podman provides a powerful and flexible way to manage containers and pods without a central daemon. For more detailed information, refer to the [official Podman documentation](https://podman.io/).