"""Exact producer algebra; analytic support/sign proof remains in the candidate."""
import json
import platform
from pathlib import Path
import sympy as S

s, L, B0, B1, q = S.symbols('s L B0 B1 q', positive=True)
e, dt, f = S.symbols('epsilon delta_T f', real=True)
v = (q*q-1)/(q*q+1)  # q=exp(eta), physical family q>1
rate = 2*q/(q*q+1)  # sqrt(1-v**2), q>0
T0 = (s+L)/(1-v)
R0 = L+v*T0
checks, rejected = {}, {}

def eq(name, a, b=0):
    residual = S.factor(S.simplify(a-b))
    checks[name] = str(residual)
    assert residual == 0, (name, residual)

def wrong(name, a, b):
    residual = S.factor(S.simplify(a-b))
    rejected[name] = str(residual)
    assert residual != 0, name  # nonidentity on the open q>1 domain

eq('proper_normalization', rate**2, 1-v**2)
eq('rapidity_clock_factor', rate/(1-v), q)
intercept = (T0+e*dt) - (s+L+v*(T0+e*dt)+2*e*(s*B0+B1))
eq('baseline_interception', intercept.subs(e,0))
delta_T = S.solve(S.diff(intercept,e),dt)[0]
eq('moving_receiver', delta_T, 2*(s*B0+B1)/(1-v))
A0 = S.simplify(rate*T0)
delta_A = S.simplify(rate*delta_T)
eq('proper_arrival', A0, q*(s+L))
eq('proper_arrival_variation', delta_A, 2*q*(s*B0+B1))
Z0 = S.diff(A0,s)
delta_Z = S.diff(delta_A,s)
eq('baseline_tick_ratio', Z0, q)
eq('tick_ratio_variation', delta_Z, 2*q*B0)
delta_D = S.cancel(delta_Z/Z0)
eq('contrast_variation', delta_D, 2*B0)
eq('contrast_density', S.log(Z0)*delta_D, 2*B0*S.log(q))

I = 2*R0*(s*B0+B1)
omega = R0/q
V = I/omega
Qfull = (S.diff(I,s)/omega-I*S.diff(omega,s)/omega**2)/Z0
eq('affine_endpoint_crosscheck', V, delta_A)
eq('full_denominator_derivative', Qfull, delta_D)
eq('matched_inverse_product', (-S.log(q))*(-delta_D), S.log(q)*delta_D)
eq('zero_rapidity_control', (S.log(q)*delta_D).subs(q,1))
g = S.diag(-S.exp(-2*e*f),S.exp(2*e*f),1,1)
h = g.diff(e).subs(e,0)
eq('finite_metric_determinant', g.det(), -1)
eq('reciprocal_trace', S.trace(g.subs(e,0).inv()*h))
eq('strain_tt_factor', h[0,0], 2*f)
eq('strain_rr_factor', h[1,1], 2*f)
wrong('dropped_receiver_motion', delta_T, 2*(s*B0+B1))
wrong('dropped_clock_normalization', delta_A, delta_T)
wrong('dropped_frequency_denominator_derivative', Qfull, S.diff(I,s)/omega/Z0)
wrong('missing_reciprocal_factor_two', delta_D, B0)

result = {'status':'PASS','kind':'exact_symbolic_regression_not_physical_adoption',
          'python':platform.python_version(),'sympy':S.__version__,
          'domain':'q=exp(eta)>1; B0>0; finite compact smooth controls in candidate',
          'exact_identities':checks,'rejected_nonidentities':rejected,
          'conclusion':'delta C = 2 B0 mean(eta) > 0 for frozen preparation class'}
out = Path(__file__).with_name('algebra_result.json')
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
