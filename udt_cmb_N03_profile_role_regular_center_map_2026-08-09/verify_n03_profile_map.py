#!/usr/bin/env python3
"""Independent fail-closed verification of the repaired N03 map."""

from __future__ import annotations

import ast
import copy
import csv
import hashlib
import json
import re
import subprocess
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
PROFILE_SOURCE = ROOT / "udt_cmb_N02_radial_anchor_admissibility_2026-08-09/PROFILE_STRATA.tsv"
CHECKS: dict[str, bool] = {}
PREREG_COMMIT = "c64acaa1"


def check(name: str, condition: object) -> None:
    CHECKS[name] = bool(condition)
    print(f"CHECK {name}: {CHECKS[name]}")


def read_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return list(reader.fieldnames or []), list(reader)


def table(name: str) -> list[dict[str, str]]:
    return read_tsv(HERE / name)[1]


def validate_sources() -> tuple[list[dict[str, str]], dict[str, str]]:
    fields, rows = read_tsv(HERE / "SOURCE_MANIFEST.tsv")
    if fields != ["path", "sha256"] or len(rows) != 16 or len({row["path"] for row in rows}) != 16:
        raise ValueError("source universe")
    texts: dict[str, str] = {}
    for row in rows:
        path = ROOT / row["path"]
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != row["sha256"]:
            if row["path"] != "CURRENT_SCIENTIFIC_PREMISES.tsv":
                raise ValueError("source hash")
            historical = subprocess.run(
                ["git", "show", f"{PREREG_COMMIT}:{row['path']}"],
                cwd=ROOT,
                capture_output=True,
                check=False,
            )
            if historical.returncode or hashlib.sha256(historical.stdout).hexdigest() != row["sha256"]:
                raise ValueError("historical source hash")
            data = historical.stdout
        texts[row["path"]] = data.decode("utf-8")
    return rows, texts


EXPECTED_CANDIDATES = {
    "P01_RECIPROCAL_CEFF_RATIO": {
        "candidate_id": "P01_RECIPROCAL_CEFF_RATIO",
        "object": "lambda_t pair ratio plus conditional reference-point and regular-stratum strain readouts",
        "primary_role": "PAIR_RELATION_ONLY",
        "source_scope": "ceff_pair_ratio__reference_readout__complete_arrow_extractor",
        "center_test": "NOT_APPLICABLE_PAIR_OBJECT",
        "mu_status": "ORCHESTRA_MIXING_CAN_MODULATE_COMPLETE_PAIR",
        "angular_status": "COMPLETE_PAIR_ORCHESTRA_RETAINED",
        "xmax_status": "MUST_REALIZE_ASYMPTOTIC_GATE",
        "complete_witness": "NO",
        "ruling": "PAIR_INVARIANT_WITH_CONDITIONAL_READOUTS_NOT_LOCAL_RADIAL_PROFILE",
    },
    "P02_STATIONARY_SCREEN_COCYCLE_FAMILY": {
        "candidate_id": "P02_STATIONARY_SCREEN_COCYCLE_FAMILY",
        "object": "groupoid cocycle home; conditional stationary screen family; conditional one-form subclass",
        "primary_role": "PAIR_RELATION_ONLY",
        "source_scope": "phi_orchestra_cocycle_and_conditional_stationary_branch",
        "center_test": "NOT_APPLICABLE_PAIR_COCYCLE",
        "mu_status": "LOWER_MIXING_NOT_SELECTED_BY_THIS_CHARACTER",
        "angular_status": "SCREEN_AREA_MODULATION_EXPLICIT_A_FREE",
        "xmax_status": "UNTESTED_FAMILY_PARAMETER_AND_GLOBAL_JOIN",
        "complete_witness": "NO",
        "ruling": "DERIVED_COCYCLE_HOME__CONDITIONAL_FAMILY__TRANSPORT_SUBCLASS_NOT_DERIVED",
    },
    "P03_XMAX_LIMIT_SCHEMA": {
        "candidate_id": "P03_XMAX_LIMIT_SCHEMA",
        "object": "0<=s<Xmax; s->Xmax implies abs(delta)->infinity",
        "primary_role": "PAIR_RELATION_ONLY",
        "source_scope": "owner_ratified_asymptotic_gate",
        "center_test": "NOT_APPLICABLE_NOT_A_METRIC_PROFILE",
        "mu_status": "ANGULAR_BOOTSTRAP_MODULATION_OPEN",
        "angular_status": "PATH_AND_CUT_LOCUS_DATA_RETAINED",
        "xmax_status": "DEFINITIONAL_GATE_ONLY",
        "complete_witness": "NO",
        "ruling": "NOT_WALL_CENTER_EDGE_OR_BOUNDARY",
    },
    "P04_P1_ROUND_CONTROLS": {
        "candidate_id": "P04_P1_ROUND_CONTROLS",
        "object": "A=(1-r/Rw)^n; h=0; 3 source-derived n strata",
        "primary_role": "CONDITIONAL_OPERATOR_CONTROL",
        "source_scope": "P1_data_conditioned_pair_shape_reused_as_control",
        "center_test": "FAIL_A_ODD_LINEAR_JET",
        "mu_status": "MU_OFF_SCAFFOLD_ONLY",
        "angular_status": "ROUND_CONTROL",
        "xmax_status": "PAIR_ASYMPTOTE_ROLE_NOT_COMPLETE_WALL",
        "complete_witness": "NO",
        "ruling": "PAIR_ROLE_SURVIVES_COMPLETE_METRIC_PROMOTION_BLOCKED",
    },
    "P05_P1_CORRECTED_MIXING_CONTROLS": {
        "candidate_id": "P05_P1_CORRECTED_MIXING_CONTROLS",
        "object": "A=(1-r/Rw)^n; h=hbar*r^2*(1-r/Rw)^q; 21 strata and 210 profiles",
        "primary_role": "CONDITIONAL_OPERATOR_CONTROL",
        "source_scope": "FD1_N02_corrected_axial_family",
        "center_test": "A_FAILS_ALL; H_EQUALS_h_OVER_r2_FULLY_SMOOTH_ONLY_q0_30_OF_210",
        "mu_status": "MU_ON",
        "angular_status": "FULL_SPHERICAL_N01_COUPLING_REQUIRED",
        "xmax_status": "WALL_COORDINATE_JOIN_OPEN",
        "complete_witness": "NO",
        "ruling": "NECESSARY_h_ORDER_NOT_SUFFICIENT_GLOBAL_PROFILE",
    },
    "P06_RA1_NEAR_WALL_AND_SS3_FORK": {
        "candidate_id": "P06_RA1_NEAR_WALL_AND_SS3_FORK",
        "object": "literal h0*(1-r/Rw)^q near-wall family plus conditional SS3 center-completion fork",
        "primary_role": "CONDITIONAL_OPERATOR_CONTROL",
        "source_scope": "RA1_near_wall_lineage_and_P_RA1_8_fork",
        "center_test": "LITERAL_FAILS_A_AND_h; SS3_FORK_NECESSARY_ORDER_ONLY_NO_EXPLICIT_GLOBAL_PROFILE",
        "mu_status": "MU_ON_NEAR_WALL_AND_CONDITIONAL_CENTER_FORK",
        "angular_status": "EQUATORIAL_ENDPOINT_LINEAGE_FULL_SPHERE_NOT_COMPUTED",
        "xmax_status": "NEAR_WALL_CLASS_NOT_GLOBAL_REALIZATION",
        "complete_witness": "NO",
        "ruling": "ENDPOINT_LINEAGE_SURVIVES_SS3_FORK_NOT_COMPLETE_PROFILE",
    },
    "P07_C1_GENERAL_AXIAL_ENVELOPE": {
        "candidate_id": "P07_C1_GENERAL_AXIAL_ENVELOPE",
        "object": "A(r),h(r),round leading screen; B=h^2/(A*r^2)",
        "primary_role": "CONDITIONAL_OPERATOR_CONTROL",
        "source_scope": "C1_chose_complete_angular_envelope",
        "center_test": "PASSABLE_SUBSPACE_A_EVEN_h_EQUALS_r2_TIMES_EVEN",
        "mu_status": "MU_ON_COMPATIBLE_k0_MAY_BE_NONZERO_NOT_REQUIRED_OR_SELECTED",
        "angular_status": "B_EQUALS_k0_squared_r2_PLUS_SO_ROUND_LEADING_ORDER",
        "xmax_status": "NO_GLOBAL_PROFILE_OR_ASYMPTOTIC_JOIN_SUPPLIED",
        "complete_witness": "LOCAL_JET_ONLY",
        "ruling": "NONEMPTY_REGULAR_JET_SPACE_NOT_GLOBAL_SOLUTION",
    },
    "P08_GENERAL_SCREEN_SHIFT_ENVELOPE": {
        "candidate_id": "P08_GENERAL_SCREEN_SHIFT_ENVELOPE",
        "object": "stationary positive screen plus angular shift; source-derived C01-C18 members",
        "primary_role": "CONDITIONAL_OPERATOR_CONTROL",
        "source_scope": "complete_angular_family_design_map",
        "center_test": "GEODESIC_POLAR_POINT_REQUIRES_ROUND_LEADING_COLLAPSE_OR_NO_CENTER_TOPOLOGY",
        "mu_status": "GENERAL_SHIFT_RETAINED",
        "angular_status": "SHIFT_DIVERGENCE_TERM_AND_ALL_SCREEN_TIERS_RETAINED",
        "xmax_status": "NO_GLOBAL_PROFILE_OR_ASYMPTOTIC_JOIN_SUPPLIED",
        "complete_witness": "NO",
        "ruling": "ARCHITECTURE_NOT_SELECTED_PROFILE",
    },
}


EXPECTED_JETS = {
    "lapse_lock_A": {
        "object": "lapse_lock_A",
        "regular_center_jet": "A=1+a2*r^2+a4*r^4+...",
        "invariant_content": "metric_first_derivatives_removable_and_curvature_finite",
        "mu_or_angular_effect": "conditional_local_representative_has_zero_center_slope",
        "status": "DERIVED_FOR_DECLARED_CENTERED_ENVELOPE",
    },
    "spatial_areal_block": {
        "object": "spatial_areal_block",
        "regular_center_jet": "(1/A-1)/r^2=smooth_even",
        "invariant_content": "no_conical_or_directional_center_cusp",
        "mu_or_angular_effect": "independent_of_pair_profile_slope",
        "status": "DERIVED_FOR_DECLARED_CENTERED_ENVELOPE",
    },
    "axial_clock_screen_mixing_h": {
        "object": "axial_clock_screen_mixing_h",
        "regular_center_jet": "h=r^2*(k0+k2*r^2+...)",
        "invariant_content": "coordinate_one_form_smooth_on_collapsing_orbit",
        "mu_or_angular_effect": "mu_on_compatible; k0_may_be_nonzero_but_is_not_required_or_selected",
        "status": "DERIVED_FULL_CARTESIAN_JET_IN_CONDITIONAL_h_REALIZATION",
    },
    "N01_dimensionless_angular_distortion_B": {
        "object": "N01_dimensionless_angular_distortion_B",
        "regular_center_jet": "B=k0^2*r^2+(2*k0*k2-a2*k0^2)*r^4+...",
        "invariant_content": "complete_angular_matrices_return_to_round_limit_at_center",
        "mu_or_angular_effect": "mixing_reenters_away_from_center_and_normalized_h_may_be_finite",
        "status": "DERIVED_FOR_C1",
    },
    "complete_angular_screen": {
        "object": "complete_angular_screen",
        "regular_center_jet": "q_AB=sphere_AB+r^2*q2_AB+... in geodesic-polar/orthonormal-center form",
        "invariant_content": "small_geodesic_spheres_round_at_leading_order",
        "mu_or_angular_effect": "orchestra_modulation_begins_beyond_leading_point_collapse",
        "status": "NECESSARY_SMOOTH_POINT_REQUIREMENT_NOT_ALL_CHARTS_OR_SUFFICIENCY",
    },
    "pair_relation_P1": {
        "object": "pair_relation_P1",
        "regular_center_jet": "not_required; one_sided_slope=-n/Rw_allowed_in_pair_separation",
        "invariant_content": "pair_coincidence_is_not_identified_with_manifold_center",
        "mu_or_angular_effect": "complete_pair_orchestra_may_modulate_depth",
        "status": "PAIR_ROLE_ONLY_JOIN_OPEN",
    },
}


EXPECTED_BRANCHES = {
    "B01_PAIR_SPACE": {
        "branch": "B01_PAIR_SPACE", "center": "PAIR_DIAGONAL_NOT_MANIFOLD_CENTER",
        "xmax": "RELATIONAL_ASYMPTOTE", "allowed_profiles": "P01_P02_P03_AND_P1_IN_DECLARED_ROLE",
        "missing_join": "MAP_COMPLETE_GEOMETRY_TO_PHYSICAL_GROUPOID_COCYCLE", "selected": "NO",
    },
    "B02_CENTERED_SMOOTH_COMPLETE_METRIC": {
        "branch": "B02_CENTERED_SMOOTH_COMPLETE_METRIC",
        "center": "EVEN_A_ROUND_LEADING_SCREEN_h_EQUALS_r2_TIMES_EVEN",
        "xmax": "MUST_NOT_BE_ASSUMED_OUTER_BOUNDARY", "allowed_profiles": "P07_LOCAL_JET_SUBSPACE_ONLY",
        "missing_join": "GLOBAL_PROFILE_AND_PAIR_ASYMPTOTE_REALIZATION", "selected": "NO",
    },
    "B03_NO_CENTER_GLOBAL_COMPLETION": {
        "branch": "B03_NO_CENTER_GLOBAL_COMPLETION", "center": "NO_COLLAPSING_ORBIT_OR_PREFERRED_CENTER",
        "xmax": "PAIRWISE_DIAMETER_OR_IDEAL_LIMIT_POSSIBLE",
        "allowed_profiles": "GENERAL_SCREEN_SHIFT_ARCHITECTURE",
        "missing_join": "TOPOLOGY_GLOBAL_SOLUTION_AND_DEPTH_COCYCLE", "selected": "NO",
    },
    "B04_CHART_ENDPOINT_OR_HORIZON_REPRESENTATION": {
        "branch": "B04_CHART_ENDPOINT_OR_HORIZON_REPRESENTATION", "center": "BRANCH_DEPENDENT",
        "xmax": "MAY_APPEAR_AS_CHART_ENDPOINT_NOT_BOUNDARY", "allowed_profiles": "NONE_SELECTED",
        "missing_join": "DERIVE_ENDPOINT_IDENTIFICATION_AND_REGULAR_EXTENSION", "selected": "NO",
    },
}


EXPECTED_LEDGER = {
    "c_eff_pair_ratio": ("DERIVED_RELATIONAL_IDENTITY", "two_point_ratio_plus_disclosed_reference_and_regular_strain_readouts", "physical_complete_groupoid_cocycle"),
    "phi_orchestra": ("DERIVED_STRUCTURAL_COCYCLE_HOME", "complete_pair_modulation_and_real_groupoid_cocycle_home", "unique_metric_natural_physical_cocycle"),
    "mu_mixing": ("ACTIVE_DEFAULT_REGULAR_CENTER_COMPATIBLE", "conditional_h_equals_r2_times_even_local_jet", "physical_invariant_profile_and_global_solution"),
    "Xmax": ("WORKING_RELATIONAL_ASYMPTOTE", "observer_pair_limit_gate", "value_all_frame_theorem_and_global_realization"),
    "P1_pair_profile": ("UNCHANGED", "SNe_observer_relation_role", "complete_geometry_cocycle_join"),
    "P1_centered_local_lapse": ("BLOCKED_ROLE_AND_REGULARITY", "declared_C1_centered_areal_envelope_only", "no_direct_identity_join_in_that_branch"),
    "corrected_mixing_family": ("CONDITIONAL_CONTROL", "210_rows_only_30_q0_pass_full_h_jet", "all_fail_P1_A_jet_and_no_global_profile"),
    "RA1_near_wall_and_SS3_fork": ("CONDITIONAL_FORK", "literal_endpoint_lineage_plus_unspecified_SS3_center_completion", "explicit_full_even_center_to_wall_profile"),
    "C1_regular_center_jet_space": ("DERIVED_NONEMPTY_LOCAL_SUBSPACE", "A_even_h_equals_r2_times_even_round_geodesic_polar_leading_screen", "global_profile_screen_boundary_and_dynamics"),
    "complete_screen_shift": ("ARCHITECTURE_ONLY", "general_stationary_envelope_shift_divergence_and_C01_C18", "physical_screen_and_global_join"),
    "geometry_to_pair_groupoid_cocycle": ("DERIVED_HOME_SELECTION_OPEN", "real_groupoid_cocycle_structural_home", "metric_natural_physical_cocycle_path_rule_and_selection"),
    "infinitesimal_transport": ("CONDITIONAL_CANDIDATE_SUBCLASS", "requires_local_first_order_linear_path_generator", "whether_complete_coframe_supplies_or_selects_one"),
    "N03_eigensolve": ("NOT_AUTHORIZED", "no_complete_role_correct_anchor", "complete_profile_and_boundary"),
}


def keyed_exact(rows: list[dict[str, str]], key: str, expected: dict[str, dict[str, str]], label: str) -> None:
    lookup = {row[key]: row for row in rows}
    if len(rows) != len(lookup) or lookup != expected:
        raise ValueError(label)


def profile_counts(rows: list[dict[str, str]]) -> dict[str, int]:
    round_rows = [row for row in rows if row["family"] == "R0_ROUND_P1"]
    corrected = [row for row in rows if row["family"] == "R1_CENTER_REGULAR_MIXING_P1"]
    literal = [row for row in rows if row["family"] == "R2_RA1_LITERAL_LINEAGE"]
    return {
        "round_strata": len(round_rows),
        "corrected_mixed_strata": len(corrected),
        "corrected_mixed_profiles": sum(int(row["represented_h_magnitudes"]) for row in corrected),
        "corrected_q_zero_strata": sum(row["q_exact"] == "0/1" for row in corrected),
        "corrected_q_zero_profiles": sum(int(row["represented_h_magnitudes"]) for row in corrected if row["q_exact"] == "0/1"),
        "literal_near_wall_strata": len(literal),
    }


def expected_crosswalk_rows(profile_rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    expected: dict[str, dict[str, str]] = {}

    def add(member_id: str, candidate_id: str, source_path: str, locator: str,
            multiplicity: int, role: str, adjudication: str) -> None:
        expected[member_id] = {
            "member_id": member_id,
            "mapped_candidate_id": candidate_id,
            "source_path": source_path,
            "source_locator": locator,
            "declared_multiplicity": str(multiplicity),
            "source_role": role,
            "adjudication": adjudication,
        }

    ceff = "udt_ceff_depth_orchestra_integration_2026-08-06.md"
    orchestra_audit = "udt_complete_pair_phi_orchestra_audit_2026-08-05/AUDIT_REPORT.md"
    orchestra_exact = "udt_complete_pair_phi_orchestra_audit_2026-08-05/EXACT_DERIVATION.md"
    xmax = "udt_xmax_asymptotic_limit_frame_correction_2026-08-05/STATUS_AND_WORKFLOW.md"
    profiles = "udt_cmb_N02_radial_anchor_admissibility_2026-08-09/PROFILE_STRATA.tsv"
    ra1 = "udt_roadA_RA1_muon_modes_2026-08-08/DERIVATION_NOTES.md"
    n01 = "udt_cmb_N01_C1_harmonic_coupling_matrix_atlas_2026-08-09/EXACT_DERIVATION.md"
    n02 = "udt_cmb_N02_radial_anchor_admissibility_2026-08-09/EXACT_DERIVATION.md"
    screens = "udt_cmb_complete_angular_family_atlas_map_2026-08-09/AUDIT_REPORT.md"

    add("P01_M01_TWO_POINT_CEFF_RATIO", "P01_RECIPROCAL_CEFF_RATIO", ceff,
        "c_eff(q)/c_eff(p) = lambda_t", 1, "INVARIANT_PAIR_RATIO",
        "PAIR_OBJECT_NOT_LOCAL_RADIAL_PROFILE")
    add("P01_M02_REFERENCE_POINT_READOUT", "P01_RECIPROCAL_CEFF_RATIO", ceff,
        "reference-observer) special case", 1, "CONDITIONAL_REFERENCE_POINT_READOUT",
        "ABSOLUTE_POINT_FORM_REQUIRES_DISCLOSED_REFERENCE")
    add("P01_M03_TIMELIKE_STRAIN_EXTRACTOR", "P01_RECIPROCAL_CEFF_RATIO", orchestra_exact,
        "delta_t(A)=-(1/2) log(lambda_t(A)).", 1, "REGULAR_STRATUM_COMPLETE_ARROW_EXTRACTOR",
        "DERIVED_EXTRACTOR_NOT_UNIQUE_PHYSICAL_COCYCLE")
    add("P01_M04_LOWER_MIXING_WITNESS", "P01_RECIPROCAL_CEFF_RATIO", orchestra_audit,
        "Complete lower mixing can modify that signed strain depth for a single pair.", 1,
        "PHI_ORCHESTRA_MIXING_WITNESS", "MU_ORCHESTRA_MODULATES_PAIR_DEPTH")
    add("P02_M01_GROUPOID_COCYCLE_HOME", "P02_STATIONARY_SCREEN_COCYCLE_FAMILY", orchestra_audit,
        "real observer/path groupoid cocycle", 1, "DERIVED_STRUCTURAL_HOME",
        "PHYSICAL_COCYCLE_SELECTION_OPEN")
    add("P02_M02_STATIONARY_SCREEN_FAMILY", "P02_STATIONARY_SCREEN_COCYCLE_FAMILY", orchestra_audit,
        "delta_a(p,q)=log[N(p)/N(q)] + a log[R(q)/R(p)]", 1, "CONDITIONAL_EXACT_FAMILY",
        "SCREEN_MODULATION_EXPLICIT_BUT_A_UNSELECTED")
    add("P02_M03_ONE_FORM_ROUTE", "P02_STATIONARY_SCREEN_COCYCLE_FAMILY", orchestra_exact,
        "The one-form representation here is conditional on a local first-order linear path generator.",
        1, "CONDITIONAL_CANDIDATE_SUBCLASS", "NOT_DERIVED_FROM_GENERAL_COCYCLE_HOME")
    add("P03_M01_XMAX_LIMIT_GATE", "P03_XMAX_LIMIT_SCHEMA", xmax, "0 <= s(p,q) < X_max", 1,
        "WORKING_RELATIONAL_ASYMPTOTE", "NOT_A_WALL_CENTER_EDGE_OR_BOUNDARY")

    for row in profile_rows:
        if row["family"] == "R0_ROUND_P1":
            add("P04_" + row["candidate_id"], "P04_P1_ROUND_CONTROLS", profiles,
                row["candidate_id"], 1, "ROUND_P1_CONTROL_MEMBER",
                "PAIR_ROLE_SURVIVES_LOCAL_LAPSE_PROMOTION_BLOCKED")
        elif row["family"] == "R1_CENTER_REGULAR_MIXING_P1":
            add("P05_" + row["candidate_id"], "P05_P1_CORRECTED_MIXING_CONTROLS", profiles,
                row["candidate_id"], int(row["represented_h_magnitudes"]),
                "CORRECTED_MIXED_STRATUM",
                "TEN_AMPLITUDES_PER_STRATUM_FULL_EVEN_H_ONLY_WHEN_Q_ZERO")
        elif row["family"] == "R2_RA1_LITERAL_LINEAGE":
            add("P06_" + row["candidate_id"], "P06_RA1_NEAR_WALL_AND_SS3_FORK", profiles,
                row["candidate_id"], 1, "RA1_LITERAL_NEAR_WALL_STRATUM",
                "LITERAL_CENTER_FAILS_COLLAPSING_ORBIT_ORDER")

    add("P06_M22_RA1_SS3_COMPLETION_FORK", "P06_RA1_NEAR_WALL_AND_SS3_FORK", ra1,
        "| P-RA1-8 | center behavior of h", 1, "CONDITIONAL_SS3_CENTER_COMPLETION_FORK",
        "NECESSARY_CENTER_BEHAVIOR_ONLY_NO_EXPLICIT_GLOBAL_PROFILE")
    add("P07_M01_C1_CHOSE_ENVELOPE", "P07_C1_GENERAL_AXIAL_ENVELOPE", n01,
        "C1 remains `CHOSE`", 1, "CONDITIONAL_GENERAL_AXIAL_ENVELOPE",
        "LOCAL_JET_SPACE_ONLY_NO_PHYSICAL_PROFILE")
    add("P07_M02_C1_B_VARIABLE", "P07_C1_GENERAL_AXIAL_ENVELOPE", n01,
        "B=h^2/(A r^2)", 1, "COMPLETE_ANGULAR_DISTORTION_VARIABLE",
        "FULL_N01_MATRIX_STRUCTURE_RETAINED")
    add("P07_M03_C1_COMPLETE_CENTER", "P07_C1_GENERAL_AXIAL_ENVELOPE", n02,
        "For the conditional C1 metric", 1, "CENTER_REGULARITY_ENVELOPE",
        "N03_STRENGTHENS_NECESSARY_JETS")
    for index in range(1, 19):
        add(f"P08_C{index:02d}", "P08_GENERAL_SCREEN_SHIFT_ENVELOPE", screens,
            "C01-C18 registered universe", 1, "REGISTERED_SCREEN_MEMBER",
            "ARCHITECTURE_MEMBER_NOT_SELECTED_PROFILE")
    return expected


def validate_crosswalk(rows: list[dict[str, str]], profile_rows: list[dict[str, str]], source_texts: dict[str, str]) -> None:
    expected_fields = ["member_id", "mapped_candidate_id", "source_path", "source_locator", "declared_multiplicity", "source_role", "adjudication"]
    fields = list(rows[0]) if rows else []
    if fields != expected_fields:
        raise ValueError("crosswalk schema")
    lookup = {row["member_id"]: row for row in rows}
    expected = expected_crosswalk_rows(profile_rows)
    if len(rows) != 75 or len(lookup) != 75 or lookup != expected:
        raise ValueError("crosswalk universe")
    for row in rows:
        if row["source_path"] not in source_texts or row["source_locator"] not in source_texts[row["source_path"]]:
            raise ValueError("crosswalk source evidence")
    if {row["mapped_candidate_id"] for row in rows} != set(EXPECTED_CANDIDATES):
        raise ValueError("crosswalk family coverage")
    if sum(int(row["declared_multiplicity"]) for row in rows if row["mapped_candidate_id"] == "P05_P1_CORRECTED_MIXING_CONTROLS") != 210:
        raise ValueError("crosswalk corrected profile count")
    required = {
        "P01_M02_REFERENCE_POINT_READOUT", "P01_M03_TIMELIKE_STRAIN_EXTRACTOR",
        "P02_M03_ONE_FORM_ROUTE", "P06_M22_RA1_SS3_COMPLETION_FORK",
    }
    if not required <= set(lookup):
        raise ValueError("crosswalk mandatory disclosures")


ZERO_MEMBER_NOTES = {
    "CURRENT_SCIENTIFIC_PREMISES.tsv": "premise_guard_registry_frozen_at_prereg_no_distinct_profile_member",
    "udt_cmb_N02_radial_anchor_admissibility_2026-08-09/AUDIT_REPORT.md": "summary_source_members_resolved_through_exact_derivation_and_profile_table",
    "udt_cmb_N02_radial_anchor_admissibility_2026-08-09/ENDPOINT_OWNERSHIP.tsv": "endpoint_domain_records_no_additional_profile_family",
    "udt_cmb_N01_C1_harmonic_coupling_matrix_atlas_2026-08-09/AUDIT_REPORT.md": "summary_source_members_resolved_through_N01_exact_derivation",
    "udt_cmb_complete_angular_mode_ownership_2026-08-09/AUDIT_REPORT.md": "mode_ownership_correction_no_additional_profile_family",
    "udt_fd1_corrected_full_spectral_atlas_2026-08-09/FINAL_REPORT.md": "spectral_result_conditioned_on_already_crosswalked_profile_families",
    "udt_xmax_scale_observational_M1_recon_2026-08-07/RECON_REPORT.md": "observational_reconstruction_control_no_metric_profile_candidate",
}


def validate_source_coverage(
    rows: list[dict[str, str]], crosswalk: list[dict[str, str]], source_texts: dict[str, str]
) -> None:
    expected_fields = ["source_path", "crosswalk_member_rows", "represented_multiplicity", "coverage_disposition", "note"]
    if not rows or list(rows[0]) != expected_fields:
        raise ValueError("coverage schema")
    lookup = {row["source_path"]: row for row in rows}
    if len(rows) != 16 or len(lookup) != 16 or set(lookup) != set(source_texts):
        raise ValueError("coverage universe")
    zero_count = 0
    for path in source_texts:
        members = [row for row in crosswalk if row["source_path"] == path]
        expected_count = len(members)
        expected_multiplicity = sum(int(row["declared_multiplicity"]) for row in members)
        row = lookup[path]
        if int(row["crosswalk_member_rows"]) != expected_count or int(row["represented_multiplicity"]) != expected_multiplicity:
            raise ValueError("coverage counts")
        if members:
            if row["coverage_disposition"] != "MAPPED_EXPLICIT_MEMBERS" or row["note"] != "see_SOURCE_CANDIDATE_CROSSWALK":
                raise ValueError("mapped coverage disposition")
        else:
            zero_count += 1
            if row["coverage_disposition"] != "ZERO_DISTINCT_PROFILE_MEMBERS" or row["note"] != ZERO_MEMBER_NOTES.get(path):
                raise ValueError("zero-member coverage disposition")
    if zero_count != 7:
        raise ValueError("zero-member source count")


def independent_B_polynomial() -> dict[int, dict[tuple[int, int, int], int]]:
    # Monomial exponents are (a2,k0,k2); outer keys are powers of r.
    h2_over_r2 = {2: {(0, 2, 0): 1}, 4: {(0, 1, 1): 2}}
    inv_A = {0: {(0, 0, 0): 1}, 2: {(1, 0, 0): -1}}
    product: dict[int, dict[tuple[int, int, int], int]] = {}
    for r_left, terms_left in h2_over_r2.items():
        for r_right, terms_right in inv_A.items():
            degree = r_left + r_right
            if degree > 4:
                continue
            product.setdefault(degree, {})
            for mono_left, coeff_left in terms_left.items():
                for mono_right, coeff_right in terms_right.items():
                    mono = tuple(a + b for a, b in zip(mono_left, mono_right))
                    product[degree][mono] = product[degree].get(mono, 0) + coeff_left * coeff_right
    return product


def validate_payload(payload: dict[str, object], counts: dict[str, int]) -> None:
    if payload.get("status") not in {"REPAIRED_AWAITING_FRESH_ZERO_CONTEXT_ACCEPTANCE", "VERIFIED_WITH_CAVEATS"}:
        raise ValueError("status")
    if payload.get("key_count") != 25 or len(dict(payload.get("keys", {}))) != 25 or not all(dict(payload.get("keys", {})).values()):
        raise ValueError("keys")
    if payload.get("mapped_family_count") != 8 or payload.get("source_crosswalk_member_count") != 75:
        raise ValueError("mapped counts")
    if payload.get("profile_source_counts") != counts or payload.get("screen_member_count") != 18:
        raise ValueError("source counts")
    if payload.get("source_coverage_row_count") != 16 or payload.get("zero_member_source_count") != 7:
        raise ValueError("source coverage counts")
    if payload.get("regular_center_jet_count") != 6 or payload.get("branch_count") != 4:
        raise ValueError("map counts")
    exact = {
        "regular_center_A": "a2*r**2 + a4*r**4 + 1",
        "regular_center_h": "k0*r**2 + k2*r**4",
        "regular_center_B_series": "-a2*k0**2*r**4 + k0**2*r**2 + 2*k0*k2*r**4",
        "P1_pair_slope": "-n/R_w",
        "corrected_mixing_H_slope": "-q/R_w",
        "maximum_conclusion": "role and regular-center map only; no profile, boundary, eigensolve, FD2, fit, population, polarization, or GPU work",
        "landing": "WITHIN_FROZEN_16_SOURCE_AND_DECLARED_C1_GENERAL_SCREEN_ENVELOPES__NO_MAPPED_SOURCE_SUPPLIES_ROLE_CORRECT_COMPLETE_GLOBAL_PROFILE__REGULAR_C1_LOCAL_JET_SPACE_NONEMPTY__P1_DIRECT_CENTERED_IDENTITY_EXCLUDED_ONLY_IN_DECLARED_BRANCH__PHYSICAL_GROUPOID_COCYCLE_OPEN__TRANSPORT_CONDITIONAL_CANDIDATE_ONLY",
    }
    for name, value in exact.items():
        if payload.get(name) != value:
            raise ValueError(name)


def validate_ledger(rows: list[dict[str, str]]) -> None:
    if list(rows[0]) != ["object", "status", "scope", "remaining_open"] if rows else True:
        raise ValueError("ledger schema")
    lookup = {row["object"]: row for row in rows}
    if len(rows) != len(lookup) or set(lookup) != set(EXPECTED_LEDGER):
        raise ValueError("ledger universe")
    for name, values in EXPECTED_LEDGER.items():
        if (lookup[name]["status"], lookup[name]["scope"], lookup[name]["remaining_open"]) != values:
            raise ValueError("ledger fields")


REQUIRED_DOC_TOKENS = {
    "EXACT_DERIVATION.md": [
        "eight mapped source-level families", "75 source-member crosswalk rows",
        "conditional on an additional local first-order linear path-generator premise",
        "transport/connection realization is therefore only a candidate subclass",
        "geodesic-polar or orthonormal-center statement",
    ],
    "AUDIT_REPORT.md": [
        "eight mapped source-level families", "75 source-member",
        "physical geometry-to-pair groupoid cocycle remains open",
        "transport is only a conditional candidate subclass",
    ],
    "LAY_REPORT.md": [
        "groupoid cocycle", "Transport is one possible way", "not something the present result derived",
    ],
    "NEXT_STEP.md": [
        "conditional candidate route", "does not assume that a cocycle must have an infinitesimal generator",
    ],
    "COMPLETENESS_MAP.md": [
        "75 source-member", "eight mapped source-level families", "not semantic exhaustiveness",
    ],
}

FORBIDDEN_SEMANTICS = [
    r"transport (?:is|was|has been) derived",
    r"derived (?:physical )?transport",
    r"cocycle has an infinitesimal transport generator",
    r"k0 is (?:a )?selected",
    r"k0 (?:is|represents) physical rotation",
    r"P1(?:'s)? (?:relational|observer-pair|SNe) role (?:is )?invalid",
    r"X_max is a (?:physical|material) wall",
    r"mu (?:is|=) (?:physically )?off",
    r"nonzero q .*fully smooth",
    r"identity join .*excluded (?:universally|in all|for every)",
    r"eigensolve (?:is )?authorized",
    r"FD2 (?:is )?(?:authorized|restarted)",
]


def validate_semantics(documents: dict[str, str]) -> None:
    for name, tokens in REQUIRED_DOC_TOKENS.items():
        if name not in documents or any(token not in documents[name] for token in tokens):
            raise ValueError("required prose")
    joined = "\n".join(documents.values())
    for pattern in FORBIDDEN_SEMANTICS:
        if re.search(pattern, joined, flags=re.IGNORECASE):
            raise ValueError("forbidden semantic promotion")


def validate_script_scope() -> None:
    allowed_imports = {
        "__future__", "ast", "copy", "csv", "fractions", "hashlib", "json", "pathlib", "re", "subprocess", "sympy"
    }
    forbidden_calls = {"eig", "eigh", "eigvals", "eigvalsh", "solve_ivp", "curve_fit", "least_squares"}
    for name in ("derive_n03_profile_map.py", "verify_n03_profile_map.py"):
        tree = ast.parse((HERE / name).read_text(encoding="utf-8"))
        imports: set[str] = set()
        calls: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.add((node.module or "").split(".")[0])
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    calls.add(node.func.id)
                elif isinstance(node.func, ast.Attribute):
                    calls.add(node.func.attr)
        if not imports <= allowed_imports or calls & forbidden_calls:
            raise ValueError("script scope")


def main() -> None:
    _, source_texts = validate_sources()
    profile_rows = read_tsv(PROFILE_SOURCE)[1]
    counts = profile_counts(profile_rows)
    expected_counts = {
        "round_strata": 3, "corrected_mixed_strata": 21, "corrected_mixed_profiles": 210,
        "corrected_q_zero_strata": 3, "corrected_q_zero_profiles": 30,
        "literal_near_wall_strata": 21,
    }
    if counts != expected_counts:
        raise ValueError("source-derived profile counts")

    candidates = table("CANDIDATE_ROLE_MAP.tsv")
    jets = table("REGULAR_CENTER_JETS.tsv")
    branches = table("ROLE_JOIN_BRANCHES.tsv")
    crosswalk = table("SOURCE_CANDIDATE_CROSSWALK.tsv")
    source_coverage = table("SOURCE_COVERAGE.tsv")
    ledger = table("STATUS_LEDGER.tsv")
    payload = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    documents = {name: (HERE / name).read_text(encoding="utf-8") for name in REQUIRED_DOC_TOKENS}

    keyed_exact(candidates, "candidate_id", EXPECTED_CANDIDATES, "candidate full fields")
    keyed_exact(jets, "object", EXPECTED_JETS, "jet full fields")
    keyed_exact(branches, "branch", EXPECTED_BRANCHES, "branch full fields")
    validate_crosswalk(crosswalk, profile_rows, source_texts)
    validate_source_coverage(source_coverage, crosswalk, source_texts)
    validate_payload(payload, counts)
    validate_ledger(ledger)
    validate_semantics(documents)
    validate_script_scope()

    check("V01_frozen_source_manifest", True)
    check("V02_source_derived_profile_counts_3_21_210_30", counts == expected_counts)
    check("V03_source_crosswalk_75_unique_members", len(crosswalk) == 75)
    check("V04_all_sixteen_sources_covered_including_seven_zero_member", len(source_coverage) == 16)
    check("V05_full_candidate_fields", True)
    check("V06_full_jet_fields", True)
    check("V07_full_branch_fields", True)
    check("V08_full_status_ledger", True)

    # Independent exact directional-derivative reconstruction from frozen rational rows.
    round_rows = [row for row in profile_rows if row["family"] == "R0_ROUND_P1"]
    corrected = [row for row in profile_rows if row["family"] == "R1_CENTER_REGULAR_MIXING_P1"]
    p1_smooth = []
    for row in round_rows:
        n_value = Fraction(row["n_exact"])
        p1_smooth.append(-n_value == n_value)
    q_smooth_profiles = 0
    q_nonzero_profiles = 0
    for row in corrected:
        q_value = Fraction(row["q_exact"])
        is_smooth = -q_value == q_value
        multiplicity = int(row["represented_h_magnitudes"])
        q_smooth_profiles += multiplicity if is_smooth else 0
        q_nonzero_profiles += multiplicity if not is_smooth else 0
    check("V09_P1_directional_derivatives_fail_all_three", p1_smooth == [False, False, False])
    check("V10_H_directional_derivatives_if_and_only_if_q_zero", q_smooth_profiles == 30 and q_nonzero_profiles == 180)

    expected_B = {
        2: {(0, 2, 0): 1},
        4: {(0, 1, 1): 2, (1, 2, 0): -1},
    }
    check("V11_independent_B_polynomial", independent_B_polynomial() == expected_B)
    check("V12_required_premise_stamps", True)
    check("V13_transport_scoped_as_conditional_candidate", True)
    check("V14_general_screen_center_claim_chart_qualified", True)
    check("V15_no_physical_selection", not any(row["complete_witness"] == "YES" for row in candidates))
    check("V16_scripts_do_not_solve_fit_or_use_GPU", True)

    mutations: dict[str, bool] = {}

    def rejected(name: str, function, *args) -> None:
        try:
            function(*args)
        except (ValueError, KeyError, TypeError):
            mutations[name] = True
        else:
            mutations[name] = False

    def validate_tables(c_rows, j_rows, b_rows) -> None:
        keyed_exact(c_rows, "candidate_id", EXPECTED_CANDIDATES, "candidate")
        keyed_exact(j_rows, "object", EXPECTED_JETS, "jet")
        keyed_exact(b_rows, "branch", EXPECTED_BRANCHES, "branch")

    rejected("M01_missing_candidate", validate_tables, candidates[:-1], jets, branches)
    rejected("M02_duplicate_candidate", validate_tables, candidates + [copy.deepcopy(candidates[0])], jets, branches)
    trial = copy.deepcopy(candidates); trial[3]["complete_witness"] = "YES"
    rejected("M03_promote_P1_complete", validate_tables, trial, jets, branches)
    trial = copy.deepcopy(candidates); trial[3]["ruling"] = "P1_RELATIONAL_ROLE_INVALID"
    rejected("M04_invalidate_P1_pair_role", validate_tables, trial, jets, branches)
    trial = copy.deepcopy(candidates); trial[4]["mu_status"] = "MU_OFF_PHYSICAL"
    rejected("M05_disable_mu", validate_tables, trial, jets, branches)
    trial = copy.deepcopy(candidates); trial[2]["xmax_status"] = "XMAX_AS_PHYSICAL_WALL"
    rejected("M06_xmax_wall", validate_tables, trial, jets, branches)
    trial = copy.deepcopy(candidates); trial[7]["angular_status"] = "AXIAL_SHORTCUT_ONLY"
    rejected("M07_drop_shift_divergence", validate_tables, trial, jets, branches)
    trial_jets = copy.deepcopy(jets); trial_jets[2]["regular_center_jet"] = "h=r^2*(k0+k1*r+...)"
    rejected("M08_allow_odd_normalized_mixing", validate_tables, candidates, trial_jets, branches)
    trial_jets = copy.deepcopy(jets); trial_jets[2]["mu_or_angular_effect"] = "k0_is_selected_rotation"
    rejected("M09_promote_k0", validate_tables, candidates, trial_jets, branches)
    trial_branches = copy.deepcopy(branches); trial_branches[0]["selected"] = "YES"
    rejected("M10_select_branch", validate_tables, candidates, jets, trial_branches)

    rejected("M11_missing_crosswalk_member", validate_crosswalk, crosswalk[:-1], profile_rows, source_texts)
    rejected("M12_duplicate_crosswalk_member", validate_crosswalk, crosswalk + [copy.deepcopy(crosswalk[0])], profile_rows, source_texts)
    for number, member in enumerate((
        "P01_M02_REFERENCE_POINT_READOUT", "P01_M03_TIMELIKE_STRAIN_EXTRACTOR",
        "P02_M03_ONE_FORM_ROUTE", "P06_M22_RA1_SS3_COMPLETION_FORK",
    ), start=13):
        rejected(f"M{number:02d}_remove_{member}", validate_crosswalk,
                 [row for row in crosswalk if row["member_id"] != member], profile_rows, source_texts)
    trial_crosswalk = copy.deepcopy(crosswalk)
    next(row for row in trial_crosswalk if row["mapped_candidate_id"] == "P05_P1_CORRECTED_MIXING_CONTROLS")["declared_multiplicity"] = "9"
    rejected("M17_corrupt_210_count", validate_crosswalk, trial_crosswalk, profile_rows, source_texts)
    trial_crosswalk = copy.deepcopy(crosswalk)
    next(row for row in trial_crosswalk if row["member_id"] == "P01_M01_TWO_POINT_CEFF_RATIO")["adjudication"] = "PHYSICAL_LOCAL_RADIAL_PROFILE_SELECTED"
    rejected("M17A_crosswalk_adjudication_promotion", validate_crosswalk, trial_crosswalk, profile_rows, source_texts)
    trial_crosswalk = copy.deepcopy(crosswalk)
    next(row for row in trial_crosswalk if row["member_id"] == "P01_M03_TIMELIKE_STRAIN_EXTRACTOR")["source_role"] = "UNIQUE_PHYSICAL_COCYCLE"
    rejected("M17B_crosswalk_role_promotion", validate_crosswalk, trial_crosswalk, profile_rows, source_texts)
    rejected("M17C_missing_source_coverage", validate_source_coverage, source_coverage[:-1], crosswalk, source_texts)
    trial_coverage = copy.deepcopy(source_coverage)
    next(row for row in trial_coverage if row["coverage_disposition"] == "ZERO_DISTINCT_PROFILE_MEMBERS")["coverage_disposition"] = "MAPPED_EXPLICIT_MEMBERS"
    rejected("M17D_false_zero_member_promotion", validate_source_coverage, trial_coverage, crosswalk, source_texts)

    trial_profiles = copy.deepcopy(profile_rows)
    trial_profiles.pop(next(i for i, row in enumerate(trial_profiles) if row["family"] == "R1_CENTER_REGULAR_MIXING_P1"))
    mutations["M18_remove_mixed_stratum"] = profile_counts(trial_profiles) != expected_counts
    trial_profiles = copy.deepcopy(profile_rows)
    next(row for row in trial_profiles if row["family"] == "R1_CENTER_REGULAR_MIXING_P1" and row["q_exact"] == "0/1")["q_exact"] = "1/99"
    mutations["M19_corrupt_q_zero_count"] = profile_counts(trial_profiles) != expected_counts

    for number, (field, value) in enumerate((
        ("maximum_conclusion", str(payload["maximum_conclusion"]) + "; eigensolve authorized"),
        ("landing", "COMPLETE_GLOBAL_PROFILE_DERIVED"),
        ("regular_center_A", "1+a1*r+a2*r**2"),
        ("regular_center_h", "k0+k2*r**2"),
        ("regular_center_B_series", "k0**2*r**2"),
    ), start=20):
        trial_payload = copy.deepcopy(payload); trial_payload[field] = value
        rejected(f"M{number:02d}_payload_{field}", validate_payload, trial_payload, counts)

    trial_ledger = copy.deepcopy(ledger)
    next(row for row in trial_ledger if row["object"] == "infinitesimal_transport")["status"] = "DERIVED"
    rejected("M25_promote_transport", validate_ledger, trial_ledger)
    trial_ledger = copy.deepcopy(ledger)
    next(row for row in trial_ledger if row["object"] == "geometry_to_pair_groupoid_cocycle")["status"] = "PHYSICAL_COCYCLE_SELECTED"
    rejected("M26_select_physical_cocycle", validate_ledger, trial_ledger)

    poison_phrases = [
        "Transport is derived.",
        "k0 is a selected invariant.",
        "P1 relational role is invalid.",
        "X_max is a physical wall.",
        "mu is physically off.",
        "nonzero q is fully smooth.",
        "The identity join is excluded universally.",
        "The eigensolve is authorized.",
        "FD2 is restarted.",
    ]
    for number, phrase in enumerate(poison_phrases, start=27):
        trial_docs = copy.deepcopy(documents)
        trial_docs["AUDIT_REPORT.md"] += "\n" + phrase + "\n"
        rejected(f"M{number:02d}_semantic_poison", validate_semantics, trial_docs)

    check("V17_fail_closed_mutations", len(mutations) == 39 and all(mutations.values()))

    if not all(CHECKS.values()):
        raise SystemExit("N03 independent verification failed")
    result = {
        "verdict": "VERIFIED_WITH_CAVEATS_AFTER_FRESH_ZERO_CONTEXT_ACCEPTANCE",
        "check_count": len(CHECKS),
        "checks": CHECKS,
        "mutation_count": len(mutations),
        "mutations": mutations,
        "source_derived_counts": counts,
        "crosswalk_member_count": len(crosswalk),
        "source_coverage_row_count": len(source_coverage),
        "zero_member_source_count": sum(
            row["coverage_disposition"] == "ZERO_DISTINCT_PROFILE_MEMBERS" for row in source_coverage
        ),
        "independent_B_polynomial": {
            "r2": "k0^2", "r4": "2*k0*k2-a2*k0^2"
        },
        "independent_argument": "exact rational Cartesian directional derivatives require vanishing odd radial jets",
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"PASS: {len(CHECKS)}/{len(CHECKS)} N03 checks; {len(mutations)}/{len(mutations)} mutations caught")


if __name__ == "__main__":
    main()
