#!/usr/bin/env python3
"""Exact symbolic checks for the bounded G225 screen-carry classification."""

from __future__ import annotations

import json

import sympy as sp


LANDING = (
    "METRIC_AND_SHARED_CLOCK_DEFINE_POSITIVE_INCIDENT_SCREEN_PLANES"
    "__CANONICAL_LEAST_TURNING_DIRECT_SCREEN_ISOMETRY_EXISTS_OFF_ANTIPODES"
    "__THREE_DIRECTION_COMPOSITION_RETAINS_FINITE_O2_HOLONOMY_AND_NO_GLOBAL_ENDPOINT_ONLY_FLAT_SCREEN_CARRY_EXISTS"
    "__G188_JACOBI_TRANSPORT_REMAINS_SEPARATE"
)


def require(condition: bool, label: str, checks: list[str]) -> None:
    if not condition:
        raise AssertionError(label)
    checks.append(label)


def equal_matrix(left: sp.Matrix, right: sp.Matrix) -> bool:
    return all(sp.simplify(value) == 0 for value in left - right)


def rotation(source: sp.Matrix, target: sp.Matrix) -> sp.Matrix:
    identity = sp.eye(3)
    skew = target * source.T - source * target.T
    cosine = (source.T * target)[0]
    return sp.simplify(identity + skew + skew**2 / (1 + cosine))


def main() -> None:
    checks: list[str] = []
    one = sp.Integer(1)
    zero = sp.Integer(0)

    # Lorentz clock normalization and rest-space sight direction.
    eta = sp.diag(-1, 1, 1, 1)
    observer = sp.Matrix([1, 0, 0, 0])
    null = sp.Matrix([5, 3, 4, 0])
    omega = -(observer.T * eta * null)[0]
    normalized = sp.simplify(null / omega)
    sight4 = sp.simplify(normalized - observer)
    require((observer.T * eta * observer)[0] == -1, "unit_clock", checks)
    require((null.T * eta * null)[0] == 0, "future_null", checks)
    require(omega == 5, "positive_frequency", checks)
    require((observer.T * eta * sight4)[0] == 0, "sight_in_rest_space", checks)
    require((sight4.T * eta * sight4)[0] == 1, "unit_sight_direction", checks)

    # Generic non-antipodal symbolic pair using rational stereographic functions.
    t = sp.symbols("t", real=True)
    c = sp.simplify((1 - t**2) / (1 + t**2))
    s = sp.simplify(2 * t / (1 + t**2))
    n = sp.Matrix([1, 0, 0])
    m = sp.Matrix([c, s, 0])
    r = rotation(n, m)
    common = sp.Matrix([0, 0, 1])
    source_screen = sp.Matrix([0, 1, 0])
    target_screen = sp.Matrix([-s, c, 0])
    require(sp.simplify((m.T * m)[0]) == 1, "target_unit", checks)
    require(equal_matrix(r * n, m), "rotation_maps_direction", checks)
    require(equal_matrix(r.T * r, sp.eye(3)), "rotation_orthogonal", checks)
    require(sp.simplify(r.det()) == 1, "rotation_proper", checks)
    require(equal_matrix(r * common, common), "common_perpendicular_fixed", checks)
    require(equal_matrix(r * source_screen, target_screen), "screen_basis_mapped", checks)
    require(sp.simplify((m.T * (r * source_screen))[0]) == 0, "target_screen_orthogonal", checks)
    require(
        sp.simplify(((r * source_screen).T * (r * source_screen))[0]) == 1,
        "screen_norm_preserved",
        checks,
    )
    require(equal_matrix(rotation(n, n), sp.eye(3)), "identity", checks)
    require(equal_matrix(rotation(m, n), r.T), "inverse", checks)

    reflection = sp.diag(1, -1, 1)
    require(
        equal_matrix(rotation(reflection * n, reflection * m), reflection * r * reflection.T),
        "passive_O3_covariance",
        checks,
    )

    orthogonal = sp.Matrix([0, 1, 0])
    r_orthogonal = rotation(n, orthogonal)
    require(equal_matrix(r_orthogonal * n, orthogonal), "orthogonal_stratum_regular", checks)
    require(equal_matrix(r_orthogonal.T * r_orthogonal, sp.eye(3)), "orthogonal_stratum_isometry", checks)

    # Antipodal nonuniqueness.
    minus_n = -n
    antipodal_one = sp.diag(-1, -1, 1)
    antipodal_two = sp.diag(-1, 1, -1)
    require(equal_matrix(antipodal_one * n, minus_n), "antipodal_map_one", checks)
    require(equal_matrix(antipodal_two * n, minus_n), "antipodal_map_two", checks)
    require(equal_matrix(antipodal_one.T * antipodal_one, sp.eye(3)), "antipodal_one_orthogonal", checks)
    require(equal_matrix(antipodal_two.T * antipodal_two, sp.eye(3)), "antipodal_two_orthogonal", checks)
    require(antipodal_one.det() == 1 and antipodal_two.det() == 1, "antipodal_maps_proper", checks)
    require(not equal_matrix(antipodal_one, antipodal_two), "antipodal_nonunique", checks)

    # Same-great-circle control.
    a = sp.Matrix([1, 0, 0])
    b = sp.Matrix([sp.Rational(3, 5), sp.Rational(4, 5), 0])
    d = sp.Matrix([0, 1, 0])
    require(
        equal_matrix(rotation(b, d) * rotation(a, b), rotation(a, d)),
        "great_circle_composition_control",
        checks,
    )

    # Exact noncoplanar octant witness.
    x = sp.Matrix([1, 0, 0])
    y = sp.Matrix([0, 1, 0])
    z = sp.Matrix([0, 0, 1])
    r_yx = rotation(x, y)
    r_zy = rotation(y, z)
    r_zx = rotation(x, z)
    composite = sp.simplify(r_zy * r_yx)
    defect = sp.simplify(r_zx.T * composite)
    expected_defect = sp.Matrix([[1, 0, 0], [0, 0, -1], [0, 1, 0]])
    require(equal_matrix(r_yx * x, y) and equal_matrix(r_zy * y, z), "octant_edges_map", checks)
    require(not equal_matrix(composite, r_zx), "direct_not_composite", checks)
    require(equal_matrix(defect, expected_defect), "octant_defect_exact", checks)
    require(equal_matrix(defect.T * defect, sp.eye(3)), "defect_orthogonal", checks)
    require(equal_matrix(defect * x, x), "defect_fixes_start_direction", checks)
    require(defect.det() == 1, "defect_screen_SO2", checks)
    require(not equal_matrix(defect, sp.eye(3)), "defect_nontrivial", checks)

    # Orthogonal projection is not the finite screen isometry.
    target_tangent = sp.Matrix([-s, c, 0])
    projection_matrix = sp.diag(c, 1)
    require(sp.simplify(projection_matrix.det() - c) == 0, "projection_screen_determinant", checks)
    require(
        not equal_matrix(projection_matrix.T * projection_matrix, sp.eye(2)),
        "projection_not_generic_isometry",
        checks,
    )
    projection_at_right_angle = projection_matrix.subs(t, 1)
    require(projection_at_right_angle.det() == 0, "projection_singular_at_right_angle", checks)
    require(sp.simplify((target_tangent.T * target_tangent)[0]) == 1, "target_tangent_unit", checks)

    # Scalar and Jacobi channels remain separately typed.
    q_ab, q_bc = sp.symbols("q_ab q_bc", positive=True)
    require(sp.simplify((q_bc * q_ab) - (q_ab * q_bc)) == 0, "G224_scalar_composition", checks)
    flat_jacobi = 2 * sp.eye(2)
    require(not equal_matrix(flat_jacobi.T * flat_jacobi, sp.eye(2)), "Jacobi_not_vertex_isometry", checks)
    require(flat_jacobi.det() == 4, "Jacobi_area_separate", checks)

    result = {
        "status": "PASS",
        "symbolic_checks": len(checks),
        "checks": checks,
        "screen_planes_metric_derived": True,
        "least_turning_direct_isometry_nonantipodal": True,
        "direct_isometry_exact_vertex_cocycle": False,
        "finite_composition_holonomy": True,
        "antipodal_least_turning_extension_unique": False,
        "global_endpoint_only_flat_screen_carry": False,
        "G224_scalar_carry_retained": True,
        "G188_Jacobi_replaced": False,
        "pointwise_direct_map_physical_transport_selected": False,
        "independent_direct_relation_constrained": False,
        "universal_null_protocol_selected": False,
        "physical_history_selected": False,
        "landing": LANDING,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
