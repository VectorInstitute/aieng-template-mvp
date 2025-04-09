#!/bin/bash

# Build script for deploying the MVP application

set -e

# Set environment variables
BUILD_ID=$(date +%Y%m%d%H%M%S)
export BUILD_ID

# Load environment variables
if [ "$ENVIRONMENT" == "production" ]; then
  echo "Building for production..."
  ENV_FILE=".env.production"
  DOCKER_COMPOSE_FILE="docker-compose.yml"
else
  echo "Building for development..."
  ENV_FILE=".env.development"
  DOCKER_COMPOSE_FILE="docker-compose.dev.yml"
fi

# Build the application
echo "Building application using $DOCKER_COMPOSE_FILE..."
docker compose --env-file "$ENV_FILE" -f "$DOCKER_COMPOSE_FILE" build

# Optional: Push to a container registry
# if [ "$PUSH_TO_REGISTRY" == "true" ]; then
#   echo "Pushing images to registry..."
#   docker compose -f "$DOCKER_COMPOSE_FILE" push
# fi

echo "Build completed successfully!"
