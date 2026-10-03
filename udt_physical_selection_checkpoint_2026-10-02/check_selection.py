"""Exact checks of stated conditional comparisons; no physical adoption."""
from pathlib import Path
import sympy as s
import json,hashlib,platform
B=Path(__file__).resolve().parent
checks={}
def zero(name,x):
    v=s.factor(x); assert v==0,(name,v); checks[name]='0'
R,H,P,A,alpha,beta,Lam=s.symbols('R H P A alpha beta Lambda',nonzero=True)
f=R+alpha*R**2+beta*R**3; F=s.diff(f,R); Fr=s.diff(F,R); Frr=s.diff(Fr,R)
Hd=R/6-2*H**2
Pd=-3*H*P+(F*R-2*f+4*Lam-3*Frr*P**2)/(3*Fr)
def flow(e): return s.diff(e,H)*Hd+s.diff(e,R)*P+s.diff(e,P)*Pd+s.diff(e,A)*A*H
Fd=Fr*P; Fdd=Fr*Pd+Frr*P**2
# Original proper-time metric Ric00=-3(Hdot+H²), Ricii/a²=Hdot+3H².
C=-3*F*(Hd+H**2)+f/2+3*H*Fd-Lam
D=F*(Hd+3*H**2)-f/2-Fdd-2*H*Fd+Lam
zero('original_00_constraint_form',C-(3*F*H**2-(F*R-f)/2+3*H*Fd-Lam))
zero('original_trace_under_flow',-C+3*D)
zero('original_constraint_propagation',flow(C)+4*H*C)
zero('original_tensor_conservation_under_flow',flow(C)+3*H*(C+D))
P0=s.symbols('P0',nonzero=True); init={H:0,R:0,P:P0,A:1,Lam:0}
zero('initial_constraint',C.subs(init))
zero('initial_Pdot',Pd.subs(init)+3*beta*P0**2/alpha)
zero('initial_Pddot',flow(Pd).subs(init)+P0/(6*alpha)-27*beta**2*P0**3/alpha**2)
M=(F-R*Fr)/(3*Fr)
zero('background_pole',M-(1-3*beta*R**2)/(6*alpha+18*beta*R))
zero('flat_pole_beta_blind',M.subs(R,0)-1/(6*alpha))
zero('quadratic_pole_constant',M.subs(beta,0)-1/(6*alpha))
zero('pole_background_slope',s.diff(M,R).subs(R,0)+beta/(2*alpha**2))
requiredLambda=(2*f-R*F)/4
zero('fixed_lambda_root_derivative',s.diff(requiredLambda,R)-(F-R*Fr)/4)
mu=s.symbols('mu',positive=True); normalizedF=1+R/(3*mu**2)
zero('constant_pole_ode',(R+3*mu**2)*s.diff(normalizedF,R)-normalizedF)
zero('constant_pole_recovered',(normalizedF-R*s.diff(normalizedF,R))/(3*s.diff(normalizedF,R))-mu**2)
eps,r1,r2,qbox1,qbox2,grad1=s.symbols('eps r1 r2 qbox1 qbox2 grad1')
tracepoly=6*alpha*s.Symbol('boxR')+18*beta*(R*s.Symbol('boxR')+s.Symbol('gradR2'))-R+beta*R**3+4*Lam
first=s.diff(tracepoly.subs({R:eps*r1,s.Symbol('boxR'):eps*qbox1,s.Symbol('gradR2'):eps**2*grad1,Lam:0}),eps).subs(eps,0)
zero('full_trace_flat_linear_beta_blind',first-(6*alpha*qbox1-r1))
# All beta-dependent Euler terms are products of at least two perturbations.
ric1,g0,hessr2,boxr2=s.symbols('ric1 g0 hessr2 boxr2')
extra=3*beta*(eps*r1)**2*(eps*ric1)-beta*(eps*r1)**3*g0/2+3*beta*eps**2*(g0*boxr2-hessr2)
zero('full_tensor_flat_linear_beta_blind',s.diff(extra,eps).subs(eps,0))
k,omega,ce,m,rad=s.symbols('k omega ce m rad',positive=True)
zero('dispersion_relation',(omega**2/ce**2-k**2-m**2).subs(omega,ce*s.sqrt(k**2+m**2)))
profile=s.exp(-m*rad)/rad
zero('static_radial_equation',s.diff(profile,rad,2)+2*s.diff(profile,rad)/rad-m**2*profile)
t,h=s.symbols('t h',real=True); afalse=s.sqrt(1+2*h*t); hf=s.diff(afalse,t)/afalse
zero('trace_only_control_R_zero',6*(s.diff(hf,t)+2*hf**2))
false00=s.factor(3*hf**2);assert false00.subs({h:1,t:0})==3
# Recover jets from original spatial tensor, not a solved trace recurrence.
c3,c4,c5=s.symbols('c3 c4 c5'); a=1+c3*t**3+c4*t**4+c5*t**5
hh=s.series(s.diff(a,t)/a,t,0,5).removeO()
rr=s.series(6*(s.diff(hh,t)+2*hh**2),t,0,4).removeO()
ff=s.series(f.subs(R,rr),t,0,4).removeO()
FF=s.series(F.subs(R,rr),t,0,4).removeO()
e00=s.series(-3*FF*(s.diff(hh,t)+hh**2)+ff/2+3*hh*s.diff(FF,t),t,0,4).removeO()
eii=s.series(FF*(s.diff(hh,t)+3*hh**2)-ff/2-s.diff(FF,t,2)-2*hh*s.diff(FF,t),t,0,2).removeO()
solution={c3:P0/36,c4:-beta*P0**2/(48*alpha),c5:-P0/(4320*alpha)+3*beta**2*P0**3/(80*alpha**2)}
for i in range(4):zero('original_00_jet_'+str(i),e00.expand().coeff(t,i).subs(solution))
for i in range(2):zero('original_spatial_jet_'+str(i),eii.expand().coeff(t,i).subs(solution))
zero('curvature_derivative_initial',s.diff(rr,t).subs(t,0).subs(solution)-P0)
ell=s.symbols('ell'); arrival=ell+c3*ell**4/4+c4*ell**5/5
zero('arrival_ODE_through_four',s.series(s.diff(arrival,ell)-a.subs(t,arrival),ell,0,5).removeO())
logp=s.series(s.log(a.subs(t,arrival)),ell,0,6).removeO()
for n,c in [(3,c3),(4,c4),(5,c5)]:zero('clock_jet_'+str(n),logp.expand().coeff(ell,n)-c)
b3,b4,b5=(solution[c] for c in [c3,c4,c5])
zero('beta_alpha_inference',-b4/(27*b3**2)-beta/alpha)
zero('nonlinear_quintic_relation',b5+b3/(120*alpha)-s.Rational(12,5)*b4**2/b3)
zero('RCD1_limit_b4',b4.subs(beta,0))
zero('RCD1_limit_b5',b5.subs(beta,0)+b3/(120*alpha))
length_scale=s.symbols('length_scale',positive=True)
for n,b in [(3,b3),(4,b4),(5,b5)]:
 zero('dimensions_b'+str(n),b.subs({alpha:alpha*length_scale**2,beta:beta*length_scale**4,P0:P0/length_scale**3},simultaneous=True)-b/length_scale**n)
v,w,rkk,F0=s.symbols('v w rkk F0',real=True); theta=-v/F0; theta_d=-theta**2/2-rkk
qprime=w+v*theta+F0*theta_d
zero('horizon_entropy_derivative',qprime-(w-F0*rkk-s.Rational(3,2)*v**2/F0))
lam,s0=s.symbols('lam s0',real=True); production=-s0*lam*s.Rational(3,2)*v**2/F0
zero('horizon_production_cancellation',s0*lam*qprime-production-s0*lam*(w-F0*rkk))
assert production.subs({s0:1,lam:-1,v:2,F0:2})==3
assert (qprime-(w-F0*rkk)).subs({F0:2,v:2})==-3
zero('constant_entropy_no_bulk_term',production.subs(v,0))
zero('linear_entropy_integrates_quadratic',s.integrate(1+2*alpha*R,R)-(R+alpha*R**2))
zero('polynomial_entropy_keeps_completion',s.integrate(F,R)-f)
cases=[]
for name,bval in [('quadratic',s.Rational(0)),('cubic_completion',s.Rational(1,10))]:
 vals={alpha:1,beta:bval,P0:s.Rational(3,100)}
 cases.append({'name':name,'alpha':'1','beta':str(bval),'P0':'3/100','b3':str(b3.subs(vals)),'b4':str(b4.subs(vals)),'b5':str(b5.subs(vals)),'flat_M2':str(M.subs(R,0).subs(vals))})
result={'status':'PASS','exact_zero_assertions':len(checks),'checks':checks,'nonzero_controls':{'trace_only_original_00_at_h1_t0':3,'omitted_entropy_production_term':-3,'positive_production':3},'saved_clock_jets':cases,'python':platform.python_version(),'sympy':s.__version__,'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Conditional exact comparisons and finite coefficient checks; no UDT adoption, practical observation, global result or complete selection.'}
with (B/'EXACT_RESULT.json').open('x') as out:json.dump(result,out,indent=2);out.write('\n')
print(json.dumps(result,indent=2))
