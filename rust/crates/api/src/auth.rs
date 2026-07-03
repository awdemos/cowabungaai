//! API-key authentication extractor.

use std::sync::Arc;

use axum::{
    extract::{FromRequestParts, Request},
    http::{StatusCode, header, request::Parts},
    response::{IntoResponse, Response},
};
use serde::Serialize;

use crate::state::AppState;

/// Authenticated request principal.
#[derive(Debug, Clone)]
pub struct AuthUser {
    pub user_id: String,
    pub api_key_id: String,
    pub api_key_name: String,
}

#[derive(Debug, Serialize)]
struct ErrorBody {
    error: String,
}

/// Extract an Authorization header of the form `Bearer <api-key>` and validate
/// it against the configured storage backend.
impl FromRequestParts<Arc<AppState>> for AuthUser {
    type Rejection = AuthError;

    async fn from_request_parts(
        parts: &mut Parts,
        state: &Arc<AppState>,
    ) -> Result<Self, Self::Rejection> {
        let header = parts
            .headers
            .get(header::AUTHORIZATION)
            .and_then(|value| value.to_str().ok())
            .ok_or(AuthError::Missing)?;

        let token = header
            .strip_prefix("Bearer ")
            .or_else(|| header.strip_prefix("bearer "))
            .ok_or(AuthError::Malformed)?;

        match state.storage.get_api_key(token).await {
            Ok(record) => {
                let _ = state.storage.record_api_key_usage(&record.id).await;
                Ok(AuthUser {
                    user_id: record.user_id,
                    api_key_id: record.id,
                    api_key_name: record.name,
                })
            }
            Err(cowabunga_db::StorageError::NotFound) => Err(AuthError::Invalid),
            Err(_) => Err(AuthError::Storage),
        }
    }
}

/// Authentication failure variants.
#[derive(Debug, Clone, Copy)]
pub enum AuthError {
    Missing,
    Malformed,
    Invalid,
    Storage,
}

impl IntoResponse for AuthError {
    fn into_response(self) -> Response {
        let (status, message) = match self {
            AuthError::Missing => (StatusCode::UNAUTHORIZED, "Missing Authorization header"),
            AuthError::Malformed => (StatusCode::UNAUTHORIZED, "Malformed Authorization header"),
            AuthError::Invalid => (StatusCode::UNAUTHORIZED, "Invalid API key"),
            AuthError::Storage => (StatusCode::INTERNAL_SERVER_ERROR, "Auth storage error"),
        };

        let body = serde_json::to_string(&ErrorBody {
            error: message.to_string(),
        })
        .unwrap_or_else(|_| format!("{{\"error\":\"{}\"}}", message));

        (status, [(header::CONTENT_TYPE, "application/json")], body).into_response()
    }
}

/// Middleware that validates auth and injects `AuthUser` into extensions.
pub async fn auth_middleware(
    state: axum::extract::State<Arc<AppState>>,
    request: Request,
    next: axum::middleware::Next,
) -> Response {
    let (mut parts, body) = request.into_parts();
    match AuthUser::from_request_parts(&mut parts, &state.0).await {
        Ok(user) => {
            parts.extensions.insert(user);
        }
        Err(err) => return err.into_response(),
    };
    let request = Request::from_parts(parts, body);
    next.run(request).await
}
