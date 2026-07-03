//! API error types and responses.

use axum::{
    Json,
    http::StatusCode,
    response::{IntoResponse, Response},
};
use serde::Serialize;

/// Errors surfaced by API route handlers.
#[derive(Debug, thiserror::Error)]
pub enum ApiError {
    /// The requested model is not configured or available.
    #[error("model not available: {0}")]
    ModelNotAvailable(String),

    /// The request body is not valid JSON or violates the OpenAI schema.
    #[error("invalid request: {0}")]
    InvalidRequest(String),

    /// A backend gRPC call failed.
    #[error("backend error: {0}")]
    Backend(#[from] tonic::Status),

    /// An unexpected internal failure.
    #[error("internal error: {0}")]
    Internal(#[from] anyhow::Error),
}

impl ApiError {
    fn status_and_message(&self) -> (StatusCode, String) {
        match self {
            ApiError::ModelNotAvailable(name) => (
                StatusCode::NOT_FOUND,
                format!("Model '{name}' is not available"),
            ),
            ApiError::InvalidRequest(msg) => (StatusCode::BAD_REQUEST, msg.clone()),
            ApiError::Backend(status) => {
                (StatusCode::BAD_GATEWAY, format!("Backend error: {status}"))
            }
            ApiError::Internal(err) => (StatusCode::INTERNAL_SERVER_ERROR, err.to_string()),
        }
    }
}

impl IntoResponse for ApiError {
    fn into_response(self) -> Response {
        let (status, message) = self.status_and_message();
        let body = Json(ErrorResponse { error: message });
        (status, body).into_response()
    }
}

/// JSON error payload returned by the API.
#[derive(Debug, Serialize)]
pub struct ErrorResponse {
    pub error: String,
}
