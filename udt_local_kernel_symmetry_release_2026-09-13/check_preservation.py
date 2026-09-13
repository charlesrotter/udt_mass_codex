"""Correspondence/preservation check only; not scientific verification."""
from pathlib import Path
import datetime, hashlib, json, platform, subprocess, sys

P=Path(__file__).resolve().parent
ROOT=P.parent
records=[]
def read(name): return json.loads((P/name).read_text())
def pin(path, expected, group):
    path=Path(path)
    actual=hashlib.sha256(path.read_bytes()).hexdigest()
    if actual!=expected: raise RuntimeError(f'{group}: hash changed: {path}')
    records.append({'group':group,'path':str(path.relative_to(ROOT)),'sha256':actual})
for name,key in [('SOURCE_PINS.json','pins'),('WORK_ORDER_FREEZE.json','pins')]:
    for f,h in read(name)[key].items():pin(ROOT/f,h,name)
for f,h in read('AUDIT_INPUT_PINS.json').items():pin(ROOT/f,h,'original_audit_inputs')
for f,h in read('CANDIDATE_FREEZE.json')['files'].items():pin(P/f,h,'initial_candidate')
pin(P/'parent_exact.py',read('IMPLEMENTATION_FREEZE.json')['parent_exact.py'],'parent_implementation')
for name in ['CLARIFICATION_FREEZE.json','CLASSIFICATION_CANDIDATE_FREEZE.json','CLASSIFICATION_IMPLEMENTATION_FREEZE.json']:
    d=read(name);pin(P/d['file'],d['sha256'],name)
for f,h in read('review/RECOMPUTATION_FREEZE.json')['hashes'].items():pin(P/'review'/f,h,'review_recomputation_freeze')
d=read('review/FINAL_FIDELITY.json')
for key in ['scientific_files','lay_files','navigation_files']:
    for f,h in d[key].items():pin(ROOT/f,h,'final_review_'+key)
pin(P/'review/REVIEW.md',d['review_sha256'],'direct_review')
commands=[]
def git(*args):
    r=subprocess.run(['git',*args],cwd=ROOT,capture_output=True,text=True)
    commands.append({'argv':['git',*args],'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
    if r.returncode:raise RuntimeError(r.stderr)
    return r.stdout
branch=git('rev-parse','--abbrev-ref','HEAD').strip()
refs=git('rev-parse','HEAD','origin/grok').splitlines()
if branch!='grok' or refs[0]!=refs[1]:raise RuntimeError('branch/ref mismatch')
if git('diff','--cached','--name-only').strip():raise RuntimeError('index not clean')
roots=git('diff','--name-only').splitlines()
allowed={'AGENTS.md','LIVE.md','HANDOFF.md','CURRENT_RESEARCH_PROGRAM.md','MEMORY.md','INDEX.md','UDT_RESEARCH_ROADMAP.md'}
if not set(roots)<=allowed:raise RuntimeError('unexpected tracked work')
status=git('status','--short','--untracked-files=all')
own=str(P.relative_to(ROOT))+'/'
other=''.join(line+'\n' for line in status.splitlines() if line.startswith('?? ') and not line[3:].startswith(own))
original=read('LAUNCH.json')['original_untracked_status']
if other!=original:raise RuntimeError('unrelated untracked names changed')
print(json.dumps({'status':'PASS','scope':'correspondence and names-only preservation; no protected payload inspected or hashed',
 'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'python':platform.python_version(),'optimize':sys.flags.optimize,'pins':records,
 'matched_pin_checks':len(records),'original_untracked_names':len(original.splitlines()),
 'original_untracked_status_sha256':hashlib.sha256(original.encode()).hexdigest(),
 'branch':branch,'refs':refs,'tracked_changed_paths':roots,'commands':commands},indent=2))
