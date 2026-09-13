#!/usr/bin/env python3
"""Read-only source/history/replay correspondence; no scientific propagation."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,math,platform

R=Path(__file__).resolve().parent;P=R.parent;root=P.parent
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
checked={}
for filename,renamed in [('CANDIDATE_FREEZE.json','INITIAL_check_discrimination.py'),
                        ('SYMBOLIC_REPAIR_FREEZE.json','SIMPLIFIER_REPAIRED_check_discrimination.py'),
                        ('COMPLETE_CAPTURE_AMENDMENT.json','check_discrimination.py')]:
    for path,want in json.loads((P/filename).read_text())['sha256'].items():
        target=P/renamed if path.endswith('/check_discrimination.py') else root/path
        assert digest(target)==want,(filename,path)
        checked[str(target.relative_to(root))]=want
for filename in [P/'SOURCE_PINS.json',P/'MAGNITUDE_SUPPLEMENT_FREEZE.json',
                 R/'SOURCE_FIRST_SEAL.json',R/'DIRECT_REVIEW_SEAL.json']:
    for path,want in json.loads(filename.read_text())['sha256'].items():
        assert digest(root/path)==want,(filename,path)
        checked[path]=want
replay=[]
for old,new in [('discrimination_complete','parent_replay'),
                ('mutant_endpoint_rulers','parent_mutant_replay')]:
    before=json.loads((P/f'checks/{old}.stdout').read_text())
    after=json.loads((R/f'checks/{new}.stdout').read_text())
    assert before==after
    receipt=json.loads((R/f'checks/{new}.json').read_text())
    assert receipt['returncode']==1 and not receipt['timeout']
    failed=[g for g in after['guards'] if not math.isfinite(g['error']) or g['error']>g['tolerance']]
    assert failed==after['failed_guards'] and after['status']=='FAIL'
    replay.append(dict(name=new,JSON_exact=True,guards=len(after['guards']),
                       failed_guards=failed,receipt=receipt))
for name in ['source_first','direct']:
    receipt=json.loads((R/f'checks/{name}.json').read_text())
    assert receipt['returncode']==0 and not receipt['timeout']
source=json.loads((R/'checks/source_first.stdout').read_text().splitlines()[-1])
direct=json.loads((R/'checks/direct.stdout').read_text().splitlines()[-1])
assert len(source['rows'])==12 and len(direct['failed_case_records'])==5
assert direct['status']=='PASS_REVIEW_CHECKS_ORIGINAL_GATE_FAILURE_CONFIRMED'
assert float(direct['failed_gate_error'])>float(direct['failed_gate_tolerance'])
out=dict(status='PASS_REVIEW_EVIDENCE_CORRESPONDENCE_ONLY',
         original_finite_plan='FAIL_ONE_FROZEN_CONVERGENCE_GATE',
         utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),
         checked_sha256=checked,replays=replay,
         no_scientific_independence_inferred_from_hash_or_replay=True)
print(json.dumps(out,indent=2))
