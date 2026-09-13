import type { RequestHandler } from './$types';
import { redirect } from '@sveltejs/kit';
import { env as envPublic } from '$env/dynamic/public';
import { env as envPrivate } from '$env/dynamic/private';

const SESSION_COOKIE = 'cowabunga-session';

/**
 * Decode a base64url-encoded string to UTF-8.
 * JWT payloads use base64url encoding (RFC 4648 §5).
 */
function base64UrlDecode(str: string): string {
  let base64 = str.replace(/-/g, '+').replace(/_/g, '/');
  while (base64.length % 4) {
    base64 += '=';
  }
  return Buffer.from(base64, 'base64').toString('utf-8');
}

/**
 * Decode the payload of a JWT id_token without verifying the signature.
 * Returns the claims object or null if decoding fails.
 */
function decodeIdToken(idToken: string): Record<string, unknown> | null {
  const parts = idToken.split('.');
  if (parts.length !== 3) return null;
  try {
    return JSON.parse(base64UrlDecode(parts[1]));
  } catch {
    return null;
  }
}

export const GET: RequestHandler = async ({ url, cookies }) => {
  const code = url.searchParams.get('code');

  if (!code) {
    throw redirect(303, '/?error=missing_code');
  }

  const keycloakUrl = envPublic.PUBLIC_KEYCLOAK_URL;
  const clientId = envPublic.PUBLIC_KEYCLOAK_CLIENT_ID;
  const clientSecret = envPrivate.KEYCLOAK_CLIENT_SECRET;

  if (!keycloakUrl || !clientId || !clientSecret) {
    console.error('Missing Keycloak configuration');
    throw redirect(303, '/?error=configuration');
  }

  const redirectUri = `${url.origin}/auth/callback`;

  const params = new URLSearchParams();
  params.append('grant_type', 'authorization_code');
  params.append('code', code);
  params.append('redirect_uri', redirectUri);
  params.append('client_id', clientId);
  params.append('client_secret', clientSecret);

  try {
    const res = await fetch(`${keycloakUrl}/protocol/openid-connect/token`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: params
    });

    if (!res.ok) {
      const errorBody = await res.text().catch(() => res.statusText);
      console.error('Token exchange failed:', res.status, errorBody);
      throw redirect(303, '/?error=token_exchange');
    }

    const tokenData = await res.json();
    const { access_token, refresh_token, id_token, expires_in, token_type } = tokenData;

    if (!access_token || !id_token) {
      console.error('Missing tokens in Keycloak response');
      throw redirect(303, '/?error=invalid_token_response');
    }

    const claims = decodeIdToken(id_token);
    if (!claims) {
      console.error('Failed to decode id_token');
      throw redirect(303, '/?error=invalid_id_token');
    }

    const userId = String(claims.sub || '');
    const email = claims.email ? String(claims.email) : undefined;
    const name = claims.name
      ? String(claims.name)
      : claims.preferred_username
        ? String(claims.preferred_username)
        : undefined;
    const fullName = claims.name ? String(claims.name) : undefined;
    const emailVerified = Boolean(claims.email_verified);

    if (!userId) {
      console.error('Missing sub claim in id_token');
      throw redirect(303, '/?error=missing_user_id');
    }

    const nowSeconds = Math.floor(Date.now() / 1000);
    const expiresInNum = typeof expires_in === 'number' ? expires_in : 0;

    const session = {
      access_token,
      refresh_token: refresh_token || null,
      expires_in: expiresInNum,
      expires_at: nowSeconds + expiresInNum,
      token_type: token_type || 'bearer',
      provider_token: null,
      provider_refresh_token: refresh_token || null,
      user: {
        id: userId,
        email,
        user_metadata: {
          name,
          full_name: fullName,
          email_verified: emailVerified,
          sub: userId,
          iss: claims.iss ? String(claims.iss) : undefined,
          provider_id: userId
        }
      }
    };

    cookies.set(SESSION_COOKIE, Buffer.from(JSON.stringify(session)).toString('base64'), {
      path: '/',
      httpOnly: true,
      sameSite: 'lax',
      secure: url.protocol === 'https:'
    });

    throw redirect(303, '/chat');
  } catch (error) {
    // Re-throw SvelteKit redirects so they are not caught as generic errors
    if (error instanceof Response && error.status === 303) {
      throw error;
    }
    console.error('Auth callback error:', error);
    throw redirect(303, '/?error=auth_failed');
  }
};
