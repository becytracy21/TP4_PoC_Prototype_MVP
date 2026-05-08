<script>
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();

  function go(href) {
    if (!href) return;
    if (href.startsWith('/')) {
      window.history.pushState({}, '', href);
      dispatch('navigate', href);
    } else {
      window.location.href = href;
    }
  }

  function navigate(e) {
    e.preventDefault();
    const a = /** @type {HTMLAnchorElement} */ (e.currentTarget);
    go(a.getAttribute('href') || '');
  }

  // ajout : impression du tableau de résultats
  function printResults(e) {
    if (e) e.preventDefault();
    const table = document.querySelector('.table-standard');
    if (!table) {
      alert('Tableau introuvable pour impression.');
      return;
    }

    const w = window.open('', '_blank', 'width=900,height=700');
    if (!w) {
      alert("Impossible d'ouvrir une nouvelle fenêtre pour l'impression.");
      return;
    }

    const doc = w.document;
    doc.write('<!doctype html><html><head><meta charset="utf-8"><title>Impression - Résultats de série</title>');
    doc.write('<link rel="stylesheet" href="/HTML-CSS/css/style.css">');
    doc.write('<style>body{padding:20px;font-family:Arial,Helvetica,sans-serif;}table{width:100%;border-collapse:collapse;}@media print{.no-print{display:none}}</style>');
    doc.write('</head><body>');
    doc.write('<h2>Résultats de série</h2>');
    doc.write(table.outerHTML);
    doc.write('</body></html>');
    doc.close();
    w.focus();

    // attendre un peu que la fenêtre rende le contenu puis imprimer
    setTimeout(() => {
      try {
        w.print();
        w.close();
      } catch (err) {
        console.error('Print error', err);
      }
    }, 300);
  }
</script>

<svelte:head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Résultats séries — YRR</title>
  <link rel="icon" href="/favicon.ico" />
  <link rel="stylesheet" href="/HTML-CSS/css/style.css" />
</svelte:head>

<header>
  <h2>YRR</h2>
  <div class="header-center" style="display: flex; justify-content: center;">
    <nav class="main-nav-bar">
      <div class="nav-left">
        <a href="/Bateaux" on:click={navigate}>Accueil</a>
        <a href="/Classes" on:click={navigate}>Classes</a>
        <a href="/Bateaux" on:click={navigate}>Bateaux</a>
        <a href="/Series" on:click={navigate}>Séries</a>
        <a href="/Course" on:click={navigate}>Course</a>
        <a href="/Inscriptions" on:click={navigate}>Inscriptions</a>
      </div>
    </nav>
  </div>
  <div class="nav-user">
    <a href="/Profil" class="nav-user-link" on:click={navigate}>
      <div class="avatar" title="Profil">JD</div>
      <div class="username">Jean Dupont</div>
    </a>
  </div>
</header>

<div class="container-main">
  <div class="hero">
    <h2 class="hero-title">Résultats des séries</h2>
    <p class="hero-subtitle">Affichage des résultats cumulés d'une série</p>
    <div class="title-underline" aria-hidden="true"></div>
  </div>

  <section class="panel">
    <h3>Résultats de série — Série A (sans déductions)</h3>
    <div class="table-wrapper">
      <table class="table-standard" aria-label="Résultats de série">
        <thead>
          <tr>
            <th>Bateau</th>
            <th>Classe</th>
            <th>Numéro<br/>de voile</th>
            <th>Barreur</th>
            <th class="text-center">Course 1</th>
            <th class="text-center">Course 2</th>
            <th class="text-center">Course 3</th>
            <th class="text-center">Course 4</th>
            <th class="text-center">Course 5</th>
            <th class="text-right">Total</th>
            <th class="text-center">Classement<br/>général</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Whisky</td>
            <td>Laser</td>
            <td>100231</td>
            <td>Fred</td>
            <td class="text-center">4</td>
            <td class="text-center">14</td>
            <td class="text-center">8</td>
            <td class="text-center">2</td>
            <td class="text-center">3</td>
            <td class="text-right">31</td>
            <td class="text-center">2</td>
          </tr>
          <tr>
            <td>Fuzzy Duck</td>
            <td>Laser</td>
            <td>132248</td>
            <td>Graham</td>
            <td class="text-center">3</td>
            <td class="text-center">5</td>
            <td class="text-center">14</td>
            <td class="text-center">1</td>
            <td class="text-center">11</td>
            <td class="text-right">34</td>
            <td class="text-center">3</td>
          </tr>
          <tr>
            <td>Shy Talk</td>
            <td>Solo</td>
            <td>4321</td>
            <td>Jim</td>
            <td class="text-center">14</td>
            <td class="text-center">2</td>
            <td class="text-center">14</td>
            <td class="text-center">5</td>
            <td class="text-center">4</td>
            <td class="text-right">39</td>
            <td class="text-center">4</td>
          </tr>
          <tr>
            <td>Matilda</td>
            <td>Solo</td>
            <td>3755</td>
            <td>John</td>
            <td class="text-center">14</td>
            <td class="text-center">10</td>
            <td class="text-center">8</td>
            <td class="text-center">9</td>
            <td class="text-center">6</td>
            <td class="text-right">47</td>
            <td class="text-center">5</td>
          </tr>
          <tr>
            <td>Blue Finch</td>
            <td>Laser</td>
            <td>99012</td>
            <td>Marie</td>
            <td class="text-center">6</td>
            <td class="text-center">8</td>
            <td class="text-center">5</td>
            <td class="text-center">12</td>
            <td class="text-center">7</td>
            <td class="text-right">38</td>
            <td class="text-center">6</td>
          </tr>
          <tr>
            <td>Seafoam</td>
            <td>Solo</td>
            <td>5010</td>
            <td>Paul</td>
            <td class="text-center">8</td>
            <td class="text-center">7</td>
            <td class="text-center">9</td>
            <td class="text-center">6</td>
            <td class="text-center">12</td>
            <td class="text-right">42</td>
            <td class="text-center">7</td>
          </tr>
          <tr>
            <td>Storm Petrel</td>
            <td>Laser</td>
            <td>77701</td>
            <td>Hugo</td>
            <td class="text-center">11</td>
            <td class="text-center">6</td>
            <td class="text-center">6</td>
            <td class="text-center">13</td>
            <td class="text-center">10</td>
            <td class="text-right">46</td>
            <td class="text-center">8</td>
          </tr>
          <tr>
            <td>Red Kite</td>
            <td>Solo</td>
            <td>6022</td>
            <td>Sophie</td>
            <td class="text-center">10</td>
            <td class="text-center">12</td>
            <td class="text-center">7</td>
            <td class="text-center">8</td>
            <td class="text-center">9</td>
            <td class="text-right">46</td>
            <td class="text-center">9</td>
          </tr>
          <tr>
            <td>Night Heron</td>
            <td>Laser</td>
            <td>42011</td>
            <td>Lucas</td>
            <td class="text-center">12</td>
            <td class="text-center">11</td>
            <td class="text-center">10</td>
            <td class="text-center">7</td>
            <td class="text-center">8</td>
            <td class="text-right">48</td>
            <td class="text-center">10</td>
          </tr>
          <tr>
            <td>Silver Gull</td>
            <td>Solo</td>
            <td>7099</td>
            <td>Nina</td>
            <td class="text-center">9</td>
            <td class="text-center">13</td>
            <td class="text-center">11</td>
            <td class="text-center">10</td>
            <td class="text-center">5</td>
            <td class="text-right">48</td>
            <td class="text-center">11</td>
          </tr>
          <tr>
            <td>Courlis</td>
            <td>Laser</td>
            <td>88120</td>
            <td>Éric</td>
            <td class="text-center">13</td>
            <td class="text-center">9</td>
            <td class="text-center">12</td>
            <td class="text-center">11</td>
            <td class="text-center">14</td>
            <td class="text-right">59</td>
            <td class="text-center">12</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="actions-row mt-2">
      <a class="btn btn-outline" href="#" on:click|preventDefault={() => { /* simulation */ }}>Déductions (simulé)</a>
      <span class="muted">Déductions : aucune (simulation)</span>
      <span class="flex-1"></span>
      <a class="btn" href="#" on:click|preventDefault={printResults}>Imprimer</a>
      <a class="button-ghost" href="#" on:click|preventDefault={() => { /* précédent */ }}>Précédent</a>
      <a class="button-ghost" href="#" on:click|preventDefault={() => { /* suivant */ }}>Suivant</a>
      <a class="button-ghost" href="/Series" on:click={navigate}>Retour aux séries</a>
    </div>
  </section>
</div>