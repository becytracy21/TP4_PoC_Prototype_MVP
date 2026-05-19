<script lang="ts">
  import { onMount } from 'svelte';
  import { get } from 'svelte/store';

  import Layout from './lib/Layout.svelte';
  import Bateaux from './Bateaux.svelte';
  import Classes from './Classes.svelte';
  import Course from './Course.svelte';
  import Inscriptions from './Inscriptions.svelte';
  import Series from './Series.svelte';
  import ResultatsSeries from './ResultatsSeries.svelte';
  import Connexion from './Connexion.svelte';
  import Inscription from './Inscription.svelte';

  import { route as authRoute, navigate } from './router';
  import { auth, isAuthenticated } from './auth';

  const TITLE_SUFFIX = 'YRR';

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
    // Redirige la racine vers /Bateaux si nécessaire
    if (window.location.pathname === '/' || window.location.pathname === '') {
      // si l'utilisateur est authentifié, on place /Bateaux dans l'historique,
      // sinon on laisse le routeur d'auth s'en charger (connexion)
      if (isAuthenticated(get(auth))) {
        window.history.replaceState({}, '', '/Bateaux');
        route = 'bateaux';
      }
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
    // si on est à la racine, redirige vers connexion ou bateaux selon l'auth
    if (window.location.pathname === '/' || window.location.pathname === '') {
      navigate(isAuthenticated(get(auth)) ? 'bateaux' : 'connexion');
    }

    // initialise la route de l'app (pour la vue principale si authentifié)
    sync();
    window.addEventListener('popstate', sync);
    return () => window.removeEventListener('popstate', sync);
  });

  // titre de la page selon l'état d'auth / route
  function titleForAuth(r: string) {
    if (r === 'bateaux') return `Bateaux | ${TITLE_SUFFIX}`;
    if (r === 'inscription') return `Inscription | ${TITLE_SUFFIX}`;
    return `Connexion | ${TITLE_SUFFIX}`;
  }

  $: if (!isAuthenticated($auth)) {
    // quand on n'est pas authentifié, le titre suit le routeur d'auth
    document.title = titleForAuth($authRoute);
  } else {
    // quand on est authentifié, titre selon la route interne de l'app
    document.title =
      route === 'bateaux' ? `Bateaux | ${TITLE_SUFFIX}` :
      route === 'classes' ? `Classes | ${TITLE_SUFFIX}` :
      route === 'course' ? `Course | ${TITLE_SUFFIX}` :
      route === 'inscriptions' ? `Inscriptions | ${TITLE_SUFFIX}` :
      route === 'series' ? `Series | ${TITLE_SUFFIX}` :
      `Résultats | ${TITLE_SUFFIX}`;
  }

  // garde : si le routeur d'auth essaie d'accéder à 'bateaux' mais qu'on n'est pas authentifié,
  // on renvoie sur connexion
  $: if ($authRoute === 'bateaux' && !isAuthenticated($auth)) {
    navigate('connexion');
  }

  // lorsque l'état d'auth change, on s'assure que le router et la vue principale sont cohérents
  auth.subscribe((s) => {
    if (isAuthenticated(s)) {
      // si on vient de s'authentifier automatiquement (ou restore de session),
      // ne forçons pas la redirection vers /Bateaux si l'utilisateur était sur une autre page;
      // on redirige vers /Bateaux uniquement si on est à la racine ou sur une page d'auth.
      const p = (window.location.pathname || '/').toLowerCase();
      if (p === '/' || p === '' || p.endsWith('/connexion') || p.endsWith('/inscription')) {
        navigate('bateaux');
      } else {
        // conserver l'URL actuelle et synchroniser la vue interne
        sync();
      }
    } else {
      navigate('connexion');
    }
  });
</script>

{#if !isAuthenticated($auth)}
  <div>
    {#if $authRoute === 'connexion'}
      <Connexion />
    {:else if $authRoute === 'inscription'}
      <Inscription onSuccess={() => navigate('bateaux')} />
    {:else}
      <!-- Par défaut, si route inconnue, afficher connexion -->
      <Connexion />
    {/if}
  </div>
{:else}
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
{/if}