"""Compare the written candidate with generic bivector derivatives, before code exposure."""
import contextlib
import io
import itertools
import json
import pathlib
import runpy
import sys
import sympy as s

with contextlib.redirect_stdout(io.StringIO()):
    z=runpy.run_path(str(pathlib.Path(__file__).with_name('source_first_check.py')))
dr=z['derivative_row']; dlam=z['dlam']; full=z['bianchi']
def C(m,i,j):
    return dr(m,i,0,0,j)+(dlam[m,:]/3 if i==j else s.zeros(1,44))
def B(m,l,i):
    return sum((s.LeviCivita(j,k,l)*dr(m,i,0,j,k)/2
                for j,k in itertools.product(range(1,4),repeat=2)),s.zeros(1,44))
def curl(F,i,j):
    return sum((s.LeviCivita(i,k,l)*F(k,l,j)+s.LeviCivita(j,k,l)*F(k,l,i)
                for k,l in itertools.product(range(1,4),repeat=2)),s.zeros(1,44))/2
mutant=sys.argv[1] if len(sys.argv)>1 else 'baseline'
eqs=[sum((F(i,i,j) for i in range(1,4)),s.zeros(1,44))
     for F in (C,B) for j in range(1,4)]
stf_slots=[(1,1),(1,2),(1,3),(2,2),(2,3)]
eqs += [C(0,i,j)+(1 if mutant!='flip_B_curl_sign' else -1)*curl(B,i,j)
        for i,j in stf_slots]
eqs += [B(0,i,j)-curl(C,i,j) for i,j in stf_slots]
if mutant=='omit_divergence':
    eqs=eqs[1:]
candidate=s.Matrix.vstack(*eqs)
joined=s.Matrix.vstack(candidate,dlam)
full_kernel=s.Matrix.hstack(*full.nullspace())
res=joined*full_kernel
stats=dict(mutant=mutant,candidate_weyl_rank=(candidate*z['fixed_scalar_basis']).rank(),
    candidate_plus_scalar_rank=joined.rank(),full_bianchi_rank=full.rank(),
    stacked_rank=s.Matrix.vstack(joined,full).rank(),
    max_residual_on_full_kernel=max(abs(v) for v in res),
    obstruction_candidate_residual=list(candidate*z['bad']))
print(json.dumps(stats,default=str,indent=2),flush=True)
assert (candidate*z['fixed_scalar_basis']).rank()==16,'sixteen_independent_equations'
assert joined.rank()==full.rank()==s.Matrix.vstack(joined,full).rank()==20,'full_row_space_equivalence'
assert res==s.zeros(joined.rows,full_kernel.cols),'candidate_accepts_all_full_bianchi_derivatives'
print('PASS: complete exact equation-map equality; finite first-jet algebra only')
