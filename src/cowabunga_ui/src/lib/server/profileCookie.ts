import type { Cookies } from '@sveltejs/kit';

const PROFILE_COOKIE = 'cowabunga-profile';

export type ProfileCookie = {
  thread_ids: string[];
};

export const getProfileCookie = (cookies: Cookies): ProfileCookie => {
  const raw = cookies.get(PROFILE_COOKIE);
  if (!raw) return { thread_ids: [] };
  try {
    return JSON.parse(Buffer.from(raw, 'base64').toString('utf-8'));
  } catch {
    return { thread_ids: [] };
  }
};

export const setProfileCookie = (cookies: Cookies, profile: ProfileCookie) => {
  cookies.set(PROFILE_COOKIE, Buffer.from(JSON.stringify(profile)).toString('base64'), {
    path: '/',
    httpOnly: true,
    sameSite: 'lax',
    secure: false
  });
};
