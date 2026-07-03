//! Storage seam for CowabungaAI persistence.

use async_trait::async_trait;

use crate::error::StorageError;

/// A validated API key record.
#[derive(Debug, Clone)]
pub struct ApiKeyRecord {
    pub id: String,
    pub user_id: String,
    pub name: String,
}

/// Abstract storage seam for all CowabungaAI persistence operations.
#[async_trait]
pub trait Storage: Send + Sync {
    /// Verify connectivity and migration state.
    async fn health_check(&self) -> Result<(), StorageError>;

    /// Look up an active API key by its raw key string.
    async fn get_api_key(&self, key: &str) -> Result<ApiKeyRecord, StorageError>;

    /// Touch the `last_used_at` timestamp for an API key.
    async fn record_api_key_usage(&self, key_id: &str) -> Result<(), StorageError>;
}
