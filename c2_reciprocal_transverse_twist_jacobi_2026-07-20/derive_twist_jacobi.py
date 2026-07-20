#!/usr/bin/env python3
"""Exact coordinate-tensor derivation for the preregistered reciprocal/twist coframe."""
from __future__ import annotations

import json
from pathlib import Path
import sympy as sp

HERE = Path(__file__).resolve().parent
r = sp.symbols("r", real=True)
epsilon = sp.symbols("epsilon", real=True)
p = sp.Function("p")(r)
u = sp.Function("u")(r)
DIM = 4
RADIAL = 1


def dr(expression, order=1):
    return sp.diff(expression, r, order)


def coordinate_derivative(expression, coordinate):
    return dr(expression) if coordinate == RADIAL else sp.S.Zero


def metric():
    # PINNED_BY_THEORY/CONDITIONAL: Lorentzian reciprocal clock/parallel block.
    # FREE_AND_VARIED: full epsilon^2 backreaction from e3=dy+epsilon*u*dx is retained.
    return sp.Matrix([
        [-sp.exp(-2 * p), 0, 0, 0],
        [0, sp.exp(2 * p), 0, 0],
        [0, 0, 1 + epsilon**2 * u**2, epsilon * u],
        [0, 0, epsilon * u, 1],
    ])


def tensors():
    g = metric()
    inverse = sp.simplify(g.inv())
    determinant = sp.simplify(g.det())
    gamma = [[[
        sp.simplify(sum(inverse[a, d] * (
            coordinate_derivative(g[d, c], b)
            + coordinate_derivative(g[d, b], c)
            - coordinate_derivative(g[b, c], d)
        ) for d in range(DIM)) / 2)
        for c in range(DIM)] for b in range(DIM)] for a in range(DIM)]
    rup = [[[[sp.S.Zero for _ in range(DIM)] for _ in range(DIM)] for _ in range(DIM)] for _ in range(DIM)]
    for a in range(DIM):
        for b in range(DIM):
            for c in range(DIM):
                for d in range(DIM):
                    value = coordinate_derivative(gamma[a][b][d], c) - coordinate_derivative(gamma[a][b][c], d)
                    value += sum(gamma[a][e][c] * gamma[e][b][d] - gamma[a][e][d] * gamma[e][b][c] for e in range(DIM))
                    rup[a][b][c][d] = sp.simplify(value)
    ricci = sp.MutableDenseMatrix(DIM, DIM, [0] * (DIM * DIM))
    for b in range(DIM):
        for d in range(DIM):
            ricci[b, d] = sp.simplify(sum(rup[a][b][a][d] for a in range(DIM)))
    scalar = sp.simplify(sum(inverse[a, b] * ricci[a, b] for a in range(DIM) for b in range(DIM)))
    rlow = [[[[sp.simplify(sum(g[a, e] * rup[e][b][c][d] for e in range(DIM)))
               for d in range(DIM)] for c in range(DIM)] for b in range(DIM)] for a in range(DIM)]
    weyl = [[[[sp.S.Zero for _ in range(DIM)] for _ in range(DIM)] for _ in range(DIM)] for _ in range(DIM)]
    for a in range(DIM):
        for b in range(DIM):
            for c in range(DIM):
                for d in range(DIM):
                    trace = (g[a, c] * ricci[b, d] - g[a, d] * ricci[b, c]
                             - g[b, c] * ricci[a, d] + g[b, d] * ricci[a, c]) / 2
                    wedge = scalar * (g[a, c] * g[b, d] - g[a, d] * g[b, c]) / 6
                    weyl[a][b][c][d] = sp.simplify(rlow[a][b][c][d] - trace + wedge)
    # Contract only nonzero covariant Weyl entries and nonzero inverse-metric entries.
    inverse_pairs = [(a, b, inverse[a, b]) for a in range(DIM) for b in range(DIM) if inverse[a, b] != 0]
    nonzero = {(a, b, c, d): weyl[a][b][c][d]
               for a in range(DIM) for b in range(DIM) for c in range(DIM) for d in range(DIM)
               if weyl[a][b][c][d] != 0}
    c2 = sp.S.Zero
    for a, e, iae in inverse_pairs:
        for b, f, ibf in inverse_pairs:
            for c, gindex, icg in inverse_pairs:
                for d, h, idh in inverse_pairs:
                    left = nonzero.get((a, b, c, d))
                    right = nonzero.get((e, f, gindex, h))
                    if left is not None and right is not None:
                        c2 += iae * ibf * icg * idh * left * right
    return g, inverse, determinant, gamma, rup, ricci, scalar, sp.simplify(c2)


def replace_jets(expression):
    symbols = sp.symbols("p0 p1 p2 p3 p4 u0 u1 u2 u3 u4", real=True)
    p0, p1, p2, p3, p4, u0, u1, u2, u3, u4 = symbols
    replacements = {
        p: p0, dr(p): p1, dr(p, 2): p2, dr(p, 3): p3, dr(p, 4): p4,
        u: u0, dr(u): u1, dr(u, 2): u2, dr(u, 3): u3, dr(u, 4): u4,
    }
    return sp.simplify(expression.xreplace(replacements)), symbols


def euler_lagrange_second_order(lagrangian):
    return sp.simplify(sp.diff(lagrangian, u) - dr(sp.diff(lagrangian, dr(u))) + dr(dr(sp.diff(lagrangian, dr(u, 2)))))


def main():
    g, inverse, determinant, gamma, rup, ricci, scalar, c2 = tensors()
    density = sp.simplify(sp.sqrt(-determinant) * c2)
    expansion = sp.series(density, epsilon, 0, 3).removeO().expand()
    linear = sp.simplify(expansion.coeff(epsilon, 1))
    quadratic = sp.factor(sp.simplify(expansion.coeff(epsilon, 2)))
    jacobi = sp.factor(euler_lagrange_second_order(quadratic))
    constant_twist = sp.simplify(quadratic.subs({dr(u): 0, dr(u, 2): 0}))
    reversal = sp.simplify(quadratic.xreplace({u: -u, dr(u): -dr(u), dr(u, 2): -dr(u, 2)}) - quadratic)
    flat = sp.simplify(quadratic.subs({dr(p): 0, dr(p, 2): 0}))
    qjets, symbols = replace_jets(quadratic)
    jjets, _ = replace_jets(jacobi)
    result = {
        "schema": "udt-c2-reciprocal-transverse-twist-jacobi-1.0",
        "metric": [[str(item) for item in row] for row in g.tolist()],
        "inverse": [[str(item) for item in row] for row in inverse.tolist()],
        "determinant": str(determinant),
        "scalar_curvature": str(sp.factor(scalar)),
        "density_linear_epsilon": str(linear),
        "density_quadratic_epsilon": str(quadratic),
        "density_quadratic_jets": str(qjets),
        "jacobi_operator": str(jacobi),
        "jacobi_operator_jets": str(jjets),
        "jet_symbol_order": [str(item) for item in symbols],
        "constant_twist_density": str(constant_twist),
        "reversal_difference": str(reversal),
        "flat_profile_quadratic_density": str(sp.factor(flat)),
        "checks": {
            "determinant_minus_one": determinant == -1,
            "linear_vanishes": linear == 0,
            "constant_twist_zero": constant_twist == 0,
            "twist_reversal_even": reversal == 0,
            # Derivative(u(r),r) structurally contains u(r), so ``has(u)`` is too broad.
            "no_undifferentiated_u": sp.simplify(sp.diff(quadratic, u)) == 0,
        },
        "compute": {"method": "exact SymPy coordinate tensor", "cpu_only": True},
    }
    if not all(result["checks"].values()):
        raise AssertionError(result["checks"])
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("determinant", determinant)
    print("scalar_curvature", sp.factor(scalar))
    print("quadratic_density", quadratic)
    print("jacobi_operator", jacobi)
    print("flat_profile_quadratic_density", sp.factor(flat))
    print("checks", result["checks"])


if __name__ == "__main__":
    main()
