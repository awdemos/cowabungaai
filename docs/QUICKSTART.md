# Quick Start Commands

> Copy-paste commands for setting up a GPU-enabled CowabungaAI cluster.

## Prerequisites

- k3d installed (`~/.local/bin/k3d`)
- kubectl installed
- k9s installed (optional)
- NVIDIA drivers and Container Toolkit

## One-Time Host Setup

```bash
# Start root podman socket
sudo systemctl start podman.socket

# Enable cgroup delegation (if not already done)
sudo mkdir -p /etc/systemd/system/user@.service.d
cat <<EOF | sudo tee /etc/systemd/system/user@.service.d/delegate.conf
[Service]
Delegate=cpu cpuset io memory pids
EOF
sudo systemctl daemon-reload
```

## Environment

```bash
export DOCKER_HOST=unix:///run/podman/podman.sock
export PATH="/home/a/.local/bin:$PATH"
```

## Create Cluster

```bash
cd /var/home/a/code/cowabungaai
make clean-all
make build-k3d-gpu

k3d cluster create uds \
  --image ghcr.io/defenseunicorns/leapfrogai/k3d-gpu:83ac415c \
  --gpus all \
  --no-lb \
  --k3s-arg "--disable=traefik@server:0" \
  -s 1 \
  --agents 1 \
  --servers-memory 4g \
  --agents-memory 8g \
  --wait
```

## Add Worker Node

```bash
k3d node create gpu-worker-1 \
  --cluster uds \
  --role agent \
  --image ghcr.io/defenseunicorns/leapfrogai/k3d-gpu:83ac415c \
  --memory 8g \
  --gpus all \
  --wait
```

## Configure Access

```bash
k3d kubeconfig merge uds --kubeconfig-switch-context
kubectl cluster-info
kubectl get nodes
```

## Launch k9s

```bash
k9s
```

## Test GPU

```bash
make test-uds-gpu-cluster
```

## Build and Deploy Packages

```bash
make silent-build-gpu
make silent-deploy-gpu
```

## Cleanup

```bash
k3d cluster delete uds
make clean-all
```
