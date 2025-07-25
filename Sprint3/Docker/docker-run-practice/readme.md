# 🚀 Docker `run` Command Guide

## 🔹 Definition

The `docker run` command is used to **create and start a new container** from a Docker image.

It is one of the most commonly used Docker commands, allowing you to:

- Run containers interactively or in the background
- Map ports between host and container
- Mount volumes or bind mounts
- Set environment variables
- Assign custom container names
- Control runtime behavior

---

## ⚙️ Basic Syntax

```bash
docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
```

**Example:**

```bash
docker run ubuntu echo "Hello, Docker!"
```

## 📋 Common docker run Options

| Option              | Description                                 | Example                                |
|---------------------|---------------------------------------------|----------------------------------------|
| `-d`, `--detach`     | Run container in the background             | `docker run -d nginx`                  |
| `-it`               | Run interactively with terminal (good for shells) | `docker run -it ubuntu bash`     |
| `--name`            | Assign a custom name to the container       | `docker run --name webserver nginx`    |
| `-p`                | Map host port to container port             | `docker run -p 8080:80 nginx`          |
| `-v`                | Mount volume or host directory              | `docker run -v mydata:/data nginx`     |
| `--rm`              | Automatically remove container when it exits | `docker run --rm ubuntu`              |
| `-e`                | Set environment variable                    | `docker run -e ENV=prod myapp`         |
| `--env-file`        | Load env variables from a file              | `docker run --env-file .env myapp`     |
| `--network`         | Connect to a specific Docker network        | `docker run --network mynet nginx`     |
| `--restart`         | Set restart policy (always, on-failure)     | `docker run --restart always myapp`    |
| `--entrypoint`      | Override default image entrypoint           | `docker run --entrypoint /bin/sh myapp`|
| `--cpus` / `--memory` | Limit CPU or memory                        | `docker run --memory 512m myapp`       |

## ✅ Real Example

```bash
docker run -d --name mynginx -p 8080:80 nginx
```

- Runs nginx in background mode
- Maps host port 8080 to container port 80
- Names the container `mynginx`