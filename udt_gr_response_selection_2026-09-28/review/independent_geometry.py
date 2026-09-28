#!/usr/bin/env python3
"""Independent coordinate-metric checks; imports no producer implementation.

Question: do reciprocal projection and unadopted EH/R² variations select the
same equation? Smooth four-dimensional Lorentz witnesses, t>0, exact algebra.
Choices: displayed metrics/charts free-and-explored; geometry definitions and
variation identities pinned-by-THEORY at stated hypotheses. No source, fit,
boundary law or physical candidate is inferred. Compact support is used in the
analytic variation argument. One process/thread; no GPU, mesh or approximation.
Maximum claim: exact witnesses and regressions, not a generic classification.
"""
import hashlib
import json
import platform
from pathlib import Path
import sympy as s

t,x,y,z=s.symbols('t x y z', real=True)
coords=(t,x,y,z)
simp=lambda q:s.factor(s.cancel(s.simplify(q)))
checks=[]

def require(label, truth):
    if not truth:
        raise AssertionError(label)
    checks.append(label)

def zero(M):
    return all(simp(v)==0 for v in M)

def geometry(g):
    """Gamma and Ricci directly from components, including every index sum."""
    inv=g.inv()
    lower=[[[s.diff(g[a,b],coords[c])+s.diff(g[a,c],coords[b])-
              s.diff(g[b,c],coords[a]) for c in range(4)] for b in range(4)] for a in range(4)]
    G=[[[simp(sum(inv[a,d]*lower[d][b][c] for d in range(4))/2)
          for c in range(4)] for b in range(4)] for a in range(4)]
    Ric=s.zeros(4)
    for a in range(4):
        for b in range(4):
            Ric[a,b]=simp(sum(s.diff(G[c][a][b],coords[c])-s.diff(G[c][a][c],coords[b])+
                sum(G[c][a][b]*G[d][c][d]-G[d][a][c]*G[c][b][d] for d in range(4))
                for c in range(4)))
    R=simp(sum(inv[a,b]*Ric[a,b] for a in range(4) for b in range(4)))
    Hess=s.Matrix(4,4,lambda a,b:simp(s.diff(R,coords[a],coords[b])-
                  sum(G[c][a][b]*s.diff(R,coords[c]) for c in range(4))))
    box=simp(sum(inv[a,b]*Hess[a,b] for a in range(4) for b in range(4)))
    E1=(Ric-g*R/2).applyfunc(simp)
    E2=(2*R*Ric-g*R**2/2+2*(g*box-Hess)).applyfunc(simp)
    TF=lambda E:(E-g*sum(inv[a,b]*E[a,b] for a in range(4) for b in range(4))/4).applyfunc(simp)
    return dict(g=g,inv=inv,G=G,Ric=Ric,R=R,Hess=Hess,box=box,E1=E1,E2=E2,TF1=TF(E1),TF2=TF(E2))

# Original metric witness, not FLRW curvature formulas as input.
w=geometry(s.diag(-1,t,t,t))
require('R_zero_metric_witness',w['R']==0)
require('Ricci_nonzero_metric_witness',w['Ric']==s.diag(3/(4*t**2),1/(4*t),1/(4*t),1/(4*t)))
require('EH_TF_nonzero_witness',not zero(w['TF1']))
require('R_squared_TF_zero_witness',zero(w['TF2']))
require('R_squared_full_EL_zero_witness',zero(w['E2']))

# Nonconstant curvature probes derivative terms and catches omission mutations.
n=geometry(s.diag(-1,t**4,t**4,t**4))
require('nonconstant_scalar_curvature',n['R']==36/t**2)
require('box_scalar_curvature',n['box']==216/t**4)
require('R_squared_EL_nonconstant_metric',n['E2']==s.diag(-648/t**4,216,216,216))
require('R_squared_TF_nonconstant_metric',n['TF2']==s.diag(-324/t**4,-108,-108,-108))
tr2=simp(sum(n['inv'][a,b]*n['E2'][a,b] for a in range(4) for b in range(4)))
require('conformal_variation_trace_identity',simp(tr2-6*n['box'])==0)
require('catch_omitted_Hessian_in_TF',not zero(n['TF2']-2*n['R']*n['TF1']))
require('catch_EH_tracefactor_half_versus_quarter',not zero(n['E1']-n['TF1']))

# Exact homothety, not coordinate transformation or physical symmetry adoption.
c=s.symbols('c',positive=True)
scaled=geometry(c**2*n['g'])
require('Ricci_covariant_homothety_weight_zero',zero(scaled['Ric']-n['Ric']))
require('R_homothety_weight_minus_two',simp(scaled['R']-n['R']/c**2)==0)
require('EH_EL_covariant_weight_zero',zero(scaled['E1']-n['E1']))
require('R_squared_EL_covariant_weight_minus_two',zero(scaled['E2']-n['E2']/c**2))
require('catch_R_squared_EL_weight_zero',not zero(scaled['E2']-n['E2']))

# Independent finite reciprocal basis: all-pair completeness supplied analytically.
eta=s.diag(-1,1,1,1)
basis=[s.eye(4)[:,i] for i in range(4)]
pair_list=[(basis[0],basis[i]) for i in range(1,4)]
for i,j in ((1,2),(1,3),(2,3)):
    pair_list.append((basis[0],s.Rational(3,5)*basis[i]+s.Rational(4,5)*basis[j]))
for i in range(1,4):
    pair_list.append((s.Rational(5,3)*basis[0]+s.Rational(4,3)*basis[i],
                      s.Rational(4,3)*basis[0]+s.Rational(5,3)*basis[i]))
symbasis=[]
for a in range(4):
    for b in range(a,4):
        B=s.zeros(4); B[a,b]=1; B[b,a]=1
        symbasis.append(B)
rows=[]
for i,(u,v) in enumerate(pair_list):
    require('orthonormal_pair_'+str(i),(u.T*eta*u)[0]==-1 and
            (v.T*eta*v)[0]==1 and (u.T*eta*v)[0]==0)
    H=2*((eta*u)*(eta*u).T+(eta*v)*(eta*v).T)
    require('reciprocal_trace_zero_'+str(i),s.trace(eta*H)==0)
    rows.append([s.trace(eta*B*eta*H) for B in symbasis])
balance=s.Matrix(rows)
require('reciprocal_rank_nine',balance.rank()==9)
null=balance.nullspace()
require('reciprocal_annihilator_metric',len(null)==1 and
        null[0]==s.Matrix([-1,0,0,0,1,0,0,1,0,1]))
require('catch_one_pair_suffices',s.Matrix([rows[0]]).rank()!=9)

# Analytic flat-linearization anchor for source-first erratum. For h_xx=t^4,
# R^(1)=d_t² h_xx. Its Hessian derivative term is nonzero, scalar order four.
R1=s.diff(t**4,t,2)
H1=s.Matrix(4,4,lambda a,b:s.diff(R1,coords[a],coords[b]))
box1=sum(eta[a,b]*H1[a,b] for a in range(4) for b in range(4))
linear2=2*(eta*box1-H1)
require('R_squared_flat_linearization_nonzero',linear2==s.diag(0,-48,-48,-48))

result={
    'status':'PASS','checks':checks,'count':len(checks),
    'python':platform.python_version(),'sympy':s.__version__,
    'implementation_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'exposure':'Source-first definitions plus parent generic check-plan description; no producer implementation, proof, results or verdict read before this script.',
    'independence':'Own coordinate-Christoffel/Ricci implementation; known variation identity shared mathematically; no producer import. No reduced-action calculation.',
    'metric_witness':{'metric':'diag(-1,t,t,t), t>0','R':str(w['R']),
        'Ricci':str(w['Ric']),'TF_EH':str(w['TF1']),'EL_R_squared':str(w['E2'])},
    'nonconstant_witness':{'metric':'diag(-1,t**4,t**4,t**4), t>0','R':str(n['R']),
        'Box_R':str(n['box']),'EL_R_squared':str(n['E2']),'TF_R_squared':str(n['TF2'])},
    'flat_linearized_R_squared':str(linear2),
    'limits':'Exact symbolic witnesses only. Not a generic classification, physical UDT admission, full GR filter, independent derivation of all variational coefficients or flat stability.'}
print(json.dumps(result,indent=2))
