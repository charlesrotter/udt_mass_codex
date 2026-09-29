"""Post-exposure independent checks; no producer scientific functions imported."""
import hashlib,itertools,json,platform
from pathlib import Path
import sympy as s
out=Path(__file__).resolve().parent
checks={};values={}
def ck(name,truth):
    checks[name]=bool(truth)
    if not checks[name]:raise AssertionError(name)
def simp(v):return s.factor(s.simplify(v))
def iszero(M):return all(simp(v)==0 for v in M)
Q=s.Rational

# Full metric-to-area differential at a nonspherical, shifted rational metric.
pos=[(i,j) for i in range(4) for j in range(i,4)]
vs=s.symbols('z0:10');g=s.zeros(4)
for v,(i,j) in zip(vs,pos):g[i,j]=g[j,i]=v
planes=list(itertools.combinations(range(4),2))
area=s.Matrix(6,6,lambda a,b:g[planes[a][0],planes[b][0]]*g[planes[a][1],planes[b][1]]-g[planes[a][0],planes[b][1]]*g[planes[a][1],planes[b][0]])
E=s.Matrix([[2,1,0,0],[0,1,1,0],[0,0,2,1],[0,0,0,1]])
g0=E.T*s.diag(-1,1,1,1)*E
sub={v:g0[i,j] for v,(i,j) in zip(vs,pos)}
arow=s.Matrix([area[i,j] for i in range(6) for j in range(i,6)])
ck('area_rank10_mixed_metric',arow.jacobian(vs).subs(sub).rank()==10)
ck('area_sign_twins',arow.subs({v:-v for v in vs},simultaneous=True)==arow)
ck('mixed_metric_nonzero_shift',g0[0,1]!=0)
values['area_control_metric']=str(g0)

# Derive radar free-fall beta equation from connection, without imposing it.
T,R=s.symbols('T R',real=True);ph=s.Function('phi')(T,R)
gb=s.exp(2*ph)*s.diag(-1,1);inv=gb.inv();co=(T,R)
Ga=[[[simp(sum(inv[a,d]*(s.diff(gb[d,c],co[b])+s.diff(gb[d,b],co[c])-s.diff(gb[b,c],co[d])) for d in range(2))/2) for c in range(2)] for b in range(2)] for a in range(2)]
beta=s.symbols('beta',real=True);v=[1,beta]
acc=-sum(Ga[1][i][j]*v[i]*v[j] for i in range(2) for j in range(2))+beta*sum(Ga[0][i][j]*v[i]*v[j] for i in range(2) for j in range(2))
ck('radar_geodesic_equation',simp(acc+(1-beta**2)*(s.diff(ph,R)+beta*s.diff(ph,T)))==0)
p,q=s.symbols('p q',positive=True)
BT=(p*q-1)/(p*q+1);Tb=(1/p+q)/2;Rb=(q-1/p)/2
ck('proper_metric_value',s.factor((p/q)*(Tb**2-Rb**2))==1)
ck('radar_velocity_consistency',s.factor(Rb/Tb-BT)==0)
Kdot,Sdot=s.symbols('Kdot Sdot')
grad=s.Matrix([[1,beta],[-beta,-1]]).inv()*s.Matrix([Kdot,Sdot])
ck('radar_inverse_gradients',simp(grad[0]-(Kdot+beta*Sdot)/(1-beta**2))==0 and simp(grad[1]-(-Sdot-beta*Kdot)/(1-beta**2))==0)

# Nontrivial conformal reconstruction, including TT mean and vector correction.
x=s.symbols('x',real=True);p0=Q(3,2);q0=Q(2,3)
tau=2+s.sin(x)+Q(1,3)*s.cos(2*x);mean=s.Integer(2)
wp=p0**6*(tau-mean)/2
TT=p0**6*s.diag(Q(2,3)*mean,q0-mean/3,-q0-mean/3)
LW=s.diag(Q(4,3)*wp,-Q(2,3)*wp,-Q(2,3)*wp)
# A^i_j=psi^-6 bar A^i_j for gamma=psi^4 delta.
Km=(TT+LW)/p0**6+tau*s.eye(3)/3
ck('nonCMC_complete_reconstruction',iszero(Km-s.diag(tau,q0,-q0)))
ck('nonCMC_hamiltonian',simp(s.trace(Km)**2-s.trace(Km*Km)+2*q0**2)==0)
mom=s.Matrix([s.diff(Km[0,i],x)-(s.diff(s.trace(Km),x) if i==0 else 0) for i in range(3)])
ck('nonCMC_all_momentum',iszero(mom))
ck('nonCMC_vector_source_nonzero',s.diff(wp,x)!=0 and s.diff(tau,x)!=0)
ck('nonCMC_momentum_normalization',simp(2*s.diff(wp,x)-p0**6*s.diff(tau,x))==0)

# Jacobi oscillator: self-adjoint T=I, exact phase map at length pi.
Js=s.zeros(4);Js[:2,2:]=s.eye(2);Js[2:,:2]=-s.eye(2)
M=-s.eye(4);B=M[:2,2:]
ck('conjugate_full_phase_invertible',M.det()==1 and M.T*Js*M==Js)
ck('conjugate_both_areas_zero',B.det()==0 and (-B.T).det()==0)
ck('conjugate_quotient_undefined',s.sympify(0)/s.sympify(0) is s.nan)
values['conjugate_rank_B']=B.rank()

# Neutral measure density and separately declared arbitrary observer weight.
w,om1,om2,ref,J1,J2,content=s.symbols('w om1 om2 ref J1 J2 content',positive=True)
n1=content/J1;n2=content/J2
ck('neutral_density_area_only',s.cancel(n2/n1-J1/J2)==0)
for power in [-2,0,1,3]:
    C1=(om1/ref)**power*n1;C2=(om2/ref)**power*n2
    ck('weighted_density_'+str(power),s.cancel(C2/C1-(om2/om1)**power*J1/J2)==0)
G1=om1*n1;G2=om2*n2
ck('clock_rate_division_free',s.cancel(G2-(om2/om1)*(J1/J2)*G1)==0)
ck('clock_zero_support',G1.subs(content,0)==0 and G2.subs(content,0)==0)

# Original optional-null quadratic and its implicit momentum derivative.
a,b,c=s.symbols('a b c',real=True);root=(-b+s.sqrt(b*b-a*c))/a
ck('null_root_quadratic',simp(a*root**2+2*b*root+c)==0)
ck('null_future_root',simp(a*root+b-s.sqrt(b*b-a*c))==0)

# Different polynomial exact algebra control for the interior-clock variation.
em=s.symbols('em',real=True);bump=x**3*(2-x)**3
B0=s.integrate(bump,(x,0,2));B1=s.integrate(x*bump,(x,0,2))
arrival=s.integrate(2*(em+x)*bump,(x,0,2))
ck('interior_clock_ODE_response',s.diff(arrival,em)==2*B0 and B0>0)
values['clock_polynomial_control']={'B0':str(B0),'B1':str(B1),'response':str(2*B0),'scope':'algebra only; not an all-endpoint-jets compact-bump witness'}
record={'python':platform.python_version(),'sympy':s.__version__,'checks':checks,'passed':sum(checks.values()),'values':values,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
with (out/'full_results.json').open('x') as f:json.dump(record,f,indent=2);f.write('\n')
print(json.dumps({'passed':record['passed'],'values':values},sort_keys=True))
