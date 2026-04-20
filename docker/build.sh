#!/usr/bin/env bash
set -euo pipefail

IMAGE_REGISTRY="${IMAGE_REGISTRY:-docker.io}"
IMAGE_REPO="${IMAGE_REPO:-leifhh/pcai-chat-demo}"
IMAGE_TAG="${IMAGE_TAG:-0.1.0}"
IMAGE="${IMAGE_REGISTRY}/${IMAGE_REPO}:${IMAGE_TAG}"

# Build from repo root so Dockerfile COPY paths resolve
cd "$(dirname "$0")/.."

echo "Building ${IMAGE} ..."
docker build -f docker/Dockerfile -t "${IMAGE}" .

echo "Pushing ${IMAGE} ..."
docker push "${IMAGE}"

echo "Done: ${IMAGE}"
