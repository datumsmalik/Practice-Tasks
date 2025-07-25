
# 📄 Docker `logs` Command Guide

## 📄 Docker Logs — Definition

The `docker logs` command is used to **fetch logs from a running or stopped container**.  
It shows the standard output (`stdout`) and standard error (`stderr`) of the main process inside the container — helpful for:
- Debugging
- Monitoring
- Troubleshooting

---

## ⚙️ Basic Syntax

```bash
docker logs [OPTIONS] <container_name_or_id>
```

### 🔹 Example

```bash
docker logs myapp
```

> Shows all logs from the container named `myapp`.

---

## 📋 Common `docker logs` Commands — Table

| Command Example                          | Description                                               |
|------------------------------------------|-----------------------------------------------------------|
| `docker logs web`                        | Show all logs of the container                            |
| `docker logs -f web`                     | Continuously stream logs (like `tail -f`)                 |
| `docker logs --tail 100 web`             | Show only the last 100 lines of logs                      |
| `docker logs -t web`                     | Show timestamps with each log line                        |
| `docker logs --since 10m web`            | Show logs from the last 10 minutes                        |
| `docker logs --until 1h web`             | Show logs up to 1 hour ago                                |
| `docker logs -n 50 web`                  | Alias for `--tail`, show last 50 lines of logs            |

---

