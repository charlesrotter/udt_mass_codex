"""Exact algebra/causal controls only; no numerical PDE or existence proof."""
import argparse
import itertools
import json
import platform

import sympy as s

parser = argparse.ArgumentParser()
parser.add_argument('--mutant', choices=['absolute_equals_shape', 'linear_blindness',
                                          'electric_only', 'unit_coordinate_cone'])
args = parser.parse_args()
checks = []


def equal(name, expr):
    residual = s.simplify(s.expand(expr))
    assert residual == 0, (name, residual)
    checks.append(name)


T, T0 = s.symbols('T T0', positive=True)
p = s.symbols('p1 p2 p3', real=True)
g = [-s.S.One] + [(T / T0) ** (2 * pi) for pi in p]
inv = [1 / gi for gi in g]


def derivative(value, index):
    return s.diff(value, T) if index == 0 else s.S.Zero


# Direct coordinate connection from the full diagonal metric, not the E formula.
Gamma = {}
for a, b, c in itertools.product(range(4), repeat=3):
    value = inv[a] * (derivative(g[a] if a == c else 0, b)
                      + derivative(g[a] if a == b else 0, c)
                      - derivative(g[b] if b == c else 0, a)) / 2
    Gamma[a, b, c] = s.simplify(value)

R = {}
for a, b, c, d in itertools.product(range(4), repeat=4):
    mixed = derivative(Gamma[a, d, b], c) - derivative(Gamma[a, c, b], d)
    mixed += sum(Gamma[a, c, e] * Gamma[e, d, b]
                 - Gamma[a, d, e] * Gamma[e, c, b] for e in range(4))
    R[a, b, c, d] = s.simplify(g[a] * mixed)
electric = [s.simplify(R[i, 0, i, 0] / g[i]) for i in range(1, 4)]
for i in range(3):
    equal('direct_electric_' + str(i), electric[i] - p[i] * (1 - p[i]) / T**2)
equal('all_magnetic_components_zero', sum(R[0, i, j, k] ** 2
      for i, j, k in itertools.product(range(1, 4), repeat=3)))
kretsch = s.simplify(sum(value**2 * inv[a] * inv[b] * inv[c] * inv[d]
                       for (a, b, c, d), value in R.items()))
expected = 4 * (sum(pi**2 * (1 - pi)**2 for pi in p)
                + sum(p[i]**2 * p[j]**2 for i in range(3) for j in range(i+1, 3))) / T**4
equal('full_contraction', kretsch - expected)
constraints = s.groebner([sum(p)-1, sum(pi*pi for pi in p)-1], *p)


def kasner_equal(name, expr):
    equal(name, constraints.reduce(s.expand(expr))[1])


P = s.prod(p)
ec = [s.simplify(ei*T*T) for ei in electric]
I2c, I3c = sum(ei**2 for ei in ec), sum(ei**3 for ei in ec)
kasner_equal('tracefree_from_constraints', sum(ec))
kasner_equal('I2_product_identity', I2c + 2*P)
kasner_equal('I3_product_identity', I3c + 3*P**2)
kasner_equal('Kretschmann_product_identity', kretsch*T**4 + 16*P)
for a, b in itertools.product(range(4), repeat=2):
    ric = s.simplify(sum(inv[c] * R[c, a, c, b] for c in range(4)))
    # Remove positive metric factors before polynomial constraint reduction.
    kasner_equal('Ric_' + str(a) + str(b), s.simplify(ric*T**2/(g[a] if a == b else 1)))

u = s.symbols('u', real=True)
c, sn = (1-u*u)/(1+u*u), 2*u/(1+u*u)
pu = [(1-2*c)/3, (1+c-s.sqrt(3)*sn)/3, (1+c+s.sqrt(3)*sn)/3]
P_u = s.factor(s.expand(s.prod(pu)))
E_u = [s.factor(pi*(1-pi)/T**2) for pi in pu]
I2, I3 = sum(ei**2 for ei in E_u), sum(ei**3 for ei in E_u)
A = s.factor(1-6*I3**2/I2**3)
expected_A = u*u*(u*u-3)**2/(1+u*u)**3
equal('exact_LG2_shape', A-expected_A)
equal('shape_is_constant', s.diff(A, T))
equal('shape_product_identity', A-1-s.Rational(27, 4)*P_u)
Ku = s.factor(-16*P_u/T**4)
equal('absolute_decay_derivative', s.diff(Ku, T)+4*Ku/T)
equal('Taub_K', Ku.subs(u, 0)-s.Rational(64, 27)/T**4)
equal('initial_linear_blindness', s.diff(A, u).subs(u, 0))
equal('second_derivative', s.diff(A, u, 2).subs(u, 0)-18)
assert A.subs(u, s.Rational(1,100)) > 0
checks.append('nonzero_shape_at_small_parameter')

# Actual complex orthogonal change of Weyl frame: full Q invariants survive;
# using its real electric part alone in the boosted frame does not.
O = s.Matrix([[s.Rational(5,4), 3*s.I/4, 0],
              [-3*s.I/4, s.Rational(5,4), 0], [0, 0, 1]])
assert O*O.T == s.eye(3) and O.det() == 1
Q = s.diag(-4,2,2)
Qboost = O*Q*O.T


def shape(matrix):
    return s.simplify(1-6*s.trace(matrix**3)**2/s.trace(matrix**2)**3)


equal('full_Weyl_frame_invariance', shape(Qboost)-shape(Q))
electric_only_shape = shape(s.re(Qboost))
assert electric_only_shape != shape(Q)
checks.append('electric_only_shortcut_rejected')

# Sufficient Euclidean coordinate travel bound in the supplied Kasner marking.
m = s.symbols('m', negative=True)
L = T0*((T/T0)**(1-m)-1)/(1-m)
equal('causal_integral_derivative', s.diff(L,T)-(T/T0)**(-m))
equal('causal_integral_initial_value', L.subs(T,T0))
fast_axis_speed = 2**s.Rational(1,3)  # lawful Taub control, T=2T0
assert fast_axis_speed > 1
checks.append('unit_coordinate_speed_shortcut_rejected')

# Deliberately wrong conclusions; each requested mutation must exit nonzero.
if args.mutant == 'absolute_equals_shape':
    assert s.simplify(A.subs(T,2*T)-A/16) == 0, 'K decay is not shape decay'
if args.mutant == 'linear_blindness':
    assert A.subs(u,s.Rational(1,100)) == 0, 'zero first variation misses quadratic shape'
if args.mutant == 'electric_only':
    assert electric_only_shape == shape(Q), 'electric spectrum alone is frame dependent'
if args.mutant == 'unit_coordinate_cone':
    assert fast_axis_speed <= 1, 'proper causal cone is not unit coordinate speed'

print(json.dumps(dict(status='PASS', python=platform.python_version(),
    python_build=platform.python_build(), sympy=s.__version__, checks=checks,
    electric_from_metric=[str(x) for x in electric], generic_K=str(kretsch),
    P_u=str(P_u), shape_A=str(A), shape_series=str(s.series(A,u,0,6)),
    K_u=str(Ku), electric_only_boosted_shape=str(electric_only_shape),
    sufficient_travel_bound=str(L),
    omissions=['not a general PDE or gluing proof','not numerical evolution',
               'no uniform lifetime','no late-time or generic stability',
               'not independent author context']), indent=2))
