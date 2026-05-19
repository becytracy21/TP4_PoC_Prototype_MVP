import { writable } from 'svelte/store';

export type Route = 'connexion' | 'inscription' | 'bateaux';

function parseRouteFromLocation(): Route {
    const path = (window.location.pathname || '/').toLowerCase();
    if (path.endsWith('/bateaux')) return 'bateaux';
    if (path.endsWith('/inscription')) return 'inscription';
    if (path.endsWith('/connexion')) return 'connexion';
    return 'connexion';
}

export const route = writable<Route>(parseRouteFromLocation());

export function navigate(to: Route) {
    const url = to === 'bateaux' ? '/bateaux' : to === 'inscription' ? '/inscription' : '/connexion';
    if (window.location.pathname !== url) {
        window.history.pushState({}, '', url);
    }
    route.set(to);
}

window.addEventListener('popstate', () => {
    route.set(parseRouteFromLocation());
});