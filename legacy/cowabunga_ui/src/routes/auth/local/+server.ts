import type { RequestHandler } from './$types';
import { redirect } from '@sveltejs/kit';
import { env as envPrivate } from '$env/dynamic/private';

const SESSION_COOKIE = 'cowabunga-session';

function base64UrlEncode(obj: Record<string, unknown>): string {
	return Buffer.from(JSON.stringify(obj))
		.toString('base64')
		.replace(/\+/g, '-')
		.replace(/\//g, '_')
		.replace(/=+$/, '');
}

function mintIdToken(claims: Record<string, unknown>): string {
	const header = base64UrlEncode({ alg: 'none', typ: 'JWT' });
	const payload = base64UrlEncode(claims);
	return `${header}.${payload}.${base64UrlEncode({ alg: 'none', sig: 'local' })}`;
}

export const POST: RequestHandler = async ({ request, cookies, url }) => {
	const form = await request.formData();
	const username = String(form.get('username') ?? '').trim();
	const password = String(form.get('password') ?? '');

	const expectedUser = envPrivate.LOCAL_AUTH_USER;
	const expectedPassword = envPrivate.LOCAL_AUTH_PASSWORD;

	if (!expectedUser || !expectedPassword) {
		throw redirect(303, '/?error=local_auth_not_configured');
	}

	if (username !== expectedUser || password !== expectedPassword) {
		throw redirect(303, '/?error=invalid_credentials');
	}

	const nowSeconds = Math.floor(Date.now() / 1000);
	const expiresInSeconds = 12 * 60 * 60;

	const session = {
		access_token: mintIdToken({ sub: expectedUser, exp: nowSeconds + expiresInSeconds }),
		refresh_token: null,
		expires_in: expiresInSeconds,
		expires_at: nowSeconds + expiresInSeconds,
		token_type: 'bearer',
		provider_token: null,
		provider_refresh_token: null,
		user: {
			id: expectedUser,
			email: `${expectedUser}@localhost`,
			user_metadata: {
				name: expectedUser,
				full_name: expectedUser,
				email_verified: true,
				sub: expectedUser,
				provider_id: expectedUser
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
};
