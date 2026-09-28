"""Post-candidate, pre-producer-code independent exact controls."""
import json
import sympy as S

s,t,x,v,L,a=S.symbols('s t x v L a',real=True)
checks=[]
def eq(name,got,want):
    d=S.factor(got-want)
    checks.append(dict(name=name,value=str(got),expected=str(want),residual=str(d),passed=d==0))
    if d!=0:raise AssertionError(checks[-1])
def neq(name,left,right):
    d=S.factor(left-right)
    checks.append(dict(name=name,residual=str(d),passed=d!=0))
    if d==0:raise AssertionError(checks[-1])

# New reciprocal polynomial control: distinct length and polynomial from author.
ell=S.Rational(3,2); bump=x**3*(ell-x)**3
B0=S.integrate(bump,(x,0,ell));B1=S.integrate(x*bump,(x,0,ell))
eq('reciprocal_B0',B0,S.Rational(2187,17920))
eq('reciprocal_B1',B1,S.Rational(6561,71680))
# Affine k=ell*(1,1), h_tt=h_xx=2*t*bump; dlambda=dx/ell.
I=S.integrate(2*ell*(s+x)*bump,(x,0,ell))
V=I/ell;Q=S.diff(V,s)
eq('reciprocal_worldfunction_V',V,2*(s*B0+B1))
eq('reciprocal_Q',Q,S.Rational(2187,8960))
# Null characteristic linearization, formed from the independent ODE.
delta_t=S.integrate(2*(s+x)*bump,(x,0,ell))
eq('reciprocal_ODE_V',delta_t,V)
eq('reciprocal_ODE_Q',S.diff(delta_t,s),Q)
neq('lost_reciprocal_factor_two',Q,B0)

# Minkowski, emitter (s,0), receiver (t,L+v*t+epsilon*a*t^2).
# This tests physical endpoint displacement and its proper-clock normalization.
A=(s+L)/(1-v)
clock_b=-2*a*v*A/(1-v**2)
arrival_V=a*A**2/(1-v)
q=clock_b+S.diff(arrival_V,s)/S.diff(A,s)
# Original Doppler law log Z=atanh(velocity), delta velocity=2*a*A.
original_q=2*a*A/(1-v**2)
eq('moving_receiver_general_Q',q,original_q)
subs={v:S.Rational(3,5),L:S.Rational(7,4),a:S.Rational(2,7),s:S.Rational(5,6)}
eq('moving_receiver_arrival',A.subs(subs),S.Rational(155,24))
eq('moving_receiver_Q',q.subs(subs),S.Rational(3875,672))
neq('missing_worldline_clock_normalization',S.diff(arrival_V,s)/S.diff(A,s),original_q)
neq('missing_arrival_slope',clock_b,original_q)
print(json.dumps(dict(count=len(checks),passed=all(c['passed'] for c in checks),checks=checks),indent=2))
