
# 🧱 ARG — Definition in Dockerfile

The `ARG` instruction is used to define **build-time variables** in a Dockerfile. These variables can be passed using `--build-arg` when running `docker build`.

## 🔧 Syntax

```dockerfile
ARG <name>[=<default_value>]
```
- `name`: Name of the argument.
- `default_value` (optional): A fallback value used if the build doesn’t provide one.

### 📌 Key Points
- `ARG` is **only available at build-time**, not at runtime (unlike `ENV`).
- Useful for customizing builds (base image version, app version, etc).

---

## 📋 Common ARG Commands — Table Format

| **Command/Usage**                            | **Description**                                                                 | **Example**                                                       |
|---------------------------------------------|---------------------------------------------------------------------------------|-------------------------------------------------------------------|
| `ARG VERSION=1.0`                            | Declares a build-time argument with a default value                            | `ARG VERSION=1.0`                                                 |
| `FROM python:${VERSION}`                     | Uses an `ARG` in the `FROM` instruction (must be declared before `FROM`)       | `ARG VERSION=3.10` <br> `FROM python:${VERSION}`                  |
| `ARG APP_ENV`                                | Declares an argument without a default value                                   | `ARG APP_ENV`                                                     |
| `ENV APP_ENV=${APP_ENV}`                     | Converts a build-time argument to a runtime environment variable               | `ARG APP_ENV` <br> `ENV APP_ENV=${APP_ENV}`                       |
| `RUN echo "Building version $VERSION"`       | Uses `ARG` value in a shell command inside the image                           | `ARG VERSION=1.2` <br> `RUN echo "Building version $VERSION"`     |
| `docker build --build-arg VERSION=2.0 .`     | Passes a custom value for the argument during build                            | CLI usage with: `ARG VERSION` in Dockerfile                       |
| `ARG DEBIAN_FRONTEND=noninteractive`         | Prevents interactive prompts in apt installs                                   | `ARG DEBIAN_FRONTEND=noninteractive`                             |
| `ARG UID=1000` <br> `RUN useradd -u $UID app`| Creates a user with a custom UID using an ARG                                  | `ARG UID=1000` <br> `RUN useradd -u $UID app`                     |

---

## 🔄 ARG vs ENV

| Feature        | `ARG`                        | `ENV`                         |
|----------------|------------------------------|-------------------------------|
| Scope          | Build-time only              | Build-time + Runtime          |