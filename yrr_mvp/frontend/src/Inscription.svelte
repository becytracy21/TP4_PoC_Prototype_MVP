<script lang="ts">
// Pas de logique spécifique pour cette page statique
import { onMount, createEventDispatcher } from 'svelte';

// Types pour bateau et course
interface Boat {
  id: string;
  name: string;
  class: string;
  numero: string;
  barreur: string;
  handicap_type: 'PY' | 'TMF';
  handicap_value: number;
}
interface Course {
  id: string;
  name: string;
  type: 'monotype' | 'handicap';
}
interface Inscription {
  bateauId: string;
  courseId: string;
  resultat: string;
}

let boats: Boat[] = [];
let courses: Course[] = [];
let inscriptions: Inscription[] = [];

let showForm = false;
let form = {
  bateauId: '',
  courseId: '',
  resultat: ''
};
let selectedCourseId: string = '';
let isSubmitting = false;
let errorMsg = '';

const dispatch = createEventDispatcher();

const API_BASE = (import.meta as any).env?.VITE_API_BASE_URL ?? 'http://localhost:8000/api';

// Simuler chargement des bateaux et courses (remplace par fetch si API)
onMount(async () => {
  // Charger les bateaux depuis l'API
  try {
    const resBoats = await fetch(`${API_BASE}/boats`);
    if (resBoats.ok) {
      const data = await resBoats.json();
      boats = data.map((b: any) => ({
        id: b.id,
        name: b.name,
        class: b.class ?? '',
        numero: b.numero ?? '',
        barreur: b.barreur ?? '',
        handicap_type: b.handicap_type ?? 'PY',
        handicap_value: b.handicap_value ?? 0
      }));
    }
    const resCourses = await fetch(`${API_BASE}/courses`);
    if (resCourses.ok) {
      const data = await resCourses.json();
      courses = data.map((c: any) => ({
        id: c.id,
        name: c.name,
        type: c.type ?? 'monotype'
      }));
    }
  } catch (e) {
    // fallback si erreur
    boats = [
      { id: '1', name: 'Whisky', class: 'Laser', numero: '100231', barreur: 'Fred', handicap_type: 'PY', handicap_value: 1100 },
      { id: '2', name: 'Fuzzy Duck', class: 'Laser', numero: '132248', barreur: 'Graham', handicap_type: 'PY', handicap_value: 1090 }
    ];
    courses = [
      { id: 'A', name: 'Série A', type: 'monotype' },
      { id: 'B', name: 'Série B', type: 'handicap' }
    ];
  }
});

// Charger les inscriptions depuis l'API
async function loadInscriptions() {
  try {
    const res = await fetch(`${API_BASE}/inscriptions`);
    if (res.ok) {
      const data = await res.json();
      inscriptions = data.map((i: any) => ({
        bateauId: i.bateauId,
        courseId: i.courseId,
        resultat: i.resultat
      }));
    }
  } catch (e) {
    // fallback : rien
  }
}

// Charger les inscriptions au montage
onMount(async () => {
  // Charger les bateaux depuis l'API
  try {
    const resBoats = await fetch(`${API_BASE}/boats`);
    if (resBoats.ok) {
      const data = await resBoats.json();
      boats = data.map((b: any) => ({
        id: b.id,
        name: b.name,
        class: b.class ?? '',
        numero: b.numero ?? '',
        barreur: b.barreur ?? '',
        handicap_type: b.handicap_type ?? 'PY',
        handicap_value: b.handicap_value ?? 0
      }));
    }
    const resCourses = await fetch(`${API_BASE}/courses`);
    if (resCourses.ok) {
      const data = await resCourses.json();
      courses = data.map((c: any) => ({
        id: c.id,
        name: c.name,
        type: c.type ?? 'monotype'
      }));
    }
    await loadInscriptions();
  } catch (e) {
    // fallback si erreur
    boats = [
      { id: '1', name: 'Whisky', class: 'Laser', numero: '100231', barreur: 'Fred', handicap_type: 'PY', handicap_value: 1100 },
      { id: '2', name: 'Fuzzy Duck', class: 'Laser', numero: '132248', barreur: 'Graham', handicap_type: 'PY', handicap_value: 1090 }
    ];
    courses = [
      { id: 'A', name: 'Série A', type: 'monotype' },
      { id: 'B', name: 'Série B', type: 'handicap' }
    ];
  }
});

function openForm() {
  showForm = true;
}
function closeForm() {
  showForm = false;
  form = { bateauId: '', courseId: '', resultat: '' };
}

// Ajout d'une inscription persistante côté API
async function addInscription() {
  if (!form.bateauId || !form.courseId || !form.resultat) return;
  isSubmitting = true;
  errorMsg = '';
  try {
    const body = JSON.stringify({
      bateauId: form.bateauId,
      courseId: form.courseId,
      resultat: form.resultat,
      // variantes pour compatibilité API
      boat: form.bateauId,
      boat_id: form.bateauId,
      course: form.courseId,
      course_id: form.courseId
    });
    const res = await fetch(`${API_BASE}/inscriptions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body
    });
    if (res.ok) {
      await loadInscriptions();
      closeForm();
    } else {
      const data = await res.json().catch(() => null);
      errorMsg = (data?.detail || JSON.stringify(data) || 'Erreur lors de l\'inscription.') + ` (code ${res.status})`;
    }
  } catch (e) {
    errorMsg = 'Erreur réseau ou serveur.';
  } finally {
    isSubmitting = false;
  }
}

// Mettre à jour form.courseId automatiquement
$: if (showForm && selectedCourseId) {
  form.courseId = selectedCourseId;
}

// Calcul position et points automatiquement
function getSortedInscriptions(courseId: string) {
  // Filtrer les inscriptions pour la course
  const insc = inscriptions.filter(i => i.courseId === courseId);
  // Trier selon le résultat (simplifié, à adapter selon règles)
  const valid = insc.filter(i => !isNaN(Number(i.resultat)));
  valid.sort((a, b) => Number(a.resultat) - Number(b.resultat));
  const invalid = insc.filter(i => isNaN(Number(i.resultat)));
  return [...valid, ...invalid];
}
function getPosition(inscription: Inscription, courseId: string) {
  const sorted = getSortedInscriptions(courseId);
  const idx = sorted.findIndex(i => i === inscription);
  return idx >= 0 ? (idx + 1).toString() : '';
}
function getPoints(inscription: Inscription, courseId: string) {
  // 1 point pour la 1ère place, 2 pour la 2e, etc.
  const pos = getPosition(inscription, courseId);
  return pos ? pos : '';
}

function onHeaderLinkClick(e: MouseEvent, page: string = '') {
  e.preventDefault();
  if (page === 'inscription') {
    dispatch('navigate', 'inscription');
  } else if (page === 'course') {
    dispatch('navigate', 'course');
  } else if (page === 'bateaux') {
    dispatch('navigate', 'bateaux');
  } else {
    // Ajoute d'autres pages si besoin
    dispatch('navigate', page);
  }
}
</script>

<header>
  <h2>YRR — Prototype</h2>
  <div class="header-center">
    <nav class="main-nav-bar">
      <div class="nav-left">
        <a href="#" on:click={(e) => onHeaderLinkClick(e, 'accueil')}>Accueil</a>
        <a href="#" on:click={(e) => onHeaderLinkClick(e, 'classes')}>Classes</a>
        <a href="#" on:click={(e) => onHeaderLinkClick(e, 'bateaux')}>Bateaux</a>
        <a href="#" on:click={(e) => onHeaderLinkClick(e, 'series')}>Séries</a>
        <a href="#" on:click={(e) => onHeaderLinkClick(e, 'course')}>Course</a>
        <a href="#" class="active" on:click={(e) => onHeaderLinkClick(e, 'inscription')}>Inscription</a>
      </div>
    </nav>
  </div>
  <div class="nav-user">
    <a href="/Profil" class="nav-user-link">
      <div class="avatar" title="Profil">JD</div>
      <div class="username">Jean Dupont</div>
    </a>
  </div>
</header>

<div class="container-main">
  <div class="hero">
    <h2 class="hero-title">Inscriptions à une course</h2>
    <p class="hero-subtitle">Liste des bateaux inscrits à la prochaine course (prototype, données simulées)</p>
    <div class="title-underline" aria-hidden="true"></div>
  </div>

  <section class="panel">
    <h3>Inscriptions à la course
      <select bind:value={selectedCourseId} style="margin-left:1rem;">
        <option value="" disabled selected>Choisir une course</option>
        {#each courses as c}
          <option value={c.id}>{c.name}</option>
        {/each}
      </select>
    </h3>
    <div class="table-wrapper">
      <table class="table-standard" aria-label="Inscriptions à la course">
        <thead>
          <tr>
            <th>Nom du bateau</th>
            <th>Résultat</th>
            <th class="text-center">Position</th>
            <th class="text-center">Points</th>
          </tr>
        </thead>
        <tbody>
          {#each inscriptions.filter(i => i.courseId === selectedCourseId) as insc}
            <tr>
              <td>{boats.find(b => b.id === insc.bateauId)?.name}</td>
              <td>{insc.resultat}</td>
              <td class="text-center">{getPosition(insc, insc.courseId)}</td>
              <td class="text-center">{getPoints(insc, insc.courseId)}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
    <div class="actions-row mt-2">
      <button class="btn" on:click={openForm} disabled={!selectedCourseId}>Ajouter</button>
    </div>
    {#if showForm}
      <div class="modal-backdrop">
        <div class="modal-form">
          <h4>Ajouter une inscription</h4>
          {#if errorMsg}
            <div class="error" style="color:red; margin-bottom:1rem;">{errorMsg}</div>
          {/if}
          <form on:submit|preventDefault={addInscription}>
            <label>Bateau
              <select bind:value={form.bateauId} required>
                <option value="" disabled selected>Choisir un bateau</option>
                {#each boats as b}
                  <option value={b.id}>{b.name} ({b.numero})</option>
                {/each}
              </select>
            </label>
            <label>Résultat <input bind:value={form.resultat} required placeholder="ex: 1 ou 14:10:22 ou DNS" /></label>
            <div class="actions">
              <button class="btn btn-primary" type="submit" disabled={isSubmitting}>Valider</button>
              <button class="btn btn-outline" type="button" on:click={closeForm} disabled={isSubmitting}>Annuler</button>
            </div>
          </form>
        </div>
      </div>
    {/if}
  </section>
</div>

<footer class="muted mt-18">Prototype non fonctionnel — interface de démonstration.</footer>

<style>
.modal-backdrop {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal-form {
  background: #fff;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.15);
  min-width: 320px;
}
.modal-form label {
  display: block;
  margin-bottom: 0.5rem;
}
.modal-form input, .modal-form select {
  width: 100%;
  padding: 0.3rem;
  margin-top: 0.2rem;
  margin-bottom: 0.7rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}
.actions-row .btn {
  min-width: 120px;
  text-align: center;
  font-weight: bold;
}
</style>
