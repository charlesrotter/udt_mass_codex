"""Authenticate admitted inputs and print a source-first evidence seal."""
import csv
import datetime
import hashlib
import json
from pathlib import Path
import subprocess

root=Path(__file__).resolve().parents[3]
campaign=root/'udt_berger_global_constraint_campaign_2026-09-08'
review=Path(__file__).resolve().parent
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
pins={}
for line in (campaign/'SOURCE_PINS_SHA256SUMS').read_text().splitlines():
    expected,name=line.split(None,1)
    assert digest(root/name)==expected, name
    pins[name]=expected
audit=json.loads((campaign/'STARTUP_AUDIT.json').read_text())
assert audit['returncode']==0 and not audit['timeout']
assert 'PASS: 358-row premise registry' in audit['stdout']
assert audit['stdout'].encode()==(campaign/'STARTUP_AUDIT.stdout').read_bytes()
assert audit['stderr'].encode()==(campaign/'STARTUP_AUDIT.stderr').read_bytes()
sources=[
 'AGENTS.md','CLAUDE.md','.claude/skills/no-shortcuts/SKILL.md',
 '.claude/skills/completeness-map/SKILL.md','.claude/skills/verifier-before-record/SKILL.md',
 '.claude/skills/solver-first/SKILL.md',
 'udt_g337_double_silent_third_normal_ownership_2026-09-03/EXACT_DERIVATION.md',
 'udt_g337_double_silent_third_normal_ownership_2026-09-03/AUDIT_REPORT.md',
 'udt_berger_initial_data_preservation_campaign_2026-09-08/step_01/CANDIDATE_INITIAL.md',
 'udt_berger_initial_data_preservation_campaign_2026-09-08/step_01/REVIEWED_RESULT.md',
 'udt_berger_initial_data_preservation_campaign_2026-09-08/step_01/review/REVIEW_REPORT.md',
 'udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py']
for name in ['WORK_ORDER.md','step_02/QUESTION.md','step_02/REVIEW_DISPATCH.md',
 'STARTUP_AUDIT.command.txt','STARTUP_AUDIT.json','STARTUP_AUDIT.stdout','STARTUP_AUDIT.stderr',
 'step_01/CANDIDATE_INITIAL.md','step_01/REVIEWED_RESULT.md',
 'step_01/review/REVIEW_REPORT.md','step_01/review/REVIEW_DISPOSITION.json']:
    sources.append(str((campaign/name).relative_to(root)))
for name in sources:
    pins[name]=digest(root/name)
assert pins[str((campaign/'step_01/CANDIDATE_INITIAL.md').relative_to(root))]=='ea499eede1127128eb5426e46a591cac71b9422f87b8982d9f7cf17212e55b9a'
assert pins[str((campaign/'step_01/review/REVIEW_REPORT.md').relative_to(root))]=='7d7902e456ee3f146f0bafbcbfd9c20b3cde501c974b5fd8c555570910eee5cb'
corrected=(review/'independent_check.py').read_text()
initial=(review/'independent_check_initial_failed.py').read_text()
assert initial==corrected.replace('for i,j,k in itertools.product(range(3),repeat=3):\n    DG','    DG')
run=json.loads((review/'source_first_check_corrected.json').read_text())
result=json.loads((review/'source_first_check_corrected.stdout').read_text())
assert run['returncode']==0 and not run['timeout']
assert result['exact_checks']==17 and len(result['mutations'])==5
assert all(v=='CAUGHT' for v in result['mutations'].values())
review_files=['REVIEW_SCOPE.md','SOURCE_FIRST.md','PRESEAL_FAILURE.md','independent_check.py',
 'independent_check_initial_failed.py','seal_source_first.py',
 'source_first_check.json','source_first_check.stdout','source_first_check.stderr',
 'source_first_check_corrected.json','source_first_check_corrected.stdout','source_first_check_corrected.stderr']
own={str((review/name).relative_to(root)):digest(review/name) for name in review_files}
print(json.dumps({'sealed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'reviewer':'/root/bg2_review','source_first':True,'author_BG2_exposure':False,
 'BG1_auxiliary_exposure':False,'startup_audit_receipt_authenticated_reused':True,
 'startup_audit_independently_replayed':False,
 'branch':subprocess.check_output(['git','branch','--show-current'],cwd=root,text=True).strip(),
 'HEAD_at_seal':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
 'source_sha256':pins,'source_first_sha256':own,
 'exact_checks':17,'executed_mutations_caught':5,
 'initial_failed_reviewer_run_preserved':True,
 'online_methods':[{'author':'Richard Melrose','url':'https://math.mit.edu/~rbm/iml/Chapter6.pdf',
 'locators':'Theorems6.1--6.3; equations6.48,6.49,6.58; generalized inverse and vector bundles',
 'accessed_utc_date':'2026-09-08','retrieval':'web tool PDF text; tool transcript, no downloaded-file hash'},
 {'author':'Richard Melrose','url':'https://math.mit.edu/~rbm/18-155-F15/PseudodifferentialOperators.pdf',
 'locators':'sections2--3, symbols and local quantization',
 'accessed_utc_date':'2026-09-08','retrieval':'web tool PDF text; tool transcript, no downloaded-file hash'}]},indent=2))
