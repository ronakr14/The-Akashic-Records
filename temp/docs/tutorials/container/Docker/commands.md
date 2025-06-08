# Docker Commands

## Docker Basic Commands

check docker version

    docker --version or docker -v

display system wide information about docker

    docker info

download an image from Docker Hub

    docker pull <image name>

list local docker images

    docker images or docker image ls

list running containers

    docker ps or docker container ls

list all containers including stopped ones

    docker ps -a or docker container ls -a

create and start a new container from an image

    docker run <options> <image name>

---
## Docker Container Lifecycle

start a stopped container

    docker start <container name/ id>

stop a running container gracefully

    docker stop <container name/ id>

forcefully stop a running container

    docker kill <container name/ id>

restart a container

    docker restart <container name/ id>

remove a stopped container

    docker rm <container name/ id>

---
## Images

Build a Docker image from a dockerfile

    docker build -t <image name> <path to dockerfile>

remove an image

    docker rmi <image name>

remove all unused images

    docker image prune

---
## docker compose

start services defined in a docker compose file

    docker-compose up

stop and remove services defined in a docker compose file

    docker-compose down

list services in a compose file and their status

    docker-compose ps

view logs for a specific service

    docker-compose logs <service_name>

run a command in a running service container

    docker-compose exec <service_name> <command>

---
## Volumes

create a named volume

    docker volume create <volume name>

mount a volume to a container

    docker run -v <volumn name>:<container path>

list volumes

    docker volume ls

remove a volume

    docker volume rm <volumn name>

---
## Docker Registry and Hub

login to docker registry

    docker login

push an image to the registry

    docker push <image name>

pull an image from the registry

    docker pull <image name>

---
## Networks

create a user-defined network

    docker network create <network name>

list networks

    docker network ls

connect a container to a network

    docker network connect <network name> <container name/ id>

disconnect a container from a network

    docker network disconnect <network name> <container name/ id>

inspect a network

    docker network inspect <network name>

---
## Logs and Debugging

view container logs

    docker logs <container name/ id>

start an interactive shell in a running container

    docker exec -it <container name/ id>

display real-time container resource usage.

    docker stats <container name/ id>

get results from container

    docker exec <conainer name/ id> <command to execute>

---
## Cleanup

remove all stopped containers, unused networks, and images

    docker system prune

remove all stopped containers

    docker container prune

remove all unused images

    docker image prune

remove all unused volumes

    docker volumn prune
