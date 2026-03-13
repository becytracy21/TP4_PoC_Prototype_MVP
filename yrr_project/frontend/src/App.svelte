<script lang="ts">
    let elapsed = "";
    let handicap = "";
    let result: number | null = null;
    let message = "";

async function sendData() {
    console.log("Le bouton fonctionne !");

    const response = await fetch("http://localhost:8000/api/calculate/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            elapsed: Number(elapsed),
            handicap: Number(handicap)
        })
    });

    console.log("Réponse brute :", response);
}


</script>

<style>
.container {
    display: flex;
    gap: 20px;
    margin-bottom: 20px;
}
.box {
    border: 2px solid #ccc;
    padding: 20px;
    width: 200px;
    text-align: center;
    font-weight: bold;
}
button {
    padding: 10px 20px;
    font-size: 16px;
}
.result {
    margin-top: 20px;
    font-size: 20px;
    font-weight: bold;
}
</style>

<div class="container">
    <div class="box">
        TEMPS ÉCOULÉ  
        <input type="number" bind:value={elapsed} />
    </div>

    <div class="box">
        HANDICAP  
        <input type="number" bind:value={handicap} />
    </div>
</div>

<button on:click={sendData}>Add</button>

{#if result !== null}
    <div class="result">
        Temps corrigé : {result} secondes  
        <br />
        {message}
    </div>
{/if}
