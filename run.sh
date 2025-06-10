#!/bin/bash
# Build and run all containers with increased timeout
DOCKER_CLIENT_TIMEOUT=120
COMPOSE_HTTP_TIMEOUT=120
export DOCKER_CLIENT_TIMEOUT COMPOSE_HTTP_TIMEOUT
docker-compose up --build