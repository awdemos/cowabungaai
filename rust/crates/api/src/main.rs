//! CowabungaAI API entry point.

use std::sync::Arc;

use cowabunga_api::{router::router, state::AppState};
use cowabunga_db::MemoryStorage;
use cowabunga_db::storage::ApiKeyRecord;
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

    let mut model_registry = ModelRegistry::new();
    model_registry.add(Model {
        name: "stub-model".to_string(),
        backend: "stub".to_string(),
    });

    let state = Arc::new(AppState::new(Arc::new(storage), Arc::new(model_registry)));

    let app = router(state);

    let listener = tokio::net::TcpListener::bind("0.0.0.0:8080").await?;
    tracing::info!("listening on {}", listener.local_addr()?);
    axum::serve(listener, app).await?;

    Ok(())
}
