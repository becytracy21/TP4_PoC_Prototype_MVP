<script lang="ts">
  import { navigate } from './router';

  let name = '';
  let email = '';
  let password = '';
  let password2 = '';

  let loading = false;
  let errorMsg = '';

  const API_BASE = (import.meta as any).env?.VITE_API_BASE_URL ?? 'http://localhost:8000/api';

  export let onSuccess: (() => void) | undefined;

  async function submit() {
    errorMsg = '';

    if (name.trim() === '') {
      errorMsg = 'Le nom complet est requis.';
      return;
    }
    if (email.trim() === '') {
      errorMsg = 'L\'adresse e-mail est requise.';
      return;
    }
    if (password.length < 6) {
      errorMsg = 'Le mot de passe doit contenir au moins 6 caractères.';
      return;
    }
    if (password !== password2) {
      errorMsg = 'Les mots de passe ne correspondent pas.';
      return;
    }

    loading = true;
    try {
      const res = await fetch(`${API_BASE}/users/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: name.trim(),
          email: email.trim(),
          password,
        }),
      });

      if (!res.ok) {
        const data = await res.json().catch(() => null);
        throw new Error(data?.detail ?? `Erreur lors de l\'inscription (HTTP ${res.status}).`);
      }

      name = '';
      email = '';
      password = '';
      password2 = '';

      onSuccess?.();
    } catch (e) {
      errorMsg = e instanceof Error ? e.message : 'Erreur réseau.';
    } finally {
      loading = false;
    }
  }
</script>

<div class="auth-page">
  <div class="container-main">
    <div class="card auth-card">
      <div class="brand">
        <h2>Yacht Racing Results</h2>
        <div class="brand-logo-wrap">
          <img class="brand-logo" src="/favicon.ico" alt="YRR" />
        </div>
      </div>

      <div class="form-wrap">
        <h1 class="mt-0">Inscription</h1>
        <p class="lead">Créez un compte en quelques secondes.</p>

        {#if errorMsg}
          <div class="error" role="alert">{errorMsg}</div>
        {/if}

        <form on:submit|preventDefault={submit}>
          <label for="regName">Nom complet</label>
          <input id="regName" type="text" bind:value={name} required placeholder="Votre nom" autocomplete="name" />

          <label for="regEmail">Email</label>
          <input id="regEmail" type="email" bind:value={email} required placeholder="exemple@domaine.com" autocomplete="email" />

          <div class="row">
            <div class="col">
              <label for="regPassword">Mot de passe</label>
              <input
                id="regPassword"
                type="password"
                bind:value={password}
                required
                minlength={6}
                placeholder="Mot de passe (min 6)"
                autocomplete="new-password"
              />
            </div>
            <div class="col">
              <label for="regPassword2">Confirmer mot de passe</label>
              <input
                id="regPassword2"
                type="password"
                bind:value={password2}
                required
                minlength={6}
                placeholder="Confirmer"
                autocomplete="new-password"
              />
            </div>
          </div>

          <div class="actions">
            <div class="small"></div>
            <button class="btn" type="submit" disabled={loading}>{loading ? 'Création…' : 'Créer le compte'}</button>
          </div>

          <div class="mt-12">
            <span class="small">Déjà inscrit ?</span>
            <a class="toggle" href="/connexion" on:click|preventDefault={() => navigate('connexion')}>Se connecter</a>
          </div>
        </form>
      </div>
    </div>
  </div>
</div>