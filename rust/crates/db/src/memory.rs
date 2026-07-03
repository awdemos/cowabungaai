//! In-memory storage adapter for unit tests.

use std::collections::HashMap;
use std::sync::Arc;

use async_trait::async_trait;
use tokio::sync::RwLock;

use crate::error::StorageError;
use crate::storage::{ApiKeyRecord, Storage};

/// In-memory implementation of the storage seam.
///
/// This adapter is intentionally trivial: it tracks whether it has been marked
/// healthy and reports `NotFound` when not. It exists to make the `Storage`
/// seam real (two adapters) and to let unit tests exercise code that depends on
/// storage without a database.
#[derive(Debug, Clone)]
pub struct MemoryStorage {
    healthy: Arc<RwLock<bool>>,
    api_keys: Arc<RwLock<HashMap<String, ApiKeyRecord>>>,
}

impl Default for MemoryStorage {
    fn default() -> Self {
        Self {
            healthy: Arc::new(RwLock::new(true)),
            api_keys: Arc::new(RwLock::new(HashMap::new())),
        }
    }
}

impl MemoryStorage {
    /// Create a new, initially healthy in-memory store.
    pub fn new() -> Self {
        Self::default()
    }

    /// Mark the store as unhealthy.
    pub async fn fail(&self) {
        *self.healthy.write().await = false;
    }

    /// Mark the store as healthy.
    pub async fn recover(&self) {
        *self.healthy.write().await = true;
    }

    /// Register an API key for testing authentication.
    pub async fn add_api_key(&self, key: String, record: ApiKeyRecord) {
        self.api_keys.write().await.insert(key, record);
    }
}

#[async_trait]
impl Storage for MemoryStorage {
    async fn health_check(&self) -> Result<(), StorageError> {
        if *self.healthy.read().await {
            Ok(())
        } else {
            Err(StorageError::Database(
                "in-memory store is unhealthy".to_string(),
            ))
        }
    }

    async fn get_api_key(&self, key: &str) -> Result<ApiKeyRecord, StorageError> {
        self.api_keys
            .read()
            .await
            .get(key)
            .cloned()
            .ok_or(StorageError::NotFound)
    }

    async fn record_api_key_usage(&self, _key_id: &str) -> Result<(), StorageError> {
        Ok(())
    }
}
