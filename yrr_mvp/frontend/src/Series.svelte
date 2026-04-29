<script>
  import { onMount } from 'svelte';

  // navigation hash: assure que l'app reste dans le SPA
  function go(href) {
    if (!href) return;
    if (href.startsWith('#')) {
      window.location.hash = href;
    } else if (href.startsWith('/')) {
      window.location.hash = '#' + href;
    } else {
      window.location.href = href;
    }
  }

  function navigate(e) {
    e.preventDefault();
    const a = /** @type {HTMLAnchorElement} */ (e.currentTarget);
    const href = a.getAttribute('href') || '';
    go(href);
  }

  // séries gérées via l'API
  let formOpen = false;
  let seriesName = '';
  let seriesRaces = 3;
  let seriesClasse = '';
  let seriesCounted = 3;
  let series = [];
  let errorMessage = '';

  async function loadSeries() {
    errorMessage = '';
    try {
      const res = await fetch('/api/series');
      if (!res.ok) {
        let detail = '';
        try {
          const body = await res.json().catch(() => null);
          if (body) detail = body.detail || JSON.stringify(body);
        } catch (e) {
          detail = '';
        }
        errorMessage = `Erreur serveur ${res.status}: ${detail || res.statusText}`;
         return;
       }
       series = await res.json();
     } catch (e) {
      errorMessage = `Erreur réseau lors du chargement des séries: ${e && e.message ? e.message : e}`;
     }
   }

  onMount(() => {
    loadSeries();
  });

  async function addSeries() {
    const name = (seriesName || '').trim();
    const classe = (seriesClasse || '').trim();
    const races = Math.max(1, Number(seriesRaces) || 1);
    const counted = Math.max(1, Number(seriesCounted) || 1);
    if (!name) {
      errorMessage = 'Veuillez saisir un nom de série.';
      formOpen = true;
      return;
    }
    if (!classe) {
      errorMessage = "Veuillez saisir un nom de classe.";
      formOpen = true;
      return;
    }
    if (counted > races) {
      errorMessage = 'Le nombre de courses à comptabiliser ne peut pas dépasser le nombre total de courses.';
      formOpen = true;
      return;
    }

    try {
      const res = await fetch('/api/series', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, classe, races, counted })
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        errorMessage = data.detail || 'Erreur lors de la création de la série.';
        formOpen = true;
        return;
      }
      // succès : insérer la série retournée par l'API
      series = [data, ...series];
      seriesName = '';
      seriesRaces = 3;
      seriesClasse = '';
      seriesCounted = 3;
      formOpen = false;
      errorMessage = '';
    } catch (e) {
      errorMessage = 'Erreur réseau lors de la création.';
      formOpen = true;
    }
  }

  async function deleteSeries(id) {
    if (!confirm('Supprimer cette série ?')) return;
    try {
      const res = await fetch(`/api/series/${id}`, { method: 'DELETE' });
      if (res.status === 204) {
        series = series.filter(s => s.id !== id);
      } else {
        const data = await res.json().catch(() => ({}));
        errorMessage = data.detail || 'Impossible de supprimer la série.';
      }
    } catch (e) {
      errorMessage = 'Erreur réseau lors de la suppression.';
    }
  }
</script>

<svelte:head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Séries — YRR Prototype</title>
  <link rel="icon" href="/favicon.ico" />
  <link rel="stylesheet" href="/HTML-CSS/css/style.css" />
</svelte:head>

<header>
  <h2>YRR — Prototype</h2>
  <div class="header-center">
    <nav class="main-nav-bar">
      <div class="nav-left">
        <a href="#/bateaux" on:click={navigate}>Accueil</a>
        <a href="#/classes" on:click={navigate}>Classes</a>
        <a href="#/bateaux" on:click={navigate}>Bateaux</a>
        <a href="#/series" class="active" on:click={navigate}>Séries</a>
        <a href="#/course" on:click={navigate}>Course</a>
      </div>
    </nav>
  </div>
  <div class="nav-user">
    <a href="#/profil" class="nav-user-link" on:click={navigate}>
      <div class="avatar" title="Profil">JD</div>
      <div class="username">Jean Dupont</div>
    </a>
  </div>
</header>

<div class="container-main">
  <div class="hero">
    <h2 class="hero-title">Gestion des séries</h2>
    <p class="hero-subtitle">Liste des séries de courses</p>
    <div class="title-underline" aria-hidden="true"></div>
  </div>

  <section class="panel">
    <h3>Liste des séries</h3>
    <div class="table-wrapper">
      <table class="table-standard" aria-label="Liste des séries">
        <thead>
          <tr>
            <th>Nom de la série</th>
            <th>Classe</th>
            <th class="text-center">Nombre de course<br/> à comptabiliser</th>
            <th class="text-center">Nombre de courses</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {#if series.length === 0}
            <tr>
              <td colspan="5" class="muted">Aucune série</td>
            </tr>
          {:else}
            {#each series as s (s.id)}
              <tr>
                <td>{s.name}</td>
                <td>{s.classe}</td>
                <td class="text-center">{s.counted}</td>
                <td class="text-center">{s.races}</td>
                <td>
                  <div class="table-actions">
                    <span class="muted">Utilisée par la page "Course"</span>
                    <a class="btn-small" href="#/resultats-series" on:click={navigate}>Résultats</a>
                    <button class="button-ghost" type="button" on:click={() => deleteSeries(s.id)}>Supprimer</button>
                  </div>
                </td>
              </tr>
            {/each}
          {/if}
        </tbody>
      </table>
    </div>

    <div class="actions-row mt-2">
      <details class="add-details" bind:open={formOpen}>
        <summary class="add-summary">Créer une série</summary>
        <form class="add-form" on:submit|preventDefault={addSeries}>
          <div class="row">
            <label class="stack" for="seriesName">
              <span>Nom de la série</span>
              <input id="seriesName" type="text" bind:value={seriesName} placeholder="Série C" />
            </label>
            {#if errorMessage}
              <div class="error mt-1">{errorMessage}</div>
            {/if}
          </div>

          <div class="row mt-6">
            <label class="stack" for="seriesClasse">
              <span>Classe</span>
              <input id="seriesClasse" type="text" bind:value={seriesClasse} placeholder="Laser" />
            </label>
          </div>

          <div class="row mt-6">
            <label class="stack" for="seriesCounted">
              <span>Nombre de courses à comptabiliser</span>
              <input id="seriesCounted" type="number" min="1" bind:value={seriesCounted} />
            </label>
          </div>

          <div class="row mt-8">
            <label class="stack" for="seriesRaces">
              <span>Nombre de courses</span>
              <input id="seriesRaces" type="number" min="2" bind:value={seriesRaces} />
            </label>
          </div>

          <div class="actions">
            <button class="btn btn-primary" type="submit">Créer</button>
            <button class="btn btn-outline" type="button" on:click={() => (formOpen = false)}>Annuler</button>
          </div>
        </form>
      </details>

      <a class="button-ghost" href="#/bateaux" on:click={navigate}>Retour</a>
    </div>
  </section>
</div>