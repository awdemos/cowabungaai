-- CowabungaAI Database Schema for Turso/libSQL
-- Replaces Supabase PostgreSQL schema with SQLite equivalent

-- Enable foreign keys
PRAGMA foreign_keys = ON;

-- ============================================================================
-- Users and Authentication
-- ============================================================================

CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    encrypted_password TEXT,
    email_confirmed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_sign_in_at TIMESTAMP,
    metadata JSON DEFAULT '{}',
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);

-- ============================================================================
-- API Keys
-- ============================================================================

CREATE TABLE IF NOT EXISTS api_keys (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    key_hash TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    last_used_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_api_keys_user ON api_keys(user_id);
CREATE INDEX IF NOT EXISTS idx_api_keys_hash ON api_keys(key_hash);

-- ============================================================================
-- Chat Conversations
-- ============================================================================

CREATE TABLE IF NOT EXISTS conversations (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    title TEXT,
    model TEXT DEFAULT 'synthia-7b',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSON DEFAULT '{}',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_conversations_user ON conversations(user_id);
CREATE INDEX IF NOT EXISTS idx_conversations_created_at ON conversations(created_at);

-- ============================================================================
-- Chat Messages
-- ============================================================================

CREATE TABLE IF NOT EXISTS messages (
    id TEXT PRIMARY KEY,
    conversation_id TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('system', 'user', 'assistant', 'function')),
    content TEXT NOT NULL,
    tokens INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSON DEFAULT '{}',
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_messages_conversation ON messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at);

-- ============================================================================
-- File Metadata (for RAG)
-- ============================================================================

CREATE TABLE IF NOT EXISTS files (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    filename TEXT NOT NULL,
    original_filename TEXT NOT NULL,
    mime_type TEXT,
    size INTEGER NOT NULL,
    storage_path TEXT NOT NULL,
    checksum TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP,
    metadata JSON DEFAULT '{}',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_files_user ON files(user_id);
CREATE INDEX IF NOT EXISTS idx_files_created_at ON files(created_at);

-- ============================================================================
-- Embeddings (for RAG with text-embeddings backend)
-- ============================================================================

CREATE TABLE IF NOT EXISTS embeddings (
    id TEXT PRIMARY KEY,
    file_id TEXT,
    user_id TEXT NOT NULL,
    content TEXT NOT NULL,
    embedding BLOB, -- Store as binary for efficiency
    embedding_model TEXT DEFAULT 'all-MiniLM-L6-v2',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSON DEFAULT '{}',
    FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_embeddings_file ON embeddings(file_id);
CREATE INDEX IF NOT EXISTS idx_embeddings_user ON embeddings(user_id);

-- ============================================================================
-- Sessions (for authentication)
-- ============================================================================

CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    token_hash TEXT UNIQUE NOT NULL,
    ip_address TEXT,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    last_accessed_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_token ON sessions(token_hash);
CREATE INDEX IF NOT EXISTS idx_sessions_expires ON sessions(expires_at);

-- ============================================================================
-- Audit Log
-- ============================================================================

CREATE TABLE IF NOT EXISTS audit_log (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    action TEXT NOT NULL,
    resource_type TEXT NOT NULL,
    resource_id TEXT,
    ip_address TEXT,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSON DEFAULT '{}',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_audit_user ON audit_log(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_action ON audit_log(action);
CREATE INDEX IF NOT EXISTS idx_audit_created_at ON audit_log(created_at);

-- ============================================================================
-- System Configuration
-- ============================================================================

CREATE TABLE IF NOT EXISTS system_config (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by TEXT,
    FOREIGN KEY (updated_by) REFERENCES users(id) ON DELETE SET NULL
);

-- Insert default configuration
INSERT OR IGNORE INTO system_config (key, value, description) VALUES
    ('max_file_size', '10485760', 'Maximum file upload size in bytes (10MB)'),
    ('max_conversation_length', '100', 'Maximum messages per conversation'),
    ('default_model', 'synthia-7b', 'Default LLM model'),
    ('enable_rag', 'true', 'Enable RAG functionality'),
    ('enable_transcription', 'false', 'Enable audio transcription'),
    ('rate_limit_requests', '100', 'Rate limit: requests per hour'),
    ('maintenance_mode', 'false', 'Enable maintenance mode');

-- ============================================================================
-- Vector Content (for RAG similarity search)
-- ============================================================================

CREATE TABLE IF NOT EXISTS vector_content (
    id TEXT PRIMARY KEY,
    vector_store_id TEXT NOT NULL,
    file_id TEXT NOT NULL,
    content TEXT NOT NULL,
    embedding F32_BLOB,
    metadata JSON DEFAULT '{}',
    user_id TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_vector_content_embedding 
ON vector_content USING libsql_vector_idx(embedding);

CREATE INDEX IF NOT EXISTS idx_vector_content_store ON vector_content(vector_store_id);
CREATE INDEX IF NOT EXISTS idx_vector_content_file ON vector_content(file_id);
CREATE INDEX IF NOT EXISTS idx_vector_content_user ON vector_content(user_id);

-- ============================================================================
-- Vector Store
-- ============================================================================

CREATE TABLE IF NOT EXISTS vector_store (
    id TEXT PRIMARY KEY,
    object TEXT,
    bytes INTEGER DEFAULT 0,
    created_at INTEGER DEFAULT 0,
    name TEXT,
    status TEXT DEFAULT 'completed',
    file_counts TEXT DEFAULT '{}',
    metadata TEXT DEFAULT '{}',
    user_id TEXT NOT NULL,
    expires_after TEXT DEFAULT '{}',
    expires_at INTEGER,
    last_active_at INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_vector_store_user ON vector_store(user_id);

-- ============================================================================
-- Vector Store File
-- ============================================================================

CREATE TABLE IF NOT EXISTS vector_store_file (
    id TEXT PRIMARY KEY,
    object TEXT,
    usage_bytes INTEGER DEFAULT 0,
    created_at INTEGER DEFAULT 0,
    vector_store_id TEXT NOT NULL,
    status TEXT DEFAULT 'completed',
    last_error TEXT DEFAULT '{}',
    chunking_strategy TEXT DEFAULT '{}',
    FOREIGN KEY (vector_store_id) REFERENCES vector_store(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_vector_store_file_store ON vector_store_file(vector_store_id);

-- ============================================================================
-- Thread Objects (OpenAI-compatible threads)
-- ============================================================================

CREATE TABLE IF NOT EXISTS thread_objects (
    id TEXT PRIMARY KEY,
    object TEXT DEFAULT 'thread',
    created_at INTEGER DEFAULT 0,
    metadata TEXT DEFAULT '{}',
    tool_resources TEXT DEFAULT '{}',
    user_id TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_thread_objects_user ON thread_objects(user_id);

-- ============================================================================
-- Message Objects (OpenAI-compatible messages)
-- ============================================================================

CREATE TABLE IF NOT EXISTS message_objects (
    id TEXT PRIMARY KEY,
    object TEXT DEFAULT 'thread.message',
    created_at INTEGER DEFAULT 0,
    thread_id TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    assistant_id TEXT,
    run_id TEXT,
    file_ids TEXT DEFAULT '[]',
    metadata TEXT DEFAULT '{}',
    user_id TEXT NOT NULL,
    FOREIGN KEY (thread_id) REFERENCES thread_objects(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_message_objects_thread ON message_objects(thread_id);
CREATE INDEX IF NOT EXISTS idx_message_objects_user ON message_objects(user_id);

-- ============================================================================
-- Run Objects (OpenAI-compatible runs)
-- ============================================================================

CREATE TABLE IF NOT EXISTS run_objects (
    id TEXT PRIMARY KEY,
    object TEXT DEFAULT 'thread.run',
    created_at INTEGER DEFAULT 0,
    thread_id TEXT NOT NULL,
    assistant_id TEXT NOT NULL,
    status TEXT DEFAULT 'queued',
    required_action TEXT DEFAULT '{}',
    last_error TEXT DEFAULT '{}',
    expires_at INTEGER,
    started_at INTEGER,
    cancelled_at INTEGER,
    failed_at INTEGER,
    completed_at INTEGER,
    model TEXT,
    instructions TEXT,
    tools TEXT DEFAULT '[]',
    metadata TEXT DEFAULT '{}',
    usage TEXT DEFAULT '{}',
    temperature REAL,
    top_p REAL,
    max_prompt_tokens INTEGER,
    max_completion_tokens INTEGER,
    truncation_strategy TEXT DEFAULT '{}',
    tool_choice TEXT DEFAULT '{}',
    response_format TEXT DEFAULT '{}',
    user_id TEXT NOT NULL,
    FOREIGN KEY (thread_id) REFERENCES thread_objects(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_run_objects_thread ON run_objects(thread_id);
CREATE INDEX IF NOT EXISTS idx_run_objects_user ON run_objects(user_id);

-- ============================================================================
-- Assistants (OpenAI-compatible assistants)
-- ============================================================================

CREATE TABLE IF NOT EXISTS assistant (
    id TEXT PRIMARY KEY,
    object TEXT DEFAULT 'assistant',
    created_at INTEGER DEFAULT 0,
    name TEXT,
    description TEXT,
    model TEXT NOT NULL,
    instructions TEXT,
    tools TEXT DEFAULT '[]',
    tool_resources TEXT DEFAULT '{}',
    metadata TEXT DEFAULT '{}',
    temperature REAL,
    top_p REAL,
    response_format TEXT DEFAULT '{}',
    user_id TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_assistant_user ON assistant(user_id);

-- ============================================================================
-- File Objects (OpenAI-compatible files)
-- ============================================================================

CREATE TABLE IF NOT EXISTS file_objects (
    id TEXT PRIMARY KEY,
    object TEXT DEFAULT 'file',
    bytes INTEGER DEFAULT 0,
    created_at INTEGER DEFAULT 0,
    filename TEXT NOT NULL,
    purpose TEXT DEFAULT 'assistants',
    status TEXT DEFAULT 'uploaded',
    status_details TEXT,
    metadata TEXT DEFAULT '{}',
    user_id TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_file_objects_user ON file_objects(user_id);

-- ============================================================================
-- Triggers for updated_at
-- ============================================================================

CREATE TRIGGER IF NOT EXISTS users_updated_at
AFTER UPDATE ON users
BEGIN
    UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS conversations_updated_at
AFTER UPDATE ON conversations
BEGIN
    UPDATE conversations SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- ============================================================================
-- Views for Common Queries
-- ============================================================================

CREATE VIEW IF NOT EXISTS active_users AS
SELECT 
    u.id,
    u.email,
    u.created_at,
    u.last_sign_in_at,
    COUNT(DISTINCT c.id) as conversation_count,
    COUNT(DISTINCT f.id) as file_count
FROM users u
LEFT JOIN conversations c ON u.id = c.user_id
LEFT JOIN files f ON u.id = f.user_id
WHERE u.is_active = TRUE
GROUP BY u.id;

CREATE VIEW IF NOT EXISTS recent_conversations AS
SELECT 
    c.id,
    c.title,
    c.model,
    c.created_at,
    c.updated_at,
    u.email as user_email,
    COUNT(m.id) as message_count
FROM conversations c
JOIN users u ON c.user_id = u.id
LEFT JOIN messages m ON c.id = m.conversation_id
WHERE c.updated_at > datetime('now', '-7 days')
GROUP BY c.id
ORDER BY c.updated_at DESC;

-- ============================================================================
-- Schema Version Tracking
-- ============================================================================

CREATE TABLE IF NOT EXISTS schema_migrations (
    version TEXT PRIMARY KEY,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT
);

INSERT OR IGNORE INTO schema_migrations (version, description) VALUES
    ('001', 'Initial schema with core tables');

-- ============================================================================
-- Complete!
-- ============================================================================

-- Schema created successfully
-- Total tables: 10
-- Total indexes: 18
-- Total views: 2
-- Total triggers: 2
