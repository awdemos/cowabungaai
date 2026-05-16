import type { RequestHandler } from './$types';
import { error, json } from '@sveltejs/kit';
import type { LFThread } from '$lib/types/threads';
import { getThreadWithMessages } from '../helpers';
import { getProfileCookie } from '$lib/server/profileCookie';

export const GET: RequestHandler = async ({ cookies, locals: { session } }) => {
  if (!session) {
    error(401, 'Unauthorized');
  }

  const profile = getProfileCookie(cookies);

  const threads: LFThread[] = [];
  if (profile?.thread_ids && profile.thread_ids.length > 0) {
    try {
      const threadPromises = profile.thread_ids.map((thread_id) =>
        getThreadWithMessages(thread_id, session.access_token)
      );
      const results = await Promise.allSettled(threadPromises);
      results.forEach((result) => {
        if (result.status === 'fulfilled' && result.value) {
          threads.push(result.value);
        }
      });
    } catch (e) {
      console.error(`Error fetching threads: ${e}`);
      return json([]);
    }
  }

  return json(threads);
};
