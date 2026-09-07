from pathlib import Path

INDEX = Path('docs/index.html')
text = INDEX.read_text(encoding='utf-8')

if 'id="inventory-view"' in text and 'id="companions-view"' in text and 'id="projects-view"' in text and 'id="calendar-view"' in text:
    print('Campaign tools integration already present; no changes needed.')
    raise SystemExit(0)

css = r'''

/* Inventory, companions, projects, and calendar */
.tool-main{display:block;max-width:1120px;margin:auto;padding:10px 14px 24px}
.tool-shell{padding:16px}
.tool-context{margin:0 0 14px;padding:10px 12px;border-left:3px solid var(--note);background:rgba(255,250,230,.3);border-radius:0 8px 8px 0;color:var(--muted);font-size:.88rem;line-height:1.4}
.tool-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.tool-section{padding:13px;border:1px solid rgba(70,50,30,.27);border-radius:10px;background:rgba(255,250,230,.22)}
.tool-section h2{margin:0 0 10px;font-size:1.03rem}
.item-stack{display:grid;gap:8px}
.item-row{padding:9px 10px;border:1px solid rgba(70,50,30,.22);border-radius:8px;background:rgba(245,228,191,.42)}
.item-title{font-weight:700;line-height:1.25}
.item-meta{margin-top:3px;color:var(--muted);font-size:.8rem;line-height:1.35}
.item-qty{float:right;font-weight:700;color:var(--muted)}
.companion-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
.companion-card{padding:12px;border:1px solid rgba(70,50,30,.25);border-radius:10px;background:rgba(245,228,191,.42)}
.companion-name{font-size:1.08rem;font-weight:700;margin-bottom:4px}
.project-list{display:grid;gap:10px}
.project-card{padding:12px;border:1px solid rgba(70,50,30,.25);border-radius:10px;background:rgba(245,228,191,.42)}
.project-top{display:flex;gap:8px;align-items:flex-start;justify-content:space-between;margin-bottom:6px}
.project-name{font-size:1.06rem;font-weight:700}
.project-status{white-space:nowrap;border:1px solid rgba(70,50,30,.3);border-radius:999px;padding:2px 7px;font-size:.68rem;letter-spacing:.04em;color:var(--muted);background:rgba(255,250,230,.34)}
.project-kind{font-size:.76rem;color:var(--muted);margin-bottom:7px}
.project-copy{font-size:.88rem;line-height:1.4;margin:5px 0}
.calendar-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin-bottom:12px}
.calendar-field{padding:12px;text-align:center;border:1px solid rgba(70,50,30,.27);border-radius:10px;background:rgba(245,228,191,.52)}
.calendar-label{font-size:.7rem;letter-spacing:.08em;font-weight:700;color:var(--muted);text-transform:uppercase}
.calendar-value{font-size:1.18rem;font-weight:700;margin-top:5px}
.calendar-marker{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin-bottom:12px}
.calendar-marker .item-row{min-height:72px}
.empty-state{color:var(--muted);font-size:.86rem;font-style:italic;line-height:1.4}
@media(max-width:760px){
  .tool-main{padding:8px}
  .tool-shell{padding:12px}
  .tool-grid,.companion-grid{grid-template-columns:1fr}
  .calendar-grid{grid-template-columns:repeat(3,1fr);gap:6px}
  .calendar-field{padding:9px 5px}
  .calendar-value{font-size:1rem}
  .calendar-marker{grid-template-columns:1fr}
  .project-top{display:block}
  .project-status{display:inline-block;margin-top:5px}
}
'''

menu_anchor = '    <button type="button" data-app-view="character">Character Sheet</button>'
menu_replacement = menu_anchor + r'''
    <button type="button" data-app-view="inventory">Inventory</button>
    <button type="button" data-app-view="companions">Companions</button>
    <button type="button" data-app-view="projects">Projects</button>
    <button type="button" data-app-view="calendar">Calendar</button>'''

views = r'''

<section id="inventory-view" class="app-view" hidden>
  <header>
    <h1>Mårék — Inventory</h1>
    <p class="sub">Player-safe carried and recently recovered items · unknown totals stay unknown</p>
  </header>
  <main class="tool-main">
    <section class="card tool-shell">
      <div id="inventory-context" class="tool-context">Loading current campaign context…</div>
      <div class="tool-grid">
        <section class="tool-section">
          <h2>Established Carried Gear</h2>
          <div id="inventory-established" class="item-stack"></div>
        </section>
        <section class="tool-section">
          <h2>Recent Recovered Items</h2>
          <div id="inventory-recovered" class="item-stack"></div>
        </section>
        <section class="tool-section" style="grid-column:1/-1">
          <h2>Still Unresolved</h2>
          <ul id="inventory-unresolved" class="sheet-list unknown-list"></ul>
        </section>
      </div>
    </section>
  </main>
</section>

<section id="companions-view" class="app-view" hidden>
  <header>
    <h1>Mårék — Companions</h1>
    <p class="sub">Player-known current company only · no hidden NPC state</p>
  </header>
  <main class="tool-main">
    <section class="card tool-shell">
      <div id="companions-context" class="tool-context">Loading current campaign context…</div>
      <div id="companions-grid" class="companion-grid"></div>
    </section>
  </main>
</section>

<section id="projects-view" class="app-view" hidden>
  <header>
    <h1>Mårék — Projects</h1>
    <p class="sub">Current undertakings and established development milestones</p>
  </header>
  <main class="tool-main">
    <section class="card tool-shell">
      <div id="projects-context" class="tool-context">Loading current campaign context…</div>
      <div id="projects-list" class="project-list"></div>
    </section>
  </main>
</section>

<section id="calendar-view" class="app-view" hidden>
  <header>
    <h1>Mårék — Campaign Calendar</h1>
    <p class="sub">Known campaign time only · unresolved dates are never invented</p>
  </header>
  <main class="tool-main">
    <section class="card tool-shell">
      <div class="calendar-marker">
        <div class="item-row"><div class="calendar-label">Current Time</div><div id="calendar-time" class="calendar-value">—</div></div>
        <div class="item-row"><div class="calendar-label">Current Location</div><div id="calendar-location" class="calendar-value">—</div></div>
      </div>
      <div class="calendar-grid">
        <div class="calendar-field"><div class="calendar-label">Day</div><div id="calendar-day" class="calendar-value">UNKNOWN</div></div>
        <div class="calendar-field"><div class="calendar-label">Season</div><div id="calendar-season" class="calendar-value">UNKNOWN</div></div>
        <div class="calendar-field"><div class="calendar-label">Year</div><div id="calendar-year" class="calendar-value">UNKNOWN</div></div>
      </div>
      <div id="calendar-status" class="tool-context"></div>
      <div class="tool-grid">
        <section class="tool-section">
          <h2>Known Elapsed Time</h2>
          <div id="calendar-elapsed" class="item-stack"></div>
        </section>
        <section class="tool-section">
          <h2>Dated Events</h2>
          <div id="calendar-events" class="item-stack"></div>
        </section>
      </div>
    </section>
  </main>
</section>
'''

js_helpers = r'''

function campaignContextText(state){
  const c=state.current_context||{};
  return [c.time_of_day,c.location,c.activity].filter(Boolean).join(' · ');
}
function makeItemRow(x){
  const row=document.createElement('div');row.className='item-row';
  const title=document.createElement('div');title.className='item-title';title.textContent=x.name||x.label||'Item';
  if(Number.isFinite(x.quantity)){
    const qty=document.createElement('span');qty.className='item-qty';qty.textContent=`×${x.quantity}`;title.appendChild(qty);
  }
  row.appendChild(title);
  const details=[x.status,x.detail,x.duration].filter(Boolean).join(' · ');
  if(details){const meta=document.createElement('div');meta.className='item-meta';meta.textContent=details;row.appendChild(meta)}
  return row;
}
function renderCampaignTools(state){
  const ctx=campaignContextText(state)||'Current campaign context is not separately established.';
  ['inventory-context','companions-context','projects-context'].forEach(id=>{const n=document.getElementById(id);if(n)n.textContent=ctx});

  const established=document.getElementById('inventory-established');established.innerHTML='';
  (state.inventory?.established_carried||[]).forEach(x=>established.appendChild(makeItemRow(x)));
  if(!established.children.length)established.innerHTML='<div class="empty-state">No established carried items are currently listed.</div>';

  const recovered=document.getElementById('inventory-recovered');recovered.innerHTML='';
  (state.inventory?.recent_recovered||[]).forEach(x=>recovered.appendChild(makeItemRow(x)));
  if(!recovered.children.length)recovered.innerHTML='<div class="empty-state">No recent recovered items are currently listed.</div>';

  const invUnknown=document.getElementById('inventory-unresolved');invUnknown.innerHTML='';
  (state.inventory?.unresolved||[]).forEach(x=>{
    const li=document.createElement('li');li.append(document.createTextNode(x));
    const badge=document.createElement('span');badge.className='unknown-badge';badge.textContent='UNKNOWN';li.appendChild(badge);invUnknown.appendChild(li);
  });

  const companions=document.getElementById('companions-grid');companions.innerHTML='';
  (state.companions||[]).forEach(x=>{
    const card=document.createElement('article');card.className='companion-card';
    const name=document.createElement('div');name.className='companion-name';name.textContent=x.name;
    const status=document.createElement('div');status.className='item-meta';status.textContent=[x.status,x.location].filter(Boolean).join(' · ');
    const detail=document.createElement('div');detail.className='project-copy';detail.textContent=x.detail||'';
    card.append(name,status);if(x.detail)card.appendChild(detail);companions.appendChild(card);
  });
  if(!companions.children.length)companions.innerHTML='<div class="empty-state">No current companions are separately established.</div>';

  const projects=document.getElementById('projects-list');projects.innerHTML='';
  (state.projects||[]).forEach(x=>{
    const card=document.createElement('article');card.className='project-card';
    const top=document.createElement('div');top.className='project-top';
    const name=document.createElement('div');name.className='project-name';name.textContent=x.name;
    const status=document.createElement('div');status.className='project-status';status.textContent=x.status||'STATUS UNKNOWN';
    top.append(name,status);card.appendChild(top);
    if(x.kind){const kind=document.createElement('div');kind.className='project-kind';kind.textContent=x.kind;card.appendChild(kind)}
    if(x.summary){const p=document.createElement('p');p.className='project-copy';p.textContent=x.summary;card.appendChild(p)}
    if(x.current_state){const p=document.createElement('p');p.className='project-copy';const b=document.createElement('strong');b.textContent='Current state: ';p.append(b,document.createTextNode(x.current_state));card.appendChild(p)}
    projects.appendChild(card);
  });
  if(!projects.children.length)projects.innerHTML='<div class="empty-state">No tracked projects are currently listed.</div>';

  const cal=state.calendar||{};
  document.getElementById('calendar-time').textContent=cal.time_of_day||'UNKNOWN';
  document.getElementById('calendar-location').textContent=cal.current_location||'UNKNOWN';
  document.getElementById('calendar-day').textContent=cal.day??'UNKNOWN';
  document.getElementById('calendar-season').textContent=cal.season??'UNKNOWN';
  document.getElementById('calendar-year').textContent=cal.year??'UNKNOWN';
  document.getElementById('calendar-status').textContent=cal.date_status||'Calendar date is unresolved.';

  const elapsed=document.getElementById('calendar-elapsed');elapsed.innerHTML='';
  (cal.known_elapsed||[]).forEach(x=>elapsed.appendChild(makeItemRow(x)));
  if(!elapsed.children.length)elapsed.innerHTML='<div class="empty-state">No exact elapsed spans are currently established.</div>';

  const events=document.getElementById('calendar-events');events.innerHTML='';
  (cal.dated_events||[]).forEach(x=>events.appendChild(makeItemRow(x)));
  if(!events.children.length)events.innerHTML='<div class="empty-state">No events have an established Day / Season / Year date yet.</div>';
}
'''

new_set_view = r'''const APP_VIEWS={
  map:mapView,
  character:sheetView,
  inventory:inventoryView,
  companions:companionsView,
  projects:projectsView,
  calendar:calendarView
};
const VIEW_TITLES={
  map:'Mårék — Known Regional Map',
  character:'Mårék — Character Sheet',
  inventory:'Mårék — Inventory',
  companions:'Mårék — Companions',
  projects:'Mårék — Projects',
  calendar:'Mårék — Campaign Calendar'
};
function viewFromHash(){
  const key=(location.hash||'#map').slice(1).toLowerCase();
  return APP_VIEWS[key]?key:'map';
}
function setAppView(which,{updateHash=true}={}){
  if(!APP_VIEWS[which])which='map';
  Object.entries(APP_VIEWS).forEach(([key,node])=>node.hidden=key!==which);
  optionsMenu.querySelectorAll('[data-app-view]').forEach(b=>b.setAttribute('aria-current',b.dataset.appView===which?'page':'false'));
  if(updateHash)history.replaceState(null,'',`#${which}`);
  document.title=VIEW_TITLES[which]||VIEW_TITLES.map;
  closeOptions();
  if(which==='map'&&typeof setView==='function')requestAnimationFrame(()=>setView());
}'''

old_set_view = r'''function setAppView(which,{updateHash=true}={}){
  const showSheet=which==='character';
  mapView.hidden=showSheet;
  sheetView.hidden=!showSheet;
  optionsMenu.querySelectorAll('[data-app-view]').forEach(b=>b.setAttribute('aria-current',b.dataset.appView===which?'page':'false'));
  if(updateHash)history.replaceState(null,'',showSheet?'#character':'#map');
  document.title=showSheet?'Mårék — Character Sheet':'Mårék — Known Regional Map';
  closeOptions();
  if(!showSheet&&typeof setView==='function')requestAnimationFrame(()=>setView());
}'''

if '</style>' not in text:
    raise RuntimeError('Could not find </style> anchor')
text = text.replace('</style>', css + '\n</style>', 1)

if menu_anchor not in text:
    raise RuntimeError('Could not find Character Sheet menu anchor')
text = text.replace(menu_anchor, menu_replacement, 1)

view_anchor = '''      <div class="sheet-footer-note sheet-note">This sheet is deliberately conservative: it shows established player-safe facts and marks unresolved mechanics instead of importing default PHB values.</div>\n    </section>\n  </main>\n</section>\n\n\n<script>'''
if view_anchor not in text:
    raise RuntimeError('Could not find character sheet / script anchor')
view_replacement = view_anchor[:-len('\n\n<script>')] + views + '\n\n<script>'
text = text.replace(view_anchor, view_replacement, 1)

const_anchor = "const mapView=document.getElementById('map-view');\nconst sheetView=document.getElementById('sheet-view');"
const_replacement = const_anchor + "\nconst inventoryView=document.getElementById('inventory-view');\nconst companionsView=document.getElementById('companions-view');\nconst projectsView=document.getElementById('projects-view');\nconst calendarView=document.getElementById('calendar-view');"
if const_anchor not in text:
    raise RuntimeError('Could not find app view const anchor')
text = text.replace(const_anchor, const_replacement, 1)

close_anchor = 'function closeOptions(){optionsMenu.hidden=true;optionsButton.setAttribute(\'aria-expanded\',\'false\')}'
if close_anchor not in text:
    raise RuntimeError('Could not find closeOptions anchor')
text = text.replace(close_anchor, js_helpers + '\n\n' + close_anchor, 1)

if old_set_view not in text:
    raise RuntimeError('Could not find original setAppView function')
text = text.replace(old_set_view, new_set_view, 1)

old_hash = "window.addEventListener('hashchange',()=>setAppView(location.hash==='#character'?'character':'map',{updateHash:false}));"
new_hash = "window.addEventListener('hashchange',()=>setAppView(viewFromHash(),{updateHash:false}));"
if old_hash not in text:
    raise RuntimeError('Could not find original hashchange handler')
text = text.replace(old_hash, new_hash, 1)

final_anchor = "});\nsetAppView(location.hash==='#character'?'character':'map',{updateHash:false});"
final_replacement = "});\n\nfetch('campaign-tools-state.json').then(r=>r.json()).then(renderCampaignTools).catch(()=>{\n  ['inventory-context','companions-context','projects-context','calendar-status'].forEach(id=>{const n=document.getElementById(id);if(n)n.textContent='Campaign tool data could not be loaded.'});\n});\nsetAppView(viewFromHash(),{updateHash:false});"
if final_anchor not in text:
    raise RuntimeError('Could not find final setAppView anchor')
text = text.replace(final_anchor, final_replacement, 1)

INDEX.write_text(text, encoding='utf-8')
print('Integrated Inventory, Companions, Projects, and Calendar views into docs/index.html')
