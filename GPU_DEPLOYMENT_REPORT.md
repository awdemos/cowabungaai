# CowabungaAI GPU Deployment Report

## Date: 2026-05-10
## Status: COMPLETE - Documentation Updated

---

## What Was Accomplished

### 1. Clean Commands Executed
- Ran `make clean-all` successfully
- Removed all artifacts, cache, logs, and build files
- Deleted existing k3d cluster

### 2. Docker Helper Created
- Created `/var/home/a/code/cowabungaai/scripts/docker-helper.sh`
- Sets `DOCKER_SOCK` workaround for rootless podman
- Provides helper functions for cluster creation and worker management

### 3. GPU Image Built
- Built k3d GPU image: `ghcr.io/defenseunicorns/leapfrogai/k3d-gpu:83ac415c`
- Based on k3s v1.28.8-k3s1 + NVIDIA CUDA 12.4.1
- Includes NVIDIA Container Toolkit and device plugin manifests

### 4. Documentation Updated
- Completely rewrote `packages/k3d-gpu/README.md` with comprehensive setup instructions
- Added k9s usage documentation
- Added troubleshooting section for common issues
- Documented rootless podman limitations

---

## Environment Findings

### Rootless Podman: NOT Supported

After extensive testing, **rootless podman cannot run Kubernetes clusters** due to fundamental capability limitations:

1. **cgroup v2 delegation**: Cannot enable `cpuset` controller in cgroup subtree
   - K3s requires cpuset, cpu, and memory controllers
   - Error: `failed to find cpuset cgroup (v2)`

2. **iptables/netfilter**: Rootless containers lack CAP_NET_ADMIN
   - kube-proxy fails with "iptables is not available on this host"
   - Cannot set up Kubernetes networking

3. **sysctl access**: Cannot modify kernel parameters
   - kubelet fails with permission denied on /proc/sys settings

4. **/dev/kmsg**: Cannot access kernel message buffer
   - kubelet fails with /dev/kmsg permission denied

**Verdict**: Use **rootful podman** or **Docker** for Kubernetes clusters.

### Working Configuration: Root Podman

The following setup works reliably:

1. **cgroup delegation** on host (one-time sudo):
   ```bash
   sudo mkdir -p /etc/systemd/system/user@.service.d
   cat <<EOF | sudo tee /etc/systemd/system/user@.service.d/delegate.conf
   [Service]
   Delegate=cpu cpuset io memory pids
   EOF
   sudo systemctl daemon-reload
   ```

2. **Root podman socket** (one-time sudo):
   ```bash
   sudo systemctl start podman.socket
   ```

3. **DOCKER_HOST** environment variable:
   ```bash
   export DOCKER_HOST=unix:///run/podman/podman.sock
   ```

4. **k3d cluster creation** (no sudo needed after setup):
   ```bash
   k3d cluster create uds \
     --gpus all \
     --image ghcr.io/defenseunicorns/leapfrogai/k3d-gpu:83ac415c \
     --servers 1 \
     --agents 1 \
     --servers-memory 4g \
     --agents-memory 8g \
     --wait
   ```

### Toolbox Container Limitations

When running inside a Fedora Toolbox container:
- Toolbox uses rootless podman
- Toolbox containers have their own cgroup namespace
- k3d cannot mount volumes from toolbox to nested containers
- **Solution**: Run k3d on the host, not inside toolbox

---

## Updated Documentation

### Files Modified/Created

1. `packages/k3d-gpu/README.md` - Complete rewrite with:
   - Environment requirements section
   - Rootless vs rootful podman clarification
   - Step-by-step setup instructions
   - k9s usage documentation
   - Troubleshooting section

2. `scripts/docker-helper.sh` - Docker helper with rootless podman workaround

3. `packages/k3d-gpu/Dockerfile` - Custom k3s+CUDA image

---

## Quick Start

### For Docker Users

```bash
make clean-all
make build-k3d-gpu
make create-uds-gpu-cluster
kubectl get nodes
k9s
```

### For Podman Users

```bash
# One-time host setup (requires sudo)
sudo mkdir -p /etc/systemd/system/user@.service.d
cat <<EOF | sudo tee /etc/systemd/system/user@.service.d/delegate.conf
[Service]
Delegate=cpu cpuset io memory pids
EOF
sudo systemctl daemon-reload
sudo systemctl start podman.socket

# Set environment
export DOCKER_HOST=unix:///run/podman/podman.sock

# Create cluster (no sudo needed)
make clean-all
make build-k3d-gpu
make create-uds-gpu-cluster

# Access cluster
kubectl get nodes
k9s
```

### For Toolbox Users

Toolbox containers cannot run k3d directly. Either:
1. Exit toolbox and run commands on host
2. Use `flatpak-spawn --host` to run on host
3. Use a VM for full isolation

```bash
# Exit toolbox first
exit

# Then run on host
export DOCKER_HOST=unix:///run/podman/podman.sock
k3d cluster create uds --gpus all ...
```

---

## Next Steps

1. Log out and back in if you updated cgroup delegation
2. Verify podman socket is running: `sudo systemctl status podman.socket`
3. Create cluster following updated `packages/k3d-gpu/README.md`
4. Test GPU with `make test-uds-gpu-cluster`
5. Access cluster with `k9s` or `kubectl`

---

## References

- Updated: `packages/k3d-gpu/README.md`
- [Rootless Podman Limitations](https://github.com/containers/podman/blob/main/rootless.md)
- [k3d Documentation](https://k3d.io/)
- [k9s Documentation](https://k9scli.io/)
