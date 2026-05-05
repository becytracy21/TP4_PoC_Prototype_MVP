<script lang="ts">
  import { onMount } from 'svelte';

  import Bateaux from './Bateaux.svelte';
  import Inscription from './Inscription.svelte';
  import Connexion from './Connexion.svelte';

  import { route, navigate } from './router';
  import { auth, isAuthenticated } from './auth';

  const TITLE_SUFFIX = 'YRR';
  function titleFor(r: string) {
    if (r === 'bateaux') return `Bateaux | ${TITLE_SUFFIX}`;
    if (r === 'inscription') return `Inscription | ${TITLE_SUFFIX}`;
    return `Connexion | ${TITLE_SUFFIX}`;
  }

  onMount(() => {
    if (window.location.pathname === '/' || window.location.pathname === '') {
      navigate(isAuthenticated($auth) ? 'bateaux' : 'connexion');
    }
  });

  // Titre de page
  $: document.title = titleFor($route);

  // Garde d'accès
  $: if ($route === 'bateaux' && !isAuthenticated($auth)) {
    navigate('connexion');
  }
</script>

{#if $route === 'connexion'}
  <Connexion />
{:else if $route === 'inscription'}
  <Inscription onSuccess={() => navigate('bateaux')} />
{:else}
  <Bateaux />
{/if}