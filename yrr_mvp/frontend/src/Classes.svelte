<script lang="ts">
  import { onMount } from 'svelte';
  import './Classes.css';

  export let onBack: () => void = () => {};

  // État pour afficher/masquer la fenêtre pop-up du formulaire
  let showModal = false;

  // État pour la modale de confirmation de suppression
  let showDeleteConfirm = false;

  // État pour la snack bar de notification
  let snackMessage = '';
  let showSnack = false;

  // Variables du formulaire
  let className = '';
  let handicap_type: 'PY' | 'TMF' = 'PY';
  let handicap_value = '';

  // Type pour les classes
  type BoatClass = {
    id: string;
    name: string;
    handicap_type: 'PY' | 'TMF';
    handicap_value: number;
  };

  // Données des classes
  let classes: BoatClass[] = [];

  // URL de base de l'API
  const API_URL = 'http://localhost:8000/api';

  // Charger les classes depuis la base de données
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

  // Charger les classes au montage du composant
  onMount(() => {
    loadClasses();
    // Mettre à jour l'URL pour refléter la page courante sans hashtag
    try {
      history.replaceState(null, '', '/Classes');
    } catch (e) {
      // ignore si l'accès à l'historique n'est pas possible
    }
  });

  // Ensemble des IDs sélectionnés
  let selectedIds = new Set<string>();

  // ID de la dernière ligne sélectionnée (pour Shift+clic)
  let lastSelectedId: string | null = null;

  // État du tri
  let sortColumn: 'name' | 'handicap_type' | 'handicap_value' | null = null;
  let sortDirection: 'asc' | 'desc' = 'asc';

  // Fonction pour afficher une notification
  function showNotification(message: string) {
    snackMessage = message;
    showSnack = true;
    // Masquer automatiquement après 3 secondes
    setTimeout(() => {
      showSnack = false;
    }, 3000);
  }

  // Fonction pour trier les classes
  function sortClasses(column: 'name' | 'handicap_type' | 'handicap_value') {
    if (sortColumn === column) {
      // Si on clique sur la même colonne, inverser la direction
      sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
    } else {
      // Sinon, trier par la nouvelle colonne en ordre croissant
      sortColumn = column;
      sortDirection = 'asc';
    }

    // Trier le tableau
    classes = [...classes].sort((a, b) => {
      let aVal: any = a[column];
      let bVal: any = b[column];

      // Convertir en minuscules pour les strings
      if (typeof aVal === 'string') aVal = aVal.toLowerCase();
      if (typeof bVal === 'string') bVal = bVal.toLowerCase();

      if (aVal < bVal) return sortDirection === 'asc' ? -1 : 1;
      if (aVal > bVal) return sortDirection === 'asc' ? 1 : -1;
      return 0;
    });
  }

  // Fonction pour ajouter une classe
  async function addClass() {
    // Validation simple
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
        headers: {
          'Content-Type': 'application/json',
        },
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
        // Réinitialiser le formulaire
        className = '';
        handicap_type = 'PY';
        handicap_value = '';
        showModal = false;
      } else {
        const error = await response.json();
        showNotification(`Erreur : ${error.detail || 'Impossible d\'ajouter la classe'}`);
      }
    } catch (error) {
      console.error('Erreur lors de l\'ajout:', error);
      showNotification('Erreur de connexion au serveur');
    }
  }

  // Fonction pour supprimer les classes sélectionnées
  function deleteSelected() {
    if (selectedIds.size === 0) {
      showNotification('Aucune classe sélectionnée');
      return;
    }
    // Afficher la modale de confirmation
    showDeleteConfirm = true;
  }

  // Fonction pour confirmer la suppression
  async function confirmDelete() {
    const count = selectedIds.size;
    const idsToDelete = Array.from(selectedIds);

    try {
      // Supprimer chaque classe une par une
      for (const id of idsToDelete) {
        const response = await fetch(`${API_URL}/classes/${id}`, {
          method: 'DELETE',
        });

        if (!response.ok) {
          showNotification(`Erreur lors de la suppression de la classe ${id}`);
          return;
        }
      }

      // Filtrer les classes supprimées
      classes = classes.filter(c => !selectedIds.has(c.id));
      selectedIds.clear();
      showNotification(`${count} classe(s) supprimée(s) avec succès !`);
      showDeleteConfirm = false;
    } catch (error) {
      console.error('Erreur lors de la suppression:', error);
      showNotification('Erreur de connexion au serveur');
    }
  }

  // Fonction pour annuler la suppression
  function cancelDelete() {
    showDeleteConfirm = false;
  }

  // Fonction pour gérer la sélection d'une ligne
  function toggleSelect(id: number) {
    if (selectedIds.has(id)) {
      selectedIds.delete(id);
    } else {
      selectedIds.add(id);
    }
    // Force la mise à jour réactive
    selectedIds = selectedIds;
    lastSelectedId = id;
  }

  // Fonction pour gérer la sélection avec Ctrl+clic (ou Cmd+clic sur Mac)
  function toggleSelectWithCtrl(id: number, event: MouseEvent) {
    if ((event.ctrlKey || event.metaKey) && lastSelectedId !== null) {
      // Trouver les indices des deux lignes
      const lastIndex = classes.findIndex(c => c.id === lastSelectedId);
      const currentIndex = classes.findIndex(c => c.id === id);
      
      if (lastIndex !== -1 && currentIndex !== -1) {
        // Sélectionner toutes les lignes entre lastSelectedId et id (inclus)
        const start = Math.min(lastIndex, currentIndex);
        const end = Math.max(lastIndex, currentIndex);
        
        for (let i = start; i <= end; i++) {
          selectedIds.add(classes[i].id);
        }
        
        // Force la mise à jour réactive
        selectedIds = selectedIds;
      }
    } else {
      // Comportement normal sans Ctrl/Cmd
      toggleSelect(id);
    }
  }

  // Fonction pour cocher/décocher tout
  function toggleSelectAll() {
    if (selectedIds.size === 0) {
      // Si rien n'est sélectionné, sélectionner tout
      selectedIds = new Set(classes.map(c => c.id));
    } else {
      // Sinon, décocher tout
      selectedIds.clear();
      selectedIds = selectedIds; // Force la réactivité
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

  // Fermer la modale en cliquant en dehors
  function handleBackdropClick(e: MouseEvent) {
    if (e.target === e.currentTarget) {
      closeModal();
    }
  }

  // Référence au checkbox du header
  let headerCheckbox: HTMLInputElement;

  // Mettre à jour l'état du checkbox du header
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

  // Fonction pour imprimer la liste des classes
  function printClasses() {
    // Ouvrir une nouvelle fenêtre
    const printWindow = window.open('', '_blank');

    if (!printWindow) {
      showNotification('Erreur lors de l\'ouverture de la fenêtre d\'impression');
      return;
    }

    // Écrire le contenu HTML dans la nouvelle fenêtre
    printWindow.document.write(`
      <html>
        <head>
          <title>Impression des classes</title>
          <style>
            /* Styles de base pour l'impression */
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
              ${classes.map(c => `
                <tr>
                  <td>${escapeHtml(c.name)}</td>
                  <td>${escapeHtml(c.handicap_type)}</td>
                  <td>${escapeHtml(c.handicap_value)}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </body>
      </html>
    `);

    // Attendre que le contenu soit chargé, puis imprimer
    printWindow.document.close();
    printWindow.focus();
    printWindow.print();
    printWindow.close();
  }

  // Nouvelle fonction utilitaire pour échapper du HTML
  function escapeHtml(str: any) {
    if (str == null) return '';
    return String(str).replace(/[&<>"]/g, (s) => {
      switch (s) {
        case '&': return '&amp;';
        case '<': return '&lt;';
        case '>': return '&gt;';
        case '"': return '&quot;';
        default: return s;
      }
    });
  }
</script>

<div class="container-main">
  <div class="hero">
    <h2 class="hero-title">Gestion des classes</h2>
    <p class="hero-subtitle">Liste des classes de bateaux et gestion (prototype, données simulées)</p>
    <div class="title-underline" aria-hidden="true"></div>
  </div>

  <section class="panel">
    <h3>Classes de bateaux</h3>
    <!-- Formulaire dans une fenêtre pop-up modale -->
    <!-- Fin du formulaire modal -->
    <div class="table-wrapper">
      <table class="table-standard" aria-label="Classes de bateaux">
        <thead>
          <tr>
            <th class="checkbox-cell">
              <input 
                bind:this={headerCheckbox}
                type="checkbox" 
                on:change={toggleSelectAll}
                aria-label="Sélectionner tout"
              />
            </th>
            <th role="button" on:click={() => sortClasses('name')} style="cursor: pointer;">
              Nom de la classe {sortColumn === 'name' ? (sortDirection === 'asc' ? '▲' : '▼') : ''}
            </th>
            <th role="button" on:click={() => sortClasses('handicap_type')} style="cursor: pointer;">
              Type de handicap {sortColumn === 'handicap_type' ? (sortDirection === 'asc' ? '▲' : '▼') : ''}
            </th>
            <th role="button" on:click={() => sortClasses('handicap_value')} class="text-center" style="cursor: pointer;">
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
              <td><span class={"badge " + (boatClass.handicap_type === 'PY' ? 'badge--py' : 'badge--tmf')}>
                {boatClass.handicap_type}
              </span></td>
              <td class="text-center">{boatClass.handicap_value}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
    <div class="actions-row mt-2">
      <button class="btn" type="button" on:click={openModal}>Ajouter</button>
      <button class="btn" type="button" on:click={printClasses}>Imprimer</button>
      <a class="button-ghost" href="#" on:click={() => onBack()}>Retour</a>
      <!-- Bouton Supprimer à droite et en rouge -->
      <button class="btn-delete" type="button" on:click={deleteSelected} disabled={selectedIds.size === 0} style="margin-left: auto;">
        Supprimer {selectedIds.size > 0 ? `(${selectedIds.size})` : ''}
      </button>
    </div>
  </section>
</div>

<!-- Fenêtre pop-up modale -->
<div class="modal-backdrop {showModal ? 'active' : ''}" on:click={handleBackdropClick}>
  <div class="modal">
    <div class="modal-header">
      <h2>Ajouter une classe</h2>
      <button class="modal-close" on:click={closeModal}>&times;</button>
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
          <input
            id="classValue"
            type="text"
            inputmode="decimal"
            bind:value={handicap_value}
            placeholder="e.g. 1.068"
          />
        </label>
      </div>

      <div class="modal-footer">
        <button class="btn btn-outline" type="button" on:click={closeModal}>Annuler</button>
        <button class="btn btn-primary" type="submit">Ajouter</button>
      </div>
    </form>
  </div>
</div>

<footer class="muted mt-18">Prototype non fonctionnel — interface de démonstration.</footer>

<!-- Snack bar de notification (sans OK, disparaît automatiquement) -->
<div class="snack-bar {showSnack ? 'active' : ''}">
  {snackMessage}
</div>

<!-- Modale de confirmation de suppression -->
<div class="modal-backdrop {showDeleteConfirm ? 'active' : ''}" on:click={(e) => {
  if (e.target === e.currentTarget) {
    cancelDelete();
  }
}}>
  <div class="modal">
    <div class="modal-header">
      <h2>Confirmer la suppression</h2>
      <button class="modal-close" on:click={cancelDelete}>&times;</button>
    </div>
    <div class="modal-body">
      <p>Êtes-vous sûr de vouloir supprimer {selectedIds.size} classe(s) ? Cette action est irréversible.</p>
    </div>
    <div class="modal-footer">
      <button class="btn btn-outline" type="button" on:click={cancelDelete}>Annuler</button>
      <button class="btn btn-primary" type="button" on:click={confirmDelete} style="background-color: #dc3545; border-color: #dc3545;">
        Supprimer
      </button>
    </div>
  </div>
</div>
