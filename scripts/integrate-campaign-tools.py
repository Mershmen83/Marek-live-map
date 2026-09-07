from pathlib import Path
import json

INDEX = Path('docs/index.html')
MAP = Path('docs/map-state.json')

text = INDEX.read_text(encoding='utf-8')

# CP100 inventory UI reconciliation. Idempotent upgrades for an already-integrated page.
text = text.replace('Player-safe carried and recently recovered items · unknown totals stay unknown',
                    'Player-safe carried, extra, mount, and recovered inventory · unknowns stay unknown')
text = text.replace('<h2>Established Carried Gear</h2>', '<h2>Mårék — Carried Inventory</h2>')
text = text.replace('<h2>Recent Recovered Items</h2>', '<h2>Extra Inventory / Recovered Property</h2>')

if 'id="inventory-mount"' not in text:
    anchor = '''        <section class="tool-section" style="grid-column:1/-1">
          <h2>Still Unresolved</h2>
          <ul id="inventory-unresolved" class="sheet-list unknown-list"></ul>
        </section>'''
    addition = '''        <section class="tool-section">
          <h2>Hask / Mount Inventory</h2>
          <div id="inventory-mount" class="item-stack"></div>
        </section>
        <section class="tool-section">
          <h2>With Others / Gifts & Loans</h2>
          <div id="inventory-with-others" class="item-stack"></div>
        </section>
        <section class="tool-section" style="grid-column:1/-1">
          <h2>Known Not Carried</h2>
          <div id="inventory-not-carried" class="item-stack"></div>
        </section>
''' + anchor
    if anchor not in text:
        raise RuntimeError('Could not find inventory unresolved section anchor')
    text = text.replace(anchor, addition, 1)

text = text.replace('(state.inventory?.recent_recovered||[]).forEach(x=>recovered.appendChild(makeItemRow(x)));',
                    '(state.inventory?.extra_inventory||state.inventory?.recent_recovered||[]).forEach(x=>recovered.appendChild(makeItemRow(x)));')
text = text.replace("if(!recovered.children.length)recovered.innerHTML='<div class=\"empty-state\">No recent recovered items are currently listed.</div>';",
                    "if(!recovered.children.length)recovered.innerHTML='<div class=\"empty-state\">No extra or recovered inventory is currently listed.</div>';")

if "const mountInv=document.getElementById('inventory-mount')" not in text:
    marker = "  const invUnknown=document.getElementById('inventory-unresolved');invUnknown.innerHTML='';"
    block = '''  const mountInv=document.getElementById('inventory-mount');mountInv.innerHTML='';
  (state.inventory?.mount_inventory||[]).forEach(x=>mountInv.appendChild(makeItemRow(x)));
  if(!mountInv.children.length)mountInv.innerHTML='<div class="empty-state">No separate mount inventory is currently listed.</div>';

  const withOthers=document.getElementById('inventory-with-others');withOthers.innerHTML='';
  (state.inventory?.with_others||[]).forEach(x=>withOthers.appendChild(makeItemRow(x)));
  if(!withOthers.children.length)withOthers.innerHTML='<div class="empty-state">No tracked gifts, loans, or items held by others are currently listed.</div>';

  const notCarried=document.getElementById('inventory-not-carried');notCarried.innerHTML='';
  (state.inventory?.known_not_carried||[]).forEach(x=>notCarried.appendChild(makeItemRow(x)));
  if(!notCarried.children.length)notCarried.innerHTML='<div class="empty-state">No separately tracked left-behind property is currently listed.</div>';

''' + marker
    if marker not in text:
        raise RuntimeError('Could not find inventory renderer marker')
    text = text.replace(marker, block, 1)

INDEX.write_text(text, encoding='utf-8')

# Keep map provenance/checkpoint aligned with CP100. No fictional geography changes here.
state = json.loads(MAP.read_text(encoding='utf-8'))
authority = state.setdefault('authority', {})
authority['source'] = 'Private GM authority Mershmen83/M-r-k-full-gm-campaign through CP100; public map contains Mårék-known facts only'
authority['checkpoint'] = 'CP100'
MAP.write_text(json.dumps(state, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')

print('CP100 campaign tools/map provenance reconciliation complete.')
