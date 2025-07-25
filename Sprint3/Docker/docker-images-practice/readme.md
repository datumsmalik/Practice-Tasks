# 🖼️ Docker `images` Command Guide

## 🔹 Definition

The `docker images` (or `docker image ls`) command is used to **list all Docker images** stored on your local system.

Docker images are the blueprints for containers — built using `docker build`, pulled using `docker pull`, and run using `docker run`.

---

## ⚙️ Basic Syntax

```bash
docker images
```
or

```bash
docker image ls
```
This lists all locally available images with details like `REPOSITORY`, `TAG`, `IMAGE ID`, `CREATED`, and `SIZE`.

---

## 📋 Common Docker Image Commands

| Command                                | Description                                      | Example                                      |
|----------------------------------------|--------------------------------------------------|----------------------------------------------|
| `docker images`                        | List all local Docker images                     | `docker images`                              |
| `docker image ls`                      | Same as above (preferred modern form)            | `docker image ls`                            |
| `docker image inspect <image>`         | Show low-level JSON metadata                     | `docker image inspect nginx`                 |
| `docker image rm <image>` or `rmi`     | Remove one or more images                        | `docker rmi myapp:1.0`                        |
| `docker image prune`                   | Remove all dangling (unused) images              | `docker image prune`                         |
| `docker image tag <src> <target>`      | Tag an image with a new name                     | `docker tag nginx:latest mynginx:v1`         |
| `docker pull <image>`                  | Download image from Docker Hub or registry       | `docker pull python:3.12`                    |
| `docker push <image>`                  | Upload a tagged image to a registry              | `docker push username/myapp:1.0`             |
| `docker save -o file.tar <image>`      | Save image as `.tar` archive                     | `docker save -o app.tar myapp:1.0`           |
| `docker load -i file.tar`              | Load image from saved `.tar` file                | `docker load -i app.tar`                     |