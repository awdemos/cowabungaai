import type { Actions } from './$types';
import { redirect } from '@sveltejs/kit';
import { env as envPublic } from '$env/dynamic/public';
import { env as envPrivate } from '$env/dynamic/private';

const SESSION_COOKIE = 'cowabunga-session';

export const actions: Actions = {
  signout: async ({ cookies, locals: { session } }) => {
    if (session) {
      if (session.provider_refresh_token) {
        const params = new URLSearchParams();
        params.append('client_id', envPublic.PUBLIC_KEYCLOAK_CLIENT_ID || '');
        params.append('client_secret', envPrivate.KEYCLOAK_CLIENT_SECRET || '');
        params.append('refresh_token', session.provider_refresh_token);

        const res = await fetch(
          `${envPublic.PUBLIC_KEYCLOAK_URL}/protocol/openid-connect/logout`,
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: params
          }
        );
        if (res.status !== 204) {
          console.error('Failed to logout from Keycloak', res.status, res.statusText);
        }
      }

      cookies.delete(SESSION_COOKIE, { path: '/' });
      throw redirect(303, '/');
    }
  }
};
