#!/bin/sh
# A script to spin down the docker cluster
docker-compose -f docker/compose.yml down
docker system prune --volumes
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker rmi $(docker images -aq)
