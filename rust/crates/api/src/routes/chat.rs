//! OpenAI-compatible chat completion endpoint.

use std::sync::Arc;

use axum::response::sse::Event;
use axum::{
    extract::{Extension, State},
    response::{IntoResponse, Json, Response, Sse},
};
use futures::stream::StreamExt;
use serde_json::Value;

use cowabunga_sdk::generated::chat::{ChatRole, Usage as GrpcUsage};

use crate::auth::AuthUser;
use crate::backend::{Backend, StubBackend};
use crate::error::ApiError;
use crate::state::AppState;
use crate::types::chat::{
    ChatChoice, ChatCompletionChunk, ChatCompletionRequest, ChatCompletionResponse, ChatDelta,
    ChatMessage, ChatStreamChoice, Usage,
};

pub async fn create_chat_completion(
    State(state): State<Arc<AppState>>,
    Extension(auth): Extension<AuthUser>,
    Json(body): Json<ChatCompletionRequest>,
) -> Result<Response, ApiError> {
    let model = body.model.clone();
    if state.model_registry.get(&model).is_none() {
        return Err(ApiError::ModelNotAvailable(model));
    }

    let backend: Arc<dyn Backend> = Arc::new(StubBackend);

    if body.stream {
        let stream = backend.complete_stream(&auth, body).await?;
        let stream = stream.map(move |result| match result {
            Ok(grpc_chunk) => {
                let item = grpc_chunk
                    .choices
                    .first()
                    .and_then(|c| c.chat_item.as_ref());
                let delta = item
                    .map(|i| ChatDelta {
                        role: Some(role_from_proto(i.role)),
                        content: Some(i.content.clone()),
                    })
                    .unwrap_or_default();
                let chunk = ChatCompletionChunk {
                    id: grpc_chunk.id,
                    object: "chat.completion.chunk",
                    created: grpc_chunk.created,
                    model: model.clone(),
                    choices: vec![ChatStreamChoice {
                        index: 0,
                        delta,
                        finish_reason: None,
                    }],
                    usage: None,
                };
                Event::default()
                    .json_data(chunk)
                    .map_err(|e| ApiError::Internal(e.into()))
            }
            Err(err) => Err(err),
        });

        let done = tokio_stream::iter(vec![Ok(Event::default().data("[DONE]"))]);
        Ok(Sse::new(stream.chain(done)).into_response())
    } else {
        let grpc_response = backend.complete(&auth, body).await?;
        let choice = grpc_response
            .choices
            .first()
            .ok_or_else(|| ApiError::Internal(anyhow::anyhow!("backend returned no choices")))?;
        let item = choice
            .chat_item
            .as_ref()
            .ok_or_else(|| ApiError::Internal(anyhow::anyhow!("backend returned no chat item")))?;

        let usage = grpc_response.usage.unwrap_or(GrpcUsage {
            prompt_tokens: 0,
            completion_tokens: 0,
            total_tokens: 0,
        });

        let response = ChatCompletionResponse {
            id: grpc_response.id,
            object: "chat.completion",
            created: grpc_response.created,
            model,
            choices: vec![ChatChoice {
                index: choice.index as usize,
                message: ChatMessage {
                    role: "assistant".to_string(),
                    content: Some(Value::String(item.content.clone())),
                    name: None,
                },
                finish_reason: Some("stop".to_string()),
            }],
            usage: Usage {
                prompt_tokens: usage.prompt_tokens,
                completion_tokens: usage.completion_tokens,
                total_tokens: usage.total_tokens,
            },
        };

        Ok(Json(response).into_response())
    }
}

fn role_from_proto(role: i32) -> String {
    match ChatRole::try_from(role) {
        Ok(ChatRole::System) => "system".to_string(),
        Ok(ChatRole::User) => "user".to_string(),
        Ok(ChatRole::Assistant) => "assistant".to_string(),
        Ok(ChatRole::Function) => "function".to_string(),
        _ => "assistant".to_string(),
    }
}
