// Logic for Connexion.html moved from inline script
(function(){
  function setup(){
    const loginBtn = document.getElementById('loginBtn');
    if(loginBtn){
      loginBtn.addEventListener('click', function(){
        window.location.href = 'Accueil.html';
      });
    }
    document.querySelectorAll('.btn-social').forEach(b=>b.addEventListener('click', function(e){ e.preventDefault(); alert('Connexion sociale non implémentée dans cette maquette.'); }));
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', setup); else setup();
})();
