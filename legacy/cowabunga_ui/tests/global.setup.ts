import { expect, test as setup } from './fixtures';
import * as OTPAuth from 'otpauth';
import { delay } from 'msw';
import type { Page } from '@playwright/test';

const doKeycloakLogin = async (page: Page) => {
  await page.goto('/'); // go to the home page
  await delay(2000); // allow page to fully hydrate
  // With Keycloak
  await page.getByRole('button', { name: 'Log In' }).click();
  await page.getByLabel('Username or email').fill(process.env.USERNAME!);
  await page.getByLabel('Password').click();
  await page.getByLabel('Password').fill(process.env.PASSWORD!);
  await page.getByRole('button', { name: 'Log In' }).click();

  if (process.env.TEST_ENV !== 'CI') {
    const totp = new OTPAuth.TOTP({
      issuer: 'Unicorn Delivery Service',
      algorithm: 'SHA1',
      digits: 6,
      period: 30,
      secret: process.env.MFA_SECRET!
    });
    const code = totp.generate();
    await page.getByLabel('Six digit code').fill(code);
    await page.getByRole('button', { name: 'Log In' }).click();
  }
};

const logout = async (page: Page) => {
  await expect(page).toHaveTitle('LeapfrogAI - Chat');
  await page.getByTestId('header-profile-btn').click();
  await page
    .getByTestId('profile-dropdown')
    .getByRole('button', { name: /log out/i })
    .click();

  await page.waitForURL('/');

  const loginBtn = page.getByRole('button', { name: /Log In with UDS SSO/i });
  await expect(loginBtn).toBeVisible();
  await loginBtn.click();
  await page.waitForURL(`**/*/realms/uds/**/*`); // ensure full logout of keycloak
};

setup('authenticate', async ({ page }) => {
  page.on('pageerror', (err) => {
    console.error('page error');
    console.error(err.message);
  });

  await doKeycloakLogin(page);

  // Wait until the page receives the cookies.
  await page.waitForURL('/chat');

  if (!process.env.SKIP_LOGOUT_TEST) {
    // First test log out, then log back in and continue.
    await logout(page);

    await delay(31000); // prevent logging back in too quickly and getting denied
    // Log back in to begin rest of tests
    await doKeycloakLogin(page);

    await page.waitForURL('/chat');
  }

  await page.context().storageState({ path: 'playwright/.auth/user.json' });
});
