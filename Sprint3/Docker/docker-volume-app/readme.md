
# 📦 Docker `volume` Command Guide

## 📦 Docker Volume — Definition

A Docker **volume** is a **persistent storage mechanism** used by Docker to store data **outside of the container’s filesystem**.  
This allows data to:
- Persist across container restarts
- Survive image rebuilds
- Be reused across containers

### ✅ Why Use Volumes?
- Managed by Docker
- Portable and isolated
- Preferred for handling persistent data

---

## ⚙️ Basic Syntax

```bash
docker volume [COMMAND]
```

---

## 📋 Common Docker Volume Commands — Table

| Command Example                          | Description                                         |
|------------------------------------------|-----------------------------------------------------|
| `docker volume create mydata`           | Create a new named volume                          |
| `docker volume ls`                      | List all volumes on the system                     |
| `docker volume inspect mydata`         | Show detailed info (mountpoint, usage, etc.)       |
| `docker volume rm mydata`              | Remove a volume (must not be in use)               |
| `docker volume prune`                  | Remove all unused volumes                          |

---

## 🔄 Using Volumes in `docker run`

| Option                                | Description                            | Example                                                      |
|--------------------------------------|----------------------------------------|--------------------------------------------------------------|
| `-v volume_name:/path/in/container`  | Mount named volume                     | `docker run -v mydata:/app/data nginx`                      |
| `-v /host/path:/container/path`      | Mount host directory (bind mount)      | `docker run -v /home/user/logs:/var/log nginx`              |
| `--mount`                            | Alternative to `-v` with clarity       | `docker run --mount type=volume,source=mydata,target=/app/data nginx` |

