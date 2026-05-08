<script lang="ts">
  import { onMount } from 'svelte';
  import Bateaux from './Bateaux.svelte';
  import Course from './Course.svelte';
  import Inscriptions from './Inscriptions.svelte';
  import Series from './Series.svelte';
  import ResultatsSeries from './ResultatsSeries.svelte';

  type Route = 'bateaux' | 'course' | 'inscriptions' | 'series' | 'resultats-series';

  let route: Route = 'bateaux';

  function parseRoute(): Route {
    const path = window.location.pathname.replace(/^\//, '').toLowerCase();
    if (path === '' || path === 'accueil') return 'bateaux';
    if (path === 'course') return 'course';
    if (path === 'inscriptions') return 'inscriptions'; // Correction ici
    if (path === 'series') return 'series';
    if (path === 'resultatsseries' || path === 'resultats-series') return 'resultats-series';
    if (path === 'bateaux') return 'bateaux';
    return 'bateaux'; // Par défaut
  }

  function sync() {
    // Redirige la racine vers /Bateaux
    if (window.location.pathname === '/' || window.location.pathname === '') {
      window.history.replaceState({}, '', '/Bateaux');
      route = 'bateaux';
      return;
    }
    route = parseRoute();
  }

  function handleNavigate(e: CustomEvent) {
    // e.detail = path (ex: '/Course')
    const path = e.detail.startsWith('/') ? e.detail : '/' + e.detail;
    window.history.pushState({}, '', path);
    sync();
  }

  onMount(() => {
    sync();
    window.addEventListener('popstate', sync);
    return () => window.removeEventListener('popstate', sync);
  });
</script>

{#if route === 'series'}
  <Series on:navigate={handleNavigate} />
{:else if route === 'resultats-series'}
  <ResultatsSeries on:navigate={handleNavigate} />
{:else if route === 'course'}
  <Course on:navigate={handleNavigate} />
{:else if route === 'inscriptions'}
  <Inscriptions on:navigate={handleNavigate} />
{:else}
  <Bateaux on:navigate={handleNavigate} />
{/if}