import datetime
import hashlib
import json
from pathlib import Path
import subprocess

root=Path.cwd()
campaign=Path('udt_berger_initial_data_preservation_campaign_2026-09-08')
out=campaign/'step_02/focused_review'
paths=['AGENTS.md','CLAUDE.md','CURRENT_SCIENTIFIC_PREMISES.md','CURRENT_SCIENTIFIC_PREMISES.tsv',
       'verify_current_scientific_premises.py']
paths += ['.claude/skills/'+s+'/SKILL.md' for s in ['no-shortcuts','completeness-map','verifier-before-record','solver-first']]
paths += [str(campaign/p) for p in ['WORK_ORDER.md','step_02/QUESTION.md','step_02/FOCUSED_REVIEW_DISPATCH.md',
    'STARTUP_AUDIT.command.txt','STARTUP_AUDIT.json','STARTUP_AUDIT.stdout','STARTUP_AUDIT.stderr',
    'step_01/REVIEWED_RESULT.md','step_01/CANDIDATE_INITIAL.md','step_01/review/REVIEW_REPORT.md',
    'step_01/review/compare_candidate.py','step_01/review/candidate_comparison.json',
    'step_01/review/candidate_comparison.stdout','step_01/review/candidate_comparison.stderr',
    'step_01/review/source_first_check.py','step_01/review/source_first_run.stdout']]
paths += [p+'/'+f for p in [
    'udt_g315_conditional_cauchy_characteristic_data_interface_2026-09-01',
    'udt_g330_berger_hopf_eigenline_local_persistence_2026-09-02',
    'udt_g321_g320_local_cauchy_development_uniqueness_2026-09-01'] for f in ['AUDIT_REPORT.md','EXACT_DERIVATION.md']]
hashes={p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in paths}
receipt=json.loads((campaign/'STARTUP_AUDIT.json').read_text())
checks={
 'direct parent stdout correspondence':receipt['stdout']==(campaign/'STARTUP_AUDIT.stdout').read_text(),
 'direct parent stderr correspondence':receipt['stderr']==(campaign/'STARTUP_AUDIT.stderr').read_text(),
 'parent passed within cap':receipt['returncode']==0 and not receipt['timeout'] and receipt['duration_seconds']<900,
 'parent correct command and cwd':receipt['command']==['python3','-B','verify_current_scientific_premises.py'] and receipt['cwd']==str(root),
 'registry unchanged from BI1 authenticated receipt':hashes['CURRENT_SCIENTIFIC_PREMISES.tsv']=='2bb885062dce0f47f7ea37562aee882d5d5d41f25cb539e9dd37755bbe722b63',
 'verifier unchanged from BI1 authenticated receipt':hashes['verify_current_scientific_premises.py']=='5eac2b421d52b7b45e060332d4b2c2d333e57f177f4103f9c30abf9e28df0540',
 'BI1 exact candidate':hashes[str(campaign/'step_01/CANDIDATE_INITIAL.md')]=='ce6b36dce14c07049ee9be193ca07989c5ea2f2507d8587c7b978317d0980fbc',
 'BI1 entire controlling review':hashes[str(campaign/'step_01/review/REVIEW_REPORT.md')]=='f68aeba4a80fa7b095122d7ea07bc45e3d0213bddbee1d23d64f96e2cd538c80',
}
comparison=json.loads((campaign/'step_01/review/candidate_comparison.stdout').read_text())
checks['BI1 prior tensor comparison records 67 exact passes']=comparison['all_pass'] and comparison['count']==67 and all(c['pass'] for c in comparison['checks'])
git={}
for name,args in [('head',['rev-parse','HEAD']),('branch',['branch','--show-current']),('status',['status','--short','--branch']),('local_remote_ref',['rev-parse','refs/remotes/origin/grok'])]:
    p=subprocess.run(['git',*args],capture_output=True,text=True,check=True)
    git[name]=dict(command=['git',*args],stdout=p.stdout,stderr=p.stderr,returncode=p.returncode)
checks['HEAD matches dispatch']=git['head']['stdout'].strip()=='8593f11cd96a575be3513d1ec56e92ac4f5811ff'
checks['branch grok']=git['branch']['stdout'].strip()=='grok'
record=dict(recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_hashes=hashes,
    checks=checks,all_pass=all(checks.values()),git=git,parent_receipt=receipt,
    prior_BI1_tensor_evidence=dict(count=comparison['count'],checks=comparison['checks']),
    limitations=['parent premise audit and BI1 checks are authenticated prior evidence, not reruns',
                'remote freshness not independently verified; no campaign-log authentication',
                'hashes show correspondence, not truth or independent chronology'])
(out/'SOURCE_HASHES.json').write_text(json.dumps(hashes,indent=2)+'\n')
print(json.dumps(record,indent=2))
raise SystemExit(0 if record['all_pass'] else 1)
