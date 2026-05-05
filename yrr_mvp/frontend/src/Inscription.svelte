<script lang="ts">
  import { navigate } from './router';

  let name = '';
  let email = '';
  let password = '';
  let password2 = '';

  let loading = false;
  let errorMsg = '';

  let showPassword = false;
  let revealLocked = false;
  let passwordInput: HTMLInputElement | null = null;
  let pendingSelection: { start: number; end: number } | null = null;

  let showPassword2 = false;
  let revealLocked2 = false;
  let passwordInput2: HTMLInputElement | null = null;
  let pendingSelection2: { start: number; end: number } | null = null;

  const API_BASE = (import.meta as any).env?.VITE_API_BASE_URL ?? 'http://localhost:8000/api';

  export let onSuccess: (() => void) | undefined;

  function setReveal(next: boolean) {
    showPassword = revealLocked ? true : next;
  }

  function setReveal2(next: boolean) {
    showPassword2 = revealLocked2 ? true : next;
  }

  function captureCaret(input: HTMLInputElement | null, value: string, slot: 1 | 2) {
    if (!input) return;
    const start = input.selectionStart;
    const end = input.selectionEnd;
    const pos = value.length;
    const selection = { start: start ?? pos, end: end ?? pos };
    if (slot === 1) pendingSelection = selection;
    else pendingSelection2 = selection;
  }

  async function restoreCaret(input: HTMLInputElement | null, slot: 1 | 2) {
    const pending = slot === 1 ? pendingSelection : pendingSelection2;
    if (!pending) return;

    const { tick } = await import('svelte');
    await tick();

    requestAnimationFrame(() => {
      if (!input) return;
      input.focus({ preventScroll: true });
      input.setSelectionRange(pending.start, pending.end);
      if (slot === 1) pendingSelection = null;
      else pendingSelection2 = null;
    });
  }

  function toggleRevealLock() {
    captureCaret(passwordInput, password, 1);
    revealLocked = !revealLocked;
    showPassword = revealLocked;
    void restoreCaret(passwordInput, 1);
  }

  function toggleRevealLock2() {
    captureCaret(passwordInput2, password2, 2);
    revealLocked2 = !revealLocked2;
    showPassword2 = revealLocked2;
    void restoreCaret(passwordInput2, 2);
  }

  function onPointerDown(e: PointerEvent) {
    if (e.pointerType === 'mouse') setReveal(true);
  }

  function onPointerDown2(e: PointerEvent) {
    if (e.pointerType === 'mouse') setReveal2(true);
  }

  async function submit() {
    errorMsg = '';

    if (name.trim() === '') {
      errorMsg = 'Le nom complet est requis.';
      return;
    }
    if (email.trim() === '') {
      errorMsg = "L'adresse e-mail est requise.";
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
        throw new Error(data?.detail ?? `Erreur lors de l'inscription (HTTP ${res.status}).`);
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
              <div class="password-field">
                <input
                  id="regPassword"
                  bind:this={passwordInput}
                  type={showPassword ? 'text' : 'password'}
                  bind:value={password}
                  required
                  minlength={6}
                  placeholder="Mot de passe (min 6)"
                  autocomplete="new-password"
                  on:blur={() => setReveal(false)}
                />
                <button
                  class="password-reveal"
                  type="button"
                  aria-label={showPassword ? 'Masquer le mot de passe' : 'Afficher le mot de passe'}
                  aria-pressed={revealLocked}
                  on:click|preventDefault={toggleRevealLock}
                  on:mouseenter={() => setReveal(true)}
                  on:mouseleave={() => setReveal(false)}
                  on:pointerdown|preventDefault={onPointerDown}
                  on:pointerup={() => setReveal(false)}
                >
                  {#if showPassword}
                    <svg class="eye-icon" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                      <path
                        d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                      />
                      <path
                        d="M9.5 9.5a3.5 3.5 0 1 0 5 5"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                      />
                      <path
                        d="M14.5 14.5a3.5 3.5 0 0 0-5-5"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                      />
                    </svg>
                  {:else}
                    <svg class="eye-icon" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                      <path
                        d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                      />
                      <path
                        d="M12 15.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7Z"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                      />
                      <path d="M4 4l16 16" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
                    </svg>
                  {/if}
                </button>
              </div>
            </div>
            <div class="col">
              <label for="regPassword2">Confirmer mot de passe</label>
              <div class="password-field">
                <input
                  id="regPassword2"
                  bind:this={passwordInput2}
                  type={showPassword2 ? 'text' : 'password'}
                  bind:value={password2}
                  required
                  minlength={6}
                  placeholder="Confirmer"
                  autocomplete="new-password"
                  on:blur={() => setReveal2(false)}
                />
                <button
                  class="password-reveal"
                  type="button"
                  aria-label={showPassword2 ? 'Masquer le mot de passe' : 'Afficher le mot de passe'}
                  aria-pressed={revealLocked2}
                  on:click|preventDefault={toggleRevealLock2}
                  on:mouseenter={() => setReveal2(true)}
                  on:mouseleave={() => setReveal2(false)}
                  on:pointerdown|preventDefault={onPointerDown2}
                  on:pointerup={() => setReveal2(false)}
                >
                  {#if showPassword2}
                    <svg class="eye-icon" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                      <path
                        d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                      />
                      <path
                        d="M9.5 9.5a3.5 3.5 0 1 0 5 5"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                      />
                      <path
                        d="M14.5 14.5a3.5 3.5 0 0 0-5-5"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                      />
                    </svg>
                  {:else}
                    <svg class="eye-icon" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                      <path
                        d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                      />
                      <path
                        d="M12 15.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7Z"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                      />
                      <path d="M4 4l16 16" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
                    </svg>
                  {/if}
                </button>
              </div>
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