#!/bin/bash

# Build the Docker image
docker stop some-backend-taskanline
docker rm some-backend-taskanline
docker rmi backend-taskanline

docker build -t backend-taskanline .

# Run the Docker container
docker run -d -p 8000:8000 --envfile .env --name some-backend-taskanline backend-taskanline
