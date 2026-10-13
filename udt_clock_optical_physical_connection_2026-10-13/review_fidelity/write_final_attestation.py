"""Bind this context's actual final review after completed correspondence check."""
import datetime
import hashlib
import json
from pathlib import Path

here=Path(__file__).resolve().parent
pkg=here.parent
repo=pkg.parent
freeze_path=pkg/'INTEGRATION_FREEZE.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
checked=json.loads((here/'checks/final_correspondence_01.stdout').read_text())
assert checked['status']=='PASS'
assert sha(freeze_path)==checked['freeze_sha256']
freeze=json.loads(freeze_path.read_text())
report=here/'FINAL_REVIEW.md'
result={
 'context':'/root/coc_review_fidelity',
 'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'verdict':'ACCEPT_WITH_LIMITS',
 'report_path':str(report.relative_to(repo)),
 'report_sha256':sha(report),
 'freeze_path':str(freeze_path.relative_to(repo)),
 'freeze_sha256':sha(freeze_path),
 'scope':'Actual source-first/direct/repair/exposed final physical-fidelity review of conditional COC1 integration; unchanged inherited corpus retains prior source-relative review, not reproof.',
 'model':'Inherited parent model; exposed Codex/GPT-6 runtime; more precise serving identifier not independently verified. Not cross-model review.',
 'independence':{'context':'fresh separate at source-first stage','argument':'independent source-first reconstruction then exposed review','implementation':'independently authored exact controls and final correspondence check','libraries':'shared Python/SymPy','human_or_formal':'UNTESTED'},
 'pending':['Normal development verifier after actual review binding','57 maintenance checks','Full406 premise audit','Staging/commit/publication and remote correspondence'],
 'accepted_sha256':freeze['accepted_sha256']}
with (here/'FINAL_ATTESTATION.json').open('x') as f:
 json.dump(result,f,indent=2)
 f.write('\n')
print(json.dumps({'status':'WRITTEN','verdict':result['verdict'],'report_sha256':result['report_sha256'],
 'accepted_count':len(result['accepted_sha256']),'attestation_sha256':sha(here/'FINAL_ATTESTATION.json')}))
