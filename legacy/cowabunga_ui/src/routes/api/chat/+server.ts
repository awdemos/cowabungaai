import type { RequestHandler } from './$types';
import { streamText } from 'ai';
import { createOpenAI } from '@ai-sdk/openai';
import { env } from '$env/dynamic/private';
import { error } from '@sveltejs/kit';
import { getMessageText } from '$helpers/threads';
import type { LFMessage } from '$lib/types/messages';
import { AIMessagesInputSchema } from '$schemas/messageSchema';

export const POST: RequestHandler = async ({ request, locals: { session } }) => {
  if (!session) {
    error(401, 'Unauthorized');
  }

  let messages;
  // Validate request body
  try {
    const requestBody = await request.json();
    const isValid = await AIMessagesInputSchema.isValid(requestBody);
    if (!isValid) error(400, 'Bad Request');
    messages = requestBody.messages;
  } catch {
    error(400, 'Bad Request');
  }

  // We have to use the Vercel AI SDK createOpenAI helper here instead of our internal getOpenAiClient for streaming to
  // work (Vercel AI uses a slightly different type of provider)
  // Direct-to-TensorZero chat: TZ serves an OpenAI-compatible streaming
  // endpoint; model names are `tensorzero::model_name::<model>`. Falls back
  // to the platform API when CHAT_API_BASE_URL is not set.
  const chatBase = env.CHAT_API_BASE_URL
    ? env.CHAT_API_BASE_URL
    : env.OPENAI_API_KEY
      ? `${env.LEAPFROGAI_API_BASE_URL}/v1`
      : `${env.LEAPFROGAI_API_BASE_URL}/openai/v1`;
  const apiKey = env.CHAT_API_KEY
    ? env.CHAT_API_KEY
    : env.OPENAI_API_KEY
      ? env.OPENAI_API_KEY
      : session.access_token;
  const openai = createOpenAI({ apiKey, baseURL: chatBase });

  const reformatedMessages = messages.map((message: LFMessage) => ({
    ...message,
    content: getMessageText(message)
  }));

  const result = await streamText({
    model: openai(env.DEFAULT_MODEL),
    messages: reformatedMessages,
    system: env.DEFAULT_SYSTEM_PROMPT
  });

  return result.toDataStreamResponse();
};
