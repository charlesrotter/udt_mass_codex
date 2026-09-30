"""CCR1 source-first exact anchors; no producer implementation imported."""
import json
import platform
import sys
import sympy as S

checks = []

def equal(name, expr):
    value = S.simplify(expr)
    assert value == 0, (name, value)
    checks.append({'name': name, 'type': 'exact_identity', 'residual': str(value)})

def reject(name, correct, wrong):
    difference = S.simplify(correct-wrong)
    assert difference != 0, (name, difference)
    checks.append({'name': name, 'type': 'wrong_formula_rejected', 'difference': str(difference)})

s, r, e, f, c, z = S.symbols('s r epsilon f c Z', positive=True)
metric = S.diag(-1, 1, 1, 1)
u = S.Matrix([1, 0, 0, 0])
n = S.Matrix([0, 1, 0, 0])
null = u+n
u_cov, n_cov = metric*u, metric*n
H = 2*(u_cov*u_cov.T+n_cov*n_cov.T)
equal('reciprocal_trace', S.trace(metric.inv()*H))
equal('null_normalization', (null.T*metric*u)[0]+1)
equal('null_contraction', (null.T*H*null)[0]-4)
metric_e = S.diag(-S.exp(-2*e*f), S.exp(2*e*f), 1, 1)
equal('finite_determinant', metric_e.det()+1)
equal('finite_family_tangent', S.trace((metric_e.diff(e).subs(e,0)-f*H).T*(metric_e.diff(e).subs(e,0)-f*H)))

# Polynomial beta is an exact integral anchor, not a compact smooth bump witness.
beta = 30*r**2*(1-r)**2
equal('normalized_beta_control', S.integrate(beta,(r,0,1))-1)
delay = S.Function('F')(s)
strain_amplitude = delay*beta/2
source_integral = S.integrate(2*strain_amplitude,(r,0,1))
equal('realized_delay_control', source_integral-delay)
I = c*source_integral
omega_o = c/z
equal('affine_scaling_cancellation', I/omega_o-z*delay)
reject('reject_missing_affine_factor', I/omega_o, source_integral/omega_o)

# Direct perturbed arrival derivative, independent of variational action code.
arrival = s+s**2/2
Z = S.diff(arrival,s)
D = S.log(Z)
a = 1+s+s**2
arrival_e = arrival+e*Z*a
Q_direct = S.diff(S.log(S.diff(arrival_e,s)),e).subs(e,0)
Q_formula = S.diff(a,s)+S.diff(D,s)*a
equal('full_arrival_derivative', Q_direct-Q_formula)
reject('reject_frozen_redshift', Q_direct, S.diff(a,s))
reject('reject_frozen_arrival_event', Q_direct, S.Integer(0))

theta = s**2
F_angle = s*theta**2
full_angle = S.diff(F_angle,s)+S.diff(D,s)*F_angle
partial_only = theta**2+S.diff(D,s)*F_angle
reject('reject_omitted_direction_motion', full_angle, partial_only)

# Exact integration-by-parts check with zero boundary weights.
w = s**2*(1-s)**2
M = 2+s
B = (M**2+1)/2
test = 1+3*s+s**2
raw = S.integrate(w*(M*S.diff(test,s)+S.diff(B,s)*test),(s,0,1))
ibp = S.integrate((w*S.diff(B,s)-S.diff(w*M,s))*test,(s,0,1))
equal('weighted_necessary_condition',raw-ibp)
wrong_ibp = S.integrate(w*(S.diff(B,s)-S.diff(M,s))*test,(s,0,1))
reject('reject_omitted_weight_derivative',raw,wrong_ibp)

# Readout-only positive witness with D=1+s, a=exp(2s), w>=0.
# This illustrates the sign algebra, not a new CES1 curved metric construction.
D_positive = 1+s
a_positive = S.exp(2*s)
Q_positive = S.diff(a_positive,s)+S.diff(D_positive,s)*a_positive
equal('positive_delay_derivative',Q_positive-3*S.exp(2*s))
positive_derivative = S.integrate(w*D_positive*Q_positive,(s,0,1))
assert positive_derivative.is_positive is True
checks.append({'name':'positive_readout_sign','type':'exact_sign','value':str(positive_derivative)})

result = {
    'scope':'source-first algebra anchors; analytic hypotheses and proof in SOURCE_FIRST.md',
    'python':sys.version,
    'sympy':S.__version__,
    'platform':platform.platform(),
    'checks':checks,
    'counts':{
        kind:sum(x['type']==kind for x in checks)
        for kind in sorted({x['type'] for x in checks})
    },
    'all_passed':True,
}
print(json.dumps(result,indent=2))
