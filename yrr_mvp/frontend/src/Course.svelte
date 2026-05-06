<script lang="ts">
  import { onMount, createEventDispatcher } from 'svelte';

  const API_BASE = (import.meta as any).env?.VITE_API_BASE_URL ?? 'http://localhost:8000/api';

  let courses = [];
  let loading = false;
  let formOpen = false;
  let od = '';
  let className = '';
  let date = '';
  let time = '';
  let name = '';
  let course = '';
  let errorMsg = '';

  // Séries
  let series = [];
  let selectedSeriesId = '';

  async function loadSeries() {
    try {
      const res = await fetch(`${API_BASE}/series`);
      if (!res.ok) throw new Error('Erreur chargement séries');
      series = await res.json();
    } catch (e) {
      // fallback ou message d'erreur si besoin
      series = [];
    }
  }

  // Filtrage dynamique
  let filterSeriesId = '';

  $: filteredCourses = filterSeriesId
    ? courses.filter(c => c.series_id === filterSeriesId)
    : courses;

  async function loadCourses() {
    loading = true;
    errorMsg = '';
    try {
      const res = await fetch(`${API_BASE}/courses`);
      if (!res.ok) throw new Error(`GET /courses -> ${res.status}`);
      courses = await res.json();
    } catch (e) {
      errorMsg = e instanceof Error ? e.message : 'Erreur réseau';
    } finally {
      loading = false;
    }
  }

  async function addCourse() {
    errorMsg = '';
    if (!od || !className || !date || !time || !name || !course) {
      errorMsg = 'Tous les champs sont obligatoires';
      return;
    }
    try {
      const res = await fetch(`${API_BASE}/courses`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          od: od.trim(),
          class_name: className.trim(),
          date,
          time,
          name: name.trim(),
          course: course.trim(),
          series_id: selectedSeriesId,
        }),
      });

      if (!res.ok) {
        const data = await res.json().catch(() => null);
        throw new Error(data?.detail ?? `POST /courses -> ${res.status}`);
      }

      od = '';
      className = '';
      date = '';
      time = '';
      name = '';
      course = '';
      selectedSeriesId = '';
      formOpen = false;

      await loadCourses();
    } catch (e) {
      errorMsg = e instanceof Error ? e.message : 'Erreur réseau';
    }
  }

  // --- Navigation SPA harmonisée ---
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

  const dispatch = createEventDispatcher();

  onMount(() => {
    loadCourses();
    loadSeries();
  });
</script>

<header>
  <h2>YRR</h2>
  <div class="header-center">
    <nav class="main-nav-bar">
      <div class="nav-left">
        <a href="/Bateaux" on:click={navigate}>Accueil</a>
        <a href="/Classes" on:click={navigate}>Classes</a>
        <a href="/Bateaux" on:click={navigate}>Bateaux</a>
        <a href="/Series" on:click={navigate}>Séries</a>
        <a href="/Course" class="active" on:click={navigate}>Course</a>
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
    <h2 class="hero-title">Gestion des courses</h2>
    <p class="hero-subtitle">Liste et détails des courses (prototype, données simulées)</p>
    <div class="title-underline"></div>
  </div>

  <section class="panel">
    <div class="row mb-18" style="align-items: center;">
      <h3 style="margin: 0;">Courses</h3>
      <select class="title-select" bind:value={filterSeriesId} style="margin-left: 18px; min-width: 180px;">
        <option value="">Toutes les séries</option>
        {#each series as s}
          <option value={s.id}>{s.name}</option>
        {/each}
      </select>
    </div>

    <div class="add-course-wrap mb-18">
      <details class="add-details" bind:open={formOpen}>
        <summary class="add-summary">+ Ajouter une course</summary>

        {#if errorMsg}
          <div class="error" role="alert">{errorMsg}</div>
        {/if}

        <form class="add-form" on:submit|preventDefault={addCourse}>
          <div class="row">
            <label class="stack" for="od">
              <span>OD/H</span>
              <input id="od" type="text" bind:value={od} />
            </label>

            <label class="stack" for="className">
              <span>Classe de course</span>
              <input id="className" type="text" bind:value={className} />
            </label>
          </div>

          <div class="row mt-8">
            <label class="stack" for="date">
              <span>Date</span>
              <input id="date" type="date" bind:value={date} />
            </label>

            <label class="stack" for="time">
              <span>Heure de départ</span>
              <input id="time" type="time" bind:value={time} />
            </label>
          </div>

          <div class="row mt-8">
            <label class="stack" for="name">
              <span>Nom de la course</span>
              <input id="name" type="text" bind:value={name} />
            </label>

            <label class="stack" for="course">
              <span>Parcours</span>
              <input id="course" type="text" bind:value={course} />
            </label>
          </div>

          <div class="row mt-8">
            <label class="stack" for="series">
              <span>Série associée</span>
              <select id="series" bind:value={selectedSeriesId} required>
                <option value="">Choisir une série</option>
                {#each series as s}
                  <option value={s.id}>{s.name}</option>
                {/each}
              </select>
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
      <table class="table-standard" aria-label="Tableau des courses">
        <thead>
          <tr>
            <th>OD/H</th>
            <th>Classe</th>
            <th>Date</th>
            <th>Heure</th>
            <th>Nom</th>
            <th>Parcours</th>
          </tr>
        </thead>

        <tbody>
          {#each filteredCourses as c}
            <tr>
              <td>{c.od}</td>
              <td>{c.class_name}</td>
              <td>{c.date}</td>
              <td>{c.time}</td>
              <td>{c.name}</td>
              <td>{c.course}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>

    <div class="actions-row mt-2">
      <a class="button-ghost" href="/Bateaux" on:click={navigate}>Retour</a>
    </div>
  </section>
</div>

<footer class="muted mt-18">Prototype non fonctionnel — interface de démonstration.</footer>
