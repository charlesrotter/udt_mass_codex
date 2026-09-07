"""PC2 initial-normal and invariant recipe identities; exact, not PDE proof."""
import argparse
from itertools import product
import json
import sys
import sympy as s
ap=argparse.ArgumentParser(); ap.add_argument('--mutant',choices=('free_normal','omit_projection'))
mode=ap.parse_args().mutant; guards=[]
def check(name,value):
    if not value:
        print(json.dumps(dict(status='FAIL',guard=name,mutant=mode,passed=guards)))
        raise SystemExit(1)
    guards.append(name)
r,s0,ax,ay,az=s.symbols('r s ax ay az',real=True)
f=s.symbols('f',positive=True); den=1+r*r+s0*s0
unit=s.Matrix([2*r/den,2*s0/den,(1-r*r-s0*s0)/den])
a=s.Matrix([ax,ay,az]); normal=-a.dot(unit)
if mode=='free_normal': normal=normal+1
check('normal_not_independent',s.factor(normal+a.dot(unit))==0)
q=s.factor(a.dot(a)-normal**2)
if mode=='omit_projection': q=a.dot(a)
check('initial_q_is_screen_square',s.factor(q-unit.cross(a).dot(unit.cross(a)))==0)
# The omitted stereographic pole is handled analytically by |u cross a|^2
# =|u|^2|a|^2-(u.a)^2 for every unit u; this chart is only a control.
check('unit_seed_sphere_control',s.factor(unit.dot(unit)-1)==0)
# Adapted orthonormal frame V=f(e0+e3). q=0 iff alpha wedge Vflat=0.
eta=(-1,1,1,1); ell=s.Matrix([-f,0,0,f])
alpha=s.Matrix([-az,ax,ay,az])
wedge=s.Matrix(4,4,lambda i,j:alpha[i]*ell[j]-alpha[j]*ell[i])
check('null_annihilation',(-az)*f+az*f==0)
check('screen_scalar',s.expand(sum(eta[i]*alpha[i]**2 for i in range(4))-ax*ax-ay*ay)==0)
check('pointwise_closure_kernel',all(s.expand(v.subs({ax:0,ay:0}))==0 for v in wedge)
      and wedge[0,1]==f*ax and wedge[0,2]==f*ay)
u,v,x,y=s.symbols('u v x y',real=True)
h=s.Function('H')(u,x,y); c=s.symbols('c',real=True); L=h+2*c
B=s.Function('b')(u,x,y) # positive b on retained region, no zero extension
logjet=s.Matrix([s.diff(B,w)/B for w in (u,x,y)])
gam_inv=s.diag(1/L,1,1); Ys=s.Matrix([-1/L,0,0]); fs=1/s.sqrt(L)
q_initial=s.simplify((logjet.T*gam_inv*logjet)[0]-(logjet.dot(Ys)/fs)**2)
q_ambient=(s.diff(B,x)**2+s.diff(B,y)**2)/B**2
check('full_spacelike_initial_scalar_matches_ambient',s.simplify(q_initial-q_ambient)==0)
# Source G355 connection: V=partial_v parallel, determinant -1, beta=-b du.
g=s.Matrix([[h,-1,0,0],[-1,0,0,0],[0,0,1,0],[0,0,0,1]])
gi=g.inv(); coord=(u,v,x,y); I=range(4)
G={(i,j,k):s.simplify(sum(gi[i,m]*(s.diff(g[m,j],coord[k])+s.diff(g[m,k],coord[j])-
    s.diff(g[j,k],coord[m])) for m in I)/2) for i,j,k in product(I,repeat=3)}
beta=s.Matrix([-B,0,0,0]); al=s.Matrix([s.diff(B,w)/B for w in coord])
check('full_recurrence_identity',all(s.simplify(s.diff(beta[j],coord[i])-
    sum(G[m,i,j]*beta[m] for m in I)-al[i]*beta[j])==0 for i,j in product(I,repeat=2)))
check('full_q_contraction',s.simplify((al.T*gi*al)[0]-q_ambient)==0)
D=q_ambient*(gi*beta)
div=s.simplify(sum(s.diff(D[i],coord[i])+sum(G[i,i,j]*D[j] for j in I) for i in I))
acc=[s.simplify(sum(D[j]*(s.diff(D[i],coord[j])+sum(G[i,j,k]*D[k] for k in I)) for j in I)) for i in I]
check('current_divergence_and_affine_acceleration',div==0 and acc==[0,0,0,0])
check('invariant_q_and_root_scale',s.diff(B,v)==0 and s.diff(q_ambient,v)==0)
print(json.dumps(dict(status='PASS',mutant=mode,guards=guards,guard_count=len(guards),
    initial_scalar=str(q_initial),arithmetic='exact symbolic, no floating tolerance',
    python=sys.version,sympy=s.__version__,
    scope='algebraic initial-data and already harmonic-class controls; general propagation uses analytic proof'),
    indent=2,sort_keys=True))
