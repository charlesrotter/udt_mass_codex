"""Reuse parent audit and pinned sources; do not rerun the premise verifier."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess

root=Path('/home/udt-admin/udt_mass_codex')
campaign=root/'udt_berger_initial_data_preservation_campaign_2026-09-08'
review=campaign/'step_02/review'
expected='8593f11cd96a575be3513d1ec56e92ac4f5811ff'
checks=[]
def check(name,ok):
    assert ok,name
    checks.append(name)
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*args):
    r=subprocess.run(['git',*args],cwd=root,capture_output=True,check=True)
    return r.stdout

check('branch',git('branch','--show-current').decode().strip()=='grok')
check('HEAD',git('rev-parse','HEAD').decode().strip()==expected)
check('origin_grok',git('rev-parse','origin/grok').decode().strip()==expected)
fetch=(root/'.git/FETCH_HEAD').read_bytes()
check('FETCH_HEAD',fetch.decode().split()[0]==expected and "branch 'grok'" in fetch.decode())
record=json.loads((campaign/'STARTUP_AUDIT.json').read_text())
check('audit_command',record['command']==['python3','-B','verify_current_scientific_premises.py'])
check('audit_cwd',record['cwd']==str(root))
check('audit_exit',record['returncode']==0 and record['timeout'] is False)
check('audit_stdout_correspondence',record['stdout'].encode()==(campaign/'STARTUP_AUDIT.stdout').read_bytes())
check('audit_stderr_correspondence',record['stderr'].encode()==(campaign/'STARTUP_AUDIT.stderr').read_bytes()==b'')
check('full358_recorded', 'PASS: 358-row premise registry' in record['stdout'])
paths=[
'AGENTS.md','CLAUDE.md','CURRENT_SCIENTIFIC_PREMISES.md',
'CURRENT_SCIENTIFIC_PREMISES.tsv','verify_current_scientific_premises.py',
'.claude/skills/no-shortcuts/SKILL.md','.claude/skills/completeness-map/SKILL.md',
'.claude/skills/solver-first/SKILL.md','.claude/skills/verifier-before-record/SKILL.md',
'udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py',
'udt_g315_conditional_cauchy_characteristic_data_interface_2026-09-01/EXACT_DERIVATION.md',
'udt_g330_berger_hopf_eigenline_local_persistence_2026-09-02/EXACT_DERIVATION.md',
'udt_g330_berger_hopf_eigenline_local_persistence_2026-09-02/AUDIT_REPORT.md',
'udt_g321_g320_local_cauchy_development_uniqueness_2026-09-01/EXACT_DERIVATION.md']
hashes={}
for p in paths:
    content=(root/p).read_bytes()
    hashes[p]=sha(content)
    check('HEAD_bytes_'+p,git('show',expected+':'+p)==content)
check('BI1_recorded_registry_hash',hashes['CURRENT_SCIENTIFIC_PREMISES.tsv']=='2bb885062dce0f47f7ea37562aee882d5d5d41f25cb539e9dd37755bbe722b63')
check('BI1_recorded_verifier_hash',hashes['verify_current_scientific_premises.py']=='5eac2b421d52b7b45e060332d4b2c2d333e57f177f4103f9c30abf9e28df0540')
for p in ['WORK_ORDER.md','step_02/QUESTION.md','step_02/REVIEW_DISPATCH.md',
          'step_01/CANDIDATE_INITIAL.md','step_01/REVIEWED_RESULT.md',
          'step_01/review/REVIEW_REPORT.md',
          'STARTUP_AUDIT.command.txt','STARTUP_AUDIT.json','STARTUP_AUDIT.stdout','STARTUP_AUDIT.stderr']:
    content=(campaign/p).read_bytes()
    name=str((campaign/p).relative_to(root))
    hashes[name]=sha(content)
    target=review/'source_snapshots'/name
    target.parent.mkdir(parents=True,exist_ok=True)
    with target.open('xb') as f:f.write(content)
check('BI1_candidate_hash',sha((campaign/'step_01/CANDIDATE_INITIAL.md').read_bytes())=='ce6b36dce14c07049ee9be193ca07989c5ea2f2507d8587c7b978317d0980fbc')
check('BI1_entire_review_hash',sha((campaign/'step_01/review/REVIEW_REPORT.md').read_bytes())=='f68aeba4a80fa7b095122d7ea07bc45e3d0213bddbee1d23d64f96e2cd538c80')
check('capture_utility_byte_identity',(review/'run_capture.py').read_bytes()==(root/'udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py').read_bytes())
out=dict(status='PASS',checks=checks,check_count=len(checks),sha256=hashes,
         reused_audit=record,git_HEAD=expected,fetch_head=fetch.decode(),
         fetch_mtime_utc=datetime.datetime.fromtimestamp((root/'.git/FETCH_HEAD').stat().st_mtime,datetime.timezone.utc).isoformat(),
         caveat='parent execution reused; no independent network observation or later remote freshness claim')
print(json.dumps(out,indent=2,sort_keys=True))
