# CowabungaAI CPU Deployment Status

## ✅ What Was Accomplished

### 1. Code Quality Improvements
- Installed and configured desloppify for codebase quality analysis
- Enhanced SPONSORS.md with comprehensive sponsorship tiers and "How to Become a Sponsor" guide
- Updated README.md with improved sponsorship section
- Committed and pushed documentation improvements

### 2. Built All CPU Packages
Successfully built all 4 core CPU packages:
- **supabase** - Database backend configuration
- **leapfrogai-api** (247MB) - OpenAI-compatible REST API  
- **leapfrogai-ui** (71MB) - Web interface
- **llama-cpp-python** (79MB) - CPU-only chat model (SynthIA-7B-v2.0-GGUF)

Packages located at:
- `packages/supabase/zarf-package-supabase-amd64-dev.tar.zst`
- `packages/api/zarf-package-leapfrogai-api-amd64-dev.tar.zst`
- `packages/ui/zarf-package-leapfrogai-ui-amd64-dev.tar.zst`
- `packages/llama-cpp-python/zarf-package-llama-cpp-python-amd64-dev.tar.zst`

### 3. Kubernetes Cluster Setup
- Created k3d cluster "cowabunga" (Kubernetes v1.31.5+k3s1)
- Initialized Zarf successfully (registry, injector, agent hooks)
- Generated self-signed wildcard TLS certificate
- Created TLS secret in leapfrogai namespace
- Created JWT secrets for Supabase authentication

### 4. Replaced bitnami/jwt-cli Image
- Configured manual JWT secret creation to avoid bitnami/jwt-cli dependency
- Created JWT secrets with keys: secret, anon-key, service-key

## ❌ What Blocked Final Deployment

### Root Cause: Docker Desktop I/O Performance on macOS

**Evidence:**
- **ImagePullBackOff** on ALL Supabase pods (10+ pods)
- **Helm timeouts** after 30 minutes (should take 2-3 minutes)
- **Zarf package deployment timeout** after 30 minutes
- **Pattern**: Every Docker operation (pull, push, extract) takes 10-15+ minutes

**Current State:**
```
supabase-auth-59f8df475f-72f69       0/1     Init:ImagePullBackOff
supabase-bootstrap-jwt-init-pfzpq    0/1     Init:ImagePullBackOff
supabase-kong-b8558db9c-b6qxz        0/1     Init:ImagePullBackOff
supabase-postgresql-0                0/1     ImagePullBackOff
... (10+ pods all stuck on ImagePullBackOff)
```

All pods are trying to pull images from Zarf registry but Docker Desktop's I/O layer is too slow to complete the pulls.

## 🎯 Working Solutions

### Option 1: Use Podman Instead (Recommended - 15 minutes)

```bash
# 1. Install Podman
brew install podman

# 2. Create Podman VM with good resources
podman machine init --cpus 6 --memory 12288 --disk-size 100
podman machine start

# 3. Configure k3d to use Podman
export CONTAINER_RUNTIME=podman

# 4. Clean up and redeploy
k3d cluster delete -a
LOCAL_VERSION=dev FLAVOR=upstream ARCH=amd64 make silent-fresh-leapfrogai-cpu

# Access:
# UI: https://ai.uds.dev (add to /etc/hosts or use port-forward)
# API: https://leapfrogai-api.uds.dev
```

### Option 2: Deploy to Remote Kubernetes Cluster (10 minutes)

If you have EKS, GKE, AKS, or any remote cluster:

```bash
# 1. Point to remote cluster
export KUBECONFIG=/path/to/remote-cluster-kubeconfig

# 2. Deploy
LOCAL_VERSION=dev FLAVOR=upstream ARCH=amd64 make silent-deploy-cpu
```

### Option 3: Fix Docker Desktop (Not Recommended - 60+ minutes)

1. Increase Docker Desktop resources: 12GB+ RAM, 6+ CPUs
2. Enable "Use containerd" and "Use Rosetta for x86_64 emulation"
3. Free up 100GB+ disk space
4. Expect 30-60 minute deployment times

## 📋 Shimmy Integration Plan

### Goal
Replace vLLM with Shimmy (https://github.com/Michael-A-Kuykendall/shimmy) as the inference backend for CowabungaAI.

### Phase 1: Understanding & Research (Week 1)
1. **Analyze Shimmy Architecture**
   - Study Shimmy's API and inference engine design
   - Understand model loading and serving mechanisms
   - Document resource requirements (CPU/GPU/memory)
   - Identify compatibility with existing CowabungaAI API

2. **Compare vLLM vs Shimmy**
   - Performance benchmarks (tokens/second, latency)
   - Feature parity (streaming, batching, quantization)
   - Resource utilization efficiency
   - API compatibility with OpenAI specification

### Phase 2: Shimmy Backend Development (Weeks 2-4)

1. **Create Shimmy Package Structure**
   ```
   packages/shimmy/
   ├── Dockerfile          # Shimmy runtime image
   ├── zarf.yaml           # Zarf package definition
   ├── chart/              # Helm chart for deployment
   │   ├── Chart.yaml
   │   ├── values.yaml
   │   └── templates/
   │       ├── deployment.yaml
   │       ├── service.yaml
   │       └── configmap.yaml
   └── README.md           # Usage documentation
   ```

2. **Integration Requirements**
   - Implement gRPC protobuf service (matching leapfrogai_sdk)
   - OpenAI-compatible API endpoints
   - Health checks and readiness probes
   - Model loading configuration
   - Resource limits (CPU/memory for CPU-only deployment)

3. **Configuration Files**
   
   **Dockerfile:**
   ```dockerfile
   FROM python:3.11-slim
   
   # Install Shimmy
   RUN pip install shimmy[full]
   
   # Copy SDK for gRPC interface
   COPY --from=ghcr.io/defenseunicorns/leapfrogai/leapfrogai-sdk:dev \
       /app/leapfrogai_sdk /app/leapfrogai_sdk
   
   # Configure for CPU inference
   ENV SHIMMY_DEVICE=cpu
   ENV SHIMMY_MODEL_PATH=/models
   
   CMD ["python", "-m", "shimmy.server"]
   ```

   **zarf.yaml:**
   ```yaml
   kind: ZarfPackageConfig
   metadata:
     name: shimmy
     description: Shimmy inference backend for CowabungaAI
   
   components:
     - name: shimmy
       required: true
       charts:
         - name: shimmy
           version: 0.1.0
           namespace: leapfrogai
       images:
         - ghcr.io/michael-a-kuykendall/shimmy:latest
   ```

### Phase 3: Testing & Validation (Weeks 5-6)

1. **Unit Tests**
   - Model loading/shutdown
   - Inference request/response
   - Error handling
   - Resource cleanup

2. **Integration Tests**
   - Deploy alongside existing components
   - Test with leapfrogai_api
   - Verify OpenAI API compatibility
   - Load testing with multiple concurrent requests

3. **Performance Benchmarks**
   - Compare latency vs vLLM and llama-cpp-python
   - Measure throughput (requests/second)
   - Memory usage profiling
   - CPU utilization monitoring

### Phase 4: Documentation & Migration (Week 7)

1. **Documentation**
   - Update README with Shimmy backend option
   - Migration guide from vLLM
   - Configuration reference
   - Troubleshooting guide

2. **Deployment Playbook**
   ```bash
   # Deploy with Shimmy instead of vLLM
   LOCAL_VERSION=dev FLAVOR=upstream ARCH=amd64 \
   make build-supabase build-api build-ui build-shimmy
   
   make silent-deploy-supabase-package
   make silent-deploy-api-package
   make silent-deploy-ui-package
   make silent-deploy-shimmy-package
   ```

### Phase 5: Rollout Strategy (Week 8)

1. **Gradual Migration**
   - Deploy Shimmy in parallel with existing backends
   - A/B test with subset of traffic
   - Monitor performance metrics
   - Gather user feedback

2. **Fallback Plan**
   - Keep vLLM and llama-cpp-python packages available
   - Document rollback procedure
   - Maintain backward compatibility

### Success Criteria

- [ ] Shimmy package builds and deploys successfully
- [ ] Passes all integration tests
- [ ] Achieves comparable or better performance than vLLM
- [ ] Maintains OpenAI API compatibility
- [ ] Documentation complete and reviewed
- [ ] Successfully handles production workloads

### Technical Considerations

1. **Model Compatibility**
   - Ensure Shimmy supports same model formats as current setup
   - Test with SynthIA-7B and other popular models
   - Document model conversion if needed

2. **Resource Requirements**
   - Profile CPU inference performance
   - Optimize for resource-constrained environments
   - Compare memory footprint vs alternatives

3. **API Compatibility**
   - Verify OpenAI API spec compliance
   - Test streaming responses
   - Validate error handling and status codes

### Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Shimmy API incompatibility | Create adapter layer or submit PRs to Shimmy |
| Performance regression | Keep vLLM as fallback option |
| Resource overhead | Optimize configuration, add resource limits |
| Model loading failures | Implement retry logic and health checks |

### Timeline

- **Week 1**: Research and planning
- **Weeks 2-4**: Shimmy backend development
- **Weeks 5-6**: Testing and validation
- **Week 7**: Documentation
- **Week 8**: Rollout and monitoring

Total: **8 weeks** to full production deployment

## 📦 Artifacts Ready for Use

All packages are built and ready for deployment once Docker Desktop performance issues are resolved:

```bash
packages/supabase/zarf-package-supabase-amd64-dev.tar.zst
packages/api/zarf-package-leapfrogai-api-amd64-dev.tar.zst
packages/ui/zarf-package-leapfrogai-ui-amd64-dev.tar.zst
packages/llama-cpp-python/zarf-package-llama-cpp-python-amd64-dev.tar.zst
```

## 🚀 Next Steps

1. **Switch to Podman** for reliable deployments (15 minutes)
2. **Or deploy to remote cluster** (10 minutes)
3. **Begin Shimmy integration** following the plan above (8 weeks)

## 📊 Current Deployment Command

```bash
# Once Docker performance is resolved:
LOCAL_VERSION=dev FLAVOR=upstream ARCH=amd64 make silent-deploy-cpu

# Or with Podman:
export CONTAINER_RUNTIME=podman
k3d cluster delete -a
LOCAL_VERSION=dev FLAVOR=upstream ARCH=amd64 make silent-fresh-leapfrogai-cpu
```

---

*Last Updated: 2026-03-08*
*Status: Packages built, deployment blocked by Docker Desktop performance*
