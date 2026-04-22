<script>
  function go(href) {
    if (!href) return;
    if (href.startsWith('#')) window.location.hash = href;
    else if (href.startsWith('/')) window.location.hash = '#' + href;
    else window.location.href = href;
  }

  function navigate(e) {
    e.preventDefault();
    const a = /** @type {HTMLAnchorElement} */ (e.currentTarget);
    go(a.getAttribute('href') || '');
  }
</script>

<svelte:head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Résultats séries — YRR Prototype</title>
  <link rel="icon" href="/favicon.ico" />
  <link rel="stylesheet" href="/HTML-CSS/css/style.css" />
</svelte:head>

<header>
  <h2>YRR — Prototype</h2>
  <div class="header-center">
    <nav class="main-nav-bar">
      <div class="nav-left">
        <a href="#/bateaux" on:click={navigate}>Accueil</a>
        <a href="#/classes" on:click={navigate}>Classes</a>
        <a href="#/bateaux" on:click={navigate}>Bateaux</a>
        <a href="#/series" class="active" on:click={navigate}>Séries</a>
        <a href="#/course" on:click={navigate}>Course</a>
      </div>
    </nav>
  </div>
  <div class="nav-user">
    <a href="#/profil" class="nav-user-link" on:click={navigate}>
      <div class="avatar" title="Profil">JD</div>
      <div class="username">Jean Dupont</div>
    </a>
  </div>
</header>

<div class="container-main">
  <div class="hero">
    <h2 class="hero-title">Résultats des séries</h2>
    <p class="hero-subtitle">Affichage des résultats cumulés d'une série (prototype, données simulées)</p>
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
            <th>Numéro de voile</th>
            <th>Barreur</th>
            <th class="text-center">Course 1</th>
            <th class="text-center">Course 2</th>
            <th class="text-center">Course 3</th>
            <th class="text-center">Course 4</th>
            <th class="text-center">Course 5</th>
            <th class="text-right">Total</th>
            <th class="text-center">Classement général</th>
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
      <a class="btn" href="#" on:click|preventDefault={() => { /* impression simulée */ }}>Imprimer</a>
      <a class="button-ghost" href="#" on:click|preventDefault={() => { /* précédent */ }}>Précédent</a>
      <a class="button-ghost" href="#" on:click|preventDefault={() => { /* suivant */ }}>Suivant</a>
      <a class="button-ghost" href="#/series" on:click={navigate}>Retour aux séries</a>
    </div>
  </section>
</div>

<footer class="muted mt-18">Prototype non fonctionnel — interface de démonstration.</footer>