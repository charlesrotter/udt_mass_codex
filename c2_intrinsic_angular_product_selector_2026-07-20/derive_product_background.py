#!/usr/bin/env python3
"""Exact C2 and full Bach tensor for a reciprocal surface times a constant-curvature screen."""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
r, theta = sp.symbols("r theta", real=True)
K = sp.symbols("K", real=True)
y = sp.Function("y")(r)
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
    return sp.diag(-y, 1 / y, 1, F**2)


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
            ricci[b, d] = reduce_constant_curvature(sum(rup[a][b][a][d] for a in range(DIM)))
    scalar = reduce_constant_curvature(sum(inverse[a, b] * ricci[a, b] for a in range(DIM) for b in range(DIM)))
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
                    weyl[a][b][c][d] = reduce_constant_curvature(rlow[a][b][c][d] - trace + wedge)
    return g, inverse, determinant, gamma, ricci, scalar, weyl


def weyl_squared(inverse, weyl):
    value = sp.S.Zero
    for a in range(DIM):
        for b in range(DIM):
            for c in range(DIM):
                for d in range(DIM):
                    if weyl[a][b][c][d] != 0:
                        value += (
                            inverse[a, a] * inverse[b, b] * inverse[c, c] * inverse[d, d]
                            * weyl[a][b][c][d] ** 2
                        )
    return reduce_constant_curvature(value)


def bach_tensor(inverse, gamma, ricci, weyl):
    divergence = [[[sp.S.Zero for _ in range(DIM)] for _ in range(DIM)] for _ in range(DIM)]
    for a in range(DIM):
        for c in range(DIM):
            for b in range(DIM):
                value = sp.S.Zero
                for d in range(DIM):
                    for e in range(DIM):
                        if inverse[d, e] == 0:
                            continue
                        covariant = coordinate_derivative(weyl[a][c][b][d], e)
                        covariant -= sum(
                            gamma[q][e][a] * weyl[q][c][b][d]
                            + gamma[q][e][c] * weyl[a][q][b][d]
                            + gamma[q][e][b] * weyl[a][c][q][d]
                            + gamma[q][e][d] * weyl[a][c][b][q]
                            for q in range(DIM)
                        )
                        value += inverse[d, e] * covariant
                divergence[a][c][b] = reduce_constant_curvature(value)
    ricci_up = sp.simplify(inverse * ricci * inverse)
    bach = sp.MutableDenseMatrix(DIM, DIM, [0] * (DIM * DIM))
    for a in range(DIM):
        for b in range(DIM):
            value = sp.S.Zero
            for c in range(DIM):
                for f in range(DIM):
                    if inverse[c, f] == 0:
                        continue
                    covariant = coordinate_derivative(divergence[a][c][b], f)
                    covariant -= sum(
                        gamma[q][f][a] * divergence[q][c][b]
                        + gamma[q][f][c] * divergence[a][q][b]
                        + gamma[q][f][b] * divergence[a][c][q]
                        for q in range(DIM)
                    )
                    value += inverse[c, f] * covariant
            value += sum(
                ricci_up[c, d] * weyl[a][c][b][d] / 2
                for c in range(DIM) for d in range(DIM)
            )
            bach[a, b] = reduce_constant_curvature(value)
    return bach


def euler_second_order(lagrangian):
    return sp.factor(
        sp.diff(lagrangian, y)
        - sp.diff(sp.diff(lagrangian, sp.diff(y, r)), r)
        + sp.diff(sp.diff(lagrangian, sp.diff(y, r, 2)), r, 2)
    )


def boundary_decomposition(lagrangian):
    second = sp.diff(lagrangian, sp.diff(y, r, 2))
    first = sp.diff(lagrangian, sp.diff(y, r)) - sp.diff(second, r)
    variation = (
        sp.diff(lagrangian, y) * eta
        + sp.diff(lagrangian, sp.diff(y, r)) * sp.diff(eta, r)
        + second * sp.diff(eta, r, 2)
    )
    bulk = euler_second_order(lagrangian) * eta
    current = first * eta + second * sp.diff(eta, r)
    return sp.factor(first), sp.factor(second), sp.simplify(variation - bulk - sp.diff(current, r))


def main():
    g, inverse, determinant, gamma, ricci, scalar, weyl = tensors()
    c2 = weyl_squared(inverse, weyl)
    # On the registered positive local angular patch sqrt(-det(g))=F(theta).
    density = sp.factor(F * c2)
    density_per_transverse_volume = sp.factor(c2)
    bach = bach_tensor(inverse, gamma, ricci, weyl)
    trace = reduce_constant_curvature(sum(inverse[a, b] * bach[a, b] for a in range(DIM) for b in range(DIM)))
    reduced_euler = euler_second_order(density_per_transverse_volume)
    boundary_y, boundary_y_prime, boundary_check = boundary_decomposition(density_per_transverse_volume)
    nonzero = {
        f"B_{a}{b}": str(reduce_constant_curvature(bach[a, b]))
        for a in range(DIM) for b in range(DIM)
        if reduce_constant_curvature(bach[a, b]) != 0
    }
    checks = {
        "determinant": sp.simplify(determinant + F**2) == 0,
        "bach_symmetric": all(reduce_constant_curvature(bach[a, b] - bach[b, a]) == 0 for a in range(DIM) for b in range(DIM)),
        "bach_tracefree": trace == 0,
        "boundary_decomposition_exact": boundary_check == 0,
        "angular_dependence_reduced_to_K": all("Derivative(F(theta)" not in value for value in nonzero.values()),
    }
    if not all(checks.values()):
        raise AssertionError(checks)
    result = {
        "schema": "udt-c2-intrinsic-angular-product-background-1.0",
        "metric": [[str(item) for item in row] for row in g.tolist()],
        "constant_curvature_identity": "Derivative(F(theta),(theta,2))=-K*F(theta)",
        "determinant": str(determinant),
        "scalar_curvature": str(scalar),
        "weyl_squared": str(c2),
        "density": str(density),
        "density_per_transverse_volume": str(density_per_transverse_volume),
        "bach_nonzero_components": nonzero,
        "bach_trace": str(trace),
        "reduced_y_euler": str(reduced_euler),
        "boundary_delta_y_coefficient": str(boundary_y),
        "boundary_delta_y_prime_coefficient": str(boundary_y_prime),
        "boundary_decomposition_difference": str(boundary_check),
        "checks": checks,
        "compute": {"method": "exact SymPy two-coordinate full Bach tensor", "cpu_only": True},
    }
    (HERE / "BACKGROUND_DERIVATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("scalar_curvature", scalar)
    print("weyl_squared", c2)
    print("bach_nonzero_components", json.dumps(nonzero, sort_keys=True))
    print("reduced_y_euler", reduced_euler)
    print("boundary_delta_y", boundary_y)
    print("boundary_delta_y_prime", boundary_y_prime)
    print("checks", checks)


if __name__ == "__main__":
    main()
