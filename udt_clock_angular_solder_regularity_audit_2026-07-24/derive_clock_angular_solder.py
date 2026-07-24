#!/usr/bin/env python3
"""Exact fixed-pairing and cap-regularity algebra for the solder audit."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def write_tsv(name: str, fields: list[str], rows: list[dict[str, str]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fields, delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def require(label: str, condition: bool, checks: dict[str, str]) -> None:
    if not condition:
        raise AssertionError(label)
    checks[label] = "PASS"


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    eta = sp.symbols("eta", positive=True)
    phi = sp.symbols("phi", real=True)
    kappa = sp.symbols("kappa", positive=True, finite=True)
    b, ell, c = sp.symbols("b ell c", positive=True, finite=True)
    weight = sp.symbols("weight", real=True)

    checks: dict[str, str] = {}

    # Exact fixed-K reciprocal pair.
    K = sp.Matrix([[0, 1], [1, 0]])
    P = sp.diag(sp.exp(-weight * phi), sp.exp(weight * phi))
    Psame = sp.diag(sp.exp(weight * phi), sp.exp(weight * phi))
    require("fixed_K_opposite_characters", sp.simplify(P.T * K * P - K) == sp.zeros(2), checks)
    require(
        "fixed_K_same_sign_rejected",
        sp.simplify(Psame.T * K * Psame - K) != sp.zeros(2),
        checks,
    )

    weights = (-sp.Integer(1), sp.Integer(1), -kappa, kappa)
    require("complete_character_determinant_one", sp.simplify(sum(weights)) == 0, checks)
    generic_edges = {
        (i, j)
        for i in range(4)
        for j in range(i + 1, 4)
        if sp.simplify(weights[i] + weights[j]) == 0
    }
    require("generic_pair_edges", generic_edges == {(0, 1), (2, 3)}, checks)
    unit_weights = tuple(sp.simplify(value.subs(kappa, 1)) for value in weights)
    unit_edges = {
        (i, j)
        for i in range(4)
        for j in range(i + 1, 4)
        if unit_weights[i] + unit_weights[j] == 0
    }
    require(
        "kappa_one_pairing_degeneracy",
        unit_edges == {(0, 1), (0, 3), (1, 2), (2, 3)},
        checks,
    )

    # Round reciprocal-toric coordinate.
    eta_of_phi = sp.atan(sp.exp(2 * kappa * phi))
    deta_dphi = sp.simplify(sp.diff(eta_of_phi, phi))
    require(
        "round_depth_derivative",
        sp.simplify(deta_dphi - kappa * sp.sech(2 * kappa * phi)) == 0,
        checks,
    )
    A_round = b * deta_dphi
    R_round = b / sp.sqrt(
        sp.exp(2 * kappa * phi) + sp.exp(-2 * kappa * phi)
    )
    cos_eta = 1 / sp.sqrt(1 + sp.exp(4 * kappa * phi))
    sin_eta = sp.exp(2 * kappa * phi) * cos_eta
    require(
        "round_first_angular_leg",
        sp.simplify(
            (R_round * sp.exp(-kappa * phi)) ** 2 - (b * cos_eta) ** 2
        )
        == 0,
        checks,
    )
    require(
        "round_second_angular_leg",
        sp.simplify(
            (R_round * sp.exp(kappa * phi)) ** 2 - (b * sin_eta) ** 2
        )
        == 0,
        checks,
    )
    require("ordinary_round_neutral_eta", eta_of_phi.subs(phi, 0) == sp.pi / 4, checks)
    require("ordinary_round_neutral_A", sp.simplify(A_round.subs(phi, 0) - b * kappa) == 0, checks)

    # Scalar curvature of -N(eta)^2 c^2 dt^2 + round S3_b.
    def laplace_ratio(function: sp.Expr) -> sp.Expr:
        return sp.trigsimp(
            (sp.diff(function, eta, 2) + 2 * sp.cot(2 * eta) * sp.diff(function, eta))
            / function
        )

    phi_eta = sp.log(sp.tan(eta)) / (2 * kappa)
    N_f01 = sp.exp(-phi_eta)
    lap_f01 = sp.simplify(sp.trigsimp(laplace_ratio(N_f01)))
    expected_lap_f01 = 1 / (kappa**2 * sp.sin(2 * eta) ** 2)
    R4_f01 = sp.simplify(6 / b**2 - 2 * lap_f01 / b**2)
    require("F01_laplacian_ratio", sp.trigsimp(lap_f01 - expected_lap_f01) == 0, checks)
    require(
        "F01_scalar_curvature",
        sp.trigsimp(R4_f01 - (6 / b**2 - 2 / (b**2 * kappa**2 * sp.sin(2 * eta) ** 2)))
        == 0,
        checks,
    )
    f01_minus_p = -1 / (2 * kappa)
    f01_plus_p = 1 / (2 * kappa)
    require("F01_minus_p_nonzero", sp.solve(sp.Eq(f01_minus_p, 0), kappa) == [], checks)
    require("F01_plus_p_nonzero", sp.solve(sp.Eq(f01_plus_p, 0), kappa) == [], checks)

    # F02: the round radial leg fixes its clock/depth common amplitude.
    ell_round = b * kappa
    C_round = sp.simplify(A_round / (ell_round * sp.exp(phi)))
    N_f02_phi = sp.simplify(C_round * sp.exp(-phi))
    require(
        "F02_common_amplitude",
        sp.simplify(C_round - sp.sech(2 * kappa * phi) * sp.exp(-phi)) == 0,
        checks,
    )
    require(
        "F02_lapse_phi",
        sp.simplify(N_f02_phi - sp.sech(2 * kappa * phi) * sp.exp(-2 * phi)) == 0,
        checks,
    )
    N_f02 = sp.sin(2 * eta) * sp.tan(eta) ** (-1 / kappa)
    log_derivative = 2 * (sp.cos(2 * eta) - 1 / kappa) / sp.sin(2 * eta)
    require(
        "F02_log_derivative",
        sp.simplify(sp.diff(sp.log(N_f02), eta) - log_derivative) == 0,
        checks,
    )
    expected_lap_f02 = (
        4
        * (
            sp.cos(4 * eta)
            + 1 / kappa**2
            - 2 * sp.cos(2 * eta) / kappa
        )
        / sp.sin(2 * eta) ** 2
    )
    lap_f02 = sp.simplify(
        sp.diff(log_derivative, eta)
        + log_derivative**2
        + 2 * sp.cot(2 * eta) * log_derivative
    )
    require("F02_laplacian_ratio", sp.trigsimp(lap_f02 - expected_lap_f02) == 0, checks)
    R4_f02 = sp.simplify(6 / b**2 - 2 * expected_lap_f02 / b**2)

    p_minus = sp.simplify(1 - 1 / kappa)
    p_plus = sp.simplify(1 + 1 / kappa)
    require("F02_minus_regular_only_kappa_one", sp.solve(sp.Eq(p_minus, 0), kappa) == [1], checks)
    require("F02_plus_never_regular", sp.solve(sp.Eq(p_plus, 0), kappa) == [], checks)
    require("F02_kappa_one_neutral_lapse", sp.simplify(N_f02_phi.subs(kappa, 1).subs(phi, 0) - 1) == 0, checks)
    require(
        "F02_kappa_one_lapse_eta",
        sp.simplify(
            sp.expand_trig(N_f02.subs(kappa, 1) - 2 * sp.cos(eta) ** 2)
        )
        == 0,
        checks,
    )

    # Open-profile metric laws.
    C = sp.Function("C")(phi)
    R = sp.Function("R")(phi)
    N_open = C * sp.exp(-phi)
    A_open = ell * C * sp.exp(phi)
    B_open = sp.simplify(1 / A_open**2)
    require("F04_transnormal_B", B_open == sp.exp(-2 * phi) / (ell**2 * C**2), checks)
    require(
        "F04_distance_derivative_positive_branch",
        sp.simplify(1 / B_open - A_open**2) == 0,
        checks,
    )
    require("F04_depth_clock_ratio", sp.simplify(A_open / N_open - ell * sp.exp(2 * phi)) == 0, checks)
    require(
        "F04_pair_volume_character_cancels",
        sp.simplify((C * sp.exp(-phi)) * (ell * C * sp.exp(phi)) - ell * C**2) == 0,
        checks,
    )
    require(
        "angular_pair_character_cancels",
        sp.simplify((R * sp.exp(-kappa * phi)) * (R * sp.exp(kappa * phi)) - R**2)
        == 0,
        checks,
    )

    families = read_tsv("SOLDER_FAMILY_REGISTRY.tsv")
    require("six_registered_families", len(families) == 6, checks)
    require(
        "family_ids_exact",
        [row["family_id"] for row in families] == [f"F0{index}" for index in range(1, 7)],
        checks,
    )

    pairing_rows = [
        {
            "case": "GENERIC_KAPPA_NOT_ONE",
            "weights": "-1;+1;-kappa;+kappa",
            "allowed_fixed_K_pairing": "(clock,depth);(angular_minus,angular_plus)",
            "metric_family_effect": "F02",
            "ruling": "UNIQUE_BLOCK_PAIRING_UP_TO_PAIR_ORDER_AND_AXIS_EXCHANGE",
        },
        {
            "case": "KAPPA_EQUALS_ONE",
            "weights": "-1;+1;-1;+1",
            "allowed_fixed_K_pairing": "any_nondegenerate_pairing_between_minus_and_plus_weight_planes",
            "metric_family_effect": "same_diagonal_metric_or_constrained_F02_subfamily",
            "ruling": "COFRAME_PAIRING_DEGENERACY_NO_NEW_DIAGONAL_METRIC_FAMILY",
        },
        {
            "case": "SAME_SIGN_PROPOSED_PAIR",
            "weights": "a;a",
            "allowed_fixed_K_pairing": "none_nontrivial",
            "metric_family_effect": "excluded",
            "ruling": "FAILS_FIXED_K_INVARIANCE",
        },
    ]
    write_tsv(
        "PAIRING_CLASSIFICATION.tsv",
        ["case", "weights", "allowed_fixed_K_pairing", "metric_family_effect", "ruling"],
        pairing_rows,
    )

    cap_rows = [
        {
            "family_id": "F01",
            "cap": "PHI_TO_MINUS_INFINITY_ETA_TO_ZERO",
            "lapse_power_in_proper_cap_radius": "-1/(2*kappa)",
            "leading_DeltaN_over_N": "1/(4*kappa^2*rho^2)",
            "leading_scalar_curvature_pole": "-1/(2*kappa^2*rho^2)",
            "regularity": "CURVATURE_SINGULAR_ALL_FINITE_KAPPA_POSITIVE",
        },
        {
            "family_id": "F01",
            "cap": "PHI_TO_PLUS_INFINITY_ETA_TO_PI_OVER_2",
            "lapse_power_in_proper_cap_radius": "+1/(2*kappa)",
            "leading_DeltaN_over_N": "1/(4*kappa^2*rho^2)",
            "leading_scalar_curvature_pole": "-1/(2*kappa^2*rho^2)",
            "regularity": "CURVATURE_SINGULAR_ALL_FINITE_KAPPA_POSITIVE",
        },
        {
            "family_id": "F02",
            "cap": "PHI_TO_MINUS_INFINITY_ETA_TO_ZERO",
            "lapse_power_in_proper_cap_radius": "1-1/kappa",
            "leading_DeltaN_over_N": "(1-1/kappa)^2/rho^2",
            "leading_scalar_curvature_pole": "-2*(1-1/kappa)^2/rho^2",
            "regularity": "REGULAR_LAPSE_POWER_ONLY_AT_KAPPA_ONE_OTHERWISE_SINGULAR",
        },
        {
            "family_id": "F02",
            "cap": "PHI_TO_PLUS_INFINITY_ETA_TO_PI_OVER_2",
            "lapse_power_in_proper_cap_radius": "1+1/kappa",
            "leading_DeltaN_over_N": "(1+1/kappa)^2/rho^2",
            "leading_scalar_curvature_pole": "-2*(1+1/kappa)^2/rho^2",
            "regularity": "CURVATURE_SINGULAR_ALL_FINITE_KAPPA_POSITIVE",
        },
        {
            "family_id": "F03",
            "cap": "BOTH_ORIGINAL_ROUND_CAPS",
            "lapse_power_in_proper_cap_radius": "F01_power_unchanged_by_smooth_positive_nonzero_Omega",
            "leading_DeltaN_over_N": "F01_pole_plus_finite_conformal_terms",
            "leading_scalar_curvature_pole": "Omega_cap^-2_times_F01_pole",
            "regularity": "CURVATURE_SINGULAR_IF_PHYSICAL_METRIC_RETAINS_BOTH_CAPS",
        },
    ]
    write_tsv(
        "CAP_REGULARITY_LEDGER.tsv",
        [
            "family_id",
            "cap",
            "lapse_power_in_proper_cap_radius",
            "leading_DeltaN_over_N",
            "leading_scalar_curvature_pole",
            "regularity",
        ],
        cap_rows,
    )

    family_rows = [
        {
            "family_id": "F01",
            "classification": "OBSTRUCTED_BOTH_CAPS_CURVATURE_SINGULAR",
            "compact_two_cap_pass": "NO",
            "open_end_status": "NOT_TESTED_IN_THIS_FAMILY",
            "smallest_uncovered_object": "changed_completion_or_distinct_clock_depth",
        },
        {
            "family_id": "F02",
            "classification": "OBSTRUCTED_AT_LEAST_ONE_CAP_ALL_FINITE_POSITIVE_KAPPA",
            "compact_two_cap_pass": "NO",
            "open_end_status": "RETAINED_IN_F04",
            "smallest_uncovered_object": "open_profile_or_nonstatic_nondiagonal_realization",
        },
        {
            "family_id": "F03",
            "classification": "OBSTRUCTED_FOR_SMOOTH_POSITIVE_NONZERO_COMMON_FACTOR",
            "compact_two_cap_pass": "NO",
            "open_end_status": "FACTOR_ZERO_OR_POLE_CHANGES_COMPLETION_AND_REMAINS_OPEN",
            "smallest_uncovered_object": "new_completion_with_full_metric_regularity_proof",
        },
        {
            "family_id": "F04",
            "classification": "OPEN_INFINITE_PROFILE_FAMILY",
            "compact_two_cap_pass": "NO_BY_PRIMITIVE_CAP_ASYMPTOTICS",
            "open_end_status": "OPEN_NO_PROFILE_OR_GLOBAL_DIAMETER_SELECTED",
            "smallest_uncovered_object": "metric_native_profile_and_observer_pairing",
        },
        {
            "family_id": "F05",
            "classification": "REGULAR_CONDITIONAL_CONTROL_ROLES_SEPARATE",
            "compact_two_cap_pass": "YES_SPATIAL_AND_CONSTANT_CLOCK_CONTROL_ONLY",
            "open_end_status": "NOT_APPLICABLE",
            "smallest_uncovered_object": "clock_angular_identity_not_present",
        },
        {
            "family_id": "F06",
            "classification": "OPEN_OUTSIDE_BOUNDED_CLASS",
            "compact_two_cap_pass": "NOT_EVALUATED",
            "open_end_status": "NOT_EVALUATED",
            "smallest_uncovered_object": "complete_shifted_time_live_patchwise_or_pair_space_metric",
        },
    ]
    write_tsv(
        "SOLDER_CLASSIFICATION.tsv",
        [
            "family_id",
            "classification",
            "compact_two_cap_pass",
            "open_end_status",
            "smallest_uncovered_object",
        ],
        family_rows,
    )

    open_rows = [
        {
            "quantity": "lapse",
            "exact_law": "N=C(phi)*exp(-phi)",
            "selected": "NO",
            "consequence": "clock_dilation_requires_endpoint_limit_of_C_exp_minus_phi",
        },
        {
            "quantity": "depth_coframe",
            "exact_law": "A=ell*C(phi)*exp(phi)",
            "selected": "NO",
            "consequence": "Dprime=A",
        },
        {
            "quantity": "clock_depth_ratio",
            "exact_law": "A/N=ell*exp(2phi)",
            "selected": "YES_CONDITIONAL_FIXED_PAIRING",
            "consequence": "profile_C_cancels_from_ratio",
        },
        {
            "quantity": "finite_positive_endpoint",
            "exact_law": "integral_phi0_to_infinity ell*C(phi)*exp(phi)dphi",
            "selected": "NO",
            "consequence": "finite_only_for_integrable_weight",
        },
        {
            "quantity": "angular_global_diameter",
            "exact_law": "requires_R_caps_lattice_and_event_pairing",
            "selected": "NO",
            "consequence": "cannot_promote_depth_endpoint_to_Xmax",
        },
    ]
    write_tsv(
        "OPEN_PROFILE_LEDGER.tsv",
        ["quantity", "exact_law", "selected", "consequence"],
        open_rows,
    )

    status_rows = [
        {
            "claim": "fixed_pairing_diagonal_solder_classification",
            "status": "DERIVED_CONDITIONAL",
            "scope": "static_diagonal_two_reciprocal_planes",
        },
        {
            "claim": "isolated_same_scalar_round_solder",
            "status": "OBSTRUCTED_IN_BOUNDED_CLASS",
            "scope": "both_primitive_round_caps_all_finite_positive_kappa",
        },
        {
            "claim": "double_pair_same_scalar_round_solder",
            "status": "OBSTRUCTED_IN_BOUNDED_CLASS",
            "scope": "at_least_one_cap_all_finite_positive_kappa",
        },
        {
            "claim": "smooth_positive_common_factor_repairs_round_solder",
            "status": "REFUTED_IN_BOUNDED_CLASS",
            "scope": "factor_finite_nonzero_smooth_at_original_caps",
        },
        {
            "claim": "same_scalar_globally_impossible_in_UDT",
            "status": "NOT_DERIVED",
            "scope": "F06_and_changed_completions_open",
        },
        {
            "claim": "open_asymptotic_solder",
            "status": "OPEN_PROFILE_FAMILY",
            "scope": "C_R_profile_and_endpoint_not_selected",
        },
        {
            "claim": "clock_and_angular_phi_must_be_distinct",
            "status": "LEAD_NOT_GLOBAL_THEOREM",
            "scope": "forced_only_for_regular_two_cap_static_diagonal_realization",
        },
        {
            "claim": "global_Xmax",
            "status": "OPEN_NOT_EVALUABLE",
            "scope": "observer_pairing_and_complete_open_profile_absent",
        },
    ]
    write_tsv("STATUS_LEDGER.tsv", ["claim", "status", "scope"], status_rows)

    for row in read_tsv("SOURCE_LINEAGE.tsv"):
        actual = hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest()
        require(f"source_{row['id']}_identity", actual == row["sha256"], checks)

    result = {
        "schema": "udt-clock-angular-solder-regularity-1.0",
        "sympy_version": sp.__version__,
        "check_count": len(checks),
        "checks": checks,
        "family_count": len(family_rows),
        "compact_same_scalar_pass_count": 0,
        "pairing": {
            "generic_weights": "-1,+1,-kappa,+kappa",
            "generic_fixed_pairing_edges": [[0, 1], [2, 3]],
            "kappa_one_extra_pairing_edges": [[0, 3], [1, 2]],
        },
        "round_control": {
            "coordinate": "tan(eta)=exp(2*kappa*phi)",
            "A": "b*kappa*sech(2*kappa*phi)",
            "R": "b/sqrt(2*cosh(2*kappa*phi))",
        },
        "F01": {
            "N": "tan(eta)^(-1/(2*kappa))",
            "scalar_curvature": "6/b^2-2/(b^2*kappa^2*sin(2eta)^2)",
            "minus_cap_power": str(f01_minus_p),
            "plus_cap_power": str(f01_plus_p),
            "two_cap_regular": False,
        },
        "F02": {
            "C": "sech(2*kappa*phi)*exp(-phi)",
            "N": "sech(2*kappa*phi)*exp(-2phi)",
            "scalar_curvature": str(R4_f02),
            "minus_cap_power": str(p_minus),
            "plus_cap_power": str(p_plus),
            "minus_regular_kappa": "1",
            "plus_regular_kappa": "NONE_FINITE_POSITIVE",
            "two_cap_regular": False,
        },
        "F03": {
            "smooth_positive_nonzero_common_factor": "LEADING_F01_POLE_PERSISTS",
            "factor_zero_or_pole": "CHANGES_COMPLETION_OPEN",
        },
        "F04": {
            "B": "exp(-2phi)/(ell^2*C(phi)^2)",
            "Dprime": "ell*C(phi)*exp(phi)",
            "A_over_N": "ell*exp(2phi)",
            "global_diameter": "OPEN",
        },
        "global_ruling": (
            "NO_REGULAR_TWO_PRIMITIVE_CAP_SAME_SCALAR_SOLDER_IN_BOUNDED_STATIC_"
            "DIAGONAL_FIXED_PAIRING_CLASS;OPEN_AND_F06_REALIZATIONS_REMAIN_OPEN"
        ),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"sympy={sp.__version__}")
    print(f"checks={len(checks)}")
    print("families=6")
    print("compact_same_scalar_pass_count=0")
    print(
        "derivation_sha256="
        + hashlib.sha256((HERE / "DERIVATION_RESULT.json").read_bytes()).hexdigest()
    )


if __name__ == "__main__":
    main()
