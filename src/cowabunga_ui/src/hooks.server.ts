import { type Handle, redirect } from '@sveltejs/kit';
import { sequence } from '@sveltejs/kit/hooks';
import { env as envPrivate } from '$env/dynamic/private';

const SESSION_COOKIE = 'cowabunga-session';

const getSessionFromCookies = (cookies: import('@sveltejs/kit').Cookies) => {
  const sessionCookie = cookies.get(SESSION_COOKIE);
  if (!sessionCookie) {
    return { session: null, user: null };
  }
  try {
    const session = JSON.parse(Buffer.from(sessionCookie, 'base64').toString('utf-8'));
    if (!session || !session.access_token || !session.user) {
      return { session: null, user: null };
    }
    return { session, user: session.user };
  } catch {
    return { session: null, user: null };
  }
};

const auth: Handle = async ({ event, resolve }) => {
  event.locals.safeGetSession = async () => getSessionFromCookies(event.cookies);

  const { session, user } = await event.locals.safeGetSession();
  event.locals.session = session;
  event.locals.user = user;
  event.locals.isUsingOpenAI = !!envPrivate.OPENAI_API_KEY;

  return resolve(event);
};

const authGuard: Handle = async ({ event, resolve }) => {
  const { session } = await event.locals.safeGetSession();
  event.locals.session = session;

  // protect all routes under /chat
  if (!event.locals.session && event.url.pathname.startsWith('/chat')) {
    redirect(303, '/');
  }

  // if already authenticated, redirect to /chat
  if (event.locals.session && event.url.pathname === '/') {
    redirect(303, '/chat');
  }

  return resolve(event);
};

const csp: Handle = async ({ event, resolve }) => {
  const response = await resolve(event);
  const directives = {
    'default-src': ["'none'"],
    'base-uri': ["'self'"],
    'object-src': ["'none'"], // typically used for legacy content, such as Flash files or Java applets
    'style-src': ["'self'", "'unsafe-inline'"],
    'font-src': ["'self'"],
    'manifest-src': ["'self'"],
    'img-src': ["'self'", "data: 'self'", "blob: 'self'"],
    'media-src': ["'self'"],
    'form-action': ["'self'"],
    'connect-src': [
      "'self'",
      process.env.LEAPFROGAI_API_BASE_URL,
      process.env.PUBLIC_KEYCLOAK_URL
    ],
    'child-src': ["'none'"],
    'frame-src': ["blob: 'self'"],
    'frame-ancestors': ["'none'"]
  };

  const CSP = Object.entries(directives)
    .map(([key, arr]) => key + ' ' + arr.join(' '))
    .join('; ');
  // We use Sveltekits generated CSP for script-src to get the nonce
  const svelteKitGeneratedCSPWithNonce = response.headers.get('Content-Security-Policy');
  response.headers.set('Content-Security-Policy', `${CSP}; ${svelteKitGeneratedCSPWithNonce}`);
  return response;
};

export const handle: Handle = sequence(csp, auth, authGuard);
