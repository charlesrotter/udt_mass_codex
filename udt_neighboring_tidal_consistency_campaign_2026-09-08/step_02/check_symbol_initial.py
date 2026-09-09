"""Exact rank-one first-Weyl derivative symbol; conditional NT1 matrix reuse."""
import argparse,json
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser()
ap.add_argument('--mutant',choices=('drop_bianchi','wrong_null_sign','drop_mixed'))
mode=ap.parse_args().mutant
p=Path(__file__).resolve().parents[1]/'step_01/author_repaired.stdout'
data=json.loads(p.read_text())
M=s.Matrix([[s.Rational(x) for x in row] for row in data['bianchi_matrix']])
checks=[]
def check(name,truth):
 if not truth:
  print(json.dumps({'status':'FAIL','mutant':mode,'failed_guard':name,'passed':checks}),flush=True)
  raise SystemExit(1)
 checks.append(name)
 print(json.dumps({'passed_guard':name}),file=__import__('sys').stderr,flush=True)
def symbol(nu):
 if mode=='drop_bianchi':return s.zeros(24,10)
 return sum((nu[i]*M[:,10*i:10*(i+1)] for i in range(4)),s.zeros(24,10))
timelike=(1,0,0,0);spacelike=(0,0,0,1)
null=(1,0,0,1 if mode=='wrong_null_sign' else -1)
At,As,An=(symbol(v) for v in (timelike,spacelike,null))
check('timelike_nonzero_curvature_factor_impossible',At.rank()==10)
check('spacelike_nonzero_curvature_factor_impossible',As.rank()==10)
check('null_symbol_rank_eight',An.rank()==8)
a,b=s.symbols('a b',real=True)
P=s.Matrix([a,-a,b,0,0,b,-b,-a,0,0])
if mode=='drop_mixed':P[5:10,0]=s.zeros(5,1)
V=P.jacobian((a,b));N=s.Matrix.hstack(*An.nullspace())
check('both_explicit_null_polarizations_satisfy_full_bianchi',An*V==s.zeros(24,2))
check('two_independent_full_null_polarizations',V.rank()==2 and N.rank()==2 and s.Matrix.hstack(V,N).rank()==2)
check('all_nonzero_real_amplitudes_nonzero_curvature',V.T*V==s.diag(4,3))
# The Gram matrix here is only a Euclidean coordinate injectivity check,
# not a metric energy, invariant curvature magnitude or positivity law.
print(json.dumps({'status':'PASS','mutant':mode,'checks':checks,'sympy':s.__version__,
 'source':'reviewed NT1 exact matrix, reused conditional dependency not independent reconstruction',
 'canonical_covectors':{'timelike':timelike,'spacelike':spacelike,'null':null},
 'symbol_ranks':[At.rank(),As.rank(),An.rank()],
 'null_P_coefficients':list(map(str,P)),'null_kernel':[[str(x) for x in row] for row in V.tolist()],
 'symbol_matrices':{k:[[str(x) for x in row] for row in A.tolist()] for k,A in [('timelike',At),('spacelike',As),('null',An)]},
 'limits':'restricted factorized first jet, not general physical mode count or metric realization'},indent=2))
