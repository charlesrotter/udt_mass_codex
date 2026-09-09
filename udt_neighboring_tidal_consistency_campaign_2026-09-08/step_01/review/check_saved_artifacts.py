"""Recompute saved matrices/kernel from generic bivector construction; no author imports."""
import contextlib
import io
import itertools
import json
from pathlib import Path
import runpy
import sympy as s

with contextlib.redirect_stdout(io.StringIO()):
    env=runpy.run_path(str(Path(__file__).with_name('compare_candidate_equations.py')))
z=env['z']; rows=z['rows']; basis=z['basis']; full=z['bianchi']
def b_row(l,i):
    return sum((s.LeviCivita(j,k,l)*rows[i,0,j,k]/2
                for j,k in itertools.product(range(1,4),repeat=2)),s.zeros(1,11))
es=list(itertools.combinations_with_replacement(range(1,4),2))
bs=[(1,1),(2,2),(1,2),(2,3),(3,1)]
param=s.Matrix.vstack(*[rows[i,0,0,j] for i,j in es],*[b_row(l,i) for l,i in bs])
assert param.det()!=0
targets=[]
for field in ['C','B']:
    for slot in [(1,1),(2,2),(1,2),(2,3),(3,1)]:
        t=s.zeros(3)
        i,j=slot
        t[i-1,j-1]=t[j-1,i-1]=1
        if i==j:t[2,2]=-1
        c=t if field=='C' else s.zeros(3)
        b=t if field=='B' else s.zeros(3)
        targets.append(s.Matrix([c[i-1,j-1] for i,j in es]+[b[l-1,i-1] for l,i in bs]))
P=param.inv()*s.Matrix.hstack(*targets)
T=s.diag(P,P,P,P)
expected=full*T
C=env['C'];B=env['B'];curl=env['curl']
cb=[sum((F(i,i,j) for i in range(1,4)),s.zeros(1,44)) for F in [C,B] for j in range(1,4)]
slots=[(1,1),(2,2),(1,2),(2,3),(3,1)]
cb += [C(0,i,j)+curl(B,i,j) for i,j in slots]
cb += [B(0,i,j)-curl(C,i,j) for i,j in slots]
expected_cb=s.Matrix.vstack(*cb)*T

root=Path(__file__).resolve().parents[1]
original=json.loads((root/'author_final.stdout').read_text())
def matrix(v):return s.Matrix([[s.Rational(e) for e in row] for row in v])
M=matrix(original['bianchi_matrix']);MCB=matrix(original['cb_equation_matrix'])
R=matrix(original['rref']);K=matrix(original['kernel_basis']).T
assert M==expected,'saved_bianchi_matrix_equals_independent_generic_tensor_map'
assert MCB==expected_cb,'saved_CB_equations_equal_independent_written_equation_map'
expected_rref,piv=M.rref()
assert R==expected_rref and list(piv)==original['pivot_columns']
assert K.shape==(40,24) and K.rank()==24
assert M*K==s.zeros(24,24)
free=[i for i in range(40) if i not in piv]
assert K[free,:]==s.eye(24)
assert original['bad_bianchi_residual']==list(map(str,z['bianchi']*z['bad']))
assert original['rank']==16 and original['full_einstein_rank']==20

decoder=json.JSONDecoder()
probe_stats=[]
for name in ['scaled_action','zero_kernel']:
    text=(Path(__file__).parent/f'author_{name}_falsepass.stdout').read_text()
    metadata,end=decoder.raw_decode(text)
    data,_=decoder.raw_decode(text[end:].lstrip())
    assert data['status']=='PASS' and len(data['checks'])==17
    details=dict(probe=name,author_status=data['status'],author_guard_count=len(data['checks']),
                 exact_mutation=metadata)
    if name=='zero_kernel':
        badK=matrix(data['kernel_basis']).T
        details['returned_kernel_rank']=badK.rank()
        details['correct_required_rank']=24
        assert badK.rank()==0
    else:
        # An explicit finite frame check gave d/dt of the transformed tensor;
        # a nonzero derivative cannot equal twice its true slot action.
        with contextlib.redirect_stdout(io.StringIO()):
            f=runpy.run_path(str(Path(__file__).with_name('frame_product_check.py')))
        diffs={str(k):str(f['transformed'][k]-2*f['correction'][k])
               for k in f['Q'] if f['transformed'][k]!=2*f['correction'][k]}
        assert diffs
        details['independent_finite_frame_rejects_scaled_action']=diffs
    probe_stats.append(details)
print(json.dumps(dict(status='PASS_BASELINE_ARTIFACTS_TWO_REAL_FALSE_PASSES_RETAINED',
    baseline=dict(bianchi_shape=list(M.shape),bianchi_rank=M.rank(),CB_shape=list(MCB.shape),
                  CB_rank=MCB.rank(),kernel_shape=list(K.shape),kernel_rank=K.rank(),
                  exact_full_matrices_and_rref_and_normalized_kernel_equal=True),
    probes=probe_stats),indent=2))
