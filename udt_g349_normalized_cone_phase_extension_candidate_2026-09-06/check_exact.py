"""Small exact witnesses; no numerical solve and no accepted-source imports.

All witness values are FREE mathematical controls, not physical parameters.
Prints JSON to stdout; writes no files. Mutation modes alter evaluated helpers.
"""
import argparse
import json
import platform
import sympy as S

parser = argparse.ArgumentParser()
parser.add_argument('--mutation', choices=['acceleration_zero', 'pullback_only',
                                         'omit_frequency', 'area_radius'])
args = parser.parse_args()
checks = []
t, x, y, z, c, a = S.symbols('t x y z c a', real=True)
coords = (t, x, y, z)
eta = S.diag(-1, 1, 1, 1)


def require(name, condition):
    if condition is not True and condition != S.true:
        raise AssertionError(name)
    checks.append(name)


def equal(name, actual, expected):
    require(name, S.simplify(actual - expected) == 0)


def acceleration(vector):
    if args.mutation == 'acceleration_zero':
        return S.zeros(4, 1)
    return S.Matrix([sum(vector[j] * S.diff(v, coords[j]) for j in range(4))
                     for v in vector])


def ambient_match(covector, expected, tangents):
    if args.mutation == 'pullback_only':
        return all(S.simplify(covector.dot(v)) == 0 for v in tangents)
    return all(S.simplify(p - q) == 0 for p, q in zip(covector, expected))


def area(gram):
    result = S.sqrt(gram.det())
    return S.sqrt(result) if args.mutation == 'area_radius' else result


def rate(omega, spacing, density, jacobian):
    weight = 1 if args.mutation == 'omit_frequency' else omega
    return weight * density / (spacing * jacobian)


# Initial first jet: arbitrary smooth functions, not a fitted initial profile.
rho, v, w = S.symbols('rho v w', real=True)
aa = S.Function('a')(v, w)
bb = S.Function('b')(rho, v, w)
phi = aa * rho + rho**2 * bb
equal('initial_value', phi.subs(rho, 0), 0)
for var, target in [(rho, aa), (v, 0), (w, 0)]:
    equal('initial_derivative_' + str(var), S.diff(phi, var).subs(rho, 0), target)
q1, q2, q3 = S.symbols('q1 q2 q3', real=True)
Qnorm = S.sqrt(q1*q1 + q2*q2 + q3*q3)
P = S.Matrix([-Qnorm, q1, q2, q3])
equal('future_null_branch_norm', (P.T * eta * P)[0], 0)
equal('future_branch_rational_clock', -P[0].subs({q1: 3, q2: 4, q3: 0}), 5)

# Exact implicit shifted-cone family, without solving a PDE or scalar root.
radius = S.sqrt(x*x + y*y + z*z)
shifted_radius = S.sqrt((x-a*c*c)**2 + y*y + z*z)
F = shifted_radius - t - c
Fc = S.diff(F, c)
D = 1 + 2*a*c*(x-a*c*c)/shifted_radius
equal('implicit_denominator', Fc, -D)
equal('implicit_ift_on_cone', Fc.subs(c, 0), -1)
implicit_gradient = S.Matrix([-S.diff(F, q)/Fc for q in coords])
base_gradient = S.Matrix([-1, x/radius, y/radius, z/radius])
equal('implicit_eikonal', (implicit_gradient.T*eta*implicit_gradient)[0], 0)
for i in range(4):
    equal('ambient_cone_component_' + str(i), implicit_gradient[i].subs(c, 0),
          base_gradient[i])
point = {a: 1, c: S.Rational(1, 10), x: S.Rational(1, 100),
         y: 1, z: 0, t: S.Rational(9, 10)}
equal('implicit_off_cone_value', F.subs(point), 0)
equal('implicit_off_cone_D', D.subs(point), 1)
ip = implicit_gradient.subs(point).applyfunc(S.simplify)
bp = base_gradient.subs(point).applyfunc(S.simplify)
for i, target in enumerate([-1, 0, 1, 0]):
    equal('implicit_off_cone_component_' + str(i), ip[i], target)
require('not_same_foliation_normal', S.simplify(ip[0]*bp[1]-ip[1]*bp[0]) != 0)
require('implicit_off_cone_future', -ip[0] > 0)

# Reparameterization preserves the ambient first jet on N, not off N.
theta0 = radius - t
factor = 1 + 2*a*theta0
regradient = factor*base_gradient
equal('reparameterized_eikonal', (regradient.T*eta*regradient)[0], 0)
for i in range(4):
    equal('reparameterized_cone_component_' + str(i), regradient[i].subs(t, radius),
          base_gradient[i])
equal('off_cone_rescaled_clock', -regradient[0].subs({a: 1, x: 0, y: 1, z: 0,
                                                  t: S.Rational(9, 10)}),
      S.Rational(6, 5))

# G349 affine geometry and an intentionally nonaffine hostile control.
K = eta * base_gradient
for i, acc in enumerate(acceleration(K)):
    equal('cone_affine_component_' + str(i), acc, 0)
ell = S.Matrix([1+t, 0, 0, 1+t])
ell_acc = acceleration(ell)
equal('nonaffine_nonzero_component', ell_acc[0], 1+t)
equal('nonaffine_parallel_component', ell_acc[3], 1+t)

# Full ambient matching versus the vacuous tangent pullback.
direction = S.Matrix([S.Rational(3, 5), S.Rational(4, 5), 0])
e1 = S.Matrix([S.Rational(4, 5), -S.Rational(3, 5), 0])
e2 = S.Matrix([0, 0, 1])
k = S.Matrix([1, *direction])
beta = eta*k
screen1, screen2 = S.Matrix([0, *e1]), S.Matrix([0, *e2])
tangents = [k, screen1, screen2]
require('matching_accepts_prescribed_beta', ambient_match(beta, beta, tangents))
require('matching_rejects_hidden_factor_two', not ambient_match(2*beta, beta, tangents))
for i, tangent in enumerate(tangents):
    equal('scaled_beta_still_zero_pullback_' + str(i), (2*beta).dot(tangent), 0)
equal('scaled_beta_changes_observer_clock', -(2*beta)[0], 2)

# Variable-cut Gram matrix, exact on an orthonormal tangent frame at this label.
r = S.symbols('r', positive=True)
g1, g2 = S.symbols('g1 g2', real=True)
B = S.Matrix.hstack(g1*k + r*screen1, g2*k + r*screen2)
gram = S.simplify(B.T*eta*B)
for i in range(2):
    for j in range(2):
        equal('cut_gram_' + str(i) + str(j), gram[i, j], r*r if i == j else 0)
equal('metric_area_not_radius', area(gram), r*r)
observers = [S.Matrix([1, 0, 0, 0]),
             S.Matrix([S.Rational(13, 12), *(S.Rational(5, 12)*direction)])]
omegas = [-observer.dot(beta) for observer in observers]
spacing, density = S.Rational(3, 2), S.Rational(7, 5)
radii = [S.Integer(3), S.Integer(5)]
jacobians = [area(gram).subs(r, rr) for rr in radii]
rates = [rate(omega, spacing, density, jac) for omega, jac in zip(omegas, jacobians)]
for i, observer in enumerate(observers):
    equal('observer_unit_' + str(i), (observer.T*eta*observer)[0], -1)
    require('observer_future_' + str(i), observer[0] > 0)
equal('clock_at_second_cut', omegas[1], S.Rational(2, 3))
equal('absolute_rate_first_cut', rates[0], S.Rational(14, 135))
equal('absolute_rate_second_cut', rates[1], S.Rational(28, 1125))
equal('transfer_ratio', rates[1]/rates[0], S.Rational(6, 25))
equal('zero_measure_zero_rate', rate(omegas[0], spacing, 0, jacobians[0]), 0)

print(json.dumps({
    'status': 'PASS_EXACT_WITNESSES_NOT_GENERAL_PROOF',
    'python': platform.python_version(), 'sympy': S.__version__,
    'mutation': args.mutation, 'assertion_count': len(checks), 'checks': checks,
    'implicit_off_cone_gradient': [str(q) for q in ip],
    'base_off_cone_gradient': [str(q) for q in bp],
    'saved_readout_inputs': {
        'direction': [str(q) for q in direction],
        'screen1': [str(q) for q in e1], 'screen2': [str(q) for q in e2],
        'cut_gradients': ['1/3', '-2/7'],
        'radii': [str(q) for q in radii],
        'observers': [[str(q) for q in obs] for obs in observers],
        'spacing': str(spacing), 'density': str(density)},
    'readout_outputs': {'jacobians': [str(q) for q in jacobians],
                        'omegas': [str(q) for q in omegas],
                        'rates': [str(q) for q in rates],
                        'ratio': str(rates[1]/rates[0])}
}, indent=2))
