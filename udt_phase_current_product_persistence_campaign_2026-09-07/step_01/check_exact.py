"""PC1 exact tensor and general spacelike-graph controls; not a PDE proof."""
import argparse
import contextlib
import io
from itertools import product
import json
from pathlib import Path
import runpy
import sys
import sympy as s
ap=argparse.ArgumentParser()
ap.add_argument('--mutant',choices=('drop_dual','wrong_K_sign','erase_scalar'))
mode=ap.parse_args().mutant
guards=[]
def check(name,condition):
    if not condition:
        print(json.dumps(dict(status='FAIL',guard=name,mutant=mode,passed=guards)))
        raise SystemExit(1)
    guards.append(name)
def zero(x): return s.simplify(x)==0
with contextlib.redirect_stdout(io.StringIO()):
    alg=runpy.run_path(str(Path(__file__).with_name('diagnose_weyl.py')))
a=alg['a']; v=a['v']; I=range(4); J=range(1,4); eta=alg['eta']
rho,p,q=v[2],v[8],v[7]
R,W,B=alg['R'],alg['W'],dict(alg['B'])
check('complete_seed_linear_rank_eight',a['A'].rank()==8)
expected=(-p,p,rho,-q,0,0,-q,q,p,0,0)
check('entire_three_parameter_solution',all(zero(x-y) for x,y in zip(a['solution'],expected)))
if mode=='erase_scalar':
    R={z:x.subs(rho,0) for z,x in R.items()}
check('scalar_not_erased',zero(sum(eta[t]*R[t,0,0,t] for t in I)-rho))
check('ambient_annihilation_iff_scalar_zero',
      all(zero((R[t,u,0,d]+R[t,u,3,d]).subs(rho,0)) for t,u,d in product(I,repeat=3))
      and zero(R[0,3,0,0]+R[0,3,3,0]-rho))
if mode=='drop_dual':
    B={(a,b,c,d):s.expand(sum(eta[e]*eta[h]*W[a,e,c,h]*W[b,e,d,h]
        for e,h in product(I,repeat=2))) for a,b,c,d in product(I,repeat=4)}
l=(-1,0,0,1)
check('full_fourth_power_coefficient',all(
    zero(B[t,u,c,d].subs(rho,0)-4*(p*p+q*q)*l[t]*l[u]*l[c]*l[d])
    for t,u,c,d in product(I,repeat=4)))
check('nonzero_scalar_root_obstruction',
      zero(B[1,1,1,1]-2*rho*rho/3) and zero(B[1,0,0,0])
      and zero(B[2,0,0,0]) and zero(B[0,0,0,0]-2*rho*rho/3-4*(p*p+q*q)))
check('zero_tensor_excluded_separately',all(zero(x.subs({rho:0,p:0,q:0})) for x in B.values()))
u,vv,x,y,c=s.symbols('u v x y c',real=True)
z=(u,vv,x,y); H=s.Function('H')(u,x,y); L=H+2*c
g=s.Matrix([[H,-1,0,0],[-1,0,0,0],[0,0,1,0],[0,0,0,1]])
inv=g.inv()
G={(a,b,d):s.simplify(sum(inv[a,e]*(s.diff(g[e,b],z[d])+s.diff(g[e,d],z[b])-
       s.diff(g[b,d],z[e])) for e in I)/2) for a,b,d in product(I,repeat=3)}
T=s.Matrix([[1,0,0],[-c,0,0],[0,1,0],[0,0,1]])
n=s.Matrix([1,H+c,0,0])/s.sqrt(L)
ell=s.Matrix([0,1,0,0]); gamma=s.simplify(T.T*g*T)
check('induced_full_spacelike_metric',gamma==s.diag(L,1,1))
check('future_unit_normal',zero((n.T*g*n)[0]+1) and
      all(zero(t) for t in T.T*g*n) and zero((n.T*g*ell)[0]+1/s.sqrt(L)))
K=s.zeros(3)
for i,j in product(range(3),repeat=2):
    nab=s.Matrix([sum(T[b,i]*(s.diff(n[a],z[b])+sum(G[a,b,d]*n[d] for d in I))
                     for b in I) for a in I])
    K[i,j]=s.simplify(-(nab.T*g*T[:,j])[0])
if mode=='wrong_K_sign': K=-K
expectedK=s.Matrix([[s.diff(H,u),s.diff(H,x),s.diff(H,y)],
                    [s.diff(H,x),0,0],[s.diff(H,y),0,0]])/(2*s.sqrt(L))
check('K_from_full_ambient_definition',all(zero(t) for t in K-expectedK))
coords=(u,x,y); gi=gamma.inv()
conn={(a,b,d):s.simplify(sum(gi[a,e]*(s.diff(gamma[e,b],coords[d])+s.diff(gamma[e,d],coords[b])-
       s.diff(gamma[b,d],coords[e])) for e in range(3))/2)
      for a,b,d in product(range(3),repeat=3)}
f=1/s.sqrt(L); Y=s.Matrix([-1/L,0,0])
check('full_seed_decomposition',all(zero(t) for t in f*n+T*Y-ell))
check('null_seed_spatial_norm',zero((Y.T*gamma*Y)[0]-f*f))
check('normal_seed_equations',all(zero(s.diff(f,coords[i])-(K*Y)[i]) for i in range(3)))
check('tangential_seed_equations',all(zero(s.diff(Y[a],coords[i])+
      sum(conn[a,i,d]*Y[d] for d in range(3))-f*(gi*K)[a,i]) for a,i in product(range(3),repeat=2)))
ric=s.zeros(3)
for i,j in product(range(3),repeat=2):
    ric[i,j]=s.simplify(sum(s.diff(conn[a,i,j],coords[a])-s.diff(conn[a,i,a],coords[j])+
        sum(conn[a,a,b]*conn[b,i,j]-conn[a,j,b]*conn[b,i,a] for b in range(3)) for a in range(3)))
scalar=s.simplify(s.trace(gi*ric)); tr=s.simplify(s.trace(gi*K))
norm=s.simplify(s.trace(gi*K*gi*K))
ham=s.simplify(scalar+tr*tr-norm)
check('original_hamiltonian_residual',zero(ham+(s.diff(H,x,2)+s.diff(H,y,2))/L))
stress=K-gamma*tr
mom=[s.simplify(sum(gi[j,j]*(s.diff(stress[i,j],coords[j])-
      sum(conn[a,j,i]*stress[a,j]+conn[a,j,j]*stress[i,a] for a in range(3))) for j in range(3)))
     for i in range(3)]
# Momentum for general nonharmonic H need not vanish; compare original residual.
check('original_momentum_residual',zero(mom[0]-(s.diff(H,x,2)+s.diff(H,y,2))/(2*s.sqrt(L)))
      and all(zero(t) for t in mom[1:]))
cubic=x**3-3*x*y**2
point={u:0,x:1,y:0,c:2}
check('nonempty_regular_harmonic_patch',
      s.diff(cubic,x,2)+s.diff(cubic,y,2)==0 and (cubic+2*c).subs(point)>0
      and (s.diff(cubic,x,2)**2+s.diff(cubic,x,y)**2).subs(point)>0)
print(json.dumps(dict(status='PASS',mutant=mode,guards=guards,guard_count=len(guards),
    arithmetic='exact symbolic, no floating tolerance',python=sys.version,sympy=s.__version__,
    seed_rank=a['A'].rank(),solution=list(map(str,expected)),
    gamma=str(gamma),K=str(K),hamiltonian=str(ham),momentum=list(map(str,mom)),
    f=str(f),Y=list(map(str,Y)),scalar_three=str(scalar),
    scope='initial data and algebra only; no recurrence normal derivative or propagation proof'),
    indent=2,sort_keys=True))
