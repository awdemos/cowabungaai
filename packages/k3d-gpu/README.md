# K3D GPU

Prepares a `k3s` + `nvidia/cuda` base image that enables a K3D cluster to utilize your host machine's NVIDIA, CUDA-capable GPU(s).

This is for development and demonstration purposes, and should not be used to deploy CowabungaAI in a production environment.

## Table of Contents

- [Pre-Requisites](#pre-requisites)
- [Environment Requirements](#environment-requirements)
- [Deployment](#deployment)
  - [Standard Setup](#standard-setup)
  - [With Root Podman](#with-root-podman)
  - [With Docker](#with-docker)
- [Adding Worker Nodes](#adding-worker-nodes)
- [Accessing the Cluster](#accessing-the-cluster)
  - [With kubectl](#with-kubectl)
  - [With k9s](#with-k9s)
- [Testing GPU](#testing-gpu)
- [Troubleshooting](#troubleshooting)
- [References](#references)

## Pre-Requisites

All system requirements and pre-requisites from the [CowabungaAI documentation website](https://docs.leapfrog.ai/docs/local-deploy-guide/quick_start/).

### Required Software

- [k3d](https://k3d.io/) v5.6.0+
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- Podman (rootful) or Docker
- NVIDIA drivers and [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)

## Environment Requirements

> [!IMPORTANT]
> **Rootless podman is NOT supported** for running Kubernetes clusters. Kubernetes requires capabilities that rootless containers cannot provide:
> - cgroup v2 controller delegation (cpuset, cpu, memory)
> - iptables/netfilter rules (CAP_NET_ADMIN)
> - /dev/kmsg access
> - sysctl modifications
>
> You must use **rootful podman** or **Docker** to create the cluster.

### Rootful Podman Setup

If using podman, ensure the root podman socket is running:

```bash
# Start root podman socket (requires sudo/pkexec one-time)
sudo systemctl start podman.socket

# Verify it's listening
sudo systemctl status podman.socket
```

Configure k3d to use root podman:

```bash
export DOCKER_HOST=unix:///run/podman/podman.sock
```

### Docker Setup

Docker runs as root by default, so no special configuration is needed:

```bash
# Docker should already be running
sudo systemctl status docker
```

### cgroup v2 Delegation (Required for podman)

Ensure your host has proper cgroup delegation for user sessions:

```bash
# Check current delegation
cat /sys/fs/cgroup/user.slice/user-$(id -u).slice/user@$(id -u).service/cgroup.subtree_control

# Should show: cpuset cpu io memory pids
# If cpuset is missing, fix it:
sudo mkdir -p /etc/systemd/system/user@.service.d
cat <<EOF | sudo tee /etc/systemd/system/user@.service.d/delegate.conf
[Service]
Delegate=cpu cpuset io memory pids
EOF
sudo systemctl daemon-reload
# Log out and back in for changes to take effect
```

## Deployment

### Standard Setup

> [!NOTE]
> The following Make targets can be executed from the root of the CowabungaAI repository or within this sub-directory.

To deploy a new K3d cluster with [UDS Core Slim Dev](https://github.com/defenseunicorns/uds-core#uds-package-development):

```bash
make create-uds-gpu-cluster
```

Or manually:

```bash
# Clean and setup
make clean-all

# Build GPU image
make build-k3d-gpu

# Create cluster with 1 server + 1 agent
k3d cluster create uds \
  --gpus all \
  --image ghcr.io/defenseunicorns/leapfrogai/k3d-gpu:$(git rev-parse --short HEAD) \
  --servers 1 \
  --agents 1 \
  --servers-memory 4g \
  --agents-memory 8g \
  --wait
```

### With Root Podman

When using root podman, configure k3d before creating the cluster:

```bash
# Set DOCKER_HOST to root podman socket
export DOCKER_HOST=unix:///run/podman/podman.sock

# Create cluster (uses root podman)
k3d cluster create uds \
  --gpus all \
  --image ghcr.io/defenseunicorns/leapfrogai/k3d-gpu:$(git rev-parse --short HEAD) \
  --servers 1 \
  --agents 1 \
  --servers-memory 4g \
  --agents-memory 8g \
  --wait
```

### With Docker

```bash
# Docker uses /var/run/docker.sock by default
k3d cluster create uds \
  --gpus all \
  --image ghcr.io/defenseunicorns/leapfrogai/k3d-gpu:$(git rev-parse --short HEAD) \
  --servers 1 \
  --agents 1 \
  --servers-memory 4g \
  --agents-memory 8g \
  --wait
```

## Adding Worker Nodes

After the cluster is running, add additional GPU worker nodes:

```bash
# Export DOCKER_HOST if using root podman
export DOCKER_HOST=unix:///run/podman/podman.sock

# Add worker node
k3d node create gpu-worker-1 \
  --cluster uds \
  --role agent \
  --image ghcr.io/defenseunicorns/leapfrogai/k3d-gpu:$(git rev-parse --short HEAD) \
  --memory 8g \
  --gpus all \
  --wait
```

Or use the provided helper:

```bash
make add-gpu-worker
```

## Accessing the Cluster

### With kubectl

After cluster creation, k3d automatically updates your kubeconfig:

```bash
# Verify cluster is accessible
kubectl cluster-info

# List nodes
kubectl get nodes

# List all pods
kubectl get pods -A
```

If kubectl cannot connect, manually load the kubeconfig:

```bash
k3d kubeconfig merge uds --kubeconfig-switch-context
# Or
export KUBECONFIG=$(k3d kubeconfig write uds)
```

### With k9s

k9s is a terminal-based UI for managing Kubernetes clusters.

#### Installation

```bash
# Install k9s
# Via package manager (Fedora)
sudo dnf install k9s

# Or download binary
curl -sS https://webinstall.dev/k9s | bash
```

#### Usage with UDS

If using UDS CLI, k9s is included:

```bash
# Via UDS CLI (recommended if using UDS)
uds zarf tools monitor

# Or with alias
alias k9s='uds zarf tools monitor'
k9s
```

#### Direct Usage

```bash
# Ensure kubeconfig is set
kubectl cluster-info

# Launch k9s
k9s

# Key bindings:
#   ?     - Show help
#   /     - Search/filter
#   :pods - View pods
#   :ns   - View namespaces
#   :svc  - View services
#   d     - Describe resource
#   l     - View logs
#   s     - Shell into container
#   q     - Quit
```

#### Common k9s Workflows

```bash
# View all pods across namespaces
k9s -A

# View pods in specific namespace
k9s -n leapfrogai

# View GPU-related resources
k9s -n kube-system
# Then filter for nvidia: /nvidia
```

## Testing GPU

Verify GPU is accessible in the cluster:

```bash
# Run test pod
make test-uds-gpu-cluster

# Or manually
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: cuda-vector-add
spec:
  restartPolicy: OnFailure
  containers:
    - name: cuda-vector-add
      image: nvidia/cuda:12.4.1-base-ubuntu22.04
      command: ["nvidia-smi"]
      resources:
        limits:
          nvidia.com/gpu: 1
EOF

kubectl logs cuda-vector-add
```

## Troubleshooting

### "failed to find cpuset cgroup (v2)"

**Cause**: cgroup delegation missing cpuset controller

**Fix**:
```bash
sudo mkdir -p /etc/systemd/system/user@.service.d
cat <<EOF | sudo tee /etc/systemd/system/user@.service.d/delegate.conf
[Service]
Delegate=cpu cpuset io memory pids
EOF
sudo systemctl daemon-reload
# Log out and back in
```

### "iptables is not available on this host"

**Cause**: Using rootless podman which lacks CAP_NET_ADMIN

**Fix**: Use rootful podman or Docker instead.

### "Cannot connect to the Docker daemon"

**Cause**: DOCKER_HOST not set correctly for root podman

**Fix**:
```bash
export DOCKER_HOST=unix:///run/podman/podman.sock
systemctl status podman.socket  # Verify root socket is running
```

### "dial tcp 0.0.0.0:PORT: connect: connection refused"

**Cause**: kubectl inside toolbox/container cannot reach host's localhost

**Fix**: Update kubeconfig to use the host's IP address instead of localhost:

```bash
# Get host IP
HOST_IP=$(hostname -I | awk '{print $1}')

# Update kubeconfig server URL
kubectl config set-cluster k3d-uds --server=https://$HOST_IP:6443
```

Or use host networking from outside the container.

### k9s shows "Boom!! runtime error"

**Cause**: No valid kubeconfig or cluster unreachable

**Fix**:
```bash
# Verify kubectl works first
kubectl get nodes

# If not, fix kubeconfig
k3d kubeconfig merge uds --kubeconfig-switch-context
```

## References

- [k3d CUDA Guide](https://k3d.io/v5.7.2/usage/advanced/cuda/)
- [k3d Documentation](https://k3d.io/)
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)
- [Rootless Podman Limitations](https://github.com/containers/podman/blob/main/rootless.md)
- [k9s Documentation](https://k9scli.io/)
