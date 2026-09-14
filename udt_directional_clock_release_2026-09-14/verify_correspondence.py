"""Documentary correspondence and preservation; not a scientific truth test."""
from pathlib import Path
import csv
import datetime
import hashlib
import json
import subprocess

root=Path.cwd().resolve()
p=Path('udt_directional_clock_release_2026-09-14')
denied=('8_25/','udt_kernel_plane_global_curvature_holonomy_atlas_2026-08-02/',
        'udt_native_onshell_timelive_reset_owner_audit_2026-08-10/',
        'udt_pair_regime_flow_reciprocal_orchestra_amplification_2026-08-12/',
        'udt_sne_xmax_G88_am_radial_compatibility_atlas_2026-08-12/')
def sha(name):
    q=Path(name).resolve(); rel=q.relative_to(root).as_posix()
    assert not rel.startswith(denied),rel
    return hashlib.sha256(q.read_bytes()).hexdigest()
def git(*args):
    return subprocess.check_output(['git',*args],text=True)
launch=json.loads((p/'LAUNCH.json').read_text())
for section in ('fixed_pins','source_pins','tool_pins'):
    for name, expected in launch[section].items(): assert sha(name)==expected,name
assert sha(p/'WORK_ORDER.md')==launch['work_order_sha256']
for name,expected in json.loads((p/'TOOL_PINS.json').read_text()).items(): assert sha(name)==expected,name
for freeze in ('INITIAL_FREEZE.json','FINAL_CANDIDATE_FREEZE.json'):
    for name,expected in json.loads((p/freeze).read_text())['files'].items(): assert sha(name)==expected,name
assert sha(p/'GATE_RECORD.md')==json.loads((p/'GATE_FREEZE.json').read_text())['gate_sha256']
review_pin_count=0
for manifest in sorted((p/'review').glob('*.sha256')):
    for line in manifest.read_text().splitlines():
        expected,name=line.split(None,1);name=name.lstrip('* ')
        assert sha(name)==expected,(str(manifest),name)
        review_pin_count+=1
assert review_pin_count>0
with open('CURRENT_SCIENTIFIC_PREMISES.tsv',newline='') as f:
    live={r['premise_id']:r for r in csv.DictReader(f,delimiter='\t')}
with (p/'SELECTED_PREMISES.tsv').open(newline='') as f:
    selected=list(csv.DictReader(f,delimiter='\t'))
assert len(selected)==8
for r in selected: assert live[r['premise_id']]==r,r['premise_id']
captures={}
for prefix in ('checks/full406','checks/parent_exact','review/independent_run','checks/navigation'):
    meta=json.loads((p/(prefix+'.json')).read_text())
    assert meta['returncode']==0 and not meta['timeout'],prefix
    assert (p/(prefix+'.stderr')).read_bytes()==b'',prefix
    assert (p/(prefix+'.stdout')).stat().st_size>0,prefix
    captures[prefix]=meta
parent=json.loads((p/'checks/parent_exact.stdout').read_text())
independent=json.loads((p/'review/independent_run.stdout').read_text())
assert parent['status']==independent['status']=='PASS'
assert parent['script_sha256']==sha(p/'check_exact.py')
assert '406-row premise registry' in (p/'checks/full406.stdout').read_text()
assert '359 passed, 1 deselected' in (p/'checks/navigation.stdout').read_text()
original=launch['original_status_names']
now=git('status','--porcelain=v1','-uall').splitlines()
actual=[x for x in now if x.startswith('?? ') and not x[3:].startswith(str(p)+'/')]
assert actual==original,'original untracked names changed'
assert len(actual)==51
allowed=set(json.loads((p/'MAINTAINED_BEFORE.json').read_text()))
for name in set(git('diff','--name-only').splitlines()+git('diff','--cached','--name-only').splitlines()):
    assert name in allowed or name.startswith(str(p)+'/'),name
assert git('rev-parse','--abbrev-ref','HEAD').strip()=='grok'
assert len(Path('MEMORY.md').read_text().split())<=450
subprocess.run(['git','diff','--check'],check=True)
files=[q for q in p.rglob('*') if q.is_file()]
assert all('__pycache__' not in q.parts and q.suffix!='.pyc' for q in files)
size=sum(q.stat().st_size for q in files);assert size<5*1024*1024
print(json.dumps({'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'fixed_pins':len(launch['fixed_pins']),'source_pins':len(launch['source_pins']),
 'selected_exact_rows':len(selected),'review_manifest_entries_checked':review_pin_count,
 'original_untracked_names':len(actual),'package_bytes_before_this_capture':size,
 'parent_named_checks':parent['named_check_count'],'independent_assertions':independent['assertions'],
 'captures':captures,'scope':'hash correspondence, actual outputs and names-only preservation; not proof, review independence or chronology'},indent=2))
