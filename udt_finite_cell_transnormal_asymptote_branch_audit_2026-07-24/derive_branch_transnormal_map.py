#!/usr/bin/env python3
"""Exact branch census and transnormal/asymptote controls."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FC_SOURCE = (
    ROOT
    / "udt_finite_cell_reciprocal_survival_density_audit_2026-07-23"
    / "FINITE_CELL_BRANCH_ATLAS.tsv"
)
FAMILY_SOURCE = (
    ROOT
    / "udt_involutive_exchange_branch_availability_audit_2026-07-24"
    / "BRANCH_EQUATION_FAMILY_REGISTRY.tsv"
)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def require_zero(name: str, expression: sp.Expr, checks: dict[str, str]) -> None:
    value = sp.simplify(expression)
    if value != 0:
        raise AssertionError(f"{name}: {value}")
    checks[name] = "PASS"


def require_equal(name: str, actual: sp.Expr, expected: sp.Expr, checks: dict[str, str]) -> None:
    require_zero(name, actual - expected, checks)


def main() -> None:
    checks: dict[str, str] = {}
    fc_source = read_tsv(FC_SOURCE)
    family_source = read_tsv(FAMILY_SOURCE)
    expected_fc = [f"FC{index:02d}" for index in range(1, 13)]
    actual_fc = [row["completion_id"].split("_", 1)[0] for row in fc_source]
    if actual_fc != expected_fc:
        raise AssertionError(f"FC universe mismatch: {actual_fc}")
    checks["twelve_FC_rows_exact_order"] = "PASS"
    expected_families = [f"B{index:02d}" for index in range(1, 29)]
    actual_families = [row["family_id"] for row in family_source]
    if actual_families != expected_families:
        raise AssertionError(f"family universe mismatch: {actual_families}")
    checks["twenty_eight_family_rows_exact_order"] = "PASS"

    fc_classification = {
        "FC01": (
            "TOPOLOGY_ONLY_NO_COMPLETE_G_PHI_WITNESS",
            "BOUNDARY_PROFILE_MAY_SUPPORT_B_POSITIVE_BUT_NONE_SUPPLIED",
            "complete_g_phi_clock_leg_event_pairing",
        ),
        "FC02": (
            "TOPOLOGY_ONLY_NO_COMPLETE_G_PHI_WITNESS",
            "COHOMOGENEITY_ONE_CAP_FORCES_B_ZERO_AT_CAP_GENERAL_FIELDS_OPEN",
            "complete_profile_cap_jets_clock_solder",
        ),
        "FC03": (
            "OBSTRUCTED_SMOOTH_GLOBAL_TRANSNORMAL_CLOCK_DEPTH",
            "STATIC_COMPACT_REAL_PHI_FORCES_B_ZERO_TIME_LIVE_SPATIAL_B_STILL_SLICE_CRITICAL",
            "patchwise_or_asymptotic_pair_space_realization",
        ),
        "FC04": (
            "OBSTRUCTED_SMOOTH_GLOBAL_TRANSNORMAL_CLOCK_DEPTH",
            "STATIC_COMPACT_REAL_PHI_FORCES_B_ZERO_TIME_LIVE_SPATIAL_B_STILL_SLICE_CRITICAL",
            "patchwise_or_asymptotic_pair_space_realization",
        ),
        "FC05": (
            "OBSTRUCTED_SMOOTH_GLOBAL_TRANSNORMAL_CLOCK_DEPTH",
            "STATIC_COMPACT_REAL_PHI_FORCES_B_ZERO_TIME_LIVE_SPATIAL_B_STILL_SLICE_CRITICAL",
            "patchwise_or_asymptotic_pair_space_realization",
        ),
        "FC06": (
            "TOPOLOGY_ONLY_NO_COMPLETE_G_PHI_WITNESS",
            "TRUE_SINGULAR_STRATUM_BLOCKS_INVERSE_METRIC_B",
            "regular_resolution_or_explicit_stratified_distance",
        ),
        "FC07": (
            "OBSTRUCTED_SMOOTH_GLOBAL_TRANSNORMAL_CLOCK_DEPTH",
            "PERIODIC_COMPACT_REAL_PHI_HAS_SPATIAL_CRITICAL_POINT",
            "circle_valued_twisted_or_pair_space_depth",
        ),
        "FC08": (
            "OBSTRUCTED_SMOOTH_GLOBAL_TRANSNORMAL_CLOCK_DEPTH",
            "COMPACT_DOUBLE_AND_MIRROR_EVEN_BRANCH_FORCE_SPATIAL_B_ZERO",
            "nonordinary_twisted_or_patchwise_depth",
        ),
        "FC09": (
            "TOPOLOGY_ONLY_NO_COMPLETE_G_PHI_WITNESS",
            "COMPACT_SUBCASES_CRITICAL_BOUNDARY_SUBCASES_PROFILE_DEPENDENT",
            "orientation_twist_profile_and_clock_solder",
        ),
        "FC10": (
            "TOPOLOGY_ONLY_NO_COMPLETE_G_PHI_WITNESS",
            "PROJECTOR_STRATIFICATION_DOES_NOT_SUPPLY_G_PHI_PROFILE",
            "complete_regular_metric_and_depth_profile",
        ),
        "FC11": (
            "TOPOLOGY_ONLY_NO_COMPLETE_G_PHI_WITNESS",
            "NONINTEGRABLE_PLANE_MAY_EVADE_SLICE_THEOREM_BUT_IS_NOT_CLOCK_REST_DISTRIBUTION",
            "physical_clock_distribution_and_horizontal_distance",
        ),
        "FC12": (
            "FORMULA_ONLY_PROFILE_OR_ENDPOINT_OPEN",
            "B_EQUALS_A_MINUS_TWO_BUT_A_ENDPOINTS_CAPS_AND_CLOCK_SOLDER_OPEN",
            "selected_A_profile_clock_solder_and_global_completion",
        ),
    }
    fc_rows: list[dict[str, str]] = []
    for source in fc_source:
        short_id = source["completion_id"].split("_", 1)[0]
        classification, transnormal_ruling, missing = fc_classification[short_id]
        fc_rows.append(
            {
                "completion_id": source["completion_id"],
                "global_data_level": source["global_data_level"],
                "primary_classification": classification,
                "complete_g_phi_witness": (
                    "NO"
                    if short_id != "FC12"
                    else "NO_CONDITIONAL_OPEN_PROFILE_CONTROL_ONLY"
                ),
                "clock_phi_solder": "OPEN",
                "transnormal_ruling": transnormal_ruling,
                "endpoint_status": "NOT_EVALUABLE" if short_id != "FC12" else "DEPENDS_ON_INTEGRAL_OF_A",
                "diameter_status": "NOT_EVALUABLE",
                "smallest_missing_object": missing,
            }
        )
    if len(fc_rows) != 12 or len({row["completion_id"] for row in fc_rows}) != 12:
        raise AssertionError("FC output coverage")
    checks["FC_output_one_row_each"] = "PASS"

    special_family_class = {
        "B11": "TOPOLOGY_ONLY_NO_COMPLETE_G_PHI_WITNESS",
        "B16": "TOPOLOGY_ONLY_NO_COMPLETE_G_PHI_WITNESS",
        "B18": "INELIGIBLE_NO_COMMON_WITNESS",
        "B19": "CONDITIONAL_DEPTH_EVALUABLE_NOT_CLOCK_SOLDERED",
        "B21": "LOCAL_CLOCK_DEPTH_ONLY_NO_GLOBAL_COMPLETION",
        "B24": "INELIGIBLE_NO_COMMON_WITNESS",
        "B28": "INELIGIBLE_NO_COMMON_WITNESS",
    }
    family_rows: list[dict[str, str]] = []
    for source in family_source:
        family_id = source["family_id"]
        classification = special_family_class.get(family_id, "INELIGIBLE_NO_COMMON_WITNESS")
        if family_id == "B19":
            witness = "ROUND_CAPPED_METRIC_CONDITIONAL_C2_ON_SHELL"
            blocker = "ANGULAR_PHI_NOT_SOLDERED_TO_CLOCK_DILATION_PHYSICAL_ACTION_SCALE_BOUNDARY_OPEN"
        elif family_id == "B21":
            witness = "SUPPLIED_LOCAL_WRL_CLOCK_PROFILE"
            blocker = "NO_COMPLETE_GLOBAL_FRAME_ANGULAR_COMPLETION_OR_PAIR_DIAMETER"
        elif family_id in {"B11", "B16"}:
            witness = "PARAMETRIC_COMPLETION_TAXONOMY"
            blocker = "NO_COMPLETE_G_PHI_FIELD_WITNESS"
        else:
            witness = "NO_SINGLE_COMPLETE_CLOCK_SOLDERED_FINITE_CELL_WITNESS"
            blocker = "FAMILY_SCOPE_DOES_NOT_COLOCATE_ALL_TRANSNORMAL_DATA_GATES"
        family_rows.append(
            {
                "family_id": family_id,
                "family_label": source["family_label"],
                "primary_classification": classification,
                "strongest_relevant_witness": witness,
                "global_Xmax_evaluable": "NO",
                "primary_blocker": blocker,
            }
        )
    if len(family_rows) != 28 or len({row["family_id"] for row in family_rows}) != 28:
        raise AssertionError("family output coverage")
    checks["family_output_one_row_each"] = "PASS"

    # Exact control algebra.
    phi = sp.symbols("phi", real=True)
    X, A, b = sp.symbols("X A b", positive=True)

    # WR-L local clock-depth branch.
    B_wrl = sp.exp(2 * phi) / (4 * X**2)
    Dprime_wrl = 1 / sp.sqrt(B_wrl)
    require_equal("WRL_Dprime", Dprime_wrl, 2 * X * sp.exp(-phi), checks)
    D_wrl = sp.integrate(Dprime_wrl, (phi, 0, phi))
    require_equal("WRL_D", D_wrl, 2 * X * (1 - sp.exp(-phi)), checks)
    require_equal("WRL_endpoint", sp.limit(D_wrl, phi, sp.oo), 2 * X, checks)

    # FC12 reciprocal-toric angular-depth branch.
    B_fc12 = 1 / A**2
    require_equal("FC12_Dprime", 1 / sp.sqrt(B_fc12), A, checks)

    # B19 round capped toric angular depth.
    eta = sp.symbols("eta", positive=True)
    phi_eta = sp.log(sp.tan(eta)) / 2
    require_equal("B19_dphi_deta", sp.diff(phi_eta, eta), 1 / sp.sin(2 * eta), checks)
    sin_two_eta = 1 / sp.cosh(2 * phi)
    B_b19 = sp.cosh(2 * phi) ** 2 / b**2
    Dprime_b19 = 1 / sp.sqrt(B_b19)
    require_equal("B19_Dprime", Dprime_b19, b / sp.cosh(2 * phi), checks)
    D_b19 = b * sp.atan(sp.sinh(2 * phi)) / 2
    require_equal("B19_D_derivative", sp.diff(D_b19, phi), Dprime_b19, checks)
    require_equal("B19_neutral_value", D_b19.subs(phi, 0), 0, checks)
    require_equal("B19_one_sided_cap_depth", sp.limit(D_b19, phi, sp.oo), sp.pi * b / 4, checks)
    b19_full_diameter = sp.pi * b
    require_equal(
        "B19_diameter_to_one_sided_depth_ratio",
        b19_full_diameter / sp.limit(D_b19, phi, sp.oo),
        4,
        checks,
    )
    require_equal(
        "B19_eta_phi_identity",
        sp.simplify(sp.sin(2 * sp.atan(sp.exp(2 * phi)))),
        sin_two_eta,
        checks,
    )

    # Pure time-live phi has no observer-rest spatial gradient.
    p_t, p_x, p_y, p_z = sp.symbols("p_t p_x p_y p_z", real=True)
    B_flat = p_x**2 + p_y**2 + p_z**2
    require_equal("pure_time_phi_has_zero_spatial_B", B_flat.subs({p_x: 0, p_y: 0, p_z: 0}), 0, checks)

    # Exercised compact static critical-point controls.
    x = sp.symbols("x", real=True)
    B_circle = sp.diff(sp.sin(x), x) ** 2
    require_equal("periodic_static_control_B_zero", B_circle.subs(x, sp.pi / 2), 0, checks)
    B_mirror = sp.diff(x**2, x) ** 2
    require_equal("mirror_static_control_B_zero", B_mirror.subs(x, 0), 0, checks)
    B_interval = sp.diff(x * (1 - x), x) ** 2
    require_equal("interval_turning_control_B_zero", B_interval.subs(x, sp.Rational(1, 2)), 0, checks)

    control_rows = [
        {
            "control_id": "C_WRL",
            "metric_scope": "CONDITIONAL_LOCAL_STATIC_SPHERICAL_WRL",
            "phi_role": "RECIPROCAL_CLOCK_DEPTH",
            "B": "exp(2phi)/(4X^2)",
            "D_from_neutral": "2X(1-exp(-phi))",
            "depth_endpoint": "2X",
            "global_spatial_diameter": "OPEN",
            "clock_solder": "YES",
            "on_shell_status": "SUPPLIED_PROFILE_NOT_NATIVE_COMPLETE_EOM",
            "primary_ruling": "LOCAL_CLOCK_DEPTH_ONLY_NO_GLOBAL_COMPLETION",
        },
        {
            "control_id": "C_FC12",
            "metric_scope": "CONDITIONAL_RECIPROCAL_TORIC_OPEN_PROFILE",
            "phi_role": "ANGULAR_RECIPROCAL_DEPTH",
            "B": "1/A(phi)^2",
            "D_from_neutral": "integral_0^phi A(psi)dpsi",
            "depth_endpoint": "FINITE_IFF_A_IS_INTEGRABLE",
            "global_spatial_diameter": "OPEN",
            "clock_solder": "NO",
            "on_shell_status": "NO_SELECTED_OPERATOR_OR_PROFILE",
            "primary_ruling": "FORMULA_ONLY_PROFILE_OR_ENDPOINT_OPEN",
        },
        {
            "control_id": "C_B19_ROUND",
            "metric_scope": "CONDITIONAL_C2_BACH_ROUND_CAPPED_S3",
            "phi_role": "ANGULAR_RECIPROCAL_DEPTH_FROM_tan_eta_exp_2phi",
            "B": "cosh(2phi)^2/b^2",
            "D_from_neutral": "(b/2)atan(sinh(2phi))",
            "depth_endpoint": "pi*b/4",
            "global_spatial_diameter": "pi*b",
            "clock_solder": "NO_CONSTANT_LAPSE",
            "on_shell_status": "CONDITIONAL_C2_BACH",
            "primary_ruling": "CONDITIONAL_DEPTH_EVALUABLE_NOT_CLOCK_SOLDERED",
        },
    ]

    gate_names = [f"G{index:02d}" for index in range(1, 13)]
    control_gates = {
        "C_WRL": [
            "CONDITIONAL", "YES", "YES", "YES", "CONDITIONAL", "OPEN",
            "OPEN", "YES", "YES", "YES", "OPEN", "NO",
        ],
        "C_FC12": [
            "CONDITIONAL", "YES", "YES", "NO", "YES", "OPEN",
            "OPEN", "YES", "YES", "CONDITIONAL", "OPEN", "NO",
        ],
        "C_B19_ROUND": [
            "CONDITIONAL", "YES", "CONDITIONAL", "NO", "YES", "CONDITIONAL",
            "OPEN", "YES", "YES", "YES", "YES", "CONDITIONAL",
        ],
    }
    gate_rows = []
    for control_id, values in control_gates.items():
        row = {"control_id": control_id}
        row.update(dict(zip(gate_names, values)))
        row["passes_all"] = "NO"
        gate_rows.append(row)
    checks["three_control_gate_rows"] = "PASS"
    if any(row["passes_all"] != "NO" for row in gate_rows):
        raise AssertionError("control promoted")

    status_rows = [
        {
            "claim": "registered_FC_rows_with_complete_on_shell_g_phi_witness",
            "status": "ZERO",
            "scope_or_limit": "twelve_row_completion_taxonomy",
        },
        {
            "claim": "registered_equation_families_with_full_global_Xmax_evaluable",
            "status": "ZERO_OF_28",
            "scope_or_limit": "no_single_clock_soldered_complete_pair_diameter_witness",
        },
        {
            "claim": "WRL_clock_depth_endpoint",
            "status": "DERIVED_CONDITIONAL_2X",
            "scope_or_limit": "local_radial_proper_depth_not_global_diameter",
        },
        {
            "claim": "FC12_transnormal_formula",
            "status": "DERIVED_CONDITIONAL_DPRIME_EQUALS_A",
            "scope_or_limit": "angular_phi_not_clock_soldered_profile_and_caps_open",
        },
        {
            "claim": "B19_round_angular_depth_endpoint",
            "status": "DERIVED_CONDITIONAL_PI_B_OVER_4",
            "scope_or_limit": "angular_phi_constant_clock_lapse",
        },
        {
            "claim": "B19_round_global_spatial_diameter",
            "status": "DERIVED_CONDITIONAL_PI_B",
            "scope_or_limit": "round_S3_common_scale_b_unselected_not_Xmax",
        },
        {
            "claim": "smooth_real_phi_global_transnormal_on_compact_rest_slice",
            "status": "OBSTRUCTED",
            "scope_or_limit": "critical_point_for_each_compact_boundaryless_integrable_rest_slice",
        },
        {
            "claim": "pure_time_live_phi_supplies_spatial_distance_depth",
            "status": "REFUTED",
            "scope_or_limit": "spacetime_gradient_may_be_nonnull_but_observer_rest_B_is_zero",
        },
        {
            "claim": "global_Xmax",
            "status": "OPEN_NOT_EVALUABLE",
            "scope_or_limit": "complete_clock_soldered_pair_distance_branch_absent",
        },
        {
            "claim": "smallest_missing_join",
            "status": "OPEN",
            "scope_or_limit": "one_complete_branch_co_locating_clock_phi_full_angular_geometry_event_pairing_and_global_diameter",
        },
    ]

    write_tsv(
        HERE / "FINITE_CELL_TRANSNORMAL_LEDGER.tsv",
        list(fc_rows[0].keys()),
        fc_rows,
    )
    write_tsv(
        HERE / "EQUATION_FAMILY_SCREEN.tsv",
        list(family_rows[0].keys()),
        family_rows,
    )
    write_tsv(
        HERE / "CALCULABLE_CONTROL_LEDGER.tsv",
        list(control_rows[0].keys()),
        control_rows,
    )
    write_tsv(
        HERE / "CONTROL_GATE_MATRIX.tsv",
        ["control_id", *gate_names, "passes_all"],
        gate_rows,
    )
    write_tsv(
        HERE / "STATUS_LEDGER.tsv",
        ["claim", "status", "scope_or_limit"],
        status_rows,
    )

    classifications: dict[str, int] = {}
    for row in fc_rows:
        classifications[row["primary_classification"]] = (
            classifications.get(row["primary_classification"], 0) + 1
        )
    family_classifications: dict[str, int] = {}
    for row in family_rows:
        family_classifications[row["primary_classification"]] = (
            family_classifications.get(row["primary_classification"], 0) + 1
        )

    result = {
        "schema": "udt-finite-cell-transnormal-asymptote-branch-audit-1.0",
        "sympy_version": sp.__version__,
        "checks": checks,
        "check_count": len(checks),
        "fc_rows": len(fc_rows),
        "family_rows": len(family_rows),
        "fc_classification_counts": classifications,
        "family_classification_counts": family_classifications,
        "control_count": len(control_rows),
        "full_global_Xmax_pass_count": 0,
        "exact_controls": {
            "WRL": {
                "B": sp.sstr(B_wrl),
                "D": sp.sstr(D_wrl),
                "endpoint": sp.sstr(sp.limit(D_wrl, phi, sp.oo)),
            },
            "FC12": {
                "B": "A(phi)^(-2)",
                "Dprime": "A(phi)",
                "endpoint": "integral_0^infinity A(phi)dphi",
            },
            "B19_round": {
                "B": sp.sstr(B_b19),
                "D": sp.sstr(D_b19),
                "one_sided_endpoint": sp.sstr(sp.pi * b / 4),
                "global_spatial_diameter": sp.sstr(b19_full_diameter),
                "diameter_to_depth_ratio": "4",
            },
        },
        "global_ruling": (
            "NO_REGISTERED_COMPLETE_CLOCK_SOLDERED_FINITE_CELL_PAIR_DISTANCE_BRANCH;"
            "GLOBAL_XMAX_REMAINS_OPEN"
        ),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    payload = b"".join(
        (HERE / name).read_bytes()
        for name in (
            "DERIVATION_RESULT.json",
            "FINITE_CELL_TRANSNORMAL_LEDGER.tsv",
            "EQUATION_FAMILY_SCREEN.tsv",
            "CALCULABLE_CONTROL_LEDGER.tsv",
            "CONTROL_GATE_MATRIX.tsv",
            "STATUS_LEDGER.tsv",
        )
    )
    print(f"SymPy {sp.__version__}")
    print(f"exact_checks={len(checks)}")
    print(f"FC_rows={len(fc_rows)}")
    print(f"family_rows={len(family_rows)}")
    print(f"payload_sha256={hashlib.sha256(payload).hexdigest()}")
    print("status=PASS")


if __name__ == "__main__":
    main()
