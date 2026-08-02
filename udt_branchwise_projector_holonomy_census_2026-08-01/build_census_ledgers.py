#!/usr/bin/env python3
"""Build complete source dispositions and the branch/object six-gate ledger."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent

# These packages were admitted only after their report text identified an
# actual projector/subbundle/holonomy object or a direct obstruction/control.
# Names locate the already-read source; they are not the evidence for the
# classification.  REPORT_DISPOSITIONS.tsv carries the source excerpt.
SIX_GATE_GROUPS = {
    "complete_coframe_seal_involution_2026-07-20",
    "metric_cartan_holonomy_audit_2026-07-19",
    "null_section_hopfion_metric_audit_2026-07-19",
    "projective_transport_section_selector_2026-07-19",
    "reciprocal_metric_null_line_selector_2026-07-19",
    "udt_alpha_plane_selector_theorem_2026-07-28",
    "udt_cap_gluing_selector_2026-07-28",
    "udt_complete_metric_intrinsic_object_audit_2026-07-23",
    "udt_complete_nonultrastatic_reciprocal_branch_audit_2026-07-27",
    "udt_complete_screen_response_branch_atlas_2026-07-28",
    "udt_complete_seal_fixed_set_selector_audit_2026-07-21",
    "udt_dual_systole_global_transport_audit_2026-07-24",
    "udt_dual_systole_wall_crossing_selector_audit_2026-07-24",
    "udt_exceptional_stratum_remainder_2026-07-28",
    "udt_finite_cell_cartan_transport_atlas_2026-07-23",
    "udt_finite_cell_reciprocal_quotient_reduction_audit_2026-07-27",
    "udt_finite_cell_reciprocal_survival_density_audit_2026-07-23",
    "udt_frame_bivector_equivariance_audit_2026-07-23",
    "udt_full_screen_hopf_toric_rederivation_2026-07-28",
    "udt_general_screen_complete_cell_atlas_2026-07-28",
    "udt_global_reciprocal_bundle_assembly_audit_2026-07-26",
    "udt_higher_isometry_plane_ownership_audit_2026-07-28",
    "udt_intrinsic_reciprocal_holonomy_audit_2026-07-27",
    "udt_intrinsic_ruler_full_screen_descent_audit_2026-07-28",
    "udt_joint_invariant_subspace_atlas_2026-07-21",
    "udt_killing_plane_strata_transition_audit_2026-07-28",
    "udt_local_selector_holonomy_closure_2026-07-22",
    "udt_metric_native_two_pair_selector_audit_2026-07-21",
    "udt_metric_natural_complete_extension_selector_audit_2026-07-27",
    "udt_metric_natural_joint_selector_nogo_2026-07-28",
    "udt_reciprocal_plane_projector_audit_2026-07-21",
    "udt_reciprocal_seam_descent_audit_2026-07-23",
    "udt_reciprocal_subbundle_ownership_audit_2026-07-22",
    "udt_reduced_holonomy_condition_audit_2026-07-27",
    "udt_temporal_soldering_atlas_2026-07-22",
    "udt_twisted_s3_intrinsic_pair_witness_audit_2026-07-27",
    "udt_twisted_s3_intrinsic_screen_cocycle_audit_2026-07-27",
}

CONTROL_ROOT = {
    "AGENTS.md", "CANON.md", "CLAUDE.md", "CURRENT_SCIENTIFIC_PREMISES.md",
    "CURRENT_SCIENTIFIC_PREMISES.tsv", "HANDOFF.md", "INDEX.md", "LIVE.md",
    "MEMORY.md", "README.md", "STATE.md", "INFLIGHT_STATE.md",
    "FOUNDATIONAL_ASSUMPTIONS_LEDGER.md", "NEGATIVES_REGISTRY.md",
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md",
}


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(name: str, rows: list[dict[str, object]], fields: list[str] | None = None) -> None:
    if fields is None:
        fields = list(rows[0])
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def report_disposition(row: dict[str, str]) -> str:
    if row["top_group"] in SIX_GATE_GROUPS:
        return "SIX_GATE_SOURCE"
    if row["triage_route"] == "MANUAL_SIX_GATE_REVIEW":
        return "SUPPORTING_OR_INCOMPLETE_BRANCH_SOURCE"
    if row["triage_route"] == "MANUAL_SUPPORT_OR_LOCAL_REVIEW":
        return "SUPPORTING_LOCAL_OR_CONTEXT_SOURCE"
    return "CONTEXT_ONLY_NOT_BRANCH_SOURCE"


def nonreport_group_disposition(group: str) -> str:
    if group == "ROOT":
        return "MIXED__SEE_PATH_LEVEL_DISPOSITIONS"
    if group.startswith("reorganization_"):
        return "REORGANIZATION_FORENSIC_RECORD"
    if group in {"archive", "legacy", "rescued_workspaces", "verifier_evidence_2026-07-14"}:
        return "PROVENANCE_OR_HISTORICAL_ONLY"
    if group in {"tests", ".claude"}:
        return "CONTROL_OR_TEST_SUPPORT"
    if group in {
        "udt_metric_to_frontier_reference_2026-07-22", "udt_scientific_consolidation_checkpoint_2026-07-23",
        "udt_century_adjacent_mathematics_survey_2026-07-22", "udt_f02_global_completion_admissibility_review_2026-08-01",
        "udt_p4_cold_review_repair_2026-08-01", "research",
    }:
        return "SUPPORTING_REFERENCE_OR_REVIEW"
    return "SUPPORTING_OR_PROVENANCE_NOT_STANDALONE_BRANCH"


def main() -> int:
    reports = read_tsv("REPORT_EVIDENCE_EXTRACT.tsv")
    report_rows = []
    report_by_group = {}
    for row in reports:
        disposition = report_disposition(row)
        report_by_group[row["top_group"]] = disposition
        report_rows.append({
            "path": row["path"], "top_group": row["top_group"], "git_blob": row["git_blob"],
            "sha256": row["sha256"], "first_commit_date": row["first_commit_date"],
            "triage_route": row["triage_route"], "scientific_disposition": disposition,
            "source_result_excerpt": row["result_excerpt"],
        })
    write_tsv("REPORT_DISPOSITIONS.tsv", report_rows)

    group_rows = []
    for row in read_tsv("DISCOVERY_GROUPS.tsv"):
        disposition = report_by_group.get(row["top_group"], nonreport_group_disposition(row["top_group"]))
        group_rows.append({**{key: value for key, value in row.items() if key != "required_disposition"},
                           "scientific_disposition": disposition})
    write_tsv("GROUP_DISPOSITIONS.tsv", group_rows)

    base_manifest = read_tsv("BASE_TREE_MANIFEST.tsv")
    source_manifest_rows = [
        row for row in base_manifest if row["top_group"] in SIX_GATE_GROUPS
    ]
    write_tsv(
        "SIX_GATE_SOURCE_MANIFEST.tsv",
        source_manifest_rows,
        ["path", "mode", "git_blob", "sha256", "top_group", "suffix", "text_discovery_eligible"],
    )

    # Every literal content hit gets a disposition.  Root is intentionally
    # split path-by-path so the mixed ROOT bucket cannot hide a missing row.
    current_class = {}
    registry = ROOT / "research/_registry/CURRENT_CLASSIFICATION.tsv"
    if registry.exists():
        with registry.open(newline="", encoding="utf-8") as handle:
            current_class = {row["current_path"]: row for row in csv.DictReader(handle, delimiter="\t")}
    hit_rows = []
    group_map = {row["top_group"]: row["scientific_disposition"] for row in group_rows}
    for row in read_tsv("DISCOVERY_HITS.tsv"):
        disposition = group_map[row["top_group"]]
        evidence = "TOP_GROUP_SOURCE_DISPOSITION"
        if row["top_group"] == "ROOT":
            if row["path"] in CONTROL_ROOT:
                disposition, evidence = "CONTROL_CONTEXT", "PERMANENT_OR_CURRENT_CONTROL_PATH"
            elif row["path"] in current_class and current_class[row["path"]]["scientific_lifecycle"] == "HISTORICAL":
                disposition, evidence = "PROVENANCE_OR_HISTORICAL_ONLY", "CURRENT_CLASSIFICATION_HISTORICAL"
            else:
                disposition, evidence = "SUPPORTING_OR_HISTORICAL_NOT_STANDALONE_BRANCH", "ROOT_PATH_NO_COMPLETE_BRANCH_REPORT"
        hit_rows.append({**row, "path_disposition": disposition, "disposition_evidence": evidence})
    write_tsv("DISCOVERY_HIT_DISPOSITIONS.tsv", hit_rows)

    source = {row["top_group"]: row for row in reports}
    cases = [
        ("B01", "complete_twisted_S3_C01_C06_intrinsic_ruler", "COMPLETE_GLOBAL_OFFSHELL_CONFIGURATION", "C03;C09", "udt_twisted_s3_intrinsic_pair_witness_audit_2026-07-27", "PASS_METRIC_INTRINSIC", "PASS_RANK1_UNIQUE_UNORIENTED_IN_FROZEN_FAMILY", "PASS_GLOBAL_SMOOTH", "PASS_COVARIANT_PROJECTED_CONNECTION__FAIL_AMBIENT_PARALLEL_HOLONOMY", "PASS_RxS3_GLOBAL_DESCENT", "PASS_NONZERO_AT_P00_ALL_6", "DERIVED_CONDITIONAL_ON_NAMED_REGISTERED_CONFIGURATION"),
        ("B02", "complete_twisted_S3_C01_C06_rank2_screen_complement", "COMPLETE_GLOBAL_OFFSHELL_CONFIGURATION", "C02;C09", "udt_finite_cell_reciprocal_quotient_reduction_audit_2026-07-27", "PASS_FROM_INTRINSIC_CLOCK_AND_RULER", "PASS_RANK2_UNIQUE_COMPLEMENT", "PASS_GLOBAL_SMOOTH", "PASS_PROJECTED_O2_CONNECTION__FAIL_AMBIENT_PARALLEL_HOLONOMY", "PASS_RxS3_GLOBAL_DESCENT", "PASS_SAME_NONZERO_RELATIVE_TERM_AS_B01", "DERIVED_CONDITIONAL_ON_NAMED_REGISTERED_CONFIGURATION"),
        ("B03", "lambda_plus1_constant_depth_round_product_clock_line", "COMPLETE_GLOBAL_OFFSHELL_CONTROL", "C12", "udt_reduced_holonomy_condition_audit_2026-07-27", "PASS_METRIC_CLOCK_LINE", "PASS_RANK1_CLOCK_ONLY", "PASS_GLOBAL_SMOOTH", "PASS_PARALLEL_SO3_REDUCED_HOLONOMY", "PASS_RxS3", "FAIL_ZERO_DP", "PARALLEL_ZERO_RESPONSE_CONTROL"),
        ("B04", "generic_lapse_static_S3_unique_clock_only", "COMPLETE_GLOBAL_OFFSHELL_CONTROL", "C03;C15", "udt_complete_nonultrastatic_reciprocal_branch_audit_2026-07-27", "PASS_METRIC_INTRINSIC_CLOCK", "PASS_CLOCK_LINE__NO_SAME_METRIC_RULER_IN_PARENT", "PASS_GLOBAL_SMOOTH", "OPEN_PROJECTOR_RESPONSE_NOT_SOURCE_AUDITED", "PASS_RxS3", "OPEN_NOT_COMPUTED_FOR_CLOCK_ONLY", "INCOMPLETE_FOR_POSITIVE_RANK3_RESPONSE"),
        ("B05", "nonnull_dphi_projector_and_3plus3_twoform_split", "LOCAL_TYPED_STRATUM", "C04", "udt_complete_metric_intrinsic_object_audit_2026-07-23", "PASS_FIELD_ASSISTED_INTRINSIC", "PASS_NONNULL_STRATUM", "PASS_UNTIL_NULL_OR_ZERO", "PASS_TENSORIAL__PARALLELISM_NOT_FORCED", "OPEN_OR_FAILS_AT_TYPE_CHANGE_AND_STATIC_COMPACT_CRITICAL_POINT", "OPEN_NO_COMPLETE_BRANCH_RESPONSE", "LOCAL_STRATUM_ONLY"),
        ("B06", "null_or_zero_dphi_stratum", "DEGENERATE_LOCAL_CONTROL", "C15", "udt_complete_metric_intrinsic_object_audit_2026-07-23", "FAIL_SEMISIMPLE_PROJECTOR", "FAIL_NULL_NILPOTENT_OR_ZERO", "FAIL_CONTINUATION", "NOT_APPLICABLE", "NOT_APPLICABLE", "NOT_APPLICABLE", "NO_PROJECTOR_ON_STRATUM"),
        ("B07", "simple_spectrum_curvature_hessian_shape_lines", "LOCAL_POINTWISE_FAMILIES", "C01;C10", "udt_metric_native_two_pair_selector_audit_2026-07-21", "PASS_ONLY_AFTER_NAMED_OPERATOR", "PASS_SIMPLE_SPECTRUM__FAIL_TIES_AND_OPERATOR_PRIORITY", "PASS_WITHIN_SIMPLE_STRATUM", "OPEN", "OPEN_OR_FAILS_AT_DEGENERACY", "OPEN", "LOCAL_NONUNIQUE_OPERATOR_FAMILIES"),
        ("B08", "dual_systole_unique_shortest_line_chambers", "GLOBAL_SET_VALUED_TORIC_FAMILY", "C06;C11", "udt_dual_systole_global_transport_audit_2026-07-24", "PASS_GIVEN_INTEGRAL_TORUS_LATTICE", "PASS_TIE_FREE_CHAMBER_ONLY", "PASS_INSIDE_CHAMBER", "PASS_PROJECTED_CONNECTION_COVARIANT", "FAIL_SINGLE_LINE_AT_WALL_OR_EXCHANGE_WITHOUT_EXTRA_GLUE", "OPEN", "SET_VALUED_GLOBAL__SINGLE_LINE_LOCAL_CHAMBER"),
        ("B09", "dual_systole_tie_pair_at_symmetric_seal", "GLOBAL_SET_VALUED_CONTROL", "C11", "udt_dual_systole_wall_crossing_selector_audit_2026-07-24", "PASS_UNORDERED_SET", "FAIL_UNIQUE_MEMBER", "PASS_SET_CONTINUATION", "PASS_SET_EQUIVARIANCE", "PASS_SET__FAIL_SINGLE_MEMBER", "OPEN", "SET_VALUED_ONLY"),
        ("B10", "seal_involution_eigenspaces", "CONDITIONAL_COMPLETION_FAMILIES", "C07", "complete_coframe_seal_involution_2026-07-20", "FAIL_CURRENT_COMPLETE_COFRAME_ACTION_UNSELECTED", "MULTIPLE_F_B_AND_ANGULAR_LIFTS", "CONDITIONAL", "CONDITIONAL", "OPEN_COMPLETE_LIFT", "OPEN", "CONDITIONAL_ON_UNSELECTED_INVOLUTION"),
        ("B11", "celestial_null_direction_fiber", "CONDITIONAL_BUNDLE_ONLY", "C08", "null_section_hopfion_metric_audit_2026-07-19", "PASS_FIBER__FAIL_SELECTED_SECTION", "FAIL_UNIQUE_RAY", "PASS_BUNDLE_LOCALLY", "CONDITIONAL_NULL_TRANSPORT", "OPEN_SECTION_AND_TRIVIALIZATION", "NOT_TYPED_AS_POSITIVE_RANK3_PROJECTOR", "FIBER_NOT_SECTION"),
        ("B12", "supplied_reciprocal_tangent_two_plane", "LOCAL_CONDITIONAL_REALIZATION", "C09;C13", "udt_reciprocal_plane_projector_audit_2026-07-21", "FAIL_METRIC_SELECTION__PLANE_SUPPLIED", "PASS_GIVEN_PLANE", "PASS_DECLARED_LOCAL_CLASS", "CONDITIONAL_PARALLEL_CONNECTION_IFF_INTEGRABLE_UMBILICAL", "OPEN_GLOBAL", "ZERO_FOR_CONSTANT_CONTROLS_OR_OPEN", "SUPPLIED_CONDITIONAL_NOT_INTRINSIC"),
        ("B13", "complete_twisted_S3_full_Lorentz_holonomy", "COMPLETE_GLOBAL_OFFSHELL_CONTROL", "C14", "udt_intrinsic_reciprocal_holonomy_audit_2026-07-27", "PASS_ACTUAL_HOLONOMY_OBJECT", "FAIL_ANY_HOLONOMY_INVARIANT_PROPER_LINE", "PASS_AT_18_BOUNDED_EVENTS", "FAIL_REDUCED_HOLONOMY_RANK6", "FAIL_ENDPOINT_ONLY_DESCENT", "NOT_APPLICABLE_TO_INVARIANT_LINE", "NO_REDUCED_HOLONOMY_ON_TESTED_BRANCH"),
        ("B14", "flat_or_round_isotropy_controls", "COMPLETE_OR_LOCAL_CONTROLS", "C12;C14", "udt_complete_metric_intrinsic_object_audit_2026-07-23", "FAIL_SELECTION__EVERY_OR_NO_LINE_EQUIVALENT", "FAIL_UNIQUE", "PASS_CONTROL", "PARALLEL_OPTIONS_EXIST_BUT_UNSELECTED", "CONDITIONAL", "ZERO_IF_CONSTANT_PARALLEL", "ISOTROPY_OR_ZERO_RESPONSE_CONTROL"),
        ("B15", "higher_isometry_multiple_Killing_planes", "COMPLETE_STATIONARY_BOUNDED_FAMILY", "C03;C06;C11", "udt_higher_isometry_plane_ownership_audit_2026-07-28", "PASS_REGISTERED_PLANES__FAIL_UNIVERSAL_PLANE_OWNER", "FAIL_UNIQUE_ACROSS_LARGER_ALGEBRA", "PASS_PRINCIPAL_STRATA", "OPEN", "CONDITIONAL_CAP_RESULTS", "OPEN", "MULTIPLE_NATURAL_PLANES"),
        ("B16", "fully_descended_nonconstant_depth_KV_plane", "COMPLETE_STATIONARY_OFFSHELL_SUBFAMILY", "C03;C06", "udt_killing_plane_strata_transition_audit_2026-07-28", "PASS_CONDITIONAL_ON_REGISTERED_KV_PLANE", "PASS_CLOCK_RULER_LINES_ON_NONCONSTANT_STRATUM", "PASS_AWAY_FROM_CONSTANT_DEPTH_DEGENERACY", "COVARIANT_FIELD__HOLONOMY_NOT_ESTABLISHED", "PASS_REGISTERED_DESCENT", "PASS_WHERE_OVERLAPPING_C01_C06__OTHERWISE_OPEN", "POSITIVE_SUBFAMILY_WITH_NAMED_PLANE_PREMISE"),
        ("B17", "reciprocal_value_character_seam_descent", "GLOBAL_ENDOMORPHISM_GLUE", "C09", "udt_reciprocal_seam_descent_audit_2026-07-23", "PASS_VALUE_CHARACTER_GIVEN_TRANSITION", "NOT_A_SELECTED_POSITIVE_RANK3_LINE", "PASS_THROUGH_DPHI_ZERO", "PASS_CONJUGACY_GLUE", "PASS_CONDITIONAL_TRANSITION", "NOT_APPLICABLE", "GLOBAL_CHARACTER_NOT_PROJECTOR_SELECTION"),
        ("B18", "eleven_structural_completion_classes_without_metrics", "INCOMPLETE_COMPLETION_TYPES", "C15", "udt_finite_cell_reciprocal_survival_density_audit_2026-07-23", "OPEN", "OPEN", "OPEN", "OPEN", "FAIL_MISSING_COMPLETE_G_PHI_WITNESS", "OPEN", "INCOMPLETE_WITNESSES_RETAINED"),
    ]
    case_fields = ["case_id", "object_family", "branch_type", "candidate_classes", "source_group", "gate1_intrinsic", "gate2_rank_uniqueness", "gate3_smooth_local", "gate4_transport_holonomy", "gate5_global_descent", "gate6_relative_curvature", "ruling"]
    case_rows = []
    for values in cases:
        row = dict(zip(case_fields, values))
        report = source[row["source_group"]]
        row["source_path"] = report["path"]
        row["source_sha256"] = report["sha256"]
        case_rows.append(row)
    write_tsv("BRANCH_OBJECT_GATE_LEDGER.tsv", case_rows, case_fields + ["source_path", "source_sha256"])

    result = {
        "reports_dispositioned": len(report_rows),
        "discovery_groups_dispositioned": len(group_rows),
        "discovery_hits_dispositioned": len(hit_rows),
        "six_gate_source_groups": sum(row["scientific_disposition"] == "SIX_GATE_SOURCE" for row in report_rows),
        "branch_object_cases": len(case_rows),
        "six_gate_source_manifest_paths": len(source_manifest_rows),
        "complete_configuration_nonzero_relative_curvature_cases": 2,
        "report_dispositions_sha256": hashlib.sha256((HERE / "REPORT_DISPOSITIONS.tsv").read_bytes()).hexdigest(),
        "group_dispositions_sha256": hashlib.sha256((HERE / "GROUP_DISPOSITIONS.tsv").read_bytes()).hexdigest(),
        "hit_dispositions_sha256": hashlib.sha256((HERE / "DISCOVERY_HIT_DISPOSITIONS.tsv").read_bytes()).hexdigest(),
        "branch_object_gate_ledger_sha256": hashlib.sha256((HERE / "BRANCH_OBJECT_GATE_LEDGER.tsv").read_bytes()).hexdigest(),
        "six_gate_source_manifest_sha256": hashlib.sha256((HERE / "SIX_GATE_SOURCE_MANIFEST.tsv").read_bytes()).hexdigest(),
        "status": "PASS",
    }
    (HERE / "CENSUS_LEDGER_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
