import { redirect } from '@sveltejs/kit';

import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({ url }) => {
  const next = url.searchParams.get('next') ?? '/';
  redirect(303, next);
};
