
# 🧱 COPY — Definition in Dockerfile

The `COPY` instruction in a Dockerfile copies files or directories from your host machine (the context) into the Docker image during the build process.

## Syntax

```dockerfile
COPY <src> <dest>
```
- `<src>`: Source path on host (relative to the build context).
- `<dest>`: Destination path in the Docker image.

You can also use the `--chown` flag to change the ownership of the copied files.

---

## 📋 Common COPY Commands — Table Format

| **Command/Usage**                     | **Description**                                                                 | **Example**                                                |
|--------------------------------------|---------------------------------------------------------------------------------|------------------------------------------------------------|
| `COPY . /app`                        | Copies **all files and folders** from current directory to `/app` in the image | `COPY . /app`                                              |
| `COPY src/ /app/src/`                | Copies the `src` folder from host to `/app/src/` inside the image              | `COPY src/ /app/src/`                                      |
| `COPY requirements.txt /app/`       | Copies a specific file (like requirements.txt) to a path in the image          | `COPY requirements.txt /app/`                              |
| `COPY ["file1", "file2", "/dest"]`  | JSON array syntax: Copies multiple files to a destination directory            | `COPY ["index.js", "package.json", "/app/"]`              |
| `COPY --chown=user:group . /app`     | Copies all files and sets ownership in image to `user:group`                   | `COPY --chown=appuser:appgroup . /app`                    |
| `COPY config/*.yml /etc/config/`     | Copies all `.yml` files from `config/` to `/etc/config/`                       | `COPY config/*.yml /etc/config/`                          |
| `COPY ./build/ /usr/share/nginx/html`| Copies the `build` directory to nginx folder in image                          | `COPY ./build/ /usr/share/nginx/html`                     |
| `COPY ./backend /app/backend/`       | Copies a sub-directory to another path                                         | `COPY ./backend /app/backend/`                            |