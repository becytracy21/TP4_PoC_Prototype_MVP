<script lang="ts">
  import { onMount } from 'svelte';

  import Bateaux from './Bateaux.svelte';
  import Inscription from './Inscription.svelte';

  import { route, navigate } from './router';

  onMount(() => {
    if (window.location.pathname === '/' || window.location.pathname === '') {
      navigate('inscription');
    }
  });
</script>

{#if $route === 'inscription'}
  <Inscription onSuccess={() => navigate('bateaux')} />
{:else}
  <Bateaux />
{/if}