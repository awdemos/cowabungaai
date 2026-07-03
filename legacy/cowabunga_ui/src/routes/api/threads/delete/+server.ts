import type { RequestHandler } from './$types';
import { error } from '@sveltejs/kit';
import { getOpenAiClient } from '$lib/server/constants';
import { stringIdSchema } from '$schemas/chat';
import { getProfileCookie, setProfileCookie } from '$lib/server/profileCookie';

export const DELETE: RequestHandler = async ({ request, cookies, locals: { session } }) => {
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

  const threadDeleted = await openai.beta.threads.del(requestData.id);

  if (!threadDeleted.deleted) {
    console.error(`Unable to delete thread: ${JSON.stringify(threadDeleted)}`);
    error(500, 'Unable to delete thread');
  }

  const profile = getProfileCookie(cookies);
  const updatedThreadIds = profile?.thread_ids.filter((id) => id !== requestData.id) ?? [];

  setProfileCookie(cookies, { thread_ids: updatedThreadIds });

  return new Response(undefined, { status: 204 });
};
