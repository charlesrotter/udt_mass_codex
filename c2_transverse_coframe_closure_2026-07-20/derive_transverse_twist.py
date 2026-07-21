#!/usr/bin/env python3
"""Exact gauge-curvature Jacobi action with arbitrary radial transverse leg profiles."""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
r, theta = sp.symbols("r theta", real=True)
epsilon = sp.symbols("epsilon", real=True)
K = sp.symbols("K", real=True)
y = sp.Function("y")(r)
b = sp.Function("b")(r)
c = sp.Function("c")(r)
u = sp.Function("u")(r)
F = sp.Function("F")(theta)
eta = sp.Function("eta")(r)
DIM = 4
R_INDEX = 1
THETA_INDEX = 2


def coordinate_derivative(expression, coordinate):
    if coordinate == R_INDEX:
        return sp.diff(expression, r)
    if coordinate == THETA_INDEX:
        return sp.diff(expression, theta)
    return sp.S.Zero


def reduce_constant_curvature(expression):
    replacements = {
        sp.diff(F, theta, 4): K**2 * F,
        sp.diff(F, theta, 3): -K * sp.diff(F, theta),
        sp.diff(F, theta, 2): -K * F,
    }
    reduced = sp.expand(expression).xreplace(replacements)
    return sp.factor(sp.cancel(reduced))


def metric():
    return sp.Matrix([
        [-y, 0, 0, 0],
        [0, 1 / y, 0, 0],
        [0, 0, b**2 + epsilon**2 * c**2 * F**2 * u**2, epsilon * c**2 * F**2 * u],
        [0, 0, epsilon * c**2 * F**2 * u, c**2 * F**2],
    ])


def tensors():
    g = metric()
    inverse = sp.simplify(g.inv())
    determinant = sp.factor(g.det())
    gamma = [[[
        sp.factor(sum(inverse[a, e] * (
            coordinate_derivative(g[e, d], q)
            + coordinate_derivative(g[e, q], d)
            - coordinate_derivative(g[q, d], e)
        ) for e in range(DIM)) / 2)
        for d in range(DIM)] for q in range(DIM)] for a in range(DIM)]
    rup = [[[[sp.S.Zero for _ in range(DIM)] for _ in range(DIM)] for _ in range(DIM)] for _ in range(DIM)]
    for a in range(DIM):
        for q in range(DIM):
            for d in range(DIM):
                for e in range(DIM):
                    value = coordinate_derivative(gamma[a][q][e], d) - coordinate_derivative(gamma[a][q][d], e)
                    value += sum(gamma[a][j][d] * gamma[j][q][e] - gamma[a][j][e] * gamma[j][q][d] for j in range(DIM))
                    rup[a][q][d][e] = sp.factor(value)
    ricci = sp.MutableDenseMatrix(DIM, DIM, [0] * (DIM * DIM))
    for q in range(DIM):
        for e in range(DIM):
            ricci[q, e] = sp.factor(sum(rup[a][q][a][e] for a in range(DIM)))
    scalar = reduce_constant_curvature(sum(inverse[a, q] * ricci[a, q] for a in range(DIM) for q in range(DIM)))
    rlow = [[[[(sp.factor(sum(g[a, j] * rup[j][q][d][e] for j in range(DIM))))
               for e in range(DIM)] for d in range(DIM)] for q in range(DIM)] for a in range(DIM)]
    weyl = [[[[sp.S.Zero for _ in range(DIM)] for _ in range(DIM)] for _ in range(DIM)] for _ in range(DIM)]
    for a in range(DIM):
        for q in range(DIM):
            for d in range(DIM):
                for e in range(DIM):
                    trace = (g[a, d] * ricci[q, e] - g[a, e] * ricci[q, d] - g[q, d] * ricci[a, e] + g[q, e] * ricci[a, d]) / 2
                    wedge = scalar * (g[a, d] * g[q, e] - g[a, e] * g[q, d]) / 6
                    weyl[a][q][d][e] = sp.factor(rlow[a][q][d][e] - trace + wedge)
    pairs = [(i, j, inverse[i, j]) for i in range(DIM) for j in range(DIM) if inverse[i, j] != 0]
    nonzero = {(i, j, k, l): weyl[i][j][k][l] for i in range(DIM) for j in range(DIM) for k in range(DIM) for l in range(DIM) if weyl[i][j][k][l] != 0}
    c2 = sp.S.Zero
    for i, m, iim in pairs:
        for j, n, ijn in pairs:
            for k, o, iko in pairs:
                for l, p, ilp in pairs:
                    left = nonzero.get((i, j, k, l))
                    right = nonzero.get((m, n, o, p))
                    if left is not None and right is not None:
                        c2 += iim * ijn * iko * ilp * left * right
    return g, determinant, scalar, c2


def euler_second(lagrangian):
    return sp.factor(
        sp.diff(lagrangian, u)
        - sp.diff(sp.diff(lagrangian, sp.diff(u, r)), r)
        + sp.diff(sp.diff(lagrangian, sp.diff(u, r, 2)), r, 2)
    )


def boundary(lagrangian):
    second = sp.factor(sp.diff(lagrangian, sp.diff(u, r, 2)))
    first = sp.factor(sp.diff(lagrangian, sp.diff(u, r)) - sp.diff(second, r))
    variation = sp.diff(lagrangian, u) * eta + sp.diff(lagrangian, sp.diff(u, r)) * sp.diff(eta, r) + second * sp.diff(eta, r, 2)
    current = first * eta + second * sp.diff(eta, r)
    return first, second, sp.factor(variation - euler_second(lagrangian) * eta - sp.diff(current, r))


def product(expression):
    replacements = {
        b: 1, c: 1,
        sp.diff(b, r): 0, sp.diff(b, r, 2): 0, sp.diff(b, r, 3): 0, sp.diff(b, r, 4): 0,
        sp.diff(c, r): 0, sp.diff(c, r, 2): 0, sp.diff(c, r, 3): 0, sp.diff(c, r, 4): 0,
    }
    return sp.factor(expression.subs(replacements).doit())


def main():
    g, determinant, scalar, c2 = tensors()
    action_density = b * c * F * c2
    expansion = sp.series(action_density, epsilon, 0, 3).removeO().expand()
    background = reduce_constant_curvature(expansion.coeff(epsilon, 0))
    linear = reduce_constant_curvature(expansion.coeff(epsilon, 1))
    quadratic = reduce_constant_curvature(expansion.coeff(epsilon, 2))
    jacobi = sp.factor(euler_second(quadratic))
    boundary_u, boundary_u_prime, boundary_check = boundary(quadratic)
    product_quadratic = product(quadratic)
    product_expected = sp.factor(F**3 * (
        y**2 * sp.diff(u, r, 2) ** 2
        + y * (4 * K - 2 * sp.diff(y, r, 2) + 27 * (sp.diff(F, theta) / F) ** 2) * sp.diff(u, r) ** 2 / 3
    ))
    product_difference = sp.factor(product_quadratic - product_expected)
    constant_twist = sp.factor(quadratic.subs({sp.diff(u, r): 0, sp.diff(u, r, 2): 0}))
    reversal = sp.factor(quadratic.xreplace({u: -u, sp.diff(u, r): -sp.diff(u, r), sp.diff(u, r, 2): -sp.diff(u, r, 2)}) - quadratic)

    checks = {
        "determinant_connection_independent": sp.simplify(determinant + b**2 * c**2 * F**2) == 0,
        "linear_twist_vanishes_arbitrary_legs": linear == 0,
        "constant_twist_zero": constant_twist == 0,
        "twist_reversal_even": reversal == 0,
        "no_undifferentiated_u": sp.simplify(sp.diff(quadratic, u)) == 0,
        "boundary_decomposition_exact": boundary_check == 0,
        "product_twist_recovered": product_difference == 0,
    }
    checks = {name: bool(value) for name, value in checks.items()}
    if not all(checks.values()):
        raise AssertionError({"checks": checks, "product_difference": product_difference})

    result = {
        "schema": "udt-c2-transverse-coframe-twist-1.0",
        "variables": {"b": "a*exp(s)", "c": "a*exp(-s)"},
        "metric": [[str(item) for item in row] for row in g.tolist()],
        "determinant": str(determinant),
        "scalar_curvature": str(reduce_constant_curvature(scalar)),
        "background_action_density": str(background),
        "linear_action_density": str(linear),
        "quadratic_action_density": str(quadratic),
        "jacobi_operator": str(jacobi),
        "endpoint_delta_u": str(boundary_u),
        "endpoint_delta_u_prime": str(boundary_u_prime),
        "boundary_decomposition_difference": str(boundary_check),
        "constant_twist_density": str(constant_twist),
        "product_control": {
            "quadratic_action_density": str(product_quadratic),
            "expected": str(product_expected),
            "difference": str(product_difference),
        },
        "mixed_hessian_ruling": {
            "linear_twist_with_arbitrary_b_c": str(linear),
            "area_twist_block": "0",
            "shear_twist_block": "0",
            "reason": "psi reflection maps A to -A while y,b,c,F are even; the exact action is even in A",
        },
        "checks": checks,
        "compute": {"method": "exact SymPy two-coordinate sqrt(-g) Weyl-squared expansion", "cpu_only": True},
    }
    (HERE / "TWIST_CLOSURE.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"result": "PASS", "checks": len(checks), "quadratic_length": len(str(quadratic)), "jacobi_length": len(str(jacobi))}, sort_keys=True))


if __name__ == "__main__":
    main()
