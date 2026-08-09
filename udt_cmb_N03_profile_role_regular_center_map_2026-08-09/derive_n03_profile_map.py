#!/usr/bin/env python3
"""Derive the N03 source crosswalk, role map, and complete-center jet conditions."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
PROFILE_SOURCE = ROOT / "udt_cmb_N02_radial_anchor_admissibility_2026-08-09/PROFILE_STRATA.tsv"
SCREEN_SOURCE = ROOT / "udt_cmb_complete_angular_family_atlas_map_2026-08-09/AUDIT_REPORT.md"
KEYS: dict[str, bool] = {}
PREREG_COMMIT = "c64acaa1"


def key(name: str, condition: object) -> None:
    KEYS[name] = bool(condition)
    print(f"KEY {name}: {KEYS[name]}")


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(name: str, rows: list[dict[str, str]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def source_manifest() -> list[dict[str, str]]:
    rows = read_tsv(HERE / "SOURCE_MANIFEST.tsv")
    if len(rows) != 16 or len({row["path"] for row in rows}) != 16:
        return []
    for row in rows:
        data = (ROOT / row["path"]).read_bytes()
        if hashlib.sha256(data).hexdigest() == row["sha256"]:
            continue
        if row["path"] != "CURRENT_SCIENTIFIC_PREMISES.tsv":
            return []
        historical = subprocess.run(
            ["git", "show", f"{PREREG_COMMIT}:{row['path']}"],
            cwd=ROOT,
            capture_output=True,
            check=False,
        )
        if historical.returncode or hashlib.sha256(historical.stdout).hexdigest() != row["sha256"]:
            return []
    return rows


def profile_counts(profile_rows: list[dict[str, str]]) -> dict[str, int]:
    round_rows = [row for row in profile_rows if row["family"] == "R0_ROUND_P1"]
    corrected_rows = [row for row in profile_rows if row["family"] == "R1_CENTER_REGULAR_MIXING_P1"]
    literal_rows = [row for row in profile_rows if row["family"] == "R2_RA1_LITERAL_LINEAGE"]
    return {
        "round_strata": len(round_rows),
        "corrected_mixed_strata": len(corrected_rows),
        "corrected_mixed_profiles": sum(int(row["represented_h_magnitudes"]) for row in corrected_rows),
        "corrected_q_zero_strata": sum(row["q_exact"] == "0/1" for row in corrected_rows),
        "corrected_q_zero_profiles": sum(
            int(row["represented_h_magnitudes"]) for row in corrected_rows if row["q_exact"] == "0/1"
        ),
        "literal_near_wall_strata": len(literal_rows),
    }


def make_crosswalk(profile_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    def add(
        member_id: str,
        candidate_id: str,
        source_path: str,
        source_locator: str,
        source_role: str,
        adjudication: str,
        multiplicity: int = 1,
    ) -> None:
        rows.append(
            {
                "member_id": member_id,
                "mapped_candidate_id": candidate_id,
                "source_path": source_path,
                "source_locator": source_locator,
                "declared_multiplicity": str(multiplicity),
                "source_role": source_role,
                "adjudication": adjudication,
            }
        )

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
        "c_eff(q)/c_eff(p) = lambda_t", "INVARIANT_PAIR_RATIO",
        "PAIR_OBJECT_NOT_LOCAL_RADIAL_PROFILE")
    add("P01_M02_REFERENCE_POINT_READOUT", "P01_RECIPROCAL_CEFF_RATIO", ceff,
        "reference-observer) special case", "CONDITIONAL_REFERENCE_POINT_READOUT",
        "ABSOLUTE_POINT_FORM_REQUIRES_DISCLOSED_REFERENCE")
    add("P01_M03_TIMELIKE_STRAIN_EXTRACTOR", "P01_RECIPROCAL_CEFF_RATIO", orchestra_exact,
        "delta_t(A)=-(1/2) log(lambda_t(A)).", "REGULAR_STRATUM_COMPLETE_ARROW_EXTRACTOR",
        "DERIVED_EXTRACTOR_NOT_UNIQUE_PHYSICAL_COCYCLE")
    add("P01_M04_LOWER_MIXING_WITNESS", "P01_RECIPROCAL_CEFF_RATIO", orchestra_audit,
        "Complete lower mixing can modify that signed strain depth for a single pair.",
        "PHI_ORCHESTRA_MIXING_WITNESS", "MU_ORCHESTRA_MODULATES_PAIR_DEPTH")

    add("P02_M01_GROUPOID_COCYCLE_HOME", "P02_STATIONARY_SCREEN_COCYCLE_FAMILY", orchestra_audit,
        "real observer/path groupoid cocycle", "DERIVED_STRUCTURAL_HOME",
        "PHYSICAL_COCYCLE_SELECTION_OPEN")
    add("P02_M02_STATIONARY_SCREEN_FAMILY", "P02_STATIONARY_SCREEN_COCYCLE_FAMILY", orchestra_audit,
        "delta_a(p,q)=log[N(p)/N(q)] + a log[R(q)/R(p)]", "CONDITIONAL_EXACT_FAMILY",
        "SCREEN_MODULATION_EXPLICIT_BUT_A_UNSELECTED")
    add("P02_M03_ONE_FORM_ROUTE", "P02_STATIONARY_SCREEN_COCYCLE_FAMILY", orchestra_exact,
        "The one-form representation here is conditional on a local first-order linear path generator.",
        "CONDITIONAL_CANDIDATE_SUBCLASS", "NOT_DERIVED_FROM_GENERAL_COCYCLE_HOME")

    add("P03_M01_XMAX_LIMIT_GATE", "P03_XMAX_LIMIT_SCHEMA", xmax,
        "0 <= s(p,q) < X_max", "WORKING_RELATIONAL_ASYMPTOTE",
        "NOT_A_WALL_CENTER_EDGE_OR_BOUNDARY")

    for row in profile_rows:
        if row["family"] == "R0_ROUND_P1":
            add(f"P04_{row['candidate_id']}", "P04_P1_ROUND_CONTROLS", profiles,
                row["candidate_id"], "ROUND_P1_CONTROL_MEMBER",
                "PAIR_ROLE_SURVIVES_LOCAL_LAPSE_PROMOTION_BLOCKED")
        elif row["family"] == "R1_CENTER_REGULAR_MIXING_P1":
            add(f"P05_{row['candidate_id']}", "P05_P1_CORRECTED_MIXING_CONTROLS", profiles,
                row["candidate_id"], "CORRECTED_MIXED_STRATUM",
                "TEN_AMPLITUDES_PER_STRATUM_FULL_EVEN_H_ONLY_WHEN_Q_ZERO",
                int(row["represented_h_magnitudes"]))
        elif row["family"] == "R2_RA1_LITERAL_LINEAGE":
            add(f"P06_{row['candidate_id']}", "P06_RA1_NEAR_WALL_AND_SS3_FORK", profiles,
                row["candidate_id"], "RA1_LITERAL_NEAR_WALL_STRATUM",
                "LITERAL_CENTER_FAILS_COLLAPSING_ORBIT_ORDER")

    add("P06_M22_RA1_SS3_COMPLETION_FORK", "P06_RA1_NEAR_WALL_AND_SS3_FORK", ra1,
        "| P-RA1-8 | center behavior of h", "CONDITIONAL_SS3_CENTER_COMPLETION_FORK",
        "NECESSARY_CENTER_BEHAVIOR_ONLY_NO_EXPLICIT_GLOBAL_PROFILE")

    add("P07_M01_C1_CHOSE_ENVELOPE", "P07_C1_GENERAL_AXIAL_ENVELOPE", n01,
        "C1 remains `CHOSE`", "CONDITIONAL_GENERAL_AXIAL_ENVELOPE",
        "LOCAL_JET_SPACE_ONLY_NO_PHYSICAL_PROFILE")
    add("P07_M02_C1_B_VARIABLE", "P07_C1_GENERAL_AXIAL_ENVELOPE", n01,
        "B=h^2/(A r^2)", "COMPLETE_ANGULAR_DISTORTION_VARIABLE",
        "FULL_N01_MATRIX_STRUCTURE_RETAINED")
    add("P07_M03_C1_COMPLETE_CENTER", "P07_C1_GENERAL_AXIAL_ENVELOPE", n02,
        "For the conditional C1 metric", "CENTER_REGULARITY_ENVELOPE",
        "N03_STRENGTHENS_NECESSARY_JETS")

    for index in range(1, 19):
        add(f"P08_C{index:02d}", "P08_GENERAL_SCREEN_SHIFT_ENVELOPE", screens,
            "C01-C18 registered universe", "REGISTERED_SCREEN_MEMBER",
            "ARCHITECTURE_MEMBER_NOT_SELECTED_PROFILE")

    return rows


def crosswalk_sources_exist(rows: list[dict[str, str]], manifest_paths: set[str]) -> bool:
    cache: dict[str, str] = {}
    for row in rows:
        path = row["source_path"]
        if path not in manifest_paths:
            return False
        cache.setdefault(path, (ROOT / path).read_text(encoding="utf-8"))
        if row["source_locator"] not in cache[path]:
            return False
    return True


ZERO_MEMBER_SOURCE_NOTES = {
    "CURRENT_SCIENTIFIC_PREMISES.tsv": "premise_guard_registry_frozen_at_prereg_no_distinct_profile_member",
    "udt_cmb_N02_radial_anchor_admissibility_2026-08-09/AUDIT_REPORT.md": "summary_source_members_resolved_through_exact_derivation_and_profile_table",
    "udt_cmb_N02_radial_anchor_admissibility_2026-08-09/ENDPOINT_OWNERSHIP.tsv": "endpoint_domain_records_no_additional_profile_family",
    "udt_cmb_N01_C1_harmonic_coupling_matrix_atlas_2026-08-09/AUDIT_REPORT.md": "summary_source_members_resolved_through_N01_exact_derivation",
    "udt_cmb_complete_angular_mode_ownership_2026-08-09/AUDIT_REPORT.md": "mode_ownership_correction_no_additional_profile_family",
    "udt_fd1_corrected_full_spectral_atlas_2026-08-09/FINAL_REPORT.md": "spectral_result_conditioned_on_already_crosswalked_profile_families",
    "udt_xmax_scale_observational_M1_recon_2026-08-07/RECON_REPORT.md": "observational_reconstruction_control_no_metric_profile_candidate",
}


def make_source_coverage(
    manifest: list[dict[str, str]], crosswalk: list[dict[str, str]]
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source in manifest:
        path = source["path"]
        members = [row for row in crosswalk if row["source_path"] == path]
        if members:
            disposition = "MAPPED_EXPLICIT_MEMBERS"
            note = "see_SOURCE_CANDIDATE_CROSSWALK"
        else:
            disposition = "ZERO_DISTINCT_PROFILE_MEMBERS"
            note = ZERO_MEMBER_SOURCE_NOTES.get(path, "")
        rows.append(
            {
                "source_path": path,
                "crosswalk_member_rows": str(len(members)),
                "represented_multiplicity": str(sum(int(row["declared_multiplicity"]) for row in members)),
                "coverage_disposition": disposition,
                "note": note,
            }
        )
    return rows


def main() -> None:
    manifest = source_manifest()
    key("K01_frozen_source_manifest", bool(manifest))
    manifest_paths = {row["path"] for row in manifest}

    profile_rows = read_tsv(PROFILE_SOURCE)
    counts = profile_counts(profile_rows)
    key("K02_source_derived_three_round", counts["round_strata"] == 3)
    key("K03_source_derived_twenty_one_corrected_strata", counts["corrected_mixed_strata"] == 21)
    key("K04_source_derived_two_hundred_ten_profiles", counts["corrected_mixed_profiles"] == 210)
    key("K05_source_derived_thirty_q_zero_profiles", counts["corrected_q_zero_strata"] == 3 and counts["corrected_q_zero_profiles"] == 30)
    key("K06_source_derived_twenty_one_literal_strata", counts["literal_near_wall_strata"] == 21)

    screen_text = SCREEN_SOURCE.read_text(encoding="utf-8")
    screen_members = [f"C{index:02d}" for index in range(1, 19)]
    key("K07_source_derived_eighteen_screen_members", "All 18 previously registered screen candidates" in screen_text and "C01-C18 registered universe" in screen_text and len(screen_members) == 18)

    r = sp.symbols("r", nonnegative=True)
    a1, a2, a3, a4 = sp.symbols("a1 a2 a3 a4", real=True)
    k0, k1, k2 = sp.symbols("k0 k1 k2", real=True)
    n, q, rw = sp.symbols("n q R_w", positive=True)
    A = 1 + a1 * r + a2 * r**2 + a3 * r**3 + a4 * r**4
    h = k0 * r**2 + k1 * r**3 + k2 * r**4
    radial_cartesian_coefficient = sp.series((1 / A - 1) / r**2, r, 0, 3).removeO().expand()
    normalized_mixing = sp.expand(h / r**2)
    regular_substitution = {a1: 0, a3: 0, k1: 0}
    regular_A = sp.expand(A.subs(regular_substitution))
    regular_h = sp.expand(h.subs(regular_substitution))
    B = sp.series((h**2 / (A * r**2)).subs(regular_substitution), r, 0, 6).removeO().expand()

    key("K08_spatial_metric_rejects_linear_A", radial_cartesian_coefficient.coeff(r, -1) == -a1)
    key("K09_complete_center_even_A_jet", regular_A == 1 + a2 * r**2 + a4 * r**4)
    key("K10_complete_center_even_normalized_mixing_jet", regular_h == k0 * r**2 + k2 * r**4 and normalized_mixing.subs(k1, 0) == k0 + k2 * r**2)
    key("K11_mu_on_compatible_not_required_or_selected", sp.limit(regular_h / r**2, r, 0, dir="+") == k0)
    key(
        "K12_N01_B_returns_to_round_at_center",
        sp.simplify(B - (k0**2 * r**2 + (2 * k0 * k2 - a2 * k0**2) * r**4)) == 0,
    )

    p1_A = (1 - r / rw) ** n
    corrected_H = (1 - r / rw) ** q
    key("K13_P1_pair_profile_has_nonzero_one_sided_slope", sp.diff(p1_A, r).subs(r, 0) == -n / rw)
    key("K14_corrected_mixing_H_slope", sp.diff(corrected_H, r).subs(r, 0) == -q / rw)

    candidates = [
        {
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
        {
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
        {
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
        {
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
        {
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
        {
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
        {
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
        {
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
    ]

    jets = [
        {
            "object": "lapse_lock_A",
            "regular_center_jet": "A=1+a2*r^2+a4*r^4+...",
            "invariant_content": "metric_first_derivatives_removable_and_curvature_finite",
            "mu_or_angular_effect": "conditional_local_representative_has_zero_center_slope",
            "status": "DERIVED_FOR_DECLARED_CENTERED_ENVELOPE",
        },
        {
            "object": "spatial_areal_block",
            "regular_center_jet": "(1/A-1)/r^2=smooth_even",
            "invariant_content": "no_conical_or_directional_center_cusp",
            "mu_or_angular_effect": "independent_of_pair_profile_slope",
            "status": "DERIVED_FOR_DECLARED_CENTERED_ENVELOPE",
        },
        {
            "object": "axial_clock_screen_mixing_h",
            "regular_center_jet": "h=r^2*(k0+k2*r^2+...)",
            "invariant_content": "coordinate_one_form_smooth_on_collapsing_orbit",
            "mu_or_angular_effect": "mu_on_compatible; k0_may_be_nonzero_but_is_not_required_or_selected",
            "status": "DERIVED_FULL_CARTESIAN_JET_IN_CONDITIONAL_h_REALIZATION",
        },
        {
            "object": "N01_dimensionless_angular_distortion_B",
            "regular_center_jet": "B=k0^2*r^2+(2*k0*k2-a2*k0^2)*r^4+...",
            "invariant_content": "complete_angular_matrices_return_to_round_limit_at_center",
            "mu_or_angular_effect": "mixing_reenters_away_from_center_and_normalized_h_may_be_finite",
            "status": "DERIVED_FOR_C1",
        },
        {
            "object": "complete_angular_screen",
            "regular_center_jet": "q_AB=sphere_AB+r^2*q2_AB+... in geodesic-polar/orthonormal-center form",
            "invariant_content": "small_geodesic_spheres_round_at_leading_order",
            "mu_or_angular_effect": "orchestra_modulation_begins_beyond_leading_point_collapse",
            "status": "NECESSARY_SMOOTH_POINT_REQUIREMENT_NOT_ALL_CHARTS_OR_SUFFICIENCY",
        },
        {
            "object": "pair_relation_P1",
            "regular_center_jet": "not_required; one_sided_slope=-n/Rw_allowed_in_pair_separation",
            "invariant_content": "pair_coincidence_is_not_identified_with_manifold_center",
            "mu_or_angular_effect": "complete_pair_orchestra_may_modulate_depth",
            "status": "PAIR_ROLE_ONLY_JOIN_OPEN",
        },
    ]

    branches = [
        {
            "branch": "B01_PAIR_SPACE",
            "center": "PAIR_DIAGONAL_NOT_MANIFOLD_CENTER",
            "xmax": "RELATIONAL_ASYMPTOTE",
            "allowed_profiles": "P01_P02_P03_AND_P1_IN_DECLARED_ROLE",
            "missing_join": "MAP_COMPLETE_GEOMETRY_TO_PHYSICAL_GROUPOID_COCYCLE",
            "selected": "NO",
        },
        {
            "branch": "B02_CENTERED_SMOOTH_COMPLETE_METRIC",
            "center": "EVEN_A_ROUND_LEADING_SCREEN_h_EQUALS_r2_TIMES_EVEN",
            "xmax": "MUST_NOT_BE_ASSUMED_OUTER_BOUNDARY",
            "allowed_profiles": "P07_LOCAL_JET_SUBSPACE_ONLY",
            "missing_join": "GLOBAL_PROFILE_AND_PAIR_ASYMPTOTE_REALIZATION",
            "selected": "NO",
        },
        {
            "branch": "B03_NO_CENTER_GLOBAL_COMPLETION",
            "center": "NO_COLLAPSING_ORBIT_OR_PREFERRED_CENTER",
            "xmax": "PAIRWISE_DIAMETER_OR_IDEAL_LIMIT_POSSIBLE",
            "allowed_profiles": "GENERAL_SCREEN_SHIFT_ARCHITECTURE",
            "missing_join": "TOPOLOGY_GLOBAL_SOLUTION_AND_DEPTH_COCYCLE",
            "selected": "NO",
        },
        {
            "branch": "B04_CHART_ENDPOINT_OR_HORIZON_REPRESENTATION",
            "center": "BRANCH_DEPENDENT",
            "xmax": "MAY_APPEAR_AS_CHART_ENDPOINT_NOT_BOUNDARY",
            "allowed_profiles": "NONE_SELECTED",
            "missing_join": "DERIVE_ENDPOINT_IDENTIFICATION_AND_REGULAR_EXTENSION",
            "selected": "NO",
        },
    ]

    crosswalk = make_crosswalk(profile_rows)
    source_coverage = make_source_coverage(manifest, crosswalk)
    write_tsv("SOURCE_CANDIDATE_CROSSWALK.tsv", crosswalk)
    write_tsv("SOURCE_COVERAGE.tsv", source_coverage)
    write_tsv("CANDIDATE_ROLE_MAP.tsv", candidates)
    write_tsv("REGULAR_CENTER_JETS.tsv", jets)
    write_tsv("ROLE_JOIN_BRANCHES.tsv", branches)

    key("K15_crosswalk_unique_and_source_backed", len(crosswalk) == 75 and len({row["member_id"] for row in crosswalk}) == 75 and crosswalk_sources_exist(crosswalk, manifest_paths))
    key("K16_eight_mapped_families_not_semantic_exhaustiveness_claim", len(candidates) == 8 and {row["mapped_candidate_id"] for row in crosswalk} == {row["candidate_id"] for row in candidates})
    key("K17_reference_readout_disclosed", any(row["member_id"] == "P01_M02_REFERENCE_POINT_READOUT" for row in crosswalk))
    key("K18_strain_extractor_disclosed", any(row["member_id"] == "P01_M03_TIMELIKE_STRAIN_EXTRACTOR" for row in crosswalk))
    key("K19_conditional_one_form_route_disclosed", any(row["member_id"] == "P02_M03_ONE_FORM_ROUTE" for row in crosswalk))
    key("K20_RA1_SS3_fork_disclosed", any(row["member_id"] == "P06_M22_RA1_SS3_COMPLETION_FORK" for row in crosswalk))
    key("K21_no_complete_global_witness", not any(row["complete_witness"] == "YES" for row in candidates))
    key("K22_mu_never_silently_disabled", all(row["mu_status"] != "MU_OFF_PHYSICAL" for row in candidates))
    key("K23_no_branch_or_physical_selection", all(row["selected"] == "NO" for row in branches) and all(row["primary_role"] != "ROLE_JOIN_DERIVED" for row in candidates))
    key("K24_full_angular_correction_retained", "SHIFT_DIVERGENCE" in candidates[7]["angular_status"])
    key(
        "K25_all_sixteen_sources_have_explicit_coverage_disposition",
        len(source_coverage) == 16
        and len({row["source_path"] for row in source_coverage}) == 16
        and sum(row["coverage_disposition"] == "ZERO_DISTINCT_PROFILE_MEMBERS" for row in source_coverage) == 7
        and all(row["note"] for row in source_coverage),
    )

    if not all(KEYS.values()):
        raise SystemExit("N03 profile-role derivation failed")

    result = {
        "status": "VERIFIED_WITH_CAVEATS",
        "key_count": len(KEYS),
        "keys": KEYS,
        "mapped_family_count": len(candidates),
        "source_crosswalk_member_count": len(crosswalk),
        "source_coverage_row_count": len(source_coverage),
        "zero_member_source_count": sum(
            row["coverage_disposition"] == "ZERO_DISTINCT_PROFILE_MEMBERS" for row in source_coverage
        ),
        "profile_source_counts": counts,
        "screen_member_count": len(screen_members),
        "regular_center_jet_count": len(jets),
        "branch_count": len(branches),
        "regular_center_A": str(regular_A),
        "regular_center_h": str(regular_h),
        "regular_center_B_series": str(B),
        "P1_pair_slope": str(sp.diff(p1_A, r).subs(r, 0)),
        "corrected_mixing_H_slope": str(sp.diff(corrected_H, r).subs(r, 0)),
        "maximum_conclusion": "role and regular-center map only; no profile, boundary, eigensolve, FD2, fit, population, polarization, or GPU work",
        "landing": "WITHIN_FROZEN_16_SOURCE_AND_DECLARED_C1_GENERAL_SCREEN_ENVELOPES__NO_MAPPED_SOURCE_SUPPLIES_ROLE_CORRECT_COMPLETE_GLOBAL_PROFILE__REGULAR_C1_LOCAL_JET_SPACE_NONEMPTY__P1_DIRECT_CENTERED_IDENTITY_EXCLUDED_ONLY_IN_DECLARED_BRANCH__PHYSICAL_GROUPOID_COCYCLE_OPEN__TRANSPORT_CONDITIONAL_CANDIDATE_ONLY",
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        f"PASS: {len(KEYS)}/{len(KEYS)} N03 keys; {len(candidates)} mapped families; "
        f"{len(crosswalk)} source members; {len(jets)} jets; {len(branches)} branches"
    )


if __name__ == "__main__":
    main()
