"""Source-first pins and authorized current-byte delta; no author imports."""
import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess

REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parents[1]
BASE = 'a9896cb190e9c4aa8fd8a317cfaaa942d64e0a19'
ALLOW = {
    'LIVE.md', 'HANDOFF.md', 'CURRENT_RESEARCH_PROGRAM.md',
    'CURRENT_SCIENTIFIC_PREMISES.md', 'INDEX.md', 'MEMORY.md',
    'CURRENT_SCIENTIFIC_PREMISES.tsv', 'verify_current_scientific_premises.py',
    'tests/test_startup_surface.py',
}

def digest(data):
    return hashlib.sha256(data).hexdigest()

def historical(path):
    p = subprocess.run(['git', '-c', 'core.preloadIndex=false', '-c',
        'index.threads=1', 'show', f'{BASE}:{path}'], cwd=ROOT,
        capture_output=True, check=True, timeout=10)
    return p.stdout

pins = list(csv.DictReader((REVIEW / 'SOURCE_FIRST_PINS.tsv').open(), delimiter='\t'))
assert len(pins) == len({r['path'] for r in pins}) == 29
changed = []
for row in pins:
    assert row['baseline'] == BASE
    assert digest(historical(row['path'])) == row['sha256'], row['path']
    if digest((ROOT / row['path']).read_bytes()) != row['sha256']:
        assert row['path'] in ALLOW, ('unallowed source change', row['path'])
        changed.append(row['path'])
assert digest((REVIEW / 'SOURCE_FIRST_REQUIREMENTS.md').read_bytes()) == \
    'd5cd2c96152a60ee5c4ee4af0f852f64a330b82441a3bf41df12aab494fd4c7f'
assert digest((REVIEW / 'SOURCE_FIRST_PINS.tsv').read_bytes()) == \
    'baa3880e058ef45d42e886d59287a843678f155185ffb29210cf146a3f0c3c30'
assert (REVIEW / 'run_capture.py').read_bytes() == \
    (ROOT / 'udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py').read_bytes()

old = historical('CURRENT_SCIENTIFIC_PREMISES.tsv')
now = (ROOT / 'CURRENT_SCIENTIFIC_PREMISES.tsv').read_bytes()
oldrows = list(csv.DictReader(io.StringIO(old.decode()), delimiter='\t'))
newrows = list(csv.DictReader(io.StringIO(now.decode()), delimiter='\t'))
assert len(oldrows) == len(newrows) == 365
assert list(oldrows[0]) == list(newrows[0])
assert [r['premise_id'] for r in oldrows] == [r['premise_id'] for r in newrows]
changed_cells = []
for a, b in zip(oldrows, newrows):
    for key in a:
        if a[key] != b[key]:
            assert a['premise_id'] == 'G312', (a['premise_id'], key)
            assert key not in ('premise_id', 'term', 'epistemic_label'), key
            changed_cells.append(key)
assert b''.join(x for x in old.splitlines(keepends=True) if not x.startswith(b'G312\t')) == \
    b''.join(x for x in now.splitlines(keepends=True) if not x.startswith(b'G312\t'))
print(json.dumps({'status': 'PASS', 'baseline': BASE, 'source_pins': len(pins),
    'source_first_seal': 'CORRESPONDENCE_VERIFIED', 'changed_sources': changed,
    'registry_rows': 365, 'g312_changed_cells': changed_cells,
    'other_registry_rows_byte_identical': True,
    'meaning': 'documentary correspondence only; no proof or full365 pass'}, indent=2))
