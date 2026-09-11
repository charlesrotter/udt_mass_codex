#!/usr/bin/env python3
"""Authenticate exact selected source rows, full old registry, and science pins."""
import csv
import hashlib
import io
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
PKG=ROOT/'udt_two_shape_nonlinear_interaction_2026-09-11'
BASE='ba934a9b542f818c9032ad37d57b8f7470fe9c9b'
raw=(ROOT/'CURRENT_SCIENTIFIC_PREMISES.tsv').read_bytes()
prior=subprocess.check_output(['git','show',BASE+':CURRENT_SCIENTIFIC_PREMISES.tsv'],cwd=ROOT)
new=[line for line in raw.splitlines(keepends=True) if line.startswith(b'G413\t')]
old=b''.join(line for line in raw.splitlines(keepends=True) if not line.startswith(b'G413\t'))
assert len(new)<=1 and old==prior
rows={row['premise_id']:row for row in csv.DictReader(io.StringIO(old.decode()),delimiter='\t')}
assert len(rows)==395
saved=json.loads((PKG/'SOURCE_REGISTRY_ROWS.json').read_text())
selected=saved['rows']
if isinstance(selected,list):
    selected={r['premise_id']:r for r in selected}
assert len(selected)==13
for pid,expected in selected.items():
    assert rows[pid]==expected,('source row changed',pid)
assert hashlib.sha256(old).hexdigest()==saved['registry_sha256']
assert 'GR_FILTER_ONLY_NOT_RESPONSE_LAW_INPUT' in rows['G312']['current_status']
assert 'WORKING_FOUNDATIONAL_CLARIFICATION_NOT_CANON' in rows['G176']['current_status']
assert 'GENERAL_3PLUS1_ASSEMBLY_CONDITIONAL' in rows['G166']['current_status']
grade='BANKED_DERIVED_CONDITIONAL__VERIFIED_WITH_CAVEATS__OWNER_AUTHORIZED__NOT_PHYSICAL_ADOPTION__NOT_CANON'
for pid in ('G388','G389','G394','G405'):
    assert rows[pid]['current_status']==grade

pins=json.loads((PKG/'SOURCE_PINS.json').read_text())['sha256']
science={name:want for name,want in pins.items()
         if name not in ('AGENTS.md','CURRENT_SCIENTIFIC_PREMISES.tsv','CURRENT_SCIENTIFIC_PREMISES.md')}
for name,want in science.items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==want,name

print(json.dumps({'status':'PASS','baseline':BASE,'original395_exact_bytes':True,
 'old_registry_sha256':hashlib.sha256(old).hexdigest(),'g413_present':len(new)==1,
 'selected_original_rows':sorted(selected),'scientific_and_capture_source_pins':science,
 'source_grades':{pid:rows[pid]['current_status'] for pid in ('G388','G389','G394','G405')},
 'meaning':'correspondence and reviewed interfaces, not reproof or physical adoption'},indent=2))
