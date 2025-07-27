print("Just a test for prune!")


# Build the Image (docker build -t prune-test .)

#Run a Container from It (docker run --name test1 prune-test)   It will run and exit immediately (container becomes “exited”).

# Create a Volume  (docker volume create unused-vol)

# Check What's There ,,,, images (docker images) ,Containers(docker ps -a) , volumes (docker volume ls)


# Time to Use docker prune Commands

#  docker container prune , docker image prune  , docker image prune ,docker volume prune

# docker system prune     This cleans: Exited containers , Dangling images , Unused volumes , Unused networks


# if want to prune specfic 
# docker rm <container_name_or_id> && docker rmi <image_name_or_id> && docker volume rm <volume_name> && docker network rm <network_name>





