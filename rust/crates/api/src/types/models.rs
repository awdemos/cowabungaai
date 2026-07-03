//! OpenAI-compatible model types.

use serde::{Deserialize, Serialize};

/// Response for `GET /v1/models`.
#[derive(Debug, Clone, Serialize)]
pub struct ModelList {
    pub object: &'static str,
    pub data: Vec<Model>,
}

impl ModelList {
    pub fn new(data: Vec<Model>) -> Self {
        Self {
            object: "list",
            data,
        }
    }
}

/// A single model object.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Model {
    pub id: String,
    pub object: &'static str,
    pub created: i64,
    pub owned_by: String,
}

impl Model {
    pub fn new(id: impl Into<String>) -> Self {
        Self {
            id: id.into(),
            object: "model",
            created: 0,
            owned_by: "cowabungaai".to_string(),
        }
    }
}
