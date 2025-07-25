
# 🧹 Docker `prune` Command Guide

## 🧹 Docker Prune — Definition

The `docker prune` family of commands is used to **clean up unused Docker resources** like:
- Stopped containers
- Dangling images
- Unused volumes
- Unused networks

It helps **free up disk space** and **keep your Docker environment clean**.

---

## ⚙️ Basic Syntax

```bash
docker <resource> prune [OPTIONS]
```

You can prune all unused:
- Containers
- Images
- Volumes
- Networks
- Or everything at once!

---

## 📋 Common `docker prune` Commands — Table

| Command Example                        | Description                                                  |
|----------------------------------------|--------------------------------------------------------------|
| `docker container prune`              | Remove all stopped containers                                |
| `docker image prune`                  | Remove all dangling (unused) images                          |
| `docker volume prune`                 | Remove all unused volumes                                    |
| `docker network prune`                | Remove all unused networks                                   |
| `docker system prune`                 | Remove all unused data (containers, networks, images, cache) |
| `docker system prune -a`              | Remove all unused data including unused (not just dangling) images |
| `docker image prune -f`               | Prune images without confirmation prompt                     |

---

## 🧠 Quick Summary of What They Clean

| Command               | Cleans                           |
|-----------------------|----------------------------------|
| `container prune`     | Stopped containers               |
| `image prune`         | Dangling images (no tags)        |
| `volume prune`        | Volumes not used by any container|
| `network prune`       | Unused networks                  |
| `system prune`        | All of the above + build cache   |

---

## ✅ Real-World Cleanup Example

```bash
docker system prune -a -f
```

> Cleans up everything not in use (including unused images).  
Skips confirmation due to `-f`.

---
