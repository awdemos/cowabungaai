import type { RequestHandler } from './$types';
import { error, json } from '@sveltejs/kit';
import { newThreadInputSchema } from '$lib/schemas/chat';
import { getOpenAiClient } from '$lib/server/constants';
import type { Thread } from 'openai/resources/beta/threads/threads';
import { getProfileCookie, setProfileCookie } from '$lib/server/profileCookie';

export const POST: RequestHandler = async ({ request, cookies, locals: { session } }) => {
  if (!session) {
    error(401, 'Unauthorized');
  }

  // Validate request body
  let requestData: { label: string };
  try {
    requestData = await request.json();
    const isValid = await newThreadInputSchema.isValid(requestData);
    if (!isValid) error(400, 'Bad Request');
  } catch {
    error(400, 'Bad Request');
  }

  let newThread: Thread;
  try {
    const openai = getOpenAiClient(session.access_token);

    newThread = await openai.beta.threads.create({
      metadata: { user_id: session.user.id, label: requestData.label }
    });
  } catch (e) {
    console.error(`Error creating thread: ${e}`);
    error(500, 'Error creating thread');
  }

  const profile = getProfileCookie(cookies);
  const updatedThreadIds = profile?.thread_ids
    ? [...profile.thread_ids, newThread.id]
    : [newThread.id];

  setProfileCookie(cookies, { thread_ids: updatedThreadIds });

  return json(newThread);
};
