//! Health/readiness/liveness endpoints.

use axum::{extract::State, response::Json};
use serde::Serialize;
use std::sync::Arc;

use crate::state::AppState;

/// Response for `GET /healthz`.
#[derive(Debug, Serialize)]
pub struct HealthResponse {
    pub status: &'static str,
    pub timestamp: String,
    pub version: &'static str,
    pub models_loaded: usize,
}

/// Individual readiness checks.
#[derive(Debug, Serialize)]
pub struct ReadinessChecks {
    pub database: bool,
    pub models: bool,
}

/// Response for `GET /ready`.
#[derive(Debug, Serialize)]
pub struct ReadinessResponse {
    pub ready: bool,
    pub timestamp: String,
    pub checks: ReadinessChecks,
}

/// Response for `GET /live`.
#[derive(Debug, Serialize)]
pub struct LivenessResponse {
    pub status: &'static str,
    pub timestamp: String,
}

pub async fn healthz(State(state): State<Arc<AppState>>) -> Json<HealthResponse> {
    Json(HealthResponse {
        status: "healthy",
        timestamp: chrono::Utc::now().to_rfc3339(),
        version: env!("CARGO_PKG_VERSION"),
        models_loaded: state.model_registry.len(),
    })
}

pub async fn ready(State(state): State<Arc<AppState>>) -> Json<ReadinessResponse> {
    let database = state.storage.health_check().await.is_ok();
    let models = state.model_registry.len() > 0;
    let ready = database && models;

    Json(ReadinessResponse {
        ready,
        timestamp: chrono::Utc::now().to_rfc3339(),
        checks: ReadinessChecks { database, models },
    })
}

pub async fn live() -> Json<LivenessResponse> {
    Json(LivenessResponse {
        status: "alive",
        timestamp: chrono::Utc::now().to_rfc3339(),
    })
}
