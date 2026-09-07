"""RC3 exact functional metric variation and fixed-query checks; no physical identity."""
import itertools,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from tensor_geometry import geometry,quadratic
import sympy as s
u,v,x,y=s.symbols('u v x y',real=True);coords=(u,v,x,y);I=range(4)
psi=s.Function('psi')(u); mode=sys.argv[1] if len(sys.argv)>1 else 'none'
P=x**3-3*x*y**2+x**4-6*x*x*y*y+y**4
Q=3*x*x*y-y**3+4*x**3*y-4*x*y**3
if mode=='nonharmonic_conjugate':Q+=y*y
H=s.cos(psi)*P+s.sin(psi)*Q
g=s.Matrix([[H,-1,0,0],[-1,0,0,0],[0,0,1,0],[0,0,0,1]])
gi,G,R,Ric=geometry(g,coords);checks={}
def simp(z):return s.factor(s.trigsimp(s.expand(z)))
def check(name,truth):
    checks[name]=bool(truth)
    if not truth:
        print(json.dumps({'status':'FAIL','mode':mode,'checks':checks,'failed':name},indent=2));sys.exit(1)
check('original_exact_Ricci',Ric==s.zeros(4))
check('conjugate_Hessian',s.diff(Q,x,2)==-s.diff(P,x,y) and s.diff(Q,x,y)==s.diff(P,x,2))
check('all16_parallel_seed',all(G[a][b][1]==0 for a,b in itertools.product(I,repeat=2)))
N=simp(s.diff(H,x,2)**2+s.diff(H,x,y)**2)
N0=s.factor(s.diff(P,x,2)**2+s.diff(P,x,y)**2)
check('full_functional_curvature_norm_invariant',N==N0 and s.diff(N,u)==0)
B,_=quadratic(g,R)
check('all256_same_fixed_B',all(simp(B[k]-N0*s.prod(s.KroneckerDelta(i,0) for i in k))==0 for k in B))
alpha=s.Matrix([s.diff(N,z)/(4*N) for z in coords]);q=simp((alpha.T*gi*alpha)[0])
q0=s.factor((s.diff(N0,x)**2+s.diff(N0,y)**2)/(16*N0**2))
check('same_full_recurrence_scalar',q==q0 and alpha[0]==alpha[1]==0)
check('nonzero_positive_query_domain',N0.subs({x:1,y:0})==324 and q0.subs({x:1,y:0})==s.Rational(25,36))
beta=-N0**s.Rational(1,4)*s.Matrix([1,0,0,0]); C=gi*beta;D=q*C
check('same_normalized_root_current',C==s.Matrix([0,N0**s.Rational(1,4),0,0]) and D==q0*C)
check('conservation_original_volume',g.det()==-1 and sum(s.diff(D[i],coords[i]) for i in I)==0)
k0,Delta=s.symbols('kappa0 Delta',positive=True)
w0=q0*N0**s.Rational(1,4);sigma0=Delta*w0/k0
actual_fixed_product_density=simp(q*N**s.Rational(1,4)/k0)
target=simp(sigma0/Delta)
check('unchanged_fixed_measure_product',simp(actual_fixed_product_density-target)==0)
# Same metric/current but a genuinely different supplied phase is not rescued by mu.
phase_slope=2*k0 if mode=='ignore_fixed_phase' else k0
tested_density=simp(q*N**s.Rational(1,4)/phase_slope)
check('fixed_phase_matching_not_automatic',simp(tested_density-target)==0)
# A separate wrong query has a known active mismatch, not an admitted-equation defect.
phase_mismatch=simp(w0/(2*k0)-sigma0/Delta)
check('changed_phase_at_fixed_mu_detected',simp(phase_mismatch+target/2)==0 and phase_mismatch!=0)
K=s.Matrix([1,H/2,0,0]);V=s.Matrix([0,1,0,0]);trans=(s.Matrix([0,0,1,0]),s.Matrix([0,0,0,1]))
check('full_ideal_query_normalization',simp((K.T*g*K)[0])==0 and (V.T*g*K)[0]==-1 and all(simp((z.T*g*K)[0])==0 and (z.T*g*V)[0]==0 for z in trans))
T=s.Matrix(2,2,lambda i,j:simp(sum(R[a,b,c,d]*trans[i][a]*K[b]*K[c]*trans[j][d] for a,b,c,d in itertools.product(I,repeat=4))))
check('tidal_query_is_full_curvature_contraction',all(simp(T[i,j]+s.diff(H,(x,y)[i],(x,y)[j])/2)==0 for i,j in itertools.product(range(2),repeat=2)))
Tp=T.subs({x:1,y:0}).applyfunc(simp)
check('same_recipe_distinct_registered_tide',Tp==s.Matrix([[-9*s.cos(psi),-9*s.sin(psi)],[-9*s.sin(psi),9*s.cos(psi)]]))
# Original-equation failure control: a transverse shape-angle is not the declared freedom.
eps=s.symbols('epsilon',real=True)
Hbad=s.cos(eps*x)*P+s.sin(eps*x)*Q
ric_bad_first=s.simplify(-s.diff(s.diff(Hbad,x,2)+s.diff(Hbad,y,2),eps).subs(eps,0)/2)
check('transverse_angle_variation_not_generally_admitted',ric_bad_first==-s.diff(Q,x) and ric_bad_first!=0)
print(json.dumps({'status':'PASS','mode':mode,'sympy':s.__version__,'checks':checks,'P':str(P),'Q':str(Q),'H':str(H),'Ricci':str(Ric),'N0':str(N0),'alpha':list(map(str,alpha)),'q0':str(q0),'w0':str(w0),'N_at_point':str(N0.subs({x:1,y:0})),'q_at_point':str(q0.subs({x:1,y:0})),'tidal_matrix':str(T),'tidal_at_point':str(Tp),'wrong_phase_product_residual':str(phase_mismatch),'transverse_angle_linear_Ricci':str(ric_bad_first),'scope':'ARBITRARY_SMOOTH_U_SHAPE_FUNCTION_FIXED_REGISTERED_QUERY_NOT_ALL_ISOMETRY_CLASSES'},indent=2))
