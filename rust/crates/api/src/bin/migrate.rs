//! Standalone migration runner for CowabungaAI.
//!
//! Connects to the configured Turso/libSQL database and applies embedded
//! SQL migrations.

use std::env;

use anyhow::{Context, Result};
use cowabunga_db::{LibsqlConfig, LibsqlStorage, Storage};
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

#[tokio::main]
async fn main() -> Result<()> {
    tracing_subscriber::registry()
        .with(
            tracing_subscriber::EnvFilter::try_from_default_env().unwrap_or_else(|_| "info".into()),
        )
        .with(tracing_subscriber::fmt::layer())
        .init();

    let url = env::var("TURSO_URL").context("TURSO_URL environment variable is required")?;
    let auth_token = env::var("TURSO_AUTH_TOKEN").ok();

    // If a local database path is provided alongside a remote URL, prefer the
    // local replica so migrations run against on-disk storage.
    let effective_url = env::var("TURSO_DATABASE_PATH")
        .ok()
        .filter(|p| !p.is_empty())
        .unwrap_or(url);

    tracing::info!(url = %effective_url, "Running CowabungaAI migrations");

    let storage = LibsqlStorage::new(LibsqlConfig {
        url: effective_url,
        auth_token,
    })
    .await
    .context("failed to connect to libSQL database and run migrations")?;

    storage
        .health_check()
        .await
        .context("migration health check failed")?;

    tracing::info!("Migrations completed successfully");
    Ok(())
}
