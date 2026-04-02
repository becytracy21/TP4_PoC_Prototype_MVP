// Maquette non fonctionnelle : redirige vers Accueil.html
(function(){
  var signupBtn = document.getElementById('signupBtn');
  if(signupBtn){
    signupBtn.addEventListener('click', function(){
      window.location.href = 'Accueil.html';
    });
  }

  document.querySelectorAll('.btn-social').forEach(function(b){
    b.addEventListener('click', function(e){
      e.preventDefault(); alert('Inscription sociale non implémentée dans cette maquette.');
    });
  });
})();
