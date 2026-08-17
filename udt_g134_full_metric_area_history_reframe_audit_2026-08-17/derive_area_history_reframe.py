#!/usr/bin/env python3
"""Exact symbolic checks for the preregistered G134 area-history audit."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


PAIR_BASIS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
OUT = Path(__file__).with_name("DERIVATION_RESULT.json")


def area_matrix(g: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [
            [g[i, k] * g[j, l] - g[i, l] * g[j, k] for k, l in PAIR_BASIS]
            for i, j in PAIR_BASIS
        ]
    )


def record(checks: dict[str, bool], name: str, value: object) -> None:
    checks[name] = bool(value)


def main() -> None:
    names = ("g00", "g01", "g02", "g03", "g11", "g12", "g13", "g22", "g23", "g33")
    values = sp.symbols(" ".join(names), real=True)
    g00, g01, g02, g03, g11, g12, g13, g22, g23, g33 = values
    g = sp.Matrix(
        [
            [g00, g01, g02, g03],
            [g01, g11, g12, g13],
            [g02, g12, g22, g23],
            [g03, g13, g23, g33],
        ]
    )
    area = area_matrix(g)
    area_components = [area[i, j] for i in range(6) for j in range(i, 6)]
    jac = sp.Matrix(area_components).jacobian(values)

    eta = sp.diag(-1, 1, 1, 1)
    eta_subs = {values[i]: eta[a, b] for i, (a, b) in enumerate(
        ((0, 0), (0, 1), (0, 2), (0, 3), (1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3))
    )}
    jac_eta = jac.subs(eta_subs)

    L = sp.Matrix(
        [
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [2, -1, 1, 0],
            [1, 2, 1, 1],
        ]
    )
    g_generic = L.T * eta * L
    generic_subs = {values[i]: g_generic[a, b] for i, (a, b) in enumerate(
        ((0, 0), (0, 1), (0, 2), (0, 3), (1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3))
    )}
    jac_generic = jac.subs(generic_subs)

    checks: dict[str, bool] = {}
    record(checks, "area_matrix_is_symmetric", area == area.T)
    record(checks, "area_map_has_21_output_components", len(area_components) == 21)
    record(checks, "area_jacobian_has_10_inputs", jac.shape == (21, 10))
    record(checks, "area_jacobian_rank_eta_is_10", jac_eta.rank() == 10)
    record(checks, "area_jacobian_cokernel_eta_is_11", len(jac_eta.T.nullspace()) == 11)
    record(checks, "area_jacobian_rank_generic_is_10", jac_generic.rank() == 10)

    area_eta = area_matrix(eta)
    area_generic = area_matrix(g_generic)
    record(checks, "eta_area_nondegenerate", area_eta.det() != 0)
    record(checks, "generic_area_nondegenerate", area_generic.det() != 0)
    record(checks, "eta_area_determinant_identity", area_eta.det() == eta.det() ** 3)
    record(checks, "generic_area_determinant_identity", area_generic.det() == g_generic.det() ** 3)

    c = sp.symbols("c", nonzero=True, real=True)
    conformal_residual = (area_matrix(c * g) - c**2 * area).applyfunc(sp.simplify)
    record(checks, "conformal_weight_is_two_in_metric_multiplier", conformal_residual == sp.zeros(6))
    record(checks, "sign_flip_is_global_algebraic_kernel", area_matrix(-g_generic) == area_generic)
    record(checks, "nonunit_scale_is_detected", area_matrix(2 * g_generic) != area_generic)

    a = sp.symbols("a", positive=True)
    K = sp.Matrix([[0, 1], [1, 0]])
    D = sp.diag(a, 1 / a)
    U = sp.Matrix([[1, 1], [0, 1]])
    record(checks, "reciprocal_D_preserves_K", sp.simplify(D.T * K * D - K) == sp.zeros(2))
    record(checks, "reciprocal_D_preserves_area_line", sp.simplify(D.det()) == 1)
    record(checks, "unipotent_also_preserves_area_line", U.det() == 1)
    record(checks, "area_line_does_not_select_reciprocity", U.T * K * U != K)

    q = sp.Rational
    g_plus = sp.Matrix(
        [[-1, q(1, 2), 0, 0], [q(1, 2), 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    )
    g_minus = sp.Matrix(
        [[-1, -q(1, 2), 0, 0], [-q(1, 2), 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    )
    area_plus = area_matrix(g_plus)
    area_minus = area_matrix(g_minus)
    diag_plus = [area_plus[i, i] for i in range(6)]
    diag_minus = [area_minus[i, i] for i in range(6)]
    record(checks, "plane_self_areas_can_match_for_distinct_labelled_metrics", diag_plus == diag_minus)
    record(checks, "cross_plane_area_resolves_self_area_ambiguity", area_plus[1, 3] == q(1, 2) and area_minus[1, 3] == -q(1, 2))
    record(checks, "full_area_matrices_distinguish_witness", area_plus != area_minus)

    s1, s2 = q(1, 4), q(4, 1)
    spherical_1 = sp.diag(-s1, 1 / s1, 1, 1)
    spherical_2 = sp.diag(-s2, 1 / s2, 1, 1)
    record(checks, "spherical_histories_share_reciprocal_base_area", spherical_1[:2, :2].det() == -1 and spherical_2[:2, :2].det() == -1)
    record(checks, "spherical_histories_have_distinct_full_area", area_matrix(spherical_1) != area_matrix(spherical_2))
    curvature_1 = 2 * (1 - s1)
    curvature_2 = 2 * (1 - s2)
    record(checks, "banked_spherical_histories_are_curvature_distinct", curvature_1 == q(3, 2) and curvature_2 == -6)

    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "check_count": len(checks),
        "passed": sum(checks.values()),
        "area_map_input_dimension": 10,
        "area_map_output_dimension": 21,
        "jacobian_rank_eta": jac_eta.rank(),
        "jacobian_rank_generic": jac_generic.rank(),
        "local_metric_induced_codimension": 21 - jac_eta.rank(),
        "eta_left_nullspace_dimension": len(jac_eta.T.nullspace()),
        "generic_metric": [[int(x) for x in row] for row in g_generic.tolist()],
        "history_witness_curvatures_at_areal_r_1": [str(curvature_1), str(curvature_2)],
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"{result['status']}: {result['passed']}/{result['check_count']} exact G134 production checks")


if __name__ == "__main__":
    main()
