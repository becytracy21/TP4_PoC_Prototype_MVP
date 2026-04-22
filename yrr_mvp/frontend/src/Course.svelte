<script lang="ts">
  // Pas de logique métier, données simulées
  import { onMount } from 'svelte';
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

  // Ajout du filtre séries
  let seriesFilter = 'none';
  let seriesOptions = [
    { value: 'none', label: 'Courses hors série' },
    { value: 'seriesA', label: 'Série A' },
    { value: 'seriesB', label: 'Série B' }
  ];
  // Filtrage dynamique
  $: filteredCourses = seriesFilter === 'none'
    ? courses.filter(c => !c.series)
    : courses.filter(c => c.series === seriesFilter);

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
      formOpen = false;
      await loadCourses();
    } catch (e) {
      errorMsg = e instanceof Error ? e.message : 'Erreur réseau';
    }
  }

  onMount(loadCourses);
</script>

<header>
  <h2>YRR — Prototype</h2>
  <div class="header-center">
    <nav class="main-nav-bar">
      <div class="nav-left">
        <a href="Accueil.html">Accueil</a>
        <a href="Classes.html">Classes</a>
        <a href="Bateaux.html">Bateaux</a>
        <a href="Series.html">Séries</a>
        <a href="Course.html" class="active">Course</a>
      </div>
    </nav>
  </div>
  <div class="nav-user">
    <a href="Profil.html" class="nav-user-link">
      <div class="avatar" title="Profil">JD</div>
      <div class="username">Jean Dupont</div>
    </a>
  </div>
</header>

<div class="container-main">
  <div class="hero">
    <h2 class="hero-title">Gestion des courses</h2>
    <p class="hero-subtitle">Liste et détails des courses (prototype, données simulées)</p>
    <div class="title-underline" aria-hidden="true"></div>
  </div>

  <section class="panel">
    <div class="row mb-18" style="align-items: center;">
      <h3 style="margin: 0;">Courses</h3>
      <select id="seriesSelector" class="title-select" bind:value={seriesFilter} style="margin-left: 18px;">
        {#each seriesOptions as opt}
          <option value={opt.value}>{opt.label}</option>
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
              <input id="od" type="text" bind:value={od} placeholder="Monotype ou Handicap" />
            </label>
            <label class="stack" for="className">
              <span>Classe de course</span>
              <input id="className" type="text" bind:value={className} placeholder="FM, Open..." />
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
              <input id="name" type="text" bind:value={name} placeholder="Nom de la course" />
            </label>
            <label class="stack" for="course">
              <span>Parcours</span>
              <input id="course" type="text" bind:value={course} placeholder="Parcours A, B..." />
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
      <table class="table-standard" id="raceTable" aria-label="Tableau des courses">
        <thead>
          <tr>
            <th>OD/H</th>
            <th>Classe de course</th>
            <th>Date</th>
            <th>Heure de départ</th>
            <th>Nom de la course</th>
            <th>Parcours</th>
          </tr>
        </thead>
        <tbody>
          {#each filteredCourses as c}
            <tr data-series={c.series ?? 'none'}>
              <td><input class="cell-input small" data-field="od" value={c.od} readonly></td>
              <td><input class="cell-input small" data-field="class" value={c.class_name ?? c.class} readonly></td>
              <td><input class="cell-input" data-field="date" type="date" value={c.date} readonly></td>
              <td><input class="cell-input small" data-field="time" type="time" value={c.time} readonly></td>
              <td><input class="cell-input" data-field="name" value={c.name} readonly></td>
              <td><input class="cell-input small" data-field="course" value={c.course} readonly></td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>

    <div class="actions-row mt-2">
      <a class="btn" href="Inscriptions.html">Gérer les inscriptions de la course (simulé)</a>
      <a class="button-ghost" href="Accueil.html">Retour</a>
    </div>
  </section>
</div>

<footer class="muted mt-18">Prototype non fonctionnel — interface de démonstration.</footer>

<style>
  :root {
  --accent: linear-gradient(90deg, var(--accent-1), var(--accent-2));
  --badge-py-bg: rgba(124, 58, 237, 0.16);
  --badge-py-border: rgba(124, 58, 237, 0.28);
  --badge-tmf-bg: rgba(52, 211, 153, 0.16);
  --badge-tmf-border: rgba(52, 211, 153, 0.28);
  --bg: linear-gradient(135deg, #f8f4ff 0%, #e9e0ff 40%, #f3eaff 100%);
  --card: #fff8fe;
  --danger: #dc2626;
  --danger-2: #b91c1c;
  --danger-shadow: 0 12px 36px rgba(220, 38, 38, 0.18);
  --green: #34d399;
  --green-2: #059669;
  --green-gradient: linear-gradient(90deg, var(--green), var(--green-2));
  --input-bg: #fbfdff;
  --input-border: #e6eef8;
  --muted: #5b4b6b;
  --radius: 12px;
  --shadow: 0 12px 36px rgba(44, 18, 80, 0.07);
  --table-border: #e1e4ea;
  --table-head-bg: rgba(162, 89, 230, 0.14);
  --table-hover: rgba(52, 211, 153, 0.10);
  --table-zebra: rgba(124, 58, 237, 0.04);
  --text: #2d1a3a;
  --accent-1: #a259e6;
  --accent-2: #7c3aed;
}

/* ...copie le CSS fourni dans la demande précédente ici... */
</style>
