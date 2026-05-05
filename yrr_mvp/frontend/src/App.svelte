<script lang="ts">
  import { onMount } from 'svelte';

  import Bateaux from './Bateaux.svelte';
  import Inscription from './Inscription.svelte';
  import Connexion from './Connexion.svelte';

  import { route, navigate } from './router';

  onMount(() => {
    if (window.location.pathname === '/' || window.location.pathname === '') {
      navigate('connexion');
    }
  });
</script>

{#if $route === 'connexion'}
  <Connexion />
{:else if $route === 'inscription'}
  <Inscription onSuccess={() => navigate('bateaux')} />
{:else}
  <Bateaux />
{/if}