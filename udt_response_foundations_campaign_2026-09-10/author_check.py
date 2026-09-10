"""Exact RF1 diagnostics; no physical law or solution family is assumed.

Frozen after the analytical candidate, before executing these checks.
Full algebraic curvature basis, normal-condition rank, actual polynomial metric,
and an independently integrated warped-metric Jacobi field. No reviewer imports.
"""
import itertools as it
import json
import platform

import sympy as s

I = range(4)
quadruples = list(it.product(I, repeat=4))
pairs = list(it.combinations(I, 2))
upper = list(it.combinations_with_replacement(range(6), 2))
free = [ij for ij in upper if ij != (0, 5)]
checks = []


def gate(name, condition):
    assert condition, name
    checks.append(name)


def curvature_basis(index):
    c = s.zeros(6)
    a, b = free[index]
    c[a, b] = c[b, a] = 1
    c[0, 5] = c[5, 0] = c[1, 4] - c[2, 3]

    def component(a, b, c1, d):
        if a == b or c1 == d:
            return s.S.Zero
        sign = (1 if a < b else -1) * (1 if c1 < d else -1)
        return sign * c[pairs.index(tuple(sorted((a, b)))),
                        pairs.index(tuple(sorted((c1, d))))]

    return {q: component(*q) for q in quadruples}


basis = [curvature_basis(i) for i in range(20)]
basis_nonzero = []
for n, r in enumerate(basis):
    gate('curvature_symmetries_bianchi_' + str(n), all(
        r[a, b, c, d] == -r[b, a, c, d]
        and r[a, b, c, d] == -r[a, b, d, c]
        and r[a, b, c, d] == r[c, d, a, b]
        and r[a, b, c, d] + r[a, c, d, b] + r[a, d, b, c] == 0
        for a, b, c, d in quadruples))
    h = {(i, j, k, l): -(r[i, k, j, l] + r[i, l, j, k]) / 3
         for i, j, k, l in quadruples}
    gate('normal_polarization_' + str(n), all(
        h[i, j, k, l] + h[i, k, j, l] + h[i, l, j, k] == 0
        for i, j, k, l in quadruples))
    rebuilt = {(a, b, c, d): (h[a, d, b, c] + h[b, c, a, d]
                              - h[a, c, b, d] - h[b, d, a, c]) / 2
               for a, b, c, d in quadruples}
    gate('full_curvature_round_trip_' + str(n), rebuilt == r)
    basis_nonzero.append(sum(v != 0 for v in r.values()))

# The normal condition acts on Sym2(V*) tensor Sym2(V*) (100 coordinates).
sympairs = list(it.combinations_with_replacement(I, 2))
columns = [(a, b) for a in sympairs for b in sympairs]
column_index = {v: n for n, v in enumerate(columns)}
rows = []
for i in I:
    for j, k, l in it.combinations_with_replacement(I, 3):
        row = [0] * len(columns)
        for a, b, c, d in ((i, j, k, l), (i, k, j, l), (i, l, j, k)):
            key = (tuple(sorted((a, b))), tuple(sorted((c, d))))
            row[column_index[key]] += 1
        rows.append(row)
normal_rank = s.Matrix(rows).rank()
gate('normal_condition_rank_80_nullity_20', normal_rank == 80)

x = s.symbols('x0:4')
eta = s.diag(-1, 1, 1, 1)
zero = dict.fromkeys(x, 0)


def h2_of(r):
    return s.Matrix(4, 4, lambda i, j:
        s.expand(-sum(r[i, a, j, b] * x[a] * x[b] for a in I for b in I) / 3))


r = {q: sum((n + 1) * b[q] for n, b in enumerate(basis)) for q in quadruples}
h2 = h2_of(r)
h3 = (x[0] + 2*x[1] - x[2])*h2
h4 = (x[0]**2 + x[1]*x[2])*h2 + (x[2]**2 - 2*x[3]**2)*h2_of(basis[7])
g = (eta + h2 + h3 + h4).applyfunc(s.expand)
radial = (g*s.Matrix(x) - eta*s.Matrix(x)).applyfunc(s.expand)
gate('full_untruncated_radial_polynomial', radial == s.zeros(4, 1))
gate('polynomial_metric_origin_eta', g.subs(zero) == eta)
gate('polynomial_metric_first_derivatives_zero', all(
    s.diff(g[i, j], x[k]).subs(zero) == 0 for i, j, k in it.product(I, repeat=3)))
christoffel_ray = []
for i in I:
    expr = sum((s.diff(g[i, k], x[j]) + s.diff(g[i, j], x[k])
                - s.diff(g[j, k], x[i]))*x[j]*x[k]/2 for j in I for k in I)
    christoffel_ray.append(s.expand(expr))
gate('first_kind_christoffel_radial_zero', all(v == 0 for v in christoffel_ray))
direct_r = {(a, b, c, d): (
    s.diff(g[a, d], x[b], x[c]) + s.diff(g[b, c], x[a], x[d])
    - s.diff(g[a, c], x[b], x[d]) - s.diff(g[b, d], x[a], x[c])
    ).subs(zero) / 2 for a, b, c, d in quadruples}
gate('actual_polynomial_origin_curvature', direct_r == r)

# A different calculation from the candidate's coefficient recurrence:
# k=-dt^2+du^2+A(u)^2dy^2+dz^2, with A(0)=1. Along the u-geodesic,
# K=-A''/A and J=A integral(1/A^2), J(0)=0, J'(0)=1 solve Jacobi exactly.
# The transverse normal metric component is (J/u)^2.
u = s.Symbol('u')
A = 1 + s.Rational(2, 5)*u + s.Rational(3, 7)*u**2 + s.Rational(5, 11)*u**3 + s.Rational(7, 13)*u**4
inv_square = s.series(A**(-2), u, 0, 5).removeO()
integral = s.integrate(inv_square, u)
J = s.series(A*integral, u, 0, 6).removeO()
transverse = s.series((J/u)**2, u, 0, 5).removeO().expand()
K = -s.diff(A, u, 2)/A
kj = [s.diff(K, u, j).subs(u, 0) for j in range(3)]
actual = [transverse.coeff(u, n) for n in (2, 3, 4)]
expected = [-kj[0]/3, -kj[1]/6, 2*kj[0]**2/45-kj[2]/20]
gate('warped_metric_exact_integral_matches_orders_2_3_4', actual == expected)
gate('warped_metric_nonzero_curvature_and_first_two_derivatives', all(v != 0 for v in kj))
gate('warped_metric_wrong_quartic_without_R_squared_rejected', actual[2] != -kj[2]/20)

print(json.dumps(dict(
    python=platform.python_version(), sympy=s.__version__, arithmetic='exact rational/symbolic',
    assertion_categories=len(checks), checks=checks,
    curvature_basis_count=20, curvature_components_per_basis=256,
    nonzero_components_per_basis=basis_nonzero,
    normal_constraint_shape=[len(rows), len(columns)], normal_constraint_rank=normal_rank,
    warped_curvature_derivatives=list(map(str, kj)),
    warped_normal_coefficients=list(map(str, actual)),
    scope='Basis and rank certify the finite linear map; examples check implementation. All-order response estimate requires analytical proof and declared hypotheses.',
    limitations='Structural zeros are not independent evidence. No development, response selection or empirical GR claim.'
), indent=2, sort_keys=True))
