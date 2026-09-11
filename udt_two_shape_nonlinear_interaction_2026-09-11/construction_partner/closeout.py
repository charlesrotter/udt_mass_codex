#!/usr/bin/env python3
"""Correspondence/preservation check; not a scientific proof or result promotion."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess

root=Path(__file__).resolve().parents[2]
here=Path(__file__).resolve().parent
inputs=json.loads((here/'inputs_serial.stdout').read_text())
source_checks=[]
for p,expected in inputs['source_pins'].items():
    actual=hashlib.sha256((root/p).read_bytes()).hexdigest()
    source_checks.append({'path':p,'expected':expected,'actual':actual,'match':actual==expected})
assert all(v['match'] for v in source_checks)
bank=root/'udt_reviewed_backlog_banking_2026-09-10/BANKED_CLAIMS.json'
banked=json.loads(bank.read_text())
selected=[row for row in banked['claims'] if row['premise_id'] in {'G388','G389','G394'}]
banked_checks=[]
for row in selected:
    for artifact in row['artifacts']:
        path=artifact['path']
        actual=hashlib.sha256((root/path).read_bytes()).hexdigest()
        banked_checks.append({'premise_id':row['premise_id'],'path':path,
             'expected':artifact['sha256'],'actual':actual,'match':actual==artifact['sha256']})
assert all(v['match'] for v in banked_checks)
capture_outcomes={}
for stem in ['inputs','inputs_serial','raw_geometry_initial','mutant_omit_axial','mutant_freeze_second_time']:
    capture_outcomes[stem]=json.loads((here/(stem+'.json')).read_text())
assert capture_outcomes['raw_geometry_initial']['returncode']==0
assert capture_outcomes['mutant_omit_axial']['returncode']==1
assert capture_outcomes['mutant_freeze_second_time']['returncode']==1
raw=json.loads((here/'raw_geometry_initial.stdout').read_text())
assert raw['status']=='PASS'
paths=sorted(p for p in here.iterdir() if p.is_file() and not p.name.startswith('closeout.'))
manifest={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
manifest[str(Path(__file__).relative_to(root))]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
print(json.dumps({'status':'PASS','completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'context':'/root/two_shape_construction','model_runtime':'UNATTESTED',
 'HEAD':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
 'tracked_diff_names':subprocess.check_output(['git','-c','core.preloadIndex=false','-c','index.threads=1','diff','--name-only'],cwd=root,text=True).splitlines(),
 'original_input_checks':source_checks,'banked_claim_correspondence':banked_checks,
 'banked_claims_sha256':hashlib.sha256(bank.read_bytes()).hexdigest(),
 'capture_outcomes':capture_outcomes,'construction_manifest':manifest,
 'review_state':'UNREVIEWED_CONSTRUCTION; separate adversarial review parent-owned',
 'omissions':'No new premise audit, upstream package replay, formal CK proof, record-join verification or promotion'},indent=2))
