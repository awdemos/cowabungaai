import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async ({ locals: { safeGetSession, isUsingOpenAI } }) => {
  const { session, user } = await safeGetSession();
  return { session, user, isUsingOpenAI };
};
