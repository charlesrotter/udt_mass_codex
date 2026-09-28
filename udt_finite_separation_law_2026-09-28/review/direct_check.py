"""Direct review, written before author-code exposure: symbolic independent controls."""
import datetime,hashlib,json,pathlib,sys
import sympy as S
ROOT=pathlib.Path('/home/udt-admin/udt_mass_codex');P=ROOT/'udt_finite_separation_law_2026-09-28';R=P/'review'
checks=[]
def ck(name,c):
 if not c:raise AssertionError(name)
 checks.append(name)
freeze=json.loads((P/'CANDIDATE_FREEZE.json').read_text())
pins={}
for group in ['candidate_and_checks','additional_sources']:
 for rel,h in freeze[group].items():
  p=P/rel if group=='candidate_and_checks' else ROOT/rel
  got=hashlib.sha256(p.read_bytes()).hexdigest();ck('frozen_'+rel,got==h);pins[str(p.relative_to(ROOT))]=got
seal=json.loads((R/'SOURCE_FIRST_SEAL.json').read_text())
for rel,h in seal['sha256'].items():ck('sealed_'+rel,hashlib.sha256((R/rel).read_bytes()).hexdigest()==h)
# Eq7 as an exact nonnegative affine relation, not a sampled limit inference.
eps,T=S.symbols('epsilon T',positive=True)
mu=1-T*S.sqrt(eps);rad=1-eps
z=(1-rad*mu)/S.sqrt(eps*(2-eps))
a=S.sqrt(eps)/S.sqrt(2-eps);b=(1-eps)/S.sqrt(2-eps)
ck('eq7_exact_decomposition',S.simplify(z-a-b*T)==0)
ck('eq7_offset_limit',S.limit(a,eps,0,dir='+')==0)
ck('eq7_coefficient_limit',S.limit(b,eps,0,dir='+')==1/S.sqrt(2))
# Rational circle parameterization makes all radicals exact and tests the
# transition powers and arbitrary positive finite limit independently.
t,K=S.symbols('t K',positive=True)
r=(1-t*t)/(1+t*t);den=2*t/(1+t*t)
ck('rational_circle',S.factor(1-r*r-den*den)==0)
limits={}
for p,expected in [(0,S.oo),(1,S.Rational(1,2)),(2,0)]:
 m=1-t**p;zz=S.factor((1-r*m)/den);tt=S.factor((1-m)/S.sqrt(1-r))
 val=S.limit(zz,t,0,dir='+');ck('limit_power_'+str(p),val==expected)
 limits[str(p)]={'Z':str(zz),'limit':str(val),'angular_factor_limit':str(S.limit(tt,t,0,dir='+'))}
m=1-2*K*t;zz=S.factor((1-r*m)/den)
ck('arbitrary_finite_positive_limit',S.limit(zz,t,0,dir='+')==K)
ck('finite_limit_angular_normalization',S.limit((1-m)/S.sqrt(1-r),t,0,dir='+')==S.sqrt(2)*K)
# Exact varying-event family in Minkowski, accelerating receiver.
s=S.symbols('s',negative=True);tau=-S.log(-s)
tr=S.sinh(tau);xr=S.cosh(tau);u=S.Matrix([S.cosh(tau),S.sinh(tau)])
eta=S.diag(-1,1);Z=S.diff(tau,s);k=S.Matrix([tr-s,xr]);Je=S.Matrix([1,0]);Jo=u*Z
simp=lambda x:S.simplify(S.expand(x.rewrite(S.exp)))
ck('event_family_null_incidence',simp(tr-xr-s)==0)
ck('receiver_proper_clock',simp((u.T*eta*u)[0])==-1)
ck('future_outgoing_affine_tangent',simp(k[0]-k[1])==0)
ck('null_family_endpoint_first_variation',simp((k.T*eta*Je)[0]-(k.T*eta*Jo)[0])==0)
omega_e=-(Je.T*eta*k)[0];omega_o=-(u.T*eta*k)[0]
ck('event_slope_equals_frequency_ratio',simp(Z-omega_e/omega_o)==0)
finite=S.integrate(Z,(s,-2,-1));ck('finite_duration_integral',finite==S.log(2))
ck('single_initial_ratio_not_duration_average',finite!=Z.subs(s,-2))
# Time-live conformal control; no field equations or physical-history claim.
D,y=S.symbols('D y',positive=True);eta_e=S.sqrt(2*y);eta_o=eta_e+D
arrival=eta_o**2/2
ck('conformal_event_slope',S.simplify(S.diff(arrival,y)-eta_o/eta_e)==0)
# Construct canonical boost in rational q and actual launch direction from inverse.
q=S.symbols('q',positive=True);gamma=1+q*q/2;v=S.Matrix([q*q/2,q,0]);I=S.eye(3)
B=S.zeros(4);B[0,0]=gamma
for i in range(3): B[0,i+1]=v[i];B[i+1,0]=v[i]
B[1:4,1:4]=I+v*v.T/(gamma+1)
eta4=S.diag(-1,1,1,1);l=S.Matrix([1,1,0,0]);inv=eta4*B.T*eta4;la=inv*l
ck('boundary_arrow_Lorentz',S.simplify(B.T*eta4*B-eta4)==S.zeros(4))
ck('boundary_launch_time_exactly_one',S.simplify(la[0])==1)
ck('boundary_actual_null_launch',S.simplify((la.T*eta4*la)[0])==0)
ck('boundary_arrow_roundtrip',S.simplify(B*la-l)==S.zeros(4,1))
ck('boundary_norm_limit',S.limit(1-1/gamma**2,q,S.oo)==1)
out={'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stage':'candidate exposed; author code/results unread except opaque hash verification','python':sys.version,'sympy':S.__version__,'count':len(checks),'checks':checks,'pins':pins,'equation7_decomposition':str(a+b*T),'limit_controls':limits,'accelerated_event':{'arrival_proper_time':str(tau),'pointwise_Z':str(Z),'finite_duration_minus2_minus1':str(finite),'initial_pointwise_Z':str(Z.subs(s,-2))},'boundary_launch_vector':[str(S.simplify(x)) for x in la]}
with (R/'direct_result_repaired.json').open('x') as f:json.dump(out,f,indent=2);f.write('\n')
print(json.dumps(out,indent=2))
