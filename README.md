# Mårék Live Map

Player-safe live regional map and campaign tools for the Mårék campaign.

## Authority

Private campaign authority: **Mershmen83/M-r-k-full-gm-saves** (paired with **Mershmen83/M-r-k-full-gm-engine**).  
Current derived basis: **canonical save/history**.

The public repository contains only information Mårék is allowed to know in-world. Unknown bearings, unresolved identities, hidden GM state, and meta/OOC-only facts stay private.

## Current player tools

- Map
- Character Sheet
- Inventory
  - Mårék — Carried Inventory
  - Extra Inventory / Recovered Property
  - Hask / Mount Inventory
  - With Others / Gifts & Loans
  - Known Not Carried
- Companions
- Projects
- Calendar

## Map doctrine

- Show only Mårék-known geography.
- Unknown bearings stay unknown.
- Reported/unvisited places remain visibly distinct from observed places.
- The mapped region grows through play.
- Roads render as winding, terrain-following routes where supported.
- Schematic coordinates are rendering aids, not new canon.
- Current scene/provenance derives from the private GM GitHub authority, not Dropbox.
- After **The Break**, remembered Crown-route geography may remain visible while timing, force scale, transit/tunnel interpretation and unsupported route details are treated as memory under correction rather than fresh physical verification.

## Current scope

The current canonical live state places Mårék and the party on **open ground immediately outside Northern Regional Command**, already in a hard mounted escape after the false-continuity rupture known as **The Break**. The former Journey Day 13 framing is no longer reliable, and the corrected elapsed-time count has not yet been established to Mårék in-scene. The exact current daypart/clock and corrected season/date remain unresolved.

The public map still renders the player-known northern campaign chain using explicitly **schematic** coordinates where exact bearings/distances were never established. After The Break, those northern links also represent Mårék's remembered geography where physical route/timing details have not yet been reverified. Renderer placement never creates new geographic canon.

Player-known map/state material includes:

- Dāren Ford and the west-road investigation chain;
- Rell Quarry and the old Crown Road pursuit through Draelan, Split Cairn, the Crown-road ruin and Ridge Watch-Fort;
- Stone Gate, Greyhook, Rook's Span, Northwatch, Cairnwatch, Harrow, Vantage Hold, House Seven, IVS-3 and Northern Regional Command as places Mårék remembers reaching;
- The Break at N.R.C., including Mårék's discovery that major parts of the Crown-route chronology, force scale and detention picture were not physically what he had believed;
- the party's current mounted escape from N.R.C.;
- explicit schematic/continuity warnings anywhere the saves no longer support literal route, timing, force or site-state conclusions.

The player-safe site deliberately does **not** publish the still-unspoken corrected travel-day total, the future westward break, Realm Two destination data, or other private/OOC-only conclusions Mårék has not yet learned in-world.

## Files

- `docs/index.html` — single current interactive player site.
- `docs/map-state.json` — current player-safe structured map state.
- `docs/character-state.json` — current player-safe character export.
- `docs/campaign-tools-state.json` — current player-safe inventory/companions/projects/calendar export.
- `.github/workflows/deploy-pages.yml` — GitHub Pages deployment.

The page reads the three JSON state files directly. Historical map render versions and one-time integration scripts are not retained in the active tree.

## Current continuity-export note

The character and campaign-tools panels are refreshed from current player-known save/history state. Older observed geography remains useful historical map content, but The Break means the northern Crown chain must now be read partly as remembered continuity rather than guaranteed literal physical route/timing history. Unsupported bearings, distances, transit interpretations and force details remain unresolved until post-break evidence re-establishes them.

The page reads the current JSON state files directly. No historical checkpoint or integration-script provenance is required.
