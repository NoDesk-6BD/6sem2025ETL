#!/usr/bin/env bash
set -euo pipefail

# Load .env.docker into the current shell
if [ -f ".env.docker" ]; then
  # export all vars from .env.docker
  set -a
  source ./.env.docker
  set +a
else
  echo ".env.docker not found!"
  exit 1
fi

# Default container name (adjust if you renamed it in docker-compose.yml)
CONTAINER_NAME="nodesk-mongo"

# Connect to mongo using root creds from env file
docker exec -it "$CONTAINER_NAME" mongosh \
  -u "$MONGO_INITDB_ROOT_USERNAME" \
  -p "$MONGO_INITDB_ROOT_PASSWORD" \
  --authenticationDatabase admin
