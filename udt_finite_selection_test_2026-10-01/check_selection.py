"""FST1 symbolic checks; analytic hypotheses and domains remain in the proof."""
import json,sys,hashlib,platform
from pathlib import Path
import sympy as S
checks=[]
def eq(name,lhs,rhs=0):
 d=S.trigsimp(S.simplify(lhs-rhs)) if not isinstance(lhs,S.MatrixBase) else (lhs-rhs).applyfunc(S.simplify)
 assert d==0 or isinstance(d,S.MatrixBase) and d==S.zeros(*d.shape),(name,d)
 checks.append(name)
eta=S.diag(-1,1,1,1); xx=S.symbols('e:10');pairs=[(i,j) for i in range(4) for j in range(i,4)]
E=S.zeros(4)
for v,(i,j) in zip(xx,pairs):E[i,j]=E[j,i]=v
rot=[]; boosts=[]
for i,j in [(1,2),(1,3),(2,3)]:
 a=S.zeros(4);a[i,j]=1;a[j,i]=-1;rot.append(a)
for i in [1,2,3]:
 a=S.zeros(4);a[0,i]=a[i,0]=1;boosts.append(a)
for n,a in enumerate(rot+boosts):eq('generator_lorentz_'+str(n),a.T*eta+eta*a,S.zeros(4))
def system(gs):return S.linear_eq_to_matrix([z for a in gs for z in a.T*E+E*a],xx)[0]
R=system(rot); M=system(rot+boosts);eq('rotation_constraint_rank',R.rank(),8);eq('full_constraint_rank',M.rank(),9)
v=S.Matrix([eta[i,j] for i,j in pairs]);eq('metric_in_kernel',M*v,S.zeros(M.rows,1));eq('full_nullspace_dimension',len(M.nullspace()),1)
k,k0,a,b=S.symbols('kappa kappa0 a b',real=True);Ric=3*k*eta;scalar=S.trace(eta*Ric);eq('scalar',scalar,12*k)
response=a*Ric+b*scalar*eta;eq('G301_tracefree',response-S.trace(eta*response)*eta/4,S.zeros(4));eq('spaceform_trace',S.trace(eta*response),4*(3*a+12*b)*k)
L,t=S.symbols('L t',positive=True)
Cp=S.cos(t*L);Cn=S.cosh(t*L)
eq('positive_original_ode',S.diff(Cp,L,2)+t*t*Cp)
eq('negative_original_ode',S.diff(Cn,L,2)-t*t*Cn)
eq('positive_curvature_sensitivity',S.diff(-S.log(Cp),t)/(2*t),L*S.tan(t*L)/(2*t))
eq('negative_curvature_sensitivity',S.diff(-S.log(Cn),t)/(-2*t),L*S.tanh(t*L)/(2*t))
eq('positive_flat_sensitivity',S.limit(L*S.tan(t*L)/(2*t),t,0),L*L/2)
eq('negative_flat_sensitivity',S.limit(L*S.tanh(t*L)/(2*t),t,0),L*L/2)
x=S.Function('x')(L);y=S.Function('y')(L);W=S.diff(x,L)*y-x*S.diff(y,L)
eq('wronskian_original_odes',S.diff(W,L).subs({S.diff(x,L,2):-k*x,S.diff(y,L,2):-k0*y}),(k0-k)*x*y)
eq('contrast_derivative',S.diff(S.log(y)-S.log(x),L),-W/(x*y))
# Controls are exact, not imported worldline or physical-admission claims.
p=S.Rational(4,5);p0=S.Rational(8,17);eq('negative_control_ratio',p/p0,S.Rational(17,10))
eq('cosh_log2',S.expand_func(S.cosh(S.log(2))).rewrite(S.exp),S.Rational(5,4))
eq('cosh_2log2',S.cosh(2*S.log(2)).rewrite(S.exp),S.Rational(17,8))
# Bound endpoints expressed by cosine rather than approximate inverse trig.
z=S.symbols('z',positive=True);eq('threshold_identity',1/S.cos(S.acos(S.exp(-z))),S.exp(z))
q=S.symbols('q',positive=True);eq('positive_calibration_identity',S.cos(S.acos(1/q)),1/q)
eq('negative_calibration_identity',S.cosh(S.acosh(1/q)),1/q)
# c and G dimensions in (length,time,mass); target curvature not in their span.
A=S.Matrix([[1,3],[-1,-2],[0,-1]]);target=S.Matrix([-2,0,0]);eq('anchor_dimension_rank',A.rank(),2);eq('curvature_augmented_rank',A.row_join(target).rank(),3)
# Native angular and imported full vacuum comparator retain different readings.
r=S.symbols('r',positive=True);f=1-k*r*r
ap=(r*r*S.diff(f,r,2)-r*S.diff(f,r))/2;at=1-f+r*S.diff(f,r)/2
eq('angular_parallel',ap);eq('angular_perp',at);eq('vacuum_E0',r*S.diff(f,r)+f-1,-3*k*r*r);eq('vacuum_E1',r*S.diff(f,r)+r*r*S.diff(f,r,2)/2,-3*k*r*r)
print(json.dumps({'status':'PASS','assertions':len(checks),'checks':checks,'python':platform.python_version(),'sympy':S.__version__,'invariance_matrix':{'rows':M.rows,'columns':M.cols,'rank':M.rank(),'kernel':[str(z) for z in M.nullspace()[0]]},'dimensions':{'anchors':A.tolist(),'target':list(target)},'limit':'Exact symbolic regression supporting scoped analytic arguments; no physical selector or continuum proof by samples.'},indent=2,default=str))
