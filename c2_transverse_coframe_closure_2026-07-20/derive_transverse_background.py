#!/usr/bin/env python3
"""Exact C2 background action and radial projections for both transverse coframe legs."""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
r, theta = sp.symbols("r theta", real=True)
K = sp.symbols("K", real=True)
y = sp.Function("y")(r)
b = sp.Function("b")(r)  # b=a*exp(s)
c = sp.Function("c")(r)  # c=a*exp(-s)
F = sp.Function("F")(theta)
eta_y = sp.Function("eta_y")(r)
eta_b = sp.Function("eta_b")(r)
eta_c = sp.Function("eta_c")(r)
FIELDS = ((y, eta_y), (b, eta_b), (c, eta_c))
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
    return sp.diag(-y, 1 / y, b**2, c**2 * F**2)


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
    return g, determinant, scalar, reduce_constant_curvature(c2)


def euler_second(lagrangian, field):
    return sp.factor(
        sp.diff(lagrangian, field)
        - sp.diff(sp.diff(lagrangian, sp.diff(field, r)), r)
        + sp.diff(sp.diff(lagrangian, sp.diff(field, r, 2)), r, 2)
    )


def boundary(lagrangian, field):
    second = sp.factor(sp.diff(lagrangian, sp.diff(field, r, 2)))
    first = sp.factor(sp.diff(lagrangian, sp.diff(field, r)) - sp.diff(second, r))
    return first, second


def product(expression):
    replacements = {
        b: 1, c: 1,
        sp.diff(b, r): 0, sp.diff(b, r, 2): 0, sp.diff(b, r, 3): 0, sp.diff(b, r, 4): 0,
        sp.diff(c, r): 0, sp.diff(c, r, 2): 0, sp.diff(c, r, 3): 0, sp.diff(c, r, 4): 0,
    }
    return sp.factor(expression.subs(replacements).doit())


def main():
    g, determinant, scalar, c2 = tensors()
    action_density = sp.factor(b * c * F * c2)
    radial_lagrangian = sp.factor(action_density / F)
    eulers = {str(field): euler_second(radial_lagrangian, field) for field, _ in FIELDS}
    boundaries = {str(field): boundary(radial_lagrangian, field) for field, _ in FIELDS}
    product_eulers = {name: product(value) for name, value in eulers.items()}
    product_boundaries = {name: tuple(product(value) for value in pair) for name, pair in boundaries.items()}

    product_density_expected = (sp.diff(y, r, 2) - 2 * K) ** 2 / 3
    product_density_difference = sp.factor(product(radial_lagrangian) - product_density_expected)
    area_projection = sp.factor(product_eulers[str(b)] + product_eulers[str(c)])
    shear_projection = sp.factor(product_eulers[str(b)] - product_eulers[str(c)])
    y_projection = sp.factor(product_eulers[str(y)])

    full_equation_1 = sp.diff(y, r, 4)
    full_equation_2 = sp.diff(y, r, 2) ** 2 - 2 * sp.diff(y, r) * sp.diff(y, r, 3) - 4 * K**2
    on_full = {
        "y": sp.factor(y_projection.subs(sp.diff(y, r, 4), 0)),
        "area": sp.factor(area_projection.subs(sp.diff(y, r, 4), 0).subs(sp.diff(y, r, 2) ** 2, 2 * sp.diff(y, r) * sp.diff(y, r, 3) + 4 * K**2)),
        "shear": sp.factor(shear_projection.subs(sp.diff(y, r, 4), 0).subs(sp.diff(y, r, 2) ** 2, 2 * sp.diff(y, r) * sp.diff(y, r, 3) + 4 * K**2)),
    }
    shear_obstruction = sp.factor(8 * K * (sp.diff(y, r, 2) - 2 * K) / 3)
    einstein_branch_shear = sp.factor(on_full["shear"].subs({sp.diff(y, r, 2): -2 * K, sp.diff(y, r, 3): 0}))
    conformal_branch_shear = sp.factor(on_full["shear"].subs({sp.diff(y, r, 2): 2 * K, sp.diff(y, r, 3): 0}))
    einstein_full_constraint = sp.factor(full_equation_2.subs({sp.diff(y, r, 2): -2 * K, sp.diff(y, r, 3): 0}))

    checks = {
        "determinant": sp.simplify(determinant + b**2 * c**2 * F**2) == 0,
        "product_density_recovered": product_density_difference == 0,
        "product_y_projection_full_system": on_full["y"] == 0,
        "product_area_projection_full_system": on_full["area"] == 0,
        "product_shear_projection_obstruction_exact": sp.simplify(on_full["shear"] - shear_obstruction) == 0,
        "conformal_branch_radial_shear_zero": conformal_branch_shear == 0,
        "einstein_branch_is_full_bach": einstein_full_constraint == 0,
        "einstein_branch_radial_shear_nonzero": einstein_branch_shear != 0,
    }
    checks = {name: bool(value) for name, value in checks.items()}
    if not all(checks.values()):
        raise AssertionError({"checks": checks, "product_eulers": product_eulers, "on_full": on_full})

    result = {
        "schema": "udt-c2-transverse-coframe-background-1.0",
        "variables": {"b": "a*exp(s)", "c": "a*exp(-s)", "inverse_map": "a=sqrt(b*c), s=log(b/c)/2"},
        "metric": [[str(item) for item in row] for row in g.tolist()],
        "determinant": str(determinant),
        "scalar_curvature": str(scalar),
        "weyl_squared": str(c2),
        "radial_action_density_per_F": str(radial_lagrangian),
        "euler_projections": {name: str(value) for name, value in eulers.items()},
        "endpoint_coefficients": {name: {"delta_field": str(pair[0]), "delta_field_prime": str(pair[1])} for name, pair in boundaries.items()},
        "area_shear_map": {
            "Euler_a": "(b*Euler_b+c*Euler_c)/a",
            "Euler_s": "b*Euler_b-c*Euler_c",
            "endpoint_delta_a_prime": "(b*Q_b+c*Q_c)/a",
            "endpoint_delta_s_prime": "b*Q_b-c*Q_c",
            "endpoint_delta_a": "b*(P_b+Q_b*s_prime)/a+c*(P_c-Q_c*s_prime)/a",
            "endpoint_delta_s": "b*P_b-c*P_c+b_prime*Q_b-c_prime*Q_c",
        },
        "product_control": {
            "radial_density": str(product(radial_lagrangian)),
            "density_difference": str(product_density_difference),
            "Euler_y": str(y_projection),
            "Euler_area": str(area_projection),
            "Euler_shear": str(shear_projection),
            "on_full_bach": {name: str(value) for name, value in on_full.items()},
            "full_system": [str(full_equation_1), str(full_equation_2)],
            "endpoint_coefficients_bc": {name: {"delta_field": str(pair[0]), "delta_field_prime": str(pair[1])} for name, pair in product_boundaries.items()},
        },
        "variation_domain_obstruction": {
            "radial_shear_projection_on_full_bach": str(on_full["shear"]),
            "conformal_branch_y_second": "2*K",
            "conformal_branch_projection": str(conformal_branch_shear),
            "einstein_branch_y_second": "-2*K",
            "einstein_branch_full_constraint": str(einstein_full_constraint),
            "einstein_branch_projection": str(einstein_branch_shear),
            "ruling": "the r-only b/c shear variation with F and angular domain frozen is not an unrestricted compact-support metric variation; it cannot overrule the pointwise full Bach equation",
        },
        "checks": checks,
        "compute": {"method": "exact SymPy two-coordinate Weyl-squared action and second-order radial variations", "cpu_only": True},
    }
    (HERE / "BACKGROUND_CLOSURE.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"result": "PASS", "checks": len(checks), "product_euler": {name: str(value) for name, value in product_eulers.items()}}, sort_keys=True))


if __name__ == "__main__":
    main()
