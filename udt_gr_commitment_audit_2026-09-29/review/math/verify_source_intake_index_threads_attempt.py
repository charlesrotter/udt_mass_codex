"""Version/intake receipt only; hashes do not certify scientific truth."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess

root=Path.cwd()
out=root/'udt_gr_commitment_audit_2026-09-29/review/math'
pins_path=root/'udt_gr_commitment_audit_2026-09-29/SOURCE_PINS.json'
pins=json.loads(pins_path.read_text())['sha256']
checks={}
for name,expected in pins.items():
    data=(subprocess.check_output(['git','show','9edec2e528e058cbfab11de7a1eff1f90d0cc970:'+name])
          if name=='UDT_DEVELOPMENT.md' else (root/name).read_bytes())
    actual=hashlib.sha256(data).hexdigest()
    checks[name]={'actual':actual,'expected':expected,'matches':actual==expected,
                 'version':'git launch HEAD' if name=='UDT_DEVELOPMENT.md' else 'disk'}
assert all(v['matches'] for v in checks.values())
extra=[
    '.claude/skills/no-shortcuts/SKILL.md',
    '.claude/skills/completeness-map/SKILL.md',
    '.claude/skills/verifier-before-record/SKILL.md',
    'development_reconstruction_2026-09-29/MAINTENANCE.md',
    'development_reconstruction_2026-09-29/SOURCE_CORRECTIONS.md',
    'startup_surface_g310_universal_reciprocity_refresh_2026-08-31/ADOPTION_RECORD.md',
    'udt_g310_differential_dual_reciprocity_tracefree_ownership_2026-08-31/EXACT_DERIVATION.md',
    'udt_local_kernel_symmetry_release_2026-09-13/capture.py',
    'udt_shared_readout_metric_constraint_campaign_2026-09-06/run_capture.py',
    'udt_gr_commitment_audit_2026-09-29/WORK_ORDER.md',
    'udt_gr_commitment_audit_2026-09-29/SOURCE_PINS.json',
]
def git(*args):return subprocess.check_output(['git',*args],text=True).strip()
status=subprocess.check_output(['git','-c','index.threads=1','status','--porcelain'],text=True).splitlines()
receipt={
    'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'branch':git('branch','--show-current'),'head':git('rev-parse','HEAD'),
    'status_at_receipt':{'tracked_count':sum(not l.startswith('??') for l in status),
       'untracked_entries':sum(l.startswith('??') for l in status),
       'scope_note':'Names only inspected; unrelated/protected payload not read'},
    'launch_pin_checks':checks,
    'additional_read_source_sha256':{n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in extra},
    'external_statements_inspected':[
       {'url':'https://arxiv.org/html/1202.5811v1','sections':'definitions, equations 1.3-1.5, Theorem 1','proof_replayed':False},
       {'url':'https://arxiv.org/html/0709.1928v2','sections':'Corollary 4.8, Theorem 5.1','proof_replayed':False}],
    'parent_startup_and_full406':'Attributed at launch HEAD; not independently rerun here',
    'packaging_failures':['source_intake_01 correctly rejected changed current UDT_DEVELOPMENT; launch central bytes are now checked through git show. No changed prose exposed to reviewer.',
                         'source_intake_02 reached git status but threaded lstat failed under the resource bound; status now sets index.threads=1 without changing git configuration.'],
    'preseal_parent_exposure':'After check run and substantive source-first draft: comparator family EH+alpha R² on a product metric, 22 checks. No metric/proof/code/output/verdict seen.',
}
assert receipt['branch']=='grok'
assert receipt['head']=='9edec2e528e058cbfab11de7a1eff1f90d0cc970'
with (out/'SOURCE_INTAKE.json').open('x') as f: json.dump(receipt,f,indent=2);f.write('\n')
print(json.dumps({'pin_count':len(checks),'all_match':True,'branch':receipt['branch'],'head':receipt['head'],'state':receipt['status_at_receipt']},indent=2))
