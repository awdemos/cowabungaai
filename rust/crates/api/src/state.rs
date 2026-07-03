//! Shared application state.

use std::sync::Arc;

use cowabunga_db::Storage;
use cowabunga_models::ModelRegistry;

/// Application state shared across axum handlers.
pub struct AppState {
    pub storage: Arc<dyn Storage>,
    pub model_registry: Arc<ModelRegistry>,
}

impl AppState {
    pub fn new(storage: Arc<dyn Storage>, model_registry: Arc<ModelRegistry>) -> Self {
        Self {
            storage,
            model_registry,
        }
    }
}
