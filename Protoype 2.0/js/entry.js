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

// Bouton logout global (certaines pages utilisent id different)
(function(){
  var btn = document.getElementById('logoutBtn');
  if(!btn) return;
  btn.addEventListener('click', function(){
    if(!confirm('Voulez-vous vraiment vous déconnecter ?')) return;
    try{ localStorage.removeItem('yrr_session_v1'); localStorage.removeItem('yrr_profile_v1'); }catch(e){}
    window.location.href = 'Connexion.html';
  });
})();

// entry.js
// Gestion des inscriptions (Entry page)
// Stockage local : localStorage.entriesData

(function(){
  const DEFAULT_CLASSES = (window.defaultData && window.defaultData.classes) ? window.defaultData.classes : ["Laser","Solo","Albacore","TS-240","Wanderer"];
  const STORAGE_KEY = 'yrr_entries_v1';

  // Structure: { series: [{name, races:[{name, entries:[]}] }], currentSeriesIndex, currentRaceIndex }
  function loadState(){
    const raw = localStorage.getItem(STORAGE_KEY);
    if(raw){
      try {
        const parsed = JSON.parse(raw);
        if(parsed && typeof parsed === 'object') return parsed; // seulement si on a un objet valide
        // si parsed est null (ou autre), on ignore et on crée l'état de demo
      } catch(e) { /* fallthrough */ }
    }
    const demo = {
      series: [
        { name: 'Series A', races: [
            { name:'Course 1', entries:[
                { boatName: 'Quick Silver', boatClass: 'Laser', sailNumber: '104', helm: 'Dana', result: '1', position: '', points: '' },
                { boatName: 'Sea Breeze', boatClass: 'Laser', sailNumber: '101', helm: 'Alice', result: '01:20:30', position: '', points: '' },
                { boatName: 'Wind Rider', boatClass: 'Solo', sailNumber: '102', helm: 'Bob', result: '01:25:10', position: '', points: '' },
                { boatName: 'Blue Horizon', boatClass: 'Albacore', sailNumber: '103', helm: 'Charlie', result: 'DNS', position: '', points: '' },
                { boatName: 'Wave Runner', boatClass: 'TS-240', sailNumber: '105', helm: 'Eve', result: '', position: '', points: '' }
              ] },
          ] },
        { name: 'Series B', races: [ {name:'Course 1', entries:[]}] }
      ],
      currentSeriesIndex: 0,
      currentRaceIndex: 0
    };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(demo));
    return demo;
  }

  function saveState(s){
    localStorage.setItem(STORAGE_KEY, JSON.stringify(s));
  }

  const state = loadState();

  // DOM refs
  const entryTitle = document.getElementById('entryTitle');
  const entrySubtitle = document.getElementById('entrySubtitle');
  const prevRaceBtn = document.getElementById('prevRace');
  const nextRaceBtn = document.getElementById('nextRace');
  const addEntryBtn = document.getElementById('addEntryBtn');
  const tableBody = document.querySelector('#entriesTable tbody');
  const messageEl = document.getElementById('message');
  const addEntryForm = document.getElementById('addEntryForm');
  const addEntryDetail = document.getElementById('addEntry');

  function currentRaceObj(){
    const s = state.series[state.currentSeriesIndex];
    if(!s) return null;
    return s.races[state.currentRaceIndex] || null;
  }

  function updateTitle(){
    const sIdx = state.currentSeriesIndex + 1;
    const rIdx = state.currentRaceIndex + 1;
    const sName = (state.series[state.currentSeriesIndex] && state.series[state.currentSeriesIndex].name) || ('Series ' + sIdx);
    const rName = (state.series[state.currentSeriesIndex] && state.series[state.currentSeriesIndex].races[state.currentRaceIndex] && state.series[state.currentSeriesIndex].races[state.currentRaceIndex].name) || ('Race ' + rIdx);
    if(entryTitle) entryTitle.textContent = `${sName} — ${rName}`;
    if(entrySubtitle) entrySubtitle.textContent = `Série ${sIdx} / Course ${rIdx}`;
  }

  function clampNavigation(){
    if(prevRaceBtn) prevRaceBtn.disabled = (state.currentSeriesIndex === 0 && state.currentRaceIndex === 0);
    if(nextRaceBtn){
      const lastSeries = state.series.length - 1;
      const lastRace = state.series[state.series.length - 1].races.length - 1;
      nextRaceBtn.disabled = (state.currentSeriesIndex === lastSeries && state.currentRaceIndex === lastRace);
    }
  }

  function renderTable(){
    if(!tableBody) return;
    tableBody.innerHTML = '';
    const race = currentRaceObj();
    if(!race) return;

    const entries = Array.isArray(race.entries) ? race.entries : [];

    entries.forEach((e, idx) => {
      const tr = document.createElement('tr');
      tr.dataset.index = idx;

      function cellText(text, className){
        const td = document.createElement('td');
        if(className) td.className = className;
        td.textContent = (text !== undefined && text !== null) ? String(text) : '';
        return td;
      }

      tr.appendChild(cellText(e.boatName || ''));
      tr.appendChild(cellText(e.boatClass || ''));
      tr.appendChild(cellText(e.sailNumber || ''));
      tr.appendChild(cellText(e.helm || ''));
      tr.appendChild(cellText(e.result || ''));
      tr.appendChild(cellText(e.position || ''));
      tr.appendChild(cellText(e.points || ''));

      // action cell with delete button (similar style to Boat.html)
      const actionTd = document.createElement('td');
      actionTd.className = 'action-cell';
      const delBtn = document.createElement('button');
      delBtn.className = 'btn-delete';
      delBtn.type = 'button';
      delBtn.textContent = 'Supprimer';
      delBtn.addEventListener('click', () => { race.entries.splice(idx, 1); saveAndRender(); });
      actionTd.appendChild(delBtn);
      tr.appendChild(actionTd);

      tableBody.appendChild(tr);
    });
  }

  function saveAndRender(){
    saveState(state);
    computePositionsAndPoints(currentRaceObj());
    updateTitle();
    clampNavigation();
    renderTable();
  }

  function validateResult(val){
    if(!val) return null; // empty allowed
    const special = ['DNS','DNC','DNF','DSQ','OCS','RDG','RTB','UFD'];
    if(special.includes(val.toUpperCase())) return null;
    // time formats: HH:MM:SS or MM:SS or H:MM:SS.m and decimals
    const timeRe = /^\d{1,2}(:\d{2}){1,2}(\.\d+)?$/;
    const posRe = /^\d+$/;
    if(timeRe.test(val) || posRe.test(val)) return null;
    return 'Format de résultat invalide (attendu HH:MM:SS, MM:SS, nombre ou DNS/OCS/etc.)';
  }

  function computePositionsAndPoints(race){
    if(!race || !Array.isArray(race.entries)) return;

    const parsed = race.entries.map((e, idx) => {
      const raw = e.result ? String(e.result).trim().toUpperCase() : '';
      const p = { idx, e, raw, time: null, special: null, numericPos: null };
      if(!raw) return p;
      if(['DNS','DNC','DNF','DSQ','OCS','RDG','RTB','UFD'].includes(raw)){
        p.special = raw; return p;
      }
      if(/^\d+$/.test(raw)){
        p.numericPos = parseInt(raw, 10); return p;
      }
      const parts = raw.split(':').map(x => x.replace(',', '.'));
      if(parts.length === 2 || parts.length === 3){
        let seconds = 0;
        if(parts.length === 2){
          const mm = parseFloat(parts[0]); const ss = parseFloat(parts[1]);
          if(!isFinite(mm) || !isFinite(ss)) return p;
          seconds = mm * 60 + ss;
        } else {
          const hh = parseFloat(parts[0]); const mm = parseFloat(parts[1]); const ss = parseFloat(parts[2]);
          if(!isFinite(hh) || !isFinite(mm) || !isFinite(ss)) return p;
          seconds = hh * 3600 + mm * 60 + ss;
        }
        p.time = seconds; return p;
      }
      return p;
    });

    // Clear
    race.entries.forEach(e => { e.position = ''; e.points = ''; });

    // Explicit numeric positions
    const explicit = parsed.filter(x => x.numericPos !== null).sort((a,b) => a.numericPos - b.numericPos);
    explicit.forEach(it => { it.e.position = it.numericPos; it.e.points = computePoints(it.e.position); });

    // Time-based
    const timed = parsed.filter(x => x.time !== null && x.numericPos === null).sort((a,b) => a.time - b.time);
    let nextPos = 1;
    const taken = new Set(explicit.map(e => e.numericPos));
    while(taken.has(nextPos)) nextPos++;
    timed.forEach(t => { t.e.position = nextPos; t.e.points = computePoints(nextPos); taken.add(nextPos); nextPos++; });

    // Specials
    const specials = parsed.filter(x => x.special !== null);
    const totalCompetitors = race.entries.length;
    specials.forEach(s => {
      s.e.position = '';
      if(['DNS','DNC','DNF','DSQ','OCS','UFD'].includes(String(s.special || '').toUpperCase())){
        s.e.points = totalCompetitors + 1;
      } else {
        s.e.points = '';
      }
    });

    saveState(state);
  }

  function computePoints(position){
    if(!position) return '';
    const pos = parseInt(position, 10);
    if(!isFinite(pos)) return '';
    return pos; // points = position (simple implementation)
  }

  function showMessage(txt, isError){
    if(!messageEl) return;
    messageEl.textContent = txt || '';
    messageEl.style.color = isError ? 'crimson' : '#666';
  }
  function clearMessage(){ if(messageEl) messageEl.textContent = ''; }

  // Navigation handlers
  if(prevRaceBtn) prevRaceBtn.addEventListener('click', () => {
    if(state.currentRaceIndex > 0){ state.currentRaceIndex--; }
    else if(state.currentSeriesIndex > 0){ state.currentSeriesIndex--; state.currentRaceIndex = state.series[state.currentSeriesIndex].races.length - 1; }
    saveAndRender();
  });

  if(nextRaceBtn) nextRaceBtn.addEventListener('click', () => {
    if(state.currentRaceIndex < state.series[state.currentSeriesIndex].races.length - 1){ state.currentRaceIndex++; }
    else if(state.currentSeriesIndex < state.series.length - 1){ state.currentSeriesIndex++; state.currentRaceIndex = 0; }
    saveAndRender();
  });

  if(addEntryBtn) addEntryBtn.addEventListener('click', () => {
    const race = currentRaceObj();
    if(!race) return;
    const newEntry = { boatName:'', boatClass: DEFAULT_CLASSES[0], sailNumber:'', helm:'', result:'', position:'', points:'' };
    race.entries.push(newEntry);
    saveAndRender();
    setTimeout(() => {
      const lastRow = tableBody.querySelector('tr[data-index="' + (race.entries.length - 1) + '"]');
      if(lastRow){ const inp = lastRow.querySelector('input'); if(inp) inp.focus(); }
    }, 50);
  });

  if(addEntryForm){
    addEntryForm.addEventListener('submit', function(e){
      e.preventDefault();
      const race = currentRaceObj(); if(!race) return;
      const boatName = document.getElementById('entryBoatName').value.trim();
      const boatClass = document.getElementById('entryBoatClass').value || DEFAULT_CLASSES[0];
      const sailNumber = document.getElementById('entrySail').value.trim();
      const helm = document.getElementById('entryHelm').value.trim();
      const result = document.getElementById('entryResult').value.trim();
      const newEntry = { boatName, boatClass, sailNumber, helm, result, position:'', points:'' };
      race.entries.push(newEntry);
      // close details
      if(addEntryDetail) addEntryDetail.removeAttribute('open');
      // reset form
      addEntryForm.reset();
      saveAndRender();
    });
  }

  // remove legacy addEntryBtn usage if present
  const oldAddBtn = document.getElementById('addEntryBtn');
  if(oldAddBtn) oldAddBtn.style.display = 'none';

  // Initial render
  updateTitle();
  clampNavigation();
  // compute initial positions for the current race so the table is filled
  computePositionsAndPoints(currentRaceObj());
  renderTable();

  // Expose for debugging
  window.__yrr_entry = { state, saveState };
})();