<script>
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

  // séries localement gérées (simulation)
  let formOpen = false;
  let seriesName = '';
  let seriesRaces = 3;
  let series = [
    { id: 1, name: 'Série A', races: 3 },
    { id: 2, name: 'Série B', races: 2 }
  ];

  function addSeries() {
    const name = (seriesName || '').trim();
    const races = Math.max(1, Number(seriesRaces) || 1);
    if (!name) return;
    const id = Date.now();
    series = [{ id, name, races }, ...series];
    seriesName = '';
    seriesRaces = 3;
    formOpen = false;
  }

  function deleteSeries(id) {
    if (!confirm('Supprimer cette série ?')) return;
    series = series.filter(s => s.id !== id);
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
    <p class="hero-subtitle">Liste des séries de courses (prototype, données simulées)</p>
    <div class="title-underline" aria-hidden="true"></div>
  </div>

  <section class="panel">
    <h3>Liste des séries</h3>
    <div class="table-wrapper">
      <table class="table-standard" aria-label="Liste des séries">
        <thead>
          <tr>
            <th>Nom de la série</th>
            <th class="text-center">Nombre de courses</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {#if series.length === 0}
            <tr>
              <td colspan="3" class="muted">Aucune série</td>
            </tr>
          {:else}
            {#each series as s (s.id)}
              <tr>
                <td>{s.name}</td>
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
      <button class="btn" type="button" on:click={() => (formOpen = true)}>Ajouter une série</button>

      <details class="add-details" bind:open={formOpen}>
        <summary class="add-summary">Créer une série</summary>
        <form class="add-form" on:submit|preventDefault={addSeries}>
          <div class="row">
            <label class="stack" for="seriesName">
              <span>Nom de la série</span>
              <input id="seriesName" type="text" bind:value={seriesName} placeholder="Série C" />
            </label>
          </div>

          <div class="row mt-8">
            <label class="stack" for="seriesRaces">
              <span>Nombre de courses</span>
              <input id="seriesRaces" type="number" min="1" bind:value={seriesRaces} />
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

<footer class="muted mt-18">Prototype non fonctionnel — interface de démonstration.</footer>