import type { RequestHandler } from './$types';
import { error } from '@sveltejs/kit';
import { getOpenAiClient } from '$lib/server/constants';
import { stringIdSchema } from '$schemas/chat';

export const DELETE: RequestHandler = async ({ request, locals: { session } }) => {
  if (!session) {
    error(401, 'Unauthorized');
  }

  let requestData: { id: string };

  // Validate request body
  try {
    requestData = await request.json();
    const isValid = await stringIdSchema.isValid(requestData);
    if (!isValid) error(400, 'Bad Request');
  } catch {
    error(400, 'Bad Request');
  }

  const openai = getOpenAiClient(session.access_token);

  // Retrieve assistant to check for avatar file
  let avatarFileId: string | null = null;
  try {
    const assistant = await openai.beta.assistants.retrieve(requestData.id);
    const avatarUrl = (assistant.metadata as Record<string, string> | undefined)?.avatar;
    if (avatarUrl && avatarUrl.startsWith('/api/files/')) {
      avatarFileId = avatarUrl.replace('/api/files/', '');
    }
  } catch (e) {
    console.error(`Error retrieving assistant before delete: ${e}`);
  }

  const assistantDeleted = await openai.beta.assistants.del(requestData.id);
  if (!assistantDeleted.deleted) {
    console.error(`error deleting assistant: ${JSON.stringify(assistantDeleted)}`);
    error(500, 'Error deleting assistant');
  }

  if (avatarFileId) {
    try {
      await openai.files.del(avatarFileId);
    } catch (e) {
      // fail silently
      console.error(`Error deleting assistant avatar file. AssistantId: ${requestData.id}, error: ${e}`);
    }
  }

  return new Response(undefined, { status: 204 });
};
