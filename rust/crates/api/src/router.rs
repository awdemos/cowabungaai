//! HTTP router and middleware wiring.

use std::sync::Arc;

use axum::{
    Router, middleware,
    routing::{get, post},
};
use tower_http::{cors::CorsLayer, trace::TraceLayer};

use crate::auth::auth_middleware;
use crate::routes;
use crate::state::AppState;

/// Assemble the full HTTP router.
pub fn router(state: Arc<AppState>) -> Router {
    let protected = Router::new()
        .route("/openai/v1/models", get(routes::models::list_models))
        .route(
            "/openai/v1/chat/completions",
            post(routes::chat::create_chat_completion),
        )
        .route_layer(middleware::from_fn_with_state(
            state.clone(),
            auth_middleware,
        ))
        .with_state(state.clone());

    let public = Router::new()
        .route("/healthz", get(routes::health::healthz))
        .route("/ready", get(routes::health::ready))
        .route("/live", get(routes::health::live));

    public
        .merge(protected)
        .layer(TraceLayer::new_for_http())
        .layer(CorsLayer::permissive())
        .with_state(state)
}
