//! Backend client seam for gRPC model backends.

use std::collections::HashMap;

use async_trait::async_trait;
use cowabunga_sdk::generated::chat::{
    ChatCompletionChoice, ChatCompletionFinishReason,
    ChatCompletionRequest as GrpcChatCompletionRequest,
    ChatCompletionResponse as GrpcChatCompletionResponse, ChatItem, ChatRole, Usage,
    chat_completion_service_client::ChatCompletionServiceClient,
    chat_completion_stream_service_client::ChatCompletionStreamServiceClient,
};
use futures::stream::{BoxStream, StreamExt};
use tonic::transport::Channel;

use crate::auth::AuthUser;
use crate::error::ApiError;
use crate::types::ChatCompletionRequest;

/// Abstraction over the gRPC backend used to generate completions.
#[async_trait]
pub trait Backend: Send + Sync {
    /// Generate a single (non-streaming) chat completion.
    async fn complete(
        &self,
        auth: &AuthUser,
        request: ChatCompletionRequest,
    ) -> Result<GrpcChatCompletionResponse, ApiError>;

    /// Generate a streaming chat completion.
    async fn complete_stream(
        &self,
        auth: &AuthUser,
        request: ChatCompletionRequest,
    ) -> Result<BoxStream<'static, Result<GrpcChatCompletionResponse, ApiError>>, ApiError>;
}

/// A backend client that selects gRPC services based on configured model endpoints.
#[derive(Clone)]
pub struct GrpcBackend {
    clients: HashMap<String, BackendClient>,
}

#[derive(Clone)]
#[allow(dead_code)]
enum BackendClient {
    Unary(ChatCompletionServiceClient<Channel>),
    Streaming(ChatCompletionStreamServiceClient<Channel>),
}

impl GrpcBackend {
    /// Create a backend with no configured endpoints. In a production deployment
    /// this would be populated from a config file or service discovery.
    pub fn new() -> Self {
        Self {
            clients: HashMap::new(),
        }
    }

    /// Register a unary backend endpoint for a model.
    pub async fn register_unary(
        &mut self,
        model: impl Into<String>,
        dst: impl Into<tonic::transport::Endpoint>,
    ) -> Result<(), tonic::transport::Error> {
        let endpoint: tonic::transport::Endpoint = dst.into();
        let client = ChatCompletionServiceClient::connect(endpoint).await?;
        self.clients
            .insert(model.into(), BackendClient::Unary(client));
        Ok(())
    }

    /// Register a streaming backend endpoint for a model.
    pub async fn register_streaming(
        &mut self,
        model: impl Into<String>,
        dst: impl Into<tonic::transport::Endpoint>,
    ) -> Result<(), tonic::transport::Error> {
        let endpoint: tonic::transport::Endpoint = dst.into();
        let client = ChatCompletionStreamServiceClient::connect(endpoint).await?;
        self.clients
            .insert(model.into(), BackendClient::Streaming(client));
        Ok(())
    }
}

impl Default for GrpcBackend {
    fn default() -> Self {
        Self::new()
    }
}

#[async_trait]
impl Backend for GrpcBackend {
    async fn complete(
        &self,
        _auth: &AuthUser,
        request: ChatCompletionRequest,
    ) -> Result<GrpcChatCompletionResponse, ApiError> {
        let _client = self
            .clients
            .get(&request.model)
            .ok_or(ApiError::ModelNotAvailable(request.model.clone()))?;
        Err(ApiError::ModelNotAvailable(request.model))
    }

    async fn complete_stream(
        &self,
        _auth: &AuthUser,
        request: ChatCompletionRequest,
    ) -> Result<BoxStream<'static, Result<GrpcChatCompletionResponse, ApiError>>, ApiError> {
        let _client = self
            .clients
            .get(&request.model)
            .ok_or(ApiError::ModelNotAvailable(request.model.clone()))?;
        Err(ApiError::ModelNotAvailable(request.model))
    }
}

/// A stub backend that returns deterministic responses without a network hop.
/// Useful for tests and for bootstrapping the API before real backends are wired.
#[derive(Debug, Default, Clone)]
pub struct StubBackend;

#[async_trait]
impl Backend for StubBackend {
    async fn complete(
        &self,
        auth: &AuthUser,
        request: ChatCompletionRequest,
    ) -> Result<GrpcChatCompletionResponse, ApiError> {
        let content = format!(
            "Hello {}, this is a stub response for model {}.",
            auth.user_id, request.model
        );
        let prompt_text: String = request
            .messages
            .iter()
            .map(|m| m.content_as_string())
            .collect::<Vec<_>>()
            .join("\n");
        let prompt_tokens =
            i32::try_from(prompt_text.split_whitespace().count()).unwrap_or(i32::MAX);
        let completion_tokens =
            i32::try_from(content.split_whitespace().count()).unwrap_or(i32::MAX);
        Ok(GrpcChatCompletionResponse {
            id: format!("stub-{}-complete", uuid::Uuid::new_v4()),
            object: "chat.completion".to_string(),
            created: chrono::Utc::now().timestamp(),
            choices: vec![ChatCompletionChoice {
                index: 0,
                chat_item: Some(ChatItem {
                    role: ChatRole::Assistant as i32,
                    content,
                }),
                finish_reason: ChatCompletionFinishReason::Stop as i32,
            }],
            usage: Some(Usage {
                prompt_tokens,
                completion_tokens,
                total_tokens: prompt_tokens.saturating_add(completion_tokens),
            }),
        })
    }

    async fn complete_stream(
        &self,
        auth: &AuthUser,
        request: ChatCompletionRequest,
    ) -> Result<BoxStream<'static, Result<GrpcChatCompletionResponse, ApiError>>, ApiError> {
        let content = format!(
            "Hello {}, this is a stub stream for model {}.",
            auth.user_id, request.model
        );
        let model = request.model;
        let user_id = auth.user_id.clone();
        let words: Vec<String> = content.split_whitespace().map(String::from).collect();
        let stream = tokio_stream::iter(words.into_iter().enumerate()).then(move |(idx, word)| {
            let user_id = user_id.clone();
            let _model = model.clone();
            async move {
                let partial = if idx == 0 {
                    format!("Hello {}, this", user_id)
                } else {
                    word
                };
                Ok(GrpcChatCompletionResponse {
                    id: format!("stub-{}-stream", uuid::Uuid::new_v4()),
                    object: "chat.completion.chunk".to_string(),
                    created: chrono::Utc::now().timestamp(),
                    choices: vec![ChatCompletionChoice {
                        index: 0,
                        chat_item: Some(ChatItem {
                            role: ChatRole::Assistant as i32,
                            content: partial,
                        }),
                        finish_reason: ChatCompletionFinishReason::None as i32,
                    }],
                    usage: None,
                })
            }
        });
        Ok(stream.boxed())
    }
}

#[allow(dead_code)]
fn build_grpc_request(_request: ChatCompletionRequest) -> GrpcChatCompletionRequest {
    GrpcChatCompletionRequest::default()
}
