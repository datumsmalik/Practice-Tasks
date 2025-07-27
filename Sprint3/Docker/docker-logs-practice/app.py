import time
import os

# Make sure log directory exists
os.makedirs("/app/logs", exist_ok=True)

# Write a new log entry with timestamp
with open("/app/logs/app.log", "a") as f:
    f.write(f"Logged at {time.ctime()}\n")

print("Log written!")


# Build Docker Image (docker build -t log-writer .)

# Run Container with Named Volume (docker volume create logdata)

# Then run the container(docker run --name log1 -v logdata:/app/logs log-writer)

#Check the Logs Inside Volume (docker run --rm -v logdata:/data ubuntu cat /data/app.log)   --rm means container ko automatically del kre de ga run krne k bad
 

# Repeat to Append More Logs (docker run --rm -v logdata:/app/logs log-writer)

#Then check: (docker run --rm -v logdata:/data ubuntu cat /data/app.log)




#Docker's built-in logging system  (  print("Log also sent to stdout")  )

# docker run --rm log-writer
# And check (docker logs log1)
# cat logs/app.log  # On your host machine
 # Basic Command to Stream Logs (docker logs -f <container_name_or_id>)