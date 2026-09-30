import json
from pathlib import Path

map_path = Path('docs/map-state.json')
data = json.loads(map_path.read_text(encoding='utf-8'))

data['current_position'] = {
    'feature': 'nrc',
    'state': 'Open ground immediately outside Northern Regional Command; post-Break corrected date/daypart/clock unresolved; Mårék, Aren, Kerr and Seyra are mounted and riding hard away from N.R.C.; Véľ runs alongside; Trinket is with the fleeing group.'
}
data.setdefault('authority', {})['truth_layer_note'] = (
    'Northern Crown-route geography remains player-known/remembered, but route timing, force scale, detention state, site control and other details exposed by The Break are not present physical truth unless reverified.'
)

target_ids = {
    'stone-gate', 'greyhook', 'rooks-span', 'northwatch',
    'cairnwatch', 'harrow', 'vantage-hold', 'house-seven',
    'ivs-3', 'nrc'
}

for feature in data.get('features', []):
    if not isinstance(feature, dict) or feature.get('id') not in target_ids:
        continue
    fid = feature.get('id')
    if fid == 'nrc':
        feature['continuity_status'] = 'mixed_current_anchor_and_remembered_site_state'
        feature['known_facts'] = [
            'Current post-Break anchor: the party reached the N.R.C. Drāv stables and is now fleeing from open ground immediately outside the installation.',
            'Current post-Break fact: Crown systems at N.R.C. continued to authenticate Mårék during The Break.',
            'Remembered continuity — not post-Break reverified: older archive, custody, force, detainee and command-transfer details require re-verification wherever they conflict with The Break.',
            'The Break established that major parts of Mårék’s prior Crown-route chronology, force scale and detention picture were not physically what he had believed.'
        ]
    else:
        feature['continuity_status'] = 'remembered_not_post_break_reverified'
        feature['known_facts'] = [
            fact if str(fact).startswith('Remembered continuity')
            else 'Remembered continuity — not post-Break reverified: ' + str(fact)
            for fact in feature.get('known_facts', [])
        ]

def rewrite_strings(obj):
    if isinstance(obj, dict):
        return {k: rewrite_strings(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [rewrite_strings(v) for v in obj]
    if not isinstance(obj, str):
        return obj
    replacements = {
        'Day-13 northern Crown campaign chain': 'Remembered northern Crown campaign chain',
        'observed_day13_northern_transit_sequence_schematic_position': 'remembered_northern_transit_sequence_schematic_position',
        'Journey Day 13 northern Crown-transit campaign': 'remembered northern Crown-transit campaign sequence',
        'Journey Day 13 after Cairnwatch in the campaign sequence': 'the remembered northern Crown-campaign sequence after Cairnwatch',
        'Journey Day 13 after Harrow in the campaign sequence': 'the remembered northern Crown-campaign sequence after Harrow',
        'Day-13 northern site sequence': 'remembered northern site sequence',
        'Day-13 campaign sites': 'remembered northern campaign sites'
    }
    out = obj
    for old, new in replacements.items():
        out = out.replace(old, new)
    return out

data = rewrite_strings(data)
map_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
