# 🛠️ Docker `build` Command Guide

## 🔹 Definition

The `docker build` command is used to create a Docker image from a set of instructions written in a Dockerfile.

It packages your application code, dependencies, and runtime environment into an image that can be run as a container.

---

## ⚙️ Basic Syntax

```bash
docker build [OPTIONS] PATH
```

`PATH` is usually `.` (the current directory containing the Dockerfile)

**Example:**

```bash
docker build -t myapp:1.0 .
```
This command builds an image from the current directory and tags it as `myapp:1.0`.

---

## 📋 Common docker build Options

| Option              | Description                                     | Example                                  |
|---------------------|-------------------------------------------------|------------------------------------------|
| `-t`, `--tag`       | Tag the image with name and optionally version  | `docker build -t myapp:latest .`         |
| `-f`, `--file`      | Specify a custom Dockerfile                     | `docker build -f Dockerfile.dev .`       |
| `--no-cache`        | Build the image without using cache             | `docker build --no-cache -t myapp .`     |
| `--build-arg`       | Pass build-time variables to Dockerfile         | `docker build --build-arg ENV=prod .`    |
| `--target`          | Specify the build stage in multi-stage builds   | `docker build --target builder .`        |
| `--platform`        | Set the target platform (e.g. linux/amd64)      | `docker build --platform linux/amd64 .`  |
| `--pull`            | Always pull the latest version of the base image| `docker build --pull .`                  |
| `--progress`        | Show build output style (auto, plain, tty)      | `docker build --progress=plain .`        |
| `--output`          | Specify output location (e.g. export to tar)    | `docker build --output type=tar,dest=image.tar .` |