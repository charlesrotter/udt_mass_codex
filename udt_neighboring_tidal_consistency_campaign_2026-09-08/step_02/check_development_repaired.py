"""Exact local Ricci-flat realization; reused coordinate tensor methods only."""
import argparse, itertools, json, runpy, sys
from pathlib import Path
import sympy as s
ap=argparse.ArgumentParser()
ap.add_argument('--mutant',choices=('nonharmonic','wrong_K_sign','omit_Hu','double_curvature'))
mode=ap.parse_args().mutant
root=Path(__file__).resolve().parents[2]
geometry=runpy.run_path(str(root/'udt_recipe_restrictiveness_campaign_2026-09-07/tensor_geometry.py'))['geometry']
checks=[]
def z(q):return s.simplify(q)==0
def check(name,truth):
 if not truth:
  print(json.dumps({'status':'FAIL','mutant':mode,'failed_guard':name,'passed':checks}),flush=True)
  raise SystemExit(1)
 checks.append(name)
 print(json.dumps({'passed_guard':name}),file=sys.stderr,flush=True)
u,v,x,y=s.symbols('u v x y',real=True)
a,b,eps=s.symbols('a b epsilon',real=True)
A=s.Function('A')(u);F=s.Function('F')(u)
H=A*(x*x-y*y)+2*F*x*y
check('declared_free_profiles_live_in_actual_family',A==s.Function('A')(u) and F==s.Function('F')(u) and A!=F and H.has(A,F) and s.diff(H,u).has(s.diff(A,u)) and s.diff(H,u).has(s.diff(F,u)) and s.diff(H,u,2).has(s.diff(A,u,2)) and s.diff(H,u,2).has(s.diff(F,u,2)))
if mode=='nonharmonic':H+=eps*u*x*x
q=(u,v,x,y);ix=range(4)
g=s.Matrix([[H,-1,0,0],[-1,0,0,0],[0,0,1,0],[0,0,0,1]])
gi,G,Q,Ric=geometry(g,q)
check('full_neighborhood_Ricci_flat_not_only_u_zero',all(z(t) for t in Ric))
check('nondegenerate_Lorentz_block',g.det()==-1 and s.det(g[:2,:2])==-1)
Hess=s.hessian(H,(x,y))
check('full_coordinate_curvature_transverse_Hessian',all(z(Q[i,0,0,j]+Hess[i-2,j-2]/2) for i in (2,3) for j in (2,3)))
# Curvature outside the transverse/u antisymmetric pairs must also vanish.
def expected_Q(i,j,k,l):
 if i in (2,3) and j==0 and k==0 and l in (2,3):return -Hess[i-2,l-2]/2
 if j in (2,3) and i==0:return -expected_Q(j,i,k,l)
 if k in (2,3) and l==0:return -expected_Q(i,j,l,k)
 return s.S(0)
check('all_256_curvature_components',all(z(Q[t]-expected_Q(*t)) for t in itertools.product(ix,repeat=4)))
# Columns are the supplied orthonormal frame e0,e1,e2,e3.
e=s.Matrix([[1,0,0,-1],[(H+1)/2,0,0,(1-H)/2],[0,1,0,0],[0,0,1,0]])
eta=s.diag(-1,1,1,1)
check('full_spacetime_orthonormal_frame',all(z(t) for t in e.T*g*e-eta))
sub={s.diff(A,u):-a,s.diff(F,u):-b,A:0,F:0,u:0,v:0,x:0,y:0}
at=lambda t:s.simplify(t.subs(sub,simultaneous=True))
Qp={t:at(Q[t]) for t in itertools.product(ix,repeat=4)}
check('Weyl_zero_event_all_components',all(t==0 for t in Qp.values()))
ep=e.subs({A:0,F:0,u:0,v:0,x:0,y:0},simultaneous=True)
nonzero={i:[(r,ep[r,i]) for r in ix if ep[r,i]!=0] for i in ix}
dQ={(mu,)+t:at(s.diff(Q[t],q[mu])) for mu in ix for t in itertools.product(ix,repeat=4)}
def transform_derivative(mu,i,j,k,l):
 return s.expand(sum(w0*w1*w2*w3*w4*dQ[r0,r1,r2,r3,r4]
  for (r0,w0),(r1,w1),(r2,w2),(r3,w3),(r4,w4) in itertools.product(nonzero[mu],nonzero[i],nonzero[j],nonzero[k],nonzero[l])))
C=s.Matrix([[a,b,0],[b,-a,0],[0,0,0]])
B=s.Matrix([[b,-a,0],[-a,-b,0],[0,0,0]])
def P(i,j,k,l):
 if i==j or k==l:return s.S(0)
 if i==0:return -P(j,i,k,l)
 if l==0:return -P(i,j,l,k)
 if j==0 and k==0:return C[i-1,l-1]
 if j==0:return sum(s.LeviCivita(k-1,l-1,m)*B[m,i-1] for m in range(3))
 if k==0:return P(k,l,i,j)
 return sum(s.LeviCivita(i-1,j-1,m)*s.LeviCivita(k-1,l-1,n)*C[m,n] for m in range(3) for n in range(3))
nu=(1,0,0,-1);factor=2 if mode=='double_curvature' else 1
check('all_1024_first_jet_components_match_normalized_null_factor',all(z(transform_derivative(mu,*t)-factor*nu[mu]*P(*t)) for mu in ix for t in itertools.product(ix,repeat=4)))
check('nonzero_jet_exactly_when_amplitudes_nonzero',s.expand(sum(P(*t)**2 for t in itertools.product(ix,repeat=4)))==32*(a*a+b*b))
# Actual spacelike slice v+2u=0, on S=H+4>0. Sqrt formulas local to this domain.
S=H+4;coords=(u,x,y)
X=s.Matrix([[1,0,0],[-2,0,0],[0,1,0],[0,0,1]])
gamma=s.diag(S,1,1)
n=s.Matrix([1,H+2,0,0])/s.sqrt(S)
positive_S=s.Symbol('positive_S',positive=True)
check('future_normal_relative_fixed_frame_on_full_S_positive_domain',z((n.T*g*e[:,0])[0]+(S+1)/(2*s.sqrt(S))) and (-(positive_S+1)/(2*s.sqrt(positive_S))).is_negative is True)
check('slice_metric_normal_and_tangency',all(z(t) for t in X.T*g*X-gamma) and z((n.T*g*n)[0]+1) and all(z(t) for t in X.T*g*n))
# Hess(F) projected, where F=v+2u and n=-grad(F)/sqrt(S).
Kdirect=s.Matrix(3,3,lambda i,j:-sum(X[r,i]*X[t,j]*(2*G[0][r][t]+G[1][r][t]) for r in ix for t in ix)/s.sqrt(S))
K=s.Matrix([[s.diff(H,u),s.diff(H,x),s.diff(H,y)],[s.diff(H,x),0,0],[s.diff(H,y),0,0]])/(2*s.sqrt(S))
if mode=='wrong_K_sign':K=-K
if mode=='omit_Hu':K[0,0]=0
check('K_full_projected_sign_and_Hu_not_squared_constraint_only',all(z(t) for t in K-Kdirect))
hgi,hG,hQ,hRic=geometry(gamma,coords)
tau=s.simplify(s.trace(hgi*K));R3=s.simplify(s.trace(hgi*hRic))
Knorm=s.simplify(s.trace(hgi*K*hgi*K))
Ham=s.simplify(R3+tau*tau-Knorm)
Mom=s.Matrix(3,1,lambda i,col:s.simplify(sum(hgi[j,k]*(s.diff(K[i,j],coords[k])-sum(hG[m][k][i]*K[m,j]+hG[m][k][j]*K[i,m] for m in range(3))) for j in range(3) for k in range(3))-s.diff(tau,coords[i])))
check('full_neighborhood_intrinsic_Hamiltonian_constraint',Ham==0)
check('full_neighborhood_intrinsic_momentum_constraints',all(z(t) for t in Mom))
check('slice_nonempty_local_domain',at(S)==4)
print(json.dumps({'status':'PASS','mutant':mode,'checks':checks,'sympy':s.__version__,
 'metric':str(g),'free_profiles':'A(u), F(u) arbitrary smooth; values 0 at u=0; derivatives -a,-b',
 'Ricci':str(Ric),'frame':str(e),'P_C':str(C),'P_B':str(B),'nu':nu,
 'slice_domain':'H+4>0, v+2u=0; local only','gamma':str(gamma),'K':str(K),
 'R3':str(R3),'tau':str(tau),'Knorm':str(Knorm),'Hamiltonian':str(Ham),'momentum':str(Mom),
 'limits':'Lambda=0 realization, not all Einstein jets; geometry() method reused, no old quadratic recipe used'},indent=2))
