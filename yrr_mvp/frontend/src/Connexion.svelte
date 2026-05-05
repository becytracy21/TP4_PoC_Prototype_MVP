<script lang="ts">
  import { navigate } from './router';

  let email = '';
  let password = '';
  let remember = false;

  let errorMsg = '';

  function submit() {
    // Prototype: pas d'auth réelle côté backend pour l'instant.
    // On simule une connexion et on redirige vers Bateaux.
    errorMsg = '';

    if (email.trim() === '') {
      errorMsg = "L'adresse e-mail est requise.";
      return;
    }
    if (password.trim() === '') {
      errorMsg = 'Le mot de passe est requis.';
      return;
    }

    void remember; // évite un warning TS si non utilisé ailleurs
    navigate('bateaux');
  }

  function onHeaderLinkClick(e: MouseEvent) {
    e.preventDefault();
    alert('Seules certaines pages sont disponibles dans ce prototype.');
  }
</script>

<div class="auth-page">
  <div class="container-main">
    <div class="card auth-card">
      <div class="brand">
        <h2>YRR - Prototype</h2>
        <p>Création de compte (fonctionnel).</p>
        <p>Les données sont enregistrées dans MongoDB.</p>
      </div>

      <div class="form-wrap">
        <h1 class="mt-0">Connexion</h1>
        <p class="lead">Entrez votre email et mot de passe.</p>

        {#if errorMsg}
          <div class="error" role="alert">{errorMsg}</div>
        {/if}

        <form on:submit|preventDefault={submit}>
          <label for="loginEmail">Email</label>
          <input
            id="loginEmail"
            type="email"
            bind:value={email}
            required
            placeholder="exemple@domaine.com"
            autocomplete="email"
          />

          <label for="loginPassword">Mot de passe</label>
          <input
            id="loginPassword"
            type="password"
            bind:value={password}
            required
            placeholder="Votre mot de passe"
            autocomplete="current-password"
          />

          <div class="actions">
            <div class="small">
              <label>
                <input type="checkbox" bind:checked={remember} />
                Se souvenir de moi
              </label>
            </div>
            <button class="btn" type="submit">Se connecter</button>
          </div>

          <div class="mt-12">
            <span class="small">Pas de compte ?</span>
            <a class="toggle" href="/inscription" on:click|preventDefault={() => navigate('inscription')}>S'inscrire</a>
          </div>
        </form>
      </div>
    </div>
  </div>
</div>