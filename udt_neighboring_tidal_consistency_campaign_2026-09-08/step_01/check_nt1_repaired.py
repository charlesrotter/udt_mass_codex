"""Exact first-curvature-derivative algebra; not a PDE existence test.

Reuses the accepted SC3 tensor/record implementation as disclosed regression.
All new derivatives, rank operations and connection action below are explicit.
"""
import argparse
from contextlib import redirect_stdout
from fractions import Fraction as F
from itertools import product, combinations
import io
import json
from pathlib import Path
import runpy
import sys

ap = argparse.ArgumentParser()
ap.add_argument('--mutant', choices=('omit_bianchi', 'wrong_cycle',
                                   'omit_connection', 'drop_divergence'))
mode = ap.parse_args().mutant
root = Path(__file__).resolve().parents[2]
original_argv = sys.argv[:]
sys.argv = ['accepted_sc3_replay']
capture = io.StringIO()
with redirect_stdout(capture):
    old = runpy.run_path(str(root / 'udt_shared_readout_metric_constraint_campaign_2026-09-06/step_03/check_exact.py'))
sys.argv = original_argv
tensor, record, constraints = (old[x] for x in ('tensor', 'record', 'constraints'))
I = list(product(range(4), repeat=4))
triples = list(combinations(range(4), 3))
pairs = list(combinations(range(4), 2))
eta = (-1, 1, 1, 1)
passed = []

def check(name, truth):
    if not truth:
        print(json.dumps({'status':'FAIL','guard':name,'mutant':mode,
                          'passed_before_failure':passed,'accepted_sc3_actual_stdout':capture.getvalue()}))
        raise SystemExit(1)
    passed.append(name)
    print(json.dumps({'passed_guard':name}),file=sys.stderr,flush=True)

def rref(matrix):
    a = [list(map(F,row)) for row in matrix]
    p = []
    for col in range(len(a[0])):
        k = next((j for j in range(len(p),len(a)) if a[j][col]), None)
        if k is None: continue
        r = len(p); a[r],a[k]=a[k],a[r]
        d=a[r][col]; a[r]=[x/d for x in a[r]]
        for j in range(len(a)):
            if j!=r and a[j][col]:
                d=a[j][col];a[j]=[x-d*y for x,y in zip(a[j],a[r])]
        p.append(col)
        if len(p)==len(a): break
    return a,p

zero = {i:F(0) for i in I}
values=[]
for k in range(5):
    v=[F(0)]*11
    if k<2: v[k]=1;v[2]=-1
    else: v[k+1]=1
    values.append(v)
for k in range(5):
    v=[F(0)]*11;v[6+k]=1;values.append(v)
W=[tensor(v)[0] for v in values]
K=tensor([-1,-1,-1]+[0]*8)[0]
check('ten_weyl_basis_tracefree',all(sum(eta[a]*q[a,b,c,a] for a in range(4))==0
    for q in W for b,c in product(range(4),repeat=2)))
check('all_basis_records_pass_eventwise',all(not any(constraints(record(q))) for q in W+[K]))

def bianchi(J):
    if mode=='omit_bianchi': return [F(0)]*24
    s=-1 if mode=='wrong_cycle' else 1
    return [J[m][a,b,c,d]+J[a][b,m,c,d]+s*J[b][m,a,c,d]
            for m,a,b in triples for c,d in pairs]

def divergence(J):
    return [sum(eta[a]*J[a][a,b,c,d] for a in range(4))
            for b in range(4) for c,d in pairs]

def derivative_basis(basis):
    return [[q if m==n else zero for m in range(4)] for n in range(4) for q in basis]

def columns_to_rows(columns): return [list(x) for x in zip(*columns)]

Jbasis=derivative_basis(W)
M=columns_to_rows([bianchi(j) for j in Jbasis])
D=columns_to_rows([divergence(j) for j in Jbasis])
R,piv=rref(M);RD,pivD=rref(D)
check('weyl_differential_rank_sixteen',len(piv)==16)
check('divergence_same_kernel',len(pivD)==16 and len(rref(M+D)[1])==16)

def cb_equations(J):
    C=[{(i,j):q[i,0,0,j] for i,j in product(range(1,4),repeat=2)} for q in J]
    B=[{(l,i):sum(F(old['eps'](j,k,l),2)*q[i,0,j,k]
        for j,k in product(range(1,4),repeat=2))
        for l,i in product(range(1,4),repeat=2)} for q in J]
    def curl(A,i,j):
        return sum(F(old['eps'](i,k,l),2)*A[k][l,j]
                   +F(old['eps'](j,k,l),2)*A[k][l,i]
                   for k,l in product(range(1,4),repeat=2))
    div=[sum(A[i][i,j] for i in range(1,4)) for A in (C,B) for j in range(1,4)]
    if mode=='drop_divergence': div=[F(0)]*6
    slots=((1,1),(2,2),(1,2),(2,3),(3,1))
    return div+[C[0][i,j]+curl(B,i,j) for i,j in slots]+[B[0][i,j]-curl(C,i,j) for i,j in slots]

MCB=columns_to_rows([cb_equations(j) for j in Jbasis])
check('explicit_six_divergences_ten_evolution_equivalent',
      len(rref(MCB)[1])==16 and len(rref(M+MCB)[1])==16)
einstein_basis=derivative_basis(W+[K])
Mfull=columns_to_rows([bianchi(j) for j in einstein_basis])
scalar_rows=[[F(i==11*m+10) for i in range(44)] for m in range(4)]
check('full_einstein_derivative_rank_twenty',len(rref(Mfull)[1])==20)
check('constant_scalar_already_implied',len(rref(Mfull+scalar_rows)[1])==20)
free=[i for i in range(40) if i not in piv]
kernel=[]
for f in free:
    v=[F(0)]*40;v[f]=1
    for r,c in enumerate(piv):v[c]=-R[r][f]
    kernel.append(v)
check('twentyfour_full_kernel_vectors',len(kernel)==24 and all(
    sum(a*b for a,b in zip(row,v))==0 for row in M for v in kernel))
check('kernel_vectors_really_independent',len(rref(kernel)[1])==24 and all(
    kernel[r][f]==F(r==s) for r in range(24) for s,f in enumerate(free)))

# Concrete pointwise-compatible but first-neighborhood-incompatible variation.
# E=x1 diag(1,-1,0)-Lambda/3 I, B=0; at x1=0 Weyl vanishes.
badW=tensor([1,-1,0]+[0]*8)[0]
badJ=[zero,badW,zero,zero]
baddiv=divergence(badJ)
check('bad_spatial_variation_divergence_one',baddiv[0*6+pairs.index((0,1))]==1)
check('bad_spatial_variation_rejected',any(bianchi(badJ)))
check('bad_family_eventwise_not_rejected',all(not any(constraints(record(
    {i:x*badW[i]+k*K[i] for i in I}))) for x in (F(-2),F(0),F(3,7)) for k in (F(0),F(2))))

def action(q,A):
    return {idx:sum(A[r][idx[s]]*q[idx[:s]+(r,)+idx[s+1:]]
                    for s in range(4) for r in range(4)) for idx in I}

generators=[]
for a,b in pairs:
    A=[[F(0)]*4 for _ in range(4)]; A[a][b]=1;A[b][a]=-eta[a]*eta[b]
    generators.append(A)
check('six_lorentz_generator_metric_compatibility',all(
    eta[a]*A[a][b]+eta[b]*A[b][a]==0 for A in generators for a,b in product(range(4),repeat=2)))
check('constant_curvature_connection_action_zero',all(not any(action(K,A).values()) for A in generators))
check('zero_weyl_connection_action_zero',all(not any(action(zero,A).values()) for A in generators))

# Independent finite-frame polynomial anchor, not action-minus-itself.
# A rational Lorentz family is L(t)=N(t)/(1+s*t*t) on each two-plane,
# with L'(0)=2*A. The numerator of a four-slot transformed tensor is a
# degree<=8 polynomial; nine exact rational nodes determine its derivative.
nodes=[F(i,10) for i in range(-4,5)]
vandermonde=[[x**k for x in nodes]+[F(k==1)] for k in range(9)]
rv,pv=rref(vandermonde)
check('finite_frame_interpolation_rank_nine',pv==list(range(9)))
weights=[row[-1] for row in rv]
qgeneric={idx:sum((k+1)*q[idx] for k,q in enumerate(W)) for idx in I}
finite_derivatives=[]
finite_metric_ok=True
for (a,b),A in zip(pairs,generators):
    s=eta[a]*eta[b]
    matrices=[]
    for t in nodes:
        denom=1+s*t*t
        N=[[denom*F(i==j) for j in range(4)] for i in range(4)]
        N[a][a]=N[b][b]=1-s*t*t
        N[a][b]=2*t;N[b][a]=-2*s*t
        finite_metric_ok &= all(sum(eta[r]*N[r][i]*N[r][j] for r in range(4))
                               ==denom**2*eta[i]*F(i==j)
                               for i,j in product(range(4),repeat=2))
        matrices.append(N)
    Aq=action(qgeneric,A)
    for ab in pairs:
        for cd in pairs:
            idx=ab+cd
            samples=[]
            for N in matrices:
                total=F(0)
                choices=[[r for r in range(4) if N[r][i]] for i in idx]
                for rs in product(*choices):
                    val=qgeneric[rs]
                    for slot in range(4):val*=N[rs[slot]][idx[slot]]
                    total+=val
                samples.append(total)
            actual=sum(w*y for w,y in zip(weights,samples))
            finite_derivatives.append((actual,2*Aq[idx]))
check('finite_rational_frames_preserve_metric',finite_metric_ok)
check('finite_frame_derivative_matches_slot_action',
      all(a==b for a,b in finite_derivatives) and any(a for a,b in finite_derivatives))
# A rotating/boosting frame on a parallel-curvature jet gives raw derivatives
# action(A)Q, not zero. Subtracting all four slot terms restores covariant zero.
frame_controls=[]
for mu in range(4):
    for A in generators:
        for q in W:
            Aq=action(q,A)
            raw=[zero]*4;raw[mu]=Aq
            corrected=[dict(j) for j in raw]
            if mode!='omit_connection':
                corrected[mu]={i:raw[mu][i]-Aq[i] for i in I}
            frame_controls.append((any(bianchi(raw)),not any(bianchi(corrected))))
check('raw_frame_derivatives_can_false_fail',any(a for a,b in frame_controls))
check('all_slot_connection_correction',all(b for a,b in frame_controls))

scalarJ=[K,zero,zero,zero]
check('changing_scalar_is_rejected',any(bianchi(scalarJ)))
print(json.dumps({'status':'PASS','mutant':mode,'checks':passed,
    'basis_order':['C11-C33','C22-C33','C12','C23','C31','B11-B33','B22-B33','B12','B23','B31'],
    'derivative_column_order':'mu=0,1,2,3 each ten basis slots',
    'bianchi_row_order':[(m,a,b,c,d) for m,a,b in triples for c,d in pairs],
    'bianchi_matrix':[[str(x) for x in row] for row in M],
    'cb_equation_matrix':[[str(x) for x in row] for row in MCB],
    'rref':[[str(x) for x in row] for row in R], 'pivot_columns':piv,
    'kernel_basis':[[str(x) for x in row] for row in kernel],
    'rank':len(piv),'first_weyl_derivative_dimension':40,'kernel_dimension':len(free),
    'full_einstein_rank':len(rref(Mfull)[1]),
    'bad_bianchi_residual':list(map(str,bianchi(badJ))),
    'bad_divergence':list(map(str,baddiv)),
    'frame_controls':len(frame_controls),'raw_frame_false_failures':sum(a for a,b in frame_controls),
    'finite_frame_derivative_anchors':len(finite_derivatives),
    'finite_frame_nonzero_derivatives':sum(bool(a) for a,b in finite_derivatives),
    'accepted_sc3_actual_stdout':capture.getvalue(),
    'scope':'exact necessary first-jet constraints, not sufficient Einstein development or instrument eligibility'},indent=2))
