// Gère le recalcul des Totals selon discards et l'affichage de l'état
(function(){
  const select = document.getElementById('discards');
  const toggle = document.getElementById('toggleDiscards');
  const status = document.getElementById('seriesStatus');
  const table = document.getElementById('seriesTable');

  let enabled = true; // discards activés

  function recalc(){
    const toCount = parseInt(select.value,10); // nombre de courses à compter
    const rows = table.querySelectorAll('tbody tr');
    rows.forEach(row=>{
      const scores = Array.from(row.querySelectorAll('td')).slice(4,9).map(td=>{
        const v = parseFloat(td.textContent);
        return isNaN(v) ? Infinity : v;
      });

      let total;
      if(enabled){
        const sorted = scores.slice().sort((a,b)=>a-b);
        const best = sorted.slice(0,toCount);
        total = best.reduce((s,n)=>s + (isFinite(n) ? n : 0),0);
      } else {
        total = scores.reduce((s,n)=> s + (isFinite(n) ? n : 0),0);
      }

      row.querySelector('.total').textContent = total;
    });

    // recalcul classement général
    const rowsArray = Array.from(rows);
    rowsArray.sort((a,b)=> parseFloat(a.querySelector('.total').textContent) - parseFloat(b.querySelector('.total').textContent));
    rowsArray.forEach((r,i)=> r.querySelector('.overall').textContent = i+1);

    // mettre à jour le titre
    status.textContent = enabled ? '(Série A — éliminations activées)' : '(Série A — éliminations désactivées)';
  }

  toggle.addEventListener('click', ()=>{
    enabled = !enabled;
    toggle.classList.toggle('active', enabled);
    toggle.textContent = enabled ? 'Eliminations activées' : 'Eliminations désactivées';
    recalc();
  });

  // bouton Resultat - navigation
  const seriesResultBtn = document.getElementById('series-result');
  if(seriesResultBtn){ seriesResultBtn.addEventListener('click', ()=>{ window.location.href = 'Resultat.html'; }); }

  select.addEventListener('change', recalc);
  recalc();
})();

// Menu profil: ouverture/fermeture et action déconnexion
(function(){
  const toggle = document.getElementById('profileToggle');
  const dropdown = document.getElementById('profileDropdown');
  if(!toggle || !dropdown) return;

  function openDropdown(){ dropdown.hidden = false; toggle.setAttribute('aria-expanded','true'); }
  function closeDropdown(){ dropdown.hidden = true; toggle.setAttribute('aria-expanded','false'); }

  toggle.addEventListener('click', function(e){ e.stopPropagation(); if(dropdown.hidden) openDropdown(); else closeDropdown(); });

  // logout from menu
  const logoutMenuBtn = document.getElementById('logoutMenuBtn');
  if(logoutMenuBtn){
    logoutMenuBtn.addEventListener('click', function(){
      if(!confirm('Voulez-vous vraiment vous déconnecter ?')) return;
      try{ localStorage.removeItem('yrr_session_v1'); localStorage.removeItem('yrr_profile_v1'); }catch(e){}
      window.location.href = 'Connexion.html';
    });
  }

  // fermer au clic dehors
  document.addEventListener('click', function(e){ if(!dropdown.hidden && !toggle.contains(e.target) && !dropdown.contains(e.target)) closeDropdown(); });
  // fermer avec Escape
  document.addEventListener('keydown', function(e){ if(e.key === 'Escape') closeDropdown(); });
})();
