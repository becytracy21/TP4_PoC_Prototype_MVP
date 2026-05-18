<script lang="ts">
  import { onMount, createEventDispatcher } from 'svelte';

  type Boat = {
    id: string;
    name?: string;
    class_name?: string | null;
    sail_number?: number | null;
    helmsman?: string | null;
  };

  type Course = {
    id: string;
    name: string;
    type?: 'monotype' | 'handicap';
  };

  type Inscription = {
    bateauId: string;
    courseId: string;
    resultat: string;
  };

  let boats: Boat[] = [];
  let courses: Course[] = [];
  let inscriptions: Inscription[] = [];

  let showForm = false;
  let form: Inscription = { bateauId: '', courseId: '', resultat: '' };
  let selectedCourseId = '';
  let isSubmitting = false;
  let errorMsg = '';

  const dispatch = createEventDispatcher<{ navigate: string }>();
  const API_BASE = (import.meta as any).env?.VITE_API_BASE_URL ?? 'http://localhost:8000/api';

  function navigate(e: MouseEvent) {
    e.preventDefault();
    const a = e.currentTarget as HTMLAnchorElement;
    const href = a.getAttribute('href') || '';
    window.history.pushState({}, '', href);
    dispatch('navigate', href);
  }

  async function loadBoatsAndCourses() {
    try {
      const [resBoats, resCourses] = await Promise.all([fetch(`${API_BASE}/boats`), fetch(`${API_BASE}/courses`)]);

      if (resBoats.ok) {
        const data = await resBoats.json();
        boats = Array.isArray(data)
          ? data.map((b: any) => ({
              id: String(b.id),
              name: b.name ?? '',
              class_name: b.class_name ?? null,
              sail_number: b.sail_number ?? null,
              helmsman: b.helmsman ?? null,
            }))
          : [];
      }

      if (resCourses.ok) {
        const data = await resCourses.json();
        courses = Array.isArray(data)
          ? data.map((c: any) => ({ id: String(c.id), name: String(c.name ?? ''), type: c.type ?? 'monotype' }))
          : [];
      }
    } catch {
      boats = [];
      courses = [];
    }
  }

  async function loadInscriptions() {
    try {
      const res = await fetch(`${API_BASE}/inscriptions`);
      if (res.ok) {
        const data = await res.json();
        inscriptions = Array.isArray(data)
          ? data.map((i: any) => ({
              bateauId: String(i.bateauId ?? i.boat_id ?? i.boat ?? ''),
              courseId: String(i.courseId ?? i.course_id ?? i.course ?? ''),
              resultat: String(i.resultat ?? ''),
            }))
          : [];
      }
    } catch {
      inscriptions = [];
    }
  }

  onMount(async () => {
    await loadBoatsAndCourses();
    await loadInscriptions();
  });

  function openForm() {
    showForm = true;
  }

  function closeForm() {
    showForm = false;
    form = { bateauId: '', courseId: '', resultat: '' };
    errorMsg = '';
  }

  async function addInscription() {
    if (!form.bateauId || !form.courseId || !form.resultat) return;
    isSubmitting = true;
    errorMsg = '';

    try {
      const body = JSON.stringify({
        bateauId: form.bateauId,
        courseId: form.courseId,
        resultat: form.resultat,
        boat: form.bateauId,
        boat_id: form.bateauId,
        course: form.courseId,
        course_id: form.courseId,
      });

      const res = await fetch(`${API_BASE}/inscriptions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body,
      });

      if (res.ok) {
        await loadInscriptions();
        closeForm();
      } else {
        const data = await res.json().catch(() => null);
        errorMsg = (data?.detail || JSON.stringify(data) || "Erreur lors de l'inscription.") + ` (code ${res.status})`;
      }
    } catch {
      errorMsg = 'Erreur réseau ou serveur.';
    } finally {
      isSubmitting = false;
    }
  }

  $: if (showForm && selectedCourseId) {
    form = { ...form, courseId: selectedCourseId };
  }
</script>

<div class="container-main">
  <div class="hero">
    <h2 class="hero-title">Inscriptions à une course</h2>
    <p class="hero-subtitle">Liste des bateaux inscrits à la prochaine course</p>
    <div class="title-underline" aria-hidden="true"></div>
  </div>

  <section class="panel">
    <div class="row" style="align-items: center;">
      <h3 style="margin: 0;">Inscriptions à la course</h3>
      <select class="title-select" bind:value={selectedCourseId} style="margin-left: 12px; min-width: 220px;">
        <option value="" disabled>Choisir une course</option>
        {#each courses as c (c.id)}
          <option value={c.id}>{c.name}</option>
        {/each}
      </select>
    </div>

    <div class="table-wrapper mt-8">
      <table class="table-standard" aria-label="Inscriptions à la course">
        <thead>
          <tr>
            <th>Nom du bateau</th>
            <th>Classe</th>
            <th>Résultat</th>
          </tr>
        </thead>
        <tbody>
          {#each inscriptions.filter((i) => i.courseId === selectedCourseId) as insc (insc.bateauId + insc.courseId)}
            <tr>
              <td>{boats.find((b) => b.id === insc.bateauId)?.name ?? ''}</td>
              <td>{boats.find((b) => b.id === insc.bateauId)?.class_name ?? ''}</td>
              <td>{insc.resultat}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>

    <div class="actions-row mt-2">
      <button class="btn" type="button" on:click={openForm} disabled={!selectedCourseId}>Ajouter</button>
      <a class="button-ghost" href="/Bateaux" on:click={navigate}>Retour</a>
    </div>

    <div class="modal-backdrop {showForm ? 'active' : ''}" on:click={(e) => e.target === e.currentTarget && closeForm()}>
      <div class="modal">
        <div class="modal-header">
          <h2>Ajouter une inscription</h2>
          <button class="modal-close" type="button" on:click={closeForm}>&times;</button>
        </div>

        <form class="modal-body" on:submit|preventDefault={addInscription}>
          {#if errorMsg}
            <div class="error" role="alert">{errorMsg}</div>
          {/if}

          <div class="row">
            <label class="stack" for="inscBoat">
              <span>Bateau</span>
              <select id="inscBoat" bind:value={form.bateauId} required>
                <option value="" disabled>Choisir un bateau</option>
                {#each boats as b (b.id)}
                  <option value={b.id}>{b.name} ({b.sail_number ?? ''})</option>
                {/each}
              </select>
            </label>
          </div>

          <div class="row mt-8">
            <label class="stack" for="inscResult">
              <span>Résultat</span>
              <input id="inscResult" type="text" bind:value={form.resultat} required placeholder="ex: 1 ou 14:10:22 ou DNS" />
            </label>
          </div>

          <div class="modal-footer">
            <button class="btn btn-outline" type="button" on:click={closeForm} disabled={isSubmitting}>Annuler</button>
            <button class="btn btn-primary" type="submit" disabled={isSubmitting}>Valider</button>
          </div>
        </form>
      </div>
    </div>
  </section>
</div>
