// Menu profil: ouverture/fermeture et action déconnexion
(function(){
  const toggle = document.getElementById('profileToggle');
  const dropdown = document.getElementById('profileDropdown');
  if(!toggle || !dropdown) return;

  function openDropdown(){ dropdown.hidden = false; toggle.setAttribute('aria-expanded','true'); }
  function closeDropdown(){ dropdown.hidden = true; toggle.setAttribute('aria-expanded','false'); }

  toggle.addEventListener('click', function(e){ e.stopPropagation(); if(dropdown.hidden) openDropdown(); else closeDropdown(); });

  const logoutMenuBtn = document.getElementById('logoutMenuBtn');
  if(logoutMenuBtn){
    logoutMenuBtn.addEventListener('click', function(){
      if(!confirm('Voulez-vous vraiment vous déconnecter ?')) return;
      try{ localStorage.removeItem('yrr_session_v1'); localStorage.removeItem('yrr_profile_v1'); }catch(e){}
      window.location.href = 'Connexion.html';
    });
  }

  document.addEventListener('click', function(e){ if(!dropdown.hidden && !toggle.contains(e.target) && !dropdown.contains(e.target)) closeDropdown(); });
  document.addEventListener('keydown', function(e){ if(e.key === 'Escape') closeDropdown(); });
})();

// Simplified logic to switch between 'hors série' and 'selected series'
(function(){
  const selector = document.getElementById('seriesSelector');
  const table = document.getElementById('raceTable');

  // example series definition (would come from Series page in real app)
  const seriesDefinitions = {
    seriesA: {od:'Monotype', class:'Laser', races: [ {date:'2026-04-12'},{date:'2026-04-13'},{date:''} ]},
    seriesB: {od:'Handicap', class:'IC', races: [ {date:''},{date:''} ]}
  };

  function renderForSeries(key){
    const tbody = table.querySelector('tbody');
    tbody.innerHTML = '';
    if(key === 'none'){
      // render examples (kept simple)
      tbody.innerHTML = `
        <tr data-series="none">
          <td><input class="cell-input small" data-field="od" value="Monotype"></td>
          <td><input class="cell-input small" data-field="class" value="FM"></td>
          <td><input class="cell-input" data-field="date" type="date" value="2026-04-10"></td>
          <td><input class="cell-input small" data-field="time" type="time" value="10:30"></td>
          <td><input class="cell-input" data-field="name" value="Regate Matinale"></td>
          <td><input class="cell-input small" data-field="course" value="Parcours A"></td>
        </tr>
        <tr data-series="none">
          <td><input class="cell-input small" data-field="od" value="Handicap"></td>
          <td><input class="cell-input small" data-field="class" value="Open"></td>
          <td><input class="cell-input" data-field="date" type="date" value="2026-04-10"></td>
          <td><input class="cell-input small" data-field="time" type="time" value="14:00"></td>
          <td><input class="cell-input" data-field="name" value="Course Après-midi"></td>
          <td><input class="cell-input small" data-field="course" value="Parcours B"></td>
        </tr>
      `;
    } else {
      const def = seriesDefinitions[key];
      def.races.forEach((r,i)=>{
        const tr = document.createElement('tr');
        tr.dataset.series = key;
        // OD and class inherited, not editable
        tr.innerHTML = `
          <td>${def.od}</td>
          <td>${def.class}</td>
          <td><input class="cell-input" data-field="date" type="date" value="${r.date||''}"></td>
          <td><input class="cell-input small" data-field="time" type="time" value=""></td>
          <td><input class="cell-input" data-field="name" value="Course ${i+1}" readonly></td>
          <td><input class="cell-input small" data-field="course" value=""></td>
        `;
        tbody.appendChild(tr);
      });
      // ensure chronological order - rows already in order of def.races
    }
  }

  selector.addEventListener('change', ()=>{
    const key = selector.value;
    renderForSeries(key);
  });

  // initial
  renderForSeries('none');

  // When a time is set in a series, propagate to following races if empty
  document.addEventListener('input', (e)=>{
    if(e.target && e.target.dataset.field === 'time'){
      const tr = e.target.closest('tr');
      if(tr && tr.dataset.series && tr.dataset.series !== 'none'){
        // propagate to subsequent rows with same series if they have empty time
        const tbody = tr.parentElement;
        const rows = Array.from(tbody.querySelectorAll(`tr[data-series="${tr.dataset.series}"]`));
        const idx = rows.indexOf(tr);
        const val = e.target.value;
        for(let i=idx+1;i<rows.length;i++){
          const input = rows[i].querySelector('input[data-field="time"]');
          if(input && !input.value) input.value = val;
        }
      }
    }
  });

})();
