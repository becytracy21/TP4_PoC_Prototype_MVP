<script lang="ts">
  import { onMount } from 'svelte';
  import { createEventDispatcher } from 'svelte';

  type Boat = {
    id: string;
    name?: string;
    handicap_type: 'PY' | 'TMF';
    handicap_value: number;
  };

  const API_BASE = (import.meta as any).env?.VITE_API_BASE_URL ?? 'http://localhost:8000/api';

  let boats: Boat[] = [];
  let loading = false;
  let errorMsg = '';

  let formOpen = false;

  let name = '';
  let handicap_type: 'PY' | 'TMF' = 'PY';
  let handicap_value = '';

  const dispatch = createEventDispatcher();

  async function loadBoats() {
    loading = true;
    errorMsg = '';
    try {
      const res = await fetch(`${API_BASE}/boats`);
      if (!res.ok) throw new Error(`GET /boats -> ${res.status}`);
      boats = (await res.json()) as Boat[];
    } catch (e) {
      errorMsg = e instanceof Error ? e.message : 'Erreur réseau';
    } finally {
      loading = false;
    }
  }

  async function addBoat() {
    errorMsg = '';
    const hv = Number(handicap_value);
    if (Number.isNaN(hv)) {
      errorMsg = 'H/cap value doit être un nombre';
      return;
    }

    try {
      const res = await fetch(`${API_BASE}/boats`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: name.trim() === '' ? undefined : name.trim(),
          handicap_type,
          handicap_value: hv,
        }),
      });

      if (!res.ok) {
        const data = await res.json().catch(() => null);
        throw new Error(data?.detail ?? `POST /boats -> ${res.status}`);
      }

      name = '';
      handicap_type = 'PY';
      handicap_value = '';
      formOpen = false;
      await loadBoats();
    } catch (e) {
      errorMsg = e instanceof Error ? e.message : 'Erreur réseau';
    }
  }

  async function deleteBoat(id: string) {
    errorMsg = '';
    if (!confirm('Supprimer ce bateau?')) return;

    try {
      const res = await fetch(`${API_BASE}/boats/${id}`, { method: 'DELETE' });
      if (!res.ok && res.status !== 204) {
        const data = await res.json().catch(() => null);
        throw new Error(data?.detail ?? `DELETE /boats/${id} -> ${res.status}`);
      }
      await loadBoats();
    } catch (e) {
      errorMsg = e instanceof Error ? e.message : 'Erreur réseau';
    }
  }

  // --- Logique de navigation SPA harmonisée ---
  function go(href: string) {
    if (!href) return;
    if (href.startsWith('/')) {
      window.history.pushState({}, '', href);
      dispatch('navigate', href);
    } else {
      window.location.href = href;
    }
  }

  function navigate(e: MouseEvent) {
    e.preventDefault();
    const a = e.currentTarget as HTMLAnchorElement;
    go(a.getAttribute('href') || '');
  }

  function onHeaderLinkClick(e: MouseEvent, page: string = '') {
    e.preventDefault();
    if (page === 'course') {
      dispatch('navigate', '/Course');
      window.history.pushState({}, '', '/Course');
    } else if (page === 'inscription') {
      dispatch('navigate', '/Inscription');
      window.history.pushState({}, '', '/Inscription');
    } else if (page === 'bateaux') {
      dispatch('navigate', '/Bateaux');
      window.history.pushState({}, '', '/Bateaux');
    } else if (page === 'series') {
      dispatch('navigate', '/Series');
      window.history.pushState({}, '', '/Series');
    } else if (page === 'classes') {
      dispatch('navigate', '/Classes');
      window.history.pushState({}, '', '/Classes');
    } else {
      // fallback
      dispatch('navigate', '/Bateaux');
      window.history.pushState({}, '', '/Bateaux');
    }
  }

  onMount(loadBoats);
</script>

<header>
  <h2>YRR</h2>
  <div class="header-center" style="display: flex; justify-content: center;">
    <nav class="main-nav-bar">
      <div class="nav-left">
        <a href="/Bateaux" on:click={navigate}>Accueil</a>
        <a href="/Classes" on:click={navigate}>Classes</a>
        <a href="/Bateaux" on:click={navigate}>Bateaux</a>
        <a href="/Series" on:click={navigate}>Séries</a>
        <a href="/Course" on:click={navigate}>Course</a>
        <a href="/Inscription" on:click={navigate}>Inscription</a>
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

<div class="container-main">
  <div class="hero">
    <h2 class="hero-title">Gestion des bateaux</h2>
    <p class="hero-subtitle">Liste des bateaux inscrits (MVP, données MongoDB)</p>
    <div class="title-underline" aria-hidden="true"></div>
  </div>

  <section class="panel">
    <h3>Liste des bateaux</h3>

    {#if errorMsg}
      <div class="error" role="alert">{errorMsg}</div>
    {/if}

    <div class="add-boat-wrap mb-18">
      <details class="add-details" bind:open={formOpen}>
        <summary class="add-summary">+ Ajouter un bateau</summary>
        <form class="add-form" on:submit|preventDefault={addBoat}>
          <div class="row">
            <label class="stack" for="boatName">
              <span>Nom du bateau</span>
              <input id="boatName" type="text" bind:value={name} placeholder="Sea Breeze" />
            </label>
          </div>

          <div class="row mt-8">
            <label class="stack" for="boatType">
              <span>H/cap type</span>
              <select id="boatType" bind:value={handicap_type}>
                <option value="PY">PY</option>
                <option value="TMF">TMF</option>
              </select>
            </label>

            <label class="stack" for="boatValue">
              <span>H/cap value</span>
              <input
                id="boatValue"
                type="text"
                inputmode="decimal"
                bind:value={handicap_value}
                placeholder="e.g. 1.234"
              />
            </label>
          </div>

          <div class="actions">
            <button class="btn btn-primary" type="submit">Ajouter</button>
            <button class="btn btn-outline" type="button" on:click={() => (formOpen = false)}>Annuler</button>
          </div>
        </form>
      </details>
    </div>

    <div class="table-wrapper">
      <table class="table-standard" aria-label="Tableau des bateaux" id="boatTable">
        <thead>
          <tr>
            <th>Nom du bateau</th>
            <th>H/cap type</th>
            <th>H/cap value</th>
            <th class="action-cell"></th>
          </tr>
        </thead>
        <tbody>
          {#if loading}
            <tr>
              <td colspan="4" class="muted">Chargement…</td>
            </tr>
          {:else if boats.length === 0}
            <tr>
              <td colspan="4" class="muted">Aucun bateau</td>
            </tr>
          {:else}
            {#each boats as b (b.id)}
              <tr>
                <td>{b.name ?? ''}</td>
                <td>
                  <span class={"badge " + (b.handicap_type === 'PY' ? 'badge--py' : 'badge--tmf')}>
                    {b.handicap_type}
                  </span>
                </td>
                <td>{b.handicap_value}</td>
                <td class="action-cell">
                  <button class="btn-delete" type="button" on:click={() => deleteBoat(b.id)}>Supprimer</button>
                </td>
              </tr>
            {/each}
          {/if}
        </tbody>
      </table>
    </div>

    <div class="actions-row mt-2">
      <a class="button-ghost" href="/Bateaux" on:click={navigate}>Retour</a>
    </div>
  </section>
</div>

<footer class="muted mt-18">MVP fonctionnel — interface connectée à MongoDB.</footer>