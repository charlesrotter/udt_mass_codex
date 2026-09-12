#!/usr/bin/env python3
"""Seal this same-context source-only supplement; preserve the initial seal."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
names=('SUPPLEMENTAL_SOURCE_ONLY.md','SUPPLEMENTAL_SOURCE_PINS.json',
 'SUPPLEMENTAL_READ_DEPTH.tsv','supplemental_pin_check.py','supplemental_pin_capture.json',
 'supplemental_pin_capture.stdout','supplemental_pin_capture.stderr',
 'supplemental_pin_capture.capture_provenance.json','seal_supplemental_source.py',
 'SOURCE_FIRST_SEAL.json')
capture=json.loads((HERE/'supplemental_pin_capture.json').read_text())
assert capture['returncode']==0 and capture['timeout'] is False
assert (HERE/'supplemental_pin_capture.stderr').read_bytes()==b''
initial=json.loads((HERE/'SOURCE_FIRST_SEAL.json').read_text())
for e in initial['files']:
    assert hashlib.sha256((ROOT/e['path']).read_bytes()).hexdigest()==e['sha256'],e['path']
receipt={'sealed_utc':datetime.now(timezone.utc).isoformat(),
 'reviewer_context':'/root/cwa1_consolidation_review','allocation':'same first reviewer context; no additional allocation',
 'first_clock':'2026-09-12T16:11:54+00:00','supplement_observed_from':'2026-09-12T16:21:15+00:00',
 'parent_overlap':'parent independently continued broader accepted-lane source work during this source-only supplement',
 'parent_candidate_exposure':'NONE; parent supplied source ranges and G178 overlay pointer only',
 'runtime_model_version':'UNATTESTED','different_model':'NOT_ESTABLISHED',
 'scientific_replays':0,'full_suite_replays':0,'original_seal_files_unchanged':len(initial['files']),
 'actual_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
 'files':[{'path':str((HERE/n).relative_to(ROOT)),'sha256':hashlib.sha256((HERE/n).read_bytes()).hexdigest()} for n in names]}
with (HERE/'SUPPLEMENTAL_SOURCE_SEAL.json').open('x') as f:
    json.dump(receipt,f,indent=2);f.write('\n')
print(json.dumps({'sealed_utc':receipt['sealed_utc'],'note_sha256':receipt['files'][0]['sha256'],
 'files':len(names),'parent_candidate_exposure':'NONE','original_seal_unchanged':True}))
