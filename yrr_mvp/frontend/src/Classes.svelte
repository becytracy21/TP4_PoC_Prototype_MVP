<script lang="ts">
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
    id: number;
    name: string;
    handicap_type: 'PY' | 'TMF';
    handicap_value: number;
  };

  // Données des classes
  let classes: BoatClass[] = [
    { id: 1, name: 'Albacore', handicap_type: 'PY', handicap_value: 1068 },
    { id: 2, name: 'Laser', handicap_type: 'PY', handicap_value: 1078 },
    { id: 3, name: 'Solo', handicap_type: 'PY', handicap_value: 1155 },
    { id: 4, name: 'TS-240', handicap_type: 'TMF', handicap_value: 998 },
    { id: 5, name: 'Wanderer', handicap_type: 'PY', handicap_value: 1155 },
  ];

  // Ensemble des IDs sélectionnés
  let selectedIds = new Set<number>();

  // ID de la dernière ligne sélectionnée (pour Shift+clic)
  let lastSelectedId: number | null = null;

  // Fonction pour afficher une notification
  function showNotification(message: string) {
    snackMessage = message;
    showSnack = true;
    // Masquer automatiquement après 3 secondes
    setTimeout(() => {
      showSnack = false;
    }, 3000);
  }

  // Fonction pour ajouter une classe
  function addClass() {
    // Validation simple
    if (!className.trim()) {
      showNotification('Le nom de la classe est requis');
      return;
    }
    if (!handicap_value.trim()) {
      showNotification('La valeur de handicap est requise');
      return;
    }
    // Ajouter la nouvelle classe à la liste
    const newId = Math.max(...classes.map(c => c.id), 0) + 1;
    classes = [...classes, {
      id: newId,
      name: className,
      handicap_type,
      handicap_value: Number(handicap_value)
    }];
    // Afficher notification de succès
    showNotification(`Classe ${className} ajoutée avec succès !`);
    // Réinitialiser le formulaire
    className = '';
    handicap_type = 'PY';
    handicap_value = '';
    showModal = false;
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
  function confirmDelete() {
    const count = selectedIds.size;
    classes = classes.filter(c => !selectedIds.has(c.id));
    selectedIds.clear();
    showNotification(`${count} classe(s) supprimée(s) avec succès !`);
    showDeleteConfirm = false;
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
            <th>Nom de la classe</th>
            <th>Type de handicap</th>
            <th class="text-center">Valeur de handicap</th>
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
      <!-- Bouton Supprimer désactivé si aucune ligne sélectionnée -->
      <button class="btn" type="button" on:click={deleteSelected} disabled={selectedIds.size === 0}>
        Supprimer {selectedIds.size > 0 ? `(${selectedIds.size})` : ''}
      </button>
      <button class="btn" type="button">Imprimer</button>
      <a class="button-ghost" href="#" on:click={() => onBack()}>Annuler / Retour</a>
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
