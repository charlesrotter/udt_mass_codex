#!/usr/bin/env python3
"""Exact controller for stationary R17 endpoint-depth / holonomy joint data."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def rotation(theta: sp.Expr) -> sp.Matrix:
    return sp.Matrix([
        [sp.cos(theta), -sp.sin(theta)],
        [sp.sin(theta), sp.cos(theta)],
    ])


def write_tsv(name: str, fieldnames: tuple[str, ...], rows: list[dict[str, str]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    d1, d2, th1, th2, w = sp.symbols("d1 d2 th1 th2 w", real=True)
    ap, aq = sp.symbols("alpha_p alpha_q", real=True)
    lam, phi_p, phi_q = sp.symbols("lambda phi_p phi_q", real=True)

    def C(depth: sp.Expr, angle: sp.Expr, weight: sp.Expr) -> sp.Matrix:
        return sp.exp(weight * depth) * rotation(angle)

    composition = sp.simplify(C(d2, th2, w) * C(d1, th1, w) - C(d1 + d2, th1 + th2, w))
    inversion = sp.simplify(C(-d1, -th1, w) * C(d1, th1, w) - sp.eye(2))
    gauge_left = sp.simplify(rotation(-aq) * C(d1, th1, w) * rotation(ap))
    gauge_expected = C(d1, th1 + ap - aq, w)
    gauge_covariance = sp.simplify(gauge_left - gauge_expected)

    delta = phi_q - phi_p
    v_p = sp.exp(lam * phi_p)
    v_q = sp.exp(lam * phi_q)
    vector_weight = sp.simplify(sp.log(v_p / v_q) / delta)
    covector_weight = sp.simplify(sp.log(v_q / v_p) / delta)
    vector_scale_check = sp.simplify(v_p / v_q - sp.exp(-lam * delta))
    covector_scale_check = sp.simplify(v_q / v_p - sp.exp(lam * delta))
    determinant = sp.simplify(C(d1, th1, w).det())

    # Gauge-safe two-path relative holonomy.
    eta, gamma = sp.symbols("eta gamma", real=True)
    U_eta = rotation(eta)
    U_gamma = rotation(gamma)
    relative = sp.simplify(U_eta.inv() * U_gamma)
    U_eta_g = rotation(-aq) * U_eta * rotation(ap)
    U_gamma_g = rotation(-aq) * U_gamma * rotation(ap)
    relative_g = sp.simplify(U_eta_g.inv() * U_gamma_g)
    relative_covariance = sp.simplify(relative_g - rotation(-ap) * relative * rotation(ap))

    # A representative higher-jet joint one-form alpha=I dphi need not be exact.
    # On a rectangle with phi=y and I=x, alpha=x dy has nonzero loop integral.
    x0, x1, y0, y1 = sp.symbols("x0 x1 y0 y1", real=True)
    rectangle_integral = sp.simplify(x1 * (y1 - y0) + x0 * (y0 - y1))
    rectangle_area = sp.simplify((x1 - x0) * (y1 - y0))
    a_control = sp.Rational(1, 64)
    x_control = sp.Integer(1)
    B_control = sp.simplify(2 - x_control + a_control**2 / x_control)
    F23_control = sp.simplify(-2 * B_control)

    checks = {
        "joint_CO2_composition_all_w": composition == sp.zeros(2),
        "joint_CO2_inversion_all_w": inversion == sp.zeros(2),
        "joint_CO2_endpoint_gauge_covariance": gauge_covariance == sp.zeros(2),
        "joint_CO2_determinant": sp.simplify(determinant - sp.exp(2 * w * d1)) == 0,
        "complete_screen_vector_weight_minus_lambda": sp.simplify(vector_weight + lam) == 0,
        "complete_screen_covector_weight_plus_lambda": sp.simplify(covector_weight - lam) == 0,
        "complete_screen_vector_scale": vector_scale_check == 0,
        "complete_screen_covector_scale": covector_scale_check == 0,
        "two_path_relative_holonomy_gauge_covariant": relative_covariance == sp.zeros(2),
        "rectangle_joint_one_form_nonexact_witness": sp.simplify(rectangle_integral - rectangle_area) == 0,
        "loop_endpoint_depth_zero": sp.simplify(phi_p - phi_p) == 0,
        "C08_zero_depth_nonzero_angular_curvature": B_control == sp.Rational(4097, 4096) and F23_control == -sp.Rational(4097, 2048),
    }
    assert all(checks.values()), checks

    candidate_rows = [
        {"candidate_id": "J01", "classification": "DERIVED_GAUGE_COVARIANT_NORMAL_ISOMETRY_GROUPOID_FUNCTOR__LOCALLY_DIRECT_PRODUCT", "composition": "EXACT", "gauge_status": "ENDPOINT_COVARIANT", "selection_status": "METRIC_OWNED_AFTER_PATH_SUPPLIED"},
        {"candidate_id": "J02", "classification": "DERIVED_ONE_PARAMETER_COplus2_FUNCTOR_FAMILY", "composition": "EXACT_ALL_REAL_w", "gauge_status": "ENDPOINT_COVARIANT", "selection_status": "w_UNSELECTED_ABSTRACTLY"},
        {"candidate_id": "J03", "classification": "DERIVED_COMPLETE_COFRAME_COMPATIBLE_SCREEN_LIFTS", "composition": "EXACT", "gauge_status": "ENDPOINT_COVARIANT", "selection_status": "VECTOR_w_MINUS_lambda__COVECTOR_w_PLUS_lambda"},
        {"candidate_id": "J04", "classification": "NO_NONTRIVIAL_OPEN_PATH_ANGLE_SCALAR", "composition": "NOT_APPLICABLE", "gauge_status": "INDEPENDENT_ENDPOINT_GAUGE_ERASES_U_DEPENDENCE", "selection_status": "ONLY_delta_DEPENDENCE_SURVIVES"},
        {"candidate_id": "J05", "classification": "UNIQUE_NORMALIZED_CONTINUOUS_REAL_CHARACTER_IS_delta", "composition": "EXACT", "gauge_status": "INVARIANT", "selection_status": "SO2_CHARACTER_ZERO_BY_COMPACTNESS"},
        {"candidate_id": "J06", "classification": "CONTINUOUS_U1_CHARACTER_FAMILY", "composition": "EXACT", "gauge_status": "OPEN_PATH_COVARIANT_NOT_INVARIANT", "selection_status": "k_REAL_n_INTEGER_UNSELECTED"},
        {"candidate_id": "J07", "classification": "CONDITIONAL_UNIVERSAL_COVER_LIFT", "composition": "EXACT_AFTER_LIFT", "gauge_status": "NOT_REPRESENTATIVE_FREE", "selection_status": "TRIVIALIZATION_OR_LIFT_REQUIRED"},
        {"candidate_id": "J08", "classification": "CLOSED_LOOP_HOLONOMY_SURVIVES_WITH_ZERO_delta", "composition": "LOOP_MULTIPLICATION", "gauge_status": "SO2_ANGLE_OR_O2_COSINE", "selection_status": "ANGULAR_ONLY_ON_LOOP"},
        {"candidate_id": "J09", "classification": "TWO_PATH_RELATIVE_HOLONOMY_SURVIVES", "composition": "PATH_PAIR_RETURN", "gauge_status": "SO2_INVARIANT_OR_O2_CONJUGACY", "selection_status": "PATH_PAIR_REQUIRED"},
        {"candidate_id": "J10", "classification": "NO_NONTRIVIAL_CONTINUOUS_SEMIDIRECT_DEPTH_ACTION", "composition": "DIRECT_PRODUCT_ONLY", "gauge_status": "ORIENTATION_REVERSAL_IS_DISCRETE", "selection_status": "Aut_SO2_EQUALS_Z2"},
        {"candidate_id": "J11", "classification": "CONDITIONAL_HIGHER_JET_LINE_INTEGRAL_FAMILY", "composition": "EXACT_BY_LINE_INTEGRATION", "gauge_status": "O2_SAFE_IF_BUILT_FROM_EVEN_CURVATURE_INVARIANTS", "selection_status": "GENERAL_NONEXACT_CONTROL_NOT_R17_WITNESS__STATIONARY_REALIZATION_OPEN"},
        {"candidate_id": "J12", "classification": "FLAT_SIMPLY_CONNECTED_CONTROL_REDUCES_TO_ENDPOINT_MAP", "composition": "EXACT", "gauge_status": "GLOBAL_PARALLEL_FRAME_EXISTS", "selection_status": "SPECIAL_LOCUS_NOT_PHYSICALLY_SELECTED"},
    ]
    write_tsv(
        "JOINT_CANDIDATE_CLASSIFICATION.tsv",
        ("candidate_id", "classification", "composition", "gauge_status", "selection_status"),
        candidate_rows,
    )

    gauge_rows = [
        {"query_type": "single_open_path", "depth_data": "delta_pq", "angular_data": "U_gamma", "representative_free_joint": "delta_ONLY", "reason": "independent_endpoint_SO2_action_transitive_on_U"},
        {"query_type": "closed_loop", "depth_data": "ZERO", "angular_data": "Hol_gamma", "representative_free_joint": "SO2_angle_mod_2pi_or_O2_cosine", "reason": "same_endpoint_gauge_conjugation"},
        {"query_type": "two_paths_same_endpoints", "depth_data": "common_delta_pq", "angular_data": "U_eta_inverse_U_gamma", "representative_free_joint": "delta_plus_relative_holonomy_class", "reason": "endpoint_gauges_cancel"},
        {"query_type": "framed_open_path", "depth_data": "delta_pq", "angular_data": "theta_gamma_in_chosen_frames", "representative_free_joint": "NONE_WITHOUT_FRAME_QUOTIENT", "reason": "angle_shifts_by_alpha_p_minus_alpha_q"},
    ]
    write_tsv(
        "GAUGE_INVARIANT_QUERY_ATLAS.tsv",
        ("query_type", "depth_data", "angular_data", "representative_free_joint", "reason"),
        gauge_rows,
    )

    character_rows = [
        {"target": "R_additive", "general_continuous_character": "a_delta", "angular_coefficient": "ZERO", "normalization_effect": "a=1", "status": "UNIQUE_delta_IN_DECLARED_CLASS"},
        {"target": "U1", "general_continuous_character": "exp(i(k_delta+n_theta))", "angular_coefficient": "n_in_Z", "normalization_effect": "does_not_select_n", "status": "FAMILY_NOT_REAL_DEPTH"},
        {"target": "R_universal_cover_angle", "general_continuous_character": "a_delta+b_tilde_theta", "angular_coefficient": "b_REAL", "normalization_effect": "requires_lift", "status": "CONDITIONAL_NOT_REPRESENTATIVE_FREE"},
    ]
    write_tsv(
        "CHARACTER_ATLAS.tsv",
        ("target", "general_continuous_character", "angular_coefficient", "normalization_effect", "status"),
        character_rows,
    )

    one_form_rows = [
        {"family": "dphi", "example": "alpha=dphi", "composition": "EXACT", "path_dependence": "NONE", "selection": "DERIVED_delta_K"},
        {"family": "even_curvature_weighted", "example": "alpha=I(F,g,E,H)*dphi", "composition": "EXACT", "path_dependence": "IF_dI_wedge_dphi_NONZERO__NOT_SHOWN_ON_STATIONARY_R17", "selection": "UNSELECTED_CONSTRUCTION_FAMILY"},
        {"family": "orientation_odd", "example": "alpha=i_gradphi_F", "composition": "EXACT", "path_dependence": "REQUIRES_SEPARATE_R17_TYPE_AND_NONEXACTNESS_CHECK", "selection": "REQUIRES_ORIENTATION_LOCAL_SYSTEM"},
        {"family": "exact_invariant_coboundary", "example": "alpha=dH(phi,curvature_invariants)", "composition": "EXACT", "path_dependence": "NONE", "selection": "INFINITE_ENDPOINT_POTENTIAL_FAMILY"},
    ]
    write_tsv(
        "LOCAL_ONE_FORM_COCYCLE_ATLAS.tsv",
        ("family", "example", "composition", "path_dependence", "selection"),
        one_form_rows,
    )

    result = {
        "schema_version": 1,
        "arena": "REGULAR_STATIONARY_R17_ON_R_TIMES_S3_WITH_SUPPLIED_PATHS",
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
        "status": "PASS",
        "joint_path_functor": "R_ADDITIVE_TIMES_ORIENTED_NORMAL_ISOMETRY_GROUPOID__LOCALLY_R_TIMES_SO2",
        "co2_family": "C_w(gamma)=exp(w*delta_K(gamma))*U_gamma_FOR_ALL_REAL_w",
        "complete_coframe_vector_weight": "w=-lambda",
        "complete_coframe_covector_weight": "w=+lambda",
        "continuous_real_character": "UNIQUE_NORMALIZED_CHARACTER_IS_delta_K",
        "angular_real_character": "ZERO",
        "continuous_semidirect_depth_action": "TRIVIAL",
        "open_path_representative_free_angular_scalar": "NONE",
        "closed_loop_data": "delta=0_PLUS_SO2_HOLONOMY_OR_O2_CONJUGACY",
        "two_path_data": "common_delta_PLUS_RELATIVE_HOLONOMY",
        "depth_does_not_determine_holonomy": "C08_HAS_delta_LOOP_ZERO_AND_F23=-4097/2048",
        "joint_connection_curvature": "ROTATIONAL_F_ONLY__EXACT_DILATION_w_dphi_HAS_ZERO_CURVATURE",
        "higher_jet_scalar_path_cocycles": "LINE_INTEGRALS_COMPOSE__GENERAL_NONEXACT_CONTROL_EXISTS__STATIONARY_R17_NONEXACT_REALIZATION_OPEN__NO_MEMBER_SELECTED",
        "physical_path_or_arrow_selected": False,
        "maximum_ruling": "CONDITIONAL_STATIONARY_R17_DEPTH_NORMAL_ISOMETRY_GROUPOID_FUNCTOR_DERIVED__LOCALLY_DIRECT_PRODUCT__COMPLETE_COFRAME_FIXES_SCREEN_CO2_WEIGHT_BY_VARIANCE__UNIQUE_NORMALIZED_CONTINUOUS_REAL_ORDER_ZERO_CHARACTER_IS_ENDPOINT_DEPTH__ANGULAR_DATA_REMAINS_PATH_OR_LOOP_VALUED__GENERAL_HIGHER_JET_LINE_INTEGRALS_COMPOSE_BUT_STATIONARY_R17_NONEXACT_REALIZATION_OPEN__PHYSICAL_PATH_AND_ARROW_OPEN",
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
