import { faker } from '@faker-js/faker';
import { POST } from './+server';
import { MAX_LABEL_SIZE } from '$lib/constants';
import { getFakeThread } from '$testUtils/fakeData';
import { mockOpenAI } from '../../../../../vitest-setup';
import { getLocalsMock, getCookiesMock } from '$lib/mocks/misc';
import type { RequestEvent } from '@sveltejs/kit';
import type { RouteParams } from '../../../../../.svelte-kit/types/src/routes/api/messages/new/$types';

const thread = getFakeThread();
const validLabel = faker.string.alpha({ length: MAX_LABEL_SIZE - 1 });
const invalidLongLabel = faker.string.alpha({ length: MAX_LABEL_SIZE + 1 });
const fakeProfile = { thread_ids: ['thread_1'] };

describe('/api/threads/new', () => {
  it('returns a 200 when successful and updates the users profile with the new thread id', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'POST',
      body: JSON.stringify({ label: thread.metadata.label })
    });

    mockOpenAI.setTempThread(thread);

    const cookies = getCookiesMock(fakeProfile);

    const res = await POST({
      request,
      cookies,
      locals: getLocalsMock()
    } as unknown as RequestEvent<RouteParams, '/api/threads/new'>);

    const resData = await res.json();
    expect(res.status).toEqual(200);
    expect(resData).toEqual(thread);

    expect(cookies.set).toHaveBeenCalled();
    const profileCookie = cookies._store['cowabunga-profile'];
    expect(profileCookie).toBeDefined();
    const parsed = JSON.parse(Buffer.from(profileCookie, 'base64').toString('utf-8'));
    expect(parsed.thread_ids).toHaveLength(2);
  });

  it('returns a 401 when there is no session', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'POST',
      body: JSON.stringify({ label: validLabel })
    });

    await expect(
      POST({
        request,
        cookies: getCookiesMock(),
        locals: getLocalsMock({ nullSession: true })
      } as unknown as RequestEvent<RouteParams, '/api/threads/new'>)
    ).rejects.toMatchObject({
      status: 401
    });
  });

  it('returns a 400 when label is too long', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'POST',
      body: JSON.stringify({ label: invalidLongLabel })
    });

    await expect(
      POST({
        request,
        cookies: getCookiesMock(),
        locals: getLocalsMock()
      } as unknown as RequestEvent<RouteParams, '/api/threads/new'>)
    ).rejects.toMatchObject({
      status: 400
    });
  });
  it('returns a 400 when label is missing', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'POST'
    });

    await expect(
      POST({
        request,
        cookies: getCookiesMock(),
        locals: getLocalsMock()
      } as unknown as RequestEvent<RouteParams, '/api/threads/new'>)
    ).rejects.toMatchObject({
      status: 400
    });
  });
  it('returns a 400 when extra body arguments are passed', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'POST',
      body: JSON.stringify({ label: validLabel, wrong: 'key' })
    });

    await expect(
      POST({
        request,
        cookies: getCookiesMock(),
        locals: getLocalsMock()
      } as unknown as RequestEvent<RouteParams, '/api/threads/new'>)
    ).rejects.toMatchObject({
      status: 400
    });
  });

  it('returns a 500 when there is an openai error', async () => {
    mockOpenAI.setError('createThread');
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'POST',
      body: JSON.stringify({ label: thread.metadata.label })
    });
    await expect(
      POST({
        request,
        cookies: getCookiesMock(fakeProfile),
        locals: getLocalsMock()
      } as unknown as RequestEvent<RouteParams, '/api/threads/new'>)
    ).rejects.toMatchObject({
      status: 500
    });
  });
});
