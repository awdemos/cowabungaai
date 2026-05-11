#!/bin/bash
# Docker Helper Script for CowabungaAI GPU Deployment
# This script ensures Docker commands run with proper privileges for GPU support

set -euo pipefail

# Set DOCKER_SOCK to a path that podman can mount (workaround for rootless podman)
export DOCKER_SOCK="${DOCKER_SOCK:-/tmp/k3d-docker/docker.sock}"
if [[ ! -e "$DOCKER_SOCK" ]]; then
    mkdir -p "$(dirname "$DOCKER_SOCK")"
    touch "$DOCKER_SOCK"
    chmod 666 "$DOCKER_SOCK"
fi

# Function to run docker with root privileges if needed
docker_root() {
    if [[ $EUID -ne 0 ]]; then
        # Check if user is in docker group
        if groups | grep -q '\bdocker\b' || groups | grep -q '\bpodman\b'; then
            docker "$@"
        else
            echo "Warning: User not in docker group, using sudo..."
            sudo docker "$@"
        fi
    else
        docker "$@"
    fi
}

# Function to run k3d with proper GPU flags
k3d_gpu_cluster_create() {
    local cluster_name="${1:-uds}"
    local image="${2:-ghcr.io/defenseunicorns/leapfrogai/k3d-gpu:latest}"
    
    echo "Creating GPU-enabled k3d cluster: $cluster_name"
    echo "Using DOCKER_SOCK=$DOCKER_SOCK"
    
    # Ensure NVIDIA runtime is configured
    if command -v nvidia-ctk &> /dev/null; then
        echo "Configuring NVIDIA container runtime..."
        sudo nvidia-ctk runtime configure --runtime=docker || true
    fi
    
    # Create cluster with GPU support
    DOCKER_SOCK="$DOCKER_SOCK" k3d cluster create "$cluster_name" \
        --gpus all \
        --image "$image" \
        --servers 1 \
        --agents 1 \
        --servers-memory 4g \
        --agents-memory 8g \
        --wait
    
    echo "Cluster $cluster_name created successfully with GPU support"
}

# Function to add worker node with GPU
k3d_add_gpu_worker() {
    local cluster_name="${1:-uds}"
    local node_name="${2:-gpu-worker-1}"
    local image="${3:-ghcr.io/defenseunicorns/leapfrogai/k3d-gpu:latest}"
    
    echo "Adding GPU worker node $node_name to cluster $cluster_name"
    
    k3d node create "$node_name" \
        --cluster "$cluster_name" \
        --role agent \
        --image "$image" \
        --memory 8g \
        --wait
    
    echo "Worker node $node_name added successfully"
}

# Export functions for use in other scripts
export -f docker_root
export -f k3d_gpu_cluster_create
export -f k3d_add_gpu_worker

# If called directly with arguments, execute the appropriate function
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    case "${1:-}" in
        create-cluster)
            shift
            k3d_gpu_cluster_create "$@"
            ;;
        add-worker)
            shift
            k3d_add_gpu_worker "$@"
            ;;
        docker)
            shift
            docker_root "$@"
            ;;
        *)
            echo "Usage: $0 {create-cluster|add-worker|docker} [args...]"
            echo ""
            echo "Commands:"
            echo "  create-cluster [name] [image]  - Create GPU-enabled k3d cluster"
            echo "  add-worker [cluster] [name]    - Add GPU worker node to cluster"
            echo "  docker [args...]               - Run docker with root privileges"
            exit 1
            ;;
    esac
fi
