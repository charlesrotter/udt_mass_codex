"""Focused post-exposure source-interface and candidate-parametrization checks."""
import json
import platform
import sympy as s

t, j, dj = s.symbols('t j dj', real=True)
metric = s.diag(1+t, 1, 1)
covector = s.Matrix([j+t*dj, 0, 0])
raised = metric.inv()*covector
extra = s.simplify(raised.diff(t).subs(t,0)-covector.diff(t).subs(t,0))
assert extra == s.Matrix([-j,0,0])
assert extra.subs(j,1) != s.zeros(3,1)

u = s.symbols('u', real=True)
a = s.symbols('a', positive=True)
# Reconstruct candidate K from its circle parameter after candidate exposure.
k = s.Matrix([a*(1-3*u*u)/(1+u*u),
              a*(-2+2*s.sqrt(3)*u)/(1+u*u),
              a*(-2-2*s.sqrt(3)*u)/(1+u*u)])
K = s.diag(*k)
tau = s.trace(K)
assert s.factor(tau+3*a)==0
assert s.factor(tau*tau-s.trace(K*K))==0
E = s.simplify(tau*K-K*K)
invariant_discriminant = s.factor(s.trace(E*E)**3/2-3*s.trace(E*E*E)**2)
expected = 6912*a**12*u**2*(3*u**2-1)**6*(u**2-3)**2/(u**2+1)**12
assert s.factor(invariant_discriminant-expected)==0
assert invariant_discriminant.subs(u,0)==0
assert invariant_discriminant.subs({u:s.Rational(1,10),a:1})>0
assert invariant_discriminant.subs({u:-s.Rational(1,10),a:1})>0
# On 0<|u|<1/10, every displayed factor is nonzero; this establishes the
# interval algebraically, not by interpreting the endpoint samples as a sweep.
assert 3*s.Rational(1,10)**2 < 1
assert s.Rational(1,10)**2 < 3

print(json.dumps({'python':platform.python_version(),'sympy':s.__version__,
 'stage':'direct, post-candidate exposure',
 'raised_map_extra_derivative':str(extra),
 'candidate_weyl_discriminant_via_traces':str(invariant_discriminant),
 'rejected_shortcut':'variable metric raising has identical nonlinear linearization',
 'scope':'exact symbolic source-interface and finite-family algebra; not PDE certification'
},indent=2,sort_keys=True))
