#!/usr/bin/env python3
"""Direct, proof-exposed algebra review; not an independent geometry rebuild."""
import json
import platform
import sympy as s

r = s.symbols('r', positive=True)
alpha = s.symbols('alpha', nonzero=True)
u, v, p, q, C, scalar, box_scalar = s.symbols('u v p q C scalar box_scalar')
checks = []


def zero(name, expr):
    residual = s.simplify(expr)
    if residual != 0:
        raise AssertionError((name, residual))
    checks.append(name)


F = 1 + 2*alpha*scalar
L = scalar + alpha*scalar**2
trace = s.expand(F*scalar - 2*L + 6*alpha*box_scalar)
zero('trace_algebra', trace - (-scalar + 6*alpha*box_scalar))

# Volume-form divergence, rather than the candidate's expanded box formula.
f = 1 + p/r + q/r**2 - v*r**2/12 - u*r**3/20
R = -s.diff(f, r, 2) - 4*s.diff(f, r)/r - 2*(f-1)/r**2
zero('integrated_scalar_family', R - (u*r+v))
box_R = s.diff(r**2 * f * s.diff(R, r), r) / r**2
poly = s.Poly(s.expand(r**2*(-R + 6*alpha*box_R - 4*C)), r)
zero('open_interval_linear_coefficient', poly.coeff_monomial(r) - 12*alpha*u)
zero('open_interval_quartic_coefficient', poly.coeff_monomial(r**4) + s.Rational(3,2)*alpha*u**2)
zero('trace_after_u_zero', s.expand(poly.as_expr().subs(u,0)) - (-v-4*C)*r**2)

fc = f.subs(u,0)
ric_t = -s.diff(fc,r,2)/2 - s.diff(fc,r)/r
ric_angle = (1-fc-r*s.diff(fc,r))/r**2
zero('constant_scalar_time_tracefree', ric_t-v/4+q/r**4)
zero('constant_scalar_angular_tracefree', ric_angle-v/4-q/r**4)
zero('remaining_DDR_factor', s.expand((1+2*alpha*v)*(ric_angle-v/4)) - (1+2*alpha*v)*q/r**4)

R0 = -1/(2*alpha)
F0 = F.subs(scalar,R0)
L0 = L.subs(scalar,R0)
C0 = 1/(8*alpha)
zero('exceptional_F_zero',F0)
zero('exceptional_pure_trace_equals_Cg', -L0/2-C0)
# In the variation of E-Cg, the direct h term cancels and delta L=F0 delta R=0.
zero('fixed_C_metric_variation_cancellation', -L0/2-C0)
zero('fixed_C_delta_L_coefficient',F0)
zero('linearized_trace_operator',s.diff(trace,scalar)+1)
zero('linearized_trace_box_coefficient',s.diff(trace,box_scalar)-6*alpha)

result = {
    'status':'PASS_DIRECT_REVIEW_ALGEBRA',
    'python':platform.python_version(),
    'sympy':s.__version__,
    'exposure':'candidate proof read before this separately written check; no parent script or output imported',
    'method':'exact symbolic direct check; sourced/candidate tensor formulas, not independent Riemann reconstruction',
    'checks':checks,
    'check_count':len(checks),
    'trace_polynomial':str(poly.as_expr()),
    'exceptional_R':str(R0),
    'exceptional_E_coefficient':str(-L0/2),
    'full_action_stationarity_excludes_exceptional_for_finite_nonzero_alpha':bool(C0.is_zero is False),
    'scope_limits':['no principal-system causality or stability proof','no physical response adoption','no full metric perturbation realization classification'],
}
print(json.dumps(result,indent=2))
