# Mårék Live Map

Player-safe live regional map and campaign tools for the Mårék campaign.

## Authority

Private campaign authority: **Mershmen83/M-r-k-full-gm-saves** (paired with **Mershmen83/M-r-k-full-gm-engine**).  
Current derived checkpoint: **CP106**.

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

## Current scope

CP106 places Mårék inside **Northern Regional Command**, Journey Day 13, at the old Warden Command Reserve. The exact present daypart/clock is unresolved. The public map now renders the player-known northern campaign chain using explicitly **schematic** coordinates where exact bearings/distances were never established. Renderer placement never creates new geographic canon.

Player-known map/state additions include:

- Dāren Ford now reached and observed;
- south ferry yard / Meln contact area;
- old Dāren Rask-associated stash shed;
- Deren's east-river freight house;
- west-river warehouse reached by Deren's dark-coated contact;
- **Rell Quarry** as a visited Journey Day 5 location, with the old Crown Road pursuit extended through Draelan, Split Cairn, the underground Crown-road ruin and Ridge Watch-Fort;
- Stone Gate → Greyhook → Rook's Span → Northwatch and the Journey Day 13 northern Crown campaign chain through Cairnwatch, Harrow, Vantage Hold, House Seven, IVS-3 and Northern Regional Command;
- explicit schematic-route warnings anywhere the saves preserve travel/order but not exact compass bearing, distance or surface geometry.

The player-safe site deliberately does **not** publish private/OOC-only conclusions that Mårék has not yet earned in-world.

## Files

- `docs/index.html` — mobile-friendly interactive player site.
- `docs/map-state.json` — player-safe structured map state.
- `docs/character-state.json` — player-safe character state.
- `docs/campaign-tools-state.json` — player-safe inventory, companions, projects and calendar state.
- `.github/workflows/deploy-pages.yml` — GitHub Pages deployment.


## CP106 continuity-export note

The character and campaign-tools panels are refreshed from player-known CP106 state. Older observed geography remains valid historical map content. The northern Crown chain is now assigned renderer coordinates only as a player-safe schematic export; explicit route order/directions remain canon, while unsupported bearings/distances remain unknown. The integration script derives provenance from the current player-safe tools export and must never hardcode an older checkpoint.
