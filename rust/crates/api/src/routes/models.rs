//! OpenAI-compatible models endpoint.

use axum::{extract::State, response::Json};
use chrono::Utc;
use std::sync::Arc;

use crate::state::AppState;
use crate::types::models::{Model, ModelList};

pub async fn list_models(State(state): State<Arc<AppState>>) -> Json<ModelList> {
    let models: Vec<Model> = state
        .model_registry
        .iter()
        .map(|m| Model {
            id: m.name.clone(),
            object: "model",
            created: Utc::now().timestamp(),
            owned_by: "cowabungaai".to_string(),
        })
        .collect();

    Json(ModelList::new(models))
}
