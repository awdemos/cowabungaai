//! Storage errors.

use thiserror::Error;

/// Errors returned by the storage seam.
#[derive(Debug, Error)]
pub enum StorageError {
    /// The requested record was not found.
    #[error("not found")]
    NotFound,

    /// A unique constraint or business invariant was violated.
    #[error("conflict: {0}")]
    Conflict(String),

    /// The underlying database returned an error.
    #[error("database error: {0}")]
    Database(String),

    /// A migration failed.
    #[error("migration error: {0}")]
    Migration(String),
}

impl From<libsql::Error> for StorageError {
    fn from(err: libsql::Error) -> Self {
        let message = err.to_string();
        if message.contains("UNIQUE constraint") || message.contains("PRIMARY KEY") {
            StorageError::Conflict(message)
        } else {
            StorageError::Database(message)
        }
    }
}

impl From<std::io::Error> for StorageError {
    fn from(err: std::io::Error) -> Self {
        StorageError::Database(err.to_string())
    }
}
