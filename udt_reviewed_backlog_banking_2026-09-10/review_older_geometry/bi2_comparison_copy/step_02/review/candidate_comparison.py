"""Authenticate exact candidate and compare distinct reviewer tensor calculations."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import re
import runpy
import sympy as s

r=Path(__file__).resolve().parent
p=r.parent
checks=[]
hashes={}
def sha(data):return hashlib.sha256(data).hexdigest()
def check(name,pred):
    assert pred,name
    checks.append(name)
def zero(name,value):
    v=list(value) if isinstance(value,s.MatrixBase) else [value]
    residuals=[s.factor(e) for e in v]
    check(name,all(e==0 for e in residuals))

seal=json.loads((r/'SOURCE_FIRST_SEAL.json').read_text())
for e in seal['files']:
    check('source_seal_'+e['path'],sha((r/e['path']).read_bytes())==e['sha256'])
freeze=(p/'CANDIDATE_FREEZE.md').read_text()
pins=re.findall(r'^\s+([a-f0-9]{64})\s+(\S+)\s*$',freeze,re.M)
check('four_exact_candidate_pins',len(pins)==4)
for digest,path in pins:
    data=(p/path).read_bytes()
    check('frozen_'+path,sha(data)==digest)
    hashes[path]=digest
for n in ['CANDIDATE_FREEZE.md','CANDIDATE_INITIAL.md','check_bi2.py','probe_bi2.py',
          'author_check_01.stdout','author_check_01.stderr','author_check_01.json',
          'author_mutations_01.stdout','author_mutations_01.stderr','author_mutations_01.json']:
    data=(p/n).read_bytes()
    hashes[n]=sha(data)
    dest=r/'candidate_snapshots'/n
    dest.parent.mkdir(exist_ok=True)
    with dest.open('xb') as f:f.write(data)

check('author_stdout_byte_replay',(r/'author_regression.stdout').read_bytes()==(p/'author_check_01.stdout').read_bytes())
check('author_mutation_stdout_byte_replay',(r/'author_mutations_replay.stdout').read_bytes()==(p/'author_mutations_01.stdout').read_bytes())
for n in ['author_regression','author_mutations_replay','spacetime_independent_run']:
    receipt=json.loads((r/(n+'.json')).read_text())
    check('capture_success_'+n,receipt['returncode']==0 and not receipt['timeout'])
    check('stderr_empty_'+n,(r/(n+'.stderr')).read_bytes()==b'')
sink=io.StringIO()
with contextlib.redirect_stdout(sink):
    independent=runpy.run_path(str(r/'source_first_check.py'))
    spacetime=runpy.run_path(str(r/'spacetime_independent.py'))
    author=runpy.run_path(str(p/'check_bi2.py'))

# Every 3D tensor entry from sealed fixed-frame reviewer computation.
size_map={independent['x']:author['A']**2,independent['y']:author['B']**2,
          independent['z']:author['C']**2}
zero('all_9_spatial_endomorphism_entries',
     independent['B'].subs(size_map)-s.diag(*author['rr']))
for i,name in enumerate(('gap31','gap32')):
    zero('gap_correspondence_'+str(i),independent[name].subs(size_map)-author['gaps'][i])
zero('projector_correspondence',independent['P']-author['P3'])
zero('horizontal_Lie_correspondence',independent['Lq'].subs(size_map)-author['Lie'])

# Compare author's moving-orthonormal Ricci to reviewer's fixed-frame Ricci,
# after converting the latter tensor by an explicit orthonormal basis change.
aa,bb,cc=author['lengths']
sp=spacetime
full_sub={sp['x'][i]:author['lengths'][i]**2 for i in range(3)}
full_sub.update({sp['k'][i]:author['k'][i] for i in range(3)})
full_sub[sp['lam']]=author['lam']
T=s.diag(1,1/aa,1/bb,1/cc)
review_orth=T*sp['solved'].subs(full_sub)*T
author_orth=author['Ric4'].subs(author['sub'])
zero('all_16_spacetime_Ricci_entries_distinct_frames',review_orth-author_orth)
zero('Hamiltonian_between_distinct_frames',sp['H'].subs(full_sub)-author['H'].subs(author['sub']))
saved=json.loads((p/'author_check_01.stdout').read_text())
for i,c in enumerate(saved['controls']):
    values=list(map(s.Rational,c['squared_sizes']))
    substitution=dict(zip((independent['x'],independent['y'],independent['z']),values))
    B=independent['B'].subs(substitution)
    rr=[s.factor(B[j,j]) for j in range(3)]
    check('control_Ricci_'+str(i),list(map(str,rr))==c['Ricci'])
    check('control_gaps_'+str(i),[str(s.factor(rr[2]-rr[j])) for j in range(2)]==c['gaps'])
    actual_Lie=independent['Lq'].subs(substitution)
    check('control_direct_descent_'+str(i),(actual_Lie==s.zeros(3))==c['direct_descent'])

print(json.dumps(dict(status='PASS',check_count=len(checks),checks=checks,
    candidate_sha256=hashes,source_seal_sha256=sha((r/'SOURCE_FIRST_SEAL.json').read_bytes()),
    full_spacetime_comparison_residual='zero in all 16 entries',
    evidence_type='exact comparison; author replays are regression only; fixed-frame Ricci is post-exposure implementation-distinct'),indent=2))
