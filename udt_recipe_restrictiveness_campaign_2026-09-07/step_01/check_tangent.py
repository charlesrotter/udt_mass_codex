"""RC1 exact first-variation checks; no finite-epsilon solution claim."""
import itertools,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from tensor_geometry import geometry,quadratic
import sympy as s
u,v,x,y,e=s.symbols('u v x y epsilon', real=True)
coords=(u,v,x,y); ix=range(4)
mutation=sys.argv[1] if len(sys.argv)>1 else 'none'
kappa=0 if mutation=='omit_required_v_term' else -2
H=x**3-3*x*y**2+kappa*e*v*y
g=s.Matrix([[H,-1,0,e*x**2],[-1,0,0,0],[0,0,1,0],[e*x**2,0,0,1]])
gi,G,R,Ric=geometry(g,coords)
checks={}
def check(name,ok):
    checks[name]=bool(ok)
    if not ok:
        print(json.dumps({'mutation':mutation,'checks':checks,'failed':name},indent=2));sys.exit(1)
check('original_linearized_Ricci',Ric.diff(e).subs(e,0)==s.zeros(4))
X=s.Matrix([[1,0,0],[-2,0,0],[0,1,0],[0,0,1]])
dt=s.Matrix([2,1,0,0]); S=s.factor(-(dt.T*gi*dt)[0]); n=-gi*dt/s.sqrt(S)
gamma=s.simplify(X.T*g*X).subs(v,-2*u)
K=s.Matrix(3,3,lambda i,j:s.simplify(-sum(X[a,i]*X[b,j]*(2*G[0][a][b]+G[1][a][b]) for a,b in itertools.product(ix,repeat=2))/s.sqrt(S))).subs(v,-2*u)
dgamma=gamma.diff(e).subs(e,0); dK=K.diff(e).subs(e,0).applyfunc(s.simplify)
# Original unpreconditioned Gauss/Codazzi projections, valid for every metric.
Ein=Ric-g*s.simplify(sum(gi[a,b]*Ric[a,b] for a,b in itertools.product(ix,repeat=2)))/2
Ham=s.simplify(2*(n.T*Ein*n)[0]).subs(v,-2*u)
Mom=s.simplify(-X.T*Ein*n).subs(v,-2*u)
check('original_linearized_Hamiltonian',s.simplify(s.diff(Ham,e).subs(e,0))==0)
check('original_linearized_momentum',Mom.diff(e).subs(e,0)==s.zeros(3,1))
check('finite_epsilon_not_mislabeled_vacuum',Ric[0,0]==4*e**2*x**2)
check('complete_gamma_variation',dgamma==s.Matrix([[4*u*y,0,x**2],[0,0,0],[x**2,0,0]]))
# Weyl equals R through first order because Ricci and scalar do; verify both.
check('Ricci_zero_through_first_order',Ric.subs(e,0)==s.zeros(4))
B,_=quadratic(g,R);N=36*(x*x+y*y)
dB={k:s.factor(s.diff(z,e).subs(e,0)) for k,z in B.items()}
r=[s.S.Zero,s.S.Zero,y/(3*(x*x+y*y)),x/(3*(x*x+y*y))]
if mutation=='omit_root_transverse_tangent': r[3]=0
pred={k:s.factor(N*sum(r[k[j]]*s.prod(s.KroneckerDelta(k[h],0) for h in ix if h!=j) for j in ix)) for k in B}
check('full256_root_tangent',all(s.simplify(dB[k]-pred[k])==0 for k in B))
check('all256_background_root',all(s.simplify(z.subs(e,0)-N*s.prod(s.KroneckerDelta(i,0) for i in k))==0 for k,z in B.items()))
relative=s.Matrix(r); root_direction_variation=-(gi.subs(e,0)*relative+gi.diff(e).subs(e,0)*s.Matrix([1,0,0,0]))
check('null_root_tangent',s.simplify((relative.T*gi.subs(e,0)*s.Matrix([1,0,0,0]))[0]*2+gi.diff(e).subs(e,0)[0,0])==0)
a=s.symbols('a0:4')
spatial=[]
for i,j,d in itertools.product(range(3),range(3),ix):
    spatial.append(s.factor(sum(X[A,i]*X[Bb,j]*(sum(R[A,Bb,c,d].subs(e,0)*a[c] for c in ix)+s.diff(R[A,Bb,1,d],e).subs(e,0)) for A,Bb in itertools.product(ix,repeat=2))))
sol=s.linsolve(spatial,a)
expected=(0,a[1],-y/(3*(x*x+y*y)),-x/(3*(x*x+y*y)))
check('full_spatial_integrability_converse',sol==s.FiniteSet(expected))
# Any smooth first-order seed must have these transverse components on the patch.
# Its (X_x,vector-y) parallel equation is partial_x a3=0: background a0=0,
# Gamma^y_xc=0 and delta Gamma^y_xv=0. Show the obstruction is active.
obstruction=s.factor(s.diff(expected[3],x))
check('seed_differential_obstruction',obstruction.subs({x:1,y:0})==s.Rational(1,3))
check('no_connection_cancellation',all(G[3][2][c].subs(e,0)==0 for c in ix) and s.diff(G[3][2][1],e).subs(e,0)==0)
print(json.dumps({'status':'PASS','mutation':mutation,'sympy':s.__version__,'checks':checks,'metric':str(g),'S':str(S),'gamma0':str(gamma.subs(e,0)),'delta_gamma':str(dgamma),'K0':str(K.subs(e,0)),'delta_K':str(dK),'Hamiltonian_projection':str(Ham),'momentum_projection':str(Mom),'Ricci':str(Ric),'delta_B_nonzero':{str(k):str(z) for k,z in dB.items() if z!=0},'relative_root_tangent':list(map(str,r)),'root_direction_variation':str(root_direction_variation),'spatial_integrability_solution':str(sol),'seed_derivative_obstruction':str(obstruction),'epsilon_scope':'EXACT_FIRST_VARIATION_ONLY','independence':'SAME_AUTHOR_SHARED_GEOMETRY_REGRESSION'},indent=2))
