#!/usr/bin/env python3
"""Join the exact geometry and invariant certificates without promoting physics."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(name: str, fields: list[str], rows: list[dict[str, str]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    candidates = read_tsv("CANDIDATE_UNIVERSE.tsv")
    geometry = {row["candidate_id"]: row for row in read_tsv("GEOMETRIC_ATLAS.tsv")}
    invariants = json.loads((HERE / "INVARIANT_CERTIFICATE.json").read_text(encoding="utf-8"))
    curvature = {row["candidate_id"]: row for row in invariants["candidate_results"]}
    expected_ids = [f"C{i:02d}" for i in range(1, 19)]
    assert [row["candidate_id"] for row in candidates] == expected_ids
    assert list(geometry) == expected_ids
    assert list(curvature) == expected_ids

    rows = []
    for candidate in candidates:
        candidate_id = candidate["candidate_id"]
        geom = geometry[candidate_id]
        curve = curvature[candidate_id]
        if candidate_id == "C18":
            killing_line = "UNDEFINED_METRIC_DEGENERATE"
            twist_line = "UNDEFINED_METRIC_DEGENERATE"
            pair_projector = "BLOCKED_METRIC_DEGENERATE"
            conclusion = "DEGENERATE_CONTROL_RETAINED"
        elif candidate_id == "C14":
            killing_line = "NOT_UNIQUE_SYMMETRY_ENHANCED"
            twist_line = "DISPLAYED_TWIST_EXISTS_BUT_NOT_UNIQUELY_OWNED"
            pair_projector = "BLOCKED_UNIQUE_KILLING_LINE_ABSENT"
            conclusion = "SYMMETRY_ENHANCED_CONTROL_RETAINED"
        else:
            assert curve["jacobian_nonzero_at_any_registered_point"]
            killing_line = "UNIQUE_TIMELIKE_KILLING_LINE_DENSE_OPEN"
            if int(candidate["a"]) == 0:
                twist_line = "ZERO"
                pair_projector = "BLOCKED_TWIST_LINE_ABSENT"
                conclusion = "UNIQUE_CLOCK_LINE_BUT_NO_INTRINSIC_PAIR"
            else:
                twist_line = "NONZERO_KILLING_TWIST_LINE"
                pair_projector = "METRIC_INTRINSIC_ON_REGISTERED_BRANCH"
                if geom["configuration_alternating_class"].startswith("NONZERO_SIMPLE"):
                    conclusion = "INTRINSIC_PROJECTOR_AND_NONZERO_ALTERNATING_COEXIST"
                else:
                    conclusion = "INTRINSIC_PROJECTOR_AND_ZERO_ALTERNATING_COEXIST"
        if pair_projector == "METRIC_INTRINSIC_ON_REGISTERED_BRANCH":
            intrinsic_alternating = geom["configuration_alternating_class"]
        elif candidate_id == "C18":
            intrinsic_alternating = "UNDEFINED_METRIC_DEGENERATE"
        elif candidate_id == "C14":
            intrinsic_alternating = "BLOCKED_PAIR_PROJECTOR_NOT_INTRINSIC"
        else:
            assert candidate_id == "C15"
            intrinsic_alternating = "BLOCKED_TWIST_LINE_ABSENT"
        rows.append({
            "candidate_id": candidate_id,
            "label": candidate["label"],
            "screen_modes_active": geom["screen_modes_active"],
            "four_metric_status": geom["four_metric_status"],
            "curvature_status": curve["curvature_status"],
            "killing_line_status": killing_line,
            "twist_line_status": twist_line,
            "pair_projector_status": pair_projector,
            "configuration_alternating_class": geom["configuration_alternating_class"],
            "intrinsic_contact_alternating_status": intrinsic_alternating,
            "causal_strata": geom["causal_strata"],
            "maximum_candidate_conclusion": conclusion,
        })

    fields = [
        "candidate_id", "label", "screen_modes_active", "four_metric_status", "curvature_status",
        "killing_line_status", "twist_line_status", "pair_projector_status",
        "configuration_alternating_class", "intrinsic_contact_alternating_status", "causal_strata",
        "maximum_candidate_conclusion",
    ]
    write_tsv("RESULT_ATLAS.tsv", fields, rows)

    unique_killing = [row["candidate_id"] for row in rows if row["killing_line_status"].startswith("UNIQUE_")]
    intrinsic_pair = [row["candidate_id"] for row in rows if row["pair_projector_status"].startswith("METRIC_")]
    intrinsic_nonzero = [
        row["candidate_id"] for row in rows
        if row["pair_projector_status"].startswith("METRIC_")
        and row["intrinsic_contact_alternating_status"].startswith("NONZERO_SIMPLE")
    ]
    full_primary = [candidate_id for candidate_id in ("C08", "C09", "C10") if candidate_id in intrinsic_nonzero]
    assert len(unique_killing) == 16
    assert len(intrinsic_pair) == 15
    assert len(intrinsic_nonzero) == 6
    assert full_primary == ["C08", "C09", "C10"]

    post_repair_path = HERE / "POST_REPAIR_RECHECK_RESULT.json"
    if post_repair_path.is_file():
        post_repair = json.loads(post_repair_path.read_text(encoding="utf-8"))
        assert post_repair["grade"] == "PASS" and post_repair["blocking_corrections_remaining"] == 0
        final_status = "PASS_VERIFIED_FRESH_COLD_REVIEW"
        four_gates = "PASS_ALL_FOUR_FOR_BOUNDED_CONFIGURATION_EXISTENCE"
    else:
        post_repair = None
        final_status = "EXACT_PRODUCTION_COMPLETE__INDEPENDENT_REVIEW_PENDING"
        four_gates = "PENDING_INDEPENDENT_REVIEW"

    status_rows = [
        {"claim_id": "S01", "object": "general_positive_screen_metric", "status": "DERIVED_CONFIGURATION_SPACE", "exact_scope": "area_plus_two_shears_on_registered_stationary_S3_family", "open_scope": "dynamics_selection_and_full_function_space"},
        {"claim_id": "S02", "object": "screen_and_pair_determinants", "status": "DERIVED_EXACT", "exact_scope": "det_shape_1_det_screen_u_2lambda_V2_det_pair_minus1", "open_scope": "none_inside_registered_coframe"},
        {"claim_id": "S03", "object": "unique_timelike_Killing_line", "status": "DERIVED_DENSE_OPEN_FOR_16_REGISTERED_METRICS", "exact_scope": "nonzero_R_Ric2_Ric3_Jacobian_at_both_registered_points", "open_scope": "unregistered_metrics_and_C14_symmetry_control"},
        {"claim_id": "S04", "object": "intrinsic_pair_projector", "status": "DERIVED_ON_15_REGISTERED_METRICS", "exact_scope": "unique_clock_line_plus_nonzero_metric_twist_line", "open_scope": "C14_C15_C18_and_unregistered_branches"},
        {"claim_id": "S05", "object": "registered_configuration_depth_area_form", "status": "MIXED_ZERO_AND_NONZERO", "exact_scope": "10_zero_7_nonzero_decomposable_1_degenerate_before_projector_gate", "open_scope": "global_zero_loci_and_general_profiles"},
        {"claim_id": "S06", "object": "intrinsic_nonzero_coexistence", "status": "DERIVED_EXISTENCE_FOR_6_REGISTERED_METRICS", "exact_scope": "C04_C08_C09_C10_C16_C17", "open_scope": "selection_equation_and_physical_role"},
        {"claim_id": "S07", "object": "full_screen_primary_coexistence", "status": "DERIVED_EXPLICIT_FOR_ALL_3_REGISTERED_LAMBDA", "exact_scope": "C08_C09_C10_epsilon_one_tenth", "open_scope": "arbitrary_lambda_profiles_and_on_shell_status"},
        {"claim_id": "S08", "object": "open_neighborhood_existence", "status": "DERIVED_CONDITIONAL_ON_STANDARD_C3_CONTINUITY", "exact_scope": "some_unquantified_neighborhood_of_each_parent_lambda_relative_to_stationary_block_screen_subspace_retaining_K", "open_scope": "arbitrary_C3_perturbations_radius_global_component_and_dynamics"},
        {"claim_id": "S09", "object": "homogeneous_twistfree_and_degenerate_controls", "status": "DERIVED_DISTINCT_FAILURE_STRATA", "exact_scope": "C14_C15_C18", "open_scope": "other_failure_strata"},
        {"claim_id": "S10", "object": "registered_causal_strata", "status": "DERIVED_EXACT", "exact_scope": "a1_positive_a4_endpoint_null_a5_sign_change", "open_scope": "physical_acceptance_or_selection"},
        {"claim_id": "S11", "object": "screen_or_branch_selection", "status": "OPEN_NOT_SUPPLIED", "exact_scope": "configuration_atlas_only", "open_scope": "native_equation_action_boundary_source_bootstrap"},
        {"claim_id": "S12", "object": "downstream_physics", "status": "OPEN_EXCLUDED", "exact_scope": "none", "open_scope": "carrier_matter_mass_stability_Xmax_phenomenology"},
    ]
    write_tsv(
        "STATUS_LEDGER.tsv",
        ["claim_id", "object", "status", "exact_scope", "open_scope"],
        status_rows,
    )

    result = {
        "schema": "udt-intrinsic-general-screen-adjudication-1.0",
        "status": final_status,
        "headline": "INTRINSIC_RECIPROCAL_PROJECTOR_AND_INDEPENDENT_ANGULAR_AREA_RESPONSE_COEXIST_ON_EXPLICIT_COMPLETE_STATIONARY_SCREENS__SELECTION_OPEN",
        "four_gates": four_gates,
        "post_repair_review_grade": post_repair["grade"] if post_repair else "PENDING",
        "candidate_count": len(rows),
        "unique_killing_candidate_count": len(unique_killing),
        "intrinsic_pair_candidate_count": len(intrinsic_pair),
        "configuration_alternating_zero_count": 10,
        "configuration_alternating_nonzero_simple_count": 7,
        "intrinsic_pair_and_nonzero_count": len(intrinsic_nonzero),
        "full_screen_primary_intrinsic_nonzero_candidates": full_primary,
        "unique_killing_candidates": unique_killing,
        "intrinsic_pair_candidates": intrinsic_pair,
        "intrinsic_pair_and_nonzero_candidates": intrinsic_nonzero,
        "symmetry_enhanced_candidates": ["C14"],
        "twist_free_candidates": ["C15"],
        "degenerate_candidates": ["C18"],
        "source_manifest_sha256": (HERE / "SOURCE_MANIFEST.sha256").read_text(encoding="utf-8").strip(),
        "candidate_universe_sha256": sha256(HERE / "CANDIDATE_UNIVERSE.tsv"),
        "geometric_result_sha256": sha256(HERE / "GEOMETRIC_RESULT.json"),
        "invariant_certificate_sha256": sha256(HERE / "INVARIANT_CERTIFICATE.json"),
        "result_atlas_sha256": sha256(HERE / "RESULT_ATLAS.tsv"),
        "screen_selected": False,
        "on_shell_claimed": False,
        "physics_promoted": False,
        "universal_full_screen_claimed": False,
        "full_GL2_or_time_live_exhausted": False,
        "nonzero_scope": "OPEN_DENSE_WITH_EXACT_ZERO_LOCUS_RETAINED",
        "open_neighborhood_scope": "STATIONARY_BLOCK_SCREEN_SUBSPACE_RETAINING_K_ONLY",
    }
    (HERE / "ADJUDICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "status": result["status"],
        "unique_killing": len(unique_killing),
        "intrinsic_pair": len(intrinsic_pair),
        "intrinsic_nonzero": len(intrinsic_nonzero),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
