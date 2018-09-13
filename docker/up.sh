#!/bin/sh
# A script to spin up the docker cluster
docker-compose -f docker/compose.yml up --build -d
