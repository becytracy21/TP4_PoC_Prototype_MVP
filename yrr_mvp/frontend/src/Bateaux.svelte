<script lang="ts">
  import { onMount, createEventDispatcher } from 'svelte';

  // --- Types et Configuration ---
  type BoatClass = {
    id: string;
    name: string;
  };

  type Boat = {
    id: string;
    name?: string;
    sail_number?: number;
    helmsman?: string;
    class_id?: string | null;
    class_name?: string | null;
  };

  const API_BASE = (import.meta as any).env?.VITE_API_BASE_URL ?? 'http://localhost:8000/api';
  const dispatch = createEventDispatcher();

  // --- État Local ---
  let boats: Boat[] = [];
  let classes: BoatClass[] = [];
  let loading = false;
  let errorMsg = '';
  let formOpen = false;

  // Champs du formulaire (ajout)
  let name = '';
  let sail_number = '';
  let helmsman = '';
  let class_id: string = '';
  let class_name = '';

  // --- Édition inline ---
  let editingId: string | null = null;
  let editName = '';
  let editSailNumber = '';
  let editHelmsman = '';
  let editClassId: string = '';

  // --- Tri ---
  let sortColumn: keyof Pick<Boat, 'name' | 'sail_number' | 'helmsman' | 'class_name'> | null = null;
  let sortDirection: 'asc' | 'desc' = 'asc';

  function applySort() {
    if (!sortColumn) return;
    const col = sortColumn;
    boats = [...boats].sort((a, b) => {
      let av: any = a[col];
      let bv: any = b[col];
      if (typeof av === 'string') av = av.toLowerCase();
      if (typeof bv === 'string') bv = bv.toLowerCase();
      // name peut être undefined
      if (av == null) av = '';
      if (bv == null) bv = '';
      if (av < bv) return sortDirection === 'asc' ? -1 : 1;
      if (av > bv) return sortDirection === 'asc' ? 1 : -1;
      return 0;
    });
  }

  function sortBoats(column: 'name' | 'sail_number' | 'helmsman' | 'class_name') {
    if (sortColumn === column) {
      sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
    } else {
      sortColumn = column;
      sortDirection = 'asc';
    }
    applySort();
  }

  // --- Logique API ---
  async function loadBoats() {
    loading = true;
    errorMsg = '';
    try {
      const res = await fetch(`${API_BASE}/boats`);
      if (!res.ok) throw new Error(`GET /boats -> ${res.status}`);
      boats = (await res.json()) as Boat[];
      applySort();
    } catch (e) {
      errorMsg = e instanceof Error ? e.message : 'Erreur réseau';
    } finally {
      loading = false;
    }
  }

  async function loadClasses() {
    try {
      const res = await fetch(`${API_BASE}/classes`);
      if (!res.ok) throw new Error(`GET /classes -> ${res.status}`);
      const raw = (await res.json()) as any[];
      classes = Array.isArray(raw)
        ? raw
            .map((c) => ({ id: String(c.id ?? c._id), name: String(c.name ?? '') }))
            .filter((c) => c.id && c.name)
        : [];
    } catch {
      classes = [];
    }
  }

  async function addBoat() {
    errorMsg = '';

    const sn = sail_number.trim() === '' ? undefined : Number(sail_number);
    if (sn !== undefined && (Number.isNaN(sn) || !Number.isInteger(sn))) {
      errorMsg = 'Sail number doit être un entier';
      return;
    }

    try {
      const res = await fetch(`${API_BASE}/boats`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: name.trim() === '' ? undefined : name.trim(),
          sail_number: sn,
          helmsman: helmsman.trim() === '' ? undefined : helmsman.trim(),
          class_id: class_id.trim() === '' ? undefined : class_id.trim(),
          class_name: class_name.trim() === '' ? undefined : class_name.trim(),
        }),
      });

      if (!res.ok) {
        const data = await res.json().catch(() => null);
        throw new Error(data?.detail ?? `POST /boats -> ${res.status}`);
      }

      // Reset formulaire
      name = '';
      sail_number = '';
      helmsman = '';
      class_id = '';
      class_name = '';
      formOpen = false;
      await loadClasses();
      await loadBoats();
    } catch (e) {
      errorMsg = e instanceof Error ? e.message : 'Erreur réseau';
    }
  }

  async function deleteBoat(id: string) {
    if (!confirm('Supprimer ce bateau ?')) return;
    errorMsg = '';
    try {
      const res = await fetch(`${API_BASE}/boats/${id}`, { method: 'DELETE' });
      if (!res.ok && res.status !== 204) {
        const data = await res.json().catch(() => null);
        throw new Error(data?.detail ?? `DELETE /boats/${id} -> ${res.status}`);
      }
      if (editingId === id) cancelEdit();
      await loadBoats();
    } catch (e) {
      errorMsg = e instanceof Error ? e.message : 'Erreur réseau';
    }
  }

  function startEdit(b: Boat) {
    editingId = b.id;
    editName = b.name ?? '';
    editSailNumber = b.sail_number == null ? '' : String(b.sail_number);
    editHelmsman = b.helmsman ?? '';
    editClassId = b.class_id ?? '';
  }

  function cancelEdit() {
    editingId = null;
    editName = '';
    editSailNumber = '';
    editHelmsman = '';
    editClassId = '';
  }

  async function saveEdit() {
    if (!editingId) return;
    errorMsg = '';

    const sn = editSailNumber.trim() === '' ? undefined : Number(editSailNumber);
    if (sn !== undefined && (Number.isNaN(sn) || !Number.isInteger(sn))) {
      errorMsg = 'Sail number doit être un entier';
      return;
    }

    try {
      const res = await fetch(`${API_BASE}/boats/${editingId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: editName.trim() === '' ? '' : editName.trim(),
          sail_number: sn ?? '',
          helmsman: editHelmsman.trim() === '' ? '' : editHelmsman.trim(),
          class_id: editClassId.trim() === '' ? '' : editClassId.trim(),
        }),
      });

      if (!res.ok) {
        const data = await res.json().catch(() => null);
        throw new Error(data?.detail ?? `PATCH /boats/${editingId} -> ${res.status}`);
      }

      const updated = (await res.json().catch(() => null)) as Boat | null;
      if (updated) {
        boats = boats.map((b) => (b.id === editingId ? updated : b));
        applySort();
      } else {
        await loadBoats();
      }

      cancelEdit();
    } catch (e) {
      errorMsg = e instanceof Error ? e.message : 'Erreur réseau';
    }
  }

  // --- Navigation SPA ---
  function navigate(e: MouseEvent) {
    e.preventDefault();
    const a = e.currentTarget as HTMLAnchorElement;
    const href = a.getAttribute('href') || '';

    window.history.pushState({}, '', href);
    dispatch('navigate', href);
  }

  onMount(() => {
    loadClasses();
    loadBoats();
  });
</script>

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
            <label class="stack" for="boatSailNumber">
              <span>Sail number</span>
              <input id="boatSailNumber" type="text" inputmode="numeric" bind:value={sail_number} placeholder="e.g. 1234" />
            </label>

            <label class="stack" for="boatHelmsman">
              <span>Helmsman</span>
              <input id="boatHelmsman" type="text" bind:value={helmsman} placeholder="Jean Dupont" />
            </label>
          </div>

          <div class="row mt-8">
            <label class="stack" for="boatClassId">
              <span>Classe</span>
              <select id="boatClassId" bind:value={class_id}>
                <option value="">(Aucune)</option>
                {#each classes as c (c.id)}
                  <option value={c.id}>{c.name}</option>
                {/each}
              </select>
            </label>

            <label class="stack" for="boatClassName">
              <span>Ou créer une classe</span>
              <input id="boatClassName" type="text" bind:value={class_name} placeholder="Nouvelle classe" />
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
      <table class="table-standard" aria-label="Tableau des bateaux">
        <thead>
          <tr>
            <th role="button" on:click={() => sortBoats('name')} style="cursor: pointer;">
              Nom du bateau {sortColumn === 'name' ? (sortDirection === 'asc' ? '▲' : '▼') : ''}
            </th>
            <th role="button" on:click={() => sortBoats('sail_number')} style="cursor: pointer;">
              Sail number {sortColumn === 'sail_number' ? (sortDirection === 'asc' ? '▲' : '▼') : ''}
            </th>
            <th role="button" on:click={() => sortBoats('helmsman')} style="cursor: pointer;">
              Helmsman {sortColumn === 'helmsman' ? (sortDirection === 'asc' ? '▲' : '▼') : ''}
            </th>
            <th role="button" on:click={() => sortBoats('class_name')} style="cursor: pointer;">
              Classe {sortColumn === 'class_name' ? (sortDirection === 'asc' ? '▲' : '▼') : ''}
            </th>
            <th class="action-cell"></th>
          </tr>
        </thead>
        <tbody>
          {#if loading}
            <tr><td colspan="6" class="muted">Chargement…</td></tr>
          {:else if boats.length === 0}
            <tr><td colspan="6" class="muted">Aucun bateau</td></tr>
          {:else}
            {#each boats as b (b.id)}
              <tr>
                <td>
                  {#if editingId === b.id}
                    <input class="cell-input" type="text" bind:value={editName} />
                  {:else}
                    {b.name ?? ''}
                  {/if}
                </td>
                <td>
                  {#if editingId === b.id}
                    <input class="cell-input" type="text" inputmode="numeric" bind:value={editSailNumber} />
                  {:else}
                    {b.sail_number ?? ''}
                  {/if}
                </td>
                <td>
                  {#if editingId === b.id}
                    <input class="cell-input" type="text" bind:value={editHelmsman} />
                  {:else}
                    {b.helmsman ?? ''}
                  {/if}
                </td>
                <td>
                  {#if editingId === b.id}
                    <select class="cell-input" bind:value={editClassId}>
                      <option value="">(Aucune)</option>
                      {#each classes as c (c.id)}
                        <option value={c.id}>{c.name}</option>
                      {/each}
                    </select>
                  {:else}
                    {b.class_name ?? ''}
                  {/if}
                </td>
                <td class="action-cell">
                  {#if editingId === b.id}
                    <button class="btn btn-outline" type="button" on:click={saveEdit}>Enregistrer</button>
                    <button class="btn btn-outline" type="button" on:click={cancelEdit}>Annuler</button>
                  {:else}
                    <button class="btn-edit" type="button" on:click={() => startEdit(b)}>Modifier</button>
                    <button class="btn-delete" type="button" on:click={() => deleteBoat(b.id)}>Supprimer</button>
                  {/if}
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