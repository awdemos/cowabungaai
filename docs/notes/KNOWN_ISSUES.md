# CowabungaAI Known Issues

This document tracks known issues encountered during deployment and development, along with their solutions and workarounds.

---

## Table of Contents

- [Docker Desktop Performance](#docker-desktop-performance)
- [UDS Certificate Expiration](#uds-certificate-expiration)
- [Bitnami Image Pull Failures](#bitnami-image-pull-failures)
- [UDS Package CRD Requirements](#uds-package-crd-requirements)
- [Zarf Template Variables](#zarf-template-variables)
- [Helm Namespace Ownership](#helm-namespace-ownership)
- [Image Import for k3d](#image-import-for-k3d)
- [Supabase JWT Configuration](#supabase-jwt-configuration)
- [Package Build Timeouts](#package-build-timeouts)

---

## Docker Desktop Performance

**Issue:** Severe I/O performance degradation on Docker Desktop for macOS causing deployment failures.

**Symptoms:**
- Image pulls taking 10-15+ minutes (should be seconds)
- Helm chart deployments timing out with "context deadline exceeded"
- Zarf initialization failing with registry seed timeouts
- Pod initialization taking 15+ minutes vs 1-2 minutes normally
- Docker Desktop crashes under load

**Root Cause:**
Docker Desktop on macOS has known I/O performance issues, particularly with:
- File system operations on macOS APFS to Linux VM translation
- Image layer extraction and decompression
- Container runtime operations during high-load scenarios

**Solutions:**

### Option 1: Use Podman (Recommended)
```bash
# Install Podman
brew install podman

# Create VM with adequate resources
podman machine init --cpus 6 --memory 12288 --disk-size 100
podman machine start

# Configure k3d to use Podman
export CONTAINER_RUNTIME=podman
```

### Option 2: Use Colima
```bash
# Install Colima
brew install colima

# Start with adequate resources
colima start --cpu 6 --memory 12 --disk 100
```

### Option 3: Optimize Docker Desktop
```bash
# Increase Docker Desktop resources in Settings > Resources:
# - Memory: 12GB+ recommended
# - CPUs: 6+ recommended
# - Disk: 100GB+ free space

# Enable performance features:
# - Use containerd: enabled
# - Use Rosetta for x86_64 emulation (Apple Silicon): enabled

# Restart Docker Desktop completely
osascript -e 'quit app "Docker"'
sleep 10
open -a Docker
```

**Status:** Ongoing issue with Docker Desktop on macOS. Alternative runtimes recommended.

---

## UDS Certificate Expiration

**Issue:** UDS bundles contain TLS certificates with expiration dates, causing deployment failures.

**Symptoms:**
```
x509: certificate has expired or is not yet valid: 
current time 2026-03-08T20:44:10Z is after 2026-02-04T14:51:49Z
```

**Root Cause:**
UDS bundles include Istio/Keycloak with embedded TLS certificates. The pre-built bundles in this repository (build date ~2025-02-04) have expired certificates.

**Solutions:**

### Option 1: Generate Self-Signed Certificates (Development)
```bash
# Generate wildcard certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /tmp/cowabunga.key \
  -out /tmp/cowabunga.crt \
  -subj "/CN=*.cowabunga.local/O=CowabungaAI" \
  -addext "subjectAltName=DNS:*.cowabunga.local,DNS:localhost"

# Create TLS secret
kubectl create secret tls cowabunga-tls \
  --cert=/tmp/cowabunga.crt \
  --key=/tmp/cowabunga.key \
  -n leapfrogai
```

### Option 2: Use Production Certificates
```bash
# For production, use your organization's wildcard certificate
kubectl create secret tls cowabunga-tls \
  --cert=path/to/wildcard.crt \
  --key=path/to/wildcard.key \
  -n istio-system
```

### Option 3: Deploy Without UDS
Deploy directly with Helm/kubectl, bypassing UDS entirely (see deployment guide).

**Certificate Requirements:**
- **Type:** Wildcard TLS certificate (e.g., `*.yourdomain.com`)
- **Secret Type:** `kubernetes.io/tls`
- **Required Keys:** `tls.crt` (certificate), `tls.key` (private key)
- **Namespace:** 
  - With UDS/Istio: `istio-system`
  - Without UDS: Same as application (e.g., `leapfrogai`)

**Status:** Requires certificate renewal for UDS deployments.

---

## Bitnami Image Pull Failures

**Issue:** Supabase bootstrap fails to pull `bitnami/jwt-cli` image during initialization.

**Symptoms:**
```
Init:ImagePullBackOff - trying and failing to pull image docker.io/bitnami/jwt-cli
```

**Root Cause:**
Bitnami images have rate limits and may require authentication. Docker Hub rate limiting combined with Docker Desktop performance issues causes failures.

**Solution:**
Pre-create JWT secrets to skip JWT auto-generation that requires the bitnami image:

```bash
# Generate JWT secret
JWT_SECRET=$(openssl rand -hex 32)

# Create secret with correct key names
kubectl create secret generic supabase-bootstrap-jwt \
  --from-literal=secret="${JWT_SECRET}" \
  --from-literal=anon-key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  --from-literal=service-key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -n leapfrogai
```

**Important Notes:**
- Secret must be named exactly `supabase-bootstrap-jwt`
- Must be in the `leapfrogai` namespace (not `supabase`)
- Required keys: `secret`, `anon-key`, `service-key`
- Must be created BEFORE deploying Supabase

**Status:** Workaround documented. Consider replacing with free alternative image.

---

## UDS Package CRD Requirements

**Issue:** Helm charts attempt to create UDS Package CRDs which don't exist in plain k3d clusters.

**Symptoms:**
```
no matches for kind "Package" in version "uds.dev/v1alpha1"
ensure CRDs are installed first
```

**Root Cause:**
Charts are designed for UDS-enabled clusters with custom Package CRDs. These CRDs manage application lifecycle in UDS but don't exist in vanilla Kubernetes.

**Solutions:**

### Option 1: Install UDS Package CRD (Minimal)
```bash
cat <<EOF | kubectl apply -f -
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: packages.uds.dev
spec:
  group: uds.dev
  versions:
    - name: v1alpha1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              x-kubernetes-preserve-unknown-fields: true
            status:
              type: object
              x-kubernetes-preserve-unknown-fields: true
  scope: Namespaced
  names:
    plural: packages
    singular: package
    kind: Package
EOF
```

### Option 2: Use UDS-Enabled Cluster
```bash
# Create cluster with UDS infrastructure
make create-uds-cpu-cluster
```

### Option 3: Deploy Without UDS (Recommended for Simple Deployments)
Deploy directly with kubectl or Helm with `--skip-crds` flag:
```bash
helm install release-name ./chart.tgz --skip-crds -n leapfrogai
```

**Status:** UDS adds complexity for simple deployments. Direct deployment recommended for non-UDS environments.

---

## Zarf Template Variables

**Issue:** Helm charts contain unresolved Zarf template variables causing deployment failures.

**Symptoms:**
```
Error: INSTALLATION FAILED: unable to build kubernetes objects from release manifest:
error validating "": error validating data: unknown object type "nil" in Package.spec.networking.serviceMesh
```

**Root Cause:**
Zarf packages embed Helm charts with template variables like `###ZARF_VAR_...###` that should be resolved during Zarf package deployment. These aren't resolved when deploying charts directly with Helm.

**Solutions:**

### Option 1: Use Zarf for Deployment
```bash
# Deploy via Zarf package (resolves variables correctly)
zarf package deploy package.tar.zst --confirm
```

### Option 2: Extract and Clean Charts
Extract charts from Zarf packages and remove/replace Zarf-specific templates:
```bash
# Extract Zarf package
tar -xzf package.tar.zst
tar -xf components/component.tar

# Find and replace Zarf variables in values files
find . -name "values/*" -exec sed -i 's/###ZARF_VAR_.*###//g' {} \;
```

### Option 3: Create Custom Deployment Manifests
Bypass Helm charts entirely and create simple Kubernetes manifests:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: leapfrogai-api
  namespace: leapfrogai
spec:
  replicas: 1
  selector:
    matchLabels:
      app: leapfrogai-api
  template:
    spec:
      containers:
      - name: api
        image: ghcr.io/defenseunicorns/leapfrogai/leapfrogai-api:dev
        ports:
        - containerPort: 8080
```

**Status:** Zarf packages require Zarf for proper deployment. Direct Helm deployment requires chart modification.

---

## Helm Namespace Ownership

**Issue:** Helm refuses to install charts into namespaces it doesn't manage.

**Symptoms:**
```
Error: INSTALLATION FAILED: namespaces "leapfrogai" is forbidden: 
user "system:serviceaccount:kube-system:generic-garbage-collector" 
cannot patch resource "namespaces" in API group "" in the namespace "leapfrogai"
```

**Root Cause:**
Helm 3 requires namespaces to have proper labels and annotations indicating Helm management. Kubernetes prevents modification of existing resources without proper ownership.

**Solutions:**

### Option 1: Label Namespace for Helm
```bash
# Create namespace
kubectl create namespace leapfrogai

# Add Helm management labels/annotations
kubectl label namespace leapfrogai app.kubernetes.io/managed-by=Helm
kubectl annotate namespace leapfrogai \
  meta.helm.sh/release-name=release-name \
  meta.helm.sh/release-namespace=leapfrogai
```

### Option 2: Let Helm Create Namespace
```bash
# Don't create namespace beforehand; let Helm create it
helm install release-name chart.tgz --create-namespace -n leapfrogai
```

### Option 3: Force Overwrite
```bash
# Delete and recreate namespace (WARNING: destroys all resources in namespace)
kubectl delete namespace leapfrogai
helm install release-name chart.tgz --create-namespace -n leapfrogai
```

**Status:** Standard Helm 3 behavior. Use `--create-namespace` flag for simplicity.

---

## Image Import for k3d

**Issue:** Docker images built locally aren't automatically available to k3d cluster pods.

**Symptoms:**
```
ImagePullBackOff: trying and failing to pull image ghcr.io/.../image:dev
```

**Root Cause:**
k3d creates a separate container runtime. Images in your local Docker daemon aren't automatically accessible to the k3d cluster nodes.

**Solutions:**

### Option 1: Import Images into k3d
```bash
# Import specific images
k3d image import \
  ghcr.io/org/image1:tag \
  ghcr.io/org/image2:tag \
  -c cluster-name
```

### Option 2: Use Local Registry
```bash
# Create k3d cluster with local registry
k3d cluster create mycluster --registry-create myregistry:5000

# Tag and push images to local registry
docker tag myimage:dev localhost:5000/myimage:dev
docker push localhost:5000/myimage:dev

# Use local registry image in deployments
image: localhost:5000/myimage:dev
```

### Option 3: Build with k3d Registry
```bash
# Set Docker context to k3d's registry
export DOCKER_HOST=tcp://localhost:5000

# Build images directly into k3d
docker build -t localhost:5000/myimage:dev .
```

**Best Practice:**
After importing images, delete pods to force restart with imported images:
```bash
kubectl delete pods --all -n leapfrogai
```

**Status:** Expected k3d behavior. Import or registry required.

---

## Supabase JWT Configuration

**Issue:** Supabase deployment fails due to missing or incorrectly configured JWT secrets.

**Symptoms:**
```
secret "supabase-bootstrap-jwt" not found
Job failed: secret "supabase-bootstrap-jwt" not found
```

**Root Cause:**
Supabase requires JWT secrets for authentication token generation. The bootstrap process expects specific secret keys in a specific namespace.

**Solution:**

### Required Secret Configuration
```bash
# Generate JWT secret
JWT_SECRET=$(openssl rand -hex 32)

# Create secret with EXACT key names
kubectl create secret generic supabase-bootstrap-jwt \
  --from-literal=secret="${JWT_SECRET}" \
  --from-literal=anon-key="$(echo -n '{"header":{"alg":"HS256","typ":"JWT"},"payload":{"iss":"supabase","role":"anon"}}' | base64)" \
  --from-literal=service-key="$(echo -n '{"header":{"alg":"HS256","typ":"JWT"},"payload":{"iss":"supabase","role":"service_role"}}' | base64)" \
  -n leapfrogai
```

**Critical Requirements:**
1. **Secret Name:** Must be exactly `supabase-bootstrap-jwt`
2. **Namespace:** Must be in `leapfrogai` (NOT `supabase`)
3. **Required Keys:**
   - `secret` - JWT signing secret (32 bytes hex)
   - `anon-key` - Anonymous user JWT token
   - `service-key` - Service role JWT token
4. **Timing:** Must be created BEFORE deploying Supabase

**Verification:**
```bash
# Check secret exists
kubectl get secret supabase-bootstrap-jwt -n leapfrogai

# Verify keys
kubectl describe secret supabase-bootstrap-jwt -n leapfrogai
```

**Status:** Documented configuration. No code fix needed.

---

## Package Build Timeouts

**Issue:** Building text-embeddings and whisper packages times out due to Docker performance.

**Symptoms:**
```
Build failed after 10+ minutes
Error: context deadline exceeded
```

**Affected Packages:**
- `text-embeddings` - Vector embeddings model
- `whisper` - Audio transcription model

**Root Cause:**
These packages require:
- Large base images (PyTorch, ML frameworks)
- Model weight downloads (huggingface_hub)
- Complex dependency installation

Docker Desktop's I/O performance makes layer extraction and package installation extremely slow.

**Solutions:**

### Option 1: Use Pre-Built Images (Recommended)
```bash
# Pull pre-built images from registry
docker pull ghcr.io/defenseunicorns/leapfrogai/text-embeddings:latest
docker pull ghcr.io/defenseunicorns/leapfrogai/whisper:latest
```

### Option 2: Build with Faster Runtime
```bash
# Use Podman for faster builds
brew install podman
podman machine init --cpus 8 --memory 16384
podman machine start

# Build with Podman
CONTAINER_RUNTIME=podman make build-text-embeddings
```

### Option 3: Build Individually with Extended Timeout
```bash
# Build with longer timeout
LOCAL_VERSION=dev FLAVOR=upstream ARCH=amd64 \
  make build-text-embeddings DOCKER_FLAGS="--timeout 3600"
```

### Option 4: Deploy Minimal Bundle (Skip These Packages)
Deploy core functionality without RAG/transcription:
```bash
# Build and deploy only essential packages
make build-supabase build-api build-ui build-llama-cpp-python
make silent-deploy-cpu
```

**Impact of Skipping:**
- ❌ No RAG (Retrieval Augmented Generation)
- ❌ No document Q&A
- ❌ No audio transcription
- ❌ No translation
- ✅ Chat still works with CPU LLM

**Status:** Docker Desktop performance limitation. Alternative runtimes recommended.

---

## Summary

**Most Common Issues:**
1. Docker Desktop performance on macOS → Use Podman/Colima
2. Missing JWT secrets → Create before deployment
3. Image not in cluster → Import with k3d
4. UDS complexity → Deploy directly without UDS

**Recommended Deployment Path:**
```bash
# 1. Use Podman instead of Docker Desktop
brew install podman
podman machine init --cpus 6 --memory 12288 --disk-size 100
podman machine start

# 2. Create cluster
k3d cluster create cowabunga --api-port 6550

# 3. Build packages
LOCAL_VERSION=dev FLAVOR=upstream ARCH=amd64 make build-cpu

# 4. Import images
k3d image import ghcr.io/defenseunicorns/leapfrogai/*:dev -c cowabunga

# 5. Create secrets
kubectl create namespace leapfrogai
# ... create JWT secrets, TLS secrets ...

# 6. Deploy
make silent-deploy-cpu
```

**Getting Help:**
- Check logs: `.logs/*.log`
- Check pod status: `kubectl get pods -A`
- Check events: `kubectl get events --sort-by='.lastTimestamp'`
- Describe failed resources: `kubectl describe pod/<pod-name>`

---

*Last Updated: 2026-03-08*
*Version: 1.0*
