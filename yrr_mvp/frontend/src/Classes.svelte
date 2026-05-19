<script lang="ts">
  import { onMount } from 'svelte';

  export let onBack: () => void = () => {};

  let showModal = false;
  let showDeleteConfirm = false;

  let snackMessage = '';
  let showSnack = false;

  let className = '';
  let handicap_type: 'PY' | 'TMF' = 'PY';
  let handicap_value = '';

  type BoatClass = {
    id: string;
    name: string;
    handicap_type: 'PY' | 'TMF';
    handicap_value: number;
  };

  let classes: BoatClass[] = [];
  const API_URL = 'http://localhost:8000/api';

  async function loadClasses() {
    try {
      const response = await fetch(`${API_URL}/classes`);
      if (response.ok) {
        classes = await response.json();
      } else {
        showNotification('Erreur lors du chargement des classes');
      }
    } catch (error) {
      console.error('Erreur lors du chargement des classes:', error);
      showNotification('Erreur de connexion au serveur');
    }
  }

  onMount(() => {
    loadClasses();
    try {
      history.replaceState(null, '', '/Classes');
    } catch {
    }
  });

  let selectedIds = new Set<string>();
  let lastSelectedId: string | null = null;

  let sortColumn: 'name' | 'handicap_type' | 'handicap_value' | null = null;
  let sortDirection: 'asc' | 'desc' = 'asc';

  function showNotification(message: string) {
    snackMessage = message;
    showSnack = true;
    setTimeout(() => {
      showSnack = false;
    }, 3000);
  }

  function sortClasses(column: 'name' | 'handicap_type' | 'handicap_value') {
    if (sortColumn === column) {
      sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
    } else {
      sortColumn = column;
      sortDirection = 'asc';
    }

    classes = [...classes].sort((a, b) => {
      let aVal: any = a[column];
      let bVal: any = b[column];
      if (typeof aVal === 'string') aVal = aVal.toLowerCase();
      if (typeof bVal === 'string') bVal = bVal.toLowerCase();
      if (aVal < bVal) return sortDirection === 'asc' ? -1 : 1;
      if (aVal > bVal) return sortDirection === 'asc' ? 1 : -1;
      return 0;
    });
  }

  async function addClass() {
    if (!className.trim()) {
      showNotification('Le nom de la classe est requis');
      return;
    }
    if (!handicap_value.trim()) {
      showNotification('La valeur de handicap est requise');
      return;
    }

    try {
      const response = await fetch(`${API_URL}/classes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: className,
          handicap_type,
          handicap_value: parseFloat(handicap_value),
        }),
      });

      if (response.ok) {
        const newClass = await response.json();
        classes = [...classes, newClass];
        showNotification(`Classe ${className} ajoutée avec succès !`);
        className = '';
        handicap_type = 'PY';
        handicap_value = '';
        showModal = false;
      } else {
        const error = await response.json();
        showNotification(`Erreur : ${error.detail || "Impossible d'ajouter la classe"}`);
      }
    } catch (error) {
      console.error("Erreur lors de l'ajout:", error);
      showNotification('Erreur de connexion au serveur');
    }
  }

  function deleteSelected() {
    if (selectedIds.size === 0) {
      showNotification('Aucune classe sélectionnée');
      return;
    }
    showDeleteConfirm = true;
  }

  async function confirmDelete() {
    const count = selectedIds.size;
    const idsToDelete = Array.from(selectedIds);

    try {
      for (const id of idsToDelete) {
        const response = await fetch(`${API_URL}/classes/${id}`, { method: 'DELETE' });
        if (!response.ok) {
          showNotification(`Erreur lors de la suppression de la classe ${id}`);
          return;
        }
      }

      classes = classes.filter((c) => !selectedIds.has(c.id));
      selectedIds.clear();
      showNotification(`${count} classe(s) supprimée(s) avec succès !`);
      showDeleteConfirm = false;
    } catch (error) {
      console.error('Erreur lors de la suppression:', error);
      showNotification('Erreur de connexion au serveur');
    }
  }

  function cancelDelete() {
    showDeleteConfirm = false;
  }

  function toggleSelect(id: string) {
    if (selectedIds.has(id)) {
      selectedIds.delete(id);
    } else {
      selectedIds.add(id);
    }
    selectedIds = selectedIds;
    lastSelectedId = id;
  }

  function toggleSelectWithCtrl(id: string, event: MouseEvent) {
    if ((event.ctrlKey || event.metaKey) && lastSelectedId !== null) {
      const lastIndex = classes.findIndex((c) => c.id === lastSelectedId);
      const currentIndex = classes.findIndex((c) => c.id === id);

      if (lastIndex !== -1 && currentIndex !== -1) {
        const start = Math.min(lastIndex, currentIndex);
        const end = Math.max(lastIndex, currentIndex);
        for (let i = start; i <= end; i++) {
          selectedIds.add(classes[i].id);
        }
        selectedIds = selectedIds;
      }
    } else {
      toggleSelect(id);
    }
  }

  function toggleSelectAll() {
    if (selectedIds.size === 0) {
      selectedIds = new Set(classes.map((c) => c.id));
    } else {
      selectedIds.clear();
      selectedIds = selectedIds;
    }
  }

  function openModal() {
    showModal = true;
  }

  function closeModal() {
    showModal = false;
    className = '';
    handicap_type = 'PY';
    handicap_value = '';
  }

  function handleBackdropClick(e: MouseEvent) {
    if (e.target === e.currentTarget) {
      closeModal();
    }
  }

  let headerCheckbox: HTMLInputElement;

  $: if (headerCheckbox) {
    if (selectedIds.size === 0) {
      headerCheckbox.checked = false;
      headerCheckbox.indeterminate = false;
    } else if (selectedIds.size === classes.length) {
      headerCheckbox.checked = true;
      headerCheckbox.indeterminate = false;
    } else {
      headerCheckbox.checked = false;
      headerCheckbox.indeterminate = true;
    }
  }

  function printClasses() {
    const printWindow = window.open('', '_blank');

    if (!printWindow) {
      showNotification("Erreur lors de l'ouverture de la fenêtre d'impression");
      return;
    }

    printWindow.document.write(`
      <html>
        <head>
          <title>Impression des classes</title>
          <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 0; }
            .table { width: 100%; border-collapse: collapse; margin: 20px 0; }
            .table th, .table td { border: 1px solid #ddd; padding: 8px; }
            .table th { background-color: #f2f2f2; }
            .table td { vertical-align: top; }
            h2 { text-align: center; }
          </style>
        </head>
        <body>
          <h2>Liste des classes de bateaux</h2>
          <table class="table">
            <thead>
              <tr>
                <th>Nom de la classe</th>
                <th>Type de handicap</th>
                <th>Valeur de handicap</th>
              </tr>
            </thead>
            <tbody>
              ${classes
                .map(
                  (c) => `
                <tr>
                  <td>${escapeHtml(c.name)}</td>
                  <td>${escapeHtml(c.handicap_type)}</td>
                  <td>${escapeHtml(c.handicap_value)}</td>
                </tr>
              `,
                )
                .join('')}
            </tbody>
          </table>
        </body>
      </html>
    `);

    printWindow.document.close();
    printWindow.focus();
    printWindow.print();
    printWindow.close();
  }

  function escapeHtml(str: any) {
    if (str == null) return '';
    return String(str).replace(/[&<>"]/g, (s) => {
      switch (s) {
        case '&':
          return '&amp;';
        case '<':
          return '&lt;';
        case '>':
          return '&gt;';
        case '"':
          return '&quot;';
        default:
          return s;
      }
    });
  }
</script>

<div class="container-main">
  <div class="hero">
    <h2 class="hero-title">Gestion des classes</h2>
    <p class="hero-subtitle">Liste des classes de bateaux et gestion</p>
    <div class="title-underline" aria-hidden="true"></div>
  </div>

  <section class="panel">
    <h3>Classes de bateaux</h3>

    <div class="table-wrapper">
      <table class="table-standard" aria-label="Classes de bateaux">
        <thead>
          <tr>
            <th class="checkbox-cell">
              <input bind:this={headerCheckbox} type="checkbox" on:change={toggleSelectAll} aria-label="Sélectionner tout" />
            </th>
            <th role="button" class="th-sort" on:click={() => sortClasses('name')}>
              Nom de la classe {sortColumn === 'name' ? (sortDirection === 'asc' ? '▲' : '▼') : ''}
            </th>
            <th role="button" class="th-sort" on:click={() => sortClasses('handicap_type')}>
              Type de handicap {sortColumn === 'handicap_type' ? (sortDirection === 'asc' ? '▲' : '▼') : ''}
            </th>
            <th role="button" class="th-sort text-center" style="text-align: center; border-left: none; border-right: none;" on:click={() => sortClasses('handicap_value')}>
              Valeur de handicap {sortColumn === 'handicap_value' ? (sortDirection === 'asc' ? '▲' : '▼') : ''}
            </th>
          </tr>
        </thead>
        <tbody>
          {#each classes as boatClass (boatClass.id)}
            <tr
              class={selectedIds.has(boatClass.id) ? 'selected' : ''}
              on:click={(e) => toggleSelectWithCtrl(boatClass.id, e)}
              role="button"
              tabindex="0"
              on:keydown={(e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                  toggleSelectWithCtrl(boatClass.id, e as any);
                }
              }}
            >
              <td class="checkbox-cell"></td>
              <td>{boatClass.name}</td>
              <td>
                <span class={'badge ' + (boatClass.handicap_type === 'PY' ? 'badge--py' : 'badge--tmf')}>{boatClass.handicap_type}</span>
              </td>
              <td class="text-center">{boatClass.handicap_value}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>

    <div class="actions-row mt-2">
      <button class="btn" type="button" on:click={openModal}>Ajouter</button>
      <button class="btn" type="button" on:click={printClasses}>Imprimer</button>
      <button class="button-ghost" type="button" on:click={onBack}>Retour</button>
      <button class="btn-delete push-right" type="button" on:click={deleteSelected} disabled={selectedIds.size === 0}>
        Supprimer {selectedIds.size > 0 ? `(${selectedIds.size})` : ''}
      </button>
    </div>
  </section>
</div>

<div
  class="modal-backdrop {showModal ? 'active' : ''}"
  aria-hidden={!showModal}
  on:click={(e) => e.target === e.currentTarget && handleBackdropClick(e)}
>
  <div class="modal">
    <div class="modal-header">
      <h2>Ajouter une classe</h2>
      <button class="modal-close" type="button" on:click={closeModal}>&times;</button>
    </div>
    <form class="modal-body" on:submit|preventDefault={addClass}>
      <div class="row">
        <label class="stack" for="className">
          <span>Nom de la classe</span>
          <input id="className" type="text" bind:value={className} placeholder="Albacore" />
        </label>
      </div>

      <div class="row mt-8">
        <label class="stack" for="classType">
          <span>H/cap type</span>
          <select id="classType" bind:value={handicap_type}>
            <option value="PY">PY</option>
            <option value="TMF">TMF</option>
          </select>
        </label>

        <label class="stack" for="classValue">
          <span>H/cap value</span>
          <input id="classValue" type="text" inputmode="decimal" bind:value={handicap_value} placeholder="e.g. 1.068" />
        </label>
      </div>

      <div class="modal-footer">
        <button class="btn btn-outline" type="button" on:click={closeModal}>Annuler</button>
        <button class="btn btn-primary" type="submit">Ajouter</button>
      </div>
    </form>
  </div>
</div>

<div class="snack-bar {showSnack ? 'active' : ''}">
  {snackMessage}
</div>

<div
  class="modal-backdrop {showDeleteConfirm ? 'active' : ''}"
  aria-hidden={!showDeleteConfirm}
  on:click={(e) => {
    if (e.target === e.currentTarget) {
      cancelDelete();
    }
  }}
>
  <div class="modal">
    <div class="modal-header">
      <h2>Confirmer la suppression</h2>
      <button class="modal-close" type="button" on:click={cancelDelete}>&times;</button>
    </div>
    <div class="modal-body">
      <p>Êtes-vous sûr de vouloir supprimer {selectedIds.size} classe(s) ? Cette action est irréversible.</p>
    </div>
    <div class="modal-footer">
      <button class="btn btn-outline" type="button" on:click={cancelDelete}>Annuler</button>
      <button class="btn-delete" type="button" on:click={confirmDelete}>Supprimer</button>
    </div>
  </div>
</div>
