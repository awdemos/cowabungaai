//! End-to-end test: the Rust API's GrpcBackend talking to the Rust repeater
//! backend over a real gRPC connection, using the shared protobuf contract.

use cowabunga_api::backend::{Backend, GrpcBackend};
use cowabunga_api::types::chat::{ChatCompletionRequest, ChatMessage};

fn free_addr() -> std::net::SocketAddr {
    let listener = std::net::TcpListener::bind("127.0.0.1:0").unwrap();
    listener.local_addr().unwrap()
}

async fn start_repeater() -> std::net::SocketAddr {
    let addr = free_addr();
    tokio::spawn(async move {
        cowabunga_repeater::serve(addr).await.unwrap();
    });
    // Give the server a moment to bind before connecting.
    tokio::time::sleep(std::time::Duration::from_millis(100)).await;
    addr
}

fn chat_request(model: &str, content: &str) -> ChatCompletionRequest {
    ChatCompletionRequest {
        model: model.to_string(),
        messages: vec![ChatMessage {
            role: "user".to_string(),
            content: Some(serde_json::Value::String(content.to_string())),
            name: None,
        }],
        stream: false,
        max_tokens: 16,
        temperature: 1.0,
        top_p: 1.0,
        stop: None,
        functions: None,
        stream_options: None,
        extra: Default::default(),
    }
}

#[tokio::test]
async fn grpc_backend_complete_talks_to_rust_repeater() {
    let addr = start_repeater().await;
    let mut backend = GrpcBackend::new();
    backend
        .register(
            "repeater",
            format!("http://{addr}")
                .parse::<tonic::transport::Endpoint>()
                .unwrap(),
        )
        .await
        .unwrap();

    let auth = authed_user();
    let response = backend
        .complete(&auth, chat_request("repeater", "hello world"))
        .await
        .unwrap();

    let choice = response.choices.first().unwrap();
    let item = choice.chat_item.as_ref().unwrap();
    assert_eq!(item.content, "hello world");
}

#[tokio::test]
async fn grpc_backend_complete_errors_for_unregistered_model() {
    let backend = GrpcBackend::new();
    let auth = authed_user();
    let err = backend
        .complete(&auth, chat_request("nope", "hello"))
        .await
        .unwrap_err();
    assert!(err.to_string().contains("nope"));
}

#[tokio::test]
async fn grpc_backend_complete_streams_from_rust_repeater() {
    use futures::StreamExt;

    let addr = start_repeater().await;
    let mut backend = GrpcBackend::new();
    backend
        .register(
            "repeater",
            format!("http://{addr}")
                .parse::<tonic::transport::Endpoint>()
                .unwrap(),
        )
        .await
        .unwrap();

    let auth = authed_user();
    let stream = backend
        .complete_stream(&auth, chat_request("repeater", "abc"))
        .await
        .unwrap();

    let chunks: Vec<String> = stream
        .map(|item| {
            let response = item.unwrap();
            response.choices[0]
                .chat_item
                .as_ref()
                .unwrap()
                .content
                .clone()
        })
        .collect()
        .await;

    assert_eq!(chunks.join(""), "abc");
    assert!(chunks.len() == 3);
}

#[tokio::test]
async fn rust_repeater_counts_tokens() {
    use cowabunga_sdk::generated::counting::{
        TokenCountRequest, token_count_service_client::TokenCountServiceClient,
    };

    let addr = start_repeater().await;
    let mut client = TokenCountServiceClient::connect(format!("http://{addr}"))
        .await
        .unwrap();
    let response = client
        .count_tokens(TokenCountRequest {
            text: "hello world".to_string(),
        })
        .await
        .unwrap();
    assert_eq!(response.into_inner().count, 11);
}

fn authed_user() -> cowabunga_api::auth::AuthUser {
    cowabunga_api::auth::AuthUser {
        user_id: "user-1".to_string(),
        api_key_id: "key-1".to_string(),
        api_key_name: "default".to_string(),
    }
}
