"""Parent checks of reviewer-origin null-lift/gauge supplement; not a third independent context."""
from pathlib import Path
import ast,json,sys,platform,hashlib
import sympy as s
source=Path('udt_current_native_radiation_feasibility_2026-09-13/check_candidate.py');tree=ast.parse(source.read_text());names={'conn_ric','exterior','closed','densdiv'}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),str(source),'exec'))
checks=[]
def check(name,actual,expected):
 if isinstance(actual,s.MatrixBase):
  assert isinstance(expected,s.MatrixBase) and actual.shape==expected.shape
  vals=list(actual-expected)
 elif isinstance(actual,list):
  assert isinstance(expected,list) and len(actual)==len(expected);vals=[a-b for a,b in zip(actual,expected)]
 else:vals=[s.sympify(actual)-s.sympify(expected)]
 rem=[s.simplify(v) for v in vals];ok=all(v==0 for v in rem);checks.append({'name':name,'pass':ok,'nonzero_residuals':[str(v) for v in rem if v!=0]});print(name,ok,flush=True)
u=s.symbols('u',positive=True);v,x,y=s.symbols('v x y',real=True);cc=(u,v,x,y);root=s.sqrt(2);H=2*(x*x-y*y)/u**2;g=s.Matrix([[H,-1,0,0],[-1,0,0,0],[0,0,1,0],[0,0,0,1]]);C,Ric=conn_ric(g,cc)
k=s.Matrix([0,1,0,0]);ell=s.Matrix([1,H/2,0,0]);ex=s.eye(4)[:,2];ey=s.eye(4)[:,3];T=(k+ell)/root;N=(ell-k)/root
def cov(V,a):return V.diff(cc[a])+s.Matrix([sum(C[i][a][j]*V[j] for j in range(4)) for i in range(4)])
a=s.Function('a',real=True)(u);b=s.Function('b',real=True)(u);P1=ex+a*ell;P2=ey+b*ell;m=k+a*ex+b*ey+(a*a+b*b)*ell/2
frame=s.Matrix.hstack(ell,m,P1,P2);eta=s.Matrix([[0,-1,0,0],[-1,0,0,0],[0,0,1,0],[0,0,0,1]]);check('null_lift_full_frame_Gram',frame.T*g*frame,eta)
A=s.Matrix([s.simplify((P1.T*g*cov(P2,i))[0]) for i in range(4)]);expected=s.Matrix([-2*(b*x+a*y)/u**2,0,0,0]);check('null_lift_original_A_all4',A,expected);F=exterior(A,cc);Fe=s.zeros(4);Fe[0,2]=2*b/u**2;Fe[0,3]=2*a/u**2;Fe[2,0]=-Fe[0,2];Fe[3,0]=-Fe[0,3];check('null_lift_original_dA_all16',F,Fe)
alpha=s.Function('alpha',real=True)(u);beta=s.Function('beta',real=True)(u);Fa=Fe.subs({a:u**2*beta/2,b:u**2*alpha/2});check('inverse_profile_pair',s.Matrix([Fa[0,2],Fa[0,3]]),s.Matrix([alpha,beta]));check('null_lift_original_divergence',densdiv(g,F,cc,s.Integer(1)),s.zeros(4,1));check('null_lift_original_closure',closed(F,cc),[s.Integer(0)]*4);check('null_lift_zero_frame_regular',frame.subs({a:0,b:0}),s.Matrix.hstack(ell,k,ex,ey))
q=s.Function('q',real=True)(u);r=s.Function('r',real=True)(u);K=s.Matrix([0,s.diff(q,u)*x+s.diff(r,u)*y,q,r]);inv={a:u**2*s.diff(r,u),b:u**2*s.diff(q,u)};AK=A.subs(inv);gradient=s.Matrix([s.diff(q*x+r*y,z) for z in cc]);check('all_K_profiles_full_potential_relation',AK-g*K,-gradient);check('all_K_profiles_field_relation',exterior(AK,cc),exterior(g*K,cc))
w1=root*u**2*s.diff(r,u);w2=root*u**2*s.diff(q,u);c=s.sqrt(1+w1*w1+w2*w2);B=(w2*s.diff(w1,u)-w1*s.diff(w2,u))/(c+1);Aw=s.Matrix([B-root*(w2*x+w1*y)/u**2,0,0,0]);check('boost_general_potential_relation',Aw-g*K,s.Matrix([B,0,0,0])-gradient)
example={a:0,b:2*u**3};check('null_example_N_component',(N.T*g*P2.subs(example))[0],root*u**3);boostP2=2*root*u**3*T+s.sqrt(1+8*u**6)*ey;check('boost_example_N_component',(N.T*g*boostP2)[0],0);check('two_distinct_reductions_same_potential',A.subs(example),s.Matrix([-4*u*x,0,0,0]));check('nonparallel_l_acceleration',cov(ell,0)+H*cov(ell,1)/2,s.Matrix([0,0,-s.diff(H,x)/2,-s.diff(H,y)/2]))
# Original mismatch would be visible: same field does not force the screen plane.
check('distinct_planes_numeric_N_separation',(N.T*g*P2.subs(example))[0].subs(u,1)**2,s.Integer(2))
record={'kind':'exact parent verification of reviewer source-first/direct contributions; no third-context independence','python':platform.python_version(),'sympy':s.__version__,'source_utility_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'original_connection':[str(z) for z in A],'checks':checks,'count':len(checks),'passed':sum(z['pass'] for z in checks),'all_pass':all(z['pass'] for z in checks)};Path(sys.argv[1]).write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({k:record[k] for k in ['count','passed','all_pass']}));sys.exit(0 if record['all_pass'] else 1)
