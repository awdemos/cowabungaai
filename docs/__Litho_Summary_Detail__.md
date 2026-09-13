# Project Analysis Summary Report (Full Version)

Generation Time: 2026-09-13 16:30:02 UTC

## Execution Timing Statistics

- **Total Execution Time**: 1317.78 seconds
- **Preprocessing Phase**: 0.40 seconds (0.0%)
- **Research Phase**: 53.98 seconds (4.1%)
- **Document Generation Phase**: 1263.40 seconds (95.9%)
- **Output Phase**: 0.00 seconds (0.0%)
- **Summary Generation Time**: 0.002 seconds

## Cache Performance Statistics and Savings

### Performance Metrics
- **Cache Hit Rate**: 92.0%
- **Total Operations**: 112
- **Cache Hits**: 103 times
- **Cache Misses**: 9 times
- **Cache Writes**: 10 times

### Savings
- **Inference Time Saved**: 589.4 seconds
- **Tokens Saved**: 163324 input + 81348 output = 244672 total
- **Estimated Cost Savings**: $0.1470
- **Performance Improvement**: 92.0%
- **Efficiency Improvement Ratio**: 0.4x (saved time / actual execution time)

## Core Research Data Summary

Complete content of four types of research materials according to Prompt template data integration rules:

### System Context Research Report
Provides core objectives, user roles, and system boundary information for the project.

```json
{
  "business_value": "Provides enterprise-grade AI chat assistant infrastructure with self-hosted LLM capabilities, reducing dependency on external AI services and enabling custom model deployment with GPU/CPU support.",
  "confidence_score": 8.5,
  "external_systems": [
    {
      "description": "LLM gateway service for model inference requests",
      "interaction_type": "gRPC",
      "name": "TensorZero"
    },
    {
      "description": "PostgreSQL database with pgvector extension for vector storage",
      "interaction_type": "Database",
      "name": "Supabase"
    },
    {
      "description": "SQLite database for application data persistence",
      "interaction_type": "Database",
      "name": "Turso"
    },
    {
      "description": "GPU acceleration infrastructure for model inference",
      "interaction_type": "Infrastructure",
      "name": "NVIDIA GPU Runtime"
    },
    {
      "description": "Container orchestration platform for service deployment",
      "interaction_type": "Infrastructure",
      "name": "Kubernetes/K3d"
    }
  ],
  "project_description": "AI-powered chat assistant platform with LLM inference, text embeddings, audio processing, and vector search capabilities. Built with Rust and Python microservices deployed on Kubernetes.",
  "project_name": "CowabungaAI",
  "project_type": "FullStackApp",
  "system_boundary": {
    "excluded_components": [
      "External LLM provider APIs beyond TensorZero gateway",
      "Third-party vector database services",
      "External audio processing services beyond Whisper",
      "Production Kubernetes cluster infrastructure",
      "CI/CD pipeline systems"
    ],
    "included_components": [
      "Rust API service with Axum framework",
      "Python LLM inference services (llama-cpp-python, vllm)",
      "Text embeddings service (InstructorEmbedding, ONNX)",
      "Whisper audio transcription service",
      "Leptos SSR web UI",
      "Turso SQLite database adapter",
      "Supabase PostgreSQL integration",
      "Kubernetes deployment manifests",
      "gRPC service stubs and repeater"
    ],
    "scope": "Self-hosted AI assistant platform with microservices architecture including LLM inference, embeddings, audio processing, and chat UI"
  },
  "target_users": [
    {
      "description": "Software engineers building AI-powered applications and chatbots",
      "name": "AI Application Developers",
      "needs": [
        "Access to LLM inference APIs",
        "Text embedding generation",
        "Audio transcription services",
        "Vector search functionality"
      ]
    },
    {
      "description": "DevOps engineers managing AI infrastructure deployments",
      "name": "System Administrators",
      "needs": [
        "Kubernetes deployment management",
        "GPU resource configuration",
        "Database migration support",
        "Service health monitoring"
      ]
    },
    {
      "description": "Users interacting with AI chat assistants through the UI",
      "name": "End Users",
      "needs": [
        "Natural language chat interface",
        "Conversation history management",
        "File upload and storage",
        "Real-time response streaming"
      ]
    }
  ]
}
```

### Domain Modules Research Report
Provides high-level domain division, module relationships, and core business process information.

```json
{
  "architecture_summary": "CowabungaAI employs a microservices architecture with Rust and Python technologies. The system is organized into five primary domains: AI Inference (LLM, embeddings, audio), API Gateway (central service layer), Data Persistence (dual database strategy with Turso SQLite and Supabase PostgreSQL), User Interface (Leptos SSR), and Infrastructure (Kubernetes deployment). Key architectural patterns include gRPC for inter-service communication, dual-database strategy for different use cases, and containerized deployment with GPU/CPU configuration support. The architecture emphasizes modularity with clear separation between inference services, API gateway, and data layers.",
  "business_flows": [
    {
      "description": "User sends chat message through UI, API processes request, LLM generates response with streaming",
      "entry_point": "/var/home/a/code/cowabungaai/rust/crates/ui/src/main.rs",
      "importance": 9.5,
      "involved_domains_count": 4,
      "name": "Chat Completion Flow",
      "steps": [
        {
          "code_entry_point": "/var/home/a/code/cowabungaai/rust/crates/ui/src/main.rs",
          "domain_module": "User Interface Domain",
          "operation": "User submits chat message via web interface",
          "step": 1,
          "sub_module": "Leptos SSR Application"
        },
        {
          "code_entry_point": "/var/home/a/code/cowabungaai/rust/crates/api/src/main.rs",
          "domain_module": "API Gateway Domain",
          "operation": "API receives and validates chat request",
          "step": 2,
          "sub_module": "HTTP API Layer"
        },
        {
          "code_entry_point": "/var/home/a/code/cowabungaai/rust/crates/api/src/backend.rs",
          "domain_module": "API Gateway Domain",
          "operation": "API forwards request to LLM backend via gRPC",
          "step": 3,
          "sub_module": "gRPC Backend Interface"
        },
        {
          "code_entry_point": "/var/home/a/code/cowabungaai/packages/llama-cpp-python/main.py",
          "domain_module": "AI Inference Domain",
          "operation": "LLM generates response with streaming token output",
          "step": 4,
          "sub_module": "LLM Inference Service"
        },
        {
          "code_entry_point": "/var/home/a/code/cowabungaai/rust/crates/db/src/libsql.rs",
          "domain_module": "Data Persistence Domain",
          "operation": "Store conversation history and message objects",
          "step": 5,
          "sub_module": "Turso SQLite Adapter"
        }
      ]
    },
    {
      "description": "Text input is processed to generate vector embeddings for vector search functionality",
      "entry_point": "/var/home/a/code/cowabungaai/rust/crates/api/src/main.rs",
      "importance": 8.0,
      "involved_domains_count": 3,
      "name": "Text Embedding Generation Flow",
      "steps": [
        {
          "code_entry_point": "/var/home/a/code/cowabungaai/rust/crates/api/src/main.rs",
          "domain_module": "API Gateway Domain",
          "operation": "API receives text embedding request",
          "step": 1,
          "sub_module": "HTTP API Layer"
        },
        {
          "code_entry_point": "/var/home/a/code/cowabungaai/packages/text-embeddings/main.py",
          "domain_module": "AI Inference Domain",
          "operation": "Text embeddings service processes input text",
          "step": 2,
          "sub_module": "Text Embeddings Service"
        },
        {
          "code_entry_point": "/var/home/a/code/cowabungaai/packages/api/supabase/migrations/20240502193159_v0.8.0_vector_stores.sql",
          "domain_module": "Data Persistence Domain",
          "operation": "Store vector embeddings in vector_store table",
          "step": 3,
          "sub_module": "Supabase PostgreSQL Integration"
        }
      ]
    },
    {
      "description": "Audio file is transcribed to text using Whisper model",
      "entry_point": "/var/home/a/code/cowabungaai/rust/crates/ui/src/main.rs",
      "importance": 7.5,
      "involved_domains_count": 4,
      "name": "Audio Transcription Flow",
      "steps": [
        {
          "code_entry_point": "/var/home/a/code/cowabungaai/rust/crates/ui/src/main.rs",
          "domain_module": "User Interface Domain",
          "operation": "User uploads audio file through UI",
          "step": 1,
          "sub_module": "Leptos SSR Application"
        },
        {
          "code_entry_point": "/var/home/a/code/cowabungaai/rust/crates/api/src/main.rs",
          "domain_module": "API Gateway Domain",
          "operation": "API receives and validates audio upload request",
          "step": 2,
          "sub_module": "HTTP API Layer"
        },
        {
          "code_entry_point": "/var/home/a/code/cowabungaai/packages/whisper/main.py",
          "domain_module": "AI Inference Domain",
          "operation": "Whisper model transcribes audio to text",
          "step": 3,
          "sub_module": "Audio Processing Service"
        },
        {
          "code_entry_point": "/var/home/a/code/cowabungaai/rust/crates/db/src/libsql.rs",
          "domain_module": "Data Persistence Domain",
          "operation": "Store transcribed text and audio metadata",
          "step": 4,
          "sub_module": "Turso SQLite Adapter"
        }
      ]
    }
  ],
  "confidence_score": 8.5,
  "domain_modules": [
    {
      "code_paths": [
        "/var/home/a/code/cowabungaai/packages/llama-cpp-python/main.py",
        "/var/home/a/code/cowabungaai/packages/vllm/src/main.py",
        "/var/home/a/code/cowabungaai/packages/text-embeddings/main.py",
        "/var/home/a/code/cowabungaai/packages/whisper/main.py"
      ],
      "complexity": 8.5,
      "description": "Core artificial intelligence capabilities including LLM inference, text embeddings, and audio processing services",
      "domain_type": "Core Business Domain",
      "importance": 9.5,
      "name": "AI Inference Domain",
      "sub_modules": [
        {
          "code_paths": [
            "/var/home/a/code/cowabungaai/packages/llama-cpp-python/main.py",
            "/var/home/a/code/cowabungaai/packages/vllm/src/main.py",
            "/var/home/a/code/cowabungaai/rust/crates/repeater/src/lib.rs"
          ],
          "description": "Handles large language model inference requests using llama-cpp-python and vLLM backends",
          "importance": 9.5,
          "key_functions": [
            "Chat completion streaming",
            "Token counting",
            "Model inference"
          ],
          "name": "LLM Inference Service"
        },
        {
          "code_paths": [
            "/var/home/a/code/cowabungaai/packages/text-embeddings/main.py",
            "/var/home/a/code/cowabungaai/packages/text-embeddings-tiny/main_tiny.py"
          ],
          "description": "Generates vector embeddings from text using InstructorEmbedding and ONNX runtime",
          "importance": 8.5,
          "key_functions": [
            "Text to vector embedding",
            "Embedding generation via gRPC",
            "Model loading from environment paths"
          ],
          "name": "Text Embeddings Service"
        },
        {
          "code_paths": [
            "/var/home/a/code/cowabungaai/packages/whisper/main.py"
          ],
          "description": "Handles audio transcription and processing using Whisper model",
          "importance": 7.5,
          "key_functions": [
            "Audio transcription",
            "Speech to text conversion"
          ],
          "name": "Audio Processing Service"
        }
      ]
    },
    {
      "code_paths": [
        "/var/home/a/code/cowabungaai/rust/crates/api/src/main.rs",
        "/var/home/a/code/cowabungaai/rust/crates/api/src/router.rs",
        "/var/home/a/code/cowabungaai/rust/crates/api/src/backend.rs"
      ],
      "complexity": 7.5,
      "description": "Central API service providing REST and gRPC endpoints for all AI capabilities",
      "domain_type": "Core Business Domain",
      "importance": 9.0,
      "name": "API Gateway Domain",
      "sub_modules": [
        {
          "code_paths": [
            "/var/home/a/code/cowabungaai/rust/crates/api/src/main.rs",
            "/var/home/a/code/cowabungaai/rust/crates/api/src/router.rs"
          ],
          "description": "RESTful API endpoints using Axum framework for client interactions",
          "importance": 9.0,
          "key_functions": [
            "Chat completion endpoints",
            "Model management",
            "Health checks"
          ],
          "name": "HTTP API Layer"
        },
        {
          "code_paths": [
            "/var/home/a/code/cowabungaai/rust/crates/api/src/backend.rs"
          ],
          "description": "Backend client interface for model backend communication",
          "importance": 8.0,
          "key_functions": [
            "GrpcBackend implementation",
            "StubBackend implementation",
            "Backend trait abstraction"
          ],
          "name": "gRPC Backend Interface"
        }
      ]
    },
    {
      "code_paths": [
        "/var/home/a/code/cowabungaai/rust/crates/db/src/libsql.rs",
        "/var/home/a/code/cowabungaai/packages/turso/api.py",
        "/var/home/a/code/cowabungaai/packages/api/supabase/migrations/20240419164109_v0.8.0_openai_types.sql"
      ],
      "complexity": 7.0,
      "description": "Database layer managing data storage, retrieval, and vector search capabilities",
      "domain_type": "Infrastructure Domain",
      "importance": 8.5,
      "name": "Data Persistence Domain",
      "sub_modules": [
        {
          "code_paths": [
            "/var/home/a/code/cowabungaai/rust/crates/db/src/libsql.rs",
            "/var/home/a/code/cowabungaai/packages/turso/api.py"
          ],
          "description": "SQLite database adapter with libSQL/Turso integration",
          "importance": 8.5,
          "key_functions": [
            "Connection management",
            "Migration support",
            "Health checks"
          ],
          "name": "Turso SQLite Adapter"
        },
        {
          "code_paths": [
            "/var/home/a/code/cowabungaai/packages/api/supabase/migrations/20240419164109_v0.8.0_openai_types.sql",
            "/var/home/a/code/cowabungaai/packages/api/supabase/migrations/20240502193159_v0.8.0_vector_stores.sql"
          ],
          "description": "PostgreSQL database with pgvector extension for vector storage",
          "importance": 8.5,
          "key_functions": [
            "User authentication",
            "Conversation management",
            "Vector search functionality"
          ],
          "name": "Supabase PostgreSQL Integration"
        }
      ]
    },
    {
      "code_paths": [
        "/var/home/a/code/cowabungaai/rust/crates/ui/src/main.rs",
        "/var/home/a/code/cowabungaai/rust/crates/ui/src/app.rs"
      ],
      "complexity": 6.0,
      "description": "Web UI application providing chat interface and user interaction capabilities",
      "domain_type": "Core Business Domain",
      "importance": 8.0,
      "name": "User Interface Domain",
      "sub_modules": [
        {
          "code_paths": [
            "/var/home/a/code/cowabungaai/rust/crates/ui/src/main.rs",
            "/var/home/a/code/cowabungaai/rust/crates/ui/src/app.rs"
          ],
          "description": "Server-side rendered web UI using Leptos framework",
          "importance": 8.0,
          "key_functions": [
            "Chat interface rendering",
            "Conversation history display",
            "File upload handling"
          ],
          "name": "Leptos SSR Application"
        }
      ]
    },
    {
      "code_paths": [
        "/var/home/a/code/cowabungaai/bundles/latest/cpu/uds-bundle.yaml",
        "/var/home/a/code/cowabungaai/bundles/dev/cpu/uds-config.yaml",
        "/var/home/a/code/cowabungaai/packages/api/chart/templates/deployment.yaml"
      ],
      "complexity": 5.0,
      "description": "Deployment configuration and infrastructure management for container orchestration",
      "domain_type": "Infrastructure Domain",
      "importance": 7.5,
      "name": "Infrastructure Domain",
      "sub_modules": [
        {
          "code_paths": [
            "/var/home/a/code/cowabungaai/packages/api/chart/templates/deployment.yaml",
            "/var/home/a/code/cowabungaai/packages/llama-cpp-python/chart/templates/deployment.yaml",
            "/var/home/a/code/cowabungaai/bundles/latest/cpu/uds-bundle.yaml"
          ],
          "description": "Kubernetes manifests and deployment configurations",
          "importance": 7.5,
          "key_functions": [
            "Pod management",
            "Resource configuration",
            "Service deployment"
          ],
          "name": "Kubernetes Deployment Manager"
        },
        {
          "code_paths": [
            "/var/home/a/code/cowabungaai/bundles/dev/cpu/uds-config.yaml",
            "/var/home/a/code/cowabungaai/bundles/latest/gpu/uds-config.yaml"
          ],
          "description": "Runtime configuration and environment variable management",
          "importance": 7.0,
          "key_functions": [
            "GPU settings configuration",
            "Environment variables",
            "Resource limits"
          ],
          "name": "Configuration Manager"
        }
      ]
    }
  ],
  "domain_relations": [
    {
      "description": "API Gateway calls LLM Inference Service, Text Embeddings Service, and Audio Processing Service for processing requests",
      "from_domain": "API Gateway Domain",
      "relation_type": "Service Call",
      "strength": 9.0,
      "to_domain": "AI Inference Domain"
    },
    {
      "description": "API Gateway depends on Data Persistence Domain for storing and retrieving conversation data, user authentication, and vector embeddings",
      "from_domain": "API Gateway Domain",
      "relation_type": "Data Dependency",
      "strength": 9.5,
      "to_domain": "Data Persistence Domain"
    },
    {
      "description": "User Interface calls API Gateway for all user interactions and chat operations",
      "from_domain": "User Interface Domain",
      "relation_type": "Service Call",
      "strength": 9.0,
      "to_domain": "API Gateway Domain"
    },
    {
      "description": "AI Inference Domain stores embeddings and conversation data in Data Persistence Domain",
      "from_domain": "AI Inference Domain",
      "relation_type": "Data Dependency",
      "strength": 7.5,
      "to_domain": "Data Persistence Domain"
    },
    {
      "description": "Infrastructure Domain provides deployment configurations and environment settings for API Gateway",
      "from_domain": "Infrastructure Domain",
      "relation_type": "Configuration Dependency",
      "strength": 6.0,
      "to_domain": "API Gateway Domain"
    },
    {
      "description": "Infrastructure Domain configures GPU resources and model deployment for AI Inference Domain",
      "from_domain": "Infrastructure Domain",
      "relation_type": "Configuration Dependency",
      "strength": 6.0,
      "to_domain": "AI Inference Domain"
    }
  ]
}
```

### Workflow Research Report
Contains static analysis results of the codebase and business process analysis.

```json
"# System Workflow Analysis\n\n## 1. Main Workflow\n\n### **Workflow Name**: Chat Completion Flow\n\n### **Description**:\nThe Chat Completion Flow is the primary business workflow of CowabungaAI, enabling users to interact with AI assistants through a web interface. This workflow orchestrates the entire conversation lifecycle from user input submission through LLM inference to response streaming and conversation history persistence. It represents the core value proposition of the system, integrating the User Interface, API Gateway, AI Inference services, and Data Persistence layers into a cohesive conversational experience.\n\n### **Flow Diagram**:\n```mermaid\ngraph TD\n    Start[User Submits Chat Message] --> UI[Leptos SSR UI Layer]\n    UI --> API[API Gateway HTTP Endpoint]\n    API --> Validate[Request Validation & Auth]\n    Validate --> Backend[Backend gRPC Interface]\n    Backend --> LLM[LLM Inference Service]\n    LLM --> Generate[Generate Response Tokens]\n    Generate --> Stream[Stream Response to Client]\n    Stream --> Store[Store Conversation History]\n    Store --> End[Return Complete Response]\n    \n    style Start fill:#e1f5e1\n    style End fill:#e1f5e1\n    style UI fill:#fff3cd\n    style API fill:#fff3cd\n    style LLM fill:#f8d7da\n    style Store fill:#d1ecf1\n```\n\n### **Key Steps**:\n\n| Step | Component | Operation | Purpose |\n|------|-----------|-----------|---------|\n| 1 | User Interface Domain | User submits chat message via web interface | Capture user input and initiate conversation |\n| 2 | API Gateway Domain | API receives and validates chat request | Authenticate request and validate input parameters |\n| 3 | API Gateway Domain | API forwards request to LLM backend via gRPC | Route request to appropriate inference service |\n| 4 | AI Inference Domain | LLM generates response with streaming token output | Process natural language and generate AI response |\n| 5 | Data Persistence Domain | Store conversation history and message objects | Persist conversation context for future reference |\n\n---\n\n## 2. Other Important Workflows\n\n### 2.1 Text Embedding Generation Flow\n\n### **Description**:\nThis workflow processes text inputs to generate vector embeddings for semantic search and vector database operations. It enables the system to convert natural language text into numerical vector representations that can be stored and queried using vector similarity search capabilities. This workflow is critical for features like conversation retrieval, semantic search, and knowledge base integration.\n\n### **Flow Diagram**:\n```mermaid\ngraph LR\n    A[API Receives Text Request] --> B[Text Embeddings Service]\n    B --> C[Model Loading Check]\n    C --> D[Generate Embeddings]\n    D --> E[Store in Vector Store]\n    E --> F[Return Embedding Data]\n    \n    style A fill:#fff3cd\n    style B fill:#f8d7da\n    style D fill:#d1ecf1\n    style E fill:#d1ecf1\n```\n\n### **Key Steps**:\n\n| Step | Component | Operation | Purpose |\n|------|-----------|-----------|---------|\n| 1 | API Gateway Domain | API receives text embedding request | Accept embedding generation request |\n| 2 | AI Inference Domain | Text embeddings service processes input text | Convert text to vector representation |\n| 3 | Data Persistence Domain | Store vector embeddings in vector_store table | Persist embeddings for vector search |\n\n### **Technical Details**:\n- **Entry Point**: `/var/home/a/code/cowabungaai/rust/crates/api/src/main.rs`\n- **Service Implementation**: `/var/home/a/code/cowabungaai/packages/text-embeddings/main.py`\n- **Alternative Implementation**: `/var/home/a/code/cowabungaai/packages/text-embeddings-tiny/main_tiny.py` (ONNX runtime)\n- **Database Storage**: Supabase PostgreSQL with pgvector extension\n\n---\n\n### 2.2 Audio Transcription Flow\n\n### **Description**:\nThis workflow handles audio file uploads and transcribes them to text using the Whisper model. It enables voice-to-text functionality for users who prefer audio input, expanding the system's accessibility and use cases. The workflow processes audio files, extracts speech content, and stores both the transcribed text and audio metadata for future reference.\n\n### **Flow Diagram**:\n```mermaid\ngraph TD\n    A[User Uploads Audio File] --> UI[Leptos SSR UI Layer]\n    UI --> API[API Gateway HTTP Endpoint]\n    API --> Validate[Request Validation]\n    Validate --> Whisper[Whisper Model Service]\n    Whisper --> Transcribe[Convert Audio to Text]\n    Transcribe --> Store[Store Transcribed Text & Metadata]\n    Store --> End[Return Transcription Result]\n    \n    style A fill:#e1f5e1\n    style End fill:#e1f5e1\n    style UI fill:#fff3cd\n    style API fill:#fff3cd\n    style Whisper fill:#f8d7da\n    style Store fill:#d1ecf1\n```\n\n### **Key Steps**:\n\n| Step | Component | Operation | Purpose |\n|------|-----------|-----------|---------|\n| 1 | User Interface Domain | User uploads audio file through UI | Capture audio input from user |\n| 2 | API Gateway Domain | API receives and validates audio upload request | Validate file format and size constraints |\n| 3 | AI Inference Domain | Whisper model transcribes audio to text | Process audio and extract speech content |\n| 4 | Data Persistence Domain | Store transcribed text and audio metadata | Persist transcription results for retrieval |\n\n---\n\n### 2.3 Model Management and Deployment Flow\n\n### **Description**:\nThis workflow manages the deployment and configuration of AI inference models across different hardware configurations (CPU/GPU). It handles model loading, resource allocation, and service initialization to ensure optimal performance based on available infrastructure. This workflow is critical for system startup, model updates, and runtime configuration management.\n\n### **Flow Diagram**:\n```mermaid\ngraph TD\n    A[Deployment Initiation] --> Config[Load Configuration Files]\n    Config --> Bundle[Load UDS Bundle Manifest]\n    Bundle --> Check[Check Hardware Resources]\n    Check --> GPU{GPU Available?}\n    GPU -->|Yes| LoadGPU[Load GPU-Optimized Models]\n    GPU -->|No| LoadCPU[Load CPU-Optimized Models]\n    LoadGPU --> Init[Initialize Inference Services]\n    LoadCPU --> Init\n    Init --> Health[Run Health Checks]\n    Health --> Ready[Services Ready]\n    \n    style A fill:#e1f5e1\n    style Ready fill:#e1f5e1\n    style Config fill:#fff3cd\n    style Bundle fill:#fff3cd\n    style Check fill:#fff3cd\n    style GPU fill:#f8d7da\n    style LoadGPU fill:#d1ecf1\n    style LoadCPU fill:#d1ecf1\n```\n\n### **Key Steps**:\n\n| Step | Component | Operation | Purpose |\n|------|-----------|-----------|---------|\n| 1 | Infrastructure Domain | Load uds-config.yaml and uds-bundle.yaml | Read deployment configuration |\n| 2 | Infrastructure Domain | Check hardware resources (GPU/CPU) | Determine available compute resources |\n| 3 | AI Inference Domain | Initialize appropriate model backends | Load llama-cpp-python or vLLM based on hardware |\n| 4 | AI Inference Domain | Run health checks and readiness probes | Verify service availability |\n\n---\n\n## 3. Workflow Insights\n\n### **Key Observations About System Operational Patterns**:\n\n1. **Dual-Database Strategy**: The system employs a sophisticated dual-database architecture where Turso SQLite handles application-level data (conversations, messages) while Supabase PostgreSQL manages vector embeddings and complex queries. This separation optimizes performance for different use cases.\n\n2. **gRPC-Centric Inter-Service Communication**: The API Gateway Domain heavily relies on gRPC for backend service communication, particularly with the LLM Inference Domain. This pattern enables efficient, typed communication between microservices with low latency.\n\n3. **Streaming-First Design**: The Chat Completion Flow prioritizes streaming responses, allowing users to see partial results immediately rather than waiting for complete generation. This improves perceived performance and user experience.\n\n4. **Configuration-Driven Deployment**: The system uses comprehensive configuration files (uds-config.yaml, uds-bundle.yaml) to manage environment-specific settings, enabling flexible deployment across CPU and GPU environments without code changes.\n\n5. **Modular Service Architecture**: Each AI capability (LLM inference, embeddings, audio processing) is implemented as an independent service, allowing for scalability, independent testing, and technology diversity (Python for inference, Rust for API/UI).\n\n### **Potential Optimization Opportunities**:\n\n1. **Caching Layer**: Consider implementing a caching layer for frequently accessed embeddings or conversation contexts to reduce database load and improve response times.\n\n2. **Connection Pooling**: The database adapter could benefit from connection pooling to handle concurrent requests more efficiently, especially during peak usage periods.\n\n3. **Async Processing Pipeline**: The audio transcription workflow could be optimized with async task queues to handle multiple uploads concurrently without blocking the main API thread.\n\n4. **Model Warm-Up**: Implement model warm-up procedures during deployment to reduce initial latency when services first start processing requests.\n\n5. **Health Check Aggregation**: Consolidate health checks across services to provide a unified system health view for monitoring and alerting.\n\n### **Dependencies Between Workflows**:\n\n```mermaid\ngraph LR\n    A[Chat Completion] -->|Uses| B[Text Embedding]\n    A -->|Uses| C[Data Persistence]\n    D[Audio Transcription] -->|Uses| C\n    D -->|Uses| E[AI Inference]\n    B -->|Uses| C\n    F[Model Deployment] -->|Enables| A\n    F -->|Enables| B\n    F -->|Enables| D\n    F -->|Enables| E\n    \n    style A fill:#e1f5e1\n    style D fill:#e1f5e1\n    style F fill:#f8d7da\n    style C fill:#d1ecf1\n```\n\n**Critical Dependencies**:\n- **Data Persistence Domain** is a shared dependency across all workflows, making it a critical component for system stability\n- **Model Deployment** must complete successfully before any user-facing workflows can function\n- **AI Inference Domain** serves as a common backend for both Chat Completion and Audio Transcription workflows\n\n### **System Boundary Considerations**:\n\nThe system boundaries clearly define what is included within CowabungaAI's scope:\n- **Included**: All Rust/Python microservices, Turso/Supabase databases, Kubernetes deployment manifests\n- **Excluded**: External LLM providers beyond TensorZero gateway, third-party vector databases, production Kubernetes infrastructure\n\nThis boundary ensures the system remains self-contained while leveraging external services only where necessary (TensorZero for model routing, Kubernetes for orchestration)."
```

### Code Insights Data
Code analysis results from preprocessing phase, including definitions of functions, classes, and modules.

```json
{
  "directory_insights": [
    {
      "file_count": 4,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "cowabunga-api",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "llama-cpp-python",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file acts as the primary deployment manifest for the standard CPU-only version of the application, linking to the API and llama-cpp-python packages.",
          "file_path": "/var/home/a/code/cowabungaai/bundles/dev/cpu/uds-bundle-full.yaml",
          "importance_score": 0.85,
          "interfaces": [],
          "name": "uds-bundle-full.yaml",
          "responsibilities": [
            "Define deployment packages for CPU-only environment",
            "Link to API and LLM model packages",
            "Set versioning and metadata for the bundle"
          ],
          "source_summary": "The file defines a UDSBundle resource with metadata and a list of packages to deploy, specifying paths and references for the API and chat model.",
          "summary": "Defines the complete CPU-only deployment bundle for CowabungaAI, including the API and LLM models."
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "turso",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "cowabunga-api",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file provides an alternative deployment configuration that substitutes the default database with Turso/libSQL, suitable for specific infrastructure requirements.",
          "file_path": "/var/home/a/code/cowabungaai/bundles/dev/cpu/uds-bundle-turso.yaml",
          "importance_score": 0.8,
          "interfaces": [],
          "name": "uds-bundle-turso.yaml",
          "responsibilities": [
            "Configure Turso database integration",
            "Define package overrides for specific environments",
            "Orchestrate deployment of API and models with database"
          ],
          "source_summary": "The file lists packages including Turso, the API, and overrides, establishing the dependency graph for a database-backed deployment.",
          "summary": "Defines a deployment bundle variant that includes the Turso database alongside the API and models."
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "cowabunga-api",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "llama-cpp-python",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file mirrors the content of uds-bundle-full.yaml, serving as a redundant or alternative entry point for the standard deployment configuration.",
          "file_path": "/var/home/a/code/cowabungaai/bundles/dev/cpu/uds-bundle.yaml",
          "importance_score": 0.75,
          "interfaces": [],
          "name": "uds-bundle.yaml",
          "responsibilities": [
            "Define standard deployment packages",
            "Provide alternative bundle entry point",
            "Specify CPU-only resource constraints"
          ],
          "source_summary": "Contains identical package definitions for the API and llama-cpp-python model, establishing the core deployment structure.",
          "summary": "A duplicate or alias of the full bundle configuration, defining the standard CPU deployment."
        },
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "This file holds critical runtime configuration including GPU settings (disabled for CPU-only), domain settings, and model specifications for the application.",
          "file_path": "/var/home/a/code/cowabungaai/bundles/dev/cpu/uds-config.yaml",
          "importance_score": 0.95,
          "interfaces": [],
          "name": "uds-config.yaml",
          "responsibilities": [
            "Define environment variables for deployment",
            "Set resource limits and GPU configurations",
            "Configure domain and subdomain settings"
          ],
          "source_summary": "The file defines variables for text embeddings, whisper, and cowabunga-ui, setting GPU limits to zero and specifying subdomains and model names.",
          "summary": "Central configuration file defining environment variables and resource limits for the deployment."
        }
      ],
      "importance_score": 0.9,
      "key_files": [
        "uds-bundle-full.yaml",
        "uds-config.yaml",
        "uds-bundle-turso.yaml",
        "uds-bundle.yaml"
      ],
      "name": "cpu",
      "path": "/var/home/a/code/cowabungaai/bundles/dev/cpu",
      "purpose": "other",
      "subdirectory_count": 0,
      "summary": "The 'cpu' directory serves as the central configuration hub for deploying the CowabungaAI application with CPU-only support. It contains UDS bundle definitions that orchestrate the deployment of the API, LLM models, and optional database components, alongside a configuration file that defines resource limits and environment variables for the deployment."
    },
    {
      "file_count": 2,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "This file acts as the manifest for the deployment bundle, linking local packages to their source paths and versions within the UDS ecosystem.",
          "file_path": "/var/home/a/code/cowabungaai/bundles/dev/gpu/uds-bundle.yaml",
          "importance_score": 0.85,
          "interfaces": [],
          "name": "uds-bundle.yaml",
          "responsibilities": [
            "Define deployment bundle metadata",
            "Specify package dependencies and paths",
            "Configure version references for components"
          ],
          "source_summary": "The file declares a UDSBundle named 'cowabungaai' and lists packages including 'cowabunga-api' and 'vllm', pointing to their respective paths in the parent directory structure.",
          "summary": "Defines the UDS bundle structure for the CowabungaAI project, specifying dependencies and paths for API and model packages."
        },
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "This configuration file controls resource allocation for GPU-enabled services, ensuring the correct runtime environment is available while allowing CPU fallback.",
          "file_path": "/var/home/a/code/cowabungaai/bundles/dev/gpu/uds-config.yaml",
          "importance_score": 0.8,
          "interfaces": [],
          "name": "uds-config.yaml",
          "responsibilities": [
            "Configure GPU runtime environment",
            "Set resource limits for AI models",
            "Define fallback behavior for CPU execution"
          ],
          "source_summary": "The file defines variables for 'text-embeddings', 'whisper', and 'vllm', setting 'gpu_runtime' to 'nvidia' and 'gpu_limit' to 0 to enable GPU support when limits are raised.",
          "summary": "Configures runtime variables for GPU acceleration, setting NVIDIA runtime classes and CPU fallback limits for AI models."
        }
      ],
      "importance_score": 0.75,
      "key_files": [
        "uds-bundle.yaml",
        "uds-config.yaml"
      ],
      "name": "gpu",
      "path": "/var/home/a/code/cowabungaai/bundles/dev/gpu",
      "purpose": "other",
      "subdirectory_count": 0,
      "summary": "The 'gpu' directory serves as a configuration hub for deploying GPU-accelerated AI services using the UDS (Unified Deployment System) framework. It contains two YAML files that define the bundle structure and runtime variables, specifically configuring NVIDIA GPU support for services like vLLM and Whisper while defaulting to CPU execution."
    },
    {
      "file_count": 2,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "This file acts as the primary deployment manifest, listing the specific software packages (cowabunga-api and llama-cpp-python) and their repository references required to build the application.",
          "file_path": "/var/home/a/code/cowabungaai/bundles/latest/cpu/uds-bundle.yaml",
          "importance_score": 0.95,
          "interfaces": [],
          "name": "uds-bundle.yaml",
          "responsibilities": [
            "Define deployment packages",
            "Specify repository references",
            "Set bundle versioning"
          ],
          "source_summary": "The file declares a UDSBundle with metadata and a list of packages. It references external repositories via ghcr.io for the API and LLM components.",
          "summary": "Defines the UDS bundle structure for CowabungaAI, specifying the API and LLM packages to be deployed."
        },
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "This file provides variable definitions for the deployment environment, allowing customization of GPU resources and network domains for the AI services.",
          "file_path": "/var/home/a/code/cowabungaai/bundles/latest/cpu/uds-config.yaml",
          "importance_score": 0.85,
          "interfaces": [],
          "name": "uds-config.yaml",
          "responsibilities": [
            "Configure GPU resources",
            "Set network domains",
            "Define UI subdomains"
          ],
          "source_summary": "The file defines variables for text embeddings, whisper, and cowabunga-ui. It includes settings for GPU runtime classes and limits, as well as subdomain and domain configurations.",
          "summary": "Configures runtime variables for the deployment, including GPU settings and domain configuration."
        }
      ],
      "importance_score": 0.9,
      "key_files": [
        "uds-bundle.yaml",
        "uds-config.yaml"
      ],
      "name": "cpu",
      "path": "/var/home/a/code/cowabungaai/bundles/latest/cpu",
      "purpose": "other",
      "subdirectory_count": 0,
      "summary": "The 'cpu' directory serves as the configuration hub for deploying the CowabungaAI application using UDS (Unified Deployment System). It contains two YAML files that define the software bundle dependencies and runtime environment variables, ensuring the correct deployment of the API and LLM components."
    },
    {
      "file_count": 2,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "This file acts as the primary deployment manifest, declaring the application identity and listing the required software packages from external repositories to be included in the deployment bundle.",
          "file_path": "/var/home/a/code/cowabungaai/bundles/latest/gpu/uds-bundle.yaml",
          "importance_score": 0.9,
          "interfaces": [],
          "name": "uds-bundle.yaml",
          "responsibilities": [
            "Define application identity and version",
            "Declare required software packages",
            "Specify package repository sources"
          ],
          "source_summary": "The file declares a UDSBundle named 'cowabungaai' and lists two packages: 'cowabunga-api' and 'vllm', both sourced from Defense Unicorns' package repositories with specific version references.",
          "summary": "Defines the UDS bundle structure for deploying the CowabungaAI application, specifying package repositories and versions."
        },
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "This configuration file controls the infrastructure behavior of the deployed services, specifically enabling NVIDIA GPU support and defining resource constraints for text embeddings, Whisper, and vLLM models.",
          "file_path": "/var/home/a/code/cowabungaai/bundles/latest/gpu/uds-config.yaml",
          "importance_score": 0.9,
          "interfaces": [],
          "name": "uds-config.yaml",
          "responsibilities": [
            "Configure GPU runtime environment",
            "Set resource limits for AI models",
            "Define fallback behavior for GPU unavailability"
          ],
          "source_summary": "The file defines variables for 'text-embeddings', 'whisper', and 'vllm', setting 'gpu_runtime' to 'nvidia' and 'gpu_limit' to 0 to ensure CPU fallback until GPU resources are provisioned.",
          "summary": "Configures runtime variables for GPU-enabled services, setting NVIDIA runtime classes and resource limits."
        }
      ],
      "importance_score": 0.85,
      "key_files": [
        "uds-bundle.yaml",
        "uds-config.yaml"
      ],
      "name": "gpu",
      "path": "/var/home/a/code/cowabungaai/bundles/latest/gpu",
      "purpose": "other",
      "subdirectory_count": 0,
      "summary": "The 'gpu' directory serves as the configuration hub for deploying GPU-accelerated AI services using the UDS (Unified Deployment System) framework. It contains two YAML files that define the bundle structure and runtime variables for services like CowabungaAI and vLLM, specifically managing GPU resource allocation and NVIDIA runtime settings."
    },
    {
      "file_count": 1,
      "file_insights": [
        {
          "code_purpose": "doc",
          "dependencies": [],
          "detailed_description": "This file is generated during Python package build/installation and contains essential metadata for package distribution and identification.",
          "file_path": "/var/home/a/code/cowabungaai/cowabungaai.egg-info/PKG-INFO",
          "importance_score": 0.15,
          "interfaces": [],
          "name": "PKG-INFO",
          "responsibilities": [
            "Store package metadata",
            "Enable package identification",
            "Provide license information",
            "Track version information"
          ],
          "source_summary": "Contains metadata fields including Metadata-Version 2.4, package name cowabungaai, version 0.14.0, summary describing OpenAI-like capabilities for secure local systems, author email, and Business Source License 1.1.",
          "summary": "Package metadata file containing version, license, author, and summary information for the cowabungaai Python package."
        }
      ],
      "importance_score": 0.15,
      "key_files": [
        "PKG-INFO"
      ],
      "name": "cowabungaai.egg-info",
      "path": "/var/home/a/code/cowabungaai/cowabungaai.egg-info",
      "purpose": "other",
      "subdirectory_count": 0,
      "summary": "This is a Python package metadata directory (egg-info) containing build artifacts and distribution information. The PKG-INFO file stores package metadata including version, license, author, and summary for the cowabungaai project."
    },
    {
      "file_count": 3,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": true,
              "line_number": null,
              "name": "cargo-chef",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "rust",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This Dockerfile implements a multi-stage build strategy with a planner stage for dependency planning and a builder stage for compiling dependencies. It uses cargo-chef to optimize Rust dependency compilation.",
          "file_path": "/var/home/a/code/cowabungaai/packages/api/Dockerfile",
          "importance_score": 0.65,
          "interfaces": [],
          "name": "Dockerfile",
          "responsibilities": [
            "Define Docker build stages for Rust project",
            "Manage dependency planning with cargo-chef",
            "Configure base image and build context",
            "Set up workspace dependency graph"
          ],
          "source_summary": "The file defines ARG LOCAL_VERSION, uses lukemathwalker/cargo-chef:0.1.71-rust-1.85-bookworm as the base image, copies Cargo.toml and Cargo.lock, and runs cargo chef prepare to generate recipe.json for dependency planning.",
          "summary": "Docker build configuration file that defines the multi-stage build process for the Rust application using cargo-chef for dependency management."
        },
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "This configuration file sets the image_version to 0.14.0 for the deployment package, using Zarf's package creation mechanism for containerized deployments.",
          "file_path": "/var/home/a/code/cowabungaai/packages/api/zarf-config.yaml",
          "importance_score": 0.45,
          "interfaces": [],
          "name": "zarf-config.yaml",
          "responsibilities": [
            "Define deployment image version",
            "Configure Zarf package settings",
            "Support automated version management"
          ],
          "source_summary": "The file contains a package configuration with create.set section that defines image_version as 0.14.0, marked with release-please version markers for automated version management.",
          "summary": "Zarf deployment configuration file that specifies the image version for container deployment."
        },
        {
          "code_purpose": "lib",
          "dependencies": [],
          "detailed_description": "This is a deployment artifact archive containing the cowabunga-api service package. It includes checksums, OCI layout files, and SBOM (Software Bill of Materials) data for the amd64 architecture.",
          "file_path": "/var/home/a/code/cowabungaai/packages/api/zarf-package-cowabunga-api-amd64-dev-upstream.tar.zst",
          "importance_score": 0.75,
          "interfaces": [],
          "name": "zarf-package-cowabunga-api-amd64-dev-upstream.tar.zst",
          "responsibilities": [
            "Store deployment artifacts for the API service",
            "Provide integrity verification through checksums",
            "Contain OCI container image layout data",
            "Include software bill of materials for compliance"
          ],
          "source_summary": "Archive contains checksums.txt, components/cowabunga-api.tar, images/blobs/sha256/, oci-layout, and sboms directories with integrity verification data.",
          "summary": "Compressed archive containing a Zarf package for the cowabunga-api service, including components, images, and SBOMs."
        },
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "This file serves as the primary configuration manifest for deploying the CowabungaAI API using Zarf package management. It defines package metadata including name, version, and description, along with configurable deployment variables.",
          "file_path": "/var/home/a/code/cowabungaai/packages/api/zarf.yaml",
          "importance_score": 0.75,
          "interfaces": [],
          "name": "zarf.yaml",
          "responsibilities": [
            "Define package deployment metadata",
            "Configure API exposure settings",
            "Set default embeddings model",
            "Manage version templating"
          ],
          "source_summary": "The file contains ZarfPackageConfig metadata with package name 'cowabunga-api', version template placeholder, constants for IMAGE_VERSION, and variables for EXPOSE_API and DEFAULT_EMBEDDINGS_MODEL configuration.",
          "summary": "Zarf package configuration file defining the CowabungaAI API deployment package with metadata, version constants, and deployment variables."
        }
      ],
      "importance_score": 0.6166666666666667,
      "key_files": [
        "Dockerfile",
        "zarf-config.yaml",
        "zarf-package-cowabunga-api-amd64-dev-upstream.tar.zst",
        "zarf.yaml"
      ],
      "name": "api",
      "path": "/var/home/a/code/cowabungaai/packages/api",
      "purpose": "api",
      "subdirectory_count": 4,
      "summary": "This directory contains multiple file groups. Key aspects: The api directory contains Docker build configuration and deployment configuration files for the Rust project. These files work together to define how the application container is built and deployed, with the Dockerfile handling the build process and zarf-config.yaml managing deployment settings. The 'api' directory appears to contain deployment artifacts and package files rather than source code. The single visible file is a compressed archive (tar.zst) containing a Zarf package for the cowabunga-api service, suggesting this directory stores build/deployment outputs. The directory likely serves as a container for API-related artifacts and may include configuration or infrastructure files in its subdirectories. The api directory contains deployment configuration files for the CowabungaAI API service using Zarf package management. It includes zarf.yaml which defines package metadata, version constants, and deployment variables for orchestrating the API infrastructure. The directory serves as the configuration layer for API deployment and orchestration."
    },
    {
      "file_count": 2,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "This file contains the core metadata for the Helm chart including apiVersion, name, and description. It identifies this as a library chart that provides utilities for the chart developer.",
          "file_path": "/var/home/a/code/cowabungaai/packages/api/chart/Chart.yaml",
          "importance_score": 0.7,
          "interfaces": [],
          "name": "Chart.yaml",
          "responsibilities": [
            "Define chart metadata",
            "Specify chart type (library)",
            "Provide versioning information"
          ],
          "source_summary": "Defines chart metadata with apiVersion v2, name 'api', and description about a Rust API shadowing OpenAI API specification. Includes library chart classification.",
          "summary": "Helm chart metadata file defining the chart name, version, and description for the api deployment."
        },
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "This file contains all configurable values for the Helm chart deployment including container image details, security context settings, and environment variables for the COWABUNGA application.",
          "file_path": "/var/home/a/code/cowabungaai/packages/api/chart/values.yaml",
          "importance_score": 0.75,
          "interfaces": [],
          "name": "values.yaml",
          "responsibilities": [
            "Configure container image",
            "Set security context",
            "Define environment variables",
            "Manage deployment parameters"
          ],
          "source_summary": "Configures api deployment with image from ghcr.io/defenseunicorns/cowabungaai/cowabunga-api tag 0.14.0, security context running as non-root user 65532 with dropped capabilities, and environment variables for logging and config paths.",
          "summary": "Helm chart values file containing deployment configuration for the api application including image, security, and environment settings."
        }
      ],
      "importance_score": 0.65,
      "key_files": [
        "Chart.yaml",
        "values.yaml"
      ],
      "name": "chart",
      "path": "/var/home/a/code/cowabungaai/packages/api/chart",
      "purpose": "other",
      "subdirectory_count": 1,
      "summary": "This is a Helm chart directory containing deployment configuration for a Rust API application that shadows the OpenAI API specification. The Chart.yaml defines chart metadata while values.yaml contains deployment configuration including image references, security settings, and environment variables."
    },
    {
      "file_count": 2,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.fullname",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.labels",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.selectorLabels",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "podSecurityContext",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "Defines a Kubernetes Job that runs database migration scripts when the application is deployed, using Helm template variables for customization including chart name, namespace, and image tags.",
          "file_path": "/var/home/a/code/cowabungaai/packages/api/chart/templates/migration-job.yaml",
          "importance_score": 0.7,
          "interfaces": [],
          "name": "migration-job.yaml",
          "responsibilities": [
            "Execute database migrations",
            "Manage deployment lifecycle",
            "Apply security context",
            "Use Helm template variables"
          ],
          "source_summary": "Creates a batch Job with security context, labels, and namespace configuration for running migrations with configurable image tags and namespace defaults.",
          "summary": "Kubernetes Job manifest for executing database migrations during deployment"
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.labels",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "Creates a dedicated Kubernetes namespace for the application with labels for resource organization and management, using Helm release namespace as default.",
          "file_path": "/var/home/a/code/cowabungaai/packages/api/chart/templates/namespace.yaml",
          "importance_score": 0.6,
          "interfaces": [],
          "name": "namespace.yaml",
          "responsibilities": [
            "Create isolated namespace",
            "Apply resource labels",
            "Manage deployment scope"
          ],
          "source_summary": "Defines a v1 Namespace resource with release namespace and chart labels for resource isolation and organization.",
          "summary": "Kubernetes Namespace manifest for isolating application resources"
        }
      ],
      "importance_score": 0.65,
      "key_files": [
        "migration-job.yaml",
        "namespace.yaml"
      ],
      "name": "templates",
      "path": "/var/home/a/code/cowabungaai/packages/api/chart/templates",
      "purpose": "other",
      "subdirectory_count": 1,
      "summary": "The templates directory contains Helm chart templates for Kubernetes deployments, including namespace creation and migration job execution. These files work together to define the infrastructure setup for the application, with the namespace providing the deployment context and the migration job handling database schema updates."
    },
    {
      "file_count": 4,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.fullname",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.labels",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.selectorLabels",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file defines the Kubernetes Deployment resource that controls the application pods, including replica count, update strategy, and pod template specifications.",
          "file_path": "/var/home/a/code/cowabungaai/packages/api/chart/templates/api/deployment.yaml",
          "importance_score": 0.85,
          "interfaces": [],
          "name": "deployment.yaml",
          "responsibilities": [
            "Define pod deployment configuration",
            "Manage replica count and scaling",
            "Configure deployment strategy",
            "Set pod labels and selectors"
          ],
          "source_summary": "Contains Deployment manifest with template variables for chart fullname, namespace, replica count, and strategy configuration using Helm templating syntax.",
          "summary": "Kubernetes Deployment manifest that defines how the API application pods are deployed and managed."
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.fullname",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.labels",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.selectorLabels",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file defines the Kubernetes Service that provides network access to the API, including OpenAPI documentation annotations for Zarf integration.",
          "file_path": "/var/home/a/code/cowabungaai/packages/api/chart/templates/api/service.yaml",
          "importance_score": 0.8,
          "interfaces": [],
          "name": "service.yaml",
          "responsibilities": [
            "Expose API service on network",
            "Configure HTTP port binding",
            "Provide OpenAPI documentation access",
            "Set service selector labels"
          ],
          "source_summary": "Contains Service manifest with HTTP port configuration, Zarf annotations for API documentation, and selector labels for pod targeting.",
          "summary": "Kubernetes Service manifest that exposes the API service for network access and documentation."
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.fullname",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.serviceAccountName",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.labels",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file defines the ServiceAccount for the application and Role-based access control rules for reading ConfigMaps and other resources.",
          "file_path": "/var/home/a/code/cowabungaai/packages/api/chart/templates/api/permissions.yaml",
          "importance_score": 0.75,
          "interfaces": [],
          "name": "permissions.yaml",
          "responsibilities": [
            "Create service account for pods",
            "Define RBAC permissions",
            "Configure ConfigMap read access",
            "Set namespace and labels"
          ],
          "source_summary": "Contains ServiceAccount and Role manifests with RBAC rules for ConfigMap access, using Helm templating for namespace and name generation.",
          "summary": "Kubernetes RBAC configuration defining ServiceAccount and Role for API access permissions."
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.fullname",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.labels",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "storage.enabled",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file defines storage for the application files, only created when storage is enabled in values configuration.",
          "file_path": "/var/home/a/code/cowabungaai/packages/api/chart/templates/api/pvc.yaml",
          "importance_score": 0.6,
          "interfaces": [],
          "name": "pvc.yaml",
          "responsibilities": [
            "Define persistent storage for application",
            "Configure storage access mode",
            "Set storage size requirements",
            "Support optional storage class"
          ],
          "source_summary": "Contains PersistentVolumeClaim manifest with storage size, access mode, and optional storage class configuration using Helm conditional templating.",
          "summary": "Kubernetes PersistentVolumeClaim manifest for application storage, conditionally enabled."
        }
      ],
      "importance_score": 0.75,
      "key_files": [
        "deployment.yaml",
        "service.yaml",
        "permissions.yaml",
        "pvc.yaml"
      ],
      "name": "api",
      "path": "/var/home/a/code/cowabungaai/packages/api/chart/templates/api",
      "purpose": "api",
      "subdirectory_count": 0,
      "summary": "This directory contains Kubernetes Helm chart manifests for deploying the CowabungaAI API service. The files work together to define the deployment configuration, service networking, storage, and security permissions for the application in a Kubernetes cluster."
    },
    {
      "file_count": 1,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "This file serves as the deployment configuration for the cowabunga-api-common Zarf package, specifying package metadata, required components, and chart deployment paths for Kubernetes infrastructure.",
          "file_path": "/var/home/a/code/cowabungaai/packages/api/common/zarf.yaml",
          "importance_score": 0.5,
          "interfaces": [],
          "name": "zarf.yaml",
          "responsibilities": [
            "Define package deployment metadata",
            "Specify component dependencies",
            "Configure chart deployment paths",
            "Set namespace for Kubernetes resources"
          ],
          "source_summary": "Contains YAML configuration with package metadata including name, version, and description. Defines a cowabunga-api component that references the cowabunga chart from the parent chart directory.",
          "summary": "Zarf package configuration file defining deployment metadata and components for the CowabungaAI API common package."
        }
      ],
      "importance_score": 0.5,
      "key_files": [
        "zarf.yaml"
      ],
      "name": "common",
      "path": "/var/home/a/code/cowabungaai/packages/api/common",
      "purpose": "other",
      "subdirectory_count": 0,
      "summary": "The common directory contains Zarf package configuration for the CowabungaAI API deployment infrastructure. The zarf.yaml file defines deployment metadata, components, and chart references for Kubernetes package management."
    },
    {
      "file_count": 8,
      "file_insights": [
        {
          "code_purpose": "database",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "storage.buckets",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This migration file establishes the foundational file storage schema by creating the file_objects table to store OpenAI File Objects and initializing a storage bucket in Supabase for file uploads.",
          "file_path": "/var/home/a/code/cowabungaai/packages/api/supabase/migrations/20240322174520_v0.7.2_api_sql_schema.sql",
          "importance_score": 0.75,
          "interfaces": [],
          "name": "20240322174520_v0.7.2_api_sql_schema.sql",
          "responsibilities": [
            "Create file_objects table schema",
            "Initialize storage bucket for files",
            "Support file upload functionality"
          ],
          "source_summary": "Creates a file_objects table with id, bytes, created_at, filename, object, purpose, status, and status_details columns. Inserts a storage bucket named 'file_bucket' with public access enabled.",
          "summary": "Initial migration creating file_objects table and storage bucket for file uploads"
        },
        {
          "code_purpose": "database",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "storage.buckets",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This migration introduces the core OpenAI object tables including assistants, messages, and runs with comprehensive indexing for efficient querying. It establishes the data model for conversation threads and AI assistant interactions.",
          "file_path": "/var/home/a/code/cowabungaai/packages/api/supabase/migrations/20240419164109_v0.8.0_openai_types.sql",
          "importance_score": 0.95,
          "interfaces": [],
          "name": "20240419164109_v0.8.0_openai_types.sql",
          "responsibilities": [
            "Define OpenAI object data models",
            "Create indexes for query performance",
            "Support conversation thread management"
          ],
          "source_summary": "Creates assistant_objects, message_objects, and run_objects tables with UUID primary keys, timestamps, and JSONB columns for metadata. Adds multiple indexes on user_id, thread_id, created_at, and id columns for query optimization.",
          "summary": "Major migration creating assistant_objects, message_objects, and run_objects tables with indexes"
        },
        {
          "code_purpose": "database",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "vector",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This migration enables vector search functionality by creating the vector_store, vector_store_file, and vector_content tables. It includes triggers for automatic usage tracking and a match_vectors function for vector similarity searches.",
          "file_path": "/var/home/a/code/cowabungaai/packages/api/supabase/migrations/20240502193159_v0.8.0_vector_stores.sql",
          "importance_score": 0.9,
          "interfaces": [
            {
              "description": null,
              "interface_type": "function",
              "name": "match_vectors",
              "parameters": [],
              "return_type": "unknown",
              "visibility": ""
            }
          ],
          "name": "20240502193159_v0.8.0_vector_stores.sql",
          "responsibilities": [
            "Enable vector search capabilities",
            "Track vector store usage",
            "Support embedding vector operations"
          ],
          "source_summary": "Enables pgvector extension and creates vector_store, vector_store_file, and vector_content tables. Implements triggers for calculating vector store file usage and a match_vectors function for vector matching operations.",
          "summary": "Creates vector_store tables with pgvector extension and triggers for embedding management"
        },
        {
          "code_purpose": "database",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "pgcrypto",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This migration establishes secure API key management by creating the api_keys table with hashed keys using pgcrypto. It enables row-level security and provides functions for key hashing and validation.",
          "file_path": "/var/home/a/code/cowabungaai/packages/api/supabase/migrations/20240618163044_v0.9.0_api_keys.sql",
          "importance_score": 0.85,
          "interfaces": [],
          "name": "20240618163044_v0.9.0_api_keys.sql",
          "responsibilities": [
            "Secure API key storage",
            "Hash API keys using pgcrypto",
            "Manage API key lifecycle"
          ],
          "source_summary": "Creates api_keys table with name, id, user_id, api_key_hash, created_at, expires_at, and checksum columns. Implements pgcrypto extension for secure hashing and enables row-level security on the table.",
          "summary": "Creates api_keys table with pgcrypto for secure API key hashing and management"
        },
        {
          "code_purpose": "database",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "api_keys",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This migration adds a row-level security policy that enables API key authentication for accessing storage.objects. It validates API keys against the api_keys table using cryptographic comparison.",
          "file_path": "/var/home/a/code/cowabungaai/packages/api/supabase/migrations/20240729193626_v0.10.0_api_keys_storage_objects.sql",
          "importance_score": 0.7,
          "interfaces": [],
          "name": "20240729193626_v0.10.0_api_keys_storage_objects.sql",
          "responsibilities": [
            "Enable API key authentication for storage",
            "Implement RLS policy for storage.objects",
            "Validate API keys cryptographically"
          ],
          "source_summary": "Creates a policy on storage.objects table that allows anonymous users to perform CRUD operations when authenticated via API key. The policy uses crypt() function to compare the request header with stored API key hashes.",
          "summary": "Creates RLS policy allowing API key authentication for storage.objects access"
        },
        {
          "code_purpose": "database",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "message_objects",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This migration fixes the metadata column in message_objects by setting a default empty JSONB object and making it non-nullable. It ensures data consistency across existing records.",
          "file_path": "/var/home/a/code/cowabungaai/packages/api/supabase/migrations/20240808164500_v10.0.0_metadata_defaults.sql",
          "importance_score": 0.5,
          "interfaces": [],
          "name": "20240808164500_v10.0.0_metadata_defaults.sql",
          "responsibilities": [
            "Fix metadata column nullability",
            "Set default metadata value",
            "Ensure data consistency"
          ],
          "source_summary": "Updates existing NULL metadata entries to empty JSONB object '{}'. Alters the metadata column to set default value and NOT NULL constraint for data integrity.",
          "summary": "Updates message_objects metadata column to have default empty object and NOT NULL constraint"
        },
        {
          "code_purpose": "database",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "vector_store_file",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This migration enhances the vector_store_file table by adding an updated_at timestamp column with automatic updates via trigger. It also creates an index on user_id for improved query performance.",
          "file_path": "/var/home/a/code/cowabungaai/packages/api/supabase/migrations/20240827103100_v0.12.0_indexing_status.sql",
          "importance_score": 0.65,
          "interfaces": [
            {
              "description": null,
              "interface_type": "function",
              "name": "update_modified_column",
              "parameters": [],
              "return_type": "unknown",
              "visibility": ""
            }
          ],
          "name": "20240827103100_v0.12.0_indexing_status.sql",
          "responsibilities": [
            "Track vector store file modifications",
            "Optimize user_id queries",
            "Maintain audit trail"
          ],
          "source_summary": "Adds updated_at column to vector_store_file table with UTC timestamp default. Creates index on user_id column and implements trigger function to automatically update the timestamp on row modifications.",
          "summary": "Adds updated_at column and trigger to vector_store_file with user_id index"
        },
        {
          "code_purpose": "database",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "file_objects",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This migration adds an updated_at timestamp column to file_objects table with automatic trigger updates. It also enables Supabase realtime publication for the table to support real-time updates.",
          "file_path": "/var/home/a/code/cowabungaai/packages/api/supabase/migrations/20240905094300_v0.12.0_file_status.sql",
          "importance_score": 0.6,
          "interfaces": [
            {
              "description": null,
              "interface_type": "trigger",
              "name": "update_file_objects_modtime",
              "parameters": [],
              "return_type": "unknown",
              "visibility": ""
            }
          ],
          "name": "20240905094300_v0.12.0_file_status.sql",
          "responsibilities": [
            "Track file object modifications",
            "Enable real-time updates",
            "Maintain audit trail"
          ],
          "source_summary": "Adds updated_at column to file_objects table with UTC timestamp default. Creates trigger to automatically update the timestamp on modifications and adds the table to supabase_realtime publication.",
          "summary": "Adds updated_at column and trigger to file_objects with Supabase realtime publication"
        }
      ],
      "importance_score": 0.95,
      "key_files": [
        "20240419164109_v0.8.0_openai_types.sql",
        "20240502193159_v0.8.0_vector_stores.sql",
        "20240618163044_v0.9.0_api_keys.sql"
      ],
      "name": "migrations",
      "path": "/var/home/a/code/cowabungaai/packages/api/supabase/migrations",
      "purpose": "database",
      "subdirectory_count": 0,
      "summary": "This migrations directory contains 8 SQL migration files that define and evolve the database schema for an OpenAI API integration system. The files collectively establish core tables for file storage, OpenAI objects (assistants, messages, runs), vector stores for embeddings, API key management, and associated triggers, indexes, and policies for data integrity and access control."
    },
    {
      "file_count": 2,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "This file defines deployment configuration for the API service using a private registry (registry1.dso.mil) with templated variables for customization during deployment.",
          "file_path": "/var/home/a/code/cowabungaai/packages/api/values/registry1-values.yaml",
          "importance_score": 0.65,
          "interfaces": [],
          "name": "registry1-values.yaml",
          "responsibilities": [
            "Define API image repository and tag",
            "Configure environment variables for the API service",
            "Set config paths and filenames",
            "Manage deployment exposure settings"
          ],
          "source_summary": "Contains image repository configuration, environment variables for logging, config paths, embeddings model, and deployment flags with templated placeholders for ZARF deployment system.",
          "summary": "Configuration file for deploying the CowabungaAI API using registry1 image repository with specific environment variables and settings."
        },
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "This file defines deployment configuration for the API service using the upstream public registry (ghcr.io) with templated variables for customization during deployment.",
          "file_path": "/var/home/a/code/cowabungaai/packages/api/values/upstream-values.yaml",
          "importance_score": 0.65,
          "interfaces": [],
          "name": "upstream-values.yaml",
          "responsibilities": [
            "Define API image repository and tag from upstream registry",
            "Configure environment variables for the API service",
            "Set config paths and filenames",
            "Manage deployment exposure settings",
            "Define port configuration for the service"
          ],
          "source_summary": "Contains image repository configuration pointing to ghcr.io, environment variables for logging, config paths, embeddings model, deployment flags, and includes a PORT environment variable setting.",
          "summary": "Configuration file for deploying the CowabungaAI API using upstream public image repository with similar environment variables and settings."
        }
      ],
      "importance_score": 0.65,
      "key_files": [
        "registry1-values.yaml",
        "upstream-values.yaml"
      ],
      "name": "values",
      "path": "/var/home/a/code/cowabungaai/packages/api/values",
      "purpose": "other",
      "subdirectory_count": 0,
      "summary": "This directory contains Helm chart values configuration files that define deployment settings for the CowabungaAI API service. The files work together to provide different deployment options (registry1 vs upstream) with environment variables, image repositories, and service exposure settings."
    },
    {
      "file_count": 2,
      "file_insights": [],
      "importance_score": 0.0,
      "key_files": [],
      "name": "k3d-gpu",
      "path": "/var/home/a/code/cowabungaai/packages/k3d-gpu",
      "purpose": "other",
      "subdirectory_count": 1,
      "summary": ""
    },
    {
      "file_count": 1,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "This file defines the Kubernetes RuntimeClass and DaemonSet required to deploy the NVIDIA device plugin on GPU-enabled nodes. It ensures GPU resources are properly exposed to pods.",
          "file_path": "/var/home/a/code/cowabungaai/packages/k3d-gpu/plugin/device-plugin-daemonset.yaml",
          "importance_score": 0.85,
          "interfaces": [],
          "name": "device-plugin-daemonset.yaml",
          "responsibilities": [
            "Define RuntimeClass for NVIDIA GPU runtime",
            "Deploy NVIDIA device plugin as DaemonSet",
            "Enable GPU passthrough on Kubernetes nodes",
            "Configure tolerations for node scheduling"
          ],
          "source_summary": "Contains two Kubernetes resource definitions: a RuntimeClass named 'nvidia' with handler 'nvidia', and a DaemonSet that deploys the NVIDIA device plugin across all nodes in the kube-system namespace.",
          "summary": "Kubernetes manifest for NVIDIA GPU device plugin deployment"
        }
      ],
      "importance_score": 0.75,
      "key_files": [
        "device-plugin-daemonset.yaml"
      ],
      "name": "plugin",
      "path": "/var/home/a/code/cowabungaai/packages/k3d-gpu/plugin",
      "purpose": "other",
      "subdirectory_count": 0,
      "summary": "This plugin directory contains Kubernetes configuration manifests for deploying the NVIDIA GPU device plugin. The single YAML file defines both a RuntimeClass and a DaemonSet to enable GPU passthrough on Kubernetes nodes."
    },
    {
      "file_count": 6,
      "file_insights": [
        {
          "code_purpose": "entry",
          "dependencies": [
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "llama_cpp",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "cowabunga_sdk",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": false,
              "line_number": null,
              "name": "logging",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": false,
              "line_number": null,
              "name": "os",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": false,
              "line_number": null,
              "name": "typing",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file serves as the primary entry point for the inference application, defining a Model class that wraps llama-cpp-python functionality with async token counting capabilities.",
          "file_path": "/var/home/a/code/cowabungaai/packages/llama-cpp-python/main.py",
          "importance_score": 0.95,
          "interfaces": [
            {
              "description": null,
              "interface_type": "async_function",
              "name": "count_tokens",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "raw_text",
                  "param_type": "str"
                }
              ],
              "return_type": "int",
              "visibility": ""
            }
          ],
          "name": "main.py",
          "responsibilities": [
            "Initialize LLM inference model",
            "Handle async token counting",
            "Manage backend configuration",
            "Log inference operations"
          ],
          "source_summary": "Imports logging, os, typing, and llama_cpp libraries. Defines a Model class decorated with @LLM that uses BackendConfig and LLM from cowabunga_sdk. Implements async token counting functionality.",
          "summary": "Main application entry point with Model class for LLM inference"
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "require",
              "is_external": true,
              "line_number": null,
              "name": "llama-cpp-python",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "require",
              "is_external": true,
              "line_number": null,
              "name": "cowabunga-sdk",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "require",
              "is_external": true,
              "line_number": null,
              "name": "huggingface_hub",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "Defines project metadata, dependencies, and Python version requirements for the llama-cpp-python wrapper package.",
          "file_path": "/var/home/a/code/cowabungaai/packages/llama-cpp-python/pyproject.toml",
          "importance_score": 0.8,
          "interfaces": [],
          "name": "pyproject.toml",
          "responsibilities": [
            "Define project metadata",
            "Manage package dependencies",
            "Specify Python version requirements",
            "Configure optional dev dependencies"
          ],
          "source_summary": "Specifies project name as lfai-llama-cpp-python with version 0.14.0. Lists llama-cpp-python 0.2.72 and cowabunga-sdk as dependencies. Requires Python 3.11 and includes dev dependencies for huggingface_hub.",
          "summary": "Python project configuration and dependency management"
        },
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "Contains model path, context length limits, stop tokens, prompt formatting, and inference parameters for the LLM.",
          "file_path": "/var/home/a/code/cowabungaai/packages/llama-cpp-python/config.yaml",
          "importance_score": 0.75,
          "interfaces": [],
          "name": "config.yaml",
          "responsibilities": [
            "Configure model file path",
            "Set context length limits",
            "Define stop token sequences",
            "Configure prompt formatting templates"
          ],
          "source_summary": "Defines model source path at /data/.model/model.gguf with max context length of 16384. Configures stop tokens including newline, end quote, and end-of-sentence markers. Sets prompt format for chat with system, assistant, and user templates.",
          "summary": "Runtime configuration for model inference settings"
        },
        {
          "code_purpose": "other",
          "dependencies": [],
          "detailed_description": "Multi-stage Dockerfile that builds a hardened Python environment with llama-cpp-python for containerized deployment.",
          "file_path": "/var/home/a/code/cowabungaai/packages/llama-cpp-python/Dockerfile",
          "importance_score": 0.7,
          "interfaces": [],
          "name": "Dockerfile",
          "responsibilities": [
            "Define multi-stage build process",
            "Configure Python virtual environment",
            "Set up hardened container image",
            "Prepare deployment artifacts"
          ],
          "source_summary": "Uses defenseunicorns/cowabunga-sdk as base SDK and leapfrogai/python:3.11-dev as builder image. Creates virtual environment and copies llama-cpp-python build artifacts for deployment.",
          "summary": "Container build configuration for the inference service"
        },
        {
          "code_purpose": "other",
          "dependencies": [],
          "detailed_description": "Provides installation and development targets for building and running the inference application.",
          "file_path": "/var/home/a/code/cowabungaai/packages/llama-cpp-python/Makefile",
          "importance_score": 0.65,
          "interfaces": [],
          "name": "Makefile",
          "responsibilities": [
            "Install package dependencies",
            "Run development CLI",
            "Manage editable installs",
            "Execute inference application"
          ],
          "source_summary": "Defines install target that installs cowabunga-sdk and the package in editable mode. Includes dev target to run the CLI application with main:Model entry point.",
          "summary": "Build and installation targets for the package"
        }
      ],
      "importance_score": 0.2833333333333333,
      "key_files": [
        "main.py",
        "pyproject.toml",
        "config.yaml",
        "Dockerfile",
        "Makefile"
      ],
      "name": "llama-cpp-python",
      "path": "/var/home/a/code/cowabungaai/packages/llama-cpp-python",
      "purpose": "other",
      "subdirectory_count": 3,
      "summary": "This directory contains a Python package wrapper around llama-cpp-python for LLM inference on CPU infrastructures. It includes the main application entry point (main.py), project configuration (pyproject.toml), runtime settings (config.yaml), and build artifacts (Dockerfile, Makefile) for containerization and installation."
    },
    {
      "file_count": 2,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "This file serves as the primary metadata definition for the Helm chart, specifying the chart name (cowabunga-model), description, and versioning information required for package management and deployment.",
          "file_path": "/var/home/a/code/cowabungaai/packages/llama-cpp-python/chart/Chart.yaml",
          "importance_score": 0.6,
          "interfaces": [],
          "name": "Chart.yaml",
          "responsibilities": [
            "Define chart metadata and versioning",
            "Specify chart type (application/library)",
            "Provide deployment package identification"
          ],
          "source_summary": "Contains Helm chart metadata including apiVersion, name, description, and chart type classification. Defines whether this is an application or library chart.",
          "summary": "Helm chart metadata file defining the chart name, version, and description for the llama-cpp-python inferencing backend deployment."
        },
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "This file contains all configurable deployment parameters including the container image repository, pull policy, version tag, environment variables, and pod security settings for the llama-cpp-python service.",
          "file_path": "/var/home/a/code/cowabungaai/packages/llama-cpp-python/chart/values.yaml",
          "importance_score": 0.65,
          "interfaces": [],
          "name": "values.yaml",
          "responsibilities": [
            "Configure container image deployment",
            "Set environment variables for the service",
            "Define pod security context and naming overrides"
          ],
          "source_summary": "Defines deployment configuration with image repository (ghcr.io/defenseunicorns/cowabungaai/llama-cpp-python), version tag (0.14.0), log level environment variable, and pod security context settings.",
          "summary": "Default configuration values for the Helm chart deployment including container image settings, environment variables, and pod security context."
        }
      ],
      "importance_score": 0.55,
      "key_files": [
        "Chart.yaml",
        "values.yaml"
      ],
      "name": "chart",
      "path": "/var/home/a/code/cowabungaai/packages/llama-cpp-python/chart",
      "purpose": "other",
      "subdirectory_count": 1,
      "summary": "This directory contains Helm chart configuration files for deploying a llama-cpp-python inferencing backend compatible with CowabungaAI. The Chart.yaml defines chart metadata and versioning while values.yaml provides deployment configuration including container image registry, version tags, and environment variables."
    },
    {
      "file_count": 4,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.fullname",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Release.Namespace",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file creates a Kubernetes ConfigMap that holds the models.toml configuration file, specifying the backend address and model ownership information for the gRPC service.",
          "file_path": "/var/home/a/code/cowabungaai/packages/llama-cpp-python/chart/templates/configmap.yaml",
          "importance_score": 0.75,
          "interfaces": [],
          "name": "configmap.yaml",
          "responsibilities": [
            "Store model configuration",
            "Define backend address",
            "Set model ownership metadata"
          ],
          "source_summary": "The file defines a ConfigMap resource with metadata including name, namespace, and labels. It contains a data section with models.toml configuration specifying the backend endpoint and model type.",
          "summary": "Defines a ConfigMap that stores model configuration data for the application."
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.fullname",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.labels",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.selectorLabels",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Values.replicaCount",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Values.strategy",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Values.podAnnotations",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file creates a Deployment manifest that manages the application pods, including replica count, update strategy, and pod template specifications for the gRPC service.",
          "file_path": "/var/home/a/code/cowabungaai/packages/llama-cpp-python/chart/templates/deployment.yaml",
          "importance_score": 0.9,
          "interfaces": [],
          "name": "deployment.yaml",
          "responsibilities": [
            "Manage pod lifecycle",
            "Configure replica count",
            "Define update strategy",
            "Set pod labels and annotations"
          ],
          "source_summary": "The file defines a Deployment with configurable replicas, strategy for updates, selector labels, and pod template metadata. It includes conditional blocks for strategy configuration and pod annotations.",
          "summary": "Defines the Kubernetes Deployment resource for running the application pods."
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Values.persistence.storageClass",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Values.persistence.accessModes",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Values.persistence.size",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file creates a PersistentVolumeClaim resource that provides persistent storage for the application, with configurable storage class, access modes, and size.",
          "file_path": "/var/home/a/code/cowabungaai/packages/llama-cpp-python/chart/templates/pvc.yaml",
          "importance_score": 0.7,
          "interfaces": [],
          "name": "pvc.yaml",
          "responsibilities": [
            "Provide persistent storage",
            "Configure storage class",
            "Set storage size and access modes"
          ],
          "source_summary": "The file defines a PVC with conditional storage class configuration, access modes, and storage size requests. It uses Helm template syntax to make storage configuration dynamic.",
          "summary": "Defines a PersistentVolumeClaim for storing application data persistently."
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.fullname",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.labels",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Values.service.type",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Values.service.port",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file creates a Service resource that exposes the application's gRPC endpoint on port 50051, with annotations for Zarf integration and configurable service type.",
          "file_path": "/var/home/a/code/cowabungaai/packages/llama-cpp-python/chart/templates/service.yaml",
          "importance_score": 0.85,
          "interfaces": [],
          "name": "service.yaml",
          "responsibilities": [
            "Expose gRPC endpoint",
            "Configure service type",
            "Set connection annotations",
            "Define port mappings"
          ],
          "source_summary": "The file defines a Service with metadata including Zarf connection annotations, labels, and port configuration. It specifies TCP protocol and targets port 50051 for gRPC communication.",
          "summary": "Defines a Kubernetes Service to expose the gRPC endpoint to other services."
        }
      ],
      "importance_score": 0.85,
      "key_files": [
        "deployment.yaml",
        "service.yaml",
        "configmap.yaml",
        "pvc.yaml"
      ],
      "name": "templates",
      "path": "/var/home/a/code/cowabungaai/packages/llama-cpp-python/chart/templates",
      "purpose": "other",
      "subdirectory_count": 0,
      "summary": "This directory contains Helm chart templates for deploying a gRPC service to Kubernetes. The files work together to define the complete deployment stack including configuration (ConfigMap), application pods (Deployment), persistent storage (PVC), and service exposure (Service)."
    },
    {
      "file_count": 1,
      "file_insights": [
        {
          "code_purpose": "util",
          "dependencies": [
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "huggingface_hub",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": false,
              "line_number": null,
              "name": "os",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This script provides functionality to download pre-trained AI models from Hugging Face Hub, with configurable parameters through environment variables including repository ID, filename, revision, checksum, and output path.",
          "file_path": "/var/home/a/code/cowabungaai/packages/llama-cpp-python/scripts/model_download.py",
          "importance_score": 0.7,
          "interfaces": [
            {
              "description": null,
              "interface_type": "function",
              "name": "download_model",
              "parameters": [],
              "return_type": "void",
              "visibility": ""
            }
          ],
          "name": "model_download.py",
          "responsibilities": [
            "Validates required environment variables are provided",
            "Downloads models from Hugging Face Hub",
            "Enables HF transfer for bandwidth optimization",
            "Handles model checksum verification"
          ],
          "source_summary": "The script defines a download_model() function that validates environment variables (REPO_ID, FILENAME, REVISION, CHECKSUM, OUTPUT_FILE) and uses huggingface_hub to download models with HF_HUB_ENABLE_HF_TRANSFER enabled for bandwidth optimization.",
          "summary": "Downloads AI models from Hugging Face Hub using environment variables for configuration"
        }
      ],
      "importance_score": 0.75,
      "key_files": [
        "model_download.py"
      ],
      "name": "scripts",
      "path": "/var/home/a/code/cowabungaai/packages/llama-cpp-python/scripts",
      "purpose": "tool",
      "subdirectory_count": 0,
      "summary": "This directory contains utility scripts for model management operations, specifically downloading AI models from Hugging Face Hub. The single file model_download.py provides infrastructure support for fetching pre-trained models with configurable parameters through environment variables."
    },
    {
      "file_count": 1,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "This YAML file serves as the upstream configuration template for deploying a machine learning inference service using Llama.cpp Python. It defines container image specifications and persistent volume claims for data storage.",
          "file_path": "/var/home/a/code/cowabungaai/packages/llama-cpp-python/values/upstream-values.yaml",
          "importance_score": 0.7,
          "interfaces": [],
          "name": "upstream-values.yaml",
          "responsibilities": [
            "Define container image repository and version",
            "Configure persistent volume claim settings",
            "Provide template variables for deployment customization"
          ],
          "source_summary": "The file contains three main sections: image configuration with repository and tag placeholders, and persistence settings including size, access modes, and storage class. Template variables marked with ###ZARF_### prefix indicate integration with ZARF deployment automation.",
          "summary": "Configuration file defining deployment parameters for a Llama.cpp Python container with persistent storage settings."
        }
      ],
      "importance_score": 0.65,
      "key_files": [
        "upstream-values.yaml"
      ],
      "name": "values",
      "path": "/var/home/a/code/cowabungaai/packages/llama-cpp-python/values",
      "purpose": "other",
      "subdirectory_count": 0,
      "summary": "This directory contains deployment configuration values for a Kubernetes-based application, specifically defining container image settings and persistent storage requirements. The single file uses template variables for parameterization, enabling flexible deployment configurations."
    },
    {
      "file_count": 7,
      "file_insights": [
        {
          "code_purpose": "service",
          "dependencies": [
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "cowabunga_sdk",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": false,
              "line_number": null,
              "name": "json",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": false,
              "line_number": null,
              "name": "logging",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": false,
              "line_number": null,
              "name": "urllib.request",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "Main entry point for the LLM stub service that handles gRPC requests and proxies to TensorZero gateway for AI inference operations.",
          "file_path": "/var/home/a/code/cowabungaai/packages/llm-stub/main.py",
          "importance_score": 0.95,
          "interfaces": [
            {
              "description": null,
              "interface_type": "function",
              "name": "_tz_call",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "prompt",
                  "param_type": "str"
                }
              ],
              "return_type": "str",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "async_function",
              "name": "count_tokens",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "raw_text",
                  "param_type": "str"
                }
              ],
              "return_type": "int",
              "visibility": ""
            }
          ],
          "name": "main.py",
          "responsibilities": [
            "Handle gRPC LLM inference requests",
            "Proxy to TensorZero gateway",
            "Stream chat completion responses",
            "Manage token counting"
          ],
          "source_summary": "Defines Model class and _tz_call function for handling LLM requests, with async token counting and gRPC service implementation.",
          "summary": "Core LLM backend service implementing TensorZero-backed gRPC communication with chat completion streaming."
        },
        {
          "code_purpose": "util",
          "dependencies": [
            {
              "dependency_type": "import",
              "is_external": false,
              "line_number": null,
              "name": "socket",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": false,
              "line_number": null,
              "name": "threading",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "Simple TCP proxy implementation that listens on port 3000 and forwards connections to the upstream TensorZero gateway.",
          "file_path": "/var/home/a/code/cowabungaai/packages/llm-stub/tz-bridge-proxy.py",
          "importance_score": 0.8,
          "interfaces": [
            {
              "description": null,
              "interface_type": "function",
              "name": "pipe",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "src",
                  "param_type": "Any"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "dst",
                  "param_type": "Any"
                }
              ],
              "return_type": "None",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "function",
              "name": "handle",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "conn",
                  "param_type": "Any"
                }
              ],
              "return_type": "None",
              "visibility": ""
            }
          ],
          "name": "tz-bridge-proxy.py",
          "responsibilities": [
            "Forward TCP traffic to upstream gateway",
            "Manage socket connections",
            "Handle connection lifecycle"
          ],
          "source_summary": "Implements pipe function for data transfer between sockets and handle function for connection management.",
          "summary": "TCP proxy that forwards traffic between the LLM stub and the TensorZero gateway."
        },
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "Multi-stage Dockerfile that builds the SDK image with Python virtual environment and installs cowabunga_sdk and related dependencies.",
          "file_path": "/var/home/a/code/cowabungaai/packages/llm-stub/Dockerfile",
          "importance_score": 0.75,
          "interfaces": [],
          "name": "Dockerfile",
          "responsibilities": [
            "Build SDK image with dependencies",
            "Set up Python virtual environment",
            "Install required packages"
          ],
          "source_summary": "Defines builder stage with SDK base image, creates venv, and installs cowabunga_sdk with grpcio and protobuf dependencies.",
          "summary": "Docker build configuration for the SDK builder image with cowabunga_sdk dependencies."
        },
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "Simple Dockerfile that copies the proxy script and runs it as a Python application.",
          "file_path": "/var/home/a/code/cowabungaai/packages/llm-stub/Dockerfile.tz-bridge",
          "importance_score": 0.7,
          "interfaces": [],
          "name": "Dockerfile.tz-bridge",
          "responsibilities": [
            "Containerize the TCP proxy",
            "Provide runtime environment for proxy"
          ],
          "source_summary": "Uses python:3.11-slim base, copies proxy.py to /app, and runs it with python command.",
          "summary": "Dockerfile for the tz-bridge proxy container using Python slim base image."
        },
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "YAML configuration for chat prompt formatting with system/user/assistant roles and default token limits.",
          "file_path": "/var/home/a/code/cowabungaai/packages/llm-stub/config.yaml",
          "importance_score": 0.65,
          "interfaces": [],
          "name": "config.yaml",
          "responsibilities": [
            "Define prompt formatting templates",
            "Set default generation parameters"
          ],
          "source_summary": "Defines prompt_format for chat interactions with system/user/assistant templates and sets max_new_tokens to 128.",
          "summary": "Configuration file defining prompt formatting and default LLM parameters."
        },
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "Kubernetes Service and Deployment resources for the tensorzero-gw application in the cowabungaai namespace.",
          "file_path": "/var/home/a/code/cowabungaai/packages/llm-stub/tz-bridge-k8s.yaml",
          "importance_score": 0.7,
          "interfaces": [],
          "name": "tz-bridge-k8s.yaml",
          "responsibilities": [
            "Deploy TensorZero gateway service",
            "Configure Kubernetes networking",
            "Manage pod lifecycle"
          ],
          "source_summary": "Defines ClusterIP service on port 3000 and Deployment with single replica for the proxy container.",
          "summary": "Kubernetes manifests for deploying the TensorZero gateway service."
        },
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "Zarf package manifest that defines the llm-stub package with version templating and deployment instructions.",
          "file_path": "/var/home/a/code/cowabungaai/packages/llm-stub/zarf.yaml",
          "importance_score": 0.6,
          "interfaces": [],
          "name": "zarf.yaml",
          "responsibilities": [
            "Package llm-stub for Zarf deployment",
            "Manage image version templating",
            "Coordinate package installation"
          ],
          "source_summary": "Defines ZarfPackageConfig with IMAGE_VERSION template and references tz-bridge-k8s.yaml for workload deployment.",
          "summary": "Zarf package configuration for deploying the llm-stub as a containerized package."
        }
      ],
      "importance_score": 0.85,
      "key_files": [
        "main.py",
        "tz-bridge-proxy.py",
        "Dockerfile",
        "tz-bridge-k8s.yaml",
        "config.yaml"
      ],
      "name": "llm-stub",
      "path": "/var/home/a/code/cowabungaai/packages/llm-stub",
      "purpose": "other",
      "subdirectory_count": 0,
      "summary": "The llm-stub directory implements a TensorZero-backed LLM gRPC service for CowabungaAI, providing backend AI inference capabilities with proxy functionality. It includes Python service code, Docker build configurations, Kubernetes deployment manifests, and Zarf package configuration for containerized deployment."
    },
    {
      "file_count": 6,
      "file_insights": [
        {
          "code_purpose": "api",
          "dependencies": [
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "cowabunga_sdk",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": false,
              "line_number": null,
              "name": "logging",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": false,
              "line_number": null,
              "name": "os",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": false,
              "line_number": null,
              "name": "typing",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file serves as the primary implementation for the repeater package, exposing multiple gRPC service interfaces including completion, embeddings, chat completion, audio, and token counting services.",
          "file_path": "/var/home/a/code/cowabungaai/packages/repeater/main.py",
          "importance_score": 0.85,
          "interfaces": [
            {
              "description": null,
              "interface_type": "async_function",
              "name": "count_tokens",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "raw_text",
                  "param_type": "str"
                }
              ],
              "return_type": "int",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "async_function",
              "name": "async_function",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "request",
                  "param_type": "Any"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "context",
                  "param_type": "Any"
                }
              ],
              "return_type": "Any",
              "visibility": ""
            }
          ],
          "name": "main.py",
          "responsibilities": [
            "Implement CompletionServiceServicer interface",
            "Implement EmbeddingsServiceServicer interface",
            "Implement ChatCompletionServiceServicer interface",
            "Handle audio and token counting requests"
          ],
          "source_summary": "Imports various service servicers from cowabunga_sdk and implements async functions for handling requests. Contains 14 functions and 1 class with moderate complexity.",
          "summary": "Main entry point implementing multiple service interfaces for the repeater pseudo-model."
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "require",
              "is_external": true,
              "line_number": null,
              "name": "cowabunga-sdk",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "require",
              "is_external": true,
              "line_number": null,
              "name": "setuptools",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "Defines the lfai-repeater package with version 0.14.0, specifies cowabunga-sdk as the only dependency, and configures build tools including pytest, ruff, and setuptools.",
          "file_path": "/var/home/a/code/cowabungaai/packages/repeater/pyproject.toml",
          "importance_score": 0.75,
          "interfaces": [],
          "name": "pyproject.toml",
          "responsibilities": [
            "Define package metadata and version",
            "Specify Python version requirements",
            "Configure build system and dependencies",
            "Set up testing and linting tools"
          ],
          "source_summary": "Contains project metadata including name, description, version, and Python version requirements. Configures pip-tools, pytest, ruff, and setuptools for development.",
          "summary": "Python project configuration defining package metadata, dependencies, and tool settings."
        },
        {
          "code_purpose": "lib",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": true,
              "line_number": null,
              "name": "defenseunicorns/cowabunga-sdk",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": true,
              "line_number": null,
              "name": "defenseunicorns/leapfrogai/python",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "Multi-stage Dockerfile that copies SDK from a base image and packages the repeater code, creating a slim Python development environment with virtual environment support.",
          "file_path": "/var/home/a/code/cowabungaai/packages/repeater/Dockerfile",
          "importance_score": 0.7,
          "interfaces": [],
          "name": "Dockerfile",
          "responsibilities": [
            "Define multi-stage build process",
            "Copy SDK from base image",
            "Include repeater package in final image",
            "Create lightweight Python development environment"
          ],
          "source_summary": "Uses two build stages: one for SDK extraction and one for the final Python development image. Copies packages and sets up virtual environment for portability.",
          "summary": "Container build configuration for creating a hardened Python development environment."
        },
        {
          "code_purpose": "util",
          "dependencies": [
            {
              "dependency_type": "require",
              "is_external": true,
              "line_number": null,
              "name": "pip",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "require",
              "is_external": true,
              "line_number": null,
              "name": "cowabunga_sdk",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "Provides install and dev targets for setting up the development environment, installing dependencies, and running the SDK CLI with the repeater application.",
          "file_path": "/var/home/a/code/cowabungaai/packages/repeater/Makefile",
          "importance_score": 0.6,
          "interfaces": [],
          "name": "Makefile",
          "responsibilities": [
            "Install cowabunga-sdk dependency",
            "Install repeater in editable mode",
            "Run development CLI with repeater app",
            "Set up development environment"
          ],
          "source_summary": "Defines two main targets: install for pip installation of dependencies and dev for development mode with CLI execution.",
          "summary": "Build automation targets for installing and developing the repeater package."
        },
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "Configuration file containing model source, context length limits, stop tokens, and prompt format definitions for chat interactions.",
          "file_path": "/var/home/a/code/cowabungaai/packages/repeater/config.yaml",
          "importance_score": 0.5,
          "interfaces": [],
          "name": "config.yaml",
          "responsibilities": [
            "Define model source location",
            "Set maximum context length limits",
            "Configure stop tokens for generation",
            "Define prompt format for chat interactions"
          ],
          "source_summary": "Defines model configuration with source path, maximum context length of 10 billion tokens, stop token, and prompt format for chat system/assistant/user roles.",
          "summary": "Configuration file for testing purposes with model and prompt settings."
        },
        {
          "code_purpose": "lib",
          "dependencies": [],
          "detailed_description": "This is a compressed tar archive containing the repeater deployment package with OCI layout files, image manifests, and SHA256 checksums for integrity verification.",
          "file_path": "/var/home/a/code/cowabungaai/packages/repeater/zarf-package-repeater-amd64-dev-upstream.tar.zst",
          "importance_score": 0.75,
          "interfaces": [],
          "name": "zarf-package-repeater-amd64-dev-upstream.tar.zst",
          "responsibilities": [
            "Store deployment artifacts for repeater component",
            "Provide OCI-compliant container image distribution",
            "Maintain integrity verification through checksums"
          ],
          "source_summary": "Binary archive file containing OCI-compliant container images, index.json manifest, oci-layout configuration, and checksums for the repeater component.",
          "summary": "Zarf package archive containing the repeater component deployment artifacts including OCI images and checksums."
        },
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "This file configures a Zarf package for deploying the repeater model to Kubernetes clusters. It specifies package metadata, version constants, and component dependencies for the deployment.",
          "file_path": "/var/home/a/code/cowabungaai/packages/repeater/zarf.yaml",
          "importance_score": 0.75,
          "interfaces": [],
          "name": "zarf.yaml",
          "responsibilities": [
            "Define package metadata and versioning",
            "Specify component dependencies",
            "Configure chart deployment paths",
            "Set namespace for chart deployment"
          ],
          "source_summary": "The file defines package metadata with name 'repeater', version template using ZARF_PKG_TMPL_IMAGE_VERSION, and constants for IMAGE_VERSION. It includes a required component named 'repeater' with an upstream flavor dependency on a chart in the cowabungaai namespace.",
          "summary": "Zarf package configuration file defining the repeater model deployment package."
        }
      ],
      "importance_score": 0.65,
      "key_files": [
        "main.py",
        "pyproject.toml",
        "Dockerfile",
        "Makefile",
        "config.yaml"
      ],
      "name": "repeater",
      "path": "/var/home/a/code/cowabungaai/packages/repeater",
      "purpose": "other",
      "subdirectory_count": 3,
      "summary": "This directory contains multiple file groups. Key aspects: This directory contains the lfai-repeater package, a Python-based API-compatible pseudo-model designed for testing purposes. It includes build infrastructure (Dockerfile, Makefile), project configuration (pyproject.toml), runtime settings (config.yaml), and the main entry point (main.py) that implements various service interfaces for testing the LeapfrogAI API. The repeater directory contains a Zarf package distribution artifact (zarf-package-repeater-amd64-dev-upstream.tar.zst) used for deploying the repeater component to Kubernetes environments. This is a binary archive file containing OCI-compliant container images and checksums for integrity verification, serving as a deployment package rather than source code. The repeater directory contains Zarf package configuration files for deploying a repeater model to Kubernetes. The zarf.yaml file defines the package metadata, version constants, and component dependencies for the repeater deployment. This directory serves as infrastructure configuration for package management and deployment."
    },
    {
      "file_count": 2,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "This file serves as the primary metadata definition for the Helm chart, specifying the chart identity, versioning, and type classification.",
          "file_path": "/var/home/a/code/cowabungaai/packages/repeater/chart/Chart.yaml",
          "importance_score": 0.65,
          "interfaces": [],
          "name": "Chart.yaml",
          "responsibilities": [
            "Define chart identity and versioning",
            "Specify chart type (application or library)",
            "Provide deployment metadata"
          ],
          "source_summary": "Defines chart metadata including apiVersion, name, description, and chart type classification for Helm package management.",
          "summary": "Helm chart metadata file defining the chart name, version, and description for the cowabunga-repeater application."
        },
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "This file contains all configurable parameters that can be overridden during chart deployment, controlling image selection and security policies.",
          "file_path": "/var/home/a/code/cowabungaai/packages/repeater/chart/values.yaml",
          "importance_score": 0.6,
          "interfaces": [],
          "name": "values.yaml",
          "responsibilities": [
            "Configure container image settings",
            "Define security context policies",
            "Provide deployment parameter defaults"
          ],
          "source_summary": "Defines deployment configuration including container image repository, tag, security contexts, and override parameters for the repeater service.",
          "summary": "Default configuration values for the Helm chart deployment including image registry, pull policy, and security context settings."
        }
      ],
      "importance_score": 0.55,
      "key_files": [
        "Chart.yaml",
        "values.yaml"
      ],
      "name": "chart",
      "path": "/var/home/a/code/cowabungaai/packages/repeater/chart",
      "purpose": "other",
      "subdirectory_count": 1,
      "summary": "This directory contains a Helm chart for deploying a CowabungaAI repeater service to Kubernetes. The Chart.yaml defines chart metadata and versioning while values.yaml provides configurable deployment parameters for the application."
    },
    {
      "file_count": 3,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.fullname",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Release.Namespace",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file defines a ConfigMap resource that stores configuration data for the application, specifically the models.toml file which contains model ownership and backend connection details.",
          "file_path": "/var/home/a/code/cowabungaai/packages/repeater/chart/templates/configmap.yaml",
          "importance_score": 0.65,
          "interfaces": [],
          "name": "configmap.yaml",
          "responsibilities": [
            "Store model configuration data",
            "Define backend connection details",
            "Provide configuration for the application"
          ],
          "source_summary": "The file creates a ConfigMap with a models.toml data key containing model configuration including ownership by Defense Unicorns, backend address, type as gRPC, and model name.",
          "summary": "Creates a Kubernetes ConfigMap containing models.toml configuration for the gRPC service"
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.fullname",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.labels",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.selectorLabels",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Values.replicaCount",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Values.strategy",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Values.podAnnotations",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file creates a Deployment manifest that manages the application pods with configurable replicas, update strategy, and pod specifications including labels and annotations.",
          "file_path": "/var/home/a/code/cowabungaai/packages/repeater/chart/templates/deployment.yaml",
          "importance_score": 0.85,
          "interfaces": [],
          "name": "deployment.yaml",
          "responsibilities": [
            "Manage application pod lifecycle",
            "Configure deployment strategy",
            "Define pod specifications and labels"
          ],
          "source_summary": "The deployment defines replica count, update strategy configuration, pod selector labels, and pod template metadata with annotations and labels for proper resource management.",
          "summary": "Defines the Kubernetes Deployment resource for running the application pods"
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.fullname",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.labels",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Values.nameOverride",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Values.service.type",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Values.service.port",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file creates a Service resource that exposes the application on port 50051 with gRPC protocol, including Zarf annotations for service discovery and connection metadata.",
          "file_path": "/var/home/a/code/cowabungaai/packages/repeater/chart/templates/service.yaml",
          "importance_score": 0.75,
          "interfaces": [],
          "name": "service.yaml",
          "responsibilities": [
            "Expose gRPC service endpoint",
            "Define service port and protocol",
            "Provide service discovery metadata"
          ],
          "source_summary": "The service defines the service type, port configuration with targetPort 50051, protocol TCP, and includes Zarf.dev annotations for connect-description and connect-name for service discovery.",
          "summary": "Defines the Kubernetes Service to expose the gRPC application endpoint"
        }
      ],
      "importance_score": 0.72,
      "key_files": [
        "deployment.yaml",
        "service.yaml",
        "configmap.yaml"
      ],
      "name": "templates",
      "path": "/var/home/a/code/cowabungaai/packages/repeater/chart/templates",
      "purpose": "other",
      "subdirectory_count": 0,
      "summary": "This templates directory contains Kubernetes Helm chart templates that define the infrastructure deployment for a gRPC service. The three YAML files work together to configure ConfigMaps, Deployments, and Services for the application, enabling container orchestration and service exposure."
    },
    {
      "file_count": 1,
      "file_insights": [
        {
          "code_purpose": "doc",
          "dependencies": [
            {
              "dependency_type": "require",
              "is_external": true,
              "line_number": null,
              "name": "cowabunga-sdk",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file contains metadata about the lfai-repeater package including its name, version, summary, Python version requirements, and dependencies. It is generated by setuptools during package installation.",
          "file_path": "/var/home/a/code/cowabungaai/packages/repeater/lfai_repeater.egg-info/PKG-INFO",
          "importance_score": 0.15,
          "interfaces": [],
          "name": "PKG-INFO",
          "responsibilities": [
            "Store package metadata for distribution",
            "Define Python version compatibility requirements",
            "List package dependencies",
            "Provide package description and summary"
          ],
          "source_summary": "Contains package metadata fields: Metadata-Version, Name, Version, Summary, Requires-Python, Description-Content-Type, and Requires-Dist. No executable code or logic.",
          "summary": "Package metadata file containing distribution information for the lfai-repeater Python package."
        }
      ],
      "importance_score": 0.15,
      "key_files": [
        "PKG-INFO"
      ],
      "name": "lfai_repeater.egg-info",
      "path": "/var/home/a/code/cowabungaai/packages/repeater/lfai_repeater.egg-info",
      "purpose": "other",
      "subdirectory_count": 0,
      "summary": "This directory contains Python package metadata generated during the build/installation process. The PKG-INFO file provides essential distribution information including package name, version, dependencies, and Python version requirements for the lfai-repeater package."
    },
    {
      "file_count": 1,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "Defines Kubernetes deployment parameters including container image references and persistent volume configurations with templated variables for deployment customization",
          "file_path": "/var/home/a/code/cowabungaai/packages/repeater/values/upstream-values.yaml",
          "importance_score": 0.7,
          "interfaces": [
            {
              "description": null,
              "interface_type": "configuration_key",
              "name": "image.repository",
              "parameters": [],
              "return_type": "string",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "configuration_key",
              "name": "image.tag",
              "parameters": [],
              "return_type": "string",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "configuration_key",
              "name": "persistence.size",
              "parameters": [],
              "return_type": "string",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "configuration_key",
              "name": "persistence.accessModes",
              "parameters": [],
              "return_type": "string",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "configuration_key",
              "name": "persistence.storageClass",
              "parameters": [],
              "return_type": "string",
              "visibility": ""
            }
          ],
          "name": "upstream-values.yaml",
          "responsibilities": [
            "Define container image repository and version",
            "Configure persistent volume storage settings",
            "Provide templated variables for deployment customization",
            "Specify PVC access modes and storage class"
          ],
          "source_summary": "Contains image repository and tag configuration, plus persistence settings for PVC size, access modes, and storage class with ZARF templating variables",
          "summary": "Kubernetes deployment configuration file with templated variables for infrastructure customization"
        }
      ],
      "importance_score": 0.65,
      "key_files": [
        "upstream-values.yaml"
      ],
      "name": "values",
      "path": "/var/home/a/code/cowabungaai/packages/repeater/values",
      "purpose": "other",
      "subdirectory_count": 0,
      "summary": "This directory contains Kubernetes deployment configuration values used for templating and customization of infrastructure deployments. The single YAML file defines image references, persistence settings, and templated variables for ZARF-based deployments."
    },
    {
      "file_count": 5,
      "file_insights": [
        {
          "code_purpose": "api",
          "dependencies": [
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "InstructorEmbedding",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "cowabunga_sdk",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": false,
              "line_number": null,
              "name": "asyncio",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": false,
              "line_number": null,
              "name": "logging",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": false,
              "line_number": null,
              "name": "os",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file implements the core text embedding service using InstructorEmbedding model. It provides async gRPC endpoints for generating embeddings from text requests and handles model loading from environment-configured paths.",
          "file_path": "/var/home/a/code/cowabungaai/packages/text-embeddings/main.py",
          "importance_score": 0.95,
          "interfaces": [
            {
              "description": null,
              "interface_type": "async_function",
              "name": "CreateEmbedding",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "request",
                  "param_type": "EmbeddingRequest"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "context",
                  "param_type": "GrpcContext"
                }
              ],
              "return_type": "EmbeddingResponse",
              "visibility": ""
            }
          ],
          "name": "main.py",
          "responsibilities": [
            "Load and initialize INSTRUCTOR embedding model",
            "Handle async gRPC embedding requests",
            "Generate text embeddings from input requests",
            "Configure logging and environment variables"
          ],
          "source_summary": "The file imports InstructorEmbedding and cowabunga_sdk, configures logging, loads the INSTRUCTOR model from environment variable, and implements async gRPC service methods for embedding requests.",
          "summary": "Main entry point for text embeddings service that implements gRPC API for embedding generation."
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "require",
              "is_external": true,
              "line_number": null,
              "name": "InstructorEmbedding",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "require",
              "is_external": true,
              "line_number": null,
              "name": "torch",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "require",
              "is_external": true,
              "line_number": null,
              "name": "numpy",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "require",
              "is_external": true,
              "line_number": null,
              "name": "tqdm",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "require",
              "is_external": true,
              "line_number": null,
              "name": "sentence-transformers",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "require",
              "is_external": true,
              "line_number": null,
              "name": "transformers",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "require",
              "is_external": true,
              "line_number": null,
              "name": "cowabunga-sdk",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file defines the project as lfai-text-embeddings with version 0.14.0. It specifies all required Python dependencies including InstructorEmbedding, torch, numpy, and other ML libraries, along with Python version requirements.",
          "file_path": "/var/home/a/code/cowabungaai/packages/text-embeddings/pyproject.toml",
          "importance_score": 0.85,
          "interfaces": [],
          "name": "pyproject.toml",
          "responsibilities": [
            "Define project metadata and version",
            "Specify Python package dependencies",
            "Set Python version compatibility requirements",
            "Configure project build and distribution settings"
          ],
          "source_summary": "The file contains project metadata including name, description, version, dependencies list, Python version requirement, and references to README documentation.",
          "summary": "Python project configuration file defining dependencies, version, and project metadata."
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": true,
              "line_number": null,
              "name": "defenseunicorns/cowabunga-sdk",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": true,
              "line_number": null,
              "name": "defenseunicorns/leapfrogai/python",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file defines a multi-stage Docker build with SDK and builder stages. It creates a hardened Python virtual environment, installs dependencies, and prepares the application for deployment with minimal footprint.",
          "file_path": "/var/home/a/code/cowabungaai/packages/text-embeddings/Dockerfile",
          "importance_score": 0.8,
          "interfaces": [],
          "name": "Dockerfile",
          "responsibilities": [
            "Define multi-stage Docker build process",
            "Create Python virtual environment",
            "Install application dependencies",
            "Configure SDK integration and deployment"
          ],
          "source_summary": "The Dockerfile uses two stages: SDK stage for building the cowabunga SDK, and builder stage that creates a Python virtual environment, installs dependencies, and prepares the application for production deployment.",
          "summary": "Multi-stage Docker build configuration for containerizing the text embeddings service."
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": true,
              "line_number": null,
              "name": "zarf",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file configures Zarf package deployment with GPU limits and image versioning. It enables declarative deployment of the text embeddings service with configurable runtime parameters.",
          "file_path": "/var/home/a/code/cowabungaai/packages/text-embeddings/zarf.yaml",
          "importance_score": 0.75,
          "interfaces": [],
          "name": "zarf.yaml",
          "responsibilities": [
            "Configure Zarf package deployment settings",
            "Define GPU resource limits for inference",
            "Manage image version templating",
            "Set deployment environment variables"
          ],
          "source_summary": "The file defines ZarfPackageConfig with metadata, constants for image version, and variables for GPU configuration including GPU limit and runtime settings.",
          "summary": "Zarf package configuration for deploying the text embeddings service in Kubernetes environments."
        },
        {
          "code_purpose": "util",
          "dependencies": [
            {
              "dependency_type": "require",
              "is_external": true,
              "line_number": null,
              "name": "pip",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "require",
              "is_external": true,
              "line_number": null,
              "name": "cowabunga_sdk",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file provides make targets for installing dependencies and running the service. It includes install, dev, and other targets for development workflow automation.",
          "file_path": "/var/home/a/code/cowabungaai/packages/text-embeddings/Makefile",
          "importance_score": 0.7,
          "interfaces": [],
          "name": "Makefile",
          "responsibilities": [
            "Install Python dependencies",
            "Run development mode with CLI",
            "Automate build and deployment workflows",
            "Provide quick start commands for developers"
          ],
          "source_summary": "The Makefile defines install target that pip installs cowabunga_sdk and development dependencies, and dev target that runs the service with CLI arguments.",
          "summary": "Build automation targets for installing and running the text embeddings service."
        }
      ],
      "importance_score": 0.85,
      "key_files": [
        "main.py",
        "pyproject.toml",
        "Dockerfile",
        "zarf.yaml",
        "Makefile"
      ],
      "name": "text-embeddings",
      "path": "/var/home/a/code/cowabungaai/packages/text-embeddings",
      "purpose": "other",
      "subdirectory_count": 3,
      "summary": "This directory contains a text embeddings library package that provides API-compatible embedding generation using InstructorEmbedding. It includes the main implementation (main.py), project configuration (pyproject.toml), build automation (Makefile), containerization (Dockerfile), and deployment configuration (zarf.yaml). The files work together to create a deployable text embedding service."
    },
    {
      "file_count": 2,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "This file serves as the primary metadata definition for the Helm chart, specifying the chart name, version, and type (application or library).",
          "file_path": "/var/home/a/code/cowabungaai/packages/text-embeddings/chart/Chart.yaml",
          "importance_score": 0.6,
          "interfaces": [],
          "name": "Chart.yaml",
          "responsibilities": [
            "Define chart metadata",
            "Specify chart type",
            "Set version information"
          ],
          "source_summary": "Contains Helm chart metadata including apiVersion, name, description, and chart type classification. Defines this as an application chart for deployment.",
          "summary": "Helm chart metadata file defining the chart name, version, and description for the CowabungaAI text-embeddings deployment."
        },
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "This file contains all configurable parameters for the Helm chart deployment, allowing customization of the Kubernetes deployment without modifying templates.",
          "file_path": "/var/home/a/code/cowabungaai/packages/text-embeddings/chart/values.yaml",
          "importance_score": 0.65,
          "interfaces": [],
          "name": "values.yaml",
          "responsibilities": [
            "Configure image registry",
            "Set environment variables",
            "Define pod security context",
            "Manage version overrides"
          ],
          "source_summary": "Defines image repository from ghcr.io/defenseunicorns, pull policy, version tag 0.14.0, environment variables for logging level, and pod security context settings.",
          "summary": "Default configuration values for the Helm chart including image registry, pull policy, version tags, and environment variables."
        }
      ],
      "importance_score": 0.55,
      "key_files": [
        "Chart.yaml",
        "values.yaml"
      ],
      "name": "chart",
      "path": "/var/home/a/code/cowabungaai/packages/text-embeddings/chart",
      "purpose": "other",
      "subdirectory_count": 1,
      "summary": "This directory contains a Helm chart for deploying a CowabungaAI text-embeddings inference backend to Kubernetes. The Chart.yaml defines chart metadata and the values.yaml provides configurable deployment parameters like image registry, tags, and environment variables."
    },
    {
      "file_count": 4,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.fullname",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Release.Namespace",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file creates a Kubernetes ConfigMap that holds the models.toml configuration file, specifying the backend address and model ownership information for the gRPC service.",
          "file_path": "/var/home/a/code/cowabungaai/packages/text-embeddings/chart/templates/configmap.yaml",
          "importance_score": 0.75,
          "interfaces": [],
          "name": "configmap.yaml",
          "responsibilities": [
            "Store model configuration",
            "Define backend address",
            "Set model ownership metadata"
          ],
          "source_summary": "The file defines a ConfigMap resource with metadata including name, namespace, and labels. It contains a data section with models.toml configuration specifying the backend endpoint and model type.",
          "summary": "Defines a ConfigMap that stores model configuration data for the application."
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.fullname",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.labels",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.selectorLabels",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Values.replicaCount",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Values.strategy",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Values.podAnnotations",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file creates a Deployment manifest that manages the application pods, including replica count, update strategy, and pod template specifications for the gRPC service.",
          "file_path": "/var/home/a/code/cowabungaai/packages/text-embeddings/chart/templates/deployment.yaml",
          "importance_score": 0.9,
          "interfaces": [],
          "name": "deployment.yaml",
          "responsibilities": [
            "Manage pod lifecycle",
            "Configure replica count",
            "Define update strategy",
            "Set pod labels and annotations"
          ],
          "source_summary": "The file defines a Deployment with configurable replicas, strategy for updates, selector labels, and pod template metadata. It includes conditional blocks for strategy configuration and pod annotations.",
          "summary": "Defines the Kubernetes Deployment resource for running the application pods."
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Values.persistence.storageClass",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Values.persistence.accessModes",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Values.persistence.size",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file creates a PersistentVolumeClaim resource that provides persistent storage for the application, with configurable storage class, access modes, and size.",
          "file_path": "/var/home/a/code/cowabungaai/packages/text-embeddings/chart/templates/pvc.yaml",
          "importance_score": 0.7,
          "interfaces": [],
          "name": "pvc.yaml",
          "responsibilities": [
            "Provide persistent storage",
            "Configure storage class",
            "Set storage size and access modes"
          ],
          "source_summary": "The file defines a PVC with conditional storage class configuration, access modes, and storage size requests. It uses Helm template syntax to make storage configuration dynamic.",
          "summary": "Defines a PersistentVolumeClaim for storing application data persistently."
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.fullname",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.labels",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Values.service.type",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Values.service.port",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file creates a Service resource that exposes the application's gRPC endpoint on port 50051, with annotations for Zarf integration and configurable service type.",
          "file_path": "/var/home/a/code/cowabungaai/packages/text-embeddings/chart/templates/service.yaml",
          "importance_score": 0.85,
          "interfaces": [],
          "name": "service.yaml",
          "responsibilities": [
            "Expose gRPC endpoint",
            "Configure service type",
            "Set connection annotations",
            "Define port mappings"
          ],
          "source_summary": "The file defines a Service with metadata including Zarf connection annotations, labels, and port configuration. It specifies TCP protocol and targets port 50051 for gRPC communication.",
          "summary": "Defines a Kubernetes Service to expose the gRPC endpoint to other services."
        }
      ],
      "importance_score": 0.85,
      "key_files": [
        "deployment.yaml",
        "service.yaml",
        "configmap.yaml",
        "pvc.yaml"
      ],
      "name": "templates",
      "path": "/var/home/a/code/cowabungaai/packages/text-embeddings/chart/templates",
      "purpose": "other",
      "subdirectory_count": 0,
      "summary": "This directory contains Helm chart templates for deploying a gRPC service to Kubernetes. The files work together to define the complete deployment stack including configuration (ConfigMap), application pods (Deployment), persistent storage (PVC), and service exposure (Service)."
    },
    {
      "file_count": 1,
      "file_insights": [
        {
          "code_purpose": "util",
          "dependencies": [
            {
              "dependency_type": "import",
              "is_external": false,
              "line_number": null,
              "name": "os",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": false,
              "line_number": null,
              "name": "time",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "huggingface_hub",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "A standalone utility script that downloads pre-trained models from Hugging Face Hub to the project environment, with configurable repository ID and revision, and includes retry logic for reliability.",
          "file_path": "/var/home/a/code/cowabungaai/packages/text-embeddings/scripts/model_download.py",
          "importance_score": 0.7,
          "interfaces": [],
          "name": "model_download.py",
          "responsibilities": [
            "Download models from Hugging Face Hub",
            "Handle environment variable configuration",
            "Manage retry logic for downloads",
            "Disable HF transfer for stability"
          ],
          "source_summary": "Imports os, time, and huggingface_hub modules; defines REPO_ID and REVISION environment variables; disables HF transfer by default for stability; includes retry logic for downloads.",
          "summary": "Utility script for downloading ML models from Hugging Face Hub with retry logic and environment configuration."
        }
      ],
      "importance_score": 0.65,
      "key_files": [
        "model_download.py"
      ],
      "name": "scripts",
      "path": "/var/home/a/code/cowabungaai/packages/text-embeddings/scripts",
      "purpose": "tool",
      "subdirectory_count": 0,
      "summary": "This is a scripts directory containing utility scripts for project setup and operations. The model_download.py file handles downloading ML models from Hugging Face Hub with retry logic and environment variable configuration for deployment."
    },
    {
      "file_count": 1,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "This file defines deployment parameters for a text embeddings service including container image, GPU runtime, resource limits, and persistent volume configuration. It uses template variables for ZARF deployment automation.",
          "file_path": "/var/home/a/code/cowabungaai/packages/text-embeddings/values/upstream-values.yaml",
          "importance_score": 0.75,
          "interfaces": [],
          "name": "upstream-values.yaml",
          "responsibilities": [
            "Define container image repository and version",
            "Configure GPU runtime and resource limits",
            "Set up persistent volume claims for data storage",
            "Provide template variables for deployment automation"
          ],
          "source_summary": "The file contains four main sections: image configuration with repository and version tag, GPU runtime settings, resource limits for NVIDIA GPUs, and persistence settings for PVC including size, access modes, and storage class.",
          "summary": "Kubernetes deployment configuration file with template variables for infrastructure deployment"
        }
      ],
      "importance_score": 0.65,
      "key_files": [
        "upstream-values.yaml"
      ],
      "name": "values",
      "path": "/var/home/a/code/cowabungaai/packages/text-embeddings/values",
      "purpose": "other",
      "subdirectory_count": 0,
      "summary": "This directory contains Kubernetes deployment configuration templates with parameterized values for infrastructure deployment. The single YAML file defines image repositories, GPU runtime settings, resource limits, and persistence configurations with template variables for ZARF deployment automation."
    },
    {
      "file_count": 4,
      "file_insights": [
        {
          "code_purpose": "service",
          "dependencies": [
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "onnxruntime",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "numpy",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "tokenizers",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "cowabunga_sdk",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file implements the core text embedding functionality with a TinyEmbedding class and CreateEmbedding gRPC service method. It uses ONNX runtime and tokenizers to process text inputs and generate embeddings without requiring PyTorch.",
          "file_path": "/var/home/a/code/cowabungaai/packages/text-embeddings-tiny/main_tiny.py",
          "importance_score": 0.95,
          "interfaces": [
            {
              "description": null,
              "interface_type": "function",
              "name": "_encode_batch",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "texts",
                  "param_type": "Any"
                }
              ],
              "return_type": "Any",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "async_function",
              "name": "CreateEmbedding",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "request",
                  "param_type": "EmbeddingRequest"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "context",
                  "param_type": "GrpcContext"
                }
              ],
              "return_type": "EmbeddingResponse",
              "visibility": ""
            }
          ],
          "name": "main_tiny.py",
          "responsibilities": [
            "Process text inputs and generate embeddings",
            "Serve embeddings via gRPC protocol",
            "Manage ONNX model inference",
            "Handle batch text encoding"
          ],
          "source_summary": "Defines TinyEmbedding class with _encode_batch method and CreateEmbedding async gRPC function. Imports onnxruntime, numpy, tokenizers, and cowabunga_sdk for serving embeddings.",
          "summary": "Main implementation file containing the TinyEmbedding class and gRPC service for text embeddings using ONNX runtime."
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "require",
              "is_external": true,
              "line_number": null,
              "name": "ghcr.io/defenseunicorns/cowabunga-sdk",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "require",
              "is_external": true,
              "line_number": null,
              "name": "ghcr.io/defenseunicorns/leapfrogai/python",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file defines the multi-stage Docker build process using a hardened Python base image. It creates a slim container image (~350MB) optimized for production deployment without PyTorch.",
          "file_path": "/var/home/a/code/cowabungaai/packages/text-embeddings-tiny/Dockerfile",
          "importance_score": 0.8,
          "interfaces": [],
          "name": "Dockerfile",
          "responsibilities": [
            "Define container build stages",
            "Configure Python environment",
            "Install ONNX runtime dependencies",
            "Optimize image size for production"
          ],
          "source_summary": "Uses multi-stage build with SDK and builder stages. Configures Python 3.11 virtual environment and installs ONNX runtime dependencies for the embedding service.",
          "summary": "Docker build configuration for creating a lightweight container image with ONNX runtime and Python dependencies."
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "require",
              "is_external": true,
              "line_number": null,
              "name": "onnxruntime",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "require",
              "is_external": true,
              "line_number": null,
              "name": "numpy",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "require",
              "is_external": true,
              "line_number": null,
              "name": "tokenizers",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "require",
              "is_external": true,
              "line_number": null,
              "name": "cowabunga-sdk",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file specifies the project name, version, dependencies, and Python version requirements. It defines the package as a lightweight ONNX MiniLM embeddings backend for CowabungaAI.",
          "file_path": "/var/home/a/code/cowabungaai/packages/text-embeddings-tiny/pyproject.toml",
          "importance_score": 0.75,
          "interfaces": [],
          "name": "pyproject.toml",
          "responsibilities": [
            "Define package metadata",
            "Specify runtime dependencies",
            "Configure Python version requirements",
            "Set up build tooling"
          ],
          "source_summary": "Defines project metadata including name, version 0.14.0, and dependencies like onnxruntime, numpy, tokenizers, and cowabunga-sdk. Configures Python 3.11 compatibility.",
          "summary": "Python project configuration file defining package metadata, dependencies, and build settings."
        },
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "This file configures the Zarf package deployment with template variables for image version and PVC size. It enables reproducible deployments with configurable storage requirements.",
          "file_path": "/var/home/a/code/cowabungaai/packages/text-embeddings-tiny/zarf.yaml",
          "importance_score": 0.7,
          "interfaces": [],
          "name": "zarf.yaml",
          "responsibilities": [
            "Configure Zarf package metadata",
            "Define deployment constants",
            "Set configurable variables",
            "Enable template-based deployment"
          ],
          "source_summary": "Defines ZarfPackageConfig with metadata, constants for image version, and variables for PVC size configuration. Supports template substitution for deployment flexibility.",
          "summary": "Zarf package configuration for deployment packaging with configurable constants and variables."
        }
      ],
      "importance_score": 0.85,
      "key_files": [
        "main_tiny.py",
        "Dockerfile",
        "pyproject.toml",
        "zarf.yaml"
      ],
      "name": "text-embeddings-tiny",
      "path": "/var/home/a/code/cowabungaai/packages/text-embeddings-tiny",
      "purpose": "other",
      "subdirectory_count": 3,
      "summary": "This directory contains a lightweight ONNX-based text embeddings backend for CowabungaAI, replacing torch-based implementations with ONNX MiniLM to reduce image size from ~5.75GB to ~350MB. The files work together to provide a production-ready embedding service with Docker build configuration, Python implementation, project metadata, and deployment packaging."
    },
    {
      "file_count": 2,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "This file defines the core metadata for the Helm chart including API version, chart name, description, and categorization as an application chart.",
          "file_path": "/var/home/a/code/cowabungaai/packages/text-embeddings-tiny/chart/Chart.yaml",
          "importance_score": 0.5,
          "interfaces": [],
          "name": "Chart.yaml",
          "responsibilities": [
            "Define chart metadata and versioning",
            "Specify chart type (application vs library)",
            "Provide chart description and categorization"
          ],
          "source_summary": "Contains Helm chart metadata including apiVersion v2, name text-embeddings-tiny, description for CowabungaAI compatible inferencing backend, and chart type classification.",
          "summary": "Helm chart metadata definition file that specifies chart name, version, and description for the text-embeddings-tiny deployment."
        },
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "This file contains configurable parameters for the chart deployment including container image settings, name overrides, and environment variable configurations.",
          "file_path": "/var/home/a/code/cowabungaai/packages/text-embeddings-tiny/chart/values.yaml",
          "importance_score": 0.5,
          "interfaces": [],
          "name": "values.yaml",
          "responsibilities": [
            "Define default deployment values",
            "Configure container image settings",
            "Set environment variables for the application",
            "Configure pod security context"
          ],
          "source_summary": "Defines image repository from ghcr.io/defenseunicorns, pull policy, version tag 0.14.0, name override, fullname override, log level environment variable, and pod security context settings.",
          "summary": "Default configuration values file for the Helm chart that defines deployment parameters including image registry, tag, and environment variables."
        }
      ],
      "importance_score": 0.45,
      "key_files": [
        "Chart.yaml",
        "values.yaml"
      ],
      "name": "chart",
      "path": "/var/home/a/code/cowabungaai/packages/text-embeddings-tiny/chart",
      "purpose": "other",
      "subdirectory_count": 1,
      "summary": "This directory contains a Helm chart for deploying a text-embeddings model inference backend compatible with CowabungaAI. The Chart.yaml defines chart metadata and versioning while values.yaml provides configurable deployment parameters for the Kubernetes deployment."
    },
    {
      "file_count": 4,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.fullname",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Release.Namespace",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file creates a Kubernetes ConfigMap that holds the models.toml configuration file, specifying the backend address and model ownership information for the gRPC service.",
          "file_path": "/var/home/a/code/cowabungaai/packages/text-embeddings-tiny/chart/templates/configmap.yaml",
          "importance_score": 0.75,
          "interfaces": [],
          "name": "configmap.yaml",
          "responsibilities": [
            "Store model configuration",
            "Define backend address",
            "Set model ownership metadata"
          ],
          "source_summary": "The file defines a ConfigMap resource with metadata including name, namespace, and labels. It contains a data section with models.toml configuration specifying the backend endpoint and model type.",
          "summary": "Defines a ConfigMap that stores model configuration data for the application."
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.fullname",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.labels",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.selectorLabels",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Values.replicaCount",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Values.strategy",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Values.podAnnotations",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file creates a Deployment manifest that manages the application pods, including replica count, update strategy, and pod template specifications for the gRPC service.",
          "file_path": "/var/home/a/code/cowabungaai/packages/text-embeddings-tiny/chart/templates/deployment.yaml",
          "importance_score": 0.9,
          "interfaces": [],
          "name": "deployment.yaml",
          "responsibilities": [
            "Manage pod lifecycle",
            "Configure replica count",
            "Define update strategy",
            "Set pod labels and annotations"
          ],
          "source_summary": "The file defines a Deployment with configurable replicas, strategy for updates, selector labels, and pod template metadata. It includes conditional blocks for strategy configuration and pod annotations.",
          "summary": "Defines the Kubernetes Deployment resource for running the application pods."
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Values.persistence.storageClass",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Values.persistence.accessModes",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Values.persistence.size",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file creates a PersistentVolumeClaim resource that provides persistent storage for the application, with configurable storage class, access modes, and size.",
          "file_path": "/var/home/a/code/cowabungaai/packages/text-embeddings-tiny/chart/templates/pvc.yaml",
          "importance_score": 0.7,
          "interfaces": [],
          "name": "pvc.yaml",
          "responsibilities": [
            "Provide persistent storage",
            "Configure storage class",
            "Set storage size and access modes"
          ],
          "source_summary": "The file defines a PVC with conditional storage class configuration, access modes, and storage size requests. It uses Helm template syntax to make storage configuration dynamic.",
          "summary": "Defines a PersistentVolumeClaim for storing application data persistently."
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.fullname",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.labels",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Values.service.type",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Values.service.port",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file creates a Service resource that exposes the application's gRPC endpoint on port 50051, with annotations for Zarf integration and configurable service type.",
          "file_path": "/var/home/a/code/cowabungaai/packages/text-embeddings-tiny/chart/templates/service.yaml",
          "importance_score": 0.85,
          "interfaces": [],
          "name": "service.yaml",
          "responsibilities": [
            "Expose gRPC endpoint",
            "Configure service type",
            "Set connection annotations",
            "Define port mappings"
          ],
          "source_summary": "The file defines a Service with metadata including Zarf connection annotations, labels, and port configuration. It specifies TCP protocol and targets port 50051 for gRPC communication.",
          "summary": "Defines a Kubernetes Service to expose the gRPC endpoint to other services."
        }
      ],
      "importance_score": 0.85,
      "key_files": [
        "deployment.yaml",
        "service.yaml",
        "configmap.yaml",
        "pvc.yaml"
      ],
      "name": "templates",
      "path": "/var/home/a/code/cowabungaai/packages/text-embeddings-tiny/chart/templates",
      "purpose": "other",
      "subdirectory_count": 0,
      "summary": "This directory contains Helm chart templates for deploying a gRPC service to Kubernetes. The files work together to define the complete deployment stack including configuration (ConfigMap), application pods (Deployment), persistent storage (PVC), and service exposure (Service)."
    },
    {
      "file_count": 1,
      "file_insights": [
        {
          "code_purpose": "util",
          "dependencies": [
            {
              "dependency_type": "import",
              "is_external": false,
              "line_number": null,
              "name": "os",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": false,
              "line_number": null,
              "name": "time",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "huggingface_hub",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This script downloads model files (tokenizer.json, config.json, model.onnx) from Hugging Face Hub repositories with configurable retry mechanisms and environment variable support.",
          "file_path": "/var/home/a/code/cowabungaai/packages/text-embeddings-tiny/scripts/model_download_tiny.py",
          "importance_score": 0.55,
          "interfaces": [],
          "name": "model_download_tiny.py",
          "responsibilities": [
            "Download model files from Hugging Face Hub",
            "Handle retry logic for failed downloads",
            "Manage environment configuration for repository settings",
            "Create destination directories for model files"
          ],
          "source_summary": "The script imports os, time, and huggingface_hub modules. It defines REPO_ID and REVISION environment variables with defaults, creates a destination directory, and implements a retry loop with MAX_RETRIES=5 for downloading model files.",
          "summary": "Utility script for downloading ML model files from Hugging Face Hub with retry logic and environment configuration."
        }
      ],
      "importance_score": 0.55,
      "key_files": [
        "model_download_tiny.py"
      ],
      "name": "scripts",
      "path": "/var/home/a/code/cowabungaai/packages/text-embeddings-tiny/scripts",
      "purpose": "tool",
      "subdirectory_count": 0,
      "summary": "The scripts directory contains utility scripts for infrastructure tasks, specifically model downloading operations. The single file model_download_tiny.py handles downloading ML model files from Hugging Face Hub with retry logic and environment configuration."
    },
    {
      "file_count": 1,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "Defines deployment parameters for the text-embeddings-tiny model including image registry, resource limits, and storage configuration with template variables for environment-specific customization",
          "file_path": "/var/home/a/code/cowabungaai/packages/text-embeddings-tiny/values/upstream-values.yaml",
          "importance_score": 0.6,
          "interfaces": [],
          "name": "upstream-values.yaml",
          "responsibilities": [
            "Define container image configuration",
            "Set resource limits and requests",
            "Configure GPU settings",
            "Define persistence storage"
          ],
          "source_summary": "Contains YAML configuration with image repository pointing to ghcr.io/defenseunicorns/cowabungaai, GPU runtime disabled, CPU/memory resource limits (500m/256Mi), and PVC persistence settings with ZARF template variables",
          "summary": "Helm/Kubernetes values configuration file for text embeddings model deployment"
        }
      ],
      "importance_score": 0.6,
      "key_files": [
        "upstream-values.yaml"
      ],
      "name": "values",
      "path": "/var/home/a/code/cowabungaai/packages/text-embeddings-tiny/values",
      "purpose": "other",
      "subdirectory_count": 0,
      "summary": "This directory contains Kubernetes/Helm deployment configuration values for a text embeddings model. The single YAML file defines container image settings, resource constraints, and storage persistence parameters with template variables for deployment customization."
    },
    {
      "file_count": 3,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "Defines the Docker container configuration including base image, dependencies, and directory structure for the Turso API service.",
          "file_path": "/var/home/a/code/cowabungaai/packages/turso/Dockerfile",
          "importance_score": 0.7,
          "interfaces": [],
          "name": "Dockerfile",
          "responsibilities": [
            "Define container base image",
            "Install system and Python dependencies",
            "Create non-root user for security",
            "Set up directory structure"
          ],
          "source_summary": "Uses python:3.11-slim as base image, installs sqlite3 and curl, installs Python dependencies (aiosqlite, fastapi, uvicorn), creates non-root user, and sets up directories for data, migrations, and scripts.",
          "summary": "Docker configuration file for containerizing the Turso SQLite API service"
        },
        {
          "code_purpose": "api",
          "dependencies": [
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "fastapi",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "aiosqlite",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "pydantic",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "Implements a FastAPI application that provides health check and query execution endpoints for the SQLite database.",
          "file_path": "/var/home/a/code/cowabungaai/packages/turso/api.py",
          "importance_score": 0.9,
          "interfaces": [
            {
              "description": null,
              "interface_type": "function",
              "name": "health",
              "parameters": [],
              "return_type": "dict",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "function",
              "name": "execute_query",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "request",
                  "param_type": "QueryRequest"
                }
              ],
              "return_type": "any",
              "visibility": ""
            }
          ],
          "name": "api.py",
          "responsibilities": [
            "Provide health check endpoint",
            "Handle SQL query requests",
            "Manage database connections",
            "Validate query parameters"
          ],
          "source_summary": "Creates a FastAPI app with a health check endpoint and a QueryRequest model for SQL query submissions. Uses aiosqlite for database connections.",
          "summary": "HTTP API implementation for Turso SQLite database operations"
        },
        {
          "code_purpose": "other",
          "dependencies": [],
          "detailed_description": "This is a binary archive file containing container image blobs in OCI (Open Container Initiative) format. It includes SHA256 checksums for integrity verification of the packaged images.",
          "file_path": "/var/home/a/code/cowabungaai/packages/turso/zarf-package-turso-amd64-dev-upstream.tar.zst",
          "importance_score": 0.45,
          "interfaces": [],
          "name": "zarf-package-turso-amd64-dev-upstream.tar.zst",
          "responsibilities": [
            "Store container image blobs",
            "Provide SHA256 checksums for integrity verification",
            "Enable deployment of Turso infrastructure components"
          ],
          "source_summary": "Binary archive file with OCI layout structure containing image blobs and their checksums. Not source code but deployment infrastructure artifact.",
          "summary": "Compressed tar archive containing OCI container image layout with SHA256 checksums for deployment artifacts."
        }
      ],
      "importance_score": 0.43333333333333335,
      "key_files": [
        "api.py",
        "Dockerfile",
        "zarf-package-turso-amd64-dev-upstream.tar.zst"
      ],
      "name": "turso",
      "path": "/var/home/a/code/cowabungaai/packages/turso",
      "purpose": "other",
      "subdirectory_count": 3,
      "summary": "This directory contains multiple file groups. Key aspects: The turso directory contains the core backend API service for a SQLite database implementation, providing HTTP endpoints for database operations. It includes a Dockerfile for containerization and an api.py file that exposes database query functionality through FastAPI. This directory contains deployment artifacts and container images for the Turso project. The files are compressed archives (tar.zst format) containing OCI layout files with SHA256 checksums for container image blobs, used for infrastructure deployment and distribution."
    },
    {
      "file_count": 2,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "This file contains the core metadata for the Helm chart including chart name, version, app version, keywords, home page, source URLs, and maintainer information.",
          "file_path": "/var/home/a/code/cowabungaai/packages/turso/chart/Chart.yaml",
          "importance_score": 0.75,
          "interfaces": [],
          "name": "Chart.yaml",
          "responsibilities": [
            "Define chart metadata and versioning",
            "Specify chart type and keywords",
            "List maintainer and source information"
          ],
          "source_summary": "Defines chart metadata with apiVersion v2, name turso, version 0.1.0, appVersion latest, keywords for turso/libSQL/database, home URL to CowabungaAI GitHub, source URL to Turso database GitHub, and maintainer info for CowabungaAI Team.",
          "summary": "Helm chart metadata file defining the Turso chart version, description, and maintainers."
        },
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "This file contains all configurable parameters for the Turso Helm chart deployment including replica count, image configuration, pull policies, and override settings.",
          "file_path": "/var/home/a/code/cowabungaai/packages/turso/chart/values.yaml",
          "importance_score": 0.7,
          "interfaces": [],
          "name": "values.yaml",
          "responsibilities": [
            "Define default deployment parameters",
            "Configure container image settings",
            "Provide override capability for deployments"
          ],
          "source_summary": "Contains deployment configuration with replicaCount set to 1, image repository from ghcr.io/tursodatabase/libsql-server with pinned digest and tag, imagePullSecrets array, and name/fullname override options.",
          "summary": "Default configuration values file for Helm chart deployment parameters."
        }
      ],
      "importance_score": 0.65,
      "key_files": [
        "Chart.yaml",
        "values.yaml"
      ],
      "name": "chart",
      "path": "/var/home/a/code/cowabungaai/packages/turso/chart",
      "purpose": "other",
      "subdirectory_count": 2,
      "summary": "This is a Helm chart directory for deploying Turso/libSQL database server to Kubernetes. It contains chart metadata (Chart.yaml) and default configuration values (values.yaml) that work together to define the deployment specifications for the CowabungaAI project."
    },
    {
      "file_count": 1,
      "file_insights": [
        {
          "code_purpose": "database",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "PRAGMA",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "users",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "conversations",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "files",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "messages",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file establishes the complete database structure including user authentication, conversation management, file storage, message history, vector embeddings, and audit logging tables.",
          "file_path": "/var/home/a/code/cowabungaai/packages/turso/chart/migrations/001_initial_schema.sql",
          "importance_score": 0.95,
          "interfaces": [
            {
              "description": null,
              "interface_type": "sql_table",
              "name": "users",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "id",
                  "param_type": "TEXT"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "email",
                  "param_type": "TEXT"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "encrypted_password",
                  "param_type": "TEXT"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "email_confirmed_at",
                  "param_type": "TIMESTAMP"
                }
              ],
              "return_type": "void",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "sql_table",
              "name": "conversations",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "id",
                  "param_type": "TEXT"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "user_id",
                  "param_type": "TEXT"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "title",
                  "param_type": "TEXT"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "model",
                  "param_type": "TEXT"
                }
              ],
              "return_type": "void",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "sql_table",
              "name": "files",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "id",
                  "param_type": "TEXT"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "user_id",
                  "param_type": "TEXT"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "filename",
                  "param_type": "TEXT"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "mime_type",
                  "param_type": "TEXT"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "size",
                  "param_type": "INTEGER"
                }
              ],
              "return_type": "void",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "sql_table",
              "name": "messages",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "id",
                  "param_type": "TEXT"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "conversation_id",
                  "param_type": "TEXT"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "role",
                  "param_type": "TEXT"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "content",
                  "param_type": "TEXT"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "tokens",
                  "param_type": "INTEGER"
                }
              ],
              "return_type": "void",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "sql_table",
              "name": "vector_store",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "id",
                  "param_type": "TEXT"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "vector_store_id",
                  "param_type": "TEXT"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "file_id",
                  "param_type": "TEXT"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "content",
                  "param_type": "TEXT"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "embedding",
                  "param_type": "F32_BLOB"
                }
              ],
              "return_type": "void",
              "visibility": ""
            }
          ],
          "name": "001_initial_schema.sql",
          "responsibilities": [
            "Define user authentication and profile tables",
            "Establish conversation and message storage structure",
            "Implement file upload and storage schema",
            "Create vector embedding storage for AI features",
            "Set up audit logging and configuration tables"
          ],
          "source_summary": "The file contains 446 lines of SQL code defining 19 interfaces including 18 table definitions and 1 view. Tables cover users, conversations, files, messages, vector stores, audit logs, and configuration storage.",
          "summary": "Initial database schema migration defining all core tables, triggers, and views for the CowabungaAI application."
        }
      ],
      "importance_score": 0.9,
      "key_files": [
        "001_initial_schema.sql"
      ],
      "name": "migrations",
      "path": "/var/home/a/code/cowabungaai/packages/turso/chart/migrations",
      "purpose": "database",
      "subdirectory_count": 0,
      "summary": "The migrations directory contains database schema definitions for the CowabungaAI application, specifically designed for Turso/libSQL (SQLite equivalent). This directory holds SQL migration files that establish the complete database structure including users, conversations, files, messages, and vector storage tables."
    },
    {
      "file_count": 7,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "turso.fullname",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "turso.labels",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This template generates a Kubernetes ConfigMap that stores database migration SQL files. It uses Helm's file globbing to include all SQL files from the migrations directory and injects them into the ConfigMap data.",
          "file_path": "/var/home/a/code/cowabungaai/packages/turso/chart/templates/configmap-migrations.yaml",
          "importance_score": 0.65,
          "interfaces": [],
          "name": "configmap-migrations.yaml",
          "responsibilities": [
            "Store database migration SQL files",
            "Enable migration execution via ConfigMap",
            "Support Helm file globbing for migrations"
          ],
          "source_summary": "The file uses Helm templating to create a ConfigMap resource that references migration SQL files via (.Files.Glob). It includes labels and metadata for proper resource identification.",
          "summary": "Creates a ConfigMap containing SQL migration files for database schema initialization."
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "turso.fullname",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "turso.labels",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "turso.selectorLabels",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This is the core deployment manifest that creates the application pods. It configures replica count, pod annotations, labels, and container specifications. The deployment is the primary workload resource in the Kubernetes cluster.",
          "file_path": "/var/home/a/code/cowabungaai/packages/turso/chart/templates/deployment.yaml",
          "importance_score": 0.85,
          "interfaces": [],
          "name": "deployment.yaml",
          "responsibilities": [
            "Define application pod specifications",
            "Configure replica count and scaling",
            "Manage pod labels and annotations",
            "Set up container runtime configuration"
          ],
          "source_summary": "The deployment template includes replica configuration, selector labels, pod annotations, and container specifications. It uses Helm values for customization and includes proper Kubernetes resource definitions.",
          "summary": "Defines the main Kubernetes Deployment for the Turso application with configurable replicas and pod specifications."
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "turso.fullname",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "turso.labels",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "turso.serviceAccountName",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This template defines a one-time Job resource that executes database migrations. It uses Helm hook annotations to ensure the job runs after installation or upgrade and is automatically cleaned up after completion.",
          "file_path": "/var/home/a/code/cowabungaai/packages/turso/chart/templates/migration-job.yaml",
          "importance_score": 0.75,
          "interfaces": [],
          "name": "migration-job.yaml",
          "responsibilities": [
            "Execute database migrations on install/upgrade",
            "Ensure migrations run as Helm hooks",
            "Configure service account for migration job",
            "Handle job cleanup after completion"
          ],
          "source_summary": "The job template includes Helm hook annotations for post-install and post-upgrade timing, service account configuration, and container specifications for running migrations. It uses a curl image for migration execution.",
          "summary": "Creates a Kubernetes Job to run database migrations with Helm hook annotations for post-install and post-upgrade execution."
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "turso.fullname",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "turso.labels",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This template generates a PersistentVolumeClaim resource for storing database data. It only creates the PVC when persistence is enabled and no existing claim is specified, using Helm values for storage configuration.",
          "file_path": "/var/home/a/code/cowabungaai/packages/turso/chart/templates/pvc.yaml",
          "importance_score": 0.7,
          "interfaces": [],
          "name": "pvc.yaml",
          "responsibilities": [
            "Provide persistent storage for database",
            "Support conditional PVC creation",
            "Configure storage class and access modes",
            "Manage storage resource requests"
          ],
          "source_summary": "The PVC template includes conditional logic based on persistence settings, storage class configuration, and access modes. It defines storage requests and proper Kubernetes resource specifications.",
          "summary": "Conditionally creates a PersistentVolumeClaim for database storage when persistence is enabled."
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "turso.fullname",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "turso.labels",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This template generates a Secret resource containing authentication tokens for the Turso service. It uses conditional logic to only create the secret when auth is enabled and no existing secret is specified.",
          "file_path": "/var/home/a/code/cowabungaai/packages/turso/chart/templates/secret.yaml",
          "importance_score": 0.68,
          "interfaces": [],
          "name": "secret.yaml",
          "responsibilities": [
            "Store authentication tokens securely",
            "Support conditional secret creation",
            "Manage token-based authentication",
            "Handle existing secret scenarios"
          ],
          "source_summary": "The secret template includes conditional logic for auth settings, token injection via stringData, and proper secret type configuration. It uses Helm values for token management.",
          "summary": "Creates a Kubernetes Secret for authentication tokens when Turso auth is enabled."
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "turso.fullname",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "turso.labels",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "turso.selectorLabels",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This template creates a Kubernetes Service that exposes the application pods. It configures service type, port mappings, and selector labels to route traffic to the deployment pods.",
          "file_path": "/var/home/a/code/cowabungaai/packages/turso/chart/templates/service.yaml",
          "importance_score": 0.8,
          "interfaces": [],
          "name": "service.yaml",
          "responsibilities": [
            "Expose application to network",
            "Configure service type and ports",
            "Route traffic to deployment pods",
            "Support different service types"
          ],
          "source_summary": "The service template includes service type configuration, port definitions with target ports, and proper selector labels. It uses Helm values for port and type customization.",
          "summary": "Defines the Kubernetes Service for exposing the Turso application to network traffic."
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "turso.serviceAccountName",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "turso.labels",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This template generates a ServiceAccount resource for the application pods. It includes optional annotations and uses Helm values for service account name configuration.",
          "file_path": "/var/home/a/code/cowabungaai/packages/turso/chart/templates/serviceaccount.yaml",
          "importance_score": 0.6,
          "interfaces": [],
          "name": "serviceaccount.yaml",
          "responsibilities": [
            "Provide service account for pods",
            "Support optional annotations",
            "Configure service account name",
            "Enable pod identity management"
          ],
          "source_summary": "The service account template includes name configuration, labels, and optional annotations. It uses Helm values for customization and proper Kubernetes resource specifications.",
          "summary": "Creates a Kubernetes ServiceAccount for the application with optional annotations."
        }
      ],
      "importance_score": 0.72,
      "key_files": [
        "deployment.yaml",
        "service.yaml",
        "migration-job.yaml"
      ],
      "name": "templates",
      "path": "/var/home/a/code/cowabungaai/packages/turso/chart/templates",
      "purpose": "other",
      "subdirectory_count": 0,
      "summary": "This directory contains Helm chart templates for deploying a Turso database application to Kubernetes. The files work together to define the complete deployment infrastructure including deployments, services, persistent storage, authentication secrets, and database migration jobs. All templates use Helm templating syntax to dynamically generate Kubernetes manifests based on values."
    },
    {
      "file_count": 1,
      "file_insights": [
        {
          "code_purpose": "database",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "PRAGMA",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "users",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "conversations",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "files",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "messages",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file establishes the complete database structure including user authentication, conversation management, file storage, message history, vector embeddings, and audit logging tables.",
          "file_path": "/var/home/a/code/cowabungaai/packages/turso/migrations/001_initial_schema.sql",
          "importance_score": 0.95,
          "interfaces": [
            {
              "description": null,
              "interface_type": "sql_table",
              "name": "users",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "id",
                  "param_type": "TEXT"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "email",
                  "param_type": "TEXT"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "encrypted_password",
                  "param_type": "TEXT"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "email_confirmed_at",
                  "param_type": "TIMESTAMP"
                }
              ],
              "return_type": "void",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "sql_table",
              "name": "conversations",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "id",
                  "param_type": "TEXT"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "user_id",
                  "param_type": "TEXT"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "title",
                  "param_type": "TEXT"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "model",
                  "param_type": "TEXT"
                }
              ],
              "return_type": "void",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "sql_table",
              "name": "files",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "id",
                  "param_type": "TEXT"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "user_id",
                  "param_type": "TEXT"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "filename",
                  "param_type": "TEXT"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "mime_type",
                  "param_type": "TEXT"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "size",
                  "param_type": "INTEGER"
                }
              ],
              "return_type": "void",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "sql_table",
              "name": "messages",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "id",
                  "param_type": "TEXT"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "conversation_id",
                  "param_type": "TEXT"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "role",
                  "param_type": "TEXT"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "content",
                  "param_type": "TEXT"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "tokens",
                  "param_type": "INTEGER"
                }
              ],
              "return_type": "void",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "sql_table",
              "name": "vector_store",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "id",
                  "param_type": "TEXT"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "vector_store_id",
                  "param_type": "TEXT"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "file_id",
                  "param_type": "TEXT"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "content",
                  "param_type": "TEXT"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "embedding",
                  "param_type": "F32_BLOB"
                }
              ],
              "return_type": "void",
              "visibility": ""
            }
          ],
          "name": "001_initial_schema.sql",
          "responsibilities": [
            "Define user authentication and profile tables",
            "Establish conversation and message storage structure",
            "Implement file upload and storage schema",
            "Create vector embedding storage for AI features",
            "Set up audit logging and configuration tables"
          ],
          "source_summary": "The file contains 446 lines of SQL code defining 19 interfaces including 18 table definitions and 1 view. Tables cover users, conversations, files, messages, vector stores, audit logs, and configuration storage.",
          "summary": "Initial database schema migration defining all core tables, triggers, and views for the CowabungaAI application."
        }
      ],
      "importance_score": 0.9,
      "key_files": [
        "001_initial_schema.sql"
      ],
      "name": "migrations",
      "path": "/var/home/a/code/cowabungaai/packages/turso/migrations",
      "purpose": "database",
      "subdirectory_count": 0,
      "summary": "The migrations directory contains database schema definitions for the CowabungaAI application, specifically designed for Turso/libSQL (SQLite equivalent). This directory holds SQL migration files that establish the complete database structure including users, conversations, files, messages, and vector storage tables."
    },
    {
      "file_count": 1,
      "file_insights": [
        {
          "code_purpose": "database",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "sqlite3",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "TURSO_DATABASE_PATH",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This script initializes the CowabungaAI database by checking if it exists, creating it if needed, and applying SQL migrations from the migrations directory to set up the database schema.",
          "file_path": "/var/home/a/code/cowabungaai/packages/turso/scripts/init-db.sh",
          "importance_score": 0.75,
          "interfaces": [
            {
              "description": null,
              "interface_type": "function",
              "name": "main",
              "parameters": [],
              "return_type": "void",
              "visibility": ""
            }
          ],
          "name": "init-db.sh",
          "responsibilities": [
            "Initialize database on first startup",
            "Apply SQL migrations",
            "Check database file existence",
            "Wait for database readiness"
          ],
          "source_summary": "The script waits for database readiness with a sleep command, checks for database file existence, creates it if missing using sqlite3, then iterates through SQL migration files to apply schema changes.",
          "summary": "Initializes the Turso database and applies migrations on first startup"
        }
      ],
      "importance_score": 0.65,
      "key_files": [
        "init-db.sh"
      ],
      "name": "scripts",
      "path": "/var/home/a/code/cowabungaai/packages/turso/scripts",
      "purpose": "tool",
      "subdirectory_count": 0,
      "summary": "This directory contains shell scripts for infrastructure setup and database initialization. The init-db.sh script handles database creation and migration application on first startup for the CowabungaAI application."
    },
    {
      "file_count": 2,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": true,
              "line_number": null,
              "name": "cargo-chef",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "rust",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This Dockerfile implements a multi-stage build strategy for Rust applications, separating dependency planning from compilation to optimize build times and reduce image sizes.",
          "file_path": "/var/home/a/code/cowabungaai/packages/ui/Dockerfile",
          "importance_score": 0.65,
          "interfaces": [],
          "name": "Dockerfile",
          "responsibilities": [
            "Define multi-stage Docker build for Rust project",
            "Capture workspace dependency graph using cargo-chef",
            "Cache compiled crates.io dependencies across builds",
            "Set up build context with Cargo.toml and Cargo.lock"
          ],
          "source_summary": "The file defines two build stages: a planner stage that captures the workspace dependency graph using cargo-chef, and a builder stage that compiles crates.io dependencies once and caches them across builds.",
          "summary": "Multi-stage Docker build configuration for Rust project using cargo-chef for dependency planning and caching."
        },
        {
          "code_purpose": "other",
          "dependencies": [],
          "detailed_description": "This is a Zarf package archive file that bundles UI components for distribution. It contains checksums for components, OCI layout files, and SBOMs for compliance tracking.",
          "file_path": "/var/home/a/code/cowabungaai/packages/ui/zarf-package-cowabunga-ui-amd64-dev-upstream.tar.zst",
          "importance_score": 0.3,
          "interfaces": [],
          "name": "zarf-package-cowabunga-ui-amd64-dev-upstream.tar.zst",
          "responsibilities": [
            "Package distribution for UI components",
            "Contains OCI layout and blob references",
            "Includes SBOM for security compliance",
            "Stores checksums for integrity verification"
          ],
          "source_summary": "Archive file containing tar.zst compressed data with embedded checksums for components/cowabunga-ui.tar, images/oci-layout, images/blobs/sha256/, sboms, and index.json.",
          "summary": "Compressed package archive containing UI components, OCI layout, and SBOMs for the cowabunga-ui application."
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "zarf",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file configures the Zarf package for deploying the CowabungaAI UI to Kubernetes clusters, defining package metadata, version constants, and deployment variables.",
          "file_path": "/var/home/a/code/cowabungaai/packages/ui/zarf.yaml",
          "importance_score": 0.65,
          "interfaces": [],
          "name": "zarf.yaml",
          "responsibilities": [
            "Define package metadata for Zarf deployment",
            "Set version constants for the UI package",
            "Configure API base URL for backend communication"
          ],
          "source_summary": "The file defines package metadata with name 'cowabunga-ui', sets IMAGE_VERSION constant, and configures COWABUNGA_API_BASE_URL variable with default cluster-local endpoint.",
          "summary": "Zarf package configuration file for the CowabungaAI UI deployment"
        }
      ],
      "importance_score": 0.46666666666666673,
      "key_files": [
        "Dockerfile",
        "zarf-package-cowabunga-ui-amd64-dev-upstream.tar.zst",
        "zarf.yaml"
      ],
      "name": "ui",
      "path": "/var/home/a/code/cowabungaai/packages/ui",
      "purpose": "frontend",
      "subdirectory_count": 2,
      "summary": "This directory contains multiple file groups. Key aspects: This directory contains Docker build configuration for a Rust project using cargo-chef for dependency management and multi-stage builds. The Dockerfile sets up a planner stage for dependency graph capture and a builder stage for compiling crates.io dependencies with caching. This directory contains a compressed package artifact (tar.zst) that serves as a distribution bundle for the cowabunga-ui component. The archive includes UI components, OCI layout files, blob checksums, and SBOMs, functioning as a build/distribution artifact rather than source code. This ui directory contains Zarf package configuration files for deploying the CowabungaAI UI application. The zarf.yaml file defines package metadata, version constants, and deployment variables for Kubernetes-native packaging and deployment."
    },
    {
      "file_count": 2,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "This file serves as the primary metadata definition for the Helm chart, specifying the chart name, version, description, and chart type (application or library).",
          "file_path": "/var/home/a/code/cowabungaai/packages/ui/chart/Chart.yaml",
          "importance_score": 0.75,
          "interfaces": [],
          "name": "Chart.yaml",
          "responsibilities": [
            "Define chart metadata",
            "Specify chart type",
            "Set version information"
          ],
          "source_summary": "Defines chart metadata including apiVersion, name, description, and chart type classification for Helm package management.",
          "summary": "Helm chart metadata file defining the chart name, version, and type for the cowabunga-ui application."
        },
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "This file provides all configurable values for the Helm chart deployment, including container image details, service configuration, security contexts, and environment variables.",
          "file_path": "/var/home/a/code/cowabungaai/packages/ui/chart/values.yaml",
          "importance_score": 0.8,
          "interfaces": [],
          "name": "values.yaml",
          "responsibilities": [
            "Configure container image settings",
            "Define service and port configuration",
            "Set security contexts and capabilities",
            "Manage environment variables"
          ],
          "source_summary": "Configures deployment parameters including image repository and tag, service port, service account settings, pod security context, security context with capability drops, and environment variables for API base URL.",
          "summary": "Helm chart values file containing deployment configuration for the cowabunga-ui application including image, service, and security settings."
        }
      ],
      "importance_score": 0.65,
      "key_files": [
        "Chart.yaml",
        "values.yaml"
      ],
      "name": "chart",
      "path": "/var/home/a/code/cowabungaai/packages/ui/chart",
      "purpose": "other",
      "subdirectory_count": 1,
      "summary": "This directory contains Helm chart configuration files for deploying the cowabunga-ui Svelte application to Kubernetes. The Chart.yaml defines chart metadata while values.yaml provides deployment configuration including image settings, service ports, and security contexts."
    },
    {
      "file_count": 2,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.fullname",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.labels",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.selectorLabels",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "podSecurityContext",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file defines a Kubernetes Job resource that runs database migrations when deployed. It uses Helm templating to inject chart-specific values and supports namespace configuration.",
          "file_path": "/var/home/a/code/cowabungaai/packages/ui/chart/templates/migration-job.yaml",
          "importance_score": 0.75,
          "interfaces": [],
          "name": "migration-job.yaml",
          "responsibilities": [
            "Define Kubernetes Job for database migrations",
            "Support Helm chart templating for deployment",
            "Configure pod security context for migrations",
            "Handle namespace and label inheritance from chart"
          ],
          "source_summary": "The file contains a Kubernetes Job specification with metadata including name templating, namespace defaults, and security context configuration for the migration container.",
          "summary": "Kubernetes Job template for executing database migrations with Helm chart templating support."
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "Release.Namespace",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.labels",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file creates a Kubernetes Namespace resource that provides isolation for the application deployment. It uses Helm templating to support namespace customization.",
          "file_path": "/var/home/a/code/cowabungaai/packages/ui/chart/templates/namespace.yaml",
          "importance_score": 0.55,
          "interfaces": [],
          "name": "namespace.yaml",
          "responsibilities": [
            "Create Kubernetes Namespace for deployment isolation",
            "Support Helm chart templating for namespace naming",
            "Apply chart labels to namespace metadata"
          ],
          "source_summary": "The file defines a v1 Namespace resource with metadata including name templating and label inheritance from the Helm chart.",
          "summary": "Kubernetes Namespace template for defining deployment isolation context."
        }
      ],
      "importance_score": 0.65,
      "key_files": [
        "migration-job.yaml",
        "namespace.yaml"
      ],
      "name": "templates",
      "path": "/var/home/a/code/cowabungaai/packages/ui/chart/templates",
      "purpose": "other",
      "subdirectory_count": 1,
      "summary": "This templates directory contains Helm chart templates for Kubernetes deployments, including a namespace definition and a migration job configuration. These files work together to define the infrastructure setup for the application, with the namespace providing the deployment context and the migration job handling database schema updates."
    },
    {
      "file_count": 3,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.fullname",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.labels",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.selectorLabels",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file configures the Kubernetes Deployment resource for the CowabungaAI UI application, specifying replica count, deployment strategy, pod template, and labels for service discovery.",
          "file_path": "/var/home/a/code/cowabungaai/packages/ui/chart/templates/ui/deployment.yaml",
          "importance_score": 0.75,
          "interfaces": [],
          "name": "deployment.yaml",
          "responsibilities": [
            "Define pod deployment configuration",
            "Manage replica count and scaling",
            "Configure deployment strategy",
            "Set pod labels and selectors"
          ],
          "source_summary": "Contains Helm template syntax with variables for namespace, replica count, and deployment strategy configuration. Uses chart template functions for labels and selectors.",
          "summary": "Kubernetes Deployment manifest that defines how the UI application pods are deployed and managed."
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.serviceAccountName",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.labels",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file creates a ServiceAccount resource for the UI application, enabling authentication and authorization within the Kubernetes cluster for the deployment.",
          "file_path": "/var/home/a/code/cowabungaai/packages/ui/chart/templates/ui/permissions.yaml",
          "importance_score": 0.6,
          "interfaces": [],
          "name": "permissions.yaml",
          "responsibilities": [
            "Define service account identity",
            "Configure namespace for the application",
            "Set application labels"
          ],
          "source_summary": "Defines a ServiceAccount with namespace configuration and labels. Uses Helm template functions for service account name generation.",
          "summary": "Kubernetes ServiceAccount manifest that defines identity and permissions for the UI application."
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.fullname",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.labels",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.selectorLabels",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file configures the Kubernetes Service resource to expose the UI application, including connection metadata for Zarf deployment integration.",
          "file_path": "/var/home/a/code/cowabungaai/packages/ui/chart/templates/ui/service.yaml",
          "importance_score": 0.7,
          "interfaces": [],
          "name": "service.yaml",
          "responsibilities": [
            "Expose application via Kubernetes Service",
            "Define service port configuration",
            "Set Zarf connection metadata",
            "Configure service selector labels"
          ],
          "source_summary": "Defines a Service with port configuration, selector labels, and Zarf-specific annotations for connection description and URL routing.",
          "summary": "Kubernetes Service manifest that exposes the UI application and defines connection metadata."
        }
      ],
      "importance_score": 0.65,
      "key_files": [
        "deployment.yaml",
        "service.yaml",
        "permissions.yaml"
      ],
      "name": "ui",
      "path": "/var/home/a/code/cowabungaai/packages/ui/chart/templates/ui",
      "purpose": "frontend",
      "subdirectory_count": 0,
      "summary": "This directory contains Kubernetes deployment manifests for the CowabungaAI UI application. The files work together to define the deployment configuration, service account permissions, and service exposure for the application in a Kubernetes environment."
    },
    {
      "file_count": 1,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "This YAML configuration file specifies the container image repository and tag, along with environment variables needed for the Cowabunga UI application deployment. It uses ZARF variable placeholders to enable dynamic configuration during deployment.",
          "file_path": "/var/home/a/code/cowabungaai/packages/ui/values/upstream-values.yaml",
          "importance_score": 0.75,
          "interfaces": [],
          "name": "upstream-values.yaml",
          "responsibilities": [
            "Define container image source and version",
            "Configure environment variables for application runtime",
            "Support dynamic deployment customization through ZARF variables",
            "Set up API and model configuration parameters"
          ],
          "source_summary": "The file defines image configuration with repository ghcr.io/defenseunicorns/cowabungaai/cowabunga-ui and tag placeholder, plus environment variables including COWABUNGA_API_BASE_URL, ORIGIN, DEFAULT_MODEL, DEFAULT_SYSTEM_PROMPT, DEFAULT_TEMPERATURE, and additional configuration parameters.",
          "summary": "Defines deployment configuration for Cowabunga UI including container image and environment variables"
        }
      ],
      "importance_score": 0.7,
      "key_files": [
        "upstream-values.yaml"
      ],
      "name": "values",
      "path": "/var/home/a/code/cowabungaai/packages/ui/values",
      "purpose": "other",
      "subdirectory_count": 0,
      "summary": "The values directory contains deployment configuration files for the Cowabunga UI application, specifically upstream-values.yaml which defines container image settings and environment variables. This file uses ZARF variable placeholders for dynamic deployment customization in Kubernetes/Helm deployments."
    },
    {
      "file_count": 6,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "nvidia/cuda",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "cowabunga-sdk",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "Multi-stage Dockerfile that builds the vLLM application using NVIDIA CUDA base image and custom SDK.",
          "file_path": "/var/home/a/code/cowabungaai/packages/vllm/Dockerfile",
          "importance_score": 0.8,
          "interfaces": [],
          "name": "Dockerfile",
          "responsibilities": [
            "Define Docker build stages",
            "Configure CUDA environment",
            "Set Python version and dependencies"
          ],
          "source_summary": "Contains two build stages: SDK stage using cowabunga-sdk and builder stage using nvidia/cuda base image with Python 3.11.9.",
          "summary": "Defines the Docker build process for the vLLM service with SDK and builder stages."
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "python",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "docker",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "Makefile providing common build targets for local development and containerized deployment workflows.",
          "file_path": "/var/home/a/code/cowabungaai/packages/vllm/Makefile",
          "importance_score": 0.75,
          "interfaces": [],
          "name": "Makefile",
          "responsibilities": [
            "Install Python dependencies",
            "Download model files",
            "Build Docker containers"
          ],
          "source_summary": "Defines targets for installing dependencies, downloading models, running in development mode, and building Docker images.",
          "summary": "Build automation script with targets for install, download, dev, and docker builds."
        },
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "YAML configuration file defining vLLM model inference settings including context length, stop tokens, and sampling parameters.",
          "file_path": "/var/home/a/code/cowabungaai/packages/vllm/config.yaml",
          "importance_score": 0.7,
          "interfaces": [],
          "name": "config.yaml",
          "responsibilities": [
            "Define model inference parameters",
            "Configure prompt formatting",
            "Set generation limits"
          ],
          "source_summary": "Contains model source path, max context length of 32768, stop tokens, prompt format templates, and generation defaults.",
          "summary": "Model inference configuration with context limits, stop tokens, and generation parameters."
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "require",
              "is_external": true,
              "line_number": null,
              "name": "pydantic",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "require",
              "is_external": true,
              "line_number": null,
              "name": "vllm",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "require",
              "is_external": true,
              "line_number": null,
              "name": "cowabunga-sdk",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "PyTorch project configuration file specifying package name, version, dependencies, and Python version requirements.",
          "file_path": "/var/home/a/code/cowabungaai/packages/vllm/pyproject.toml",
          "importance_score": 0.85,
          "interfaces": [],
          "name": "pyproject.toml",
          "responsibilities": [
            "Define project metadata",
            "Specify Python dependencies",
            "Set version requirements"
          ],
          "source_summary": "Defines project as lfai-vllm with version 0.14.0, lists core dependencies including vllm 0.4.3, and specifies Python 3.11 compatibility.",
          "summary": "Python project metadata defining dependencies and package configuration for the vLLM wrapper."
        },
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "Zarf deployment configuration specifying model repository ID, revision, and vLLM runtime parameters.",
          "file_path": "/var/home/a/code/cowabungaai/packages/vllm/zarf-config.yaml",
          "importance_score": 0.75,
          "interfaces": [],
          "name": "zarf-config.yaml",
          "responsibilities": [
            "Configure model repository",
            "Set deployment parameters",
            "Define runtime configuration"
          ],
          "source_summary": "Configures model deployment with TheBloke/Synthia-7B-v2.0-GPTQ model and sets runtime options like trust_remote_code and tensor_parallel_size.",
          "summary": "Zarf package configuration for deployment with model repository and runtime settings."
        },
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "Zarf package configuration file with metadata and templated constants for image version and model repository ID.",
          "file_path": "/var/home/a/code/cowabungaai/packages/vllm/zarf.yaml",
          "importance_score": 0.7,
          "interfaces": [],
          "name": "zarf.yaml",
          "responsibilities": [
            "Define package metadata",
            "Set templated constants",
            "Configure Zarf deployment"
          ],
          "source_summary": "Defines package metadata with name and version, includes templated constants for IMAGE_VERSION and MODEL_REPO_ID.",
          "summary": "Zarf package manifest defining package metadata and templated configuration constants."
        }
      ],
      "importance_score": 0.75,
      "key_files": [
        "pyproject.toml",
        "zarf.yaml",
        "Dockerfile",
        "config.yaml",
        "Makefile"
      ],
      "name": "vllm",
      "path": "/var/home/a/code/cowabungaai/packages/vllm",
      "purpose": "other",
      "subdirectory_count": 3,
      "summary": "The vllm directory serves as the configuration and deployment layer for a LeapfrogAI-compatible vLLM wrapper project. It contains build automation files (Dockerfile, Makefile), project metadata (pyproject.toml), and deployment configurations (zarf-config.yaml, zarf.yaml, config.yaml) that work together to define how the vLLM service is built, configured, and deployed."
    },
    {
      "file_count": 2,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "This file defines the CowabungaAI vLLM chart as an application chart with versioning and deployment metadata for Kubernetes.",
          "file_path": "/var/home/a/code/cowabungaai/packages/vllm/chart/Chart.yaml",
          "importance_score": 0.75,
          "interfaces": [],
          "name": "Chart.yaml",
          "responsibilities": [
            "Define chart metadata and versioning",
            "Specify chart type (application vs library)",
            "Declare chart dependencies"
          ],
          "source_summary": "Defines chart metadata including apiVersion, name, description, and chart type classification.",
          "summary": "Main Helm chart definition file that describes the chart metadata, version, and dependencies."
        },
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "This file provides default values for container image, model configuration, context length, and stop tokens for the vLLM inference backend.",
          "file_path": "/var/home/a/code/cowabungaai/packages/vllm/chart/values.yaml",
          "importance_score": 0.7,
          "interfaces": [],
          "name": "values.yaml",
          "responsibilities": [
            "Set default container image configuration",
            "Define model source and context parameters",
            "Configure stop tokens for inference"
          ],
          "source_summary": "Configures image repository, pull policy, tag, name overrides, and cowabungaaiConfig settings including model source and context length.",
          "summary": "Default configuration values file for the Helm chart that controls deployment parameters."
        }
      ],
      "importance_score": 0.65,
      "key_files": [
        "Chart.yaml",
        "values.yaml"
      ],
      "name": "chart",
      "path": "/var/home/a/code/cowabungaai/packages/vllm/chart",
      "purpose": "other",
      "subdirectory_count": 1,
      "summary": "This directory contains Helm chart configuration files for deploying the CowabungaAI vLLM model inference backend to Kubernetes. The Chart.yaml defines chart metadata, versioning, and dependencies, while values.yaml provides configurable deployment parameters for the vLLM container and model settings."
    },
    {
      "file_count": 6,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.fullname",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "Defines the models configuration that connects to the gRPC backend service, specifying ownership and backend address using Helm template variables.",
          "file_path": "/var/home/a/code/cowabungaai/packages/vllm/chart/templates/configmap.yaml",
          "importance_score": 0.7,
          "interfaces": [],
          "name": "configmap.yaml",
          "responsibilities": [
            "Define model configuration for the AI service",
            "Set backend gRPC connection address",
            "Manage model ownership metadata"
          ],
          "source_summary": "Contains a ConfigMap resource with models.toml data defining the AI model configuration with backend connection details.",
          "summary": "Creates a ConfigMap containing models.toml configuration for the AI service backend."
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.fullname",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.labels",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.selectorLabels",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "Core deployment configuration that manages pod lifecycle, replicas, and deployment strategy for the AI service application.",
          "file_path": "/var/home/a/code/cowabungaai/packages/vllm/chart/templates/deployment.yaml",
          "importance_score": 0.85,
          "interfaces": [],
          "name": "deployment.yaml",
          "responsibilities": [
            "Manage pod lifecycle and scaling",
            "Configure deployment strategy",
            "Define pod template specifications"
          ],
          "source_summary": "Defines a Deployment resource with configurable replicas, deployment strategy, and pod template specifications.",
          "summary": "Kubernetes Deployment manifest for running the AI service pods with configurable replicas and strategy."
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "cowabungaaiConfig",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "Provides SDK-specific configuration for the AI service including model source, maximum context length, and stop token settings.",
          "file_path": "/var/home/a/code/cowabungaai/packages/vllm/chart/templates/leapfrogai-sdk-configmap.yaml",
          "importance_score": 0.65,
          "interfaces": [],
          "name": "leapfrogai-sdk-configmap.yaml",
          "responsibilities": [
            "Configure SDK model source",
            "Set maximum context length",
            "Define stop tokens for model generation"
          ],
          "source_summary": "Contains SDK configuration with model source, max context length, and stop tokens from values configuration.",
          "summary": "ConfigMap for LeapFrogAI SDK configuration including model source, context length, and stop tokens."
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "persistence",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "Defines storage requirements for the AI service including storage class, access modes, and requested storage size.",
          "file_path": "/var/home/a/code/cowabungaai/packages/vllm/chart/templates/pvc.yaml",
          "importance_score": 0.6,
          "interfaces": [],
          "name": "pvc.yaml",
          "responsibilities": [
            "Allocate persistent storage",
            "Configure storage class",
            "Set storage access modes"
          ],
          "source_summary": "Creates a PersistentVolumeClaim with configurable storage class, access modes, and storage size from values.",
          "summary": "PersistentVolumeClaim for storage allocation to support persistent data storage for the service."
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.fullname",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.labels",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "Defines the network service that exposes the AI service gRPC endpoint with proper annotations and labels for service discovery.",
          "file_path": "/var/home/a/code/cowabungaai/packages/vllm/chart/templates/service.yaml",
          "importance_score": 0.8,
          "interfaces": [],
          "name": "service.yaml",
          "responsibilities": [
            "Expose gRPC endpoint externally",
            "Configure service port and protocol",
            "Enable service discovery with labels"
          ],
          "source_summary": "Creates a Service resource with gRPC port configuration, annotations for Zarf integration, and proper labeling.",
          "summary": "Kubernetes Service manifest exposing the gRPC endpoint on port 50051 for external access."
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "vllmConfig",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "Provides VLLM engine configuration parameters that control model serving behavior including parallelization and memory utilization.",
          "file_path": "/var/home/a/code/cowabungaai/packages/vllm/chart/templates/vllm-engine-configmap.yaml",
          "importance_score": 0.75,
          "interfaces": [],
          "name": "vllm-engine-configmap.yaml",
          "responsibilities": [
            "Configure VLLM engine parameters",
            "Set tensor parallelization",
            "Manage GPU memory utilization"
          ],
          "source_summary": "Contains VLLM engine configuration with trust remote code, tensor parallel size, eager enforcement, GPU memory utilization, and worker settings.",
          "summary": "ConfigMap for VLLM engine configuration including trust remote code, tensor parallel size, and GPU memory settings."
        }
      ],
      "importance_score": 0.75,
      "key_files": [
        "deployment.yaml",
        "service.yaml",
        "configmap.yaml",
        "vllm-engine-configmap.yaml",
        "leapfrogai-sdk-configmap.yaml"
      ],
      "name": "templates",
      "path": "/var/home/a/code/cowabungaai/packages/vllm/chart/templates",
      "purpose": "other",
      "subdirectory_count": 0,
      "summary": "This directory contains Helm chart templates for deploying a gRPC-based AI service on Kubernetes. The files work together to define the complete deployment infrastructure including ConfigMaps for configuration, Deployment for pod management, Service for networking, and PersistentVolumeClaim for storage."
    },
    {
      "file_count": 4,
      "file_insights": [
        {
          "code_purpose": "module",
          "dependencies": [],
          "detailed_description": "Standard Python package marker file with no implementation code. It enables the directory to be imported as a module.",
          "file_path": "/var/home/a/code/cowabungaai/packages/vllm/src/__init__.py",
          "importance_score": 0.1,
          "interfaces": [],
          "name": "__init__.py",
          "responsibilities": [
            "Define package boundaries",
            "Enable module imports"
          ],
          "source_summary": "File contains no source code, only serves as package marker.",
          "summary": "Empty package initialization file that makes this directory a Python package."
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "confz",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "pydantic",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "Defines four configuration classes (ConfigOptions, DownloadOptions, AppConfig, DownloadConfig) using pydantic and confz for environment variable support and validation.",
          "file_path": "/var/home/a/code/cowabungaai/packages/vllm/src/config.py",
          "importance_score": 0.85,
          "interfaces": [
            {
              "description": null,
              "interface_type": "class",
              "name": "ConfigOptions",
              "parameters": [],
              "return_type": "ConfigOptions",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "class",
              "name": "DownloadOptions",
              "parameters": [],
              "return_type": "DownloadOptions",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "class",
              "name": "AppConfig",
              "parameters": [],
              "return_type": "AppConfig",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "class",
              "name": "DownloadConfig",
              "parameters": [],
              "return_type": "DownloadConfig",
              "visibility": ""
            }
          ],
          "name": "config.py",
          "responsibilities": [
            "Define application configuration schema",
            "Support environment variable configuration",
            "Validate configuration values",
            "Provide download configuration options"
          ],
          "source_summary": "Contains 4 configuration classes with fields for tensor parallel size, quantization options, and download settings. Uses Field() for validation and metadata.",
          "summary": "Configuration management module with Pydantic-based config classes for application and download settings."
        },
        {
          "code_purpose": "entry",
          "dependencies": [
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "vllm",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": false,
              "line_number": null,
              "name": "config",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "cowabunga_sdk",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": false,
              "line_number": null,
              "name": "asyncio",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": false,
              "line_number": null,
              "name": "logging",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "Core application file that initializes vllm AsyncLLMEngine, handles model inference requests, and manages async iteration of outputs. Contains 26 functions and 2 classes with high complexity.",
          "file_path": "/var/home/a/code/cowabungaai/packages/vllm/src/main.py",
          "importance_score": 0.95,
          "interfaces": [
            {
              "description": null,
              "interface_type": "class",
              "name": "Model",
              "parameters": [],
              "return_type": "Model",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "method",
              "name": "is_queue_empty",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "request_id",
                  "param_type": "Any"
                }
              ],
              "return_type": "bool",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "async_function",
              "name": "count_tokens",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "raw_text",
                  "param_type": "str"
                }
              ],
              "return_type": "int",
              "visibility": ""
            }
          ],
          "name": "main.py",
          "responsibilities": [
            "Initialize vllm async engine",
            "Handle inference requests",
            "Manage async output iteration",
            "Token counting and queue management",
            "Application entry point"
          ],
          "source_summary": "Imports vllm components, config, and cowabunga_sdk. Defines Model class and async functions for token counting, queue management, and output iteration. Uses asyncio for async operations.",
          "summary": "Main application entry point with async LLM engine integration and request handling."
        },
        {
          "code_purpose": "util",
          "dependencies": [
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "huggingface_hub",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": false,
              "line_number": null,
              "name": "config",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "Provides model download functionality using huggingface_hub snapshot_download with support for environment-based allowlist filtering to optimize download size.",
          "file_path": "/var/home/a/code/cowabungaai/packages/vllm/src/model_download.py",
          "importance_score": 0.7,
          "interfaces": [],
          "name": "model_download.py",
          "responsibilities": [
            "Download models from HuggingFace",
            "Support allowlist filtering",
            "Read configuration for download settings",
            "Handle revision selection"
          ],
          "source_summary": "Uses huggingface_hub for snapshot downloads. Reads DownloadConfig for repo_id and revision. Supports GGUF allowlist via COWABUNGA_MODEL_ALLOW environment variable.",
          "summary": "Utility module for downloading models from HuggingFace with optional allowlist filtering."
        }
      ],
      "importance_score": 0.88,
      "key_files": [
        "main.py",
        "config.py",
        "model_download.py",
        "__init__.py"
      ],
      "name": "src",
      "path": "/var/home/a/code/cowabungaai/packages/vllm/src",
      "purpose": "core",
      "subdirectory_count": 0,
      "summary": "This is the core source directory containing the main application logic for a vllm-based AI inference service. It includes configuration management, main entry point with async LLM engine integration, and model download utilities. The files work together to provide a complete application that can download models from HuggingFace and run inference."
    },
    {
      "file_count": 1,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "This file serves as the primary configuration source for deploying the CowabungaAI vLLM service, containing image registry settings, deployment naming overrides, and model runtime parameters that are templated with ZARF variables.",
          "file_path": "/var/home/a/code/cowabungaai/packages/vllm/values/upstream-values.yaml",
          "importance_score": 0.75,
          "interfaces": [],
          "name": "upstream-values.yaml",
          "responsibilities": [
            "Define container image deployment settings",
            "Configure model runtime parameters",
            "Set prompt format templates for chat interactions",
            "Enable ZARF template variable substitution"
          ],
          "source_summary": "The file defines image repository and tag configuration, name override for deployment customization, and cowabungaaiConfig section with model source path, max context length, stop tokens, and prompt format settings for chat interactions.",
          "summary": "Helm values configuration file for vLLM AI model deployment with ZARF template variables for dynamic parameterization."
        }
      ],
      "importance_score": 0.65,
      "key_files": [
        "upstream-values.yaml"
      ],
      "name": "values",
      "path": "/var/home/a/code/cowabungaai/packages/vllm/values",
      "purpose": "other",
      "subdirectory_count": 0,
      "summary": "This directory contains Helm chart configuration values for deploying a vLLM AI model service. The single YAML file defines container image settings, deployment naming, and model-specific configurations with ZARF template variables for parameterization during deployment."
    },
    {
      "file_count": 5,
      "file_insights": [],
      "importance_score": 0.0,
      "key_files": [],
      "name": "whisper",
      "path": "/var/home/a/code/cowabungaai/packages/whisper",
      "purpose": "other",
      "subdirectory_count": 2,
      "summary": ""
    },
    {
      "file_count": 2,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "This file serves as the primary metadata definition for the Helm chart, specifying the chart name as cowabunga-model and describing it as a CowabungaAI compatible inferencing backend using whisper.",
          "file_path": "/var/home/a/code/cowabungaai/packages/whisper/chart/Chart.yaml",
          "importance_score": 0.75,
          "interfaces": [],
          "name": "Chart.yaml",
          "responsibilities": [
            "Define chart metadata and versioning",
            "Specify chart type (application or library)",
            "Provide deployment identification information"
          ],
          "source_summary": "Contains Helm chart metadata including apiVersion v2, chart name, description, and configuration for chart type classification.",
          "summary": "Helm chart metadata file defining the chart name, description, and versioning information for the whisper inference backend deployment."
        },
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "This file provides default deployment values including the container image repository from ghcr.io, pull policy, environment variables for logging, and pod security context settings.",
          "file_path": "/var/home/a/code/cowabungaai/packages/whisper/chart/values.yaml",
          "importance_score": 0.7,
          "interfaces": [],
          "name": "values.yaml",
          "responsibilities": [
            "Define default container image configuration",
            "Set environment variables for application",
            "Configure pod security context and permissions"
          ],
          "source_summary": "Contains YAML-formatted configuration values for image repository, tag versioning, environment variables, and pod security context with fsGroup and runAsNonRoot settings.",
          "summary": "Default configuration values file for the Helm chart containing container image settings, environment variables, and pod security configurations."
        }
      ],
      "importance_score": 0.65,
      "key_files": [
        "Chart.yaml",
        "values.yaml"
      ],
      "name": "chart",
      "path": "/var/home/a/code/cowabungaai/packages/whisper/chart",
      "purpose": "other",
      "subdirectory_count": 1,
      "summary": "This directory contains Helm chart configuration files for deploying a CowabungaAI whisper model inference backend to Kubernetes. The Chart.yaml defines chart metadata and versioning while values.yaml provides deployment configuration defaults including container image settings and environment variables."
    },
    {
      "file_count": 4,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.fullname",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Release.Namespace",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file creates a Kubernetes ConfigMap that holds the models.toml configuration file, specifying the backend address and model ownership information for the gRPC service.",
          "file_path": "/var/home/a/code/cowabungaai/packages/whisper/chart/templates/configmap.yaml",
          "importance_score": 0.75,
          "interfaces": [],
          "name": "configmap.yaml",
          "responsibilities": [
            "Store model configuration",
            "Define backend address",
            "Set model ownership metadata"
          ],
          "source_summary": "The file defines a ConfigMap resource with metadata including name, namespace, and labels. It contains a data section with models.toml configuration specifying the backend endpoint and model type.",
          "summary": "Defines a ConfigMap that stores model configuration data for the application."
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.fullname",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.labels",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.selectorLabels",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Values.replicaCount",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Values.strategy",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Values.podAnnotations",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file creates a Deployment manifest that manages the application pods, including replica count, update strategy, and pod template specifications for the gRPC service.",
          "file_path": "/var/home/a/code/cowabungaai/packages/whisper/chart/templates/deployment.yaml",
          "importance_score": 0.9,
          "interfaces": [],
          "name": "deployment.yaml",
          "responsibilities": [
            "Manage pod lifecycle",
            "Configure replica count",
            "Define update strategy",
            "Set pod labels and annotations"
          ],
          "source_summary": "The file defines a Deployment with configurable replicas, strategy for updates, selector labels, and pod template metadata. It includes conditional blocks for strategy configuration and pod annotations.",
          "summary": "Defines the Kubernetes Deployment resource for running the application pods."
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Values.persistence.storageClass",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Values.persistence.accessModes",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Values.persistence.size",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file creates a PersistentVolumeClaim resource that provides persistent storage for the application, with configurable storage class, access modes, and size.",
          "file_path": "/var/home/a/code/cowabungaai/packages/whisper/chart/templates/pvc.yaml",
          "importance_score": 0.7,
          "interfaces": [],
          "name": "pvc.yaml",
          "responsibilities": [
            "Provide persistent storage",
            "Configure storage class",
            "Set storage size and access modes"
          ],
          "source_summary": "The file defines a PVC with conditional storage class configuration, access modes, and storage size requests. It uses Helm template syntax to make storage configuration dynamic.",
          "summary": "Defines a PersistentVolumeClaim for storing application data persistently."
        },
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.fullname",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chart.labels",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Values.service.type",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "Values.service.port",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file creates a Service resource that exposes the application's gRPC endpoint on port 50051, with annotations for Zarf integration and configurable service type.",
          "file_path": "/var/home/a/code/cowabungaai/packages/whisper/chart/templates/service.yaml",
          "importance_score": 0.85,
          "interfaces": [],
          "name": "service.yaml",
          "responsibilities": [
            "Expose gRPC endpoint",
            "Configure service type",
            "Set connection annotations",
            "Define port mappings"
          ],
          "source_summary": "The file defines a Service with metadata including Zarf connection annotations, labels, and port configuration. It specifies TCP protocol and targets port 50051 for gRPC communication.",
          "summary": "Defines a Kubernetes Service to expose the gRPC endpoint to other services."
        }
      ],
      "importance_score": 0.85,
      "key_files": [
        "deployment.yaml",
        "service.yaml",
        "configmap.yaml",
        "pvc.yaml"
      ],
      "name": "templates",
      "path": "/var/home/a/code/cowabungaai/packages/whisper/chart/templates",
      "purpose": "other",
      "subdirectory_count": 0,
      "summary": "This directory contains Helm chart templates for deploying a gRPC service to Kubernetes. The files work together to define the complete deployment stack including configuration (ConfigMap), application pods (Deployment), persistent storage (PVC), and service exposure (Service)."
    },
    {
      "file_count": 1,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "Defines deployment parameters including container image, GPU runtime, resource limits, and persistent volume settings for a Whisper AI model deployment. Uses ZARF templating syntax for variable substitution during deployment.",
          "file_path": "/var/home/a/code/cowabungaai/packages/whisper/values/upstream-values.yaml",
          "importance_score": 0.7,
          "interfaces": [],
          "name": "upstream-values.yaml",
          "responsibilities": [
            "Define container image settings",
            "Configure GPU resources",
            "Set persistent storage parameters",
            "Manage deployment variables"
          ],
          "source_summary": "Contains YAML configuration with templated variables (###ZARF_CONST_IMAGE_VERSION###, ###ZARF_VAR_GPU_RUNTIME###, etc.) for image repository, GPU runtime class, resource limits, and PVC settings",
          "summary": "Configuration file for Kubernetes deployment with templated variables for ZARF deployment tool"
        }
      ],
      "importance_score": 0.65,
      "key_files": [
        "upstream-values.yaml"
      ],
      "name": "values",
      "path": "/var/home/a/code/cowabungaai/packages/whisper/values",
      "purpose": "other",
      "subdirectory_count": 0,
      "summary": "This directory contains deployment configuration templates for Kubernetes workloads, specifically for a Whisper AI model deployment. The single YAML file uses ZARF templating variables to define container image, GPU resources, and persistent storage settings."
    },
    {
      "file_count": 4,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "tokio",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "axum",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "tower",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "serde",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "Defines the workspace members including api, sdk, db, models, ui, and repeater crates, along with shared dependencies like tokio, axum, tower, and serde.",
          "file_path": "/var/home/a/code/cowabungaai/rust/Cargo.toml",
          "importance_score": 0.95,
          "interfaces": [],
          "name": "Cargo.toml",
          "responsibilities": [
            "Define workspace structure and member crates",
            "Configure shared dependencies across all crates",
            "Set workspace-level package metadata",
            "Specify Rust edition and toolchain version"
          ],
          "source_summary": "Configures workspace resolver to version 3, sets edition to 2024, specifies Rust version 1.85, and lists shared dependencies with their features.",
          "summary": "Workspace configuration file defining the Rust workspace with multiple crates and shared dependencies."
        },
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "Configures cargo deny to check for unlicensed dependencies, yanked crates, and copyleft licenses, with specific targets for x86_64 and aarch64 Linux.",
          "file_path": "/var/home/a/code/cowabungaai/rust/deny.toml",
          "importance_score": 0.85,
          "interfaces": [],
          "name": "deny.toml",
          "responsibilities": [
            "Enforce license compliance across dependencies",
            "Block yanked and insecure crates",
            "Configure security auditing targets",
            "Set feature analysis depth"
          ],
          "source_summary": "Sets license policy to deny unlicensed and copyleft dependencies, allows specific MIT and Apache licenses, and configures feature depth for dependency analysis.",
          "summary": "Cargo deny configuration for license compliance and security auditing across the workspace."
        },
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "Defines shell recipes for checking, building, testing, linting, and other development workflows using the just command runner.",
          "file_path": "/var/home/a/code/cowabungaai/rust/justfile",
          "importance_score": 0.8,
          "interfaces": [],
          "name": "justfile",
          "responsibilities": [
            "Automate common development workflows",
            "Enforce strict warning policies",
            "Provide consistent build commands",
            "Support multi-target builds"
          ],
          "source_summary": "Sets up bash shell, exports RUSTFLAGS with warnings as errors, and provides recipes for check, build, test, lint, and other common operations.",
          "summary": "Justfile providing build automation recipes for common development tasks."
        },
        {
          "code_purpose": "config",
          "dependencies": [],
          "detailed_description": "Configures the Rust toolchain to use version 1.85 with rustfmt, clippy, and rust-analyzer components for consistent development environment.",
          "file_path": "/var/home/a/code/cowabungaai/rust/rust-toolchain.toml",
          "importance_score": 0.75,
          "interfaces": [],
          "name": "rust-toolchain.toml",
          "responsibilities": [
            "Specify Rust version for the project",
            "Enable formatting and linting tools",
            "Configure rust-analyzer for IDE support",
            "Ensure consistent toolchain across environments"
          ],
          "source_summary": "Sets channel to 1.85 and includes formatting, linting, and analysis components for the development workflow.",
          "summary": "Rust toolchain configuration specifying the Rust version and components."
        }
      ],
      "importance_score": 0.9,
      "key_files": [
        "Cargo.toml",
        "deny.toml",
        "justfile",
        "rust-toolchain.toml"
      ],
      "name": "rust",
      "path": "/var/home/a/code/cowabungaai/rust",
      "purpose": "other",
      "subdirectory_count": 3,
      "summary": "This is a Rust workspace root directory containing critical configuration files that define the project structure, build automation, and toolchain settings. The files work together to establish workspace members, enforce security and license policies, automate common development tasks, and specify the Rust toolchain version."
    },
    {
      "file_count": 1,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "cowabunga-sdk",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "cowabunga-db",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "cowabunga-models",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "axum",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "tokio",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "tower-http",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "serde",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "serde_json",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "tonic",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "tracing",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "tracing-subscriber",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "Defines package metadata including name, version, edition, and license settings while declaring all internal and external dependencies required for the cowabunga-api project",
          "file_path": "/var/home/a/code/cowabungaai/rust/crates/api/Cargo.toml",
          "importance_score": 0.9,
          "interfaces": [],
          "name": "Cargo.toml",
          "responsibilities": [
            "Package configuration and metadata definition",
            "Dependency management for internal and external crates",
            "Workspace inheritance for shared settings",
            "Build system configuration for Rust project"
          ],
          "source_summary": "Configures package name as cowabunga-api with workspace inheritance for version, edition, license, and rust-version. Declares internal dependencies on cowabunga-sdk, cowabunga-db, and cowabunga-models packages plus external dependencies for web framework and serialization.",
          "summary": "Main configuration file for the Rust API package defining package metadata and dependencies"
        }
      ],
      "importance_score": 0.85,
      "key_files": [
        "Cargo.toml"
      ],
      "name": "api",
      "path": "/var/home/a/code/cowabungaai/rust/crates/api",
      "purpose": "api",
      "subdirectory_count": 1,
      "summary": "This is the API package directory containing the main Cargo.toml manifest file for the cowabunga-api Rust project. It serves as the entry point for the API layer, coordinating with other cowabunga-* packages (sdk, db, models) and external dependencies like axum for web framework functionality."
    },
    {
      "file_count": 7,
      "file_insights": [
        {
          "code_purpose": "middleware",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "Arc",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "Serialize",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "AppState",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "Implements authentication middleware that extracts API key credentials from requests and creates AuthUser structs for authenticated operations.",
          "file_path": "/var/home/a/code/cowabungaai/rust/crates/api/src/auth.rs",
          "importance_score": 0.75,
          "interfaces": [
            {
              "description": null,
              "interface_type": "struct",
              "name": "AuthUser",
              "parameters": [],
              "return_type": "struct",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "struct",
              "name": "ErrorBody",
              "parameters": [],
              "return_type": "struct",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "trait implementation",
              "name": "FromRequestParts",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "request",
                  "param_type": "Request"
                }
              ],
              "return_type": "Result<AuthUser, AuthError>",
              "visibility": ""
            }
          ],
          "name": "auth.rs",
          "responsibilities": [
            "Extract API key from request headers",
            "Validate authentication credentials",
            "Create authenticated user context",
            "Handle authentication errors"
          ],
          "source_summary": "Defines AuthUser struct for authenticated request principals, ErrorBody for error responses, and implements FromRequestParts trait for extracting authentication from request parts.",
          "summary": "API-key authentication extractor that validates and extracts authenticated user information from requests."
        },
        {
          "code_purpose": "service",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "HashMap",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "async_trait",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "BoxStream",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "Channel",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "AuthUser",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "Defines Backend trait for model backend abstraction and implements GrpcBackend and StubBackend for gRPC and stub implementations respectively.",
          "file_path": "/var/home/a/code/cowabungaai/rust/crates/api/src/backend.rs",
          "importance_score": 0.95,
          "interfaces": [
            {
              "description": null,
              "interface_type": "trait",
              "name": "Backend",
              "parameters": [],
              "return_type": "trait",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "struct",
              "name": "GrpcBackend",
              "parameters": [],
              "return_type": "struct",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "function",
              "name": "new",
              "parameters": [],
              "return_type": "Self",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "function",
              "name": "has_model",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "model",
                  "param_type": "&str"
                }
              ],
              "return_type": "bool",
              "visibility": ""
            }
          ],
          "name": "backend.rs",
          "responsibilities": [
            "Define backend abstraction trait",
            "Implement gRPC backend client",
            "Provide stub backend for testing",
            "Handle chat completion requests"
          ],
          "source_summary": "Implements Backend trait with async methods for chat completion, provides GrpcBackend with gRPC client integration, and includes StubBackend for testing purposes.",
          "summary": "Backend client interface and gRPC implementation for model backend communication."
        },
        {
          "code_purpose": "types",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "Serialize",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "Defines ApiError enum with various error conditions and implements IntoResponse for converting errors to HTTP responses.",
          "file_path": "/var/home/a/code/cowabungaai/rust/crates/api/src/error.rs",
          "importance_score": 0.7,
          "interfaces": [
            {
              "description": null,
              "interface_type": "enum",
              "name": "ApiError",
              "parameters": [],
              "return_type": "enum",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "trait implementation",
              "name": "IntoResponse",
              "parameters": [],
              "return_type": "Response",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "function",
              "name": "status_and_message",
              "parameters": [],
              "return_type": "(StatusCode, String)",
              "visibility": ""
            }
          ],
          "name": "error.rs",
          "responsibilities": [
            "Define API error types",
            "Convert errors to HTTP responses",
            "Provide status codes for errors",
            "Serialize error responses"
          ],
          "source_summary": "Creates ApiError enum with ModelNotAvailable and InvalidRequest variants, defines ErrorResponse struct, and implements IntoResponse trait for HTTP conversion.",
          "summary": "API error types and response handlers for consistent error handling across the application."
        },
        {
          "code_purpose": "lib",
          "dependencies": [],
          "detailed_description": "Serves as the library entry point, declaring all public modules including auth, backend, error, router, routes, state, and types.",
          "file_path": "/var/home/a/code/cowabungaai/rust/crates/api/src/lib.rs",
          "importance_score": 0.6,
          "interfaces": [],
          "name": "lib.rs",
          "responsibilities": [
            "Declare library modules",
            "Export public API",
            "Define module boundaries",
            "Provide library entry point"
          ],
          "source_summary": "Exports seven public modules that comprise the entire application structure, serving as the main module declaration for the CowabungaAI API library.",
          "summary": "Root module that exports all public modules and defines the library structure."
        },
        {
          "code_purpose": "entry",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "Arc",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "router::router",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "ApiKeyRecord",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "LibsqlConfig",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "Contains the main async function that sets up tracing, initializes database storage, creates application state, and starts the Axum HTTP server.",
          "file_path": "/var/home/a/code/cowabungaai/rust/crates/api/src/main.rs",
          "importance_score": 0.9,
          "interfaces": [
            {
              "description": null,
              "interface_type": "async_function",
              "name": "main",
              "parameters": [],
              "return_type": "anyhow::Result<()>",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "async_function",
              "name": "dev_memory_storage",
              "parameters": [],
              "return_type": "MemoryStorage",
              "visibility": ""
            }
          ],
          "name": "main.rs",
          "responsibilities": [
            "Initialize application state",
            "Configure logging/tracing",
            "Start HTTP server",
            "Initialize database storage"
          ],
          "source_summary": "Defines main async function with tokio runtime, configures tracing subscriber, initializes Libsql or Memory storage, creates AppState, and starts the router.",
          "summary": "Application entry point that initializes the server, configures logging, and starts the HTTP server."
        },
        {
          "code_purpose": "router",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "Arc",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "cors::CorsLayer",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "auth_middleware",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "routes",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "Creates the Axum router with authentication middleware, CORS layer, and routes to various API endpoints.",
          "file_path": "/var/home/a/code/cowabungaai/rust/crates/api/src/router.rs",
          "importance_score": 0.8,
          "interfaces": [
            {
              "description": null,
              "interface_type": "function",
              "name": "router",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "state",
                  "param_type": "Arc<AppState>"
                }
              ],
              "return_type": "Router",
              "visibility": ""
            }
          ],
          "name": "router.rs",
          "responsibilities": [
            "Configure HTTP router",
            "Apply authentication middleware",
            "Set up CORS headers",
            "Wire API routes"
          ],
          "source_summary": "Defines router function that creates protected routes with auth middleware, configures CORS, adds tracing layer, and wires all API routes together.",
          "summary": "HTTP router configuration that wires together middleware, routes, and application state."
        },
        {
          "code_purpose": "context",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "Arc",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "Storage",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "ModelRegistry",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "Defines AppState struct that is shared across all Axum handlers, containing storage and model registry as Arc-wrapped dependencies.",
          "file_path": "/var/home/a/code/cowabungaai/rust/crates/api/src/state.rs",
          "importance_score": 0.65,
          "interfaces": [
            {
              "description": null,
              "interface_type": "struct",
              "name": "AppState",
              "parameters": [],
              "return_type": "struct",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "function",
              "name": "new",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "storage",
                  "param_type": "Arc<dyn Storage>"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "model_registry",
                  "param_type": "Arc<ModelRegistry>"
                }
              ],
              "return_type": "Self",
              "visibility": ""
            }
          ],
          "name": "state.rs",
          "responsibilities": [
            "Define application state structure",
            "Provide shared state for handlers",
            "Store database reference",
            "Store model registry"
          ],
          "source_summary": "Creates AppState struct with storage and model_registry fields, implements new constructor function for initializing application state.",
          "summary": "Shared application state struct that holds database storage and model registry references."
        }
      ],
      "importance_score": 0.92,
      "key_files": [
        "backend.rs",
        "main.rs",
        "router.rs",
        "auth.rs",
        "state.rs"
      ],
      "name": "src",
      "path": "/var/home/a/code/cowabungaai/rust/crates/api/src",
      "purpose": "core",
      "subdirectory_count": 2,
      "summary": "This is the core backend source directory for a Rust-based OpenAI-compatible API server. It contains authentication, backend client interfaces, error handling, routing, and application state management modules that work together to provide a complete REST API service with gRPC model backend integration."
    },
    {
      "file_count": 4,
      "file_insights": [
        {
          "code_purpose": "api",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "Arc",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "Event",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "StreamExt",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "Value",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "ChatRole",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "AuthUser",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "Backend",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "ApiError",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "AppState",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "Handles chat completion requests with streaming support, integrating authentication, backend services, and role management for AI chat interactions.",
          "file_path": "/var/home/a/code/cowabungaai/rust/crates/api/src/routes/chat.rs",
          "importance_score": 0.9,
          "interfaces": [
            {
              "description": null,
              "interface_type": "function",
              "name": "role_from_proto",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "role",
                  "param_type": "i32"
                }
              ],
              "return_type": "String",
              "visibility": ""
            }
          ],
          "name": "chat.rs",
          "responsibilities": [
            "Handle chat completion requests",
            "Stream SSE responses to clients",
            "Manage chat role conversions",
            "Integrate with backend services"
          ],
          "source_summary": "Defines role_from_proto function for converting role integers to strings, uses SSE for streaming responses, and depends on AppState, AuthUser, and Backend components.",
          "summary": "Implements OpenAI-compatible chat completion endpoint with streaming SSE responses"
        },
        {
          "code_purpose": "api",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "State",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "Serialize",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "Arc",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "AppState",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "Implements standard Kubernetes-style health checks including healthz, ready, and live endpoints with response structs for status reporting.",
          "file_path": "/var/home/a/code/cowabungaai/rust/crates/api/src/routes/health.rs",
          "importance_score": 0.75,
          "interfaces": [
            {
              "description": null,
              "interface_type": "async_function",
              "name": "healthz",
              "parameters": [],
              "return_type": "Json<HealthResponse>",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "async_function",
              "name": "ready",
              "parameters": [],
              "return_type": "Json<ReadinessResponse>",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "async_function",
              "name": "live",
              "parameters": [],
              "return_type": "Json<LivenessResponse>",
              "visibility": ""
            }
          ],
          "name": "health.rs",
          "responsibilities": [
            "Provide health status endpoint",
            "Check database connectivity",
            "Verify model loading status",
            "Report service liveness"
          ],
          "source_summary": "Defines HealthResponse, ReadinessChecks, ReadinessResponse, and LivenessResponse structs, with async functions healthz, ready, and live for endpoint handling.",
          "summary": "Provides health, readiness, and liveness check endpoints for service monitoring"
        },
        {
          "code_purpose": "api",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "State",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "Utc",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "Arc",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "AppState",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "Model",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "Provides a simple endpoint to list available AI models with metadata including creation timestamps and model information.",
          "file_path": "/var/home/a/code/cowabungaai/rust/crates/api/src/routes/models.rs",
          "importance_score": 0.7,
          "interfaces": [
            {
              "description": null,
              "interface_type": "async_function",
              "name": "list_models",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "state",
                  "param_type": "State<Arc<AppState>>"
                }
              ],
              "return_type": "Json<ModelList>",
              "visibility": ""
            }
          ],
          "name": "models.rs",
          "responsibilities": [
            "List available AI models",
            "Return model metadata",
            "Track model creation timestamps"
          ],
          "source_summary": "Contains list_models async function that retrieves models from AppState model_registry, returning ModelList with model metadata.",
          "summary": "Implements OpenAI-compatible models listing endpoint"
        },
        {
          "code_purpose": "module",
          "dependencies": [],
          "detailed_description": "Declares and exports the chat, health, and models submodules, serving as the entry point for the routes package.",
          "file_path": "/var/home/a/code/cowabungaai/rust/crates/api/src/routes/mod.rs",
          "importance_score": 0.5,
          "interfaces": [],
          "name": "mod.rs",
          "responsibilities": [
            "Declare route submodules",
            "Export route functions",
            "Organize API handlers"
          ],
          "source_summary": "Contains three module declarations: chat, health, and models, establishing the package structure for API route handlers.",
          "summary": "Module declaration file organizing route submodules"
        }
      ],
      "importance_score": 0.85,
      "key_files": [
        "chat.rs",
        "health.rs",
        "models.rs",
        "mod.rs"
      ],
      "name": "routes",
      "path": "/var/home/a/code/cowabungaai/rust/crates/api/src/routes",
      "purpose": "other",
      "subdirectory_count": 0,
      "summary": "The routes directory contains API endpoint implementations for a Rust backend using the axum framework. It organizes HTTP handlers into chat completions, health checks, and model listing endpoints, serving as the primary interface layer for external API requests."
    },
    {
      "file_count": 3,
      "file_insights": [
        {
          "code_purpose": "types",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "serde",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "std::collections::HashMap",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file contains the core data structures for chat operations including ChatCompletionRequest, ChatMessage, ChatCompletionResponse, and streaming variants. It provides default values for common parameters like max_tokens and temperature.",
          "file_path": "/var/home/a/code/cowabungaai/rust/crates/api/src/types/chat.rs",
          "importance_score": 0.85,
          "interfaces": [
            {
              "description": null,
              "interface_type": "struct",
              "name": "ChatCompletionRequest",
              "parameters": [],
              "return_type": "struct",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "function",
              "name": "default_max_tokens",
              "parameters": [],
              "return_type": "i32",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "function",
              "name": "default_temperature",
              "parameters": [],
              "return_type": "f32",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "function",
              "name": "default_top_p",
              "parameters": [],
              "return_type": "f32",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "function",
              "name": "content_as_string",
              "parameters": [],
              "return_type": "String",
              "visibility": ""
            }
          ],
          "name": "chat.rs",
          "responsibilities": [
            "Define chat completion request structure",
            "Define chat message and response types",
            "Provide default parameter values",
            "Support streaming chat functionality"
          ],
          "source_summary": "Defines 12 interfaces including structs for chat requests, messages, responses, and usage statistics. Implements default functions for max_tokens and temperature parameters.",
          "summary": "Defines chat completion request/response types for OpenAI-compatible API interactions."
        },
        {
          "code_purpose": "types",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "serde",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file contains data structures for model-related API responses including ModelList and Model structs. It provides factory methods for creating model instances.",
          "file_path": "/var/home/a/code/cowabungaai/rust/crates/api/src/types/models.rs",
          "importance_score": 0.7,
          "interfaces": [
            {
              "description": null,
              "interface_type": "struct",
              "name": "ModelList",
              "parameters": [],
              "return_type": "struct",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "function",
              "name": "new",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "data",
                  "param_type": "Vec<Model>"
                }
              ],
              "return_type": "Self",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "struct",
              "name": "Model",
              "parameters": [],
              "return_type": "struct",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "function",
              "name": "new",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "id",
                  "param_type": "impl Into<String>"
                }
              ],
              "return_type": "Self",
              "visibility": ""
            }
          ],
          "name": "models.rs",
          "responsibilities": [
            "Define model listing response structure",
            "Define individual model data structure",
            "Provide factory methods for model creation"
          ],
          "source_summary": "Defines ModelList struct for listing all available models and Model struct for individual model information. Includes new() constructor functions for both types.",
          "summary": "Defines model listing types for the OpenAI models API endpoint."
        },
        {
          "code_purpose": "module",
          "dependencies": [],
          "detailed_description": "This file serves as the public API gateway for the types directory, re-exporting all types from chat and models submodules for convenient external access.",
          "file_path": "/var/home/a/code/cowabungaai/rust/crates/api/src/types/mod.rs",
          "importance_score": 0.6,
          "interfaces": [],
          "name": "mod.rs",
          "responsibilities": [
            "Export chat module types",
            "Export models module types",
            "Provide unified public API surface"
          ],
          "source_summary": "Declares chat and models submodules and uses re-export statements to expose all public types from both modules at the types directory level.",
          "summary": "Module file that exports chat and models submodules and re-exports all types."
        }
      ],
      "importance_score": 0.75,
      "key_files": [
        "chat.rs",
        "models.rs",
        "mod.rs"
      ],
      "name": "types",
      "path": "/var/home/a/code/cowabungaai/rust/crates/api/src/types",
      "purpose": "other",
      "subdirectory_count": 0,
      "summary": "This directory contains type definitions for an OpenAI-compatible API client, defining request/response structures for chat completions and model listings. The files work together to provide a complete type system with chat.rs handling chat operations, models.rs handling model data, and mod.rs providing module exports."
    },
    {
      "file_count": 1,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "libsql",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "tokio",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "thiserror",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "async-trait",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "tracing",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "sha2",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "hex",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "tokio-test",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file defines the package metadata, dependencies, and build configuration for the cowabunga-db crate. It specifies external libraries needed for database operations and async functionality.",
          "file_path": "/var/home/a/code/cowabungaai/rust/crates/db/Cargo.toml",
          "importance_score": 0.85,
          "interfaces": [],
          "name": "Cargo.toml",
          "responsibilities": [
            "Define package metadata and versioning",
            "Specify external dependencies for database operations",
            "Configure async runtime and error handling libraries",
            "Enable cryptographic utilities for data processing",
            "Support testing infrastructure"
          ],
          "source_summary": "Defines package name, version, edition, license settings, and lists all required dependencies including libsql for database access, tokio for async runtime, thiserror for error handling, async-trait for async traits, tracing for logging, sha2 and hex for cryptographic operations, and tokio-test for testing.",
          "summary": "Rust package manifest defining the database library configuration and dependencies."
        }
      ],
      "importance_score": 0.85,
      "key_files": [
        "Cargo.toml"
      ],
      "name": "db",
      "path": "/var/home/a/code/cowabungaai/rust/crates/db",
      "purpose": "database",
      "subdirectory_count": 1,
      "summary": "This is a database library package (cowabunga-db) that provides database functionality for the project. It uses libsql as the database backend with async support via tokio, and includes cryptographic utilities (sha2, hex) for data handling. The package serves as a core infrastructure component for data persistence operations."
    },
    {
      "file_count": 6,
      "file_insights": [
        {
          "code_purpose": "module",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "error",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "libsql",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "memory",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "migrations",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "storage",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file serves as the central module declaration for the storage subsystem, exposing all submodules and their public types to consumers of the crate.",
          "file_path": "/var/home/a/code/cowabungaai/rust/crates/db/src/lib.rs",
          "importance_score": 0.85,
          "interfaces": [],
          "name": "lib.rs",
          "responsibilities": [
            "Module organization",
            "Public API exposure",
            "Type re-exporting"
          ],
          "source_summary": "Declares and exports five submodules (error, libsql, memory, migrations, storage) and re-exports key types like StorageError, LibsqlConfig, LibsqlStorage, MemoryStorage, and Storage trait.",
          "summary": "Main module entry point that exports all storage subsystem components and re-exports public types."
        },
        {
          "code_purpose": "types",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "async_trait",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "StorageError",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file establishes the abstraction boundary for storage operations, defining the contract that libSQL and in-memory adapters must implement.",
          "file_path": "/var/home/a/code/cowabungaai/rust/crates/db/src/storage.rs",
          "importance_score": 0.9,
          "interfaces": [
            {
              "description": null,
              "interface_type": "async_function",
              "name": "health_check",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "self",
                  "param_type": "&self"
                }
              ],
              "return_type": "Result<(), StorageError>",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "async_function",
              "name": "get_api_key",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "key",
                  "param_type": "&str"
                }
              ],
              "return_type": "Result<ApiKeyRecord, StorageError>",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "async_function",
              "name": "record_api_key_usage",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "key_id",
                  "param_type": "&str"
                }
              ],
              "return_type": "Result<(), StorageError>",
              "visibility": ""
            }
          ],
          "name": "storage.rs",
          "responsibilities": [
            "Define storage abstraction",
            "Type definitions",
            "Trait contract"
          ],
          "source_summary": "Defines ApiKeyRecord struct with id, user_id, and name fields, and the Storage async trait with health_check, get_api_key, and record_api_key_usage methods.",
          "summary": "Defines the Storage trait and ApiKeyRecord type that all storage implementations must conform to."
        },
        {
          "code_purpose": "database",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "PathBuf",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "Arc",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "async_trait",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "Builder",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "Digest",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "StorageError",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "run_migrations",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "ApiKeyRecord",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file provides the production database implementation using libSQL, handling connection management, migrations, and health checks.",
          "file_path": "/var/home/a/code/cowabungaai/rust/crates/db/src/libsql.rs",
          "importance_score": 0.92,
          "interfaces": [
            {
              "description": null,
              "interface_type": "async_function",
              "name": "new",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "config",
                  "param_type": "LibsqlConfig"
                }
              ],
              "return_type": "Result<Self, StorageError>",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "async_function",
              "name": "health_check",
              "parameters": [],
              "return_type": "Result<(), StorageError>",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "async_function",
              "name": "get_api_key",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "key",
                  "param_type": "&str"
                }
              ],
              "return_type": "Result<ApiKeyRecord, StorageError>",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "async_function",
              "name": "record_api_key_usage",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "key_id",
                  "param_type": "&str"
                }
              ],
              "return_type": "Result<(), StorageError>",
              "visibility": ""
            }
          ],
          "name": "libsql.rs",
          "responsibilities": [
            "Database connectivity",
            "Migration execution",
            "Health monitoring",
            "API key persistence"
          ],
          "source_summary": "Defines LibsqlConfig struct for connection settings and LibsqlStorage struct implementing the Storage trait with async methods for health checks, API key operations, and migration execution.",
          "summary": "Implements the libSQL/Turso database adapter with configuration and migration support."
        },
        {
          "code_purpose": "database",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "HashMap",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "Arc",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "async_trait",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "RwLock",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "StorageError",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "ApiKeyRecord",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file implements a lightweight in-memory storage solution that tracks health state and provides basic API key operations for unit testing.",
          "file_path": "/var/home/a/code/cowabungaai/rust/crates/db/src/memory.rs",
          "importance_score": 0.75,
          "interfaces": [
            {
              "description": null,
              "interface_type": "function",
              "name": "new",
              "parameters": [],
              "return_type": "Self",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "async_function",
              "name": "health_check",
              "parameters": [],
              "return_type": "Result<(), StorageError>",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "async_function",
              "name": "get_api_key",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "key",
                  "param_type": "&str"
                }
              ],
              "return_type": "Result<ApiKeyRecord, StorageError>",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "async_function",
              "name": "record_api_key_usage",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "key_id",
                  "param_type": "&str"
                }
              ],
              "return_type": "Result<(), StorageError>",
              "visibility": ""
            }
          ],
          "name": "memory.rs",
          "responsibilities": [
            "In-memory persistence",
            "Test support",
            "Health state tracking",
            "API key management"
          ],
          "source_summary": "Defines MemoryStorage struct implementing the Storage trait with HashMap-based storage, supporting health checks, API key CRUD operations, and usage tracking.",
          "summary": "Provides an in-memory storage adapter for testing and development environments."
        },
        {
          "code_purpose": "types",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "Error",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file provides error type definitions using thiserror, covering not found, conflict, database errors, and migration failures.",
          "file_path": "/var/home/a/code/cowabungaai/rust/crates/db/src/error.rs",
          "importance_score": 0.7,
          "interfaces": [
            {
              "description": null,
              "interface_type": "function",
              "name": "from",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "err",
                  "param_type": "libsql::Error"
                }
              ],
              "return_type": "Self",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "function",
              "name": "from",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "err",
                  "param_type": "std::io::Error"
                }
              ],
              "return_type": "Self",
              "visibility": ""
            }
          ],
          "name": "error.rs",
          "responsibilities": [
            "Error type definition",
            "Error conversion",
            "Error messaging"
          ],
          "source_summary": "Defines StorageError enum with NotFound, Conflict, Database, and Migration error variants, implementing From trait for libsql::Error and std::io::Error.",
          "summary": "Defines StorageError enum with error variants for storage operations."
        },
        {
          "code_purpose": "database",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "HashMap",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "StorageError",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file handles migration definitions and execution, providing a way to apply schema changes through libSQL connections.",
          "file_path": "/var/home/a/code/cowabungaai/rust/crates/db/src/migrations.rs",
          "importance_score": 0.78,
          "interfaces": [
            {
              "description": null,
              "interface_type": "function",
              "name": "migrations",
              "parameters": [],
              "return_type": "Vec<Migration>",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "async_function",
              "name": "run_migrations",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "conn",
                  "param_type": "&mut libsql::Connection"
                }
              ],
              "return_type": "Result<Vec<String>, StorageError>",
              "visibility": ""
            }
          ],
          "name": "migrations.rs",
          "responsibilities": [
            "Migration definition",
            "Migration execution",
            "Schema management"
          ],
          "source_summary": "Defines Migration struct with version, name, and sql fields, provides migrations() function returning all migrations, and run_migrations() async function for execution.",
          "summary": "Manages database migrations with embedded SQL and execution logic."
        }
      ],
      "importance_score": 0.88,
      "key_files": [
        "lib.rs",
        "storage.rs",
        "libsql.rs",
        "memory.rs",
        "error.rs"
      ],
      "name": "src",
      "path": "/var/home/a/code/cowabungaai/rust/crates/db/src",
      "purpose": "core",
      "subdirectory_count": 0,
      "summary": "This is the core storage layer implementation directory for CowabungaAI, providing a persistence seam with multiple adapters (libSQL and in-memory). It defines the Storage trait, error types, migration management, and database connectivity interfaces for API key persistence operations."
    },
    {
      "file_count": 1,
      "file_insights": [
        {
          "code_purpose": "lib",
          "dependencies": [
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "serde",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "tokio-test",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "Defines the package metadata and dependencies for the models library, including workspace inheritance for version, edition, license, and rust-version settings.",
          "file_path": "/var/home/a/code/cowabungaai/rust/crates/models/Cargo.toml",
          "importance_score": 0.85,
          "interfaces": [],
          "name": "Cargo.toml",
          "responsibilities": [
            "Package metadata definition",
            "Dependency management",
            "Workspace integration",
            "Build configuration"
          ],
          "source_summary": "Configures package name as cowabunga-models, inherits workspace settings for version/edition/license/rust-version, and declares serde as a dependency with tokio-test for development testing.",
          "summary": "Package configuration file for the models library"
        }
      ],
      "importance_score": 0.85,
      "key_files": [
        "Cargo.toml"
      ],
      "name": "models",
      "path": "/var/home/a/code/cowabungaai/rust/crates/models",
      "purpose": "other",
      "subdirectory_count": 1,
      "summary": "This is a Rust library package directory containing data models for the application. The directory serves as a dependency library that defines data structures using serde for serialization and deserialization, with workspace-level configuration for versioning and licensing."
    },
    {
      "file_count": 2,
      "file_insights": [
        {
          "code_purpose": "types",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "serde::Deserialize",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "std::collections::HashMap",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file contains the core data structures for model management including the Model struct with name and backend fields, and the ModelRegistry struct that manages a collection of models using HashMap for efficient lookup.",
          "file_path": "/var/home/a/code/cowabungaai/rust/crates/models/src/config.rs",
          "importance_score": 0.8,
          "interfaces": [
            {
              "description": null,
              "interface_type": "function",
              "name": "new",
              "parameters": [],
              "return_type": "Self",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "function",
              "name": "get",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "name",
                  "param_type": "&str"
                }
              ],
              "return_type": "Option<&Model>",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "function",
              "name": "len",
              "parameters": [],
              "return_type": "usize",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "function",
              "name": "is_empty",
              "parameters": [],
              "return_type": "bool",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "function",
              "name": "iter",
              "parameters": [],
              "return_type": "impl Iterator<Item = &Model>",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "function",
              "name": "add",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "model",
                  "param_type": "Model"
                }
              ],
              "return_type": "()",
              "visibility": ""
            }
          ],
          "name": "config.rs",
          "responsibilities": [
            "Define Model data structure with name and backend fields",
            "Implement ModelRegistry for managing model collections",
            "Provide CRUD operations for model management",
            "Enable deserialization of model configurations"
          ],
          "source_summary": "Defines two main structs: Model with name and backend fields, and ModelRegistry with methods for adding, retrieving, and iterating over models.",
          "summary": "Defines Model and ModelRegistry structs for managing AI model configurations with CRUD operations."
        },
        {
          "code_purpose": "lib",
          "dependencies": [],
          "detailed_description": "This file serves as the main library declaration, exposing the config module and re-exporting the ModelRegistry type for external use by other parts of the application.",
          "file_path": "/var/home/a/code/cowabungaai/rust/crates/models/src/lib.rs",
          "importance_score": 0.7,
          "interfaces": [],
          "name": "lib.rs",
          "responsibilities": [
            "Declare the config module for internal organization",
            "Re-export ModelRegistry for public API access",
            "Serve as the library entry point"
          ],
          "source_summary": "Declares the config module and re-exports ModelRegistry from config for public API access.",
          "summary": "Library entry point that declares and exports the config module and ModelRegistry type."
        }
      ],
      "importance_score": 0.85,
      "key_files": [
        "config.rs",
        "lib.rs"
      ],
      "name": "src",
      "path": "/var/home/a/code/cowabungaai/rust/crates/models/src",
      "purpose": "core",
      "subdirectory_count": 0,
      "summary": "This src directory contains the core Rust library structure with configuration and data models. It defines the Model and ModelRegistry types for managing AI model configurations, with lib.rs serving as the module declaration and export point."
    },
    {
      "file_count": 1,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "cowabunga-sdk",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "tokio",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "tokio-stream",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "tonic",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "async-trait",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "tracing",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "tracing-subscriber",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "chrono",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "uuid",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file configures the cowabunga-repeater binary crate, specifying package metadata, workspace inheritance, and external dependencies required for building the repeater service.",
          "file_path": "/var/home/a/code/cowabungaai/rust/crates/repeater/Cargo.toml",
          "importance_score": 0.75,
          "interfaces": [],
          "name": "Cargo.toml",
          "responsibilities": [
            "Define package metadata and versioning",
            "Configure workspace inheritance for shared settings",
            "Declare external and local dependencies",
            "Set up binary target for compilation"
          ],
          "source_summary": "Defines package name, version, edition, and license from workspace. Declines a binary target pointing to src/main.rs. Lists dependencies including cowabunga-sdk (local), tokio runtime, tonic for gRPC, async-trait, tracing, chrono, and uuid.",
          "summary": "Rust package configuration file defining the repeater binary crate with its dependencies and build settings."
        }
      ],
      "importance_score": 0.65,
      "key_files": [
        "Cargo.toml"
      ],
      "name": "repeater",
      "path": "/var/home/a/code/cowabungaai/rust/crates/repeater",
      "purpose": "other",
      "subdirectory_count": 1,
      "summary": "This directory contains the main binary crate for the cowabunga-repeater service, which serves as an entry point for the repeater functionality. The Cargo.toml configuration defines the package metadata, dependencies, and binary target that connects to the cowabunga-sdk for core operations."
    },
    {
      "file_count": 2,
      "file_insights": [
        {
          "code_purpose": "lib",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "Pin",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "async_trait",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "Stream",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file contains the main business logic implementation including the Repeater struct with ChatCompletionService, ChatCompletionStreamService, TokenCountService, and NameService trait implementations. It also exposes the full_prompt and response functions for chat completion handling.",
          "file_path": "/var/home/a/code/cowabungaai/rust/crates/repeater/src/lib.rs",
          "importance_score": 0.95,
          "interfaces": [
            {
              "description": null,
              "interface_type": "function",
              "name": "full_prompt",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "request",
                  "param_type": "&ChatCompletionRequest"
                }
              ],
              "return_type": "String",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "function",
              "name": "response",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "content",
                  "param_type": "String"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "finish_reason",
                  "param_type": "ChatCompletionFinishReason"
                }
              ],
              "return_type": "ChatCompletionResponse",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "async_function",
              "name": "serve",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "addr",
                  "param_type": "std::net::SocketAddr"
                }
              ],
              "return_type": "Result<(), tonic::transport::Error>",
              "visibility": ""
            }
          ],
          "name": "lib.rs",
          "responsibilities": [
            "Implement gRPC service traits for chat completion",
            "Handle prompt echoing functionality",
            "Manage token counting and name services",
            "Provide async serve function for server startup"
          ],
          "source_summary": "Defines the Repeater struct implementing multiple gRPC service traits, with async functions for full_prompt, response, and serve that handle chat completion requests and echo prompts character by character.",
          "summary": "Core library implementing gRPC service logic for the repeater backend with trait-based service implementations."
        },
        {
          "code_purpose": "entry",
          "dependencies": [],
          "detailed_description": "This file serves as the binary entry point using tokio::main. It configures tracing subscriber with environment-based filtering, reads the REPEATER_BIND environment variable for the server address, and starts the cowabunga_repeater service.",
          "file_path": "/var/home/a/code/cowabungaai/rust/crates/repeater/src/main.rs",
          "importance_score": 0.85,
          "interfaces": [
            {
              "description": null,
              "interface_type": "async_function",
              "name": "main",
              "parameters": [],
              "return_type": "Result<(), Box<dyn std::error::Error>>",
              "visibility": ""
            }
          ],
          "name": "main.rs",
          "responsibilities": [
            "Initialize application logging with tracing",
            "Parse and configure server bind address",
            "Start the gRPC server on specified address"
          ],
          "source_summary": "Defines the main async function that initializes logging with tracing_subscriber, parses the bind address from environment or defaults to 0.0.0.0:50051, and starts the gRPC server.",
          "summary": "Application entry point that initializes logging configuration and starts the gRPC server."
        }
      ],
      "importance_score": 0.92,
      "key_files": [
        "lib.rs",
        "main.rs"
      ],
      "name": "src",
      "path": "/var/home/a/code/cowabungaai/rust/crates/repeater/src",
      "purpose": "core",
      "subdirectory_count": 0,
      "summary": "This directory contains the core backend implementation for the CowabungaAI repeater gRPC service. The lib.rs file implements the main business logic with trait-based service implementations, while main.rs serves as the application entry point that initializes logging and starts the server."
    },
    {
      "file_count": 2,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "tonic",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "prost",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "tokio",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "tonic-build",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "walkdir",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file defines the package metadata, version, edition, license, and all dependencies for the Rust SDK. It uses workspace inheritance for common settings and specifies tonic, prost, tokio as runtime dependencies plus tonic-build and walkdir for code generation.",
          "file_path": "/var/home/a/code/cowabungaai/rust/crates/sdk/Cargo.toml",
          "importance_score": 0.75,
          "interfaces": [],
          "name": "Cargo.toml",
          "responsibilities": [
            "Define package metadata and version",
            "Specify runtime dependencies",
            "Configure build-time dependencies",
            "Enable workspace inheritance"
          ],
          "source_summary": "Contains package configuration with name, version, edition, license, rust-version all inherited from workspace. Dependencies include tonic, prost, tokio for runtime. Build dependencies include tonic-build and walkdir for protobuf code generation.",
          "summary": "Rust package manifest defining the cowabunga-sdk library with workspace settings and dependencies."
        },
        {
          "code_purpose": "module",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "std::path::PathBuf",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "walkdir",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This build script configures the protobuf code generation process by setting the proto directory path, creating the output directory, and walking through proto files to generate Rust code. It uses walkdir for recursive directory traversal.",
          "file_path": "/var/home/a/code/cowabungaai/rust/crates/sdk/build.rs",
          "importance_score": 0.6,
          "interfaces": [
            {
              "description": null,
              "interface_type": "function",
              "name": "main",
              "parameters": [],
              "return_type": "void",
              "visibility": ""
            }
          ],
          "name": "build.rs",
          "responsibilities": [
            "Configure protobuf code generation paths",
            "Create output directory for generated code",
            "Walk through proto directory structure",
            "Filter and process proto files"
          ],
          "source_summary": "Imports PathBuf from std::path. Defines main function that sets proto_dir to ../../proto, joins with cowabunga_sdk subdirectory, and creates src/generated output directory. Uses walkdir to iterate through proto files and filter for actual files.",
          "summary": "Build script that generates Rust code from protobuf definitions located in the proto directory."
        }
      ],
      "importance_score": 0.65,
      "key_files": [
        "Cargo.toml",
        "build.rs"
      ],
      "name": "sdk",
      "path": "/var/home/a/code/cowabungaai/rust/crates/sdk",
      "purpose": "other",
      "subdirectory_count": 1,
      "summary": "This is a Rust SDK package directory containing the package manifest (Cargo.toml) and a build script (build.rs) that generates code from protobuf definitions. The directory serves as a library package providing gRPC/protobuf-based services using tonic and prost dependencies."
    },
    {
      "file_count": 1,
      "file_insights": [
        {
          "code_purpose": "lib",
          "dependencies": [],
          "detailed_description": "This file serves as the root library module that re-exports generated gRPC types, providing a clean interface for the backend API contracts and shared type definitions.",
          "file_path": "/var/home/a/code/cowabungaai/rust/crates/sdk/src/lib.rs",
          "importance_score": 0.8,
          "interfaces": [],
          "name": "lib.rs",
          "responsibilities": [
            "Export generated gRPC types",
            "Provide API contract definitions",
            "Enable backend type sharing"
          ],
          "source_summary": "The file contains a module declaration for 'generated' and includes a clippy lint allow attribute for private items documentation.",
          "summary": "Main library module that exports generated gRPC types and contracts for the CowabungaAI backend system."
        }
      ],
      "importance_score": 0.75,
      "key_files": [
        "lib.rs"
      ],
      "name": "src",
      "path": "/var/home/a/code/cowabungaai/rust/crates/sdk/src",
      "purpose": "core",
      "subdirectory_count": 1,
      "summary": "This is the root source directory containing the main library module that exports generated gRPC types and contracts for the CowabungaAI backend system. The directory serves as the infrastructure layer for shared API type definitions across backend services."
    },
    {
      "file_count": 7,
      "file_insights": [
        {
          "code_purpose": "module",
          "dependencies": [
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "audio.rs",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "chat.rs",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "completion.rs",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "counting.rs",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "embeddings.rs",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "include",
              "is_external": false,
              "line_number": null,
              "name": "name.rs",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file serves as the module root that includes all generated service modules, providing a unified namespace for the generated gRPC API definitions.",
          "file_path": "/var/home/a/code/cowabungaai/rust/crates/sdk/src/generated/mod.rs",
          "importance_score": 0.7,
          "interfaces": [],
          "name": "mod.rs",
          "responsibilities": [
            "Include all generated service modules",
            "Provide unified module namespace",
            "Organize generated code structure"
          ],
          "source_summary": "Contains include statements for audio, chat, completion, counting, embeddings, and name modules, organizing all generated code under a single module namespace.",
          "summary": "Module aggregator that includes all generated service files"
        },
        {
          "code_purpose": "api",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "prost",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "Uri",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "Defines audio service client implementations and message types for audio metadata, format handling, and client configuration with compression support.",
          "file_path": "/var/home/a/code/cowabungaai/rust/crates/sdk/src/generated/audio.rs",
          "importance_score": 0.6,
          "interfaces": [
            {
              "description": null,
              "interface_type": "struct",
              "name": "AudioMetadata",
              "parameters": [],
              "return_type": "struct",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "enum",
              "name": "AudioFormat",
              "parameters": [],
              "return_type": "enum",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "struct",
              "name": "AudioClient",
              "parameters": [],
              "return_type": "struct",
              "visibility": ""
            }
          ],
          "name": "audio.rs",
          "responsibilities": [
            "Define audio service message types",
            "Provide audio client implementation",
            "Handle audio format and metadata"
          ],
          "source_summary": "Contains AudioMetadata struct, AudioFormat enum, AudioRequest, AudioResponse, Segment, AudioTask, and AudioClient with methods for compression and origin configuration.",
          "summary": "Generated gRPC service definitions for audio-related operations"
        },
        {
          "code_purpose": "api",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "prost",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "Uri",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "Defines chat service client implementations and message types for chat completion requests, responses, and role-based message handling.",
          "file_path": "/var/home/a/code/cowabungaai/rust/crates/sdk/src/generated/chat.rs",
          "importance_score": 0.65,
          "interfaces": [
            {
              "description": null,
              "interface_type": "struct",
              "name": "ChatItem",
              "parameters": [],
              "return_type": "struct",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "struct",
              "name": "ChatCompletionRequest",
              "parameters": [],
              "return_type": "struct",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "struct",
              "name": "ChatCompletionServiceClient",
              "parameters": [],
              "return_type": "struct",
              "visibility": ""
            }
          ],
          "name": "chat.rs",
          "responsibilities": [
            "Define chat service message types",
            "Provide chat completion client",
            "Handle chat role and completion data"
          ],
          "source_summary": "Contains ChatItem, ChatCompletionRequest, ChatCompletionChoice, Usage, ChatCompletionResponse, ChatRole, ChatCompletionFinishReason, and ChatCompletionServiceClient.",
          "summary": "Generated gRPC service definitions for chat completion operations"
        },
        {
          "code_purpose": "api",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "prost",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "Uri",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "Defines completion service client implementations and message types for text completion requests with support for suffix, max tokens, and streaming.",
          "file_path": "/var/home/a/code/cowabungaai/rust/crates/sdk/src/generated/completion.rs",
          "importance_score": 0.65,
          "interfaces": [
            {
              "description": null,
              "interface_type": "struct",
              "name": "CompletionRequest",
              "parameters": [],
              "return_type": "struct",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "struct",
              "name": "CompletionServiceClient",
              "parameters": [],
              "return_type": "struct",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "struct",
              "name": "CompletionStreamServiceClient",
              "parameters": [],
              "return_type": "struct",
              "visibility": ""
            }
          ],
          "name": "completion.rs",
          "responsibilities": [
            "Define completion service message types",
            "Provide completion client implementations",
            "Handle text completion and streaming"
          ],
          "source_summary": "Contains CompletionRequest, CompletionChoice, CompletionUsage, CompletionResponse, CompletionFinishReason, CompletionServiceClient, and CompletionStreamServiceClient.",
          "summary": "Generated gRPC service definitions for text completion operations"
        },
        {
          "code_purpose": "api",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "prost",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "Uri",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "Defines token counting service client implementations and message types for counting tokens in text input.",
          "file_path": "/var/home/a/code/cowabungaai/rust/crates/sdk/src/generated/counting.rs",
          "importance_score": 0.5,
          "interfaces": [
            {
              "description": null,
              "interface_type": "struct",
              "name": "TokenCountRequest",
              "parameters": [],
              "return_type": "struct",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "struct",
              "name": "TokenCountResponse",
              "parameters": [],
              "return_type": "struct",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "struct",
              "name": "TokenCountServiceClient",
              "parameters": [],
              "return_type": "struct",
              "visibility": ""
            }
          ],
          "name": "counting.rs",
          "responsibilities": [
            "Define token counting service types",
            "Provide token counting client",
            "Handle text token count requests"
          ],
          "source_summary": "Contains TokenCountRequest, TokenCountResponse, TokenCountServiceClient, TokenCountService trait, and TokenCountServiceServer.",
          "summary": "Generated gRPC service definitions for token counting operations"
        },
        {
          "code_purpose": "api",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "prost",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "Uri",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "Defines embedding service client implementations and message types for creating vector embeddings from text inputs.",
          "file_path": "/var/home/a/code/cowabungaai/rust/crates/sdk/src/generated/embeddings.rs",
          "importance_score": 0.55,
          "interfaces": [
            {
              "description": null,
              "interface_type": "struct",
              "name": "EmbeddingRequest",
              "parameters": [],
              "return_type": "struct",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "struct",
              "name": "Embedding",
              "parameters": [],
              "return_type": "struct",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "struct",
              "name": "EmbeddingsServiceClient",
              "parameters": [],
              "return_type": "struct",
              "visibility": ""
            }
          ],
          "name": "embeddings.rs",
          "responsibilities": [
            "Define embedding service types",
            "Provide embedding client",
            "Handle vector embedding requests"
          ],
          "source_summary": "Contains EmbeddingRequest, Embedding, EmbeddingResponse, EmbeddingsServiceClient, EmbeddingsService trait, and EmbeddingsServiceServer.",
          "summary": "Generated gRPC service definitions for embedding operations"
        },
        {
          "code_purpose": "api",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "prost",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "Uri",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "tonic",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "Defines name service client implementations and message types for retrieving or generating names.",
          "file_path": "/var/home/a/code/cowabungaai/rust/crates/sdk/src/generated/name.rs",
          "importance_score": 0.45,
          "interfaces": [
            {
              "description": null,
              "interface_type": "struct",
              "name": "NameResponse",
              "parameters": [],
              "return_type": "struct",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "struct",
              "name": "NameServiceClient",
              "parameters": [],
              "return_type": "struct",
              "visibility": ""
            }
          ],
          "name": "name.rs",
          "responsibilities": [
            "Define name service types",
            "Provide name service client",
            "Handle name retrieval operations"
          ],
          "source_summary": "Contains NameResponse, NameServiceClient, NameService trait, NameServiceServer, and tonic implementation.",
          "summary": "Generated gRPC service definitions for name-related operations"
        }
      ],
      "importance_score": 0.65,
      "key_files": [
        "mod.rs",
        "audio.rs",
        "chat.rs",
        "completion.rs",
        "counting.rs"
      ],
      "name": "generated",
      "path": "/var/home/a/code/cowabungaai/rust/crates/sdk/src/generated",
      "purpose": "other",
      "subdirectory_count": 0,
      "summary": "This directory contains auto-generated gRPC service definitions created by prost-build, providing API contracts for audio, chat, completion, token counting, embeddings, and name services. The files work together to define message types and client implementations for external service communication in a Rust backend system."
    },
    {
      "file_count": 1,
      "file_insights": [
        {
          "code_purpose": "config",
          "dependencies": [
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "leptos",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "leptos_axum",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "leptos_meta",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "axum",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "tokio",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "tower",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "tower-http",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "tracing",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file configures the Rust package with Leptos web framework dependencies, SSR support, and backend integration libraries like axum and tokio.",
          "file_path": "/var/home/a/code/cowabungaai/rust/crates/ui/Cargo.toml",
          "importance_score": 0.75,
          "interfaces": [],
          "name": "Cargo.toml",
          "responsibilities": [
            "Define package metadata and versioning",
            "Configure Leptos web framework dependencies",
            "Set up backend integration libraries",
            "Specify binary entry point location"
          ],
          "source_summary": "Defines package metadata including name, version, edition, and license. Declares dependencies on leptos with SSR features, leptos_axum, leptos_meta, and backend infrastructure libraries. Configures a binary target pointing to src/main.rs.",
          "summary": "Package configuration file defining dependencies and build settings for the cowabunga-ui application."
        }
      ],
      "importance_score": 0.65,
      "key_files": [
        "Cargo.toml"
      ],
      "name": "ui",
      "path": "/var/home/a/code/cowabungaai/rust/crates/ui",
      "purpose": "frontend",
      "subdirectory_count": 1,
      "summary": "This is the UI package directory containing the main configuration file for a Leptos-based web application. The Cargo.toml defines package metadata, dependencies including Leptos framework with SSR support, and entry point configuration for the cowabunga-ui application."
    },
    {
      "file_count": 3,
      "file_insights": [
        {
          "code_purpose": "entry",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "axum",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "leptos",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "leptos_axum",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "tower",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "tower_http",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "cowabunga_ui",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file serves as the application entry point, initializing configuration, setting up the Axum router, and starting the server with Leptos server-side rendering capabilities.",
          "file_path": "/var/home/a/code/cowabungaai/rust/crates/ui/src/main.rs",
          "importance_score": 0.95,
          "interfaces": [
            {
              "description": null,
              "interface_type": "async_function",
              "name": "main",
              "parameters": [],
              "return_type": "void",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "function",
              "name": "shell",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "options",
                  "param_type": "LeptosOptions"
                }
              ],
              "return_type": "impl IntoView",
              "visibility": ""
            }
          ],
          "name": "main.rs",
          "responsibilities": [
            "Initialize application configuration",
            "Set up Axum web server",
            "Configure Leptos SSR routes",
            "Start the web server"
          ],
          "source_summary": "Defines the main async function that loads configuration, sets up Leptos options, creates the Axum router with LeptosRoutes, and starts the server.",
          "summary": "Main entry point for the CowabungaAI Leptos SSR application using Axum web framework."
        },
        {
          "code_purpose": "lib",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "app",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file serves as the crate root, making the app module and App component publicly available for use by other crates and the main application.",
          "file_path": "/var/home/a/code/cowabungaai/rust/crates/ui/src/lib.rs",
          "importance_score": 0.75,
          "interfaces": [
            {
              "description": null,
              "interface_type": "pub_use",
              "name": "App",
              "parameters": [],
              "return_type": "impl IntoView",
              "visibility": ""
            }
          ],
          "name": "lib.rs",
          "responsibilities": [
            "Define crate root",
            "Export app module",
            "Re-export App component"
          ],
          "source_summary": "Exports the app module and re-exports the App component from app.rs as a public interface.",
          "summary": "Library root that exports the app module and App component for the CowabungaAI UI crate."
        },
        {
          "code_purpose": "widget",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": true,
              "line_number": null,
              "name": "leptos",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file defines the main App component using Leptos view macro, creating the root UI structure with a main element containing the application title and status message.",
          "file_path": "/var/home/a/code/cowabungaai/rust/crates/ui/src/app.rs",
          "importance_score": 0.8,
          "interfaces": [
            {
              "description": null,
              "interface_type": "function",
              "name": "App",
              "parameters": [],
              "return_type": "impl IntoView",
              "visibility": ""
            }
          ],
          "name": "app.rs",
          "responsibilities": [
            "Define root application component",
            "Render main UI structure",
            "Display application branding"
          ],
          "source_summary": "Defines the App component function that returns a view with a main element containing an h1 heading and paragraph.",
          "summary": "Root Leptos application component that renders the main UI with CowabungaAI branding."
        }
      ],
      "importance_score": 0.88,
      "key_files": [
        "main.rs",
        "lib.rs",
        "app.rs"
      ],
      "name": "src",
      "path": "/var/home/a/code/cowabungaai/rust/crates/ui/src",
      "purpose": "core",
      "subdirectory_count": 0,
      "summary": "This is the root source directory of a CowabungaAI Leptos web application with server-side rendering. It contains the main entry point (main.rs), library root (lib.rs), and root application component (app.rs) that work together to create a Rust-based SSR web UI."
    },
    {
      "file_count": 2,
      "file_insights": [
        {
          "code_purpose": "database",
          "dependencies": [],
          "detailed_description": "This file establishes the complete database schema for the CowabungaAI application, replacing a PostgreSQL Supabase schema with SQLite/libSQL equivalents. It defines 20+ tables covering user management, file uploads, AI conversations, embeddings, and audit logging.",
          "file_path": "/var/home/a/code/cowabungaai/rust/migrations/refinery/V1__initial_schema.sql",
          "importance_score": 0.9,
          "interfaces": [],
          "name": "V1__initial_schema.sql",
          "responsibilities": [
            "Define user authentication and profile tables",
            "Establish file storage and upload metadata",
            "Create conversation and message history tables",
            "Set up AI embedding and vector storage",
            "Implement audit logging for user actions"
          ],
          "source_summary": "Contains CREATE TABLE statements for users, conversations, files, messages, embeddings, audit logs, and various configuration tables. Includes foreign key constraints and triggers for data integrity.",
          "summary": "Initial database schema defining all core tables including users, authentication, conversations, files, messages, and AI-related data structures."
        },
        {
          "code_purpose": "database",
          "dependencies": [
            {
              "dependency_type": "use",
              "is_external": false,
              "line_number": null,
              "name": "assistant",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This migration file addresses a naming inconsistency between the initial schema (using 'assistant') and the CRUD layer (expecting 'assistant_objects'). It creates an alias table and migrates existing rows to maintain data consistency.",
          "file_path": "/var/home/a/code/cowabungaai/rust/migrations/refinery/V2__reconcile_assistant_table.sql",
          "importance_score": 0.7,
          "interfaces": [],
          "name": "V2__reconcile_assistant_table.sql",
          "responsibilities": [
            "Create assistant_objects alias table",
            "Reconcile naming with CRUD layer expectations",
            "Migrate existing assistant data to new table"
          ],
          "source_summary": "Creates the assistant_objects table with fields for id, object type, creation timestamp, name, description, model, instructions, and tools. Includes a comment explaining the reconciliation purpose.",
          "summary": "Migration file that creates an alias table assistant_objects to reconcile naming differences with the CRUD layer."
        }
      ],
      "importance_score": 0.85,
      "key_files": [
        "V1__initial_schema.sql",
        "V2__reconcile_assistant_table.sql"
      ],
      "name": "refinery",
      "path": "/var/home/a/code/cowabungaai/rust/migrations/refinery",
      "purpose": "other",
      "subdirectory_count": 0,
      "summary": "This directory contains database migration files that define the core data schema for the application, including user authentication, file storage, conversations, messages, and AI assistant objects. The files work together to establish the foundational database structure using SQLite/libSQL compatible schema definitions."
    },
    {
      "file_count": 1,
      "file_insights": [
        {
          "code_purpose": "types",
          "dependencies": [],
          "detailed_description": "This file defines the data contract for audio-related API operations, specifying message structures for metadata and requests that clients use to interact with audio services",
          "file_path": "/var/home/a/code/cowabungaai/rust/proto/cowabunga_sdk/audio/audio.proto",
          "importance_score": 0.85,
          "interfaces": [
            {
              "description": null,
              "interface_type": "enum",
              "name": "AudioTask",
              "parameters": [],
              "return_type": "AudioTask",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "enum",
              "name": "AudioFormat",
              "parameters": [],
              "return_type": "AudioFormat",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "message",
              "name": "AudioMetadata",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "prompt",
                  "param_type": "string"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "temperature",
                  "param_type": "float"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "inputlanguage",
                  "param_type": "string"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "format",
                  "param_type": "AudioFormat"
                }
              ],
              "return_type": "AudioMetadata",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "message",
              "name": "AudioRequest",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "request",
                  "param_type": "oneof"
                }
              ],
              "return_type": "AudioRequest",
              "visibility": ""
            }
          ],
          "name": "audio.proto",
          "responsibilities": [
            "Define audio task types for transcription and translation",
            "Specify audio metadata structure including prompt, temperature, and language",
            "Establish request format contracts for audio API interactions"
          ],
          "source_summary": "Contains enum definitions for AudioTask (TRANSCRIBE, TRANSLATE) and AudioFormat (JSON, TEXT, SRT, VERBOSE_JSON, VTT), along with message definitions for AudioMetadata and AudioRequest",
          "summary": "Defines Protocol Buffer message types for audio operations including transcription and translation"
        }
      ],
      "importance_score": 0.75,
      "key_files": [
        "audio.proto"
      ],
      "name": "audio",
      "path": "/var/home/a/code/cowabungaai/rust/proto/cowabunga_sdk/audio",
      "purpose": "other",
      "subdirectory_count": 0,
      "summary": "This directory contains Protocol Buffer definitions for audio-related API operations including transcription and translation tasks. The file defines data structures for audio metadata and requests that serve as the contract for audio service interactions."
    },
    {
      "file_count": 1,
      "file_insights": [
        {
          "code_purpose": "types",
          "dependencies": [],
          "detailed_description": "This file defines the core data structures for the chat system, including role enumeration (USER, SYSTEM, FUNCTION, ASSISTANT), chat item messages, and chat completion request structures used for AI chat interactions.",
          "file_path": "/var/home/a/code/cowabungaai/rust/proto/cowabunga_sdk/chat/chat.proto",
          "importance_score": 0.7,
          "interfaces": [
            {
              "description": null,
              "interface_type": "enum",
              "name": "ChatRole",
              "parameters": [],
              "return_type": "ChatRole",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "message",
              "name": "ChatItem",
              "parameters": [],
              "return_type": "ChatItem",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "message",
              "name": "ChatCompletionRequest",
              "parameters": [],
              "return_type": "ChatCompletionRequest",
              "visibility": ""
            }
          ],
          "name": "chat.proto",
          "responsibilities": [
            "Define chat role enumeration for conversation participants",
            "Define chat item structure for message content",
            "Define chat completion request format for AI interactions"
          ],
          "source_summary": "Contains ChatRole enum with four values, ChatItem message with role and content fields, and ChatCompletionRequest message with chat_items and max_new_tokens parameters for OpenAI/HF compatibility.",
          "summary": "Defines Protocol Buffer message types for chat communication including roles, items, and completion requests"
        }
      ],
      "importance_score": 0.7,
      "key_files": [
        "chat.proto"
      ],
      "name": "chat",
      "path": "/var/home/a/code/cowabungaai/rust/proto/cowabunga_sdk/chat",
      "purpose": "other",
      "subdirectory_count": 0,
      "summary": "This directory contains Protocol Buffer definitions for chat-related data structures, defining message types and roles used in the chat system. The files work together to establish a standardized data contract for chat communication between client and server components."
    },
    {
      "file_count": 1,
      "file_insights": [
        {
          "code_purpose": "types",
          "dependencies": [],
          "detailed_description": "This file defines the data contract for completion requests, specifying all parameters needed to interact with AI completion services including prompt text, sampling parameters, and token limits.",
          "file_path": "/var/home/a/code/cowabungaai/rust/proto/cowabunga_sdk/completion/completion.proto",
          "importance_score": 0.75,
          "interfaces": [],
          "name": "completion.proto",
          "responsibilities": [
            "Define completion request data structure",
            "Specify AI generation parameters",
            "Enable cross-language API contracts"
          ],
          "source_summary": "The file defines a CompletionRequest message with fields for prompt, suffix, max_new_tokens, temperature, top_k, top_p, do_sample, and other generation parameters following HuggingFace and OpenAI conventions.",
          "summary": "Defines the CompletionRequest protobuf message for AI completion API calls"
        }
      ],
      "importance_score": 0.65,
      "key_files": [
        "completion.proto"
      ],
      "name": "completion",
      "path": "/var/home/a/code/cowabungaai/rust/proto/cowabunga_sdk/completion",
      "purpose": "other",
      "subdirectory_count": 0,
      "summary": "This directory contains Protocol Buffer definitions for completion API requests in a Go project. The completion.proto file defines the CompletionRequest message structure used for communicating with AI completion services, supporting various parameters like temperature, top_k, and token limits."
    },
    {
      "file_count": 1,
      "file_insights": [
        {
          "code_purpose": "api",
          "dependencies": [],
          "detailed_description": "This file defines the protobuf schema for the TokenCountService gRPC service, establishing the API contract for token counting functionality.",
          "file_path": "/var/home/a/code/cowabungaai/rust/proto/cowabunga_sdk/counting/counting.proto",
          "importance_score": 0.75,
          "interfaces": [
            {
              "description": null,
              "interface_type": "rpc",
              "name": "CountTokens",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "request",
                  "param_type": "TokenCountRequest"
                }
              ],
              "return_type": "TokenCountResponse",
              "visibility": ""
            }
          ],
          "name": "counting.proto",
          "responsibilities": [
            "Define token counting request/response schema",
            "Establish gRPC service contract",
            "Specify message field types and numbers"
          ],
          "source_summary": "The file defines two message types (TokenCountRequest with text field, TokenCountResponse with count field) and one service (TokenCountService) with a CountTokens RPC method.",
          "summary": "Defines the gRPC service contract for token counting operations"
        }
      ],
      "importance_score": 0.65,
      "key_files": [
        "counting.proto"
      ],
      "name": "counting",
      "path": "/var/home/a/code/cowabungaai/rust/proto/cowabunga_sdk/counting",
      "purpose": "other",
      "subdirectory_count": 0,
      "summary": "This directory contains a gRPC service definition for token counting functionality. The counting.proto file defines the protocol buffer schema for the TokenCountService, including request/response message types and the CountTokens RPC method."
    },
    {
      "file_count": 1,
      "file_insights": [
        {
          "code_purpose": "api",
          "dependencies": [],
          "detailed_description": "This file defines the complete API contract for the embeddings service using Protocol Buffers, establishing message structures and service methods for gRPC communication.",
          "file_path": "/var/home/a/code/cowabungaai/rust/proto/cowabunga_sdk/embeddings/embeddings.proto",
          "importance_score": 0.9,
          "interfaces": [
            {
              "description": null,
              "interface_type": "rpc",
              "name": "CreateEmbedding",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "EmbeddingRequest",
                  "param_type": "EmbeddingRequest"
                }
              ],
              "return_type": "EmbeddingResponse",
              "visibility": ""
            }
          ],
          "name": "embeddings.proto",
          "responsibilities": [
            "Define embedding request structure with input strings",
            "Define embedding response structure with float vectors",
            "Define service interface for gRPC communication",
            "Establish data contract for embedding operations"
          ],
          "source_summary": "Contains three message definitions (EmbeddingRequest, Embedding, EmbeddingResponse) and one service definition (EmbeddingsService) with a CreateEmbedding RPC method.",
          "summary": "Defines the protobuf schema for the embeddings gRPC service including request/response messages and service interface"
        }
      ],
      "importance_score": 0.85,
      "key_files": [
        "embeddings.proto"
      ],
      "name": "embeddings",
      "path": "/var/home/a/code/cowabungaai/rust/proto/cowabunga_sdk/embeddings",
      "purpose": "other",
      "subdirectory_count": 0,
      "summary": "This directory contains Protocol Buffer definitions for the embeddings service API, defining request/response message structures and service contracts for gRPC communication. The single file establishes the data schema and service interface for embedding operations."
    },
    {
      "file_count": 1,
      "file_insights": [
        {
          "code_purpose": "api",
          "dependencies": [
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "google/protobuf/empty.proto",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This file defines the NameService gRPC service with a Name RPC method that takes an empty request and returns a NameResponse containing a name string field. It establishes the service contract for the name functionality.",
          "file_path": "/var/home/a/code/cowabungaai/rust/proto/cowabunga_sdk/name/name.proto",
          "importance_score": 0.8,
          "interfaces": [
            {
              "description": null,
              "interface_type": "rpc",
              "name": "Name",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "",
                  "param_type": "google.protobuf.Empty"
                }
              ],
              "return_type": "NameResponse",
              "visibility": ""
            }
          ],
          "name": "name.proto",
          "responsibilities": [
            "Define gRPC service contract",
            "Specify message types for responses",
            "Define RPC method signatures",
            "Establish package structure for Go code generation"
          ],
          "source_summary": "Defines a proto3 syntax file with a NameResponse message containing a string name field, and a NameService with a Name RPC method that takes google.protobuf.Empty and returns NameResponse. The file imports google/protobuf/empty.proto and sets the go_package for Go code generation.",
          "summary": "Defines a gRPC service contract for name operations with a NameService and NameResponse message"
        }
      ],
      "importance_score": 0.8,
      "key_files": [
        "name.proto"
      ],
      "name": "name",
      "path": "/var/home/a/code/cowabungaai/rust/proto/cowabunga_sdk/name",
      "purpose": "other",
      "subdirectory_count": 0,
      "summary": "This directory contains a Protocol Buffer definition file that defines a gRPC service contract for name-related operations. The file specifies the NameService with a Name RPC method that returns a NameResponse message containing a name string field."
    },
    {
      "file_count": 2,
      "file_insights": [
        {
          "code_purpose": "util",
          "dependencies": [],
          "detailed_description": "This script sets up the Docker socket path for GPU-enabled deployments, creating the socket file with proper permissions if it doesn't exist. It ensures Docker commands can run with the necessary privileges for GPU support.",
          "file_path": "/var/home/a/code/cowabungaai/scripts/docker-helper.sh",
          "importance_score": 0.5,
          "interfaces": [],
          "name": "docker-helper.sh",
          "responsibilities": [
            "Configure Docker socket path for GPU support",
            "Create socket file with proper permissions",
            "Enable rootless podman compatibility"
          ],
          "source_summary": "The script exports DOCKER_SOCK environment variable, creates the socket directory and file if needed, and sets permissions to 666 for accessibility. It includes a function to run docker commands with root privileges when necessary.",
          "summary": "Bash script that configures Docker socket for GPU deployment with rootless podman support."
        },
        {
          "code_purpose": "util",
          "dependencies": [
            {
              "dependency_type": "import",
              "is_external": false,
              "line_number": null,
              "name": "shutil",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": false,
              "line_number": null,
              "name": "sys",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": false,
              "line_number": null,
              "name": "pathlib",
              "path": null,
              "version": null
            },
            {
              "dependency_type": "import",
              "is_external": true,
              "line_number": null,
              "name": "yam",
              "path": null,
              "version": null
            }
          ],
          "detailed_description": "This script processes zarf package directories to exclude the .model/ weights directory and dataInjections blocks from zarf.yaml. It enables creation of smaller, faster packages for development loops while keeping full packages for air-gapped release builds.",
          "file_path": "/var/home/a/code/cowabungaai/scripts/strip_data_injections.py",
          "importance_score": 0.6,
          "interfaces": [
            {
              "description": null,
              "interface_type": "function",
              "name": "main",
              "parameters": [],
              "return_type": "int",
              "visibility": ""
            },
            {
              "description": null,
              "interface_type": "function",
              "name": "ignore",
              "parameters": [
                {
                  "description": null,
                  "is_optional": false,
                  "name": "dirpath",
                  "param_type": "Any"
                },
                {
                  "description": null,
                  "is_optional": false,
                  "name": "names",
                  "param_type": "Any"
                }
              ],
              "return_type": "None",
              "visibility": ""
            }
          ],
          "name": "strip_data_injections.py",
          "responsibilities": [
            "Strip model weights from zarf packages",
            "Remove dataInjections blocks from configuration",
            "Create lightweight development packages"
          ],
          "source_summary": "The script accepts source package directory and destination directory as arguments. It uses shutil for file operations and yam for YAML processing to strip data injections. The main function orchestrates the package creation workflow.",
          "summary": "Python script that removes model weights and data injections from zarf packages for faster development builds."
        }
      ],
      "importance_score": 0.45,
      "key_files": [
        "strip_data_injections.py",
        "docker-helper.sh"
      ],
      "name": "scripts",
      "path": "/var/home/a/code/cowabungaai/scripts",
      "purpose": "tool",
      "subdirectory_count": 0,
      "summary": "This directory contains utility scripts for deployment and development workflows. The docker-helper.sh script configures Docker socket for GPU support with rootless podman, while strip_data_injections.py creates lightweight development packages by removing model weights and data injections from zarf packages."
    },
    {
      "file_count": 6,
      "file_insights": [],
      "importance_score": 0.0,
      "key_files": [],
      "name": "website",
      "path": "/var/home/a/code/cowabungaai/website",
      "purpose": "other",
      "subdirectory_count": 4,
      "summary": ""
    },
    {
      "file_count": 1,
      "file_insights": [],
      "importance_score": 0.0,
      "key_files": [],
      "name": "scss",
      "path": "/var/home/a/code/cowabungaai/website/assets/scss",
      "purpose": "other",
      "subdirectory_count": 0,
      "summary": ""
    }
  ],
  "file_insights": []
}
```

## Memory Storage Statistics

**Total Storage Size**: 676759 bytes

- **studies_research**: 85680 bytes (12.7%)
- **preprocess**: 358988 bytes (53.0%)
- **documentation**: 232054 bytes (34.3%)
- **timing**: 37 bytes (0.0%)

## Generated Documents Statistics

Number of Generated Documents: 10

- Core Workflows
- Key Modules and Components Research Report_Data Persistence Domain
- Key Modules and Components Research Report_AI Inference Domain
- Key Modules and Components Research Report_API Gateway Domain
- Boundary Interfaces
- Key Modules and Components Research Report_Infrastructure Domain
- Database Overview
- Architecture Description
- Key Modules and Components Research Report_User Interface Domain
- Project Overview
