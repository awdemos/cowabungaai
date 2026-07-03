import { faker } from '@faker-js/faker';
import { vi } from 'vitest';

type GetLocalsMockParams = {
  nullSession?: boolean;
};
export const getLocalsMock = (params: GetLocalsMockParams = {}) => {
  const { nullSession = false } = params;

  const id = faker.string.uuid();
  const email = faker.internet.email();
  const full_name = faker.person.fullName();
  const currentDate = new Date();
  const yesterday = new Date(
    currentDate.getFullYear(),
    currentDate.getMonth(),
    currentDate.getDate() - 1
  );

  const user = {
    id,
    aud: 'authenticated',
    role: 'authenticated',
    email,
    app_metadata: { provider: 'keycloak', providers: ['keycloak'] },
    user_metadata: {
      email,
      email_verified: true,
      full_name,
      iss: 'https://sso.uds.dev/realms/uds',
      name: full_name,
      phone_verified: false,
      provider_id: faker.string.uuid(),
      sub: faker.string.uuid()
    },
    created_at: yesterday.toISOString()
  };

  const session = nullSession
    ? null
    : {
        access_token: 'abc',
        refresh_token: 'abc',
        expires_in: 3600,
        token_type: 'bearer',
        user
      };

  return {
    user,
    session,
    safeGetSession: () => Promise.resolve({ session, user }),
    isUsingOpenAI: false
  };
};

export const getCookiesMock = (profile?: { thread_ids: string[] }) => {
  const store: Record<string, string> = {};
  if (profile) {
    store['cowabunga-profile'] = Buffer.from(JSON.stringify(profile)).toString('base64');
  }
  return {
    get: (name: string) => store[name] || undefined,
    set: vi.fn((name: string, value: string, _opts?: unknown) => {
      store[name] = value;
    }),
    delete: vi.fn((name: string, _opts?: unknown) => {
      delete store[name];
    }),
    _store: store
  };
};
