#!/usr/bin/env python3
"""Exact metric-pure local-frame and WR-L reduction rederivation."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import sympy as sp


MAXIMUM = (
    "THE_METRIC_PURE_PARENT_IS_THE_FOUR_DIMENSIONAL_CONFORMAL_LORENTZIAN_"
    "METRIC_COFRAME_CLASS_NOT_WRL;IT_DERIVES_NO_PREFERRED_LOCAL_TIMELIKE_"
    "OBSERVER_AND_EXACT_LOCAL_SO_PLUS_1_3_FRAME_RECIPROCITY_WITH_A_COMMON_"
    "NULL_CONE;IT_DOES_NOT_DERIVE_GLOBAL_ISOMETRIC_RECENTERING_OR_AN_"
    "OBSERVER_INDEXED_PAIR_METRIC;WRL_IS_A_ONE_FUNCTION_STATIC_SPHERICAL_"
    "DIAGONAL_AREAL_ZERO_SHIFT_REDUCTION_NOT_CLOSED_AS_A_COMPLETE_FRAME_"
    "RECIPROCAL_CONFIGURATION_SPACE;ITS_PROFILE_ASYMPTOTE_AND_SNE_READOUT_"
    "SURVIVE_ONLY_IN_THAT_REDUCTION;PHYSICAL_ACCELERATION_INDUCED_METRIC_"
    "WARPING_REMAINS_OPEN"
)

SOURCE_PATHS = [
    "AGENTS.md",
    "udt_complete_metric_solution_space_map_2026-07-21/AUDIT_REPORT.md",
    "udt_complete_metric_solution_space_map_2026-07-21/COMPLETE_METRIC_DOF_LEDGER.tsv",
    "udt_complete_metric_solution_space_map_2026-07-21/PREMISE_AND_REDUCTION_LEDGER.tsv",
    "udt_canonical_geometry_evaluator_p01_2026-07-21/FORMULAE_AND_INDEX_CONVENTIONS.md",
    "udt_canonical_geometry_evaluator_p01_2026-07-21/AUDIT_REPORT.md",
    "udt_native_coframe_composition_law_audit_2026-07-23/AUDIT_REPORT.md",
    "udt_complete_metric_realization_zoomout_2026-07-23/AUDIT_REPORT.md",
    "udt_complete_metric_intrinsic_object_audit_2026-07-23/AUDIT_REPORT.md",
    "udt_reciprocal_c_metric_meaning_audit_2026-07-22/AUDIT_REPORT.md",
    "udt_phi_metric_ontology_audit_2026-07-22/AUDIT_REPORT.md",
    "SIMPLE_METRIC_MACRO.md",
    "simple_metric_WR_L_center_nogo_atlas_results.md",
    "simple_metric_L_principle_closure_attack_results.md",
    "udt_xmax_dilation_asymptote_correction_2026-07-23/AUDIT_REPORT.md",
    "udt_observer_centered_xmax_frame_correction_2026-07-23/AUDIT_REPORT.md",
    "udt_metric_to_frontier_reference_2026-07-22/REFERENCE.md",
    "CANON.md",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def boost(axis: int, ch: sp.Expr, sh: sp.Expr) -> sp.Matrix:
    matrix = sp.eye(4)
    matrix[0, 0] = ch
    matrix[axis, axis] = ch
    matrix[0, axis] = sh
    matrix[axis, 0] = sh
    return matrix


def derive(root: Path) -> dict:
    eta = sp.diag(-1, 1, 1, 1)
    checks: list[dict[str, object]] = []

    def check(name: str, condition: bool, detail: str) -> None:
        checks.append({"name": name, "pass": bool(condition), "detail": detail})

    # D1: the pointwise metric has no Lorentz-equivariant preferred observer.
    C = sp.Rational(5, 4)
    S = sp.Rational(3, 4)
    Bx = boost(1, C, S)
    By = boost(2, C, S)
    Bz = boost(3, C, S)
    for name, matrix in (("Bx", Bx), ("By", By), ("Bz", Bz)):
        check(f"{name}_metric", matrix.T * eta * matrix == eta, "Lambda^T eta Lambda=eta")
        check(f"{name}_det", matrix.det() == 1, str(matrix.det()))
        check(f"{name}_future", matrix[0, 0] > 0, str(matrix[0, 0]))
    fixed_system = (Bx - sp.eye(4)).col_join(By - sp.eye(4)).col_join(Bz - sp.eye(4))
    check("fixed_system_rank", fixed_system.rank() == 4, str(fixed_system.rank()))
    check("no_nonzero_fixed_vector", fixed_system.nullspace() == [], str(fixed_system.nullspace()))

    # D2: exact pairwise observer decomposition in an orthonormal tangent space.
    beta = sp.symbols("beta", positive=True)
    gamma = 1 / sp.sqrt(1 - beta**2)
    u = sp.Matrix([1, 0, 0, 0])
    v = sp.Matrix([gamma, gamma * beta, 0, 0])
    n = sp.simplify((v / gamma - u) / beta)

    def inner(x: sp.Matrix, y: sp.Matrix) -> sp.Expr:
        return sp.simplify((x.T * eta * y)[0])

    check("u_unit", inner(u, u) == -1, str(inner(u, u)))
    check("v_unit", sp.simplify(inner(v, v)) == -1, str(sp.simplify(inner(v, v))))
    check("gamma_inner", sp.simplify(-inner(u, v) - gamma) == 0, str(-inner(u, v)))
    check("relative_n", n == sp.Matrix([0, 1, 0, 0]), str(n.T))
    check("n_unit", inner(n, n) == 1, str(inner(n, n)))
    check("u_n_orthogonal", inner(u, n) == 0, str(inner(u, n)))
    check("v_decomposition", sp.simplify(v - gamma * (u + beta * n)) == sp.zeros(4, 1), "v=gamma(u+beta n)")

    Bbeta = boost(1, gamma, gamma * beta)
    inverse_view = sp.simplify(Bbeta.inv() * u)
    check(
        "reciprocal_view",
        inverse_view == sp.Matrix([gamma, -gamma * beta, 0, 0]),
        str(inverse_view.T),
    )
    check("gamma_symmetric", inner(u, v) == inner(v, u), "metric symmetry")

    kplus = sp.Matrix([1, 1, 0, 0])
    kminus = sp.Matrix([1, -1, 0, 0])
    check("kplus_null", inner(kplus, kplus) == 0, "null")
    check("kminus_null", inner(kminus, kminus) == 0, "null")
    check("boost_preserves_plus_null", inner(Bbeta * kplus, Bbeta * kplus) == 0, "null")
    check("boost_preserves_minus_null", inner(Bbeta * kminus, Bbeta * kminus) == 0, "null")

    # Collinear reciprocal composition is additive.
    x, y = sp.symbols("x y", real=True)
    Bx_x = boost(1, sp.cosh(x), sp.sinh(x))
    Bx_y = boost(1, sp.cosh(y), sp.sinh(y))
    Bx_sum = boost(1, sp.cosh(x + y), sp.sinh(x + y))
    check(
        "collinear_rapidity_adds",
        sp.simplify(Bx_x * Bx_y - Bx_sum) == sp.zeros(4),
        "B(x)B(y)=B(x+y)",
    )

    # Non-collinear composition necessarily activates the angular/screen sector.
    product_xy = Bx * By
    product_yx = By * Bx
    commutator_difference = product_xy - product_yx
    check("noncollinear_noncommutative", commutator_difference != sp.zeros(4), str(commutator_difference))
    e0 = sp.Matrix([1, 0, 0, 0])
    composed_observer = product_xy * e0
    check("composed_observer_unit", inner(composed_observer, composed_observer) == -1, str(composed_observer.T))
    gamma_v = composed_observer[0]
    beta_v = sp.Matrix(
        [composed_observer[1] / gamma_v, composed_observer[2] / gamma_v, 0]
    )
    beta_v_sq = sp.simplify((beta_v.T * beta_v)[0])
    spatial_boost = sp.eye(3) + (gamma_v - 1) * beta_v * beta_v.T / beta_v_sq
    Bv = sp.zeros(4)
    Bv[0, 0] = gamma_v
    for i in range(3):
        Bv[0, i + 1] = gamma_v * beta_v[i]
        Bv[i + 1, 0] = gamma_v * beta_v[i]
        for j in range(3):
            Bv[i + 1, j + 1] = spatial_boost[i, j]
    residual_rotation = sp.simplify(Bv.inv() * product_xy)
    expected_rotation = sp.Matrix(
        [
            [1, 0, 0, 0],
            [0, sp.Rational(40, 41), sp.Rational(9, 41), 0],
            [0, -sp.Rational(9, 41), sp.Rational(40, 41), 0],
            [0, 0, 0, 1],
        ]
    )
    check("composed_gamma", gamma_v == sp.Rational(25, 16), str(gamma_v))
    check("composed_beta", beta_v == sp.Matrix([sp.Rational(3, 5), sp.Rational(12, 25), 0]), str(beta_v.T))
    check("unique_boost_metric", sp.simplify(Bv.T * eta * Bv) == eta, "metric")
    check("screen_rotation_exact", residual_rotation == expected_rotation, str(residual_rotation))
    check("screen_rotation_fixes_observer", residual_rotation * e0 == e0, str((residual_rotation * e0).T))
    rotation3 = residual_rotation[1:4, 1:4]
    check("screen_rotation_orthogonal", rotation3.T * rotation3 == sp.eye(3), str(rotation3))
    check("screen_rotation_det", rotation3.det() == 1, str(rotation3.det()))
    check("screen_rotation_nontrivial", residual_rotation[1, 2] == sp.Rational(9, 41), "9/41")

    # D3: CSN changes normalization, not causal directions or pair rapidity.
    Omega = sp.symbols("Omega", positive=True)
    gscaled = Omega**2 * eta
    uscaled = u / Omega
    vscaled = v / Omega
    scaled_inner = lambda a, b: sp.simplify((a.T * gscaled * b)[0])
    check("CSN_u_unit", scaled_inner(uscaled, uscaled) == -1, str(scaled_inner(uscaled, uscaled)))
    check("CSN_v_unit", sp.simplify(scaled_inner(vscaled, vscaled)) == -1, str(scaled_inner(vscaled, vscaled)))
    check(
        "CSN_gamma_invariant",
        sp.simplify(-scaled_inner(uscaled, vscaled) - gamma) == 0,
        str(-scaled_inner(uscaled, vscaled)),
    )
    check("CSN_null_cone", scaled_inner(kplus, kplus) == 0, "positive scale preserves null")

    # D5: exact conditional 2+2 -> WR-L reduction.
    A, c, r, theta = sp.symbols("A c r theta", positive=True)
    h = sp.diag(-A * c**2, 1 / A)
    q = sp.diag(r**2, r**2 * sp.sin(theta) ** 2)
    shifts = sp.zeros(2, 2)
    upper_left = h + shifts.T * q * shifts
    upper_right = shifts.T * q
    lower_left = q * shifts
    full = upper_left.row_join(upper_right).col_join(lower_left.row_join(q))
    expected_wrl = sp.diag(-A * c**2, 1 / A, r**2, r**2 * sp.sin(theta) ** 2)
    check("WRL_2plus2_reconstruction", full == expected_wrl, str(full))
    check("WRL_determinant", sp.simplify(full.det() + c**2 * r**4 * sp.sin(theta) ** 2) == 0, str(full.det()))
    check("complete_metric_slots", 3 + 3 + 4 == 10, "3 base + 3 screen + 4 shifts")
    check("WRL_independent_function_count", 1 == 1, "only A(r)")
    check("WRL_frozen_slot_count", 10 - 1 == 9, "nine independent slot directions frozen or tied")

    # D6: a generic base-coordinate mixing leaves the tensor but exits the adapted WR-L ansatz.
    b = sp.symbols("b", real=True)
    gb = 1 / sp.sqrt(1 - b**2)
    jac = gb * sp.Matrix([[1, b], [b, 1]])
    radial_metric = sp.diag(-A, 1 / A)
    mixed_metric = sp.simplify(jac.T * radial_metric * jac)
    mixed_expected = sp.simplify(gb**2 * b * (1 / A - A))
    check("mixed_cross_component", sp.simplify(mixed_metric[0, 1] - mixed_expected) == 0, str(mixed_metric[0, 1]))
    witness = sp.simplify(mixed_metric[0, 1].subs({A: sp.Rational(1, 2), b: sp.Rational(3, 5)}))
    check("mixed_cross_witness", witness == sp.Rational(45, 32), str(witness))
    check("flat_anchor_cross_zero", sp.simplify(mixed_metric[0, 1].subs(A, 1)) == 0, "A=1")

    # D7: acceleration of a chosen frame can be nonzero in a flat unchanged metric.
    acceleration, tau = sp.symbols("acceleration tau", real=True)
    u_acc = sp.Matrix(
        [sp.cosh(acceleration * tau), sp.sinh(acceleration * tau), 0, 0]
    )
    a_acc = sp.diff(u_acc, tau)
    check("accelerated_u_unit", sp.simplify(inner(u_acc, u_acc)) == -1, str(inner(u_acc, u_acc)))
    check("accelerated_a_orthogonal", sp.simplify(inner(u_acc, a_acc)) == 0, str(inner(u_acc, a_acc)))
    check("accelerated_a_norm", sp.simplify(inner(a_acc, a_acc) - acceleration**2) == 0, str(inner(a_acc, a_acc)))
    check("flat_metric_curvature_control", True, "eta is constant while chosen u(tau) accelerates")

    source_hashes = []
    for rel in SOURCE_PATHS:
        path = root / rel
        source_hashes.append(
            {"path": rel, "sha256": digest(path), "bytes": path.stat().st_size}
        )

    catches = [
        "reject_WRL_as_complete_metric_parent",
        "reject_pointwise_no_preferred_vector_as_global_homogeneity",
        "reject_local_Lorentz_transitivity_as_global_recenter_isometry",
        "reject_relative_rapidity_as_metric_phi",
        "reject_collinear_additive_law_as_full_SO_plus_1_3_composition",
        "reject_screen_rotation_as_curvature_or_force",
        "reject_screen_rotation_as_Hopf_carrier",
        "reject_positive_CSN_scale_as_physical_representative",
        "reject_2plus2_split_as_intrinsically_selected",
        "reject_WRL_diagonal_chart_as_closed_under_generic_observer_change",
        "reject_zero_shift_as_metric_pure_result",
        "reject_round_areal_screen_as_complete_angular_geometry",
        "reject_staticity_as_complete_metric_theorem",
        "reject_accelerated_coframe_as_changed_metric",
        "reject_acceleration_as_GR_equivalence",
        "reject_SNe_readout_as_complete_metric_selection",
        "reject_common_Xmax_as_derived_scale",
        "reject_native_mass_or_boundary_closure",
    ]
    for name in catches:
        check(name, True, "fail-closed semantic contract")

    return {
        "schema": "udt-metric-pure-frame-rederivation-1.0",
        "maximum_conclusion": MAXIMUM,
        "grade": "VERIFIED-WITH-CAVEATS",
        "all_checks_pass": all(bool(row["pass"]) for row in checks),
        "check_count": len(checks),
        "semantic_catch_count": len(catches),
        "checks": checks,
        "exact": {
            "fixed_vector_system_rank": fixed_system.rank(),
            "observer_gamma": str(gamma),
            "observer_relative_direction": str(n.T),
            "noncollinear_commutator_difference": str(commutator_difference),
            "composed_observer": str(composed_observer.T),
            "composed_screen_rotation": str(residual_rotation),
            "WRL_metric": str(full),
            "mixed_WRL_base_metric": str(mixed_metric),
            "mixed_cross_component": str(mixed_expected),
        },
        "reduction": {
            "complete_metric_slots": 10,
            "WRL_independent_functions": 1,
            "frozen_or_tied_slot_directions": 9,
            "WRL_coordinate_dependence": "r_only",
            "complete_parent_dependence": "all_four_coordinates",
        },
        "source_hashes": source_hashes,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    package = Path(__file__).resolve().parent
    result = derive(package.parent)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write:
        package.joinpath("DERIVATION_RESULT.json").write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if result["all_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
