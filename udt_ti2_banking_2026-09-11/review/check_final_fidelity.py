"""Final receipt/navigation/scope metadata only; not a full audit rerun."""
from pathlib import Path
import datetime
import hashlib
import json
import subprocess
import sys
repo=Path(__file__).resolve().parents[2]
bank=repo/'udt_ti2_banking_2026-09-11'
sys.path.insert(0,str(repo))
import ti2_banking_guard as guard
def git(*args):return subprocess.check_output(['git',*args],cwd=repo,text=True,timeout=15)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
base='b95ace99315b816b9a53abe8102b478d1e1cd188'
assert git('branch','--show-current').strip()=='grok'
assert git('rev-parse','HEAD').strip()==git('rev-parse','origin/grok').strip()==base
assert not git('diff','--cached','--name-only').strip()
guard.validate_ti2_banking(repo)
scope=json.loads((bank/'FULL397_INPUTS.json').read_text())
changed=[path for path,digest in scope['sha256'].items() if sha(repo/path)!=digest]
nav=['CURRENT_RESEARCH_PROGRAM.md','CURRENT_SCIENTIFIC_PREMISES.md','HANDOFF.md',
     'INDEX.md','LIVE.md','MEMORY.md','UDT_RESEARCH_ROADMAP.md']
assert sorted(changed)==sorted(nav),changed
full=json.loads((bank/'checks/full397.json').read_text())
reported=json.loads((bank/'FULL397_RESULT.json').read_text())
assert reported['receipt']==full and reported['actual_result']=='PASS_397'
assert full['returncode']==0 and not full['timeout']
assert full['duration_seconds']==403.0194429080002
assert full['cpu_seconds']==900 and full['address_space_bytes']==2147483648
assert not (bank/'checks/full397.stderr').read_bytes()
assert b'PASS: G414/TI2 conditional initial evolution' in (bank/'checks/full397.stdout').read_bytes()
late=json.loads((bank/'checks/final_navigation.json').read_text())
assert late['returncode']==0 and not late['timeout']
assert not (bank/'checks/final_navigation.stderr').read_bytes()
assert '592 passed, 1 deselected' in (bank/'checks/final_navigation.stdout').read_text()
assert late['cpu_seconds']==180 and late['address_space_bytes']==2147483648
caps={'LIVE.md':(135,900),'HANDOFF.md':(100,600),'INDEX.md':(118,570),
      'MEMORY.md':(70,450),'CURRENT_RESEARCH_PROGRAM.md':(155,1100),
      'CURRENT_SCIENTIFIC_PREMISES.md':(140,1320)}
sizes={}
for path,(lines,words) in caps.items():
 text=(repo/path).read_text()
 sizes[path]={'lines':len(text.splitlines()),'words':len(text.split())}
 assert sizes[path]['lines']<=lines and sizes[path]['words']<=words
 assert max(map(len,text.splitlines()))<=220
next_gate='G383--G412 exact-scope banking is COMPLETE; G413=TI1 and G414=TI2 conditionally banked; authorized TI3 scope: INDEX.'
for path in ['LIVE.md','HANDOFF.md','CURRENT_RESEARCH_PROGRAM.md']:
 assert next_gate in (repo/path).read_text()
assert 'stale expected396 error-message text (current397)' in (bank/'INTEGRATION_HISTORY.md').read_text()
for name in ['BANKING_RECORD.md','WORK_ORDER.md','CLOSEOUT.md','MANIFEST_SCOPE.md']:
 assert (bank/name).is_file()
allowed_tracked=set(scope['sha256'])-{'ti2_banking_guard.py','tests/test_ti2_banking.py'}
assert set(git('diff','--name-only').splitlines())==allowed_tracked
status=git('status','--porcelain=v1','--untracked-files=normal')
owned={bank.name+'/', 'ti2_banking_guard.py','tests/test_ti2_banking.py'}
unrelated=''.join(line+'\n' for line in status.splitlines() if line.startswith('?? ') and line[3:] not in owned)
assert len(unrelated.splitlines())==46
assert hashlib.sha256(unrelated.encode()).hexdigest()=='55e7c4508622f912730f9c068cc571c370b3977bc1110eb0a48a8218dbe024c2'
assert not (repo/'udt_two_shape_profile_dependence_2026-09-11').exists()
caches=[str(p.relative_to(repo)) for p in bank.rglob('*') if p.is_dir() and p.name in ['__pycache__','.pytest_cache']]
print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'verdict':'PASS',
 'full397':'actual parent receipt inspected, not reviewer rerun','full397_seconds':full['duration_seconds'],
 'late_suite':'592passed/1duplicate-wrapper-deselected','late_suite_seconds':late['duration_seconds'],
 'later_navigation_inputs':changed,'unchanged_other_audit_inputs':len(scope['sha256'])-len(changed),
 'current_surface_sizes':sizes,'original46_status_names_preserved':True,
 'cache_exclusions':caches,'replay_scratch_exists':(bank/'review/_uncreated_probe').exists(),
 'publication':'future; nothing staged; no commit/push outcome anticipated',
 'runtime_model_version':'UNATTESTED'},indent=2))
