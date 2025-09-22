# CowabungaAI Technical Handbook

*Comprehensive technical guide for self-hosted AI platform deployment and development*

## Overview

CowabungaAI is an open-source platform designed for deploying generative AI capabilities in resource-constrained and air-gapped environments. This handbook provides comprehensive technical guidance for deployment, development, and operation of the platform.

### Project Heritage

CowabungaAI is a fork of [Unicorn Defense's LeapfrogAI](https://github.com/defenseunicorns/leapfrogai) project. We extend our sincere gratitude to the original LeapfrogAI development team and contributors for their groundbreaking work in creating this comprehensive self-hosted AI platform.

#### Our Appreciation

We deeply appreciate the foundational work done by the LeapfrogAI team, including:

- **Architecture Design**: The microservices architecture that enables flexible deployment
- **OpenAI Compatibility**: The comprehensive API compatibility layer
- **Multi-Model Support**: The extensive backend implementations for various AI models
- **Documentation**: The thorough technical documentation and guides
- **Community Building**: The open-source community engagement and support

#### Fork Philosophy

This fork maintains the core philosophy of the original project while adapting it for specific use cases and requirements. We remain committed to:
- Open-source principles and community collaboration
- Maintaining compatibility with the OpenAI ecosystem
- Supporting air-gapped and resource-constrained deployments
- Continuous improvement and innovation in self-hosted AI

### Licensing

CowabungaAI operates under a **dual-license model** to respect upstream contributions while enabling commercial use:

#### License Structure

- **Upstream Code**: Original LeapfrogAI contributions remain under **Apache License 2.0** (see `LICENSE`)
- **New Contributions**: CowabungaAI-specific contributions are under **Business Source License 1.1** (see `LICENSE.bsl`)
- **Commercial Use**: Requires commercial license for production deployments involving BSL-licensed components

#### License Terms

**Apache License 2.0 (Upstream Code):**
- Free for all uses, including commercial
- Permissive open-source license
- Requires attribution and license preservation

**Business Source License 1.1 (New Contributions):**
- **Non-Commercial Use**: Free for personal, academic, research, evaluation, and testing purposes
- **Commercial Use**: Requires a commercial license for production deployments and commercial gain
- **Change License**: BSL components will convert to Apache License 2.0 on January 1, 2029

#### Commercial Licensing

For commercial production use involving BSL-licensed components, organizations must obtain a commercial license. This includes:

- **Production Deployments**: Any use for commercial gain or competitive advantage
- **Commercial Products**: Integration into commercial products or services
- **Enterprise Scale**: Large-scale deployments beyond evaluation/testing

#### How to Obtain a Commercial License

To inquire about a commercial license, please create a GitHub issue at:

https://github.com/defenseunicorns/leapfrogai/issues/new/choose

**Please include the following information in your inquiry:**

- **Organization Name**: Your company or organization name
- **Contact Information**: Email address and phone number for follow-up
- **Intended Use Case**: Description of how you plan to use CowabungaAI
- **Scale of Deployment**: Expected usage scale and deployment environment
- **Timeline**: When you plan to deploy
- **Additional Details**: Any other relevant information about your requirements

#### License Benefits

Commercial license holders receive:

- **Production Use Rights**: Legal permission for commercial deployment
- **Support**: Priority support and maintenance
- **Customization**: Options for custom features and modifications
- **Consulting**: Professional services for deployment and integration
- **Training**: Technical training and documentation support

#### License Compliance

We take license compliance seriously and work with organizations to ensure proper licensing for their use cases. Our team will review your inquiry and provide appropriate licensing options based on your specific needs.

### Platform Architecture

The platform follows a microservices architecture with the following key components:

- **API Service**: FastAPI-based REST API with OpenAI compatibility
- **Model Backends**: Various AI model implementations (LLaMA, vLLM, Whisper, etc.)
- **Vector Database**: For embeddings and similarity search
- **User Interface**: Web-based interaction platform
- **Authentication**: User management and access control

### Key Features

- **Self-Hosted Deployment**: Complete control over data and models
- **Air-Gap Support**: Operates without external internet connectivity
- **OpenAI Compatibility**: Seamless integration with existing tools
- **Multi-Model Support**: Various AI models for different use cases
- **Scalable Architecture**: From edge devices to cloud deployments

## System Requirements

### Minimum Specifications

- **Storage**: 256 GB SSD (1 TB recommended)
- **Memory**: 32 GB RAM (128 GB recommended)
- **Processing**: 8 CPU cores @ 3.0 GHz (32 cores recommended)
- **Graphics**: 1 NVIDIA GPU with 12 GB VRAM (2x RTX 4090 recommended)
- **Network**: Local network connectivity

### Supported Operating Systems

- Ubuntu 20.04/22.04 LTS
- Pop!_OS 22.04
- macOS Sonoma 14.x

### GPU Support

The platform supports both CPU-only and GPU-accelerated deployments:

- **CPU Deployment**: Suitable for development and small-scale use
- **GPU Deployment**: Required for production workloads and larger models

## Deployment Guide

### Prerequisites

1. **Python Environment**: Python 3.11.9 with virtual environment
2. **Container Runtime**: Docker with NVIDIA container toolkit (for GPU)
3. **Kubernetes**: UDS (Unicorn Delivery Service) cluster
4. **Development Tools**: Git, Make, and build essentials

### Environment Setup

```bash
# Install Python version management
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

# Install Python 3.11.9
pyenv install 3.11.9
pyenv virtualenv 3.11.9 leapfrogai-dev
pyenv activate leapfrogai-dev

# Install system dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install build-essential zlib1g-dev libffi-dev \
  libssl-dev libbz2-dev libreadline-dev libsqlite3-dev \
  liblzma-dev libncurses-dev curl
```

### UDS CLI Configuration

```bash
# Add useful aliases to shell configuration
echo 'alias k="uds zarf tools kubectl"' >> ~/.bashrc
echo 'alias kubectl="uds zarf tools kubectl"' >> ~/.bashrc
echo 'alias zarf="uds zarf"' >> ~/.bashrc
echo 'alias k9s="uds zarf tools monitor"' >> ~/.bashrc

# Create kubectl binary wrapper
sudo touch /usr/local/bin/kubectl
sudo echo '#!/bin/bash' > /usr/local/bin/kubectl
sudo echo 'uds zarf tools kubectl "$@"' >> /usr/local/bin/kubectl
sudo chmod +x /usr/local/bin/kubectl
```

### Cluster Deployment

#### CPU Cluster Setup

```bash
# Create UDS cluster for CPU deployment
make create-uds-cpu-cluster

# Build and deploy CPU components
LOCAL_VERSION=dev FLAVOR=upstream ARCH=amd64 make build-cpu
cd bundles/dev/cpu
uds create . --confirm
uds deploy <bundle-name> --confirm
```

#### GPU Cluster Setup

```bash
# Verify GPU support
nvidia-smi
nvidia-ctk --version
docker info | grep "nvidia"

# Create UDS cluster for GPU deployment
make create-uds-gpu-cluster

# Build and deploy GPU components
LOCAL_VERSION=dev FLAVOR=upstream ARCH=amd64 make build-gpu
cd bundles/dev/gpu
uds create . --confirm
uds deploy <bundle-name> --confirm
```

### Platform Access

After successful deployment, access the platform at:

- **Web Interface**: https://ai.uds.dev
- **API Documentation**: https://leapfrogai-api.uds.dev/docs
- **API Endpoints**: https://leapfrogai-api.uds.dev/v1

## Component Architecture

### API Service

The API service provides OpenAI-compatible endpoints with the following features:

- **RESTful Interface**: Standard HTTP methods and status codes
- **Authentication**: JWT-based token authentication
- **Rate Limiting**: Configurable request limits
- **Logging**: Structured logging for debugging and monitoring

#### Key Endpoints

```
POST   /v1/chat/completions    - Chat completions
POST   /v1/completions         - Text completions
POST   /v1/embeddings          - Text embeddings
GET    /v1/models              - Available models
POST   /v1/audio/transcriptions - Audio transcription
POST   /v1/audio/translations  - Audio translation
```

### Model Backends

#### LLaMA CPP Backend

- **Purpose**: CPU-based LLM inference
- **Models**: Supports various LLaMA model variants
- **Performance**: Optimized for CPU execution
- **Memory**: Efficient memory usage for constrained environments

#### vLLM Backend

- **Purpose**: GPU-accelerated LLM inference
- **Performance**: High-throughput inference with PagedAttention
- **Models**: Supports large language models
- **Scalability**: Multi-GPU support for large models

#### Whisper Backend

- **Purpose**: Audio transcription and translation
- **Features**: Multi-language support
- **Performance**: Real-time processing capabilities
- **Formats**: Various audio format support

#### Text Embeddings Backend

- **Purpose**: Text vectorization for semantic search
- **Models**: Instructor-XL and similar embedding models
- **Performance**: Batch processing capabilities
- **Integration**: Seamless integration with vector databases

### Vector Database

The platform includes a vector database for:

- **Storage**: Efficient vector storage and retrieval
- **Search**: Similarity search capabilities
- **Integration**: Built-in RAG (Retrieval-Augmented Generation) support
- **Scalability**: Horizontal scaling for large datasets

## Development Guide

### Local Development Setup

#### Environment Preparation

```bash
# Create development environment
pyenv virtualenv 3.11.9 leapfrogai-dev
pyenv activate leapfrogai-dev

# Install project dependencies
python -m pip install ".[dev]"
python -m pip install ".[dev-whisper]"
python -m pip install ".[dev-vllm]"
```

#### Component Development

Individual components can be developed and tested independently:

```bash
# Development workflow for a single component
cd packages/<component-name>

# Build local development version
LOCAL_VERSION=dev FLAVOR=upstream REGISTRY_PORT=5000 ARCH=amd64 make build-<component>

# Deploy to existing cluster
uds zarf package remove leapfrogai-<component> --confirm
uds zarf tools registry prune --confirm
LOCAL_VERSION=dev FLAVOR=upstream REGISTRY_PORT=5000 ARCH=amd64 make deploy-<component>
```

### Backend Development

#### Local Backend Testing

```bash
# Test backend locally
cd packages/<backend-name>
python -m pip install -e .
python -m <backend-name>.main

# Test with local API
cd src/leapfrogai_api
cp config.example.yaml config.yaml
# Update config.yaml with local backend addresses
python -m leapfrogai_api.main
```

#### Cluster Backend Integration

```bash
# Port-forward cluster backends for local testing
#!/bin/bash

# Set environment variables
export SUPABASE_URL="https://supabase-kong.uds.dev"
export SUPABASE_ANON_KEY=$(kubectl get secret supabase-bootstrap-jwt -n leapfrogai -o jsonpath='{.data.anon-key}' | base64 --decode)

# Port-forward backends
uds zarf tools kubectl port-forward svc/text-embeddings-model -n leapfrogai 50052:50051 &
uds zarf tools kubectl port-forward svc/llama-cpp-python-model -n leapfrogai 50051:50051 &
```

### API Development

#### Local API Setup

```bash
# Configure API for local development
cd src/leapfrogai_api
cp config.example.yaml config.yaml

# Edit config.yaml for local backend addresses
# Example configuration:
backends:
  text-embeddings:
    url: "localhost:50052"
  llama-cpp-python:
    url: "localhost:50051"

# Start API server
python -m leapfrogai_api.main
```

#### API Testing

```bash
# Test API endpoints
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "model": "llama-cpp-python",
    "messages": [{"role": "user", "content": "Hello, world!"}]
  }'
```

### Bundle Development

#### Custom Bundle Creation

```bash
# Build all components
LOCAL_VERSION=dev FLAVOR=upstream ARCH=amd64 make build-all

# Create custom bundle
cd bundles/custom
vim uds-config.yaml  # Customize configuration
vim uds-bundle.yaml  # Customize bundle composition

# Create and deploy bundle
uds create . --confirm
uds deploy <bundle-name> --confirm
```

#### Bundle Overrides

```yaml
# uds-bundle.yaml with overrides
- name: leapfrogai-api
  repository: ghcr.io/defenseunicorns/packages/leapfrogai/leapfrogai-api
  ref: 0.13.1
  overrides:
    leapfrogai-api:
      leapfrogai:
        variables:
          name: API_REPLICAS
          description: "Number of API replicas"
          path: api.replicas
```

```yaml
# uds-config.yaml with variable overrides
variables:
  leapfrogai-api:
    api_replicas: 2
```

## Configuration Management

### Environment Variables

#### API Configuration

```bash
# API server configuration
LEAPFROGAI_API_HOST=0.0.0.0
LEAPFROGAI_API_PORT=8000
LEAPFROGAI_API_DEBUG=false
LEAPFROGAI_API_LOG_LEVEL=INFO

# Database configuration
SUPABASE_URL=https://supabase-kong.uds.dev
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key

# Security configuration
LEAPFROGAI_API_SECRET_KEY=your-secret-key
LEAPFROGAI_API_ALGORITHM=HS256
LEAPFROGAI_API_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### Backend Configuration

```bash
# Model backend configuration
MODEL_BACKEND_HOST=0.0.0.0
MODEL_BACKEND_PORT=50051
MODEL_BACKEND_MODEL_PATH=/models/your-model.bin
MODEL_BACKEND_CONTEXT_SIZE=2048
MODEL_BACKEND_MAX_TOKENS=512

# GPU configuration (if applicable)
CUDA_VISIBLE_DEVICES=0
TORCH_CUDA_ARCH_LIST=8.6  # Adjust for your GPU architecture
```

### Configuration Files

#### API Configuration (config.yaml)

```yaml
# API server configuration
server:
  host: "0.0.0.0"
  port: 8000
  debug: false
  log_level: "INFO"

# Backend service configuration
backends:
  text-embeddings:
    url: "text-embeddings-model:50051"
    timeout: 30
  llama-cpp-python:
    url: "llama-cpp-python-model:50051"
    timeout: 60
  vllm:
    url: "vllm-model:50051"
    timeout: 60
  whisper:
    url: "whisper-model:50051"
    timeout: 120

# Database configuration
database:
  url: "https://supabase-kong.uds.dev"
  anon_key: "${SUPABASE_ANON_KEY}"
  service_key: "${SUPABASE_SERVICE_KEY}"

# Security configuration
security:
  secret_key: "${LEAPFROGAI_API_SECRET_KEY}"
  algorithm: "HS256"
  access_token_expire_minutes: 30

# Rate limiting
rate_limit:
  requests_per_minute: 60
  burst_size: 10
```

## Monitoring and Observability

### Logging

#### Structured Logging

The platform uses structured logging with the following format:

```json
{
  "timestamp": "2024-01-01T12:00:00Z",
  "level": "INFO",
  "service": "leapfrogai-api",
  "message": "Request processed",
  "request_id": "req_123456",
  "method": "POST",
  "path": "/v1/chat/completions",
  "status_code": 200,
  "duration_ms": 150,
  "user_id": "user_789012"
}
```

#### Log Levels

- **DEBUG**: Detailed diagnostic information
- **INFO**: General operational information
- **WARN**: Warning conditions that might need attention
- **ERROR**: Error conditions that should be investigated

### Metrics Collection

#### API Metrics

- **Request Count**: Number of requests per endpoint
- **Response Time**: Request processing duration
- **Error Rate**: Percentage of failed requests
- **Active Connections**: Number of concurrent connections

#### Backend Metrics

- **Model Loading Time**: Time to load models into memory
- **Inference Time**: Time spent on model inference
- **Memory Usage**: RAM and VRAM consumption
- **GPU Utilization**: GPU usage statistics

### Health Checks

#### API Health Check

```bash
# Check API health
curl http://localhost:8000/health

# Expected response
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00Z",
  "version": "0.13.1",
  "components": {
    "database": "healthy",
    "backends": {
      "text-embeddings": "healthy",
      "llama-cpp-python": "healthy"
    }
  }
}
```

#### Backend Health Check

```bash
# Check backend health
curl http://localhost:50051/health

# Expected response
{
  "status": "healthy",
  "model": "llama-2-7b-chat",
  "loaded": true,
  "memory_usage_mb": 4500,
  "gpu_usage_percent": 75
}
```

## Security Considerations

### Data Protection

#### Encryption

- **Data at Rest**: Encrypted storage for sensitive data
- **Data in Transit**: TLS 1.3 for all network communications
- **Model Weights**: Encrypted model file storage

#### Access Control

- **Authentication**: JWT-based authentication
- **Authorization**: Role-based access control
- **Rate Limiting**: Prevent abuse and ensure fair usage
- **Audit Logging**: Comprehensive audit trail

### Network Security

#### Air-Gap Deployment

For air-gapped environments:

1. **Package Management**: Local package repositories
2. **Container Images**: Pre-loaded container registry
3. **Model Files**: Local model storage
4. **Dependencies**: All dependencies bundled locally

#### Network Policies

```yaml
# Example network policy for API service
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: leapfrogai-api-network-policy
  namespace: leapfrogai
spec:
  podSelector:
    matchLabels:
      app: leapfrogai-api
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: istio-system
    - namespaceSelector:
        matchLabels:
          name: leapfrogai
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: leapfrogai
```

### Container Security

#### Image Hardening

- **Base Images**: Use minimal, hardened base images
- **Security Scanning**: Regular vulnerability scanning
- **Non-root Users**: Run containers as non-root users
- **Read-only Filesystems**: Where possible, use read-only filesystems

#### Runtime Security

```yaml
# Example security context for API deployment
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  runAsGroup: 3000
  fsGroup: 2000
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
  capabilities:
    drop:
    - ALL
```

## Troubleshooting

### Common Issues

#### GPU-related Problems

**Symptoms**: GPU not detected, CUDA errors, performance issues

**Solutions**:

```bash
# Check GPU status
nvidia-smi

# Verify CUDA toolkit
nvcc --version

# Check NVIDIA container toolkit
nvidia-ctk --version

# Test CUDA functionality
docker run --gpus all nvidia/cuda:11.8.0-base nvidia-smi

# Check GPU resource usage
uds zarf tools kubectl get pods \
  --all-namespaces \
  --output=yaml \
  | uds zarf tools yq eval '.items[] | select(.spec.containers[].resources.requests["nvidia.com/gpu"])'
```

#### Memory Issues

**Symptoms**: Out-of-memory errors, pod crashes, slow performance

**Solutions**:

```bash
# Check memory usage
uds zarf tools kubectl top pods

# Monitor node resources
uds zarf tools kubectl describe node

# Check pod events
uds zarf tools kubectl describe pod <pod-name> -n leapfrogai

# View container logs
uds zarf tools kubectl logs <pod-name> -n leapfrogai --all-containers=true --follow
```

#### Network Issues

**Symptoms**: Connection timeouts, service unreachable, DNS resolution failures

**Solutions**:

```bash
# Check service connectivity
uds zarf tools kubectl get svc -n leapfrogai

# Test DNS resolution
uds zarf tools kubectl exec -it <pod-name> -n leapfrogai -- nslookup leapfrogai-api

# Check network policies
uds zarf tools kubectl get networkpolicy -n leapfrogai

# Verify Istio configuration
uds zarf tools kubectl get virtualservice -n leapfrogai
```

### Debugging Tools

#### k9s for Cluster Management

```bash
# Launch k9s for interactive cluster management
uds zarf tools monitor

# Common k9s commands:
# / : Filter resources
# s : View pods
# d : View deployments
# :logs : View logs
# :describe : Describe resource
```

#### Port Forwarding

```bash
# Forward API service locally
uds zarf tools kubectl port-forward svc/leapfrogai-api 8000:8000 -n leapfrogai

# Forward backend services
uds zarf tools kubectl port-forward svc/llama-cpp-python-model 50051:50051 -n leapfrogai
uds zarf tools kubectl port-forward svc/text-embeddings-model 50052:50051 -n leapfrogai
```

### Performance Optimization

#### Model Optimization

```bash
# Quantize models for reduced memory usage
python -m llama_cpp.server --model /models/llama-2-7b-chat.Q4_K_M.gguf \
  --n_ctx 2048 --n_batch 512 --n-gpu-layers 35

# Optimize vLLM configuration
python -m vllm.entrypoints.openai.api_server \
  --model /models/llama-2-7b-chat \
  --tensor-parallel-size 1 \
  --gpu-memory-utilization 0.9 \
  --max-num-batched-tokens 8192
```

#### Resource Allocation

```yaml
# Example resource requests and limits
resources:
  requests:
    cpu: "2"
    memory: "4Gi"
    nvidia.com/gpu: "1"
  limits:
    cpu: "4"
    memory: "8Gi"
    nvidia.com/gpu: "1"
```

## Best Practices

### Development Practices

#### Code Quality

- **Testing**: Comprehensive unit, integration, and contract tests
- **Code Review**: All changes require review
- **Documentation**: Maintain up-to-date documentation
- **Error Handling**: Implement proper error handling and logging

#### Version Control

```bash
# Feature branch workflow
git checkout -b feature/your-feature-name
# Make changes
git commit -m "feat: add your feature"
git push origin feature/your-feature-name
# Create pull request for review
```

### Deployment Practices

#### Environment Management

- **Development**: Local development environment
- **Testing**: Dedicated testing cluster
- **Staging**: Pre-production environment
- **Production**: Production deployment

#### Rollback Strategy

```bash
# Quick rollback to previous version
uds zarf package remove leapfrogai-api --confirm
uds zarf package deploy zarf-package-leapfrogai-api-previous-version.tar.zst --confirm
```

### Monitoring Practices

#### Alerting

- **Resource Usage**: Monitor CPU, memory, and GPU utilization
- **Error Rates**: Alert on increased error rates
- **Response Times**: Monitor API response times
- **Availability**: Ensure service availability

#### Incident Response

1. **Detection**: Automated monitoring and alerting
2. **Assessment**: Evaluate impact and scope
3. **Mitigation**: Implement temporary fixes
4. **Resolution**: Address root cause
5. **Prevention**: Implement preventive measures

## API Reference

### Authentication

#### API Key Authentication

```bash
# Set API key
export LEAPFROGAI_API_KEY="your-api-key-here"

# Use in requests
curl -H "Authorization: Bearer $LEAPFROGAI_API_KEY" \
  https://leapfrogai-api.uds.dev/v1/models
```

### Chat Completions

#### Request Format

```json
{
  "model": "llama-cpp-python",
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful assistant."
    },
    {
      "role": "user",
      "content": "Hello, how are you?"
    }
  ],
  "max_tokens": 512,
  "temperature": 0.7,
  "stream": false
}
```

#### Response Format

```json
{
  "id": "chatcmpl-1234567890",
  "object": "chat.completion",
  "created": 1640995200,
  "model": "llama-cpp-python",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "I'm doing well, thank you for asking!"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 25,
    "completion_tokens": 12,
    "total_tokens": 37
  }
}
```

### Text Embeddings

#### Request Format

```json
{
  "model": "text-embeddings",
  "input": "Hello, world!",
  "encoding_format": "float"
}
```

#### Response Format

```json
{
  "data": [
    {
      "object": "embedding",
      "embedding": [0.1, 0.2, 0.3, ...],
      "index": 0
    }
  ],
  "model": "text-embeddings",
  "usage": {
    "prompt_tokens": 3,
    "total_tokens": 3
  }
}
```

### Audio Transcription

#### Request Format

```bash
curl -X POST https://leapfrogai-api.uds.dev/v1/audio/transcriptions \
  -H "Authorization: Bearer $LEAPFROGAI_API_KEY" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@audio.mp3" \
  -F "model=whisper" \
  -F "language=en"
```

#### Response Format

```json
{
  "text": "Hello, this is a transcription of the audio file.",
  "language": "en",
  "duration": 5.2
}
```

## Conclusion

This handbook provides comprehensive guidance for deploying, developing, and operating the CowabungaAI platform. The platform's modular architecture and open-source nature make it suitable for various deployment scenarios, from edge computing to cloud environments.

For additional information and community support, refer to the project documentation and community resources.

*Last Updated: September 2025*