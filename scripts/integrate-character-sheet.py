from pathlib import Path

INDEX = Path('docs/index.html')
text = INDEX.read_text(encoding='utf-8')

if 'id="sheet-view"' in text and 'id="app-options"' in text:
    print('Character sheet integration already present; no changes needed.')
    raise SystemExit(0)

css = r'''

/* App navigation + character sheet */
.app-options{position:fixed;z-index:80;left:10px;top:10px;font-family:Georgia,'Times New Roman',serif}
.options-button{border:1px solid rgba(62,45,27,.42);background:rgba(245,228,191,.96);color:var(--ink);font:700 13px Georgia,serif;border-radius:9px;padding:8px 10px;box-shadow:0 3px 10px rgba(50,34,17,.2)}
.options-menu{position:absolute;left:0;top:42px;min-width:170px;padding:6px;border:1px solid rgba(62,45,27,.38);border-radius:10px;background:rgba(245,228,191,.98);box-shadow:0 10px 24px rgba(50,34,17,.24)}
.options-menu[hidden]{display:none}
.options-menu button{display:block;width:100%;border:0;background:transparent;color:var(--ink);font:700 14px Georgia,serif;text-align:left;padding:9px 10px;border-radius:7px}
.options-menu button:hover,.options-menu button[aria-current="page"]{background:rgba(209,181,125,.46)}
.app-view[hidden]{display:none!important}
.sheet-main{display:block;max-width:1120px;margin:auto;padding:10px 14px 24px}
.sheet-shell{padding:16px}
.sheet-identity{display:flex;flex-wrap:wrap;gap:8px 18px;align-items:baseline;margin-bottom:14px;padding-bottom:12px;border-bottom:1px solid rgba(70,50,30,.25)}
.sheet-name{font-size:clamp(1.55rem,4vw,2.25rem);font-weight:700}
.sheet-meta{color:var(--muted);font-size:.95rem}
.sheet-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.sheet-section{padding:13px;border:1px solid rgba(70,50,30,.27);border-radius:10px;background:rgba(255,250,230,.22)}
.sheet-section h2{margin:0 0 10px;font-size:1.03rem}
.ability-grid{display:grid;grid-template-columns:repeat(6,minmax(72px,1fr));gap:8px}
.ability{padding:10px 6px;text-align:center;border:1px solid rgba(70,50,30,.3);border-radius:10px;background:rgba(245,228,191,.62)}
.ability-name{font-size:.72rem;letter-spacing:.08em;font-weight:700;color:var(--muted)}
.ability-score{font-size:1.55rem;font-weight:700;line-height:1.1;margin-top:4px}
.ability-mod{font-size:.86rem;color:var(--muted);margin-top:3px}
.sheet-list{margin:0;padding-left:18px}
.sheet-list li{margin:6px 0;line-height:1.3}
.status-pill{display:inline-block;margin-left:5px;border:1px solid rgba(70,50,30,.3);border-radius:999px;padding:1px 6px;font-size:.72rem;color:var(--muted)}
.unknown-list li{color:#5f5140}
.unknown-badge{display:inline-block;font-size:.67rem;letter-spacing:.05em;font-weight:700;border:1px solid rgba(95,71,37,.4);border-radius:999px;padding:2px 6px;margin-left:5px;color:#6c5635;background:rgba(232,204,148,.3)}
.sheet-note{font-size:.83rem;line-height:1.4;color:var(--muted)}
.sheet-footer-note{margin-top:12px;padding:10px 12px;border-left:3px solid var(--note);background:rgba(255,250,230,.3);border-radius:0 8px 8px 0}
@media(max-width:760px){
  .app-options{left:7px;top:7px}
  .sheet-main{padding:8px}
  .sheet-shell{padding:12px}
  .sheet-grid{grid-template-columns:1fr}
  .ability-grid{grid-template-columns:repeat(3,1fr)}
}
'''

menu = r'''<div id="app-options" class="app-options">
  <button id="options-button" class="options-button" aria-haspopup="true" aria-expanded="false">☰ Options</button>
  <div id="options-menu" class="options-menu" role="menu" hidden>
    <button type="button" data-app-view="map" aria-current="page">Map</button>
    <button type="button" data-app-view="character">Character Sheet</button>
  </div>
</div>
<section id="map-view" class="app-view">
'''

sheet = r'''
</section>

<section id="sheet-view" class="app-view" hidden>
  <header>
    <h1>Mårék — Character Sheet</h1>
    <p class="sub">Player-safe live character state · unresolved mechanics remain visibly unknown</p>
  </header>
  <main class="sheet-main">
    <section class="card sheet-shell">
      <div id="sheet-identity" class="sheet-identity">
        <div class="sheet-name">Mårék</div>
        <div class="sheet-meta">Loading character state…</div>
      </div>

      <section class="sheet-section" style="margin-bottom:12px">
        <h2>Ability Scores</h2>
        <div id="ability-grid" class="ability-grid"></div>
      </section>

      <div class="sheet-grid">
        <section class="sheet-section">
          <h2>Known Competencies</h2>
          <ul id="competency-list" class="sheet-list"></ul>
        </section>
        <section class="sheet-section">
          <h2>Established Equipment</h2>
          <ul id="equipment-list" class="sheet-list"></ul>
        </section>
        <section class="sheet-section">
          <h2>Mechanics Still Unresolved</h2>
          <ul id="unresolved-list" class="sheet-list unknown-list"></ul>
        </section>
        <section class="sheet-section">
          <h2>Sheet Rules</h2>
          <div id="rules-notes"></div>
        </section>
      </div>
      <div class="sheet-footer-note sheet-note">This sheet is deliberately conservative: it shows established player-safe facts and marks unresolved mechanics instead of importing default PHB values.</div>
    </section>
  </main>
</section>
'''

js = r'''

// App view + character sheet integration
const appOptions=document.getElementById('app-options');
const optionsButton=document.getElementById('options-button');
const optionsMenu=document.getElementById('options-menu');
const mapView=document.getElementById('map-view');
const sheetView=document.getElementById('sheet-view');

function fmtMod(n){return n>=0?`+${n}`:`${n}`}
function renderCharacterSheet(c){
  const identity=document.getElementById('sheet-identity');
  identity.innerHTML='';
  const name=document.createElement('div');name.className='sheet-name';name.textContent=c.name||'Mårék';
  const meta=document.createElement('div');meta.className='sheet-meta';
  meta.textContent=[c.species,c.age?`Age ${c.age}`:'',c.class,c.level?`Level ${c.level}`:''].filter(Boolean).join(' · ');
  identity.append(name,meta);

  const abilityRoot=document.getElementById('ability-grid');abilityRoot.innerHTML='';
  ['STR','DEX','CON','INT','WIS','CHA'].forEach(key=>{
    const a=c.ability_scores?.[key];if(!a)return;
    const box=document.createElement('div');box.className='ability';
    const k=document.createElement('div');k.className='ability-name';k.textContent=key;
    const score=document.createElement('div');score.className='ability-score';score.textContent=a.score;
    const mod=document.createElement('div');mod.className='ability-mod';mod.textContent=`Modifier ${fmtMod(a.modifier)}`;
    box.append(k,score,mod);abilityRoot.appendChild(box);
  });

  const comps=document.getElementById('competency-list');comps.innerHTML='';
  (c.competencies||[]).forEach(x=>{
    const li=document.createElement('li');li.textContent=x.name;
    if(x.status){const pill=document.createElement('span');pill.className='status-pill';pill.textContent=x.status;li.appendChild(pill)}
    comps.appendChild(li);
  });

  const equip=document.getElementById('equipment-list');equip.innerHTML='';
  (c.equipment||[]).forEach(x=>{
    const li=document.createElement('li');
    const qty=Number.isFinite(x.quantity)?` ×${x.quantity}`:'';
    li.append(document.createTextNode(`${x.name}${qty}`));
    if(x.status){const pill=document.createElement('span');pill.className='status-pill';pill.textContent=x.status;li.appendChild(pill)}
    equip.appendChild(li);
  });

  const unresolved=document.getElementById('unresolved-list');unresolved.innerHTML='';
  (c.unresolved||[]).forEach(x=>{
    const li=document.createElement('li');li.append(document.createTextNode(x));
    const badge=document.createElement('span');badge.className='unknown-badge';badge.textContent='UNKNOWN';li.appendChild(badge);
    unresolved.appendChild(li);
  });

  const notes=document.getElementById('rules-notes');notes.innerHTML='';
  (c.rules_notes||[]).forEach(x=>{const p=document.createElement('p');p.className='sheet-note';p.textContent=x;notes.appendChild(p)});
}

function closeOptions(){optionsMenu.hidden=true;optionsButton.setAttribute('aria-expanded','false')}
function openOptions(){optionsMenu.hidden=false;optionsButton.setAttribute('aria-expanded','true')}
function setAppView(which,{updateHash=true}={}){
  const showSheet=which==='character';
  mapView.hidden=showSheet;
  sheetView.hidden=!showSheet;
  optionsMenu.querySelectorAll('[data-app-view]').forEach(b=>b.setAttribute('aria-current',b.dataset.appView===which?'page':'false'));
  if(updateHash)history.replaceState(null,'',showSheet?'#character':'#map');
  document.title=showSheet?'Mårék — Character Sheet':'Mårék — Known Regional Map';
  closeOptions();
  if(!showSheet&&typeof setView==='function')requestAnimationFrame(()=>setView());
}

optionsButton.addEventListener('click',()=>optionsMenu.hidden?openOptions():closeOptions());
optionsMenu.querySelectorAll('[data-app-view]').forEach(b=>b.addEventListener('click',()=>setAppView(b.dataset.appView)));
document.addEventListener('click',e=>{if(!appOptions.contains(e.target))closeOptions()});
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeOptions()});
window.addEventListener('hashchange',()=>setAppView(location.hash==='#character'?'character':'map',{updateHash:false}));

fetch('character-state.json').then(r=>r.json()).then(renderCharacterSheet).catch(()=>{
  const identity=document.getElementById('sheet-identity');
  identity.innerHTML='<div class="sheet-name">Mårék</div><div class="sheet-meta">Character data could not be loaded.</div>';
});
setAppView(location.hash==='#character'?'character':'map',{updateHash:false});
'''

if '</style>' not in text:
    raise RuntimeError('Could not find </style> anchor in docs/index.html')
text = text.replace('</style>', css + '\n</style>', 1)

body_anchor = '<body>\n<header>'
if body_anchor not in text:
    raise RuntimeError('Could not find <body>/<header> anchor in docs/index.html')
text = text.replace(body_anchor, '<body>\n' + menu + '<header>', 1)

main_script_anchor = '</main>\n\n<script>'
if main_script_anchor not in text:
    raise RuntimeError('Could not find map </main>/<script> anchor in docs/index.html')
text = text.replace(main_script_anchor, '</main>' + sheet + '\n\n<script>', 1)

script_anchor = "window.addEventListener('resize',()=>requestAnimationFrame(resolveCollisions));\n</script>"
if script_anchor not in text:
    raise RuntimeError('Could not find final map script anchor in docs/index.html')
text = text.replace(script_anchor, "window.addEventListener('resize',()=>requestAnimationFrame(resolveCollisions));\n" + js + '\n</script>', 1)

INDEX.write_text(text, encoding='utf-8')
print('Integrated options menu and character sheet into docs/index.html')
