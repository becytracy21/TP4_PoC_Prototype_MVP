<script lang="ts">
  import { onMount } from 'svelte';

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
    if (!confirm('Supprimer ce bateau ?')) return;

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

  onMount(loadBoats);
</script>

<div class="container-main">
  <div class="hero">
    <h2 class="hero-title">Gestion des bateaux</h2>
    <p class="hero-subtitle">Liste des bateaux inscrits (MVP)</p>
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
            <div class="col">
              <label for="boatName">Nom du bateau (optionnel)</label>
              <input id="boatName" type="text" bind:value={name} placeholder="Sea Breeze" />
            </div>
          </div>

          <div class="row mt-8">
            <div class="col">
              <label for="boatType">H/cap type</label>
              <select id="boatType" bind:value={handicap_type}>
                <option value="PY">PY</option>
                <option value="TMF">TMF</option>
              </select>
            </div>

            <div class="col">
              <label for="boatValue">H/cap value</label>
              <input
                id="boatValue"
                type="number"
                step="any"
                bind:value={handicap_value}
                placeholder="e.g. 1.234"
                required
              />
            </div>
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
              <td colspan="4" class="muted">Aucun bateau (ajoute-en un avec “+ Ajouter un bateau”).</td>
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
  </section>
</div>

<footer class="muted mt-18">MVP — page unique Bateaux (MongoDB + Django + Svelte).</footer>

<style>
  /* Styles adaptés du prototype HTML/CSS (look & feel) */
  :global(:root) {
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
    --table-hover: rgba(52, 211, 153, 0.1);
    --table-zebra: rgba(124, 58, 237, 0.04);
    --text: #2d1a3a;
    --accent-1: #a259e6;
    --accent-2: #7c3aed;
  }

  :global(html, body, #app) {
    height: 100%;
  }

  :global(body) {
    margin: 0;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    font-family: Inter, Segoe UI, Roboto, Arial, sans-serif;
    font-size: 16px;
    color: var(--text);
    background: var(--bg);
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

  .container-main {
    margin: auto;
    max-width: 1160px;
    min-height: 0;
    padding: 24px;
    padding-bottom: 120px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }

  .hero {
    position: relative;
    margin: 12px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
  }

  .hero-title {
    margin: 0;
    font-size: 2.2rem;
    line-height: 1.02;
    font-weight: 800;
    color: var(--accent-2);
  }

  .hero-subtitle {
    margin: 0;
    font-size: 1rem;
    color: var(--muted);
    opacity: 0.95;
  }

  .title-underline {
    width: 120px;
    height: 8px;
    margin: 8px auto;
    border-radius: 999px;
    background: var(--accent);
    box-shadow: 0 8px 20px rgba(124, 58, 237, 0.12);
  }

  .panel {
    width: 1160px;
    min-width: 1160px;
    max-width: 1160px;
    height: 480px;
    min-height: 480px;
    max-height: 480px;
    padding: 12px 18px;
    border-radius: var(--radius);
    background: var(--card);
    box-shadow: var(--shadow);
    display: flex;
    flex-direction: column;
    overflow: auto;
  }

  h3 {
    margin: 6px 0 12px;
    color: var(--accent-2);
  }

  .row {
    display: flex;
    gap: 12px;
  }

  .col {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  label {
    font-size: 13px;
    color: var(--muted);
  }

  input[type='text'],
  input[type='number'],
  select {
    padding: 10px;
    border-radius: var(--radius);
    border: 1px solid var(--input-border);
    background: var(--input-bg);
    color: var(--text);
    outline: none;
  }

  .actions {
    margin-top: 6px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
  }

  .btn {
    padding: 12px 18px;
    border: none;
    cursor: pointer;
    border-radius: var(--radius);
    font-weight: 800;
    background: var(--accent);
    color: var(--card);
    box-shadow: 0 12px 36px rgba(124, 58, 237, 0.12);
  }

  .btn:hover {
    background: var(--green-gradient);
  }

  .btn.btn-outline {
    background: transparent;
    border: 1px solid rgba(124, 58, 237, 0.22);
    color: var(--accent-2);
    box-shadow: none;
  }

  .btn.btn-outline:hover {
    background: rgba(52, 211, 153, 0.14);
    border-color: rgba(52, 211, 153, 0.65);
    color: var(--text);
  }

  .btn-delete {
    padding: 8px 12px;
    border: none;
    border-radius: var(--radius);
    cursor: pointer;
    background: var(--danger);
    color: var(--card);
    font-weight: 800;
    box-shadow: var(--danger-shadow);
  }

  .btn-delete:hover {
    background: var(--danger-2);
  }

  .table-wrapper {
    width: 100%;
    margin-bottom: 18px;
    overflow: auto;
    max-height: 277.5px;
    border: 1px solid var(--table-border);
    border-radius: var(--radius);
    background: rgba(255, 255, 255, 0.55);
    box-shadow: var(--shadow);
  }

  .table-standard {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    background-color: transparent;
  }

  .table-standard thead {
    background: var(--table-head-bg);
  }

  .table-standard th,
  .table-standard td {
    padding: 10px 12px;
    border-bottom: 1px solid var(--table-border);
  }

  .table-standard th {
    white-space: nowrap;
    text-align: left;
    font-weight: 800;
    color: var(--accent-2);
  }

  .table-standard td {
    vertical-align: middle;
    background: rgba(255, 255, 255, 0.35);
  }

  .table-standard tbody tr:nth-child(even) td {
    background: var(--table-zebra);
  }

  .table-standard tbody tr:hover td {
    background: var(--table-hover);
  }

  .table-standard tbody tr:last-child td {
    border-bottom: none;
  }

  .action-cell {
    white-space: nowrap;
    text-align: center;
  }

  .badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 4px 10px;
    border: 1px solid transparent;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 0.02em;
  }

  .badge--py {
    background: var(--badge-py-bg);
    border-color: var(--badge-py-border);
    color: var(--accent-2);
  }

  .badge--tmf {
    background: var(--badge-tmf-bg);
    border-color: var(--badge-tmf-border);
    color: var(--green-2);
  }

  details.add-details {
    overflow: hidden;
    border: 1px solid rgba(124, 58, 237, 0.14);
    border-radius: var(--radius);
    background: rgba(255, 255, 255, 0.55);
    box-shadow: 0 10px 28px rgba(44, 18, 80, 0.05);
  }

  summary.add-summary {
    padding: 12px 14px;
    cursor: pointer;
    list-style: none;
    font-weight: 900;
    color: var(--accent-2);
  }

  summary.add-summary::-webkit-details-marker {
    display: none;
  }

  .add-form {
    padding: 14px;
    border-top: 1px solid rgba(124, 58, 237, 0.1);
  }

  footer {
    position: fixed;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 1000;
    padding: 12px 24px;
    text-align: center;
    font-size: 13px;
    color: var(--muted);
    background: rgba(255, 255, 255, 0.5);
    box-shadow: 0 -6px 20px rgba(11, 36, 64, 0.05);
  }

  .muted {
    color: var(--muted);
    font-weight: 700;
  }

  .mt-8 {
    margin-top: 8px;
  }

  .mb-18 {
    margin-bottom: 18px;
  }

  .mt-18 {
    margin-top: 18px;
  }

  .error {
    border-radius: var(--radius);
    padding: 10px 12px;
    margin-bottom: 12px;
    background: rgba(220, 38, 38, 0.08);
    border: 1px solid rgba(220, 38, 38, 0.22);
    color: var(--danger-2);
    font-weight: 800;
  }

  @media (max-width: 960px) {
    .panel {
      width: 100%;
      min-width: 0;
      max-width: 100%;
      height: auto;
      min-height: 0;
      max-height: none;
    }

    .row {
      flex-direction: column;
    }

    footer {
      position: static;
    }

    .container-main {
      padding-bottom: 24px;
    }
  }
</style>
