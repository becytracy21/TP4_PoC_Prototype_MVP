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

function load(): AuthState {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return { token: null, user: null };
    const parsed = JSON.parse(raw) as AuthState;
    return {
      token: typeof parsed.token === 'string' ? parsed.token : null,
      user: parsed.user ?? null,
    };
  } catch {
    return { token: null, user: null };
  }
}

export const auth = writable<AuthState>(load());

auth.subscribe((v) => {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(v));
  } catch {
    // ignore
  }
});

export function isAuthenticated(state: AuthState): boolean {
  return !!state.token;
}

export function logout() {
  auth.set({ token: null, user: null });
}
