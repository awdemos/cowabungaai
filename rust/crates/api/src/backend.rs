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

/// A backend client that connects to gRPC model backend endpoints.
///
/// One connection (channel) is kept per model; unary and streaming service
/// clients are built on demand from the channel, so a single registration
/// supports both `complete` and `complete_stream`.
#[derive(Clone, Default)]
pub struct GrpcBackend {
    channels: HashMap<String, Channel>,
}

impl GrpcBackend {
    /// Create a backend with no configured endpoints. In a production deployment
    /// this would be populated from a config file or service discovery.
    pub fn new() -> Self {
        Self {
            channels: HashMap::new(),
        }
    }

    /// Register a backend endpoint for a model. Both the unary and streaming
    /// chat services are served from this one connection.
    pub async fn register(
        &mut self,
        model: impl Into<String>,
        dst: impl Into<tonic::transport::Endpoint>,
    ) -> Result<(), tonic::transport::Error> {
        let endpoint: tonic::transport::Endpoint = dst.into();
        let channel = endpoint.connect().await?;
        self.channels.insert(model.into(), channel);
        Ok(())
    }

    /// Whether a backend endpoint is registered for `model`.
    pub fn has_model(&self, model: &str) -> bool {
        self.channels.contains_key(model)
    }
}

/// Map an OpenAI role string onto the protobuf `ChatRole` enum.
fn role_to_proto(role: &str) -> ChatRole {
    match role {
        "system" => ChatRole::System,
        "user" => ChatRole::User,
        "function" => ChatRole::Function,
        _ => ChatRole::Assistant,
    }
}

fn build_grpc_request(request: &ChatCompletionRequest) -> GrpcChatCompletionRequest {
    let chat_items = request
        .messages
        .iter()
        .map(|message| ChatItem {
            role: role_to_proto(&message.role) as i32,
            content: message.content_as_string(),
        })
        .collect();
    let stop = match &request.stop {
        Some(stop) => vec![stop.clone()],
        None => Vec::new(),
    };
    GrpcChatCompletionRequest {
        chat_items,
        max_new_tokens: request.max_tokens,
        temperature: Some(request.temperature),
        top_k: None,
        top_p: Some(request.top_p),
        do_sample: None,
        n: None,
        stop,
        repetition_penalty: None,
        presence_penalty: None,
        frequency_penalty: None,
        best_of: None,
        logit_bias: Default::default(),
        return_full_text: None,
        truncate: None,
        typical_p: None,
        watermark: None,
        seed: None,
        user: None,
    }
}

#[async_trait]
impl Backend for GrpcBackend {
    async fn complete(
        &self,
        _auth: &AuthUser,
        request: ChatCompletionRequest,
    ) -> Result<GrpcChatCompletionResponse, ApiError> {
        let channel = self
            .channels
            .get(&request.model)
            .ok_or_else(|| ApiError::ModelNotAvailable(request.model.clone()))?;
        let mut client = ChatCompletionServiceClient::new(channel.clone());
        let response = client.chat_complete(build_grpc_request(&request)).await?;
        Ok(response.into_inner())
    }

    async fn complete_stream(
        &self,
        _auth: &AuthUser,
        request: ChatCompletionRequest,
    ) -> Result<BoxStream<'static, Result<GrpcChatCompletionResponse, ApiError>>, ApiError> {
        let channel = self
            .channels
            .get(&request.model)
            .ok_or_else(|| ApiError::ModelNotAvailable(request.model.clone()))?;
        let mut client = ChatCompletionStreamServiceClient::new(channel.clone());
        let response = client
            .chat_complete_stream(build_grpc_request(&request))
            .await?;
        let stream = response
            .into_inner()
            .map(|item| item.map_err(ApiError::Backend));
        Ok(stream.boxed())
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
