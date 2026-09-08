"""Independent source-first CD1 normal-form/coarea checks. Exact, not existence."""
import json
import platform
import sympy as S

x, y, z = S.symbols('x y z', real=True)
beta, lam = S.symbols('beta lam', nonzero=True, real=True)
T, B, C, D, V = [S.Function(n)(x, y, z) for n in ['T', 'B', 'C', 'D', 'V']]
profile = S.Function('s')(y, z)
F = S.Function('F')(x)
source = beta * profile * S.diff(F, x)**2
A = (2 * lam + 2 * source - (T*T-D*D)/2 + 2*(B*B+C*C+V*V))/(2*T)
K = S.Matrix([[A, B, C], [B, (T+D)/2, V], [C, V, (T-D)/2]])
coords = [x, y, z]
tr = S.trace(K)
hamiltonian = tr*tr-S.trace(K*K)-2*lam-2*source
momentum = [sum(S.diff(K[j, i], coords[j]) for j in range(3))-S.diff(tr, coords[i]) for i in range(3)]
normal = {
    S.diff(T, x): S.diff(B, y)+S.diff(C, z)-source,
    S.diff(B, x): S.diff(A+(T-D)/2, y)-S.diff(V, z),
    S.diff(C, x): S.diff(A+(T+D)/2, z)-S.diff(V, y),
}
checks = []
def zero(name, value):
    residual = S.factor(value)
    assert residual == 0, (name, residual)
    checks.append({'name': name, 'residual': str(residual)})

zero('full_flat_H_after_algebraic_elimination', hamiltonian)
for i, expected in enumerate([source, 0, 0]):
    zero('full_flat_M_'+str(i), momentum[i].subs(normal, simultaneous=True)-expected)

# Negative controls evaluate actual nonzero symbolic expressions at exact data.
bad = {}
wrong_sign = dict(normal)
wrong_sign[S.diff(T, x)] = S.diff(B, y)+S.diff(C, z)+source
bad['reversed_momentum_sign'] = S.factor(momentum[0].subs(wrong_sign, simultaneous=True)-source)
lost_transverse = dict(normal)
lost_transverse[S.diff(T, x)] = -source
bad['lost_transverse_divergence'] = S.factor(momentum[0].subs(lost_transverse, simultaneous=True)-source)
bad['missing_density_source_H'] = S.factor(hamiltonian.subs(lam, lam)-2*source)
values = {beta: S.Rational(-3, 2), profile: 5, S.diff(F, x): 2,
          S.diff(B, y): 7, S.diff(C, z): 11}
for name, expr in list(bad.items()):
    value = S.simplify(expr.subs(values))
    assert value.is_number and value != 0, (name, expr, value)
    bad[name] = {'expression': str(expr), 'nonzero_exact_value': str(value)}

# General spatial coarea identity in phase-adapted coordinates, including shifts.
L = S.Matrix([[2, 0, 0], [S.Rational(1,3), 3, 0], [S.Rational(-2,5), S.Rational(4,7), 5]])
g = L*L.T
E2 = g.inv()[0,0]
J2 = g[1:3,1:3].det()
zero('coarea_E2_detgamma_equals_actual_cut_Gram', E2*g.det()-J2)
bad['wrong_spatial_volume_as_screen_area'] = str(S.factor(g.det()-J2))
assert g.det()-J2 != 0

ph, uu, vv = S.symbols('ph uu vv', real=True)
rho = (2+ph**2)*(3+uu**2+vv**2)
bad['conservation_does_not_force_fixed_product'] = str(S.diff(rho, ph).subs({ph:1,uu:2,vv:3}))
assert S.diff(rho, ph).subs({ph:1,uu:2,vv:3}) != 0

print(json.dumps({'python':platform.python_version(), 'sympy':S.__version__,
                  'checks':checks, 'count':len(checks), 'negative_controls':bad,
                  'scope':'symbolic flat constraint normal-form and nonorthogonal coarea diagnostics; no existence theorem'}, indent=2))
