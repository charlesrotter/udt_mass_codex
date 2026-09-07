"""Exploration: full first-order root tangent and ambient parallel-seed test."""
import itertools,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from tensor_geometry import geometry,quadratic
import sympy as s
u,v,x,y,e=s.symbols('u v x y epsilon', real=True)
coords=(u,v,x,y)
H=x**3-3*x*y**2-2*e*v*y
g=s.Matrix([[H,-1,0,e*x**2],[-1,0,0,0],[0,0,1,0],[e*x**2,0,0,1]])
gi,G,R,Ric=geometry(g,coords)
# First-order Ricci vanishes; Weyl subtraction has no zeroth/first contribution.
B,dual=quadratic(g,R)
B0={k:s.factor(z.subs(e,0)) for k,z in B.items()}
dB={k:s.factor(s.diff(z,e).subs(e,0)) for k,z in B.items()}
N=B0[0,0,0,0]
# beta=-N^(1/4) du; encode delta(beta)/beta_u as a covector r.
r=[s.factor(dB[i,0,0,0]/N/(4 if i==0 else 1)) for i in range(4)]
def tangent(k):
    return s.factor(N*sum(r[k[j]]*s.prod(s.KroneckerDelta(k[h],0) for h in range(4) if h!=j) for j in range(4)))
bad={str(k):str(s.factor(dB[k]-tangent(k))) for k in B if s.factor(dB[k]-tangent(k))!=0}
# For a parallel field V0=partial_v, deltaV components a: full integrability.
a=s.symbols('a0:4')
eq=[s.factor(sum(R[i,j,c,d].subs(e,0)*a[c] for c in range(4))+s.diff(R[i,j,1,d],e).subs(e,0)) for i,j,d in itertools.product(range(4),repeat=3)]
sol=s.linsolve(eq,a)
print(json.dumps({'sympy':s.__version__,'ricci':str(Ric),'linearized_ricci':str(Ric.diff(e).subs(e,0)), 'B0_nonzero':{str(k):str(z) for k,z in B0.items() if z!=0},'dB_nonzero':{str(k):str(z) for k,z in dB.items() if z!=0},'root_relative_tangent':list(map(str,r)),'full256_tangent_defects':bad,'full_curvature_parallel_integrability':str(sol)},indent=2))
