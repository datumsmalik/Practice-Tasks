
# 🐳 Docker `exec` Command Guide

## 🧮 Docker exec — Definition

The `docker exec` command is used to **run a command inside a running container**.  
It's commonly used to:
- Open a shell (`bash`, `sh`)
- Run admin/debug tasks (e.g., checking logs, restarting services)  
All without restarting the container.

---

## ⚙️ Basic Syntax

```bash
docker exec [OPTIONS] <container_name_or_id> <command>
```

### 🔹 Example

```bash
docker exec -it myapp bash
```

> This opens an interactive bash shell inside the `myapp` container.

---

## 📋 Most Common `docker exec` Commands — Table

| Command Example                                     | Description                                                  |
|-----------------------------------------------------|--------------------------------------------------------------|
| `docker exec -it myapp bash`                        | Run in interactive mode with a terminal (bash shell)         |
| `docker exec myapp ls /app`                         | List files in container’s `/app` directory                   |
| `docker exec myapp env`                             | View environment variables inside the container              |
| `docker exec myapp ps aux`                          | View processes running in the container                      |
| `docker exec myapp tail -f /var/log/app.log`        | View logs or file content in real-time                       |
| `docker exec myapp service nginx restart`           | Restart nginx service (if supported in container OS)         |
| `docker exec --user root myapp whoami`              | Run command as a specific user (`root` in this case)         |

