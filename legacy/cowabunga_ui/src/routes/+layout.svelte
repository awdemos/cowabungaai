<script lang="ts">
  import '../app.css';
  import { onMount } from 'svelte';
  import { Toasts } from '$components';
  import { page } from '$app/stores';
  import '$webComponents/CodeBlock';
  import { filesStore, uiStore } from '$stores';
  import vectorStatusStore from '$stores/vectorStatusStore';

  export let data;

  let { session } = data;
  $: ({ session } = data);

  onMount(() => {
    // Any client-side initialization can go here
    return () => {
      // Cleanup
    };
  });
</script>

<svelte:head>
  <title>{$page.data.title || ''}</title>
</svelte:head>

<Toasts />
<div class="flex h-screen flex-col bg-gray-900">
  <slot />
</div>
