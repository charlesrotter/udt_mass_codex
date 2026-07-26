#!/usr/bin/env python3
"""Deterministically classify every frozen active-result candidate."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent

ALLOWED = {
    "CORRECT_FOUNDED_CHANNEL_AND_SCOPE",
    "PROFILE_OR_PAIR_ASSIGNMENT_OPEN_ONLY",
    "COMPLETE_EXTENSION_OPEN_ONLY",
    "OVERBROAD_ALL_SOLDER_OPEN",
    "FALSE_UNDEFINED_PLACEHOLDER",
    "FALSE_ELEVENTH_POINTWISE_MODE",
    "CONDITIONAL_SLOT_SCOPE_REQUIRES_RETENTION",
    "UNRELATED_PHI_USAGE",
    "HISTORICAL_OR_FROZEN_PRESERVE_ONLY",
    "BLOCKED_REQUIRES_MANUAL_REVIEW",
}

# These are exact per-file semantic rulings, not filename inference. Each line
# was read in context against the founded-pair sources before this table was
# encoded. No source artifact is rewritten by this script.
AFFECTED = {
    "udt_native_coframe_composition_law_audit_2026-07-23/AUDIT_REPORT.md": (
        "OVERBROAD_ALL_SOLDER_OPEN",
        "The sentence that the separate phi/dphi sector is not composed must distinguish the chosen atlas scalar from founded reciprocal depth.",
        "ALGEBRA_UNCHANGED__STATUS_WORDING_NARROWED",
        "Add an append-only overlay: pair-depth composition is derived; only independent-atlas scalar composition and complete-coframe extension remain open.",
        "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md;reciprocal_c_clock_channel_correction_2026-07-19/AUDIT_REPORT.md",
    ),
    "udt_native_coframe_composition_law_audit_2026-07-23/LAY_REPORT.md": (
        "OVERBROAD_ALL_SOLDER_OPEN",
        "The lay sentence that phi still needs its own composition rule is unqualified.",
        "LAY_WORDING_ONLY",
        "Clarify that founded pair depth already adds; a separately chosen atlas scalar and the full coframe extension remain open.",
        "udt_native_coframe_composition_law_audit_2026-07-23/RESULT.json;EXTENSION_CLASS_LEDGER.tsv",
    ),
    "udt_native_coframe_composition_law_audit_2026-07-23/STATUS_LEDGER.tsv": (
        "OVERBROAD_ALL_SOLDER_OPEN",
        "S15 says the scalar is outside the ten-field group without separating the expanded atlas field from founded reciprocal depth.",
        "STATUS_ROW_SCOPE_ONLY",
        "Supersede S15 by a typed two-row distinction; do not alter its chart-group calculation.",
        "udt_reciprocal_c_metric_meaning_audit_2026-07-22/AUDIT_REPORT.md;EXTENSION_CLASS_LEDGER.tsv",
    ),
    "udt_coframe_hopf_bridge_audit_2026-07-23/AUDIT_REPORT.md": (
        "CONDITIONAL_SLOT_SCOPE_REQUIRES_RETENTION",
        "The ten-field-plus-scalar paragraph can be misread as three equally foundation-free depth variables; the separate scalar is a chosen atlas branch.",
        "HOPF_CROSSWALK_UNCHANGED__ONTOLOGY_SCOPE_CLARIFIED",
        "Add an overlay preserving the open base-versus-angular physical owner while stating that founded phi already parameterizes the supplied two-channel base subgroup.",
        "udt_reciprocal_c_metric_meaning_audit_2026-07-22/AUDIT_REPORT.md;udt_coframe_hopf_bridge_audit_2026-07-23/RESULT.json",
    ),
    "udt_global_local_relational_closure_audit_2026-07-25/STATUS_LEDGER.tsv": (
        "OVERBROAD_ALL_SOLDER_OPEN",
        "S01's phrase founding depth solder can be read as reopening the founded clock/ruler subgroup rather than the physical observer/path assignment.",
        "STATUS_WORDING_ONLY",
        "Rename the missing gate to physical observer/path-to-founded-depth assignment; retain the cocycle and closure results.",
        "udt_global_local_relational_closure_audit_2026-07-25/AUDIT_REPORT.md;udt_observer_pair_clock_operator_audit_2026-07-24/AUDIT_REPORT.md",
    ),
}

FOUNDED_CORRECT = {
    "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md",
    "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_MAP.md",
}

FOUNDED_PREFIXES = (
    "reciprocal_c_clock_channel_correction_2026-07-19/",
    "udt_reciprocal_c_metric_meaning_audit_2026-07-22/",
    "udt_phi_metric_ontology_audit_2026-07-22/",
    "udt_observer_pair_clock_operator_audit_2026-07-24/",
)

PROFILE_PREFIXES = (
    "projective_position_",
    "projective_transport_",
    "udt_center_free_observer_optical_correspondence_audit_",
    "udt_finite_cell_transnormal_asymptote_branch_audit_",
    "udt_invariant_xmax_asymptotic_boundary_audit_",
    "udt_metric_native_observer_separation_asymptote_audit_",
    "udt_observer_centered_xmax_frame_correction_",
    "udt_observer_longitudinal_transverse_cocycle_audit_",
    "udt_pair_space_metric_transform_sne_readout_audit_",
    "udt_reciprocal_pair_global_module_audit_",
    "udt_registered_branch_distance_profile_compatibility_audit_",
    "udt_relational_pair_depth_realization_audit_",
    "udt_three_reciprocity_delta_k_audit_",
    "udt_two_frame_regime_metric_limit_audit_",
    "udt_two_observer_separation_selector_audit_",
    "udt_wrl_xmax_lightcone_frame_audit_",
    "udt_xmax_dilation_asymptote_correction_",
    "xmax_",
)

EXTENSION_PREFIXES = (
    "complete_coframe_",
    "udt_chart_coframe_invariance_atlas_",
    "udt_clock_angular_solder_regularity_audit_",
    "udt_clock_ruler_soldering_selector_audit_",
    "udt_coframe_hopf_bridge_audit_",
    "udt_complete_connector_assembly_audit_",
    "udt_complete_metric_intrinsic_object_audit_",
    "udt_complete_metric_realization_zoomout_",
    "udt_csn_dphi_transport_selector_audit_",
    "udt_finite_cell_cartan_transport_atlas_",
    "udt_frame_bivector_equivariance_audit_",
    "udt_global_coframe_cocycle_audit_",
    "udt_global_reciprocal_persistence_selector_audit_",
    "udt_intrinsic_clock_transverse_solder_audit_",
    "udt_metric_native_two_pair_selector_audit_",
    "udt_metric_pure_frame_rederivation_",
    "udt_native_coframe_composition_law_audit_",
    "udt_reciprocal_angular_intertwiner_audit_",
    "udt_reciprocal_seam_descent_audit_",
    "udt_reciprocal_subbundle_ownership_audit_",
    "udt_reciprocal_transport_naturality_selector_audit_",
    "udt_temporal_soldering_atlas_",
)

# These packages intentionally enlarged configuration space by holding phi
# separate. Their calculations remain valid in that declared CHOSE branch;
# they may not be read as a native eleven-field census.
CONDITIONAL_ATLAS_PREFIXES = (
    "udt_amplitude_volume_metric_atlas_",
    "udt_bank_simplex_interior_atlas_",
    "udt_canonical_geometry_evaluator_p01_",
    "udt_complete_metric_solution_space_map_",
    "udt_configuration_space_adjacency_atlas_",
    "udt_constructive_metric_family_atlas_",
    "udt_dynamics_branch_ruling_p04_",
    "udt_full_equation_variation_p05_",
    "udt_global_kinematic_assembly_p03g_",
    "udt_global_metric_assembly_atlas_",
    "udt_independent_amplitude_metric_atlas_",
    "udt_instrument_motif_atlas_",
    "udt_joint_invariant_subspace_atlas_",
    "udt_local_jet_atlas_p02_",
    "udt_local_selector_holonomy_closure_",
    "udt_motif_hopf_correspondence_audit_",
    "udt_phi_causal_interface_atlas_",
    "udt_structural_ensemble_metric_atlas_",
    "udt_time_live_characteristic_flux_audit_",
)


def classify(row: dict[str, str]) -> tuple[str, str, str, str, str, str]:
    path = row["path"]
    if path in AFFECTED:
        ruling, claim, math, action, evidence = AFFECTED[path]
        return ruling, "YES", claim, math, action, evidence
    if row["source_status"] == "FROZEN_ACTIVE_EVIDENCE" or path in {
        "UDT_NATIVE_ACTION_COLD_PACKET.md",
        "UDT_NATIVE_ACTION_DERIVATION_DISPATCH.md",
    }:
        return (
            "HISTORICAL_OR_FROZEN_PRESERVE_ONLY", "NO",
            "Immutable provenance statement; later semantic overlays do not rewrite it.",
            "PRESERVE_BYTE_IDENTICAL", "No source edit; cite the current overlay when relevant.",
            "PREREGISTRATION.md",
        )
    if path in FOUNDED_CORRECT or path.startswith(FOUNDED_PREFIXES):
        return (
            "CORRECT_FOUNDED_CHANNEL_AND_SCOPE", "NO",
            "Distinguishes founded reciprocal depth from the open profile or complete extension.",
            "UNCHANGED", "None.",
            "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md",
        )
    if path.startswith(CONDITIONAL_ATLAS_PREFIXES):
        return (
            "CONDITIONAL_SLOT_SCOPE_REQUIRES_RETENTION", "NO",
            "Uses an intentionally enlarged or supplied independent-phi configuration branch.",
            "UNCHANGED_IN_CHOSEN_CONFIGURATION_SCOPE", "Retain the CHOSE premise on every reuse.",
            "udt_reciprocal_c_metric_meaning_audit_2026-07-22/AUDIT_REPORT.md",
        )
    if path.startswith(PROFILE_PREFIXES):
        return (
            "PROFILE_OR_PAIR_ASSIGNMENT_OPEN_ONLY", "NO",
            "Leaves the physical pair/path/profile assignment open without reopening the founded subgroup.",
            "UNCHANGED", "None.",
            "udt_observer_pair_clock_operator_audit_2026-07-24/AUDIT_REPORT.md",
        )
    if path.startswith(EXTENSION_PREFIXES):
        return (
            "COMPLETE_EXTENSION_OPEN_ONLY", "NO",
            "Addresses angular, shear, shift, frame, path, or global extension beyond the founded pair.",
            "UNCHANGED", "None.",
            "EXTENSION_CLASS_LEDGER.tsv",
        )
    return (
        "UNRELATED_PHI_USAGE", "NO",
        "No load-bearing assertion that phi is an undefined placeholder or an eleventh native pointwise metric mode.",
        "UNCHANGED", "None.",
        "ACTIVE_RESULT_CANDIDATES.tsv",
    )


def main() -> None:
    with (HERE / "ACTIVE_RESULT_CANDIDATES.tsv").open(encoding="utf-8", newline="") as handle:
        candidates = list(csv.DictReader(handle, delimiter="\t"))
    if len({row["candidate_id"] for row in candidates}) != len(candidates):
        raise AssertionError("duplicate candidate id")
    if len({row["path"] for row in candidates}) != len(candidates):
        raise AssertionError("duplicate candidate path")

    rows = []
    for row in candidates:
        ruling, affected, claim, math, action, evidence = classify(row)
        if ruling not in ALLOWED:
            raise AssertionError((row["path"], ruling))
        rows.append({
            **row,
            "primary_ruling": ruling,
            "affected": affected,
            "disputed_claim_or_scope": claim,
            "mathematical_result_effect": math,
            "future_correction_action": action,
            "ruling_evidence": evidence,
        })

    fields = list(rows[0])
    with (HERE / "ACTIVE_RESULT_IMPACT_LEDGER.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    affected = [row for row in rows if row["affected"] == "YES"]
    with (HERE / "AFFECTED_RESULT_CORRECTION_PLAN.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(affected)

    print(f"active_candidates={len(rows)}")
    print(f"affected_results={len(affected)}")
    for key, value in sorted(Counter(row["primary_ruling"] for row in rows).items()):
        print(f"ruling[{key}]={value}")


if __name__ == "__main__":
    main()
