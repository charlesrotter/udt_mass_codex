"""Source/claim correspondence and names-only workspace check; no payload mining."""
from pathlib import Path
import csv
import hashlib
import json
import subprocess
import platform
import sys

p=Path(__file__).resolve().parent.relative_to(Path.cwd().resolve())
def digest(f): return hashlib.sha256(Path(f).read_bytes()).hexdigest()
checked=[]
for name in ['SOURCE_PINS.json','ADDITIONAL_SOURCE_PINS.json','FINAL_SOURCE_PINS.json']:
    for f,h in json.loads((p/name).read_text())['pins'].items():
        assert digest(f)==h,f
        checked.append(f)
for f,h in json.loads((p/'PROTECTED_EVIDENCE_PINS.json').read_text()).items():
    assert digest(f)==h,f
    checked.append(f)
for f,h in json.loads((p/'CANDIDATE_FREEZE.json').read_text())['pins'].items():
    assert digest(p/f)==h,f
assert digest(p/'parent_exact.py')==json.loads((p/'PARENT_CODE_FREEZE.json').read_text())['parent_code_sha256']
with open('CURRENT_SCIENTIFIC_PREMISES.tsv') as f:
    current={r['premise_id']:r for r in csv.DictReader(f,delimiter='\t')}
with (p/'LOAD_BEARING_REGISTRY_ROWS.tsv').open() as f:
    selected=list(csv.DictReader(f,delimiter='\t'))
assert len(selected)==16
assert all(current[r['premise_id']]==r for r in selected)
for name in ['premise406','parent_exact','startup_tests']:
    meta=json.loads((p/'checks'/f'{name}.json').read_text())
    assert meta['returncode']==0 and not meta['timeout'],name
    assert (p/'checks'/f'{name}.stderr').read_bytes()==b'',name
assert 'PASS: 406-row premise registry' in (p/'checks/premise406.stdout').read_text()
assert '359 passed, 1 deselected' in (p/'checks/startup_tests.stdout').read_text()
parent=json.loads((p/'checks/parent_exact.stdout').read_text())
assert parent['status']=='PASS' and parent['check_count']==35
assert parent['balance_rank']==parent['density_rank']==5
assert len(parent['hostile_recomputations'])==5 and all(parent['hostile_recomputations'].values())
independent=json.loads((p/'review/independent_center_check.stdout').read_text())
assert independent['status']=='PASS' and independent['assertions']==6307
meta=json.loads((p/'review/INDEPENDENT_CHECK_EXECUTION.json').read_text())
assert meta['exit_code']==0 and meta['elapsed_seconds']<120
for name,h in meta['sha256'].items(): assert digest(p/'review'/name)==h
assert (p/'review/independent_center_check.stderr').read_bytes()==b''

commands=[]
def git(*args):
    r=subprocess.run(['git',*args],text=True,capture_output=True)
    commands.append({'command':['git',*args],'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
    assert r.returncode==0,args
    return r.stdout
launch=json.loads((p/'LAUNCH.json').read_text())
assert git('rev-parse','--abbrev-ref','HEAD').strip()=='grok'
assert git('rev-parse','HEAD','origin/grok').splitlines()==[launch['head'],launch['origin']]
assert not git('diff','--cached','--name-only').strip()
status=git('status','--short','--untracked-files=all')
other=''.join(l+'\n' for l in status.splitlines() if l.startswith('?? ') and not l[3:].startswith(str(p)+'/'))
assert other==launch['original_untracked_status']
assert hashlib.sha256(other.encode()).hexdigest()==launch['original_untracked_status_sha256']
allowed={'LIVE.md','HANDOFF.md','CURRENT_RESEARCH_PROGRAM.md','MEMORY.md','INDEX.md','UDT_RESEARCH_ROADMAP.md'}
changed=git('diff','--name-only').splitlines()
assert set(changed)==allowed,changed
assert not git('diff','--check').strip()
print(json.dumps({'status':'PASS','python':platform.python_version(),'argv':sys.argv,
 'source_pins_and_fixed_evidence_checked':len(checked),'selected_registry_rows_exact':16,
 'initial_candidate_and_code_preserved':True,'own_navigation_only':changed,
 'original_untracked_names_exact':len(other.splitlines()),'original_untracked_sha256':hashlib.sha256(other.encode()).hexdigest(),
 'protected_payloads':'not read or hashed; status names only',
 'full406_parent_symbolic_independent_and_navigation_captures_verified':True,
 'commands':commands,'limits':'correspondence/regression, not independent scientific proof or backup completeness'},indent=2))
