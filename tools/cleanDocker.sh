# kill running containers
docker kill $(docker ps -q)
# delete exited containers
docker rm -v $(docker ps -a -q -f status=exited)
# delete images
docker rmi $(docker images -f "dangling=true" -q)
# delete all images
docker rmi $(docker images -q)
# delete vfs
docker run -v /var/run/docker.sock:/var/run/docker.sock -v /var/lib/docker:/var/lib/docker --rm martin/docker-cleanup-volumes
