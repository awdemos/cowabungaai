//! CowabungaAI repeater backend library.
//!
//! A minimal gRPC model backend written in Rust against the same protobuf
//! contract the Python SDK (`legacy/cowabunga_sdk`) implements. It echoes the
//! prompt back character by character, mirroring `packages/repeater/main.py`,
//! and proves the Rust SDK's generated server side works end to end.

use std::pin::Pin;

use async_trait::async_trait;
use tokio_stream::{Stream, StreamExt};

use cowabunga_sdk::generated::chat::{
    ChatCompletionChoice, ChatCompletionFinishReason, ChatCompletionRequest,
    ChatCompletionResponse, ChatItem, ChatRole, Usage,
    chat_completion_service_server::{ChatCompletionService, ChatCompletionServiceServer},
    chat_completion_stream_service_server::{
        ChatCompletionStreamService, ChatCompletionStreamServiceServer,
    },
};
use cowabunga_sdk::generated::counting::{
    TokenCountRequest, TokenCountResponse,
    token_count_service_server::{TokenCountService, TokenCountServiceServer},
};
use cowabunga_sdk::generated::name::{
    NameResponse,
    name_service_server::{NameService, NameServiceServer},
};

const NAME: &str = "repeater";

fn full_prompt(request: &ChatCompletionRequest) -> String {
    request
        .chat_items
        .iter()
        .filter(|item| item.role != ChatRole::System as i32)
        .map(|item| item.content.clone())
        .collect::<Vec<_>>()
        .join("\n")
}

fn response(content: String, finish_reason: ChatCompletionFinishReason) -> ChatCompletionResponse {
    let completion_tokens = i32::try_from(content.split_whitespace().count()).unwrap_or(i32::MAX);
    ChatCompletionResponse {
        id: format!("repeater-{}", uuid::Uuid::new_v4()),
        object: "chat.completion".to_string(),
        created: chrono::Utc::now().timestamp(),
        choices: vec![ChatCompletionChoice {
            index: 0,
            chat_item: Some(ChatItem {
                role: ChatRole::Assistant as i32,
                content,
            }),
            finish_reason: finish_reason as i32,
        }],
        usage: Some(Usage {
            prompt_tokens: 0,
            completion_tokens,
            total_tokens: completion_tokens,
        }),
    }
}

/// Echo backend implementing the chat (unary + streaming), token-count, and
/// name services from the CowabungaAI protobuf contract.
#[derive(Debug, Default, Clone, Copy)]
pub struct Repeater;

#[async_trait]
impl ChatCompletionService for Repeater {
    async fn chat_complete(
        &self,
        request: tonic::Request<ChatCompletionRequest>,
    ) -> Result<tonic::Response<ChatCompletionResponse>, tonic::Status> {
        let echoed = full_prompt(request.get_ref());
        Ok(tonic::Response::new(response(
            echoed,
            ChatCompletionFinishReason::Stop,
        )))
    }
}

#[async_trait]
impl ChatCompletionStreamService for Repeater {
    type ChatCompleteStreamStream =
        Pin<Box<dyn Stream<Item = Result<ChatCompletionResponse, tonic::Status>> + Send>>;

    async fn chat_complete_stream(
        &self,
        request: tonic::Request<ChatCompletionRequest>,
    ) -> Result<tonic::Response<Self::ChatCompleteStreamStream>, tonic::Status> {
        let echoed = full_prompt(request.get_ref());
        let chars: Vec<char> = echoed.chars().collect();
        let total = chars.len();
        let stream = tokio_stream::iter(chars.into_iter().enumerate()).map(move |(idx, ch)| {
            let finish_reason = if idx + 1 == total {
                ChatCompletionFinishReason::Stop
            } else {
                ChatCompletionFinishReason::None
            };
            Ok(response(ch.to_string(), finish_reason))
        });
        Ok(tonic::Response::new(Box::pin(stream)))
    }
}

#[async_trait]
impl TokenCountService for Repeater {
    async fn count_tokens(
        &self,
        request: tonic::Request<TokenCountRequest>,
    ) -> Result<tonic::Response<TokenCountResponse>, tonic::Status> {
        let count = request.get_ref().text.chars().count();
        Ok(tonic::Response::new(TokenCountResponse {
            count: i32::try_from(count).unwrap_or(i32::MAX),
        }))
    }
}

#[async_trait]
impl NameService for Repeater {
    async fn name(
        &self,
        _request: tonic::Request<()>,
    ) -> Result<tonic::Response<NameResponse>, tonic::Status> {
        Ok(tonic::Response::new(NameResponse {
            name: NAME.to_string(),
        }))
    }
}

/// Serve all repeater services on `addr` until the process is signaled.
pub async fn serve(addr: std::net::SocketAddr) -> Result<(), tonic::transport::Error> {
    tonic::transport::Server::builder()
        .add_service(ChatCompletionServiceServer::new(Repeater))
        .add_service(ChatCompletionStreamServiceServer::new(Repeater))
        .add_service(TokenCountServiceServer::new(Repeater))
        .add_service(NameServiceServer::new(Repeater))
        .serve(addr)
        .await
}
