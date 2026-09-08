"""Bounded post-exposure replay and distinct saved tensor comparison."""
import hashlib
import json
from pathlib import Path
import subprocess
import sympy as s

root=Path(__file__).resolve().parents[3]
review=Path(__file__).resolve().parent
step=review.parent
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
sealed=json.loads((review/'SOURCE_FIRST_SEAL.stdout').read_text())
for group in ['source_sha256','source_first_sha256']:
    for name,expected in sealed[group].items():
        assert sha(root/name)==expected, name
expected_author={
 'CANDIDATE_INITIAL.md':'71c8ce991929516b387a00dfca55c0459a7a0662cf78b26cb32b3e8dc2d857a4',
 'check_bg2.py':'0eef4df8c9c0223172be9c71ff9bccf9a6f08df43170e0f44ec7b938c8280bb9',
 'check_baseline.stdout':'5824304d062a4324a5d99567d1f1d8113de74f62f92fa2c7468e11d123efc830',
 'inherited_fulltensor_replay.stdout':'7444f2aabdcf89e436ef48997501c3f84f74b3fda1f830aa4fd79e6ba4f7c4b4'}
for name,digest in expected_author.items():assert sha(step/name)==digest,name
for line in (step/'SOURCE_PINS_SHA256SUMS').read_text().splitlines():
    digest,name=line.split(None,1)
    assert sha(root/name)==digest,name
script=str((step/'check_bg2.py').relative_to(root))
cases=[('check_baseline',[],0)]+[(f'mutation_{x}',['--mutant',x],1) for x in
  ['Q_plus','no_laplacian','omit_raising','omit_derivative_index','wrong_image_block']]+[
  (f'symbol_false_pass_{x}',['--mutant',x,'--symbol-only'],0) for x in
  ['omit_raising','omit_derivative_index','wrong_image_block']]
replays=[]
for name,flags,expected_rc in cases:
    cmd=['python3','-B',script,*flags]
    r=subprocess.run(cmd,cwd=root,capture_output=True,timeout=10)
    assert r.returncode==expected_rc,(name,r.returncode,r.stderr)
    same_out=r.stdout==(step/(name+'.stdout')).read_bytes()
    same_err=r.stderr==(step/(name+'.stderr')).read_bytes()
    assert same_out and same_err,name
    result=json.loads(r.stdout)
    replays.append({'name':name,'command':cmd,'returncode':r.returncode,
      'stdout_byte_identical':same_out,'stderr_byte_identical':same_err,
      'checks':result['count'],'false_checks':[c['name'] for c in result['checks'] if not c['pass']],
      'stdout':r.stdout.decode(),'stderr':r.stderr.decode()})

# Compare the new source-first direct Koszul derivative to every saved author
# baseline tensor entry, with an explicitly invertible relabeling of all6 K DOF.
ind=json.loads((review/'source_first_check_corrected.stdout').read_text())
author=json.loads((step/'check_baseline.stdout').read_text())
p,q=s.symbols('p q',positive=True)
a,b,c,d,e,f=s.symbols('k11 k22 k33 k12 k13 k23',real=True)
ours=dict(zip(['p','q','u','v','w','b','c','d'],[p,q,a,b,c,d,e,f]))
theirs=dict(zip(['p','q','x','y','z','u','v','w'],[p,q,a,b,c,d,e,f]))
S0=s.sympify(ind['full_direct_S'],locals=ours)
B0=s.sympify(ind['full_raised_Bdot'],locals=ours)
S1=s.sympify(author['anchors']['S'],locals=theirs)
B1=s.sympify(author['anchors']['Bdot'],locals=theirs)
assert all(s.expand(x)==0 for x in S0-S1)
assert all(s.expand(x)==0 for x in B0-B1)
srcY=s.diag(1,1,0)*B0*s.Matrix([0,0,1])/(q*(q-p))
auY=s.sympify(author['anchors']['Y'],locals=theirs)
assert all(s.simplify(x)==0 for x in srcY-auY)
print(json.dumps({'scope':'post-exposure regression/authentication and saved implementation-distinct tensor comparison',
  'author_sha256':expected_author,'source_first_seal_sha256':sha(review/'SOURCE_FIRST_SEAL.stdout'),
  'all_source_and_sealed_payloads_unchanged':True,
  'direct_full_tensor_comparison':'all9 S entries, all9 Bdot entries, all3 Y entries agree',
  'replay_count':len(replays),'full_mutations_caught':5,'symbol_only_false_passes_reproduced':3,
  'replays':replays},indent=2))
