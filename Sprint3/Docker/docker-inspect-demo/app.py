print("Hello from inspect container!")


# Build the Image (docker build -t inspect-demo .)

# Run the Container (docker run -d --name inspectme inspect-demo) -d runs it in detached mode (background)

# Base command: (docker inspect inspectme)     This returns full JSON metadata for the container.





