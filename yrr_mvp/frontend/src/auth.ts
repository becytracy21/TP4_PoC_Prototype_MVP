import { writable } from 'svelte/store';

export type AuthUser = {
  id: string;
  name: string;
  email: string;
};

export type AuthState = {
  token: string | null;
  user: AuthUser | null;
};

const STORAGE_KEY = 'yrr_auth';

type PersistMode = 'local' | 'session';

function readStorage(s: Storage): AuthState | null {
  try {
    const raw = s.getItem(STORAGE_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw) as AuthState;
    return {
      token: typeof parsed.token === 'string' ? parsed.token : null,
      user: parsed.user ?? null,
    };
  } catch {
    return null;
  }
}

function initialMode(): PersistMode {
  // si sessionStorage contient une session, on reste en 'session'
  if (readStorage(sessionStorage)?.token) return 'session';
  // sinon si localStorage contient une session, on est en 'local'
  if (readStorage(localStorage)?.token) return 'local';
  // défaut: session (plus sûr)
  return 'session';
}

function load(): AuthState {
  // priorité: sessionStorage (session courante), sinon localStorage (remember)
  return readStorage(sessionStorage) ?? readStorage(localStorage) ?? { token: null, user: null };
}

export const auth = writable<AuthState>(load());

let persist: PersistMode = initialMode();

export function setRemember(remember: boolean) {
  persist = remember ? 'local' : 'session';

  // migre l'état courant vers le storage choisi
  try {
    const current = readStorage(sessionStorage) ?? readStorage(localStorage) ?? null;
    sessionStorage.removeItem(STORAGE_KEY);
    localStorage.removeItem(STORAGE_KEY);
    if (current) {
      (persist === 'local' ? localStorage : sessionStorage).setItem(STORAGE_KEY, JSON.stringify(current));
    }
  } catch {
    // ignore
  }
}

auth.subscribe((v) => {
  try {
    (persist === 'local' ? localStorage : sessionStorage).setItem(STORAGE_KEY, JSON.stringify(v));
  } catch {
    // ignore
  }
});

export function isAuthenticated(state: AuthState): boolean {
  return !!state.token;
}

export function logout() {
  auth.set({ token: null, user: null });
  try {
    sessionStorage.removeItem(STORAGE_KEY);
    localStorage.removeItem(STORAGE_KEY);
  } catch {
    // ignore
  }
}
