<script lang="ts">
  import { onMount } from 'svelte';
  import Bateaux from './Bateaux.svelte';
  import Course from './Course.svelte';
  import Inscription from './Inscription.svelte';
  import Series from './Series.svelte';
  import ResultatsSeries from './ResultatsSeries.svelte';

  type Route = 'bateaux' | 'course' | 'inscription' | 'series' | 'resultats-series';

  let route: Route = 'bateaux';

  function parseRoute(): Route {
    const raw = (window.location.hash || '').replace(/^#\/?/, '');
    const key = raw.split('?')[0].split('/')[0];
    
    if (key === 'course') return 'course';
    if (key === 'inscription') return 'inscription';
    if (key === 'series') return 'series';
    if (key === 'resultats-series') return 'resultats-series';
    return 'bateaux'; // Default
  }

  function sync() {
    route = parseRoute();
  }

  // Permet de garder la compatibilité avec l'ancien système d'événements si nécessaire
  function handleNavigate(e: CustomEvent) {
    window.location.hash = e.detail;
  }

  onMount(() => {
    sync();
    window.addEventListener('hashchange', sync);
    return () => window.removeEventListener('hashchange', sync);
  });
</script>

{#if route === 'series'}
  <Series on:navigate={handleNavigate} />
{:else if route === 'resultats-series'}
  <ResultatsSeries on:navigate={handleNavigate} />
{:else if route === 'course'}
  <Course on:navigate={handleNavigate} />
{:else if route === 'inscription'}
  <Inscription on:navigate={handleNavigate} />
{:else}
  <Bateaux on:navigate={handleNavigate} />
{/if}