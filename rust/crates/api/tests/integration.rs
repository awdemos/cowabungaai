//! Integration tests for the CowabungaAI API routes.

use std::sync::Arc;

use axum::{
    body::{Body, to_bytes},
    http::{Request, StatusCode, header},
};
use serde_json::{Value, json};
use tower::ServiceExt;

use cowabunga_api::router::router;
use cowabunga_api::state::AppState;
use cowabunga_db::MemoryStorage;
use cowabunga_db::storage::ApiKeyRecord;
use cowabunga_models::ModelRegistry;
use cowabunga_models::config::Model;

async fn test_state() -> Arc<AppState> {
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

    let mut registry = ModelRegistry::new();
    registry.add(Model {
        name: "stub-model".to_string(),
        backend: "stub".to_string(),
    });

    Arc::new(AppState::new(Arc::new(storage), Arc::new(registry)))
}

async fn app() -> axum::Router {
    router(test_state().await)
}

async fn body_json(response: axum::response::Response) -> Value {
    let bytes = to_bytes(response.into_body(), usize::MAX).await.unwrap();
    serde_json::from_slice(&bytes).unwrap()
}

#[tokio::test]
async fn healthz_returns_healthy() {
    let response = app()
        .await
        .oneshot(Request::get("/healthz").body(Body::empty()).unwrap())
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::OK);
    let body = body_json(response).await;
    assert_eq!(body["status"], "healthy");
}

#[tokio::test]
async fn live_returns_alive() {
    let response = app()
        .await
        .oneshot(Request::get("/live").body(Body::empty()).unwrap())
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::OK);
    let body = body_json(response).await;
    assert_eq!(body["status"], "alive");
}

#[tokio::test]
async fn models_requires_auth() {
    let response = app()
        .await
        .oneshot(
            Request::get("/openai/v1/models")
                .body(Body::empty())
                .unwrap(),
        )
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::UNAUTHORIZED);
}

#[tokio::test]
async fn models_returns_list_with_auth() {
    let response = app()
        .await
        .oneshot(
            Request::get("/openai/v1/models")
                .header(header::AUTHORIZATION, "Bearer test-key")
                .body(Body::empty())
                .unwrap(),
        )
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::OK);
    let body = body_json(response).await;
    assert_eq!(body["object"], "list");
    let data = body["data"].as_array().unwrap();
    assert!(!data.is_empty());
    assert_eq!(data[0]["id"], "stub-model");
}

#[tokio::test]
async fn chat_completions_unary_with_auth() {
    let body = json!({
        "model": "stub-model",
        "messages": [{"role": "user", "content": "Hello"}]
    });
    let response = app()
        .await
        .oneshot(
            Request::post("/openai/v1/chat/completions")
                .header(header::AUTHORIZATION, "Bearer test-key")
                .header(header::CONTENT_TYPE, "application/json")
                .body(Body::from(body.to_string()))
                .unwrap(),
        )
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::OK);
    let body = body_json(response).await;
    assert_eq!(body["object"], "chat.completion");
    assert_eq!(body["model"], "stub-model");
    let choices = body["choices"].as_array().unwrap();
    assert!(!choices.is_empty());
}

#[tokio::test]
async fn chat_completions_stream_with_auth() {
    let body = json!({
        "model": "stub-model",
        "messages": [{"role": "user", "content": "Hello"}],
        "stream": true
    });
    let response = app()
        .await
        .oneshot(
            Request::post("/openai/v1/chat/completions")
                .header(header::AUTHORIZATION, "Bearer test-key")
                .header(header::CONTENT_TYPE, "application/json")
                .body(Body::from(body.to_string()))
                .unwrap(),
        )
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::OK);
    let content_type = response
        .headers()
        .get(header::CONTENT_TYPE)
        .unwrap()
        .to_str()
        .unwrap();
    assert!(content_type.starts_with("text/event-stream"));

    let bytes = to_bytes(response.into_body(), usize::MAX).await.unwrap();
    let text = String::from_utf8(bytes.to_vec()).unwrap();
    assert!(text.contains("data:"));
    assert!(text.contains("[DONE]"));
}

#[tokio::test]
async fn chat_completions_rejects_unknown_model() {
    let body = json!({
        "model": "unknown",
        "messages": [{"role": "user", "content": "Hello"}]
    });
    let response = app()
        .await
        .oneshot(
            Request::post("/openai/v1/chat/completions")
                .header(header::AUTHORIZATION, "Bearer test-key")
                .header(header::CONTENT_TYPE, "application/json")
                .body(Body::from(body.to_string()))
                .unwrap(),
        )
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::NOT_FOUND);
}
