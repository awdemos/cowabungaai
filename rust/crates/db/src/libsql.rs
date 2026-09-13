//! Turso/libSQL adapter for the storage seam.

use std::path::PathBuf;
use std::sync::Arc;

use async_trait::async_trait;
use libsql::Builder;
use sha2::Digest;

use crate::error::StorageError;
use crate::migrations::run_migrations;
use crate::storage::{ApiKeyRecord, Storage};

/// Configuration for connecting to a libSQL database.
#[derive(Debug, Clone)]
pub struct LibsqlConfig {
    /// libSQL connection URL. May be a local file path, `:memory:`, or a
    /// `libsql://` / `https://` remote URL.
    pub url: String,
    /// Auth token for remote libSQL servers.
    pub auth_token: Option<String>,
}

/// Turso/libSQL implementation of the storage seam.
#[derive(Debug, Clone)]
pub struct LibsqlStorage {
    db: Arc<libsql::Database>,
    local_path: PathBuf,
}

impl LibsqlStorage {
    /// Open a libSQL database from configuration and run migrations.
    pub async fn new(config: LibsqlConfig) -> Result<Self, StorageError> {
        let is_remote = config.url.starts_with("libsql://") || config.url.starts_with("https://");
        let (db, local_path) = if is_remote {
            let token = config.auth_token.clone().unwrap_or_default();
            let db = Builder::new_remote(config.url.clone(), token)
                .build()
                .await?;
            (db, PathBuf::from(":memory:"))
        } else {
            let path = PathBuf::from(&config.url);
            let db = Builder::new_local(&config.url).build().await?;
            (db, path)
        };

        let storage = Self {
            db: Arc::new(db),
            local_path,
        };

        if !is_remote {
            let mut conn = storage.db.connect()?;
            run_migrations(&mut conn).await?;
        }

        Ok(storage)
    }

    /// Local database path used for migrations.
    pub fn local_path(&self) -> &PathBuf {
        &self.local_path
    }
}

#[async_trait]
impl Storage for LibsqlStorage {
    async fn health_check(&self) -> Result<(), StorageError> {
        let conn = self.db.connect()?;
        conn.query("SELECT 1", ()).await?;
        Ok(())
    }

    async fn get_api_key(&self, key: &str) -> Result<ApiKeyRecord, StorageError> {
        let mut hasher = sha2::Sha256::new();
        sha2::Digest::update(&mut hasher, key.as_bytes());
        let hash = hex::encode(sha2::Digest::finalize(hasher));

        let conn = self.db.connect()?;
        let mut rows = conn
            .query(
                "SELECT id, user_id, name FROM api_keys WHERE key_hash = ? AND is_active = TRUE AND (expires_at IS NULL OR expires_at > datetime('now'))",
                [hash],
            )
            .await?;

        let row = rows.next().await?.ok_or(StorageError::NotFound)?;
        Ok(ApiKeyRecord {
            id: row.get(0)?,
            user_id: row.get(1)?,
            name: row.get(2)?,
        })
    }

    async fn record_api_key_usage(&self, key_id: &str) -> Result<(), StorageError> {
        let conn = self.db.connect()?;
        conn.execute(
            "UPDATE api_keys SET last_used_at = CURRENT_TIMESTAMP WHERE id = ?",
            [key_id],
        )
        .await?;
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn memory_storage_health_check() {
        let store = crate::MemoryStorage::new();
        store.health_check().await.unwrap();
    }

    #[tokio::test]
    async fn memory_storage_reports_error_when_unhealthy() {
        let store = crate::MemoryStorage::new();
        store.fail().await;
        assert!(store.health_check().await.is_err());
    }

    #[tokio::test]
    async fn libsql_in_memory_runs_migrations_and_is_healthy() {
        let store = LibsqlStorage::new(LibsqlConfig {
            url: ":memory:".to_string(),
            auth_token: None,
        })
        .await
        .unwrap();

        store.health_check().await.unwrap();
    }
}
