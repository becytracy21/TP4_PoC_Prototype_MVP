<script lang="ts">
  import { onMount } from 'svelte';
  import Layout from './lib/Layout.svelte';
  import Bateaux from './Bateaux.svelte';
  import Classes from './Classes.svelte';
  import Course from './Course.svelte';
  import Inscriptions from './Inscriptions.svelte';
  import Series from './Series.svelte';
  import ResultatsSeries from './ResultatsSeries.svelte';

  type Route = 'bateaux' | 'classes' | 'course' | 'inscriptions' | 'series' | 'resultats-series';

  let route: Route = 'bateaux';

  function parseRoute(): Route {
    const path = window.location.pathname.replace(/^\//, '').toLowerCase();
    if (path === '') return 'bateaux';
    if (path === 'classes') return 'classes';
    if (path === 'course') return 'course';
    if (path === 'inscriptions') return 'inscriptions';
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
  <Layout active="series" on:navigate={handleNavigate}>
    <Series on:navigate={handleNavigate} />
  </Layout>
{:else if route === 'resultats-series'}
  <Layout active="resultats-series" on:navigate={handleNavigate}>
    <ResultatsSeries on:navigate={handleNavigate} />
  </Layout>
{:else if route === 'course'}
  <Layout active="course" on:navigate={handleNavigate}>
    <Course on:navigate={handleNavigate} />
  </Layout>
{:else if route === 'inscriptions'}
  <Layout active="inscriptions" on:navigate={handleNavigate}>
    <Inscriptions on:navigate={handleNavigate} />
  </Layout>
{:else if route === 'classes'}
  <Layout active="classes" on:navigate={handleNavigate}>
    <Classes onBack={() => {
      window.history.pushState({}, '', '/Bateaux');
      sync();
    }} />
  </Layout>
{:else}
  <Layout active="bateaux" on:navigate={handleNavigate}>
    <Bateaux on:navigate={handleNavigate} />
  </Layout>
{/if}