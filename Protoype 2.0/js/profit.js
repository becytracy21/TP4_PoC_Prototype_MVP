// Déconnexion : confirmation et nettoyage clé locale
(function(){
  var btn = document.getElementById('logoutBtn');
  if(!btn) return;
  btn.addEventListener('click', function(){
    if(!confirm('Voulez-vous vraiment vous déconnecter ?')) return;
    try{ localStorage.removeItem('yrr_profile_v1'); localStorage.removeItem('yrr_session_v1'); }catch(e){}
    window.location.href = 'Connexion.html';
  });
})();

// Réplique fonctionnelle du snippet : gestion du profil en local
(function(){
  const KEY = 'yrr_profile_v1';
  const inputFile = document.getElementById('avatarInput');
  const preview = document.getElementById('avatarPreview'); // now a div
  const removeBtn = document.getElementById('removeAvatar');
  const saveBtn = document.getElementById('saveProfile');
  const cancelBtn = document.getElementById('cancelProfile');
  const msgEl = document.getElementById('profileMsg');

  const fields = {
    fullName: document.getElementById('fullName'),
    username: document.getElementById('username'),
    email: document.getElementById('email'),
    phone: document.getElementById('phone')
  };

  let currentAvatarData = null;

  function showMsg(text, success=true){
    if(!msgEl) return; msgEl.textContent = text;
    msgEl.style.color = success ? '#28a745' : '#d9534f';
    setTimeout(()=>{ msgEl.textContent = ''; }, 3000);
  }

  function readFileAsDataURL(file){
    return new Promise((res,rej)=>{
      const r = new FileReader();
      r.onload = ()=> res(r.result);
      r.onerror = ()=> rej(new Error('Lecture impossible'));
      r.readAsDataURL(file);
    });
  }

  function loadProfile(){
    try{
      const raw = localStorage.getItem(KEY);
      if(!raw) return;
      const obj = JSON.parse(raw);
      if(obj.avatar){
        preview.style.backgroundImage = `url(${obj.avatar})`; preview.textContent = '';
        currentAvatarData = obj.avatar;
      }
      if(obj.fullName) fields.fullName.value = obj.fullName;
      if(obj.username) fields.username.value = obj.username;
      if(obj.email) fields.email.value = obj.email;
      if(obj.phone) fields.phone.value = obj.phone;
      // update displayed names under avatar
      document.getElementById('displayFullName').textContent = obj.fullName || 'John Doe';
      document.getElementById('displayUsername').textContent = obj.username ? '@'+obj.username : '@jdupont';
    }catch(e){}
  }

  function saveProfile(){
    const payload = {
      avatar: currentAvatarData || null,
      fullName: fields.fullName.value.trim(),
      username: fields.username.value.trim(),
      email: fields.email.value.trim(),
      phone: fields.phone.value.trim()
    };

    if(!payload.fullName){ showMsg('Le nom complet est requis', false); return; }
    if(!payload.username){ showMsg("Le nom d'utilisateur est requis", false); return; }
    if(payload.email && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(payload.email)){ showMsg('Email invalide', false); return; }
    if(payload.phone && !/^[0-9+\s\-()]{6,20}$/.test(payload.phone)){ showMsg('Téléphone invalide', false); return; }

    try{ localStorage.setItem(KEY, JSON.stringify(payload)); showMsg('Profil enregistré', true);
      // met à jour l'affichage sous l'avatar
      document.getElementById('displayFullName').textContent = payload.fullName;
      document.getElementById('displayUsername').textContent = payload.username ? '@'+payload.username : '';
    }catch(e){ showMsg('Impossible d\'enregistrer', false); }
  }

  if(inputFile){
    inputFile.addEventListener('change', async (e)=>{
      const f = e.target.files && e.target.files[0];
      if(!f) return;
      if(!/^image\//.test(f.type)){ showMsg('Veuillez choisir une image', false); return; }
      try{
        const data = await readFileAsDataURL(f);
        preview.style.backgroundImage = `url(${data})`;
        preview.textContent = '';
        currentAvatarData = data;
      }catch(err){ showMsg('Lecture du fichier impossible', false); }
    });
  }

  if(removeBtn){
    removeBtn.addEventListener('click', ()=>{ 
      preview.style.backgroundImage = ''; preview.textContent = 'JD'; currentAvatarData = null; 
    });
  }

  // remplacer le binding des boutons pour qu'ils retournent à la page précédente
  if(saveBtn) saveBtn.addEventListener('click', function(e){
    // ne pas enregistrer ici, juste revenir à la page précédente
    try{ window.history.back(); }catch(err){ window.location.href = 'Accueil.html'; }
  });
  if(cancelBtn) cancelBtn.addEventListener('click', function(e){
    // annuler => revenir à la page précédente
    try{ window.history.back(); }catch(err){ window.location.href = 'Accueil.html'; }
  });

  loadProfile();
})();
