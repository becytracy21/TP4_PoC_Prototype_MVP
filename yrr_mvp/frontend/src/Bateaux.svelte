<script lang="ts">
  import { onMount } from 'svelte';

  type Boat = {
    id: string;
    name?: string;
    classe?: 'Albacore' | 'Comet' | 'Fireball' | 'Laser' | 'Mirror';
    sail_number?: number;
    helmsman?: string;
  };

  const API_BASE = (import.meta as any).env?.VITE_API_BASE_URL ?? 'http://localhost:8000/api';

  let boats: Boat[] = [];
  let loading = false;
  let errorMsg = '';

  let formOpen = false;

  let name = '';
  let classe: 'Albacore' | 'Comet' | 'Fireball' | 'Laser' | 'Mirror' = 'Albacore';
  let sail_number = '';
  let helmsman = '';

  const CLASS_OPTIONS = ['Albacore', 'Comet', 'Fireball', 'Laser', 'Mirror'].sort();

  function mapBoat(raw: any): Boat {
    return {
      id: raw.id ?? raw._id ?? String(raw._id ?? Date.now()),
      name: raw.name ?? raw.nom ?? undefined,
      classe: raw.classe ?? raw.class ?? undefined,
      sail_number: raw.sail_number ?? raw.numero_voile ?? undefined,
      helmsman: raw.helmsman ?? raw.barreur ?? undefined,
    } as Boat;
  }

  async function loadBoats() {
    loading = true;
    errorMsg = '';
    try {
      const res = await fetch(`${API_BASE}/boats`);
      if (!res.ok) throw new Error(`GET /boats -> ${res.status}`);
      const raw = await res.json().catch(() => []);
      boats = (Array.isArray(raw) ? raw.map(mapBoat) : []).filter(Boolean) as Boat[];
    } catch (e) {
      errorMsg = e instanceof Error ? e.message : 'Erreur réseau';
    } finally {
      loading = false;
    }
  }

  async function addBoat() {
    errorMsg = '';

    try {
      const nv = sail_number === '' ? undefined : Number(sail_number);
      if (nv !== undefined && Number.isNaN(nv)) {
        errorMsg = 'Numéro de voile doit être un nombre';
        return;
      }

      const payload = {
        name: name.trim() === '' ? undefined : name.trim(),
        classe: classe,
        sail_number: nv,
        class: classe,
        helmsman: helmsman.trim() === '' ? undefined : helmsman.trim(),
      };

      console.debug('POST /boats payload:', payload);

      const res = await fetch(`${API_BASE}/boats`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const txt = await res.text().catch(() => null);
        let detail: string | null = null;
        if (txt) {
          try {
            const j = JSON.parse(txt);
            detail = j.detail ?? j.message ?? JSON.stringify(j);
          } catch {
            detail = txt;
          }
        }
        throw new Error(detail ? `POST /boats -> ${res.status}: ${detail}` : `POST /boats -> ${res.status}`);
      }

      const createdRaw = await res.json().catch(() => null);
      console.debug('addBoat created (raw):', createdRaw);

      if (createdRaw) {
        const createdBoat = mapBoat(createdRaw);
        boats = [createdBoat, ...boats];
      } else {
        const localBoat: Boat = {
          id: `local-${Date.now()}`,
          name: name.trim() === '' ? undefined : name.trim(),
          classe: classe,
          sail_number: nv,
          helmsman: helmsman.trim() === '' ? undefined : helmsman.trim(),
        };
        boats = [localBoat, ...boats];
      }

      name = '';
      classe = 'Albacore';
      sail_number = '';
      helmsman = '';
      formOpen = false;
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

  function onHeaderLinkClick(e: MouseEvent) {
    e.preventDefault();
    alert('MVP : seule la page Bateaux est disponible.');
  }

  onMount(loadBoats);
</script>

<header>
  <h2>YRR — Prototype</h2>
  <div class="header-center">
    <nav class="main-nav-bar">
      <div class="nav-left">
        <a href="#" on:click={onHeaderLinkClick}>Accueil</a>
        <a href="#" on:click={onHeaderLinkClick}>Classes</a>
        <a href="#" class="active" on:click={onHeaderLinkClick}>Bateaux</a>
        <a href="#" on:click={onHeaderLinkClick}>Séries</a>
        <a href="#" on:click={onHeaderLinkClick}>Course</a>
      </div>
    </nav>
  </div>
  <div class="nav-user">
    <a href="#" class="nav-user-link" on:click={onHeaderLinkClick}>
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

            <label class="stack" for="boatClass">
              <span>Classe</span>
              <select id="boatClass" bind:value={classe}>
                {#each CLASS_OPTIONS as opt}
                  <option value={opt}>{opt}</option>
                {/each}
              </select>
            </label>

            <label class="stack" for="boatNumber">
              <span>Numéro de voile</span>
              <input id="boatNumber" type="text" inputmode="decimal" bind:value={sail_number} placeholder="e.g. 1234" />
            </label>

            <label class="stack" for="boatHelmsman">
              <span>Barreur</span>
              <input id="boatHelmsman" type="text" bind:value={helmsman} placeholder="Jean Dupont" />
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
            <th>Classe</th>
            <th>Numéro de voile</th>
            <th>Barreur</th>
            <th class="action-cell"></th>
          </tr>
        </thead>
        <tbody>
          {#if loading}
            <tr>
              <td colspan="5" class="muted">Chargement…</td>
            </tr>
          {:else if boats.length === 0}
            <tr>
              <td colspan="5" class="muted">Aucun bateau</td>
            </tr>
          {:else}
            {#each boats as b (b.id)}
              <tr>
                <td>{b.name ?? ''}</td>
                <td>{b.classe ?? ''}</td>
                <td>{b.sail_number ?? ''}</td>
                <td>{b.helmsman ?? ''}</td>
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
      <a class="button-ghost" href="#" on:click={onHeaderLinkClick}>Retour</a>
    </div>
  </section>
</div>

<footer class="muted mt-18">MVP fonctionnel — interface connectée à MongoDB.</footer>