"""Independent FCV1 controls. No producer or candidate imports."""
import json
import platform
import sympy as S

s,x,e,t=S.symbols('s x e t', real=True)
checks=[]
def eq(name,got,want):
    residual=S.simplify(got-want)
    checks.append(dict(name=name,got=str(got),want=str(want),residual=str(residual),passed=residual==0))
    if residual!=0: raise AssertionError(checks[-1])
def neq(name,left,right):
    residual=S.simplify(left-right)
    checks.append(dict(name=name,residual=str(residual),passed=residual!=0))
    if residual==0: raise AssertionError(checks[-1])

# Metric -dt^2+(1+e*t*f(x))^2 dx^2+dy^2+dz^2; fixed static observers.
# Null equation dt/dx=1+e*t*f gives d_s T=exp(e*integral f).
f=x**2*(1-x)**2
A=S.integrate(f,(x,0,1)); B=S.integrate(x*f,(x,0,1))
J=S.integrate((s+x)*f,(x,0,1))
eq('interior_A',A,S.Rational(1,30))
eq('interior_B',B,S.Rational(1,60))
eq('arrival_first_variation',J,s*A+B)
eq('ratio_first_variation',S.diff(J,s),A)
eq('exact_ODE_ratio',S.diff(S.log(S.exp(e*A)),e).subs(e,0),A)
eq('endpoint_metric_variation_A',f.subs(x,0),0)
eq('endpoint_metric_variation_B',f.subs(x,1),0)
neq('endpoint_only_mutant_rejected',A,0)

# Joint pullback: h=L_X eta, xi=-X. Baseline ray k=(1,1), X=(t^2,0).
g=S.diag(-1,1); k=S.Matrix([1,1]); X=S.Matrix([t**2,0])
h=S.diag(-4*t,0)
Jg=S.integrate((k.T*h.subs(t,s+x)*k)[0]/2,(x,0,1))
pA=-(g*k); pB=g*k
xiA=-X.subs(t,s); xiB=-X.subs(t,s+1)
eq('gauge_world_function',Jg+(pA.T*xiA)[0]+(pB.T*xiB)[0],0)
v=S.Matrix([1,0]); xidot=-S.diff(X,t)
eq('gauge_clock_rate',(v.T*h*v)[0]+2*(v.T*g*xidot)[0],0)
neq('metric_only_gauge_mutant_rejected',Jg,0)

# Nonlinear proper-time map F_e(s)=s^2+e*s, locally s>0.
# It has an explicit future-timelike Minkowski realization in the review text.
F=s**2+e*s
inv=(-e+S.sqrt(e**2+4*t))/2
q=S.diff(S.log(S.diff(F,s)),e).subs(e,0)
qinv=S.diff(S.log(S.diff(inv,t)),e).subs(e,0)
eq('inverse_fixed_target',qinv,0)
eq('inverse_response_with_argument_shift',-q+S.Rational(1,2)*S.diff(S.log(2*s),s),0)
neq('inverse_missing_shift_mutant_rejected',-q,qinv)
eq('inverse_pair_slope_identity',(S.diff(inv,t).subs(t,F)*S.diff(F,s))**2,1)

# Conformal g_e=exp(2e*(t^2+x))*eta leaves coordinate null arrival t=s+1.
eq('conformal_log_ratio_response',((t**2+x).subs({t:s+1,x:1})-(t**2+x).subs({t:s,x:0})),2*s+2)

# Base g=(1+t)^2 eta; homothety exp(2e), fixed clock origin t=0.
# Coordinate ratio unchanged but fixed source proper-time relocates s.
r=(s+2)/(s+1); tau=s+s**2/2; shift=-tau/(s+1)
eq('proper_time_anchor_response',shift*S.diff(S.log(r),s),s/(2*(s+1)**2))
neq('fixed_label_vs_proper_time_mutant_rejected',shift*S.diff(S.log(r),s),0)
print(json.dumps(dict(python=platform.python_version(),sympy=S.__version__,checks=checks,
                     count=len(checks),passed=all(c['passed'] for c in checks)),indent=2))
