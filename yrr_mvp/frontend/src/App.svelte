<script lang="ts">
  import { onMount } from 'svelte';
  import Bateaux from './Bateaux.svelte';
  import Series from './Series.svelte';
  import ResultatsSeries from './ResultatsSeries.svelte';

  type Route = 'bateaux' | 'series' | 'resultats-series';

  let route: Route = 'bateaux';

  function parseRoute(): Route {
    const raw = (window.location.hash || '').replace(/^#\/?/, '');
    const key = raw.split('?')[0].split('/')[0];
    if (key === 'series') return 'series';
    if (key === 'resultats-series') return 'resultats-series';
    if (key === 'bateaux' || key === '' || key === '/') return 'bateaux';
    return 'bateaux';
  }

  function sync() {
    route = parseRoute();
  }

  onMount(() => {
    sync();
    window.addEventListener('hashchange', sync);
    return () => window.removeEventListener('hashchange', sync);
  });
</script>

{#if route === 'series'}
  <Series />
{:else if route === 'resultats-series'}
  <ResultatsSeries />
{:else}
  <Bateaux />
{/if}