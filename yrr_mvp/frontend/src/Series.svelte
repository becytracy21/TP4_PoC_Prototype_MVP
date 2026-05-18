<script lang="ts">
  import { onMount, createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher<{ navigate: string }>();

  const API_BASE = (import.meta as any).env?.VITE_API_BASE_URL ?? 'http://localhost:8000/api';

  let formOpen = false;
  let seriesName = '';
  let seriesRaces = 3;
  let seriesClasse = '';
  let seriesCounted = 3;
  let series: any[] = [];
  let errorMessage = '';
  let courses: any[] = [];
  let coursesCountBySeries: Record<string, number> = {};
  let loading = false;

  function navigate(e: MouseEvent) {
    e.preventDefault();
    const a = e.currentTarget as HTMLAnchorElement;
    const href = a.getAttribute('href') || '';
    window.history.pushState({}, '', href);
    dispatch('navigate', href);
  }

  async function loadSeries() {
    errorMessage = '';
    try {
      const res = await fetch(`${API_BASE}/series`);
      if (!res.ok) {
        const body = await res.json().catch(() => null);
        const detail = body?.detail ? String(body.detail) : body ? JSON.stringify(body) : '';
        errorMessage = `Erreur serveur ${res.status}: ${detail || res.statusText}`;
        return;
      }
      series = await res.json();
    } catch (e: any) {
      errorMessage = `Erreur réseau lors du chargement des séries: ${e?.message ?? String(e)}`;
    }
  }

  async function loadCourses() {
    loading = true;
    errorMessage = '';
    try {
      const res = await fetch(`${API_BASE}/courses`);
      if (!res.ok) throw new Error(`GET /courses -> ${res.status}`);
      courses = await res.json();

      coursesCountBySeries = {};
      if (Array.isArray(courses)) {
        for (const c of courses) {
          if (c.series_id) {
            const key = String(c.series_id);
            coursesCountBySeries[key] = (coursesCountBySeries[key] || 0) + 1;
          }
        }
      }
    } catch {
      courses = [];
      coursesCountBySeries = {};
    } finally {
      loading = false;
    }
  }

  onMount(() => {
    loadSeries();
    loadCourses();
  });

  async function addSeries() {
    const name = (seriesName || '').trim();
    const classe = (seriesClasse || '').trim();
    const counted = Math.max(1, Number(seriesCounted) || 1);

    if (!name) {
      errorMessage = 'Veuillez saisir un nom de série.';
      formOpen = true;
      return;
    }
    if (!classe) {
      errorMessage = 'Veuillez saisir un nom de classe.';
      formOpen = true;
      return;
    }

    try {
      const res = await fetch(`${API_BASE}/series`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, classe, counted }),
      });

      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        errorMessage = data.detail || 'Erreur lors de la création de la série.';
        formOpen = true;
        return;
      }

      series = [data, ...series];
      seriesName = '';
      seriesClasse = '';
      seriesCounted = 1;
      formOpen = false;
      errorMessage = '';
      loadCourses();
    } catch {
      errorMessage = 'Erreur réseau lors de la création.';
      formOpen = true;
    }
  }

  async function deleteSeries(id: string) {
    if (!confirm('Supprimer cette série ?')) return;
    try {
      const res = await fetch(`${API_BASE}/series/${id}`, { method: 'DELETE' });
      if (res.status === 204) {
        series = series.filter((s) => s.id !== id);
      } else {
        const data = await res.json().catch(() => ({}));
        errorMessage = data.detail || 'Impossible de supprimer la série.';
      }
    } catch {
      errorMessage = 'Erreur réseau lors de la suppression.';
    }
  }
</script>

<svelte:head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Séries — YRR</title>
  <link rel="icon" href="/favicon.ico" />
</svelte:head>

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
            <th class="text-center">Nombre de course<br />à comptabiliser</th>
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
                <td class="text-center">{coursesCountBySeries[s.id] || 0}</td>
                <td>
                  <div class="table-actions">
                    <span class="muted">Utilisée par la page "Course"</span>
                    <a class="btn-small" href="/ResultatsSeries" on:click={navigate}>Résultats</a>
                    <button class="btn-delete" type="button" on:click={() => deleteSeries(String(s.id))}>Supprimer</button>
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

          <div class="actions">
            <button class="btn btn-primary" type="submit" disabled={loading}>Créer</button>
            <button class="btn btn-outline" type="button" on:click={() => (formOpen = false)} disabled={loading}>Annuler</button>
          </div>
        </form>
      </details>

      <a class="button-ghost" href="/Bateaux" on:click={navigate}>Retour</a>
    </div>
  </section>
</div>