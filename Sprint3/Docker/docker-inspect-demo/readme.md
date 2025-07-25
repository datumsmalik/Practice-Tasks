
# 🔍 Docker `inspect` Command Guide

## 🔍 Docker Inspect — Definition

The `docker inspect` command is used to retrieve **detailed, low-level information (in JSON format)** about:
- Containers
- Images
- Networks
- Volumes

It’s commonly used for:
- Debugging
- Checking IP addresses
- Environment variables
- Mounts and metadata

---

## ⚙️ Basic Syntax

```bash
docker inspect [OPTIONS] NAME|ID [NAME|ID...]
```

### 🔹 Example

```bash
docker inspect my_container
```

> Returns a full JSON output with all details about the container.

---

## 📋 Common `docker inspect` Commands — Table

| Command Example                                      | Description                                    |
|------------------------------------------------------|------------------------------------------------|
| `docker inspect myapp`                               | Full metadata of a container                   |
| `docker inspect nginx`                               | Full metadata of an image                      |
| `docker inspect myvolume`                            | Inspect a volume                               |
| `docker inspect bridge`                              | Inspect a Docker network                       |
| `docker inspect -f '{{.State.Status}}' myapp`        | Extract specific field using Go template       |
| `docker inspect -f '{{json .Config.Env}}' myapp`     | Output environment variables in JSON format    |

---

## 🧠 Most Useful Fields (with `-f`)

| Use Case            | Format String                            | Example Command                                          |
|---------------------|-------------------------------------------|----------------------------------------------------------|
| Container status     | `{{.State.Status}}`                      | `docker inspect -f '{{.State.Status}}' myapp`            |
| Container IP address | `{{.NetworkSettings.IPAddress}}`         | `docker inspect -f '{{.NetworkSettings.IPAddress}}' myapp`|
| Environment vars     | `{{.Config.Env}}`                        | `docker inspect -f '{{.Config.Env}}' myapp`              |
| Mounts info          | `{{.Mounts}}`                            | `docker inspect -f '{{.Mounts}}' myapp`                  |

---

## ✅ Real-World Example

```bash
docker inspect -f '{{.NetworkSettings.IPAddress}}' nginx
```

> Quickly shows the container's IP address.

---
