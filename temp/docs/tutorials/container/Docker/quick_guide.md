# Docker Tutorial

## Overview

Docker is an open-source platform that automates the deployment, scaling, and management of applications using containerization. Containers are lightweight, portable, and ensure consistency across different environments.

## Installing Docker

### On Linux

To install Docker on a Linux system, follow these steps:

```sh
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io
```

### On macOS

1. Download Docker Desktop for Mac from the [Docker website](https://www.docker.com/products/docker-desktop).
2. Open the downloaded `.dmg` file and drag Docker to your Applications folder.
3. Open Docker from your Applications folder.

### On Windows

1. Download Docker Desktop for Windows from the [Docker website](https://www.docker.com/products/docker-desktop).
2. Run the installer and follow the installation instructions.
3. Start Docker Desktop from your Start menu.

## Basic Docker Commands

### 1. `docker --version`

Check the installed Docker version.

```sh
docker --version
```

#### Example

```sh
Docker version 20.10.8, build 3967b7d
```

### 2. `docker pull`

Download an image from Docker Hub.

```sh
docker pull image_name
```

#### Example

```sh
docker pull nginx
```

### 3. `docker images`

List all available Docker images on your system.

```sh
docker images
```

#### Example

```sh
REPOSITORY          TAG       IMAGE ID       CREATED       SIZE
nginx               latest    f6b22f3dfc8f   2 weeks ago   133MB
```

### 4. `docker rmi`

Remove a Docker image.

```sh
docker rmi image_name
```

#### Example

```sh
docker rmi nginx
```

### 5. `docker run`

Run a Docker container from an image.

```sh
docker run [OPTIONS] image_name
```

#### Example

```sh
docker run -d -p 80:80 nginx
```

### 6. `docker ps`

List running Docker containers.

```sh
docker ps
```

#### Example

```sh
CONTAINER ID   IMAGE     COMMAND                  CREATED         STATUS         PORTS                NAMES
abcd1234efgh   nginx     "nginx -g 'daemon of…"   10 minutes ago  Up 10 minutes  0.0.0.0:80->80/tcp   quizzical_hermann
```

### 7. `docker stop`

Stop a running Docker container.

```sh
docker stop container_id
```

#### Example

```sh
docker stop abcd1234efgh
```

### 8. `docker rm`

Remove a stopped Docker container.

```sh
docker rm container_id
```

#### Example

```sh
docker rm abcd1234efgh
```

### 9. `docker exec`

Execute a command inside a running container.

```sh
docker exec -it container_id command
```

#### Example

```sh
docker exec -it abcd1234efgh /bin/bash
```

### 10. `docker-compose`

`docker-compose` is a tool for defining and running multi-container Docker applications.

#### Example `docker-compose.yml`

```yaml
version: '3'
services:
  web:
    image: nginx
    ports:
      - "8080:80"
  db:
    image: postgres
    environment:
      POSTGRES_DB: exampledb
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
```

#### Commands

- **Start Services**: `docker-compose up`
- **Stop Services**: `docker-compose down`
- **View Logs**: `docker-compose logs`

## Dockerfile

A Dockerfile is a script that contains a series of instructions to create a Docker image.

### Example Dockerfile

```dockerfile
# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]
```

### Build Image

```sh
docker build -t my-python-app .
```

### Run Container

```sh
docker run -p 4000:80 my-python-app
```

## Summary

Docker simplifies application deployment by using containers that package code and dependencies together. Understanding these basic commands will help you get started with Docker and manage your containerized applications effectively. For more detailed information, refer to the [official Docker documentation](https://docs.docker.com/).