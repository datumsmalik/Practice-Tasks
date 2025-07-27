# app.py
print("Hello from ARG practice!")


# Build with default value (APP_NAME = "default-app")        (docker build -t arg-demo-default .)
#Build with custom APP_NAME (docker build -t arg-demo-custom --build-arg APP_NAME=arg-folder .)

# Run and Inspect (docker run --rm arg-demo-default)
# (docker run --rm arg-demo-custom)



# ARG	Used at build time
# ENV	Used at runtime