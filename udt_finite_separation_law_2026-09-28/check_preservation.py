"""Source/packaging correspondence only; not scientific verification."""
from pathlib import Path
import csv
import hashlib
import json
import subprocess

p = Path(__file__).resolve().parent
root = p.parent
launch = json.loads((p/'LAUNCH.json').read_text())
freeze = json.loads((p/'CANDIDATE_FREEZE.json').read_text())
maintained = {'LIVE.md','HANDOFF.md','CURRENT_RESEARCH_PROGRAM.md','MEMORY.md','INDEX.md','UDT_RESEARCH_ROADMAP.md'}
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
for f,h in launch['sources'].items():
    if f not in maintained:
        assert digest(root/f)==h,f
for f,h in freeze['additional_sources'].items():
    assert digest(root/f)==h,f
for f,h in freeze['candidate_and_checks'].items():
    assert digest(p/f)==h,f
seal=json.loads((p/'review/SOURCE_FIRST_SEAL.json').read_text())
for f,h in seal['sha256'].items():
    assert digest(p/'review'/f)==h,f
rows={r['premise_id']:r for r in csv.DictReader((root/'CURRENT_SCIENTIFIC_PREMISES.tsv').open(),delimiter='\t')}
assert len(rows)==406
selected=json.loads((p/'SCOPED_REGISTRY.json').read_text())
assert all(rows[r['premise_id']]==r for r in selected)
git=['git','-c','core.preloadIndex=false','-c','index.threads=1']
def output(*args):
    return subprocess.check_output(git+list(args),cwd=root,text=True)
untracked=set(output('ls-files','--others','--exclude-standard').splitlines())
assert {f for f in untracked if not f.startswith(p.name+'/')}==set(launch['prior_untracked_paths'])
assert set(output('diff','--name-only').splitlines())==maintained
before=output('show',launch['head']+':CURRENT_RESEARCH_PROGRAM.md')
now=(root/'CURRENT_RESEARCH_PROGRAM.md').read_text()
assert before.split('## Current next gate')[0]==now.split('## Current next gate')[0]
subprocess.run(git+['diff','--check'],cwd=root,check=True)
size=sum(f.stat().st_size for f in p.rglob('*') if f.is_file())
assert size<2*1024**2,size
print(json.dumps({'status':'PASS','evidence':'correspondence/preservation, not truth',
    'preserved_prior_untracked_paths':len(launch['prior_untracked_paths']),
    'registry_rows_unchanged':len(rows),'selected_rows_verified':len(selected),
    'candidate_and_check_pins':len(freeze['candidate_and_checks']),
    'source_first_pins':len(seal['sha256']),'package_bytes':size,
    'maintained':sorted(maintained),'founding_opening_unchanged':True},indent=2))
