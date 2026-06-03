#!/bin/bash

# Docker run script for Resident Orca

set -e

IMAGE_NAME="resident-orca"
CONTAINER_NAME="orca-c2"

echo "🐋 Building Docker image..."
docker build -t $IMAGE_NAME .

echo "Starting Resident Orca container..."
docker run -d \
    --name $CONTAINER_NAME \
    --hostname orca-c2 \
    -p 5000:5000 \
    -p 8080:8080 \
    -v orca_data:/app/.resident_orca \
    -v orca_reports:/app/orca_reports \
    --cap-add=NET_ADMIN \
    --cap-add=NET_RAW \
    --restart unless-stopped \
    $IMAGE_NAME

echo "✅ Container started: $CONTAINER_NAME"
echo "🌐 Web Dashboard: http://localhost:5000"
echo ""
echo "View logs: docker logs -f $CONTAINER_NAME"
echo "Stop: docker stop $CONTAINER_NAME"