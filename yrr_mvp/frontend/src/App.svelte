<script lang="ts">
    import { onMount } from 'svelte';

    let elapsed: number | string = "";
    let handicap: number | string = "";
    let result: number | null = null;
    let message = "";

    type Calc = {
        elapsed: number;
        handicap: number;
        corrected: number;
        message?: string;
        time: string;
    };

    let history: Calc[] = [];

    onMount(() => {
        const raw = localStorage.getItem('calcul_history_v1');
        if (raw) {
            try {
                history = JSON.parse(raw) as Calc[];
            } catch (e) {
                console.error('Impossible de parser l\'historique', e);
                history = [];
            }
        }
    });

    function saveHistory() {
        try {
            localStorage.setItem('calcul_history_v1', JSON.stringify(history));
        } catch (e) {
            console.error('Impossible de sauvegarder l\'historique', e);
        }
    }

    async function sendData() {
        console.log("Le bouton fonctionne !");
        result = null;
        message = "";

        try {
            const response = await fetch("http://localhost:8000/api/calculate/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    elapsed: Number(elapsed),
                    handicap: Number(handicap)
                })
            });

            console.log("Réponse brute :", response);

            const data = await response.json().catch(() => null);

            if (response.ok && data) {
                // Supporte plusieurs formats possibles renvoyés par l'API
                const corrected = data.corrected ?? data.result ?? data.corrected_time ?? data.correctedTime ?? null;
                if (corrected !== null) {
                    result = Number(corrected);
                } else if (typeof data === 'number') {
                    result = data;
                }
                message = data.message ?? data.detail ?? "";

                // ajouter à l'historique si on a un résultat
                if (result !== null) {
                    const entry: Calc = {
                        elapsed: Number(elapsed),
                        handicap: Number(handicap),
                        corrected: Number(result),
                        message,
                        time: new Date().toLocaleString()
                    };
                    history = [entry, ...history];
                    saveHistory();
                }
            } else if (data) {
                message = data.message ?? data.detail ?? `Erreur: ${response.status}`;
            } else {
                message = `Erreur: ${response.status}`;
            }
        } catch (err) {
            console.error(err);
            message = 'Erreur réseau ou inattendue';
        }
    }

    function clearHistory() {
        history = [];
        saveHistory();
    }

</script>

<style>
:global(html, body, #app) {
    height: 100%;
    overflow: hidden; /* Empêche le scroll de la page entière */
}

:global(#app) {
    display: flex;
    align-items: center;
    justify-content: center;
}

:global(body) {
    margin: 0;
    font-family: Inter, system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    /* fond en gradient plus marqué */
    background: linear-gradient(135deg, #f0fbff 0%, #e6f0ff 40%, #eef7f9 100%);
    color: #0b2440;
    min-height: 100vh;
}

/* Base plus grande pour les écrans */
:global(body) { font-size: 18px; }

.app {
    position: relative; /* nécessaire pour les éléments décoratifs */
    width: 100%;
    max-width: 960px;
    padding: 36px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

/* Titre principal */
.hero-title {
    font-size: 2.6rem;
    line-height: 1.05;
    margin: 0 0 8px 0;
    font-weight: 800;
    color: #07223a;
    text-align: center;
    letter-spacing: -0.02em;
}

.hero-subtitle {
    font-size: 1.05rem;
    color: #23445a;
    margin: 0 0 20px 0;
    text-align: center;
    opacity: 0.95;
}

/* Barre décorative sous le titre */
.title-underline {
    height: 8px;
    width: 120px;
    border-radius: 999px;
    background: linear-gradient(90deg, #06b6d4, #3b82f6);
    margin: 12px auto 20px auto;
    box-shadow: 0 8px 20px rgba(59,130,246,0.12);
}

/* Éléments artistiques flous */
.decor {
    position: absolute;
    width: 260px;
    height: 260px;
    border-radius: 50%;
    filter: blur(40px);
    opacity: 0.22;
    pointer-events: none;
    transform: translate3d(0,0,0);
    animation: float 6s ease-in-out infinite;
}
.decor-left {
    left: -80px;
    top: -80px;
    background: radial-gradient(circle at 30% 30%, #a7f3d0, transparent 40%);
}
.decor-right {
    right: -100px;
    bottom: -80px;
    background: radial-gradient(circle at 70% 70%, #bfdbfe, transparent 40%);
    animation-duration: 8s;
}

@keyframes float {
    0% { transform: translateY(0) translateX(0) ; }
    50% { transform: translateY(-10px) translateX(6px); }
    100% { transform: translateY(0) translateX(0); }
}

/* Ajustements titre sur petits écrans */
@media (max-width: 720px) {
    .hero-title { font-size: 1.6rem; }
    .hero-subtitle { font-size: 0.95rem; }
}

.container {
    display: flex;
    gap: 28px;
    margin-bottom: 24px;
    justify-content: center;
}

.box {
    background: #ffffff;
    border: 1px solid rgba(11,36,64,0.06);
    padding: 28px;
    width: 340px;
    text-align: center;
    font-weight: 700;
    border-radius: 14px;
    box-shadow: 0 12px 36px rgba(11,36,64,0.06);
    color: inherit;
    font-size: 1.15rem;
}

input[type="number"] {
    margin-top: 10px;
    width: 100%;
    padding: 14px;
    border-radius: 10px;
    border: 1px solid #e6eef8;
    background: #f6fafc;
    color: #0b2440;
    outline: none;
    box-sizing: border-box;
    font-size: 1rem;
}

button {
    padding: 16px 34px;
    font-size: 1.05rem;
    border-radius: 14px;
    border: none;
    cursor: pointer;
    background: linear-gradient(90deg, #06b6d4 0%, #3b82f6 100%);
    color: white;
    box-shadow: 0 14px 36px rgba(59,130,246,0.12);
    transition: transform 0.12s ease, box-shadow 0.12s ease;
}

button:hover { transform: translateY(-2px); box-shadow: 0 18px 48px rgba(59,130,246,0.18); }

.result {
    margin-top: 22px;
    font-size: 1.18rem;
    font-weight: 700;
    background: #ffffff;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid rgba(11,36,64,0.04);
    box-shadow: 0 10px 28px rgba(11,36,64,0.04);
    color: inherit;
}

/* Nouveau: liste d'historique et cards individuelles */
.history-list {
    margin-top: 32px;
    width: 100%;
    --history-card-h: 104px;
    --history-gap: 10px;
}
.history-scroll {
    max-height: calc(var(--history-card-h) * 2 + var(--history-gap));
    overflow-y: auto;
    margin-top: 16px;
    border-top: 1px solid rgba(11,36,64,0.1);
    padding-top: 16px;
    display: flex;
    flex-direction: column;
    gap: var(--history-gap);
}
.history-card {
    background: #ffffff;
    height: var(--history-card-h);
    padding: 8px 12px;
    border-radius: 10px;
    border: 1px solid rgba(11,36,64,0.03);
    box-shadow: 0 5px 14px rgba(11,36,64,0.02);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 8px;
    box-sizing: border-box;
}
.history-card .left {
    max-width: 100%;
    width: 100%;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden; /* empêche débordement */
}
.history-result {
    background: #fbfdff;
    padding: 6px 10px;
    border-radius: 8px;
    border: 1px solid rgba(11,36,64,0.02);
    box-shadow: none;
    font-size: 1rem; /* un peu plus grand */
    line-height: 1.05; /* compacte les lignes */
    font-weight: 700;
    color: inherit;
    width: 100%;
    box-sizing: border-box;
    white-space: normal; /* autorise le retour à la ligne */
    word-break: break-word; /* coupe si nécessaire */
    overflow: hidden; /* coupe l'excès */
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 3; /* autorise jusqu'à 3 lignes visibles */
    -webkit-box-orient: vertical;
}
.history-result .sub {
    margin-top: 4px;
    font-weight: 600;
    font-size: 0.9rem;
    line-height: 1;
}
.history-result .msg {
    margin-top: 4px;
    color: rgba(11,36,64,0.7);
    font-size: 0.85rem;
    font-weight: 500;
    line-height: 1;
}
.history-card .meta {
    opacity: 0.75;
    font-style: italic;
    font-size: 0.82rem; /* légèrement plus lisible */
    margin-top: 4px;
}

@media (max-width: 720px) {
    .history-list { --history-card-h: 90px; }
    .history-card { height: var(--history-card-h); }
    .history-result { -webkit-line-clamp: 3; }
}

/* Ajustements responsives pour petits écrans */
@media (max-width: 720px) {
    :global(body) { font-size: 16px; }
    .container { flex-direction: column; gap: 16px; }
    .box { width: 100%; padding: 18px; }
    button { width: 100%; justify-content: center; }
}

</style>

<div class="app">
    <!-- éléments décoratifs -->
    <div class="decor decor-left" aria-hidden="true"></div>
    <div class="decor decor-right" aria-hidden="true"></div>

    <!-- Titre principal et description -->
    <header style="text-align:center; width:100%;">
        <h1 class="hero-title">Calculateur de temps corrigé</h1>
        <p class="hero-subtitle">Entrez le temps écoulé et le handicap — l'application calcule automatiquement le temps corrigé.</p>
        <div class="title-underline" aria-hidden="true"></div>
    </header>

    <div class="container">
        <div class="box">
            TEMPS ÉCOULÉ
            <input type="number" bind:value={elapsed} aria-label="Temps écoulé" />
        </div>

        <div class="box">
            HANDICAP
            <input type="number" bind:value={handicap} aria-label="Handicap" />
        </div>
    </div>

    <div style="display:flex; gap:12px; align-items:center;">
        <button on:click={sendData}>Ajouter</button>
    </div>

    {#if result !== null}
        <div class="result">
            Temps corrigé : {result} secondes
            <br />
            {message}
        </div>
    {/if}

    <!-- Historique des calculs (cards) -->
    <div class="history-list">
        <h2 style="font-size: 1.8rem; text-align: center; margin:0;">Historique des calculs</h2>
        <div class="history-scroll">
            {#each history as entry, i (entry.time)}
                <div class="history-card">
                    <div class="left">
                        <!-- Titre supprimé : pas de "Calcul X" affiché -->

                        <!-- Card compacte pour l'historique -->
                        <div class="history-result">
                            {entry.corrected} s
                            <div class="sub">{entry.elapsed} s + {entry.handicap} s</div>
                            {#if entry.message}
                                <div class="msg">{entry.message}</div>
                            {/if}
                        </div>
                    </div>

                    <div class="meta">{entry.time}</div>
                </div>
            {/each}
        </div>

        <div style="text-align: center; margin-top: 12px;">
            <button on:click={clearHistory} style="font-size: 0.9rem; padding: 10px 20px; background: rgba(11,36,64,0.05); color: #0b2440; border: none; border-radius: 10px; cursor: pointer;">
                Effacer l'historique
            </button>
        </div>
    </div>
</div>
