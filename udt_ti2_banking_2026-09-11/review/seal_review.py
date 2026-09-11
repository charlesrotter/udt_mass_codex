"""Seal the completed substantive banking review; final full397 remains pending."""
from pathlib import Path
import datetime
import hashlib
import json
import platform
import subprocess

repo=Path(__file__).resolve().parents[2]
review=Path(__file__).resolve().parent
bank=review.parent
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
roots=['CURRENT_SCIENTIFIC_PREMISES.tsv','ti1_banking_guard.py','ti2_banking_guard.py',
 'verify_current_scientific_premises.py','tests/test_startup_surface.py',
 'tests/test_ti1_banking.py','tests/test_ti2_banking.py']
names=[repo/p for p in roots]
names += [bank/n for n in ['WORK_ORDER.md','LAUNCH.json','BANKING_RECORD.md',
 'BANKED_CLAIM.json','BANKED_ROW.tsv','SOURCE_EVIDENCE_SHA256SUMS','PREBANK_PREMISE_RESULT.json',
 'catch_previous_snapshot_guard.py']]
names += [p for p in review.rglob('*') if p.is_file() and '__pycache__' not in p.parts
          and '.pytest_cache' not in p.parts and p.name!='REVIEW_RECEIPT.json']
for stem in ['prebank396','initial_integration','repaired_integration','snapshot_repair_integration',
             'persistent_snapshot_catchproof','persistent_snapshot_live']:
 names += [bank/'checks'/(stem+suffix) for suffix in ['.json','.stdout','.stderr','.capture_provenance.json']]
source=repo/'udt_two_shape_evolution_2026-09-11'
names += [source/p for p in ['INITIAL_CANDIDATE.md','REVIEWED_RESULT.md','DISCOVERY_AND_FREEZE.md',
 'review/REVIEW.md','review/FINAL_FIDELITY.md','review/REVIEW_RECEIPT.json','review/FINAL_FIDELITY_RECEIPT.json']]
status=subprocess.check_output(['git','status','--porcelain=v1','--untracked-files=normal'],cwd=repo,text=True)
owned={bank.name+'/', 'ti2_banking_guard.py','tests/test_ti2_banking.py'}
unrelated=''.join(line+'\n' for line in status.splitlines() if line.startswith('?? ') and line[3:] not in owned)
assert len(unrelated.splitlines())==46
assert hashlib.sha256(unrelated.encode()).hexdigest()=='55e7c4508622f912730f9c068cc571c370b3977bc1110eb0a48a8218dbe024c2'
current={str(p.relative_to(repo)):digest(p) for p in sorted(set(names))}
captures=[]
for stem in ['initial_preservation','second_snapshot_initial','second_snapshot_repaired',
 'independent_hostile','postrepair_preservation','hostile_final_implementation']:
 captures.append(json.loads((review/(stem+'.json')).read_text()))
record={'context':'/root/ti2_banking_fidelity','first_observed_utc':'2026-09-11T18:54:40Z',
 'sealed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'parent_overlap':'Concurrent construction/integration in same continuing parent session',
 'python':platform.python_version(),'runtime_model_version':'UNATTESTED',
 'verdict':'VERIFIED_WITH_CAVEATS__EXACT_SCOPE_FIDELITY_AND_REPAIRED_INTEGRATION',
 'scientific_repairs_required':0,'integration_defects_found_and_repaired':1,
 'persistent_test_blind_spot_repaired_and_catch_proved':True,
 'reviewer_execution_receipts':captures,'original46_status_sha256':hashlib.sha256(unrelated.encode()).hexdigest(),
 'protected_payloads':'Never read or hashed; status names only',
 'final397_audit':'PENDING_PARENT_EXECUTION','final_navigation_and_publication':'PENDING_ACTUAL_OUTCOMES',
 'sha256':current}
with (review/'REVIEW_RECEIPT.json').open('x') as stream:
 json.dump(record,stream,indent=2);stream.write('\n')
print(json.dumps({'sealed_utc':record['sealed_utc'],'pins':len(current),
 'receipt_sha256':digest(review/'REVIEW_RECEIPT.json'),'review_sha256':digest(review/'REVIEW.md'),
 'original46_name_status_fingerprint_match':True},indent=2))
