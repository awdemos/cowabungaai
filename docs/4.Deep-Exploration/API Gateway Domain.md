# API Gateway Domain Technical Documentation

## 1. Overview

The API Gateway Domain serves as the central service layer in the CowabungaAI microservices architecture, providing RESTful HTTP endpoints and gRPC interfaces for all AI capabilities. Built with Rust and the Axum framework, this domain acts as the primary entry point for client requests, orchestrating communication between the User Interface, AI Inference services, and Data Persistence layers.

### 1.1 Domain Responsibilities

| Responsibility | Description |
|---------------|-------------|
| Request Routing | Routes incoming HTTP requests to appropriate backend services |
| Authentication | Validates API keys and manages user authentication |
| Request Validation | Ensures input parameters meet schema requirements |
| Inter-Service Communication | Facilitates gRPC calls to AI Inference Domain services |
| Response Aggregation | Combines responses from multiple services into unified output |
| Error Handling | Implements graceful error propagation and fallback mechanisms |

### 1.2 Strategic Importance

The API Gateway Domain holds a critical importance score of **9.0/10** within the system architecture. It serves as the single point of entry for all client interactions, making it essential for:

- **Security**: Centralized authentication and authorization
- **Scalability**: Load balancing and request distribution
- **Observability**: Unified logging and tracing across services
- **Maintainability**: Clear separation of concerns between client-facing and backend logic

---

## 2. Architecture

### 2.1 Component Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                    API Gateway Domain                            │
│                        /rust/crates/api/                         │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              HTTP API Layer (Axum Framework)             │   │
│  │  - main.rs: Application entry point                      │   │
│  │  - router.rs: Route configuration                        │   │
│  │  - auth.rs: Authentication middleware                    │   │
│  │  - types.rs: Request/response type definitions          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │           gRPC Backend Interface                         │   │
│  │  - backend.rs: Backend trait abstraction                 │   │
│  │  - GrpcBackend: Production gRPC client implementation   │   │
│  │  - StubBackend: Development/testing mock implementation │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| HTTP Server | Axum (Rust) | RESTful API implementation |
| Runtime | Tokio | Async runtime for high concurrency |
| Logging | Tracing | Structured logging and distributed tracing |
| Database | LibSQL/Turso | Application data persistence |
| Inter-Service | gRPC | High-performance RPC communication |
| Serialization | Serde | JSON and Protobuf serialization |

---

## 3. Core Components

### 3.1 HTTP API Layer

The HTTP API Layer is the client-facing interface that receives all external requests and routes them to appropriate handlers.

#### 3.1.1 Entry Point (`main.rs`)

The application entry point initializes the entire API Gateway infrastructure:

```rust
// Key initialization steps:
1. Configure Tokio async runtime
2. Set up tracing logging with environment variables
3. Initialize database connection (LibSQL or Memory for testing)
4. Create AppState with application context
5. Configure Axum router with middleware stack
6. Start HTTP server on configured port
```

**Key Features:**
- **Async Runtime**: Uses Tokio for non-blocking I/O operations
- **Database Integration**: Supports both production (Turso) and development (Memory) modes
- **State Management**: AppState provides shared application context across handlers

#### 3.1.2 Router Configuration (`router.rs`)

The router defines all HTTP endpoints and applies middleware:

```
┌─────────────────────────────────────────────────────────────────┐
│                        Router Configuration                      │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Middleware Stack                            │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │   │
│  │  │ Auth Check  │→│ CORS Handler │→│ Tracing     │      │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘      │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Route Definitions                           │   │
│  │  POST   /chat/completions    → Chat completion handler  │   │
│  │  POST   /embeddings          → Embedding generation     │   │
│  │  POST   /audio/transcribe    → Audio transcription     │   │
│  │  GET    /health              → Health check endpoint    │   │
│  │  GET    /models              → Model listing endpoint   │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

**Middleware Stack:**
1. **Authentication Middleware**: Validates API keys before request processing
2. **CORS Handler**: Configures Cross-Origin Resource Sharing for web clients
3. **Tracing Layer**: Adds distributed tracing headers for observability

#### 3.1.3 Authentication (`auth.rs`)

The authentication module implements API key validation:

```rust
// Authentication flow:
1. Extract API key from request headers
2. Validate against stored API keys (Turso database)
3. Create authenticated user context
4. Attach context to request state
```

**Security Features:**
- API key validation against database records
- Rate limiting integration (recommended enhancement)
- Request signing support for enhanced security

### 3.2 gRPC Backend Interface

The gRPC Backend Interface provides abstraction for backend service communication, enabling both production and development modes.

#### 3.2.1 Backend Trait (`backend.rs`)

The Backend trait defines the contract for all backend implementations:

```rust
pub trait Backend: Send + Sync {
    /// Execute chat completion request
    async fn chat_completion(
        &self,
        request: ChatCompletionRequest,
    ) -> Result<ChatCompletionResponse, Error>;
    
    /// Execute streaming chat completion
    async fn chat_completion_stream(
        &self,
        request: ChatCompletionStreamRequest,
    ) -> Result<ChatCompletionStream, Error>;
    
    /// Generate text embeddings
    async fn generate_embeddings(
        &self,
        request: EmbeddingsRequest,
    ) -> Result<EmbeddingsResponse, Error>;
    
    /// Transcribe audio to text
    async fn transcribe_audio(
        &self,
        request: AudioTranscriptionRequest,
    ) -> Result<AudioTranscriptionResponse, Error>;
}
```

**Key Design Principles:**
- **Async/Await**: All methods are async for non-blocking I/O
- **Error Handling**: Returns Result type for proper error propagation
- **Type Safety**: Strongly typed request/response structures
- **Future-Proof**: Trait abstraction allows backend substitution

#### 3.2.2 GrpcBackend Implementation

The GrpcBackend implements the Backend trait using gRPC client communication:

```rust
pub struct GrpcBackend {
    client: CowabungaSdkClient,  // Generated gRPC client
    endpoint: String,             // Backend service endpoint
}

impl Backend for GrpcBackend {
    async fn chat_completion(&self, request: ChatCompletionRequest) -> Result<ChatCompletionResponse, Error> {
        // 1. Create gRPC request
        let grpc_request = self.client.chat_completion(request).await?;
        
        // 2. Handle streaming responses
        let mut stream = grpc_request.into_stream();
        
        // 3. Aggregate tokens into final response
        let mut tokens = Vec::new();
        while let Some(token) = stream.next().await {
            tokens.push(token?);
        }
        
        // 4. Return aggregated response
        Ok(ChatCompletionResponse { tokens, ... })
    }
}
```

**Production Deployment:**
- Connects to TensorZero or self-hosted LLM services via gRPC
- Uses environment variables for endpoint configuration
- Implements connection pooling for efficiency

#### 3.2.3 StubBackend Implementation

The StubBackend provides mock implementations for development and testing:

```rust
pub struct StubBackend {
    mock_responses: HashMap<String, MockResponse>,
}

impl Backend for StubBackend {
    async fn chat_completion(&self, _request: ChatCompletionRequest) -> Result<ChatCompletionResponse, Error> {
        // Return predefined mock response
        Ok(ChatCompletionResponse {
            tokens: vec!["mock".to_string()],
            ...
        })
    }
}
```

**Development Benefits:**
- Enables API development without backend dependencies
- Facilitates unit testing with deterministic responses
- Supports integration testing with mock services

---

## 4. Business Flow Integration

### 4.1 Chat Completion Flow

The API Gateway Domain orchestrates the primary chat completion workflow:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Chat Completion Flow                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. User Interface Domain                                        │
│     └─ User submits chat message via Leptos SSR UI               │
│                                                                  │
│  2. API Gateway Domain (HTTP API Layer)                          │
│     ├─ POST /chat/completions                                    │
│     ├─ Validate request parameters                               │
│     ├─ Check API key authentication                              │
│     └─ Forward to gRPC backend                                   │
│                                                                  │
│  3. API Gateway Domain (gRPC Backend)                            │
│     └─ Forward request to LLM Inference Service via gRPC         │
│                                                                  │
│  4. AI Inference Domain                                          │
│     └─ LLM generates response with streaming tokens              │
│                                                                  │
│  5. API Gateway Domain                                           │
│     ├─ Aggregate streaming tokens                                │
│     ├─ Store conversation history in Turso SQLite                │
│     └─ Return complete response to client                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Key Operations:**
- Request validation and sanitization
- Authentication middleware execution
- gRPC request forwarding
- Streaming response aggregation
- Conversation history persistence

### 4.2 Text Embedding Generation Flow

The API Gateway handles text embedding requests for vector search:

```
┌─────────────────────────────────────────────────────────────────┐
│                   Text Embedding Flow                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. API Gateway Domain (HTTP API Layer)                          │
│     └─ POST /embeddings                                          │
│                                                                  │
│  2. API Gateway Domain (gRPC Backend)                            │
│     └─ Forward to Text Embeddings Service via gRPC               │
│                                                                  │
│  3. AI Inference Domain                                          │
│     └─ Generate vector embeddings using InstructorEmbedding      │
│                                                                  │
│  4. API Gateway Domain                                           │
│     └─ Store embeddings in Supabase PostgreSQL vector_store      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Key Operations:**
- Embedding request validation
- gRPC communication with embeddings service
- Vector data storage in Supabase
- Metadata association with embeddings

### 4.3 Audio Transcription Flow

The API Gateway processes audio transcription requests:

```
┌─────────────────────────────────────────────────────────────────┐
│                   Audio Transcription Flow                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. User Interface Domain                                        │
│     └─ User uploads audio file through UI                        │
│                                                                  │
│  2. API Gateway Domain (HTTP API Layer)                          │
│     ├─ POST /audio/transcribe                                    │
│     ├─ Validate file format and size constraints                 │
│     └─ Forward to gRPC backend                                   │
│                                                                  │
│  3. API Gateway Domain (gRPC Backend)                            │
│     └─ Forward to Whisper Service via gRPC                       │
│                                                                  │
│  4. AI Inference Domain                                          │
│     └─ Whisper model transcribes audio to text                   │
│                                                                  │
│  5. API Gateway Domain                                           │
│     └─ Store transcribed text and metadata in Turso SQLite       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Key Operations:**
- File upload validation
- Audio format verification
- gRPC communication with Whisper service
- Transcription metadata storage

---

## 5. Inter-Service Communication

### 5.1 Communication Patterns

The API Gateway Domain uses multiple communication protocols:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Communication Patterns                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              HTTP Communication (REST)                  │   │
│  │  UI ──→ API Gateway ──→ Supabase (PostgreSQL)          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              gRPC Communication (Internal)              │   │
│  │  API Gateway ──→ LLM Service                            │   │
│  │  API Gateway ──→ Embeddings Service                     │   │
│  │  API Gateway ──→ Audio Service                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Database Communication                      │   │
│  │  API Gateway ──→ Turso (libSQL)                         │   │
│  │  API Gateway ──→ Supabase (PostgreSQL)                  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 gRPC Protocol Specifications

**Protobuf Definitions:**
- Location: `/rust/proto/cowabunga_sdk/`
- Generated Code: `/rust/crates/sdk/src/generated/`

**Services:**
| Service | Description |
|---------|-------------|
| ChatCompletionService | Chat completion requests and responses |
| ChatCompletionStreamService | Streaming chat completion support |
| EmbeddingsService | Text embedding generation |
| AudioService | Audio transcription |
| CountingService | Token counting utilities |
| NameService | Model name management |

**gRPC Client Configuration:**
```rust
// Production gRPC client setup
let client = CowabungaSdkClient::connect(
    "grpc://llm-service:50051",
    ChannelArgs::new()
        .set("grpc.max_send_message_length", "104857600")  // 100MB
        .set("grpc.max_receive_message_length", "104857600")
);
```

### 5.3 External Systems Integration

| System | Type | Interaction | Purpose |
|--------|------|-------------|---------|
| TensorZero | LLM Gateway | gRPC | Model inference requests |
| Supabase | Database | PostgreSQL | Vector storage, user data |
| Turso | Database | libSQL | Application persistence |
| NVIDIA GPU Runtime | Infrastructure | CUDA | GPU acceleration |
| Kubernetes/K3d | Orchestration | Container | Service deployment |

---

## 6. Implementation Details

### 6.1 Code Structure

```
rust/crates/api/
├── src/
│   ├── main.rs          # Application entry point
│   │   └─ Tokio runtime initialization
│   │   └─ AppState creation
│   │   └─ Server startup
│   ├── router.rs        # HTTP routing configuration
│   │   └─ Route definitions
│   │   └─ Middleware stack
│   │   └─ Protected routes with auth
│   ├── backend.rs       # gRPC backend interface
│   │   └─ Backend trait definition
│   │   └─ GrpcBackend implementation
│   │   └─ StubBackend implementation
│   ├── auth.rs          # Authentication logic
│   │   └─ API key validation
│   │   └─ User context creation
│   ├── types.rs         # Request/response types
│   │   └─ ChatCompletionRequest
│   │   └─ ChatCompletionResponse
│   │   └─ EmbeddingsRequest
│   │   └─ AudioTranscriptionRequest
│   └── error.rs         # Error handling
│       └─ Custom error types
│       └─ Error propagation
└── Cargo.toml           # Dependencies
```

### 6.2 Database Integration

**Turso SQLite Adapter:**
```rust
// Database connection initialization
let db = Libsql::new(
    "turso://api-key:password@host:port/database",
    Config::default()
);

// Connection management
db.health_check().await?;
db.run_migration().await?;
```

**Supabase PostgreSQL Integration:**
```rust
// Vector data storage
let client = SupabaseClient::new(
    "postgresql://user:password@host:5432/database"
);

// Store embeddings
client
    .table("vector_store")
    .insert(embedding_data)
    .execute()
    .await?;
```

### 6.3 Configuration Management

The API Gateway supports environment-specific configuration:

```yaml
# Example configuration (uds-config.yaml)
api:
  port: 8080
  workers: 4
  
database:
  turso:
    url: "turso://..."
    timeout: 30000
  supabase:
    url: "postgresql://..."
    pool_size: 10

backend:
  grpc:
    endpoint: "grpc://llm-service:50051"
    timeout: 60000
    retry_attempts: 3

security:
  api_key_validation: true
  cors_origins:
    - "https://example.com"
    - "https://app.example.com"
```

---

## 7. Security and Authentication

### 7.1 Authentication Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    Authentication Flow                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Client Request                                              │
│     └─ POST /chat/completions                                   │
│     └─ Header: Authorization: Bearer <api_key>                  │
│                                                                  │
│  2. Auth Middleware                                            │
│     ├─ Extract API key from header                              │
│     ├─ Query Turso database for valid keys                      │
│     ├─ Validate key format and permissions                      │
│     └─ Create authenticated user context                        │
│                                                                  │
│  3. Request Processing                                          │
│     └─ Process request with user context                        │
│                                                                  │
│  4. Response                                                    │
│     └─ Return response with user context                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 7.2 Security Features

| Feature | Implementation | Status |
|---------|---------------|--------|
| API Key Validation | Database lookup | ✅ Implemented |
| CORS Configuration | Middleware | ✅ Implemented |
| Request Validation | Schema validation | ✅ Implemented |
| Rate Limiting | Recommended | ⚠️ Enhancement |
| Request Signing | Recommended | ⚠️ Enhancement |

---

## 8. Error Handling and Fallback

### 8.1 Error Propagation

The API Gateway implements comprehensive error handling:

```rust
// Error handling pattern
async fn chat_completion(request: ChatCompletionRequest) -> Result<Response, Error> {
    // 1. Validate request
    let validated = validate_request(&request)?;
    
    // 2. Check backend availability
    let backend = get_backend()?;
    
    // 3. Execute with timeout
    let result = timeout(Duration::from_secs(60), async {
        backend.chat_completion(validated).await
    }).await??;
    
    // 4. Handle errors
    match result {
        Ok(response) => Ok(response),
        Err(e) => {
            // Log error with tracing
            tracing::error!("Backend error: {:?}", e);
            
            // Return appropriate error response
            Err(ApiError::BackendUnavailable(e.to_string()))
        }
    }
}
```

### 8.2 Stub Backend for Testing

The StubBackend enables development without backend dependencies:

```rust
// Development mode configuration
#[cfg(feature = "dev")]
pub fn get_backend() -> Result<StubBackend, Error> {
    Ok(StubBackend::new())
}

// Production mode configuration
#[cfg(not(feature = "dev"))]
pub fn get_backend() -> Result<GrpcBackend, Error> {
    GrpcBackend::new("grpc://llm-service:50051").await
}
```

**Benefits:**
- Enables API development without backend services
- Facilitates unit testing with deterministic responses
- Supports integration testing with mock services

---

## 9. Deployment and Infrastructure

### 9.1 Kubernetes Integration

The API Gateway is deployed using Helm charts:

```yaml
# packages/api/chart/templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-gateway
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api-gateway
  template:
    spec:
      containers:
      - name: api
        image: cowabungaai/api:latest
        ports:
        - containerPort: 8080
        env:
        - name: TURSO_URL
          valueFrom:
            secretKeyRef:
              name: api-secrets
              key: turso-url
        - name: SUPABASE_URL
          valueFrom:
            secretKeyRef:
              name: api-secrets
              key: supabase-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

### 9.2 Environment Configuration

**Development Environment:**
- Memory: 256Mi
- CPU: 250m
- Database: Memory (in-memory)
- Backend: StubBackend

**Production Environment:**
- Memory: 512Mi+
- CPU: 500m+
- Database: Turso (production)
- Backend: GrpcBackend (production)

### 9.3 Health Checks

The API Gateway provides health check endpoints:

```
GET /health
├─ Status: healthy/unhealthy
├─ Database: connected/disconnected
├─ Backend: available/unavailable
└─ Timestamp: current time
```

---

## 10. Performance Considerations

### 10.1 Connection Pooling

Database connections use connection pooling for efficiency:

```rust
// Connection pool configuration
let pool = Libsql::new_with_pool(
    "turso://...",
    PoolConfig {
        max_size: 20,
        min_size: 5,
        timeout: Duration::from_secs(30),
    }
);
```

### 10.2 Streaming Support

The API Gateway supports streaming responses for chat completions:

```rust
// Streaming response handling
async fn chat_completion_stream(request: ChatCompletionStreamRequest) -> Result<Stream, Error> {
    let mut stream = backend.chat_completion_stream(request).await?;
    
    // Stream tokens to client
    while let Some(token) = stream.next().await {
        let response = ChatCompletionChunk {
            id: request.id.clone(),
            choices: vec![ChatCompletionChoice {
                delta: Delta { content: token? },
                ...
            }],
            ...
        };
        
        // Send SSE response
        send_sse(&response).await?;
    }
    
    Ok(())
}
```

### 10.3 Request Timeout

All backend calls have configurable timeouts:

```rust
// Timeout configuration
let timeout = Duration::from_secs(60);  // 60 seconds max

// Apply timeout to backend calls
let result = timeout(timeout, async {
    backend.chat_completion(request).await
}).await??;
```

---

## 11. Monitoring and Observability

### 11.1 Tracing Integration

The API Gateway implements distributed tracing:

```rust
// Tracing middleware
axum::middleware::from_fn_with_state(state, tracing_layer);

// Request tracing
#[instrument(skip_all)]
async fn chat_completion(request: Request<ChatCompletionRequest>) -> Result<Response, Error> {
    let span = tracing::info_span!("chat_completion");
    let _guard = span.enter();
    
    // Process request with tracing
    let result = process_request(request).await;
    
    // Record metrics
    metrics::counter!("api.requests").increment(1);
    metrics::histogram!("api.duration").record(duration);
    
    result
}
```

### 11.2 Metrics Collection

Key metrics collected:
- Request count per endpoint
- Response latency (p50, p95, p99)
- Error rates
- Backend availability
- Database connection pool usage

---

## 12. Best Practices and Recommendations

### 12.1 Security Enhancements

1. **Rate Limiting**: Implement per-API-key rate limiting to prevent abuse
2. **Request Validation**: Add schema validation for all request parameters
3. **API Key Rotation**: Document procedures for API key rotation
4. **Input Sanitization**: Ensure all user inputs are sanitized before processing

### 12.2 Performance Optimizations

1. **Connection Pooling**: Implement database connection pooling
2. **Caching Layer**: Add caching for frequently accessed embeddings
3. **Compression**: Enable gzip compression for responses
4. **Load Balancing**: Configure Kubernetes load balancing for high availability

### 12.3 Development Practices

1. **Testing Strategy**: Implement integration tests for gRPC communication
2. **Chaos Engineering**: Create scenarios for backend failure handling
3. **Documentation**: Add comprehensive API documentation (OpenAPI/Swagger)
4. **Monitoring**: Implement comprehensive monitoring and alerting

---

## 13. Conclusion

The API Gateway Domain is a critical component of the CowabungaAI architecture, serving as the central hub for all client interactions. Built with Rust and the Axum framework, it provides robust RESTful APIs and gRPC interfaces for AI capabilities. The domain's design emphasizes modularity, security, and performance, with clear separation between HTTP API handling and backend service communication.

**Key Strengths:**
- Clear separation of concerns between HTTP and gRPC layers
- Comprehensive error handling and fallback mechanisms
- Support for both development (StubBackend) and production (GrpcBackend) modes
- Integration with dual-database strategy (Turso + Supabase)
- Kubernetes-ready deployment configuration

**Areas for Enhancement:**
- Rate limiting implementation
- Comprehensive API documentation
- Enhanced monitoring and observability
- Security hardening (request signing, input validation)

The API Gateway Domain successfully balances complexity with maintainability, providing a solid foundation for enterprise AI applications while remaining accessible for development and deployment.