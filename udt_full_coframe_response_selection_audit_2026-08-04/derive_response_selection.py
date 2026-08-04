#!/usr/bin/env python3
"""Exact algebra for the bounded full-coframe response-selection audit."""

from __future__ import annotations

import json

import sympy as sp


def coefficient_row(expression: sp.Expr, variables: list[sp.Symbol]) -> list[sp.Expr]:
    return [sp.expand(expression).coeff(variable) for variable in variables]


def symmetric_matrix(prefix: str) -> tuple[sp.Matrix, list[sp.Symbol]]:
    names = [f"{prefix}{i}{j}" for i in range(4) for j in range(i, 4)]
    variables = list(sp.symbols(" ".join(names), real=True))
    matrix = sp.zeros(4)
    cursor = 0
    for i in range(4):
        for j in range(i, 4):
            matrix[i, j] = variables[cursor]
            matrix[j, i] = variables[cursor]
            cursor += 1
    return matrix, variables


def main() -> None:
    checks: list[tuple[str, bool]] = []

    def check(name: str, condition: bool) -> None:
        checks.append((name, bool(condition)))

    eta = sp.diag(-1, 1, 1, 1)
    H = sp.diag(-1, 1, 0, 0)
    T_H = H.T * eta + eta * H
    check("founded_generator_trace_zero", sp.trace(H) == 0)
    check("founded_metric_tangent", T_H == sp.diag(2, 2, 0, 0))
    check("founded_volume_tangent_zero", sp.trace(eta * T_H) / 2 == 0)
    check("anisotropic_response_sees_founded_tangent", sp.trace(sp.diag(1, 0, 0, 0) * T_H) == 2)

    # The full coframe-to-metric tangent map has rank ten and a six-dimensional Lorentz kernel.
    xvars = list(sp.symbols("x0:16", real=True))
    X = sp.Matrix(4, 4, xvars)
    T = X.T * eta + eta * X
    t_components = [T[i, j] for i in range(4) for j in range(i, 4)]
    tangent_map = sp.Matrix([coefficient_row(item, xvars) for item in t_components])
    check("coframe_metric_tangent_rank_ten", tangent_map.rank() == 10)
    check("coframe_metric_tangent_kernel_six", len(tangent_map.nullspace()) == 6)

    signs = [-1, 1, 1, 1]
    lorentz_generators: list[sp.Matrix] = []
    for i in range(4):
        for j in range(i + 1, 4):
            L = sp.zeros(4)
            L[i, j] = 1
            L[j, i] = -sp.Rational(signs[i], signs[j])
            lorentz_generators.append(L)
            check(f"lorentz_generator_{i}{j}_in_kernel", L.T * eta + eta * L == sp.zeros(4))
    lorentz_flat = sp.Matrix.hstack(*[sp.Matrix(L).reshape(16, 1) for L in lorentz_generators])
    check("lorentz_kernel_rank_six", lorentz_flat.rank() == 6)

    # Every symmetric metric response pulls back injectively to a coframe covector and automatically
    # annihilates local Lorentz gauge directions. The full coframe therefore retains, rather than
    # selects among, inequivalent metric responses.
    E, evars = symmetric_matrix("e")
    pairing = sp.expand(sum(E[i, j] * T[i, j] for i in range(4) for j in range(4)) / 2)
    pullback_components = [sp.diff(pairing, variable) for variable in xvars]
    pullback_map = sp.Matrix([coefficient_row(item, evars) for item in pullback_components])
    check("metric_response_pullback_injective", pullback_map.rank() == 10)
    for index, L in enumerate(lorentz_generators):
        gauge_sub = {xvars[4 * i + j]: L[i, j] for i in range(4) for j in range(4)}
        check(f"response_annihilates_lorentz_{index}", sp.expand(pairing.subs(gauge_sub)) == 0)

    # Exact constant-curvature f(R) controls in four dimensions, using inverse-metric variation:
    # E_mn = f'(R) R_mn - 1/2 f(R) g_mn when R is constant and R_mn=(R/4)g_mn.
    R = sp.symbols("R", real=True)
    fr_coefficients: dict[str, str] = {}
    for n in range(7):
        f = R**n
        coeff = sp.factor(R * sp.diff(f, R) / 4 - f / 2)
        expected = sp.factor(sp.Rational(n - 2, 4) * R**n)
        check(f"fR_power_{n}_constant_curvature", sp.simplify(coeff - expected) == 0)
        fr_coefficients[str(n)] = str(coeff)
    check("EH_nonzero_on_R12", sp.Rational(-1, 4) * 12 == -3)
    check("R2_stationary_on_constant_curvature", sp.Rational(2 - 2, 4) * 12**2 == 0)
    response_vectors = sp.Matrix(
        [
            [sp.Rational(1 - 2, 4) * 4, sp.Rational(1 - 2, 4) * 12],
            [sp.Rational(3 - 2, 4) * 4**3, sp.Rational(3 - 2, 4) * 12**3],
        ]
    )
    check("distinct_fR_response_shapes", response_vectors.det() != 0)

    # c and G cannot alone manufacture an inverse-length-squared coefficient. This does not select
    # a law; it only keeps a cosmological/curvature scale open.
    dimension_matrix = sp.Matrix([[1, 3], [0, -1], [-1, -2]])
    dimension_target = sp.Matrix([-2, 0, 0])
    check("cG_no_inverse_length_squared_monomial", dimension_matrix.rank() < dimension_matrix.row_join(dimension_target).rank())

    # Reproduce the registered all-query rank-nine control with rational normalized pairs.
    S, svars = symmetric_matrix("s")
    e = [sp.eye(4)[:, i] for i in range(4)]
    pairs: list[tuple[sp.Matrix, sp.Matrix]] = []
    for i in (1, 2, 3):
        pairs.append((e[0], e[i]))
    pairs.extend(
        [
            (e[0], (3 * e[1] + 4 * e[2]) / 5),
            (e[0], (3 * e[1] + 4 * e[3]) / 5),
            (e[0], (3 * e[2] + 4 * e[3]) / 5),
            (sp.Rational(5, 3) * e[0] + sp.Rational(4, 3) * e[1], e[2]),
            (sp.Rational(5, 3) * e[0] + sp.Rational(4, 3) * e[2], e[3]),
            (sp.Rational(5, 3) * e[0] + sp.Rational(4, 3) * e[3], e[1]),
        ]
    )
    residuals: list[sp.Expr] = []
    for index, (u, n) in enumerate(pairs):
        check(f"query_{index}_unit_timelike", sp.simplify((u.T * eta * u)[0]) == -1)
        check(f"query_{index}_unit_spacelike", sp.simplify((n.T * eta * n)[0]) == 1)
        check(f"query_{index}_orthogonal", sp.simplify((u.T * eta * n)[0]) == 0)
        residuals.append(sp.expand((u.T * S * u)[0] + (n.T * S * n)[0]))
    query_matrix = sp.Matrix([coefficient_row(item, svars) for item in residuals])
    query_kernel = query_matrix.nullspace()
    metric_line = sp.Matrix([1, 0, 0, 0, -1, 0, 0, -1, 0, -1])
    check("universal_query_rank_nine", query_matrix.rank() == 9)
    check("universal_query_kernel_one", len(query_kernel) == 1)
    check("universal_query_metric_line_invisible", query_matrix * metric_line == sp.zeros(9, 1))

    # Founded endpoint composition is an identity for every supplied potential and hence cannot
    # distinguish any of the response families above.
    p0, p1, p2 = sp.symbols("p0 p1 p2", real=True)
    composition_residual = sp.expand((p2 - p0) - (p2 - p1) - (p1 - p0))
    check("endpoint_composition_identity", composition_residual == 0)
    check("endpoint_composition_zero_jacobian", sp.Matrix([composition_residual]).jacobian([p0, p1, p2]) == sp.zeros(1, 3))

    failed = [name for name, passed in checks if not passed]
    result = {
        "status": "PASS" if not failed else "FAIL",
        "checks": len(checks),
        "failed": failed,
        "sympy_version": sp.__version__,
        "coframe_metric_tangent_rank": tangent_map.rank(),
        "coframe_gauge_kernel_dimension": len(tangent_map.nullspace()),
        "metric_response_pullback_rank": pullback_map.rank(),
        "founded_volume_direction_response": str(sp.trace(eta * T_H) / 2),
        "founded_anisotropic_direction_response": str(sp.trace(sp.diag(1, 0, 0, 0) * T_H)),
        "constant_curvature_fR_coefficients_n0_to_n6": fr_coefficients,
        "fR_shape_control_determinant": str(response_vectors.det()),
        "cG_curvature_scale_coefficient_rank": dimension_matrix.rank(),
        "cG_curvature_scale_augmented_rank": dimension_matrix.row_join(dimension_target).rank(),
        "universal_query_rank": query_matrix.rank(),
        "universal_query_nullity": 10 - query_matrix.rank(),
        "maximum_conclusion": "EXACT_ALGEBRA_CONTROLS_ONLY__SELECTION_REQUIRES_SOURCE_ADJUDICATION",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if not failed else 1)


if __name__ == "__main__":
    main()
