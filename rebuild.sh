#!/usr/bin/env bash

docker build -t webapp .
docker tag webapp arthur2706/webapp:v2
docker push arthur2706/webapp:v2
docker stack deploy -c docker-compose.yml webappstack