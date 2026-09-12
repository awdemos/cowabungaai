//! CowabungaAI API entry point.

use std::sync::Arc;

use cowabunga_api::{router::router, state::AppState};
use cowabunga_db::storage::ApiKeyRecord;
use cowabunga_db::{LibsqlConfig, LibsqlStorage, MemoryStorage, Storage};
use cowabunga_models::ModelRegistry;
use cowabunga_models::config::Model;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    tracing_subscriber::registry()
        .with(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "info,cowabunga_api=debug".into()),
        )
        .with(tracing_subscriber::fmt::layer().json())
        .init();

    tracing::info!("CowabungaAI API starting");

    // Note: the libsql client only speaks TLS for remote URLs (libsql:// or
    // https://). A plain http:// endpoint cannot be served remotely by this
    // client build — falling back to in-memory rather than letting libsql
    // silently open a local file named after the URL.
    let storage: Arc<dyn Storage> = match std::env::var("TURSO_URL") {
        Ok(url) if url.starts_with("libsql://") || url.starts_with("https://") => {
            tracing::info!(%url, "using remote libSQL storage");
            let auth_token = std::env::var("TURSO_AUTH_TOKEN").ok();
            Arc::new(LibsqlStorage::new(LibsqlConfig { url, auth_token }).await?)
        }
        Ok(url) if url.contains("://") => {
            tracing::warn!(
                %url,
                "TURSO_URL uses a non-TLS scheme this client cannot use remotely \
                 — falling back to in-memory storage"
            );
            Arc::new(dev_memory_storage().await)
        }
        Ok(url) => {
            tracing::info!(%url, "using local-file libSQL storage");
            Arc::new(
                LibsqlStorage::new(LibsqlConfig {
                    url,
                    auth_token: None,
                })
                .await?,
            )
        }
        Err(_) => {
            tracing::warn!(
                "TURSO_URL not set — falling back to in-memory storage with the \
                 hardcoded 'test-key' dev credential; do not use in production"
            );
            Arc::new(dev_memory_storage().await)
        }
    };

    let mut model_registry = ModelRegistry::new();
    model_registry.add(Model {
        name: "stub-model".to_string(),
        backend: "stub".to_string(),
    });

    let state = Arc::new(AppState::new(storage, Arc::new(model_registry)));

    let app = router(state);

    let listener = tokio::net::TcpListener::bind("0.0.0.0:8080").await?;
    tracing::info!("listening on {}", listener.local_addr()?);
    axum::serve(listener, app).await?;

    Ok(())
}

/// In-memory storage seeded with a hardcoded dev API key. Only for local
/// development and tests; production deployments must use libSQL.
async fn dev_memory_storage() -> MemoryStorage {
    let storage = MemoryStorage::new();
    storage
        .add_api_key(
            "test-key".to_string(),
            ApiKeyRecord {
                id: "key-1".to_string(),
                user_id: "user-1".to_string(),
                name: "default".to_string(),
            },
        )
        .await;
    storage
}
