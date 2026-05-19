<script lang="ts">
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher<{ navigate: string }>();

  function navigate(e: MouseEvent) {
    e.preventDefault();
    const a = e.currentTarget as HTMLAnchorElement;
    const href = a.getAttribute('href') || '';
    window.history.pushState({}, '', href);
    dispatch('navigate', href);
  }

  function printResults(e: MouseEvent) {
    e.preventDefault();
    window.print();
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
      <a class="button-ghost" href="/Series" on:click={navigate}>Retour aux séries</a>
    </div>
  </section>
</div>