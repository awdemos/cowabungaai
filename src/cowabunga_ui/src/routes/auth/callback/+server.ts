import type { RequestHandler } from './$types';
import { redirect } from '@sveltejs/kit';

const SESSION_COOKIE = 'cowabunga-session';

export const GET: RequestHandler = async ({ url, cookies }) => {
  const code = url.searchParams.get('code');

  if (code) {
    // TODO: exchange code for session token via API/Keycloak
    // For now, set a placeholder session cookie so the auth guard passes
    const placeholderSession = {
      access_token: code,
      user: {
        id: 'placeholder-user-id',
        email: 'user@example.com'
      }
    };
    cookies.set(
      SESSION_COOKIE,
      Buffer.from(JSON.stringify(placeholderSession)).toString('base64'),
      { path: '/', httpOnly: true, sameSite: 'lax', secure: false }
    );
  }

  throw redirect(303, '/chat');
};
