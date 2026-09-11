#!/usr/bin/env python3
"""Read-only source/candidate correspondence; does not establish science/chronology."""
import csv
import hashlib
import json
import pathlib
import subprocess
import datetime

root=pathlib.Path(__file__).resolve().parents[2]
package=root/'udt_two_shape_nonlinear_interaction_2026-09-11'
review=package/'review'
checks={}
for manifest,base in [(package/'SOURCE_PINS.json',root),(package/'CANDIDATE_FREEZE.json',package),
                      (review/'STAGE_A_SEAL.json',root)]:
    pins=json.loads(manifest.read_text())['sha256']
    for name,expected in pins.items():
        actual=hashlib.sha256((base/name).read_bytes()).hexdigest()
        if actual!=expected:raise AssertionError((str(manifest),name,actual,expected))
    checks[str(manifest.relative_to(root))]=len(pins)
snapshot=json.loads((package/'SOURCE_REGISTRY_ROWS.json').read_text())
current={row['premise_id']:row for row in csv.DictReader((root/'CURRENT_SCIENTIFIC_PREMISES.tsv').open(),delimiter='\t')}
saved=snapshot['rows']
if isinstance(saved,dict):saved=list(saved.values())
for row in saved:
    if current[row['premise_id']]!=row:raise AssertionError(('registry row',row['premise_id']))
branch=subprocess.check_output(['git','branch','--show-current'],cwd=root,text=True).strip()
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
if branch!='grok' or head!='b318072a9403d6acdd3a6d5749e1b366d76d29c5':raise AssertionError(('branch/head',branch,head))
status=subprocess.check_output(['git','-c','core.preloadIndex=false','-c','index.threads=1','status','--short'],cwd=root,text=True)
original='\n'.join(line for line in status.splitlines() if not line.endswith('udt_two_shape_nonlinear_interaction_2026-09-11/'))+'\n'
statushash=hashlib.sha256(original.encode()).hexdigest()
if statushash!='55e7c4508622f912730f9c068cc571c370b3977bc1110eb0a48a8218dbe024c2':raise AssertionError(('original names/status fingerprint',statushash))
out={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'branch':branch,'head':head,
 'matched_manifests':checks,'matched_registry_ids':[r['premise_id'] for r in saved],
 'original_untracked_status_count':len(original.splitlines()),'original_status_fingerprint':statushash,
 'meaning':'Byte correspondence and names/status preservation, not protected-payload validation, scientific proof or chronology'}
print(json.dumps(out,indent=2))
