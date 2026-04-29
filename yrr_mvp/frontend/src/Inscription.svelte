<script lang="ts">
// Pas de logique spécifique pour cette page statique
import { onMount } from 'svelte';

interface Inscription {
  nom: string;
  classe: string;
  numero: string;
  barreur: string;
  resultat: string;
  position: string;
  points: string;
}

let inscriptions: Inscription[] = [
  { nom: 'Whisky', classe: 'Laser', numero: '100231', barreur: 'Fred', resultat: '14:10:22', position: '3', points: '3' },
  { nom: 'Fuzzy Duck', classe: 'Laser', numero: '132248', barreur: 'Graham', resultat: '14:09:46', position: '1', points: '1' }
];

let showForm = false;
let form = {
  nom: '',
  classe: '',
  numero: '',
  barreur: '',
  resultat: '',
  position: '',
  points: ''
};

function openForm() {
  showForm = true;
}
function closeForm() {
  showForm = false;
  form = { nom: '', classe: '', numero: '', barreur: '', resultat: '', position: '', points: '' };
}
function addInscription() {
  inscriptions = [...inscriptions, { ...form }];
  closeForm();
}
</script>

<header>
  <h2>YRR — Prototype</h2>
  <div class="header-center">
    <nav class="main-nav-bar">
      <div class="nav-left">
        <a href="/Accueil">Accueil</a>
        <a href="/Classes">Classes</a>
        <a href="/Bateaux">Bateaux</a>
        <a href="/Series">Séries</a>
        <a href="/Course">Course</a>
        <a href="/Inscription" class="active">Inscription</a>
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
    <h3>Inscriptions à la course — Série A ({inscriptions.length})</h3>
    <div class="table-wrapper">
      <table class="table-standard" aria-label="Inscriptions à la course">
        <thead>
          <tr>
            <th>Nom du bateau</th>
            <th>Classe de bateau</th>
            <th>Numéro de voile</th>
            <th>Barreur</th>
            <th>Résultat</th>
            <th class="text-center">Position</th>
            <th class="text-center">Points</th>
          </tr>
        </thead>
        <tbody>
          {#each inscriptions as insc}
            <tr>
              <td>{insc.nom}</td>
              <td>{insc.classe}</td>
              <td>{insc.numero}</td>
              <td>{insc.barreur}</td>
              <td>{insc.resultat}</td>
              <td class="text-center">{insc.position}</td>
              <td class="text-center">{insc.points}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
    <div class="actions-row mt-2">
      <button class="btn" on:click={openForm}>Ajouter</button>
      <a class="btn" href="#">Supprimer</a>
      <a class="btn" href="#">Imprimer</a>
      <a class="button-ghost" href="#">Précédent</a>
      <a class="button-ghost" href="#">Suivant</a>
      <a class="button-ghost" href="Accueil.html">Annuler / Retour</a>
    </div>
    {#if showForm}
      <div class="modal-backdrop">
        <div class="modal-form">
          <h4>Ajouter une inscription</h4>
          <form on:submit|preventDefault={addInscription}>
            <label>Nom du bateau <input bind:value={form.nom} required placeholder="ex: Whisky" /></label>
            <label>Classe de bateau <input bind:value={form.classe} required placeholder="ex: Laser" /></label>
            <label>Numéro de voile <input bind:value={form.numero} required placeholder="ex: 123456" /></label>
            <label>Barreur <input bind:value={form.barreur} required placeholder="ex: Jean" /></label>
            <label>Résultat <input bind:value={form.resultat} placeholder="ex: 14:10:22 ou RTD" /></label>
            <label>Position <input bind:value={form.position} placeholder="ex: 1" /></label>
            <label>Points <input bind:value={form.points} placeholder="ex: 1" /></label>
            <div class="actions">
              <button class="btn btn-primary" type="submit">Valider</button>
              <button class="btn btn-outline" type="button" on:click={closeForm}>Annuler</button>
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
.modal-form input {
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
