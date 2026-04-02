(function(){
  function setup(){
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
        try{
          localStorage.removeItem('yrr_session_v1');
          localStorage.removeItem('yrr_profile_v1');
          localStorage.removeItem('yrr_user');
        }catch(e){}
        window.location.href = 'Connexion.html';
      });
    }

    // fermer au clic dehors
    document.addEventListener('click', function(e){ if(!dropdown.hidden && !toggle.contains(e.target) && !dropdown.contains(e.target)) closeDropdown(); });
    // fermer avec Escape
    document.addEventListener('keydown', function(e){ if(e.key === 'Escape') closeDropdown(); });
  }

  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', setup); else setup();
})();
