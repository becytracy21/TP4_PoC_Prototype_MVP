<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import { onMount, onDestroy } from 'svelte';
    import { auth, logout as authLogout } from "../auth";

    export let active: "bateaux" | "classes" | "series" | "course" | "inscriptions" | "resultats-series" = "bateaux";

    const dispatch = createEventDispatcher<{ navigate: string }>();
    let showDropdown = false;

    const toggleDropdown = (e: MouseEvent) => { e.stopPropagation(); showDropdown = !showDropdown; };
    // Écoute globale pour fermer le dropdown si on clique en dehors — n'écrase pas d'autres handlers
    let _globalClickHandler: ((e: Event) => void) | null = null;
    onMount(() => {
        _globalClickHandler = () => { showDropdown = false; };
        window.addEventListener('click', _globalClickHandler);
    });
    onDestroy(() => {
        if (_globalClickHandler) window.removeEventListener('click', _globalClickHandler);
    });

    function navigate(e: MouseEvent) {
        e.preventDefault();
        const a = e.currentTarget as HTMLAnchorElement;
        const href = a.getAttribute("href") || "";
        dispatch("navigate", href);
    }

    function initialsFromName(name?: string | null): string {
        if (!name) return "??";
        const parts = name.trim().split(/\s+/).filter(Boolean);
        if (parts.length === 0) return "??";
        if (parts.length === 1) return parts[0].slice(0, 1).toUpperCase();
        return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
    }

    function logout() {
        // utilise la fonction de logout du store pour nettoyer correctement l'état
        authLogout();
        // redirige vers la racine (le composant parent gèrera la redirection vers /connexion)
        window.location.href = "/";
    }

    // Récupère l'utilisateur depuis le store `auth` de façon réactive
    $: user = $auth?.user;
</script>

<header style="display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; width: 100%; padding: 0 1.5rem;">
    <div style="justify-self: start;"><h2 style="margin: 0; white-space: nowrap;">Yacht Racing Results</h2></div>
    
    <div class="header-center" style="justify-self: center;">
        <nav class="main-nav-bar">
            <div class="nav-left" style="display: flex; gap: 0.5rem;">
                <a href="/Bateaux" class="button-ghost {active === 'bateaux' ? 'active' : ''}" on:click={navigate}>Bateaux</a>
                <a href="/Classes" class="button-ghost {active === 'classes' ? 'active' : ''}" on:click={navigate}>Classes</a>
                <a href="/Series" class="button-ghost {active === 'series' ? 'active' : ''}" on:click={navigate}>Séries</a>
                <a href="/ResultatsSeries" class="button-ghost {active === 'resultats-series' ? 'active' : ''}" on:click={navigate}>Résultats</a>
                <a href="/Course" class="button-ghost {active === 'course' ? 'active' : ''}" on:click={navigate}>Course</a>
                <a href="/Inscriptions" class="button-ghost {active === 'inscriptions' ? 'active' : ''}" on:click={navigate}>Inscriptions</a>
            </div>
        </nav>
    </div>

    <div class="nav-user" class:open={showDropdown} style="justify-self: end; position: relative;">
        <button type="button" class="nav-user-btn" on:click={toggleDropdown} aria-haspopup="menu" aria-expanded={showDropdown} style="display: flex; align-items: center; gap: 0.75rem; padding: 0.5rem; background: none; border: none; cursor: pointer; color: inherit; font: inherit;">
            <div class="avatar" title="Profil">{initialsFromName(user?.name)}</div>
            <div class="username">{user?.name ?? user?.email ?? "Invité"}</div>
        </button>
        <div class="dropdown-content" role="menu" aria-hidden={!showDropdown} style="position: absolute; top: calc(100% + 8px); right: 0; background-color: white; min-width: 180px; box-shadow: 0px 4px 12px rgba(0,0,0,0.1); border: 1px solid #e5e7eb; border-radius: var(--radius); z-index: 1000; flex-direction: column; padding: 0.5rem;">
            <button class="btn-delete" on:click={logout} role="menuitem" style="width: 100%;">Déconnexion</button>
        </div>
    </div>
</header>

<slot />

<footer class="muted mt-18">© 2026 Yacht Racing Results (YRR) - Radmehr Rahmani (2356157)</footer>

<style>
    .nav-user .dropdown-content { display: none; }
    .nav-user.open .dropdown-content { display: flex !important; }
</style>