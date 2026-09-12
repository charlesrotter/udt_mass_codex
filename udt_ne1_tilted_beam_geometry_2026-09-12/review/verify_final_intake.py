#!/usr/bin/env python3
"""Prepublication correspondence checks only, not scientific proof or timeless replay."""
from pathlib import Path
import json
import hashlib
import subprocess
import datetime

r=Path('udt_ne1_tilted_beam_geometry_2026-09-12')
p=r/'REVIEW_INTAKE.json'
assert hashlib.sha256(p.read_bytes()).hexdigest()=='599dbb132cb5304cbe97fa21f071a47dc3df284528fa2d1acd224260af1b86ab'
d=json.loads(p.read_text())
assert all(hashlib.sha256(Path(k).read_bytes()).hexdigest()==v for block in ('files','navigation') for k,v in d[block].items())
pins=json.loads((r/'SOURCE_PINS.json').read_text()); nav=set(d['navigation'])
assert all(hashlib.sha256(Path(k).read_bytes()).hexdigest()==v for k,v in pins.items() if k not in nav)
launch=json.loads((r/'LAUNCH.json').read_text())
status=subprocess.check_output(['git','status','--short'],text=True).splitlines()
assert all(x in status for x in launch['original_status_entries'])
assert set(subprocess.check_output(['git','diff','--name-only'],text=True).splitlines())==nav
assert subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()==''
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==launch['head']
assert subprocess.check_output(['git','rev-parse','origin/grok'],text=True).strip()==launch['head']
assert subprocess.check_output(['git','branch','--show-current'],text=True).strip()=='grok'
cap=json.loads((r/'checks/navigation_verified.json').read_text())
out=(r/'checks/navigation_verified.stdout').read_text()
assert cap['returncode']==0 and not cap['timeout'] and '359 passed, 1 deselected' in out
pres=json.loads((r/'NAVIGATION_AND_PRESERVATION.json').read_text())
assert pres['navigation_execution']==cap and pres['navigation_stdout']==out
seal=json.loads((r/'review/SOURCE_FIRST_OUTCOMES_SEAL.json').read_text())
assert all(hashlib.sha256(Path(k).read_bytes()).hexdigest()==v for k,v in seal['files'].items())
print(json.dumps(dict(status='PASS',checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    intake_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),core_hashes=len(d['files']),
    navigation_hashes=len(nav),unchanged_other_source_pins=len(pins)-len(nav),
    original_untracked_entries=len(launch['original_status_entries']),
    navigation_selected_passes=359,navigation_deselected=1,head=launch['head'],
    branch='grok',staged_paths=[],scope='Prepublication byte/status correspondence; no scientific proof or backup assertion.'),indent=2))
