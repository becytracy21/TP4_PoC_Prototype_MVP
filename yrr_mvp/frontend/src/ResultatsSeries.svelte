<script lang="ts">
  import { createEventDispatcher } from 'svelte';

  export let onBack: () => void = () => {};

  const dispatch = createEventDispatcher<{ navigate: string }>();

  let results: ResultsClass[] = [];

  function navigate(e: MouseEvent) {
    e.preventDefault();
    const a = e.currentTarget as HTMLAnchorElement;
    const href = a.getAttribute('href') || '';
    window.history.pushState({}, '', href);
    dispatch('navigate', href);
  }

  function printResults(e: MouseEvent) {
    e.preventDefault();

    const table = document.querySelector(".table-standard")?.outerHTML;
    if (!table) {
      showNotification("Impossible de trouver le tableau");
      return;
    }

    const printWindow = window.open("", "_blank");
    if (!printWindow) {
      showNotification("Erreur lors de l'ouverture de la fenêtre d'impression");
      return;
    }

    printWindow.document.write(`
      <html>
        <head>
          <title>Impression des résultats</title>
          <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
            table { width: 100%; border-collapse: collapse; }
            th, td { border: 1px solid #ddd; padding: 8px; }
            th { background-color: #f2f2f2; }
            h2 { text-align: center; }
          </style>
        </head>
        <body>
          <h2>Résultats de la course</h2>
          ${table}
        </body>
      </html>
    `);

    printWindow.document.close();
    printWindow.focus();
    printWindow.print();
    printWindow.close();
  }
</script>

<div class="container-main">
  <div class="hero">
    <h2 class="hero-title">Résultats des séries</h2>
    <p class="hero-subtitle">Affichage des résultats cumulés d'une série</p>
    <div class="title-underline" aria-hidden="true"></div>
  </div>

  <section class="panel">
    <h3>Résultats de série — Série A</h3>
    <div class="table-wrapper">
      <table class="table-standard" aria-label="Résultats de série">
        <thead>
          <tr>
            <th>Bateau</th>
            <th>Classe</th>
            <th>Numéro<br />de voile</th>
            <th>Barreur</th>
            <th style="width: 80px;">Course 1</th>
            <th style="width: 80px;">Course 2</th>
            <th style="width: 80px;">Course 3</th>
            <th style="width: 80px;">Course 4</th>
            <th style="width: 120px;">Course 5</th>
            <th style="width: 70px;">Total</th>
            <th>Classement</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Whisky</td>
            <td>Laser</td>
            <td>100231</td>
            <td>Fred</td>
            <td>4</td>
            <td>14</td>
            <td>8</td>
            <td>2</td>
            <td>3</td>
            <td>31</td>
            <td>2</td>
          </tr>
          <tr>
            <td>Fuzzy Duck</td>
            <td>Laser</td>
            <td>132248</td>
            <td>Graham</td>
            <td>3</td>
            <td>5</td>
            <td>14</td>
            <td>1</td>
            <td>11</td>
            <td>34</td>
            <td>3</td>
          </tr>
          <tr>
            <td>Shy Talk</td>
            <td>Solo</td>
            <td>4321</td>
            <td>Jim</td>
            <td>14</td>
            <td>2</td>
            <td>14</td>
            <td>5</td>
            <td>4</td>
            <td>39</td>
            <td>4</td>
          </tr>
          <tr>
            <td>Matilda</td>
            <td>Solo</td>
            <td>3755</td>
            <td>John</td>
            <td>14</td>
            <td>10</td>
            <td>8</td>
            <td>9</td>
            <td>6</td>
            <td>47</td>
            <td>5</td>
          </tr>
          <tr>
            <td>Blue Finch</td>
            <td>Laser</td>
            <td>99012</td>
            <td>Marie</td>
            <td>6</td>
            <td>8</td>
            <td>5</td>
            <td>12</td>
            <td>7</td>
            <td>38</td>
            <td>6</td>
          </tr>
          <tr>
            <td>Seafoam</td>
            <td>Solo</td>
            <td>5010</td>
            <td>Paul</td>
            <td>8</td>
            <td>7</td>
            <td>9</td>
            <td>6</td>
            <td>12</td>
            <td>42</td>
            <td>7</td>
          </tr>
          <tr>
            <td>Storm Petrel</td>
            <td>Laser</td>
            <td>77701</td>
            <td>Hugo</td>
            <td>11</td>
            <td>6</td>
            <td>6</td>
            <td>13</td>
            <td>10</td>
            <td>46</td>
            <td>8</td>
          </tr>
          <tr>
            <td>Red Kite</td>
            <td>Solo</td>
            <td>6022</td>
            <td>Sophie</td>
            <td>10</td>
            <td>12</td>
            <td>7</td>
            <td>8</td>
            <td>9</td>
            <td>46</td>
            <td>9</td>
          </tr>
          <tr>
            <td>Night Heron</td>
            <td>Laser</td>
            <td>42011</td>
            <td>Lucas</td>
            <td>12</td>
            <td>11</td>
            <td>10</td>
            <td>7</td>
            <td>8</td>
            <td>48</td>
            <td>10</td>
          </tr>
          <tr>
            <td>Silver Gull</td>
            <td>Solo</td>
            <td>7099</td>
            <td>Nina</td>
            <td>9</td>
            <td>13</td>
            <td>11</td>
            <td>10</td>
            <td>5</td>
            <td>48</td>
            <td>11</td>
          </tr>
          <tr>
            <td>Courlis</td>
            <td>Laser</td>
            <td>88120</td>
            <td>Éric</td>
            <td>13</td>
            <td>9</td>
            <td>12</td>
            <td>11</td>
            <td>14</td>
            <td>59</td>
            <td>12</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="actions-row mt-2">      
      <span class="flex-1"></span>
      <button class="btn" type="button" on:click={printResults}>Imprimer</button>
      <button class="button-ghost" type="button" on:click={() => {}}>Précédent</button>
      <button class="button-ghost" type="button" on:click={() => {}}>Suivant</button>
      <button class="button-ghost" type="button" on:click={onBack}>Retour</button>
    </div>
  </section>
</div>