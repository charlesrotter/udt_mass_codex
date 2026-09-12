#!/usr/bin/env python3
"""Seal exact final-fidelity verdict; no approval of future publication bytes."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

HERE=Path(__file__).resolve().parent
PKG=HERE.parent
ROOT=PKG.parent
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
freeze=json.loads((PKG/'CORRECTED_REVIEW_FREEZE.json').read_text())
for p,h in freeze['files'].items():
    assert digest(ROOT/p)==h,p
for name in ('SOURCE_FIRST_SEAL.json','SUPPLEMENTAL_SOURCE_SEAL.json','DIRECT_REVIEW_SEAL.json'):
    for e in json.loads((HERE/name).read_text())['files']:
        assert digest(ROOT/e['path'])==e['sha256'],e['path']
capture=json.loads((HERE/'final_correspondence_capture.json').read_text())
assert capture['returncode']==0 and capture['timeout'] is False
assert (HERE/'final_correspondence_capture.stderr').read_bytes()==b''
names=('FINAL_FIDELITY.md','FINAL_CORRESPONDENCE.json','final_correspondence.py',
 'final_correspondence_capture.json','final_correspondence_capture.stdout',
 'final_correspondence_capture.stderr','final_correspondence_capture.capture_provenance.json',
 'seal_final_fidelity.py')
files=[HERE/n for n in names]+[PKG/'CORRECTED_REVIEW_FREEZE.json',PKG/'checks/navigation_review.diff',PKG/'checks/preintegration_sync.json']
for stem in ('corrected_correspondence','navigation_final'):
    files += [PKG/'checks'/(stem+s) for s in ('.json','.stdout','.stderr','.capture_provenance.json')]
result={'sealed_utc':datetime.now(timezone.utc).isoformat(),
 'verdict':'ACCEPT_CWA1_SOURCE_PRESERVING_CONSOLIDATION_WITH_STATED_LIMITS',
 'reviewer_context':'/root/cwa1_consolidation_review',
 'allocation':'same ONE context; no override or subdelegation; single grouped documentary correction',
 'runtime_model_version':'UNATTESTED','different_model':'NOT_ESTABLISHED',
 'unresolved_load_bearing_objections':[],'candidate_scientific_repairs':0,'candidate_documentary_cycles':1,
 'corrected_target_files':freeze['files'],'publication':'NOT_CLAIMED_COMPLETED; later parent-owned receipts not reviewed',
 'actual_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
 'files':[{'path':str(p.relative_to(ROOT)),'sha256':digest(p)} for p in files]}
with (HERE/'FINAL_FIDELITY_SEAL.json').open('x') as f:
    json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({'sealed_utc':result['sealed_utc'],'verdict':result['verdict'],
 'final_fidelity_sha256':result['files'][0]['sha256'],'review_receipt_files':len(files),
 'corrected_target_files':len(freeze['files']),'unresolved_objections':0}))
