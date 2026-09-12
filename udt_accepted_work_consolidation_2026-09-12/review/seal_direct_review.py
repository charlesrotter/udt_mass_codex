#!/usr/bin/env python3
"""Pin the grouped direct review before the authorized candidate correction."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess

HERE=Path(__file__).resolve().parent
PKG=HERE.parent
ROOT=PKG.parent
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
freeze=json.loads((PKG/'INITIAL_FREEZE.json').read_text())
for e in freeze['files']:
    assert digest(ROOT/e['original_path'])==digest(PKG/e['snapshot'])==e['sha256'],e
for seal in ('SOURCE_FIRST_SEAL.json','SUPPLEMENTAL_SOURCE_SEAL.json'):
    for e in json.loads((HERE/seal).read_text())['files']:
        assert digest(ROOT/e['path'])==e['sha256'],e['path']
evidence=json.loads((HERE/'DIRECT_CORRESPONDENCE.json').read_text())
sources=evidence['direct_stage_source_additions']
for p in ('udt_quiet_correspondence_campaign_2026-09-10/DECISION_BRIEF.md',
 'udt_g333_metric_native_initial_pair_response_2026-09-03/AUDIT_REPORT.md',
 'udt_g337_double_silent_third_normal_ownership_2026-09-03/AUDIT_REPORT.md'):
    sources.append({'path':p,'sha256':digest(ROOT/p),
      'read_depth':'full controlling brief/audit after parent editorial proposal; original proof/suite not reopened'})
for e in sources:
    assert digest(ROOT/e['path'])==e['sha256']
    baseline=subprocess.check_output(['git','show',freeze['source_baseline']+':'+e['path']],cwd=ROOT)
    assert hashlib.sha256(baseline).hexdigest()==e['sha256'],e['path']
names=['DIRECT_REVIEW.md','DIRECT_CORRESPONDENCE.json','direct_correspondence.py',
 'direct_correspondence_continuation.py','seal_direct_review.py']
for stem in ('direct_correspondence_capture','direct_continuation_capture'):
    names += [stem+s for s in ('.json','.stdout','.stderr','.capture_provenance.json')]
files=[HERE/n for n in names]+[PKG/'INITIAL_FREEZE.json']+[PKG/e['snapshot'] for e in freeze['files']]
result={'sealed_utc':datetime.now(timezone.utc).isoformat(),
 'verdict':'ACCEPT_WITH_DOCUMENTARY_CORRECTIONS__SCIENTIFIC_SCOPE_RETAINED',
 'reviewer_context':'/root/cwa1_consolidation_review','runtime_model_version':'UNATTESTED',
 'different_model':'NOT_ESTABLISHED','allocation':'same one separate context; no override or subdelegation',
 'candidate_exposure':'initial candidate after both source-only seals; later parent QC/G333/G337 editorial proposal disclosed',
 'candidate_correction_cycles_used':0,'scientific_candidate_defects_found':0,
 'documentary_items':['D1 exposure underreport','D2 explicit accepted-cluster credit','D3 next-question reuse gate'],
 'direct_stage_source_additions':sources,
 'files':[{'path':str(p.relative_to(ROOT)),'sha256':digest(p)} for p in files]}
with (HERE/'DIRECT_REVIEW_SEAL.json').open('x') as f:
    json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({'sealed_utc':result['sealed_utc'],'verdict':result['verdict'],
 'direct_review_sha256':result['files'][0]['sha256'],'files':len(files),'direct_source_additions':len(sources)}))
