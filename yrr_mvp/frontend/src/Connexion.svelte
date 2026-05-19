<script lang="ts">
  import { navigate } from './router';
  import { tick } from 'svelte';
  import { auth, setRemember } from './auth';

  let email = '';
  let password = '';
  let remember = false;
  let errorMsg = '';
  let loading = false;

  const API_BASE = (import.meta as any).env?.VITE_API_BASE_URL ?? 'http://localhost:8000/api';

  let showPassword = false;
  let revealLocked = false;

  let passwordInput: HTMLInputElement | null = null;

  async function submit() {
    errorMsg = '';

    if (email.trim() === '') {
      errorMsg = "L'adresse e-mail est requise.";
      return;
    }

    if (password.trim() === '') {
      errorMsg = 'Le mot de passe est requis.';
      return;
    }

    loading = true;
    try {
      const res = await fetch(`${API_BASE}/users/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: email.trim(),
          password,
        }),
      });

      if (!res.ok) {
        const data = await res.json().catch(() => null);
        throw new Error(data?.detail ?? `Erreur de connexion (HTTP ${res.status}).`);
      }

      const data = (await res.json()) as { token?: string; user?: { id: string; name: string; email: string } };
      if (!data?.token || !data?.user) {
        throw new Error('Réponse serveur invalide.');
      }

      setRemember(remember);
      auth.set({ token: data.token, user: data.user });

      navigate('bateaux');
    } catch (e) {
      errorMsg = e instanceof Error ? e.message : 'Erreur réseau.';
    } finally {
      loading = false;
    }
  }

  function setReveal(next: boolean) {
    showPassword = revealLocked ? true : next;
  }

  async function withCaret(fn: () => void) {
    if (!passwordInput) {
      fn();
      return;
    }

    const start = passwordInput.selectionStart ?? password.length;
    const end = passwordInput.selectionEnd ?? password.length;

    fn();

    await tick();
    requestAnimationFrame(() => {
      if (!passwordInput) return;
      passwordInput.focus({ preventScroll: true });
      passwordInput.setSelectionRange(start, end);
    });
  }

  function toggleRevealLock() {
    void withCaret(() => {
      revealLocked = !revealLocked;
      showPassword = revealLocked;
    });
  }

  function onPointerDown(e: PointerEvent) {
    if (e.pointerType === 'mouse') setReveal(true);
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
          <div class="password-field">
            <input
              id="loginPassword"
              bind:this={passwordInput}
              type={showPassword ? 'text' : 'password'}
              bind:value={password}
              required
              placeholder="Votre mot de passe"
              autocomplete="current-password"
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

          <div class="actions">
            <div class="small">
              <label>
                <input type="checkbox" bind:checked={remember} />
                Se souvenir de moi
              </label>
            </div>
            <button class="btn" type="submit" disabled={loading} aria-busy={loading}>
              {#if loading}
                Connexion…
              {:else}
                Se connecter
              {/if}
            </button>
          </div>

          <br />
          <br />
          <br />

          <div class="mt-12">
            <span class="small">Pas de compte ?</span>
            <a class="toggle" href="/inscription" on:click|preventDefault={() => navigate('inscription')}>S'inscrire</a>
          </div>
        </form>
      </div>
    </div>
  </div>
</div>