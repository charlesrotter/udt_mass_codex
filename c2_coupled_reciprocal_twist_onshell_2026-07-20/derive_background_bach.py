#!/usr/bin/env python3
"""Exact full Bach tensor for the twist-free reciprocal background."""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
r = sp.symbols("r", real=True)
p = sp.Function("p")(r)
eta = sp.Function("eta")(r)
DIM = 4
RADIAL = 1


def dr(expression, order=1):
    return sp.diff(expression, r, order)


def coordinate_derivative(expression, coordinate):
    return dr(expression) if coordinate == RADIAL else sp.S.Zero


def metric():
    return sp.diag(-sp.exp(-2 * p), sp.exp(2 * p), 1, 1)


def curvature():
    g = metric()
    inverse = sp.simplify(g.inv())
    determinant = sp.simplify(g.det())
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
    scalar = sp.factor(sum(inverse[a, b] * ricci[a, b] for a in range(DIM) for b in range(DIM)))
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
                    weyl[a][b][c][d] = sp.factor(rlow[a][b][c][d] - trace + wedge)
    return g, inverse, determinant, gamma, ricci, scalar, weyl


def weyl_squared(inverse, weyl):
    # The background inverse is diagonal, so the full contraction reduces exactly to four sums.
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
    return sp.factor(value)


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
                divergence[a][c][b] = sp.factor(value)

    ricci_up = sp.MutableDenseMatrix(DIM, DIM, [0] * (DIM * DIM))
    for c in range(DIM):
        for d in range(DIM):
            ricci_up[c, d] = sp.simplify(sum(
                inverse[c, a] * inverse[d, b] * ricci[a, b]
                for a in range(DIM) for b in range(DIM)
            ))

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
            bach[a, b] = sp.factor(value)
    return bach


def euler_second_order(lagrangian):
    return sp.factor(
        sp.diff(lagrangian, p)
        - dr(sp.diff(lagrangian, dr(p)))
        + dr(dr(sp.diff(lagrangian, dr(p, 2))))
    )


def boundary_decomposition(lagrangian):
    momentum_two = sp.diff(lagrangian, dr(p, 2))
    momentum_one = sp.diff(lagrangian, dr(p)) - dr(momentum_two)
    variation = (
        sp.diff(lagrangian, p) * eta
        + sp.diff(lagrangian, dr(p)) * dr(eta)
        + momentum_two * dr(eta, 2)
    )
    bulk = euler_second_order(lagrangian) * eta
    current = momentum_one * eta + momentum_two * dr(eta)
    return sp.factor(momentum_one), sp.factor(momentum_two), sp.simplify(variation - bulk - dr(current))


def main():
    g, inverse, determinant, gamma, ricci, scalar, weyl = curvature()
    c2 = weyl_squared(inverse, weyl)
    density = sp.factor(sp.sqrt(-determinant) * c2)
    bach = bach_tensor(inverse, gamma, ricci, weyl)
    raised = sp.simplify(inverse * bach * inverse)
    reduced_euler = euler_second_order(density)
    boundary_p, boundary_p_prime, boundary_check = boundary_decomposition(density)
    metric_projection = sp.factor(sum(
        raised[a, b] * sp.diff(g[a, b], p)
        for a in range(DIM) for b in range(DIM)
    ))
    nonzero = {
        f"B_{a}{b}": str(sp.factor(bach[a, b]))
        for a in range(DIM) for b in range(DIM)
        if bach[a, b] != 0
    }
    trace = sp.factor(sum(inverse[a, b] * bach[a, b] for a in range(DIM) for b in range(DIM)))
    projection_relation = sp.factor(reduced_euler / metric_projection) if metric_projection != 0 else sp.nan
    result = {
        "schema": "udt-c2-coupled-reciprocal-background-bach-1.0",
        "metric": [[str(item) for item in row] for row in g.tolist()],
        "determinant": str(determinant),
        "scalar_curvature": str(scalar),
        "weyl_squared": str(c2),
        "background_density": str(density),
        "bach_nonzero_components": nonzero,
        "bach_trace": str(trace),
        "reduced_p_euler": str(reduced_euler),
        "boundary_delta_p_coefficient": str(boundary_p),
        "boundary_delta_p_prime_coefficient": str(boundary_p_prime),
        "boundary_decomposition_difference": str(boundary_check),
        "full_metric_path_projection": str(metric_projection),
        "reduced_euler_to_projection_ratio": str(projection_relation),
        "checks": {
            "determinant_minus_one": determinant == -1,
            "bach_symmetric": all(sp.simplify(bach[a, b] - bach[b, a]) == 0 for a in range(DIM) for b in range(DIM)),
            "bach_tracefree": trace == 0,
            "boundary_decomposition_exact": boundary_check == 0,
            "reduced_projection_nonzero_identity": metric_projection != 0,
        },
        "compute": {"method": "exact SymPy full coordinate Bach tensor", "cpu_only": True},
    }
    if not all(result["checks"].values()):
        raise AssertionError(result["checks"])
    (HERE / "BACKGROUND_DERIVATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("scalar_curvature", scalar)
    print("background_density", density)
    print("bach_nonzero_components", json.dumps(nonzero, sort_keys=True))
    print("reduced_p_euler", reduced_euler)
    print("boundary_delta_p", boundary_p)
    print("boundary_delta_p_prime", boundary_p_prime)
    print("projection_ratio", projection_relation)
    print("checks", result["checks"])


if __name__ == "__main__":
    main()
