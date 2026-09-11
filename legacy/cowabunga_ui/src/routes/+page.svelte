<script lang="ts">
  import logo from '$assets/LeapfrogAI.png';
  import { Button } from 'flowbite-svelte';
  import { env } from '$env/dynamic/public';

  export let data;

  let { url } = data;
  $: ({ url } = data);

  function signInWithKeycloak() {
    const keycloakUrl = env.PUBLIC_KEYCLOAK_URL;
    const clientId = env.PUBLIC_KEYCLOAK_CLIENT_ID;
    if (!keycloakUrl || !clientId) {
      console.error('Keycloak URL or Client ID is not configured');
      return;
    }
    const redirectUri = `${url}/auth/callback`;
    const authUrl = new URL(`${keycloakUrl}/protocol/openid-connect/auth`);
    authUrl.searchParams.set('client_id', clientId);
    authUrl.searchParams.set('redirect_uri', redirectUri);
    authUrl.searchParams.set('response_type', 'code');
    authUrl.searchParams.set('scope', 'openid');
    window.location.href = authUrl.toString();
  }
</script>

<div class="flex w-full flex-col items-center gap-10 pt-3">
  <div class="h-[72px] w-[252px]">
    <img alt="LeapfrogAI Logo" src={logo} class="logo" />
  </div>
  <Button on:click={signInWithKeycloak}>Log In with UDS SSO</Button>
  <form method="POST" action="/auth/local" class="flex flex-col gap-2 w-72">
    <input name="username" placeholder="username" class="h-10 rounded border border-gray-400 px-3 text-black" required />
    <input name="password" type="password" placeholder="password" class="h-10 rounded border border-gray-400 px-3 text-black" required />
    <Button type="submit">Log In</Button>
  </form>
</div>
