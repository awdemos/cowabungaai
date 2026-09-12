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

# Node pool labels. GPU workloads should nodeSelect cowabungaai/gpu=true;
# everything else stays on the unlabeled pool by default (or via anti-affinity).
GPU_NODE_LABEL="cowabungaai/gpu=true"
CPU_NODE_LABEL="cowabungaai/cpu=true"

# Function to run k3d with proper GPU flags
k3d_gpu_cluster_create() {
    local cluster_name="${1:-uds}"
    local image="${2:-ghcr.io/defenseunicorns/leapfrogai/k3d-gpu:latest}"
    local taint_gpu_node="${TAINT_GPU_NODE:-false}"

    # Rootless podman cannot run a functional k3s cluster: kube-proxy needs
    # NET_ADMIN/iptables (userspace mode was removed in k8s 1.28), and k3s
    # --rootless needs subuid delegation a container userns does not have.
    # The podman-docker shim does not serve docker's info template, so fall
    # back to podman info.
    local rootless=""
    rootless=$(docker info --format '{{.Host.Security.Rootless}}' 2>/dev/null || true)
    if [ -z "$rootless" ] && command -v podman >/dev/null 2>&1; then
        rootless=$(podman info --format '{{.Host.Security.Rootless}}' 2>/dev/null || true)
    fi
    if [ "$rootless" = "true" ]; then
        cat >&2 <<'EOF'
WARNING: your container engine is rootless podman. k3s will NOT run
functionally here (kubelet needs the KubeletInUserNamespace gate, but
kube-proxy then fails: no iptables/NET_ADMIN, and userspace proxy mode was
removed in Kubernetes 1.28).

Working options on this host:
  1. Rootful podman socket (recommended):
       sudo podman system service -p 2375 --log-level=warn &
       export DOCKER_HOST=tcp://127.0.0.1:2375
       scripts/docker-helper.sh create-cluster
     (GPU passthrough additionally needs an nvidia CDI spec:
      sudo nvidia-ctk cdi generate --output=/etc/cdi/nvidia.yaml)
  2. Any rootful docker host.
EOF
        return 1
    fi

    echo "Creating GPU-enabled k3d cluster: $cluster_name"
    echo "Shape: 1 server + 2 agents (agent-0 = GPU pool, agent-1 = CPU pool)"
    echo "Using DOCKER_SOCK=$DOCKER_SOCK"

    # Ensure NVIDIA runtime is configured
    if command -v nvidia-ctk &> /dev/null; then
        echo "Configuring NVIDIA container runtime..."
        sudo nvidia-ctk runtime configure --runtime=docker || true
    fi

    # Create cluster with GPU support.
    # NOTE: k3d (v5.7) only supports --gpus at cluster scope, so every node
    # container sees the physical GPU; the cowabungaai/gpu label is the
    # scheduling control, not the device plugin's resource accounting.
    # NOTE: under rootless podman (the common setup on this host) kubelet
    # cannot open /dev/kmsg without the KubeletInUserNamespace feature gate.
    DOCKER_SOCK="$DOCKER_SOCK" k3d cluster create "$cluster_name" \
        --gpus all \
        --image "$image" \
        --servers 1 \
        --agents 2 \
        --servers-memory 4g \
        --agents-memory 8g \
        --k3s-node-label "$GPU_NODE_LABEL@agent:0" \
        --k3s-node-label "$CPU_NODE_LABEL@agent:1" \
        --k3s-arg "--kubelet-arg=feature-gates=KubeletInUserNamespace=true@server:*" \
        --k3s-arg "--kubelet-arg=feature-gates=KubeletInUserNamespace=true@agent:*" \
        --wait

    if [[ "$taint_gpu_node" == "true" ]]; then
        echo "Tainting GPU agent (NoSchedule) for dedicated GPU workloads..."
        local gpu_agent
        gpu_agent=$(kubectl get nodes -l "$GPU_NODE_LABEL" -o jsonpath='{.items[0].metadata.name}')
        kubectl taint nodes "$gpu_agent" "$GPU_NODE_LABEL:NoSchedule"
    fi

    echo "Cluster $cluster_name created successfully with GPU support"
    echo "GPU pool:  kubectl get nodes -l $GPU_NODE_LABEL"
    echo "CPU pool:  kubectl get nodes -l $CPU_NODE_LABEL"
}

# Function to add a worker node. k3d v5.7 `node create` has no --gpus flag, so
# added nodes inherit cluster-scope GPU access; label them into the right pool.
k3d_add_gpu_worker() {
    local cluster_name="${1:-uds}"
    local node_name="${2:-gpu-worker-1}"
    local image="${3:-ghcr.io/defenseunicorns/leapfrogai/k3d-gpu:latest}"
    local label="${4:-$GPU_NODE_LABEL}"

    echo "Adding worker node $node_name (label: $label) to cluster $cluster_name"

    k3d node create "$node_name" \
        --cluster "$cluster_name" \
        --role agent \
        --image "$image" \
        --memory 8g \
        --k3s-node-label "$label" \
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
