#!/usr/bin/env python3
"""Build the preregistered macro phi/angular/Xmax extension atlas."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent
BASE = "3ff555b4a48a70067313afef0cf10eba2e17fd49"

SOURCES = [
    "udt_founded_phi_complete_coframe_extension_audit_2026-07-25/EXTENSION_CLASS_LEDGER.tsv",
    "udt_founded_phi_complete_coframe_extension_audit_2026-07-25/AUDIT_REPORT.md",
    "udt_metric_native_observer_separation_asymptote_audit_2026-07-24/EXACT_DERIVATION.md",
    "udt_metric_native_observer_separation_asymptote_audit_2026-07-24/AUDIT_REPORT.md",
    "udt_xmax_observer_separation_audit_2026-07-24/AUDIT_REPORT.md",
    "udt_two_observer_separation_selector_audit_2026-07-24/COMPLETION_DESCENT_ATLAS.tsv",
    "udt_finite_cell_completion_atlas_2026-07-21/COMPLETION_AXIS_SCHEMA.tsv",
    "udt_finite_cell_completion_atlas_2026-07-21/GLOBAL_OUTPUT_ATLAS.tsv",
    "udt_angular_generator_branch_census_2026-07-23/BRANCH_GENERATOR_ATLAS.tsv",
    "udt_angular_generator_branch_census_2026-07-23/BRANCH_UNIVERSE.tsv",
    "udt_global_reciprocal_persistence_selector_audit_2026-07-23/AUDIT_REPORT.md",
]

DIRECTIONS = [
    {
        "direction_id": "D01_ANGULAR_TRACE",
        "generator_slot": "K_TRACE=diag(1,1)",
        "sector": "ANGULAR",
        "founded_pair_effect": "NONE",
        "aligned_local_B_effect": "NONE_EXACT",
        "nonaligned_local_B_effect": "POSSIBLE_IF_DPHI_HAS_ANGULAR_COMPONENT",
        "fixed_rest_spatial_effect": "CHANGES_TRANSVERSE_COMMON_SCALE",
        "four_d_metric_effect": "YES",
    },
    {
        "direction_id": "D02_ANGULAR_RECIPROCAL",
        "generator_slot": "K_RECIP=diag(-1,1)",
        "sector": "ANGULAR",
        "founded_pair_effect": "NONE",
        "aligned_local_B_effect": "NONE_EXACT",
        "nonaligned_local_B_effect": "POSSIBLE_IF_DPHI_HAS_ANGULAR_COMPONENT",
        "fixed_rest_spatial_effect": "CHANGES_TRANSVERSE_SHAPE",
        "four_d_metric_effect": "YES",
    },
    {
        "direction_id": "D03_ANGULAR_SHEAR",
        "generator_slot": "K_12",
        "sector": "ANGULAR",
        "founded_pair_effect": "NONE",
        "aligned_local_B_effect": "NONE_EXACT",
        "nonaligned_local_B_effect": "POSSIBLE_IF_DPHI_HAS_ANGULAR_COMPONENT",
        "fixed_rest_spatial_effect": "CHANGES_TRANSVERSE_SHAPE_AND_AXES",
        "four_d_metric_effect": "YES",
    },
    {
        "direction_id": "D04_MIX_CLOCK_TO_ANGULAR_2",
        "generator_slot": "C_20",
        "sector": "BASE_ANGULAR_MIXING",
        "founded_pair_effect": "NONE",
        "aligned_local_B_effect": "NONE_EXACT",
        "nonaligned_local_B_effect": "NONE_IN_FIXED_FOUNDED_REST_SLICE",
        "fixed_rest_spatial_effect": "NONE_WHEN_THETA_CLOCK_HORIZONTAL",
        "four_d_metric_effect": "YES_CROSS_TERM",
    },
    {
        "direction_id": "D05_MIX_DEPTH_TO_ANGULAR_2",
        "generator_slot": "C_21",
        "sector": "BASE_ANGULAR_MIXING",
        "founded_pair_effect": "NONE",
        "aligned_local_B_effect": "NONE_EXACT",
        "nonaligned_local_B_effect": "POSSIBLE_IF_DPHI_HAS_ANGULAR_COMPONENT",
        "fixed_rest_spatial_effect": "CHANGES_DEPTH_ANGULAR_CROSS_TERM",
        "four_d_metric_effect": "YES_CROSS_TERM",
    },
    {
        "direction_id": "D06_MIX_CLOCK_TO_ANGULAR_3",
        "generator_slot": "C_30",
        "sector": "BASE_ANGULAR_MIXING",
        "founded_pair_effect": "NONE",
        "aligned_local_B_effect": "NONE_EXACT",
        "nonaligned_local_B_effect": "NONE_IN_FIXED_FOUNDED_REST_SLICE",
        "fixed_rest_spatial_effect": "NONE_WHEN_THETA_CLOCK_HORIZONTAL",
        "four_d_metric_effect": "YES_CROSS_TERM",
    },
    {
        "direction_id": "D07_MIX_DEPTH_TO_ANGULAR_3",
        "generator_slot": "C_31",
        "sector": "BASE_ANGULAR_MIXING",
        "founded_pair_effect": "NONE",
        "aligned_local_B_effect": "NONE_EXACT",
        "nonaligned_local_B_effect": "POSSIBLE_IF_DPHI_HAS_ANGULAR_COMPONENT",
        "fixed_rest_spatial_effect": "CHANGES_DEPTH_ANGULAR_CROSS_TERM",
        "four_d_metric_effect": "YES_CROSS_TERM",
    },
]


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def blob_at_base(path: str) -> str:
    return subprocess.check_output(
        ["git", "rev-parse", f"{BASE}:{path}"], cwd=ROOT, text=True
    ).strip()


def source_manifest() -> None:
    rows = []
    for relative in SOURCES:
        path = ROOT / relative
        data = path.read_bytes()
        rows.append(
            {
                "path": relative,
                "git_blob_at_base": blob_at_base(relative),
                "sha256": hashlib.sha256(data).hexdigest(),
                "size_bytes": str(len(data)),
            }
        )
    write_tsv(
        OUT / "INPUT_SOURCE_MANIFEST.tsv",
        rows,
        ["path", "git_blob_at_base", "sha256", "size_bytes"],
    )


def algebra() -> dict[str, object]:
    w, r, t = sp.symbols("w r t", positive=True)
    ell2, ell3, e = sp.symbols("ell2 ell3 e", real=True)
    p, p1, p2, p3 = sp.symbols("p p1 p2 p3", real=True)
    A = sp.Matrix([[w, 0, 0], [ell2, r, e], [ell3, 0, t]])
    h = sp.simplify(A.T * A)
    aligned = sp.Matrix([p, 0, 0])
    general = sp.Matrix([p1, p2, p3])
    B_aligned = sp.factor((aligned.T * h.inv() * aligned)[0])
    coframe_components = sp.simplify(A.T.inv() * general)
    B_general = sp.factor((general.T * h.inv() * general)[0])
    expected_components = sp.Matrix(
        [
            (p1 - ell2 * p2 / r - ell3 * (p3 - e * p2 / r) / t) / w,
            p2 / r,
            (p3 - e * p2 / r) / t,
        ]
    )
    if sp.simplify(B_aligned - p**2 / w**2) != 0:
        raise AssertionError("aligned identity failed")
    if any(sp.simplify(value) != 0 for value in coframe_components - expected_components):
        raise AssertionError("general coframe components failed")
    if sp.simplify(B_general - sum(value**2 for value in expected_components)) != 0:
        raise AssertionError("general B failed")

    # Exact fixed-level controls for phi=x+eps sin(y), evaluated at phi0=log(2).
    eps = sp.Rational(1, 10)
    angular_B_y0 = sp.Rational(1, 4) + eps**2 * 4
    angular_B_ypi2 = sp.Rational(1, 4)
    shift = 2 - 1
    shift_B_y0 = sp.Rational(1, 4) * (1 - shift * eps) ** 2 + eps**2
    shift_B_ypi2 = sp.Rational(1, 4)
    if angular_B_y0 == angular_B_ypi2:
        raise AssertionError("angular non-aligned witness is vacuous")
    if shift_B_y0 == shift_B_ypi2:
        raise AssertionError("shift non-aligned witness is vacuous")

    L, R, Q = sp.Integer(1), sp.Integer(1), sp.Integer(1)
    diameter_sq_a = L**2 + sp.pi**2 * (R**2 + Q**2)
    diameter_sq_b = L**2 + sp.pi**2 * ((2 * R) ** 2 + Q**2)
    if sp.simplify(diameter_sq_b - diameter_sq_a) != 3 * sp.pi**2:
        raise AssertionError("diameter witness failed")

    return {
        "schema": "udt-macro-phi-angular-xmax-algebra-1.0",
        "result": "PASS",
        "sympy_version": sp.__version__,
        "checks": {
            "spatial_metric_positive_chart_determinant": str(sp.factor(h.det())),
            "aligned_B": str(B_aligned),
            "general_coframe_components": [str(value) for value in coframe_components],
            "general_B": str(B_general),
            "angular_fixed_level_B_y0": str(angular_B_y0),
            "angular_fixed_level_B_ypi2": str(angular_B_ypi2),
            "angular_fixed_level_difference": str(sp.factor(angular_B_y0 - angular_B_ypi2)),
            "shift_fixed_level_B_y0": str(shift_B_y0),
            "shift_fixed_level_B_ypi2": str(shift_B_ypi2),
            "shift_fixed_level_difference": str(sp.factor(shift_B_y0 - shift_B_ypi2)),
            "product_diameter_squared_difference": str(3 * sp.pi**2),
        },
        "rulings": {
            "aligned_depth": "ANGULAR_AND_LOWER_MIXING_DIRECTIONS_DO_NOT_CHANGE_LOCAL_B",
            "nonaligned_depth": "ANGULAR_AND_DEPTH_ANGULAR_DIRECTIONS_CAN_CHANGE_B_AND_BREAK_LEVEL_SET_CONSTANCY",
            "clock_angular_mix": "NO_EFFECT_ON_FIXED_FOUNDED_CLOCK_HORIZONTAL_SPATIAL_METRIC",
            "global_distance": "ANGULAR_GEOMETRY_CAN_CHANGE_COMPLETE_CELL_DIAMETER_WITHOUT_CHANGING_ALIGNED_LOCAL_B",
            "selection": "NO_EXTENSION_OR_COMPLETION_SELECTED",
            "xmax": "NOT_DERIVED",
        },
    }


def completion_status(completion: str, direction: str) -> tuple[str, str]:
    angular = direction.startswith(("D01", "D02", "D03"))
    if completion == "FC01_BOUNDARY_BOUNDARY":
        return "OPEN_BOUNDARY_DATA", "boundary_profile_and_identification"
    if completion.startswith(("FC02", "FC03", "FC04", "FC05")):
        requirement = "cap_cycle_smoothness_for_angular_block" if angular else "cap_cycle_smoothness_for_mixing_cocycle"
        return "REGULAR_INTERIOR_ONLY__CAP_DESCENT_OPEN", requirement
    if completion == "FC06_NONPRIMITIVE_CAP":
        return "REGULAR_COMPLEMENT_ONLY__SINGULAR_DESCENT_BLOCKED", "singular_stratum_resolution_or_admissible_completion"
    if completion == "FC07_PERIODIC_TORUS_BUNDLE":
        requirement = "GL2Z_monodromy_centralizer_and_periodic_profile" if angular else "GL2Z_equivariant_mixing_cocycle_and_periodic_profile"
        return "OPEN_MONODROMY_DESCENT", requirement
    if completion == "FC08_MIRROR_DOUBLE":
        return "OPEN_LIFT_PARITY_DESCENT", "chosen_mirror_lift_and_direction_parity"
    if completion == "FC09_NONORIENTABLE_GLUE":
        requirement = "signed_monomial_normalizer_data" if angular else "orientation_twisted_mixing_cocycle"
        return "OPEN_NONORIENTABLE_DESCENT", requirement
    if completion == "FC10_STRATIFIED_PROJECTOR":
        return "STRATUM_LOCAL_ONLY__TRANSITION_OPEN", "rank_transition_extension_data"
    if completion == "FC11_NONINTEGRABLE_DISTRIBUTION":
        return "INSUFFICIENT_COMPLETE_METRIC_DATA", "coframe_connection_and_observer_quotient"
    if completion == "FC12_RECIPROCAL_TORIC_DIAGONAL":
        if direction.startswith(("D01", "D02")):
            return "CONDITIONAL_REGULAR_INTERIOR__ENDPOINT_OPEN", "fixed_integral_T2_basis_and_endpoint_completion"
        if direction.startswith("D03"):
            return "OPEN_ENLARGEMENT_BEYOND_DIAGONAL_BRANCH", "shear_extension_and_endpoint_completion"
        return "OPEN_ENLARGEMENT_BEYOND_BLOCK_DIAGONAL_BRANCH", "mixing_extension_and_endpoint_completion"
    raise AssertionError(completion)


def atlas() -> None:
    branch_rows = read_tsv(
        ROOT / "udt_angular_generator_branch_census_2026-07-23/BRANCH_UNIVERSE.tsv"
    )
    descent_rows = read_tsv(
        ROOT / "udt_two_observer_separation_selector_audit_2026-07-24/COMPLETION_DESCENT_ATLAS.tsv"
    )
    completions = [row["completion_id"] for row in branch_rows]
    if len(completions) != 12 or len(set(completions)) != 12:
        raise AssertionError("completion universe is not exactly twelve unique rows")
    if set(completions) != {row["completion"] for row in descent_rows}:
        raise AssertionError("completion sources disagree")

    write_tsv(
        OUT / "EXTENSION_DIRECTION_LEDGER.tsv",
        DIRECTIONS,
        list(DIRECTIONS[0]),
    )

    rows: list[dict[str, str]] = []
    for completion in completions:
        for direction in DIRECTIONS:
            direction_id = direction["direction_id"]
            global_status, unresolved = completion_status(completion, direction_id)
            if direction_id.startswith(("D04", "D06")):
                global_distance = "NO_EFFECT_IN_FIXED_FOUNDED_REST_SLICE__OTHER_OBSERVER_COMPARISON_OPEN"
            else:
                global_distance = "POSSIBLE_IF_GLOBAL_EXTENSION_DESCENDS"
            rows.append(
                {
                    "completion_id": completion,
                    "direction_id": direction_id,
                    "sector": direction["sector"],
                    "aligned_local_B_effect": direction["aligned_local_B_effect"],
                    "nonaligned_local_B_effect": direction["nonaligned_local_B_effect"],
                    "global_observer_rest_distance_effect": global_distance,
                    "global_descent_status": global_status,
                    "unresolved_requirement": unresolved,
                    "selection_status": "NOT_SELECTED",
                    "xmax_consequence": "DOES_NOT_SELECT_FINITE_OR_NUMERICAL_XMAX",
                    "evidence": (
                        "udt_angular_generator_branch_census_2026-07-23/BRANCH_GENERATOR_ATLAS.tsv:"
                        + completion
                        + ";udt_two_observer_separation_selector_audit_2026-07-24/COMPLETION_DESCENT_ATLAS.tsv:"
                        + completion
                    ),
                }
            )
    if len(rows) != 84 or len({(r["completion_id"], r["direction_id"]) for r in rows}) != 84:
        raise AssertionError("atlas cross product failed")
    write_tsv(OUT / "BRANCH_EXTENSION_ATLAS.tsv", rows, list(rows[0]))

    channels = [
        {
            "channel_id": "M01_ALIGNED_LOCAL_DEPTH",
            "condition": "dphi_has_only_founded_depth_component_on_clock_horizontal_slice",
            "metric_result": "B=(p/w)^2",
            "angular_role": "NO_LOCAL_B_MODULATION",
            "status": "DERIVED_EXACT_BOUNDED",
            "xmax_role": "RADIAL_REACH_STILL_REQUIRES_PROFILE_p_over_w",
        },
        {
            "channel_id": "M02_NONALIGNED_LOCAL_DEPTH",
            "condition": "dphi_has_angular_component",
            "metric_result": "B_contains_angular_inverse_metric_and_depth_angular_shift_terms",
            "angular_role": "CAN_MODULATE_B_AND_BREAK_TRANSNORMALITY",
            "status": "DERIVED_POSSIBILITY_WITH_EXACT_COUNTERWITNESSES",
            "xmax_role": "ONE_SCALAR_D_OF_PHI_CAN_FAIL",
        },
        {
            "channel_id": "M03_TRANSVERSE_GLOBAL_DISTANCE",
            "condition": "global_angular_extension_descends_and_cell_distance_is_defined",
            "metric_result": "same_aligned_B_can_coexist_with_different_complete_cell_diameter",
            "angular_role": "CAN_MODULATE_GLOBAL_OBSERVER_PAIR_DISTANCE",
            "status": "DERIVED_CONDITIONAL_WITNESS",
            "xmax_role": "DIRECTIONAL_OR_DIAMETER_VARIATION_POSSIBLE_NOT_SELECTED",
        },
        {
            "channel_id": "M04_CLOCK_ANGULAR_FOUR_D_MIX",
            "condition": "fixed_founded_clock_horizontal_rest_slice",
            "metric_result": "clock_angular_lower_entries_drop_out_of_induced_spatial_metric",
            "angular_role": "FOUR_D_CROSS_TERM_ONLY_IN_THIS_FRAME",
            "status": "DERIVED_EXACT_BOUNDED",
            "xmax_role": "OTHER_OBSERVER_OR_CAUSAL_COMPARISON_REMAINS_OPEN",
        },
        {
            "channel_id": "M05_SCALAR_FEEDBACK",
            "condition": "equation_selecting_phi_profile_or_extension",
            "metric_result": "not_supplied_by_pointwise_extension_or_completion_atlas",
            "angular_role": "NO_NATIVE_FEEDBACK_LAW_DERIVED",
            "status": "OPEN",
            "xmax_role": "NO_FINITE_OR_NUMERICAL_XMAX_SELECTED",
        },
    ]
    write_tsv(OUT / "MODULATION_CHANNEL_LEDGER.tsv", channels, list(channels[0]))


def main() -> None:
    source_manifest()
    result = algebra()
    (OUT / "ALGEBRA_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    atlas()
    print(json.dumps({"result": "PASS", "atlas_rows": 84, "directions": 7, "completions": 12, "sympy": sp.__version__}, sort_keys=True))


if __name__ == "__main__":
    main()
