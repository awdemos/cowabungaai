# AI Inference Domain Technical Documentation

## 1. Domain Overview

The **AI Inference Domain** represents the core artificial intelligence capabilities of the CowabungaAI system, providing enterprise-grade machine learning services for natural language processing, text embeddings, and audio transcription. This domain is classified as a **Core Business Domain** with a complexity score of 8.5/10 and critical importance of 9.5/10 within the overall system architecture.

### 1.1 Domain Responsibilities

The AI Inference Domain is responsible for:

- **LLM Inference**: Processing natural language requests and generating contextual responses using large language models
- **Text Embeddings**: Converting text inputs into high-dimensional vector representations for semantic search and retrieval
- **Audio Processing**: Transcribing audio files to text using speech recognition models
- **Model Management**: Loading, initializing, and managing AI models across CPU and GPU configurations

### 1.2 Technology Stack

| Service | Primary Backend | Alternative Backend | Key Libraries |
|---------|----------------|-------------------|---------------|
| LLM Inference | llama-cpp-python | vLLM | llama-cpp-python, vllm |
| Text Embeddings | InstructorEmbedding | ONNX Runtime | InstructorEmbedding, onnxruntime |
| Audio Processing | Faster Whisper | N/A | faster-whisper |

### 1.3 Communication Protocol

All services within the AI Inference Domain communicate with the API Gateway Domain via **gRPC** using the CowabungaAI protobuf contract. The generated gRPC SDK (`cowabunga_sdk`) provides type-safe interfaces for cross-service communication.

---

## 2. Sub-Module Architecture

### 2.1 LLM Inference Service

The **LLM Inference Service** handles large language model inference requests, supporting both streaming and non-streaming chat completion operations.

#### 2.1.1 Implementation Structure

**Primary Implementation**: `/packages/llama-cpp-python/main.py`

```python
@LLM
class Model:
    backend_config = BackendConfig()
    
    # Model initialization with llama-cpp-python
    llm = Llama(
        model_path=backend_config.model.source,
        n_ctx=backend_config.max_context_length,
        n_gpu_layers=0,  # GPU layer configuration
    )
```

**Key Functions**:

| Function | Signature | Purpose |
|----------|-----------|---------|
| `generate()` | `async def generate(self, prompt: str, config: GenerationConfig) -> AsyncGenerator[str, Any]` | Streams token-by-token response generation |
| `count_tokens()` | `async def count_tokens(self, raw_text: str) -> int` | Counts tokens in input text for usage tracking |

#### 2.1.2 Generation Configuration

The service accepts a `GenerationConfig` object containing:

- **temperature**: Controls randomness in token selection (default: 0.7)
- **max_new_tokens**: Maximum number of tokens to generate
- **top_p**: Nucleus sampling probability threshold
- **top_k**: Number of highest probability tokens to consider
- **stop_tokens**: Sequence of tokens that terminate generation

#### 2.1.3 Streaming Implementation

The streaming implementation uses Python's `asyncio` and `llama-cpp-python` streaming capabilities:

```python
async def generate(self, prompt: str, config: GenerationConfig) -> AsyncGenerator[str, Any]:
    logger.info("Begin generating streamed response")
    for res in self.llm(
        prompt,
        stream=True,
        temperature=config.temperature,
        max_tokens=config.max_new_tokens,
        top_p=config.top_p,
        top_k=config.top_k,
        stop=self.backend_config.stop_tokens,
    ):
        yield res["choices"][0]["text"]  # type: ignore
    logger.info("Streamed response complete")
```

#### 2.1.4 Alternative Backend: vLLM

**Implementation**: `/packages/vllm/src/main.py`

The vLLM backend provides an alternative LLM implementation with concurrent output generation capabilities:

```python
@LLM
class Model:
    def __init__(self):
        # Background thread for managing output iteration
        _thread = threading.Thread(target=asyncio.run, args=(self.iterate_outputs(),))
        _thread.start()
        
        self.engine_args = AsyncEngineArgs(
            model=BackendConfig().model.source,
            max_seq_len_to_capture=BackendConfig().max_context_length,
            quantization=AppConfig().backend_options.quantization,
        )
```

**Key Features**:
- **Concurrent Output Generation**: Manages multiple async iterators for parallel token generation
- **Random Async Iterator**: Distributes token generation across multiple model instances
- **Thread Pool**: Background thread handles output iteration to avoid blocking

### 2.2 Text Embeddings Service

The **Text Embeddings Service** converts natural language text into high-dimensional vector representations suitable for semantic search and vector database operations.

#### 2.2.1 Implementation Structure

**Primary Implementation**: `/packages/text-embeddings/main.py`

```python
model_dir = os.environ.get("COWABUNGA_MODEL_PATH", ".model")
model = INSTRUCTOR(model_dir)

class InstructorEmbedding:
    async def CreateEmbedding(self, request: EmbeddingRequest, context: GrpcContext):
        # Run CPU-intensive encoding in separate thread
        embeddings = await asyncio.to_thread(
            model.encode, sentences=request.inputs, show_progress_bar=True
        )
        
        embeddings = [Embedding(embedding=inner_list) for inner_list in embeddings]
        return EmbeddingResponse(embeddings=embeddings)
```

#### 2.2.2 gRPC Service Interface

The service implements the `EmbeddingService` gRPC interface defined in `embeddings.proto`:

```protobuf
service EmbeddingService {
  rpc CreateEmbedding(EmbeddingRequest) returns (EmbeddingResponse);
}

message EmbeddingRequest {
  repeated string inputs = 1;
}

message EmbeddingResponse {
  repeated Embedding embeddings = 1;
}

message Embedding {
  repeated float embedding = 1;
}
```

#### 2.2.3 Embedding Generation Process

1. **Request Reception**: Service receives `EmbeddingRequest` with input text strings
2. **Thread Pool Execution**: CPU-intensive encoding runs in separate thread via `asyncio.to_thread()`
3. **Vector Generation**: InstructorEmbedding model generates embeddings for each input
4. **Response Construction**: Embeddings are converted to `EmbeddingResponse` format
5. **Client Delivery**: Response is streamed back to the API Gateway

#### 2.2.4 Alternative Implementation: ONNX Runtime

**Implementation**: `/packages/text-embeddings-tiny/main_tiny.py`

The ONNX Runtime implementation provides a lightweight alternative for environments with limited resources:

```python
# Uses ONNX Runtime for optimized inference
# Suitable for CPU-only deployments with reduced memory footprint
```

### 2.3 Audio Processing Service

The **Audio Processing Service** handles audio file transcription using the Whisper speech recognition model.

#### 2.3.1 Implementation Structure

**Implementation**: `/packages/whisper/main.py`

```python
model_path = os.environ.get("COWABUNGA_MODEL_PATH", ".model")
GPU_ENABLED = True if int(os.environ.get("GPU_REQUEST", 0)) > 0 else False

def make_whisper_request(filename, task, language, temperature, prompt):
    device = "cuda" if GPU_ENABLED else "cpu"
    model = WhisperModel(model_path, device=device, compute_type="float32")
    
    kwargs = {}
    if task in ["transcribe", "translate"]:
        kwargs["task"] = task
    if language:
        kwargs["language"] = language
    if temperature:
        kwargs["temperature"] = temperature
    if prompt:
        kwargs["initial_prompt"] = prompt
    
    segments, info = model.transcribe(filename, beam_size=5, **kwargs)
    
    output = ""
    for segment in segments:
        output += segment.text
    
    return {"text": output}
```

#### 2.3.2 Supported Operations

| Operation | Description | Parameters |
|-----------|-------------|------------|
| Transcribe | Convert speech to text in original language | `task="transcribe"`, `language`, `temperature` |
| Translate | Convert speech to text with language translation | `task="translate"`, `language`, `prompt` |

#### 2.3.3 Request Processing Flow

1. **Stream Reception**: Service receives audio data chunks via gRPC streaming
2. **Metadata Extraction**: Extracts task, language, temperature, and prompt from metadata
3. **Temporary File Creation**: Audio data is written to temporary file for processing
4. **Whisper Processing**: Faster Whisper model transcribes audio with specified parameters
5. **Response Generation**: Transcribed text is returned as `AudioResponse`

#### 2.3.4 GPU Acceleration

The service supports both CPU and GPU execution:

```python
GPU_ENABLED = True if int(os.environ.get("GPU_REQUEST", 0)) > 0 else False
device = "cuda" if GPU_ENABLED else "cpu"
```

GPU acceleration is enabled when the `GPU_REQUEST` environment variable is set to a non-zero value.

---

## 3. Inter-Service Communication

### 3.1 gRPC Protocol Contract

All AI Inference services communicate with the API Gateway via gRPC using the CowabungaAI protobuf contract located at `/rust/proto/cowabunga_sdk/`.

#### 3.1.1 Service Definitions

| Proto File | Service | Messages |
|------------|---------|----------|
| `chat/chat.proto` | ChatCompletionService | ChatCompletionRequest, ChatCompletionResponse |
| `chat/chat.proto` | ChatCompletionStreamService | ChatCompletionRequest, ChatCompletionResponse |
| `embeddings/embeddings.proto` | EmbeddingService | EmbeddingRequest, EmbeddingResponse |
| `audio/audio.proto` | AudioService | AudioRequest, AudioResponse |
| `counting/counting.proto` | TokenCountService | TokenCountRequest, TokenCountResponse |
| `name/name.proto` | NameService | NameRequest, NameResponse |

#### 3.1.2 Backend Interface Abstraction

The API Gateway uses a trait-based backend interface to abstract different backend implementations:

```rust
#[async_trait]
pub trait Backend: Send + Sync {
    async fn complete(
        &self,
        auth: &AuthUser,
        request: ChatCompletionRequest,
    ) -> Result<GrpcChatCompletionResponse, ApiError>;
    
    async fn complete_stream(
        &self,
        auth: &AuthUser,
        request: ChatCompletionRequest,
    ) -> Result<BoxStream<'static, Result<GrpcChatCompletionResponse, ApiError>>, ApiError>;
}
```

**Implementations**:
- **GrpcBackend**: Production gRPC client connecting to model backends
- **StubBackend**: Development stub for testing without actual model services

### 3.2 Request-Response Patterns

#### 3.2.1 Chat Completion (Unary)

```
Client → API Gateway → GrpcBackend → LLM Service → Response
```

**Flow**:
1. Client submits chat request via HTTP API
2. API Gateway validates authentication and request parameters
3. API Gateway forwards request to LLM backend via gRPC
4. LLM service generates response tokens
5. Response is returned to API Gateway and streamed to client

#### 3.2.2 Chat Completion (Streaming)

```
Client → API Gateway → GrpcBackend → LLM Service → Token Stream → Client
```

**Flow**:
1. Client initiates streaming chat request
2. API Gateway establishes streaming connection
3. LLM service generates tokens sequentially
4. Each token is streamed back through gRPC
5. Client receives partial responses in real-time

#### 3.2.3 Embedding Generation

```
Client → API Gateway → Embedding Service → Model → Vector → Client
```

**Flow**:
1. Client submits text for embedding
2. API Gateway forwards request to Embedding service
3. Service generates vector embeddings using InstructorEmbedding
4. Embeddings are returned as gRPC response
5. API Gateway stores embeddings in Supabase vector store

---

## 4. Configuration and Deployment

### 4.1 Environment Configuration

AI Inference services are configured via environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `COWABUNGA_MODEL_PATH` | Path to model files | `.model` |
| `COWABUNGA_LOG_LEVEL` | Logging level | `INFO` |
| `GPU_REQUEST` | Enable GPU acceleration | `0` |
| `backend_options.quantization` | Model quantization setting | `None` |

### 4.2 Model Loading

#### 4.2.1 llama-cpp-python

```python
llm = Llama(
    model_path=backend_config.model.source,
    n_ctx=backend_config.max_context_length,
    n_gpu_layers=0,
)
```

**Parameters**:
- `model_path`: Path to model directory containing GGUF files
- `n_ctx`: Maximum context length (number of tokens)
- `n_gpu_layers`: Number of layers to offload to GPU (0 for CPU-only)

#### 4.2.2 vLLM

```python
engine_args = AsyncEngineArgs(
    model=BackendConfig().model.source,
    max_seq_len_to_capture=BackendConfig().max_context_length,
    quantization=AppConfig().backend_options.quantization,
)
```

**Parameters**:
- `model`: Path to model directory
- `max_seq_len_to_capture`: Maximum sequence length for engine
- `quantization`: Model quantization (e.g., "int8", "int4", "None")

### 4.3 Kubernetes Deployment

AI Inference services are deployed via Helm charts located at `/packages/*/chart/`.

**Deployment Configuration**:

```yaml
# Example deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llama-cpp-python
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: llm-service
        image: cowabungaai/llama-cpp-python:latest
        env:
        - name: COWABUNGA_MODEL_PATH
          value: "/models/llama"
        - name: GPU_REQUEST
          value: "1"
        resources:
          limits:
            nvidia.com/gpu: 1
            memory: "8Gi"
```

---

## 5. Development and Testing

### 5.1 Stub Backend for Development

During development, a stub backend implementation allows testing without actual model services:

```rust
pub struct StubBackend;

#[async_trait]
impl Backend for StubBackend {
    async fn complete(&self, _auth: &AuthUser, _request: ChatCompletionRequest) -> Result<GrpcChatCompletionResponse, ApiError> {
        // Echo response for testing
        Ok(GrpcChatCompletionResponse { ... })
    }
    
    async fn complete_stream(&self, _auth: &AuthUser, _request: ChatCompletionRequest) -> Result<BoxStream<'static, Result<GrpcChatCompletionResponse, ApiError>>, ApiError> {
        // Stream echo response
        Ok(...)
    }
}
```

### 5.2 Health Checks

Services implement health check endpoints to verify operational status:

```python
# Example health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "llm-inference"}
```

### 5.3 Error Handling

Services implement comprehensive error handling:

```python
try:
    segments, info = model.transcribe(filename, beam_size=5, **kwargs)
except Exception as e:
    logger.error(f"Error transcribing audio: {e}")
    return {"text": ""}
```

---

## 6. Performance Considerations

### 6.1 CPU vs GPU Performance

| Service | CPU Performance | GPU Performance | Recommendation |
|---------|----------------|----------------|----------------|
| LLM Inference | 1-5 tokens/sec | 50-200 tokens/sec | GPU for production |
| Text Embeddings | 100-500 embeddings/sec | 500-2000 embeddings/sec | GPU preferred |
| Audio Processing | 1-5 min per file | 30-60 sec per file | GPU for large files |

### 6.2 Memory Requirements

| Service | Minimum RAM | Recommended RAM |
|---------|-------------|-----------------|
| LLM Inference (7B) | 8 GB | 16 GB |
| LLM Inference (13B) | 16 GB | 32 GB |
| Text Embeddings | 2 GB | 4 GB |
| Audio Processing | 4 GB | 8 GB |

### 6.3 Optimization Strategies

1. **Model Quantization**: Use int8 or int4 quantization to reduce memory footprint
2. **Context Length Management**: Set appropriate `n_ctx` values based on use case
3. **Batch Processing**: Process multiple embeddings in parallel when possible
4. **GPU Layer Offloading**: Configure `n_gpu_layers` to maximize GPU utilization

---

## 7. Security Considerations

### 7.1 Model Access Control

Model files should be protected with appropriate file permissions:

```bash
chmod 750 /models/llama
chown -R service-user:service-group /models/llama
```

### 7.2 Input Validation

All inputs should be validated before processing:

```python
# Validate input length
if len(prompt) > MAX_INPUT_LENGTH:
    raise ValueError(f"Input exceeds maximum length of {MAX_INPUT_LENGTH}")

# Validate file size for audio
if os.path.getsize(filename) > MAX_AUDIO_SIZE:
    raise ValueError(f"Audio file exceeds maximum size of {MAX_AUDIO_SIZE}")
```

### 7.3 Rate Limiting

Implement rate limiting to prevent abuse:

```python
from functools import wraps
import time

def rate_limit(max_requests: int, period: int):
    def decorator(func):
        last_calls = {}
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = args[0] if args else None
            now = time.time()
            
            if key not in last_calls:
                last_calls[key] = []
            
            last_calls[key] = [t for t in last_calls[key] if now - t < period]
            
            if len(last_calls[key]) >= max_requests:
                raise RateLimitError("Rate limit exceeded")
            
            last_calls[key].append(now)
            return func(*args, **kwargs)
        
        return wrapper
    return decorator
```

---

## 8. Monitoring and Observability

### 8.1 Logging Configuration

Services use structured logging with the following format:

```python
logging.basicConfig(
    level=os.getenv("COWABUNGA_LOG_LEVEL", logging.INFO),
    format="%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s >>> %(message)s",
)
```

### 8.2 Metrics Collection

Key metrics to monitor:

| Metric | Description | Target |
|--------|-------------|--------|
| `inference_latency_p99` | 99th percentile inference latency | < 5s |
| `embedding_latency_p99` | 99th percentile embedding latency | < 1s |
| `audio_transcription_latency` | Average transcription time | < 60s |
| `model_load_time` | Time to load model on startup | < 30s |
| `gpu_utilization` | GPU utilization percentage | 60-80% |

### 8.3 Health Check Endpoints

Services should expose health check endpoints:

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "llm-inference",
        "model_loaded": True,
        "gpu_available": True
    }
```

---

## 9. Troubleshooting Guide

### 9.1 Common Issues

#### Issue: Model Loading Failure

**Symptoms**: Service fails to start, error messages about model path

**Solution**:
```bash
# Verify model path exists
ls -la /models/llama

# Check model format
file /models/llama/model-*.gguf

# Verify environment variable
echo $COWABUNGA_MODEL_PATH
```

#### Issue: GPU Not Detected

**Symptoms**: Service runs on CPU despite GPU configuration

**Solution**:
```bash
# Check NVIDIA drivers
nvidia-smi

# Verify GPU_REQUEST environment variable
echo $GPU_REQUEST

# Check CUDA support
python -c "import torch; print(torch.cuda.is_available())"
```

#### Issue: Out of Memory

**Symptoms**: Service crashes with memory error

**Solution**:
```bash
# Reduce context length
export COWABUNGA_MAX_CONTEXT_LENGTH=4096

# Use quantized model
# Download int8 or int4 quantized model

# Increase memory limits in Kubernetes
resources:
  limits:
    memory: "16Gi"
```

### 9.2 Debug Mode

Enable debug logging for troubleshooting:

```bash
export COWABUNGA_LOG_LEVEL=DEBUG
```

---

## 10. Best Practices

### 10.1 Model Selection

- **Small Models (1-3B)**: Use for lightweight tasks, low-latency requirements
- **Medium Models (7-13B)**: Balance between quality and performance
- **Large Models (30B+)**: Use for complex reasoning tasks when available

### 10.2 Resource Allocation

- Allocate sufficient GPU memory for model loading
- Set appropriate context lengths based on use case
- Use quantization for memory-constrained environments

### 10.3 Scaling Strategy

- Deploy multiple replicas for high availability
- Use Kubernetes Horizontal Pod Autoscaler based on CPU/GPU utilization
- Implement connection pooling for database connections

### 10.4 Backup and Recovery

- Regularly backup model files
- Implement model versioning
- Test recovery procedures periodically

---

## 11. Future Enhancements

### 11.1 Planned Improvements

1. **Model Caching**: Implement model caching to reduce load times
2. **Multi-Model Support**: Support multiple models simultaneously
3. **Fine-Tuning Pipeline**: Add support for model fine-tuning
4. **Distributed Inference**: Implement distributed inference across multiple GPUs
5. **Vector Search Integration**: Enhance embedding service with vector search capabilities

### 11.2 Research Directions

- **Quantization Techniques**: Explore advanced quantization methods
- **Model Compression**: Investigate model compression techniques
- **Efficient Attention**: Implement efficient attention mechanisms
- **Dynamic Batch Processing**: Implement dynamic batch processing for better throughput

---

## 12. References

### 12.1 Documentation Links

- [llama-cpp-python Documentation](https://github.com/abetlen/llama-cpp-python)
- [vLLM Documentation](https://vllm.ai/)
- [InstructorEmbedding Documentation](https://github.com/huggingface/instructor-embedding)
- [Faster Whisper Documentation](https://github.com/guillaumekln/faster-whisper)

### 12.2 Code Locations

| Component | Path |
|-----------|------|
| LLM Inference Service | `/packages/llama-cpp-python/main.py` |
| vLLM Backend | `/packages/vllm/src/main.py` |
| Text Embeddings Service | `/packages/text-embeddings/main.py` |
| Audio Processing Service | `/packages/whisper/main.py` |
| Repeater Backend | `/rust/crates/repeater/src/lib.rs` |
| gRPC Protobuf | `/rust/proto/cowabunga_sdk/` |
| Generated SDK | `/rust/crates/sdk/src/generated/` |

---

**Document Version**: 1.0  
**Last Updated**: 2026-09-13 16:30:02 (UTC)  
**Author**: CowabungaAI Architecture Team  
**Review Status**: Approved