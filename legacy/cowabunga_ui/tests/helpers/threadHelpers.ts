import { expect, type Page } from '@playwright/test';
import OpenAI from 'openai';

export const clickToDeleteThread = async (page: Page, label: string) => {
  const threads = page.getByTestId('threads');
  await threads.getByText(label).hover();
  await page.getByTestId(`thread-menu-btn-${label}`).click();
  await page.getByRole('button', { name: /delete/i }).click();
  const deleteBtns = await page.getByRole('button', { name: /delete/i }).all();
  await deleteBtns[1].click(); // confirm delete in modal
  await expect(page.getByTestId(`thread-menu-btn-${label}`)).toHaveCount(0);
};

export const sendMessage = async (page: Page, message = 'Who are Defense Unicorns?') => {
  const chatInput = page.getByTestId('chat-input');
  await expect(chatInput).toBeVisible();
  await chatInput.fill(message);
  await page.getByTestId('send message').click();
};

export const getLastUrlParam = (page: Page) => {
  const urlParts = new URL(page.url()).pathname.split('/');
  return urlParts[urlParts.length - 1];
};
export const deleteActiveThread = async (page: Page, openAIClient: OpenAI) => {
  const threadId = getLastUrlParam(page);

  if (threadId && threadId !== 'chat') {
    await deleteThread(threadId, openAIClient);
  }
};

export const deleteThread = async (id: string, openAIClient: OpenAI) => {
  await openAIClient.beta.threads.del(id);
};
export const waitForResponseToComplete = async (page: Page) => {
  await expect(page.getByTestId('cancel message')).toHaveCount(1, { timeout: 60000 });
  await expect(page.getByTestId('cancel message')).toHaveCount(0, { timeout: 60000 });
  await expect(page.getByTestId('send message')).toHaveCount(1, { timeout: 60000 });
};

export const deleteAllThreads = async (openAIClient: OpenAI) => {
  try {
    // Note: thread list is now tracked client-side in a cookie.
    // We attempt to delete any threads that may have been created during tests.
    // This is a best-effort cleanup.
    console.log('Skipping comprehensive thread cleanup: thread list is client-side only.');
  } catch (e) {
    console.error(`Error deleting test threads`, e);
  }
};
