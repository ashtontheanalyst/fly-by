#!/usr/bin/env bash
# This script builds the new Docker image, deletes any containers running the old image
# and builds a new container from the new image.
set -euo pipefail

IMAGE="ashtonrwsmith/fly-by"
CONTAINER="fly-by"
PORT="8008"

echo "Building $IMAGE..."
docker build --tag "$IMAGE" .

echo "Removing old container (if it exists)..."
docker rm -f "$CONTAINER" 2>/dev/null || true

echo "Starting new container..."
docker run --detach --name "$CONTAINER" --publish "$PORT:$PORT" "$IMAGE"

echo "Done. Running at http://localhost:$PORT"
docker ps --filter "name=$CONTAINER"