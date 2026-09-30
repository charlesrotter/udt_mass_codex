"""CCR1 exact algebra and original-null-ODE anchors; not a physical solver."""
import json
import platform
from pathlib import Path
import sympy as S

s, e, F, v, ae, ao, H, t = S.symbols('s epsilon F v a_e a_o H t', real=True)
alpha = S.Function('alpha')(s)
A = S.Function('A')(s)
Z = S.diff(A,s)
D = S.log(Z)
identities, rejected = {}, {}

def eq(name,a,b=0):
    r=S.simplify(S.expand(a-b));identities[name]=str(r)
    assert r==0,(name,r)

def bad(name,a,b):
    r=S.factor(S.simplify(a-b));rejected[name]=str(r)
    assert r!=0,name

g=S.diag(-S.exp(-2*e*F),S.exp(2*e*F),1,1)
h=g.diff(e).subs(e,0);K=S.Matrix([1,1,0,0])
eq('reciprocal_determinant',g.det(),-1)
eq('trace_free',S.trace(g.subs(e,0).inv()*h))
eq('normalized_null_contraction',(K.T*h*K)[0],4*F)
q=S.symbols('q',positive=True)
ch,sh=(q+1/q)/2,(q-1/q)/2
boost=S.Matrix([[ch,sh,0,0],[sh,ch,0,0],[0,0,1,0],[0,0,0,1]])
gb=g.subs(e,0);eq('boost_lorentz',(boost.T*gb*boost-gb).norm()**2)
# A carried tensor and vector must give the same contraction.
hb=boost.inv().T*h*boost.inv();Kb=boost*K
eq('carried_boost_contraction',(Kb.T*hb*Kb)[0],4*F)
Q=S.diff(Z*alpha,s)/Z
eq('full_clock_drift',Q,S.diff(alpha,s)+S.diff(D,s)*alpha)
bad('dropping_curved_clock_drift',Q,S.diff(alpha,s))
# Curved/time-dependent analytic arrival example, mathematical only.
Ac=s+s**2/2
Qc=S.diff(S.diff(Ac,s)*(1+s**2),s)/S.diff(Ac,s)
eq('nonconstant_arrival',Qc,2*s+(1+s**2)/(1+s))  # s>0
bad('nonconstant_arrival_wrong',Qc,2*s)

M=S.Function('M')(s);J=S.Function('J')(s);w=S.Function('w')(s)
eq('integration_by_parts',w*(M*S.diff(alpha,s)+J*alpha),
   S.diff(w*M*alpha,s)+(w*J-S.diff(w*M,s))*alpha)
ap=S.symbols('alpha_prime')
eq('integrating_factor_witness',(M*ap+J*alpha).subs(ap,1-J*alpha/M),M)
bad('dropping_J_in_stationarity',w*J-S.diff(w*M,s),-S.diff(w*M,s))
kappa=S.symbols('kappa',positive=True)
ac=S.exp(kappa*s)
eq('exponential_witness',M*S.diff(ac,s)+J*ac,ac*(kappa*M+J))
# Two constant contrasts of opposite signs, positive mean; NOT a metric witness.
Ds=[S.Integer(2),S.Integer(-1)];weights=[S.Rational(3,4),S.Rational(1,4)]
eq('mixed_individual_sign_positive_mean',sum(x*y for x,y in zip(Ds,weights)),S.Rational(5,4))
eq('zero_mean_subset_control',(1+(-1))/S.Integer(2),0)

# Original conformal null ODE: d eta/dr=exp(2 epsilon f).
# On the baseline shell f=alpha*rho/(2*a_e), integral rho dr=1.
# Coordinate exit delay is alpha/a_e. Interception with X(eta) has local slope v.
delay=alpha/ae
delta_eta=delay/(1-v)
No=ao*S.sqrt(1-v*v)
Zc=No/(ae*(1-v))
delta_A=No*delta_eta
eq('curved_null_ode_arrival',delta_A,Zc*alpha)
bad('omitted_receiver_motion',delta_A,No*delay)
bad('omitted_receiver_proper_rate',delta_A,delta_eta)

# Compute R^1_{212} and lower its first index from the actual conformal metric.
coords=S.symbols('t x y z',real=True);tt=coords[0]
scale=S.exp(H*tt);gc=S.diag(-scale**2,scale**2,scale**2,scale**2);gi=gc.inv()
Gamma={}
for a in range(4):
 for b in range(4):
  for c in range(4):
   Gamma[a,b,c]=S.simplify(sum(gi[a,d]*(S.diff(gc[d,c],coords[b])+S.diff(gc[d,b],coords[c])-S.diff(gc[b,c],coords[d])) for d in range(4))/2)
a,b,c,d=1,2,1,2
R=S.diff(Gamma[a,b,d],coords[c])-S.diff(Gamma[a,b,c],coords[d])+sum(Gamma[a,j,c]*Gamma[j,b,d]-Gamma[a,j,d]*Gamma[j,b,c] for j in range(4))
Rlow=S.simplify(gc[1,1]*R)
eq('actual_nonzero_curvature_component',Rlow,H**2*S.exp(2*H*tt))
bad('curved_control_not_flat',Rlow,0)  # H !=0

result={'status':'PASS','python':platform.python_version(),'sympy':S.__version__,
        'domain':'regular branches; Z>0; mean-sign proof needs M nonzero; conformal control a_e,a_o>0, |v|<1, H!=0; controls are not selected geometry',
        'identities':identities,'wrong_nonidentities_rejected':rejected,
        'scope':'exact algebra/original-null-ODE comparison; analytic support and recovery proof not replaced'}
Path(__file__).with_name('curved_result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
