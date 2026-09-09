"""LG2 independent exact checks; original author's proof/code not yet exposed.

Controls are supplied diagnostic choices, not physical premises. No PDE
existence, smooth inverse, or genericity claim is certified by finite algebra.
"""
import itertools
import json
import platform
import sympy as s

x, y, z = s.symbols('x y z', real=True)
q, T = s.symbols('q T', positive=True)
X = s.Matrix([x, y, z])
basis = [s.eye(3)[:, j] for j in range(3)] + [s.Matrix([0, -z, y])]
representations = []
for signs in itertools.product((-1, 1), repeat=3):
    R = s.diag(*signs)
    cols = []
    for field in basis:
        transformed = R * field.subs(dict(zip(X, R * X)), simultaneous=True)
        coeffs = s.symbols('c0:4')
        residual = transformed - sum((c * b for c, b in zip(coeffs, basis)), s.zeros(3, 1))
        equations = [co for r in residual for co in s.Poly(r, x, y, z).coeffs()]
        solution, = s.solve(equations, coeffs, dict=True)
        cols.append(s.Matrix([solution[c] for c in coeffs]))
    representations.append(s.Matrix.hstack(*cols))
average = sum(representations, s.zeros(4)) / 8
assert average == s.zeros(4)
inversion = representations[0]
weak_parity_average = (s.eye(4) + inversion) / 2
assert weak_parity_average.rank() == 1
assert weak_parity_average * s.eye(4)[:, 3] == s.eye(4)[:, 3]

# A separately chosen rational parametrization, not a sampled constraint fit.
p = s.Matrix([-q, 1 + q, q * (1 + q)]) / (1 + q + q**2)
K = -s.diag(*p) / T
tau = s.trace(K)
assert s.factor(tau + 1 / T) == 0
H = s.factor(tau**2 - s.trace(K*K))
assert H == 0
momentum = [s.simplify(sum(s.diff(K[j, i], X[j]) for j in range(3)) - s.diff(tau, X[i])) for i in range(3)]
assert momentum == [0, 0, 0]
assert p.subs(q, 1) == s.Matrix([-s.Rational(1, 3), s.Rational(2, 3), s.Rational(2, 3)])

# Vacuum Gauss projection on these flat, constant-K patches:
# E = Ric(gamma) + tau*K - K^2, and B = curl K = 0.
E = s.simplify(tau*K-K*K)
assert s.factor(s.trace(E)) == 0
lam = s.symbols('lam')
characteristic = s.factor((lam*s.eye(3)-E).det())
discriminant = s.factor(s.discriminant(characteristic, lam))
product = s.factor(s.prod((E[i, i]-E[j, j])**2 for i in range(3) for j in range(i+1, 3)))
assert s.factor(product-discriminant) == 0
assert discriminant.subs(q, 1) == 0
assert discriminant.subs({q: s.Rational(6, 5), T: 1}) > 0
I2 = s.trace(E*E)
I3 = s.trace(E*E*E)
assert s.factor(discriminant-(I2**3 / 2 - 3*I3**2)) == 0

# Catch the false inference that lawful endpoints make their cutoff blend lawful.
c = s.symbols('c', real=True)
K0 = K.subs(q, 1)
delta = s.simplify(K-K0)
blend = K0+c*delta
blend_H = s.factor(s.trace(blend)**2-s.trace(blend*blend))
assert s.factor(blend_H-c*(1-c)*s.trace(delta*delta)) == 0
assert blend_H.subs({c: s.Rational(1, 2), q: s.Rational(6, 5), T: 1}) > 0
gradient = s.Matrix([1, 2, 3])
blend_M = delta*gradient
assert any(v.subs({q: s.Rational(6, 5), T: 1}) != 0 for v in blend_M)

print(json.dumps({
    'python': platform.python_version(), 'sympy': s.__version__,
    'evidence': 'independent exact rational/symbolic algebra, not PDE certification',
    'group_average': str(average),
    'central_inversion_surviving_dimension': weak_parity_average.rank(),
    'kasner_hamiltonian': str(H),
    'kasner_momentum': [str(v) for v in momentum],
    'weyl_discriminant': str(discriminant),
    'nonzero_discriminant_control': str(discriminant.subs({q:s.Rational(6,5),T:1})),
    'blend_hamiltonian': str(blend_H),
    'nonzero_blend_hamiltonian_control': str(blend_H.subs({c:s.Rational(1,2),q:s.Rational(6,5),T:1})),
    'blend_momentum_control': [str(v.subs({q:s.Rational(6,5),T:1})) for v in blend_M],
    'catch_controls': {'central_inversion_is_insufficient': True,
                       'lawful_endpoints_do_not_make_blend_lawful': True},
}, sort_keys=True, indent=2))
