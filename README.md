# Mårék Live Map

Player-safe live regional map for the Mårék campaign.

## Purpose

This repository publishes only geography and travel information Mårék currently knows. It is intentionally separate from the private campaign-system repository so hidden/GM-side material never needs to be exposed.

## Map doctrine

- Show only Mårék-known geography.
- Unknown bearings stay unknown.
- The mapped region grows through play.
- Roads render as winding, terrain-following routes rather than straight lines.
- Layout is deliberately asymmetrical.
- Schematic coordinates are rendering aids, not new canon.
- Dropbox LIVE campaign masters remain the authority.

## Files

- `docs/index.html` — mobile-friendly interactive map.
- `docs/map-state.json` — player-safe structured map state.
- `.github/workflows/deploy-pages.yml` — GitHub Pages deployment.

## Expected Pages URL

Once this repository is public and GitHub Pages has deployed successfully:

`https://mershmen83.github.io/Marek-live-map/`

## Current scope

Placed only where direction is established:

- Kareth
- Kareth Quarry
- Candidate Avelin Site
- Saddle Ridge
- Avelin

Valek remains intentionally unpinned because its exact compass bearing from Kareth is still unknown. Its known route chain is shown separately as Kareth → Low Ridge → Stone-bottomed Stream Crossing → Valek.
