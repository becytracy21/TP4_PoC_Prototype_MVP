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

  // notification state
  let notification = '';
  let notificationType: 'success' | 'error' = 'success';
  function showNotification(msg: string, type: 'success' | 'error' = 'success') {
    notification = msg;
    notificationType = type;
    setTimeout(() => {
      notification = '';
    }, 3000);
  }

  let formOpen = false;
  let editingId: string | null = null;

  let name = '';
  let classe: 'Albacore' | 'Comet' | 'Fireball' | 'Laser' | 'Mirror' = 'Albacore';
  let sail_number = '';
  let helmsman = '';

  // fields used for inline row editing (ne pas confondre avec le formulaire d'ajout)
  let editName = '';
  let editClasse: 'Albacore' | 'Comet' | 'Fireball' | 'Laser' | 'Mirror' = 'Albacore';
  let editSailNumber = '';
  let editHelmsman = '';

  const CLASS_OPTIONS = ['Albacore', 'Comet', 'Fireball', 'Laser', 'Mirror'].sort();

  // filtre / contrôle de la classe (apparence « pill / dropdown »)
  let classFilter: string | null = null;
  let classFilterOpen = false;

  // liste visible selon filtre
  $: visibleBoats = classFilter ? boats.filter(b => b.classe === classFilter) : boats;

  function toggleClassFilter() {
    classFilterOpen = !classFilterOpen;
  }

  function selectClassFilter(c: string) {
    classFilter = c;
    classFilterOpen = false;
  }

  function clearClassFilter() {
    classFilter = null;
    classFilterOpen = false;
  }

  // état de tri pour le nom (null = pas de tri, true = A→Z, false = Z→A)
  let sortAsc: boolean | null = null;
  // état de tri pour le barreur
  let sortHelmsAsc: boolean | null = null;

  function sortBoatsByName() {
    if (sortAsc === null) return;
    boats = [...boats].sort((a, b) => {
      const na = (a.name ?? '').toLowerCase();
      const nb = (b.name ?? '').toLowerCase();
      if (na < nb) return sortAsc ? -1 : 1;
      if (na > nb) return sortAsc ? 1 : -1;
      return 0;
    });
  }

  function sortBoatsByHelmsman() {
    if (sortHelmsAsc === null) return;
    boats = [...boats].sort((a, b) => {
      const ha = (a.helmsman ?? '').toLowerCase();
      const hb = (b.helmsman ?? '').toLowerCase();
      if (ha < hb) return sortHelmsAsc ? -1 : 1;
      if (ha > hb) return sortHelmsAsc ? 1 : -1;
      return 0;
    });
  }

  function toggleSortName() {
    // bascule entre ascendant / descendant
    sortAsc = sortAsc === null ? true : !sortAsc;
    // désactiver le tri sur Barreur
    sortHelmsAsc = null;
    sortBoatsByName();
  }

  function toggleSortHelmsman() {
    sortHelmsAsc = sortHelmsAsc === null ? true : !sortHelmsAsc;
    // désactiver le tri sur Nom
    sortAsc = null;
    sortBoatsByHelmsman();
  }

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
      // Appliquer le tri si actif
      if (sortAsc !== null) sortBoatsByName();
      if (sortHelmsAsc !== null) sortBoatsByHelmsman();
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
        showNotification(errorMsg, 'error');
        return;
      }

      const payload = {
        name: name.trim() === '' ? undefined : name.trim(),
        classe: classe,
        sail_number: nv,
        class: classe,
        helmsman: helmsman.trim() === '' ? undefined : helmsman.trim(),
      };

      const isEdit = !!editingId;
      const method = isEdit ? 'PUT' : 'POST';
      const url = isEdit ? `${API_BASE}/boats/${editingId}` : `${API_BASE}/boats`;

      console.debug(`${method} ${isEdit ? `/boats/${editingId}` : '/boats'} payload:`, payload);

      const res = await fetch(url, {
        method,
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
        throw new Error(detail ? `${method} ${isEdit ? `/boats/${editingId}` : '/boats'} -> ${res.status}: ${detail}` : `${method} ${isEdit ? `/boats/${editingId}` : '/boats'} -> ${res.status}`);
      }

      const createdRaw = await res.json().catch(() => null);
      console.debug('addBoat/updateBoat result (raw):', createdRaw);

      if (isEdit) {
        // remplacer le bateau existant dans la liste
        if (createdRaw) {
          const updatedBoat = mapBoat(createdRaw);
          boats = boats.map(b => (b.id === editingId ? updatedBoat : b));
        } else {
          const updatedBoat: Boat = {
            id: editingId!,
            name: name.trim() === '' ? undefined : name.trim(),
            classe: classe,
            sail_number: nv,
            helmsman: helmsman.trim() === '' ? undefined : helmsman.trim(),
          };
          boats = boats.map(b => (b.id === editingId ? updatedBoat : b));
        }
      } else {
        // création normale
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
      }

      // Afficher notification de succès pour ajout ou modification
      showNotification(isEdit ? 'Modification enregistrée.' : 'Bateau ajouté.', 'success');

      // reset form
      name = '';
      classe = 'Albacore';
      sail_number = '';
      helmsman = '';
      formOpen = false;
      editingId = null;
    } catch (e) {
      errorMsg = e instanceof Error ? e.message : 'Erreur réseau';
      showNotification(errorMsg, 'error');
    }
  }

  async function deleteBoat(id: string) {
    errorMsg = '';
    if (!confirm('Supprimer ce bateau?')) return;

    // Mise à jour optimiste : retirer immédiatement le bateau de la liste affichée
    const originalBoats = boats.slice();
    boats = boats.filter(b => b.id !== id);

    try {
      const res = await fetch(`${API_BASE}/boats/${id}`, { method: 'DELETE' });
      if (!res.ok && res.status !== 204) {
        const data = await res.json().catch(() => null);
        throw new Error(data?.detail ?? `DELETE /boats/${id} -> ${res.status}`);
      }
      // Si besoin de s'assurer de la cohérence serveur -> on pourrait recharger
      // await loadBoats();
    } catch (e) {
      // Restaure la liste locale et affiche l'erreur
      boats = originalBoats;
      errorMsg = e instanceof Error ? e.message : 'Erreur réseau';
    }
  }

  function editBoat(b: Boat) {
    editingId = b.id;
    // pré-remplir champs d'édition inline
    editName = b.name ?? '';
    editClasse = b.classe ?? 'Albacore';
    editSailNumber = b.sail_number?.toString() ?? '';
    editHelmsman = b.helmsman ?? '';
    // scroll vers la ligne si besoin
    const row = document.querySelector(`#boatRow-${CSS.escape(b.id)}`);
    if (row) (row as HTMLElement).scrollIntoView({ behavior: 'smooth', block: 'center' });
  }

  async function saveEdit() {
    if (!editingId) return;
    errorMsg = '';
    try {
      const nv = editSailNumber === '' ? undefined : Number(editSailNumber);
      if (nv !== undefined && Number.isNaN(nv)) {
        errorMsg = 'Numéro de voile doit être un nombre';
        showNotification(errorMsg, 'error');
        return;
      }

      const payload = {
        name: editName.trim() === '' ? undefined : editName.trim(),
        classe: editClasse,
        sail_number: nv,
        class: editClasse,
        helmsman: editHelmsman.trim() === '' ? undefined : editHelmsman.trim(),
      };

      const url = `${API_BASE}/boats/${editingId}`;
      const methodsToTry = ['PUT', 'PATCH', 'POST'];
      let res: Response | null = null;
      let lastStatus: number | null = null;

      for (const method of methodsToTry) {
        res = await fetch(url, {
          method,
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        }).catch(() => null);

        if (!res) continue;
        lastStatus = res.status;

        if (res.ok) {
          // success
          break;
        }

        // If server explicitly rejects method, try next method
        if (res.status === 405) {
          // try next method
          continue;
        }

        // For other errors, parse detail and throw
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
        throw new Error(detail ? `${method} ${url} -> ${res.status}: ${detail}` : `${method} ${url} -> ${res.status}`);
      }

      // Si toutes les méthodes sur /boats/:id retournent 405, tenter POST /boats avec id
      if (!res || !res.ok) {
        // si dernier status est 405, tenter POST /boats en incluant l'id
        if (lastStatus === 405) {
          const postUrl = `${API_BASE}/boats`;
          const payloadWithId = { id: editingId, ...payload };
          const tryPost = await fetch(postUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payloadWithId),
          }).catch(() => null);

          if (tryPost && tryPost.ok) {
            res = tryPost;
          } else {
            // fallback: appliquer localement et informer l'utilisateur
            boats = boats.map(b => (b.id === editingId ? ({ id: editingId!, name: payload.name, classe: payload.classe, sail_number: payload.sail_number, helmsman: payload.helmsman } as Boat) : b));
            errorMsg = 'Mise à jour appliquée localement — le serveur n’accepte pas les méthodes de mise à jour (405). Vérifiez l’API.';
            editingId = null;
            return;
          }
        } else {
          throw new Error(lastStatus ? `Update failed -> ${lastStatus}` : 'Erreur réseau');
        }
      }

      const updatedRaw = await res.json().catch(() => null);
      if (updatedRaw) {
        const updatedBoat = mapBoat(updatedRaw);
        boats = boats.map(b => (b.id === editingId ? updatedBoat : b));
      } else {
        boats = boats.map(b => (b.id === editingId ? ({ id: editingId!, name: payload.name, classe: payload.classe, sail_number: payload.sail_number, helmsman: payload.helmsman } as Boat) : b));
      }

      editingId = null;
      showNotification('Modification enregistrée.', 'success');
    } catch (e) {
      errorMsg = e instanceof Error ? e.message : 'Erreur réseau';
    }
  }

  function cancelEdit() {
    editingId = null;
    editName = '';
    editClasse = 'Albacore';
    editSailNumber = '';
    editHelmsman = '';
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

  <section class="panel" style="position:relative;">
    <h3>Liste des bateaux</h3>

    {#if notification}
      <div class={"notification-wrap " + (notificationType === 'success' ? 'success' : 'error')} role="status" aria-live="polite" style="position:absolute;left:50%;transform:translateX(-50%);top:46px;z-index:9999;pointer-events:none;">
        <div style="pointer-events:auto;min-width:220px;max-width:640px;padding:0.45rem 0.9rem;border-radius:10px;background:linear-gradient(90deg,#7c3aed,#a78bfa);box-shadow:0 10px 30px rgba(0,0,0,0.12);color:#fff;text-align:center;font-weight:700;">
          {notification}
        </div>
      </div>
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
            <button class="btn btn-primary" type="submit">{editingId ? 'Enregistrer' : 'Ajouter'}</button>
            <button class="btn btn-outline" type="button" on:click={() => { formOpen = false; editingId = null; }}>Annuler</button>
          </div>
        </form>
      </details>
    </div>

    <div class="table-wrapper" class:filter-open={classFilterOpen}>
      <table class="table-standard" aria-label="Tableau des bateaux" id="boatTable">
        <thead>
          <tr>
            <th style="display:flex;align-items:center;gap:6px;">
              <span>Nom du bateau</span>
              <button class="mini-sort" type="button" on:click={toggleSortName} aria-label="Trier par nom" title="Trier par nom" style="font-size:0.8rem;padding:2px 6px;border-radius:6px;">
                {#if sortAsc === null}⇅{:else if sortAsc}▲{:else}▼{/if}
              </button>
            </th>
            <th style="min-width:160px;">
              <div class="class-filter-wrap" style="display:flex;align-items:center;gap:10px;">
                <span class="th-label">Classe</span>
                <div class="class-filter">
                  <button type="button" class="class-filter-btn" on:click={toggleClassFilter} aria-haspopup="listbox" aria-expanded={classFilterOpen} title="Filtrer par classe">
                    <span class="pill-label">{classFilter ?? 'Toutes'}</span>
                    <span class="caret">▾</span>
                  </button>
                  {#if classFilterOpen}
                    <ul class="class-filter-menu" role="listbox">
                      <li class="class-filter-item all" on:click={clearClassFilter}>Tous</li>
                      {#each CLASS_OPTIONS as opt}
                        <li class="class-filter-item" on:click={() => selectClassFilter(opt)} aria-selected={classFilter === opt}>{opt}</li>
                      {/each}
                    </ul>
                  {/if}
                </div>
              </div>
            </th>
            <th>Numéro de voile</th>
            <th style="display:flex;align-items:center;gap:6px;">
              <span>Barreur</span>
              <button class="mini-sort" type="button" on:click={toggleSortHelmsman} aria-label="Trier par barreur" title="Trier par barreur" style="font-size:0.8rem;padding:2px 6px;border-radius:6px;">
                {#if sortHelmsAsc === null}⇅{:else if sortHelmsAsc}▲{:else}▼{/if}
              </button>
            </th>
            <th class="action-cell"></th>
          </tr>
        </thead>
        <tbody>
          {#if loading}
            <tr>
              <td colspan="5" class="muted">Chargement…</td>
            </tr>
          {:else if visibleBoats.length === 0}
            <tr>
              <td colspan="5" class="muted">Aucun bateau</td>
            </tr>
          {:else}
            {#each visibleBoats as b (b.id)}
              <tr id={"boatRow-" + b.id}>
                {#if editingId === b.id}
                  <td><input type="text" class="input-inline" bind:value={editName} /></td>
                  <td>
                    <select bind:value={editClasse} class="input-inline">
                      {#each CLASS_OPTIONS as opt}
                        <option value={opt}>{opt}</option>
                      {/each}
                    </select>
                  </td>
                  <td><input type="text" inputmode="decimal" class="input-inline" bind:value={editSailNumber} /></td>
                  <td><input type="text" class="input-inline" bind:value={editHelmsman} /></td>
                  <td class="action-cell">
                    <button class="btn btn-primary" type="button" on:click={saveEdit}>Enregistrer</button>
                    <button class="btn btn-outline" type="button" on:click={cancelEdit}>Annuler</button>
                  </td>
                {:else}
                  <td>{b.name ?? ''}</td>
                  <td>{b.classe ?? ''}</td>
                  <td>{b.sail_number ?? ''}</td>
                  <td>{b.helmsman ?? ''}</td>
                  <td class="action-cell">
                    <button class="btn btn-primary" type="button" on:click={() => editBoat(b)}>Modifier</button>
                    <button class="btn-delete" type="button" on:click={() => deleteBoat(b.id)}>Supprimer</button>
                  </td>
                {/if}
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

<!-- Styles déplacés dans `src/app.css` -->