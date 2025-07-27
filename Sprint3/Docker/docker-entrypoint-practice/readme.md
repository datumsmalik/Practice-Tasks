# Dockerfile Instructions: RUN, CMD, ENTRYPOINT

This README explains the difference between `RUN`, `CMD`, and `ENTRYPOINT` in Dockerfiles with simple explanations and examples.

---

## 🏗️ RUN — Used During Image Build

**What it does:** Executes commands **when building the image**. Used for installing software, updating packages, copying files, etc.

**Runs only once at build time**.

**Example:**
```dockerfile
RUN apt update && apt install -y apache2
```

---

## 🚀 CMD — used when running the container


**It tells Docker::** when the user starts the container, run this default command.**.

**Can be overridden** with `docker run` arguments.

**Example:**
```dockerfile
CMD ["apache2ctl", "-DFOREGROUND"]
```

---

## 🎯 ENTRYPOINT — fixed main command when container runs


**It makes sure one specific command always runs when the container starts.** 

**Arguments passed** to `docker run` are added **after** ENTRYPOINT.

**Example:**
```dockerfile
ENTRYPOINT ["python", "script.py"]
```

**Run command:**
```bash
docker run my-image test
```
This becomes:
```bash
python script.py test
```

---

## 🔁 Combine ENTRYPOINT and CMD

You can combine both:

```dockerfile
ENTRYPOINT ["python", "script.py"]
CMD ["default_arg"]
```

### Examples:
- `docker run my-image` → runs `python script.py default_arg`
- `docker run my-image custom_arg` → runs `python script.py custom_arg`

---

## 🧠 Summary Table

| Instruction  | When It Runs     | Can Be Overridden? | Purpose |
|--------------|------------------|---------------------|---------|
| `RUN`        | At **build time** | ❌ No               | Install/setup tasks |
| `CMD`        | At **run time**   | ✅ Yes              | Default command |
| `ENTRYPOINT` | At **run time**   | 🚫 Only with `--entrypoint` | Force main command |

---

Happy Dockering! 🐳