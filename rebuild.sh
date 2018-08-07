#!/usr/bin/env bash

docker build -t webapp .
docker stack deploy -c docker-compose.yml webappstack
