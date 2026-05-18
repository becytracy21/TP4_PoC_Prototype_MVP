<script lang="ts">
  import { createEventDispatcher } from 'svelte';

  export let active: 'bateaux' | 'classes' | 'series' | 'course' | 'inscriptions' | 'resultats-series' = 'bateaux';

  const dispatch = createEventDispatcher<{ navigate: string }>();

  function navigate(e: MouseEvent) {
    e.preventDefault();
    const a = e.currentTarget as HTMLAnchorElement;
    const href = a.getAttribute('href') || '';
    dispatch('navigate', href);
  }
</script>

<header>
  <h2>YRR</h2>
  <div class="header-center" style="display: flex; justify-content: center;">
    <nav class="main-nav-bar">
      <div class="nav-left">
        <a href="/Bateaux" class={active === 'bateaux' ? 'active' : ''} on:click={navigate}>Bateaux</a>
        <a href="/Classes" class={active === 'classes' ? 'active' : ''} on:click={navigate}>Classes</a>
        <a href="/Series" class={active === 'series' ? 'active' : ''} on:click={navigate}>Séries</a>
        <a href="/Course" class={active === 'course' ? 'active' : ''} on:click={navigate}>Course</a>
        <a href="/Inscriptions" class={active === 'inscriptions' ? 'active' : ''} on:click={navigate}>Inscriptions</a>
      </div>
    </nav>
  </div>
  <div class="nav-user">
    <a href="/Profil" class="nav-user-link" on:click={navigate}>
      <div class="avatar" title="Profil">JD</div>
      <div class="username">Jean Dupont</div>
    </a>
  </div>
</header>

<slot />

<footer class="muted mt-18">Prototype non fonctionnel — interface de démonstration.</footer>
