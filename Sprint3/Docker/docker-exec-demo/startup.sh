#!/bin/bash
echo "Container started!"

#Keep running forever by watching a file that never changes
#tail -f: Follows the end of a file and waits for new lines (like real-time log watching).

tail -f /dev/null 







#The docker exec command is used to run a command inside a running container. It's commonly used to open a shell (bash, sh) or run admin/debug tasks (e.g., checking logs, restarting services) without restarting the container.

# Build the Docker Image (docker build -t exec-demo .)
# Run the Container (Detached)   (docker run -dit --name myexeccontainer exec-demo)

#-d: Detached (background)

#-i: Interactive

#-t: Allocate a pseudo-TTY

#--name myexeccontainer: Name your container



# Create a Folder Inside the Container (docker exec myexeccontainer mkdir /workspace/testdir)
# Create a File in the Folder (docker exec myexeccontainer bash -c "echo 'Hello exec!' > /workspace/testdir/hello.txt")
#  Read the File (docker exec myexeccontainer cat /workspace/testdir/hello.txt)
#  List Files Inside Container (docker exec myexeccontainer ls /workspace/testdir)
#  direct container me jana he to (docker exec -it myexeccontainer bash)
