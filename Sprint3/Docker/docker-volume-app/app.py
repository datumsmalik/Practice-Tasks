# app.py
import time

with open("/app/logs/log.txt", "a") as f:
    f.write(f"Log entry at {time.ctime()}\n")

print("Log written!")


#This writes the current timestamp into log.txt inside /app/logs.

#Build Docker Image  (docker build -t py-logger .)

#Create a Volume   (docker volume create logvolume)


#Volume mount means connecting external storage (managed by Docker) to a folder inside a container.
#Run Container with Volume Mounted   (docker run --name log-container -v logvolume:/app/logs py-logger) py-logger vol name he ,  -v logvolume:/app/logs (Mount a Docker volume named logvolume to the container path /app/logs)
#-v stands for volume mount.



# Create a Volume  (docker volume create logvolume)

#Run another container to see the log content (docker run --rm -v logvolume:/logs ubuntu cat /logs/log.txt)

#The log file grows with new entries. (docker run --rm -v logvolume:/app/logs py-logger)
