#!/usr/bin/env python3
"""Exact quadratic transverse-twist C2 operator on the intrinsic-curvature product background."""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
r, theta = sp.symbols("r theta", real=True)
epsilon = sp.symbols("epsilon", real=True)
K = sp.symbols("K", real=True)
y = sp.Function("y")(r)
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
        [0, 0, 1 + epsilon**2 * u**2 * F**2, epsilon * u * F**2],
        [0, 0, epsilon * u * F**2, F**2],
    ])


def tensors():
    g = metric()
    inverse = sp.simplify(g.inv())
    determinant = sp.factor(g.det())
    gamma = [[[
        sp.simplify(sum(inverse[a, e] * (
            coordinate_derivative(g[e, c], b)
            + coordinate_derivative(g[e, b], c)
            - coordinate_derivative(g[b, c], e)
        ) for e in range(DIM)) / 2)
        for c in range(DIM)] for b in range(DIM)] for a in range(DIM)]
    rup = [[[[sp.S.Zero for _ in range(DIM)] for _ in range(DIM)] for _ in range(DIM)] for _ in range(DIM)]
    for a in range(DIM):
        for b in range(DIM):
            for c in range(DIM):
                for d in range(DIM):
                    value = coordinate_derivative(gamma[a][b][d], c) - coordinate_derivative(gamma[a][b][c], d)
                    value += sum(
                        gamma[a][e][c] * gamma[e][b][d]
                        - gamma[a][e][d] * gamma[e][b][c]
                        for e in range(DIM)
                    )
                    rup[a][b][c][d] = sp.simplify(value)
    ricci = sp.MutableDenseMatrix(DIM, DIM, [0] * (DIM * DIM))
    for b in range(DIM):
        for d in range(DIM):
            ricci[b, d] = sp.simplify(sum(rup[a][b][a][d] for a in range(DIM)))
    scalar = sp.simplify(sum(inverse[a, b] * ricci[a, b] for a in range(DIM) for b in range(DIM)))
    rlow = [[[[
        sp.simplify(sum(g[a, e] * rup[e][b][c][d] for e in range(DIM)))
        for d in range(DIM)] for c in range(DIM)] for b in range(DIM)] for a in range(DIM)]
    weyl = [[[[sp.S.Zero for _ in range(DIM)] for _ in range(DIM)] for _ in range(DIM)] for _ in range(DIM)]
    for a in range(DIM):
        for b in range(DIM):
            for c in range(DIM):
                for d in range(DIM):
                    trace = (
                        g[a, c] * ricci[b, d] - g[a, d] * ricci[b, c]
                        - g[b, c] * ricci[a, d] + g[b, d] * ricci[a, c]
                    ) / 2
                    wedge = scalar * (g[a, c] * g[b, d] - g[a, d] * g[b, c]) / 6
                    weyl[a][b][c][d] = sp.simplify(rlow[a][b][c][d] - trace + wedge)
    inverse_pairs = [(a, b, inverse[a, b]) for a in range(DIM) for b in range(DIM) if inverse[a, b] != 0]
    nonzero = {
        (a, b, c, d): weyl[a][b][c][d]
        for a in range(DIM) for b in range(DIM) for c in range(DIM) for d in range(DIM)
        if weyl[a][b][c][d] != 0
    }
    c2 = sp.S.Zero
    for a, e, iae in inverse_pairs:
        for b, f, ibf in inverse_pairs:
            for c, gindex, icg in inverse_pairs:
                for d, h, idh in inverse_pairs:
                    left = nonzero.get((a, b, c, d))
                    right = nonzero.get((e, f, gindex, h))
                    if left is not None and right is not None:
                        c2 += iae * ibf * icg * idh * left * right
    return g, inverse, determinant, scalar, sp.simplify(c2)


def euler_second_order(lagrangian):
    return sp.factor(
        sp.diff(lagrangian, u)
        - sp.diff(sp.diff(lagrangian, sp.diff(u, r)), r)
        + sp.diff(sp.diff(lagrangian, sp.diff(u, r, 2)), r, 2)
    )


def boundary_decomposition(lagrangian):
    second = sp.diff(lagrangian, sp.diff(u, r, 2))
    first = sp.diff(lagrangian, sp.diff(u, r)) - sp.diff(second, r)
    variation = (
        sp.diff(lagrangian, u) * eta
        + sp.diff(lagrangian, sp.diff(u, r)) * sp.diff(eta, r)
        + second * sp.diff(eta, r, 2)
    )
    bulk = euler_second_order(lagrangian) * eta
    current = first * eta + second * sp.diff(eta, r)
    return sp.factor(first), sp.factor(second), sp.simplify(variation - bulk - sp.diff(current, r))


def main():
    g, inverse, determinant, scalar, c2 = tensors()
    density_per_transverse_volume = sp.simplify(c2)
    expansion = sp.series(density_per_transverse_volume, epsilon, 0, 3).removeO().expand()
    linear = reduce_constant_curvature(expansion.coeff(epsilon, 1))
    quadratic = reduce_constant_curvature(expansion.coeff(epsilon, 2))
    background = reduce_constant_curvature(expansion.coeff(epsilon, 0))
    jacobi = sp.factor(euler_second_order(quadratic))
    boundary_u, boundary_u_prime, boundary_check = boundary_decomposition(quadratic)
    constant_twist = sp.simplify(quadratic.subs({sp.diff(u, r): 0, sp.diff(u, r, 2): 0}))
    reversal = sp.simplify(
        quadratic.xreplace({u: -u, sp.diff(u, r): -sp.diff(u, r), sp.diff(u, r, 2): -sp.diff(u, r, 2)})
        - quadratic
    )
    flat_expected = y**2 * sp.diff(u, r, 2) ** 2 - sp.Rational(2, 3) * y * sp.diff(y, r, 2) * sp.diff(u, r) ** 2
    flat_difference = sp.simplify(quadratic.subs(K, 0) - flat_expected)
    checks = {
        "determinant": sp.simplify(determinant + F**2) == 0,
        "linear_vanishes": linear == 0,
        "constant_twist_zero": constant_twist == 0,
        "twist_reversal_even": reversal == 0,
        "no_undifferentiated_u": sp.simplify(sp.diff(quadratic, u)) == 0,
        "boundary_decomposition_exact": boundary_check == 0,
        "flat_parent_recovered": flat_difference == 0,
        "angular_dependence_reduced_to_K": "Derivative(F(theta)" not in str(quadratic),
    }
    if not all(checks.values()):
        raise AssertionError(checks)
    result = {
        "schema": "udt-c2-intrinsic-angular-product-twist-1.0",
        "metric": [[str(item) for item in row] for row in g.tolist()],
        "determinant": str(determinant),
        "scalar_curvature": str(reduce_constant_curvature(scalar)),
        "background_density_per_transverse_volume": str(background),
        "density_linear_epsilon": str(linear),
        "density_quadratic_epsilon": str(quadratic),
        "jacobi_operator": str(jacobi),
        "boundary_delta_u_coefficient": str(boundary_u),
        "boundary_delta_u_prime_coefficient": str(boundary_u_prime),
        "boundary_decomposition_difference": str(boundary_check),
        "constant_twist_density": str(constant_twist),
        "reversal_difference": str(reversal),
        "flat_parent_difference": str(flat_difference),
        "checks": checks,
        "compute": {"method": "exact SymPy two-coordinate Weyl-squared twist expansion", "cpu_only": True},
    }
    (HERE / "TWIST_DERIVATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("background_density", background)
    print("quadratic_density", quadratic)
    print("jacobi_operator", jacobi)
    print("boundary_delta_u", boundary_u)
    print("boundary_delta_u_prime", boundary_u_prime)
    print("checks", checks)


if __name__ == "__main__":
    main()
