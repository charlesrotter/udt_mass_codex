#!/usr/bin/env python3
"""Render the preregistered CMB observation-query and branch-ownership map.

This deterministic renderer verifies the frozen source manifest and family universe,
then materializes source-audited classifications. It does not algorithmically derive
semantic ownership from natural-language source texts. It does not solve an eigenvalue
problem, load observational arrays, rank families, or fit any quantity.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def verify_source_manifest() -> list[dict[str, str]]:
    rows = read_tsv(HERE / "SOURCE_MANIFEST.tsv")
    if len(rows) != 16:
        raise RuntimeError(f"expected 16 frozen sources, got {len(rows)}")
    for row in rows:
        path = ROOT / row["path"]
        actual = sha256(path)
        if actual != row["sha256"]:
            raise RuntimeError(f"source hash mismatch: {row['path']}")
    return rows


QUERY_LAYERS = [
    {
        "layer_id": "Q00",
        "object": "ORDERED_OBSERVER_SKY_QUERY",
        "mathematical_home": "typed_observer_event_frame_and_celestial_screen",
        "required_for": "all_CMB_observables",
        "current_owner": "OPEN_PHYSICAL_CMB_QUERY",
        "what_is_banked": "query_architecture_only",
        "status": "OPEN",
    },
    {
        "layer_id": "Q01",
        "object": "REGULAR_BRANCH_REALIZATION",
        "mathematical_home": "query_indexed_pair_immersion_or_correspondence",
        "required_for": "connect_remote_pattern_to_observer",
        "current_owner": "NO_F00_F17_FAMILY_SUPPLIES_A_CMB_PAIR_IMMERSION",
        "what_is_banked": "conditional_ambient_metric_families",
        "status": "OPEN",
    },
    {
        "layer_id": "Q02",
        "object": "TERMINAL_PAIR_METRIC",
        "mathematical_home": "first_fundamental_form_h_equal_F_pullback_g",
        "required_for": "kappa_phi_beta_pair_state",
        "current_owner": "DERIVED_ONCE_F_IS_SUPPLIED",
        "what_is_banked": "exact_terminal_decomposition",
        "status": "DERIVED_CONDITIONAL",
    },
    {
        "layer_id": "Q03",
        "object": "PAIR_CONE_READOUT",
        "mathematical_home": "terminal_pair_metric",
        "required_for": "inter_observer_clock_ruler_ratio",
        "current_owner": "c_eff_pair_over_c_E_equal_exp_minus_2_phi_pair",
        "what_is_banked": "conditional_pair_readout_not_local_speed",
        "status": "CONDITIONAL",
    },
    {
        "layer_id": "Q04",
        "object": "OBSERVER_SKY_ANGULAR_MAP",
        "mathematical_home": "screen_Jacobi_or_equivalent_query_map",
        "required_for": "remote_scale_to_observed_multipole",
        "current_owner": "OPEN_FOR_PHYSICAL_CMB_QUERY",
        "what_is_banked": "conditional_screen_geometries_and_separate_Jacobi_controls",
        "status": "OPEN",
    },
    {
        "layer_id": "Q05",
        "object": "AMBIENT_TRANSPORT",
        "mathematical_home": "path_groupoid_functor_after_path_is_supplied",
        "required_for": "carry_complete_frame_or_orientation_sensitive_data",
        "current_owner": "METRIC_CONDITIONAL_ON_PATH",
        "what_is_banked": "no_physical_CMB_path",
        "status": "CONDITIONAL_PATH_ONLY",
    },
    {
        "layer_id": "Q06",
        "object": "NORMAL_SCREEN_TRANSPORT",
        "mathematical_home": "normal_bundle_of_supplied_pair_immersion",
        "required_for": "polarization_and_screen_orientation_memory",
        "current_owner": "OPEN_FOR_PHYSICAL_CMB_QUERY",
        "what_is_banked": "conditional_normal_transport_on_non_CMB_query_controls",
        "status": "OPEN",
    },
    {
        "layer_id": "Q07",
        "object": "CONDITIONAL_MODE_OPERATOR",
        "mathematical_home": "chosen_scalar_operator_domain_and_boundary_realization",
        "required_for": "candidate_mode_locations",
        "current_owner": "C0_SOLVED_C1_MATRIX_ONLY_GENERAL_SCREEN_FORM_ONLY",
        "what_is_banked": "scalar_controls_not_native_dynamics",
        "status": "CHOSE_CONDITIONAL",
    },
    {
        "layer_id": "Q08",
        "object": "MODE_TO_MULTIPOLE_PROJECTION",
        "mathematical_home": "observer_sky_evaluation_map",
        "required_for": "TT_peak_position_comparison",
        "current_owner": "RA2_TWO_PARAMETER_AFFINE_DIAGNOSTIC_ONLY",
        "what_is_banked": "attributed_compatibility_not_prediction",
        "status": "CONDITIONAL_WEAK",
    },
    {
        "layer_id": "Q09",
        "object": "STATE_SOURCE_COVARIANCE",
        "mathematical_home": "mode_space_or_response_kernel",
        "required_for": "which_modes_have_nonzero_power_and_peak_heights",
        "current_owner": "NONE_FROM_METRIC_ALONE",
        "what_is_banked": "absence_explicitly_proved_in_mode_ownership_audit",
        "status": "OPEN",
    },
    {
        "layer_id": "Q10",
        "object": "SCALAR_TEMPERATURE_SKY_FIELD",
        "mathematical_home": "real_scalar_on_observer_celestial_screen",
        "required_for": "a_lm_and_C_ell_TT",
        "current_owner": "OBSERVED_MAP_TYPE_BUT_NO_NATIVE_PREDICTION_LAW",
        "what_is_banked": "published_peak_locations_only",
        "status": "OBSERVED_READOUT_OPEN_THEORY",
    },
    {
        "layer_id": "Q11",
        "object": "POLARIZATION_SKY_FIELD",
        "mathematical_home": "orientation_sensitive_screen_field",
        "required_for": "TE_EE_BB_channels",
        "current_owner": "NONE",
        "what_is_banked": "scalar_operator_only",
        "status": "OPEN",
    },
    {
        "layer_id": "Q12",
        "object": "XMAX_ASYMPTOTIC_GUARD",
        "mathematical_home": "observer_pair_positional_dilation_limit",
        "required_for": "global_branch_admissibility_only",
        "current_owner": "WORKING_FRAME",
        "what_is_banked": "not_local_wall_not_selector_not_value",
        "status": "WORKING",
    },
    {
        "layer_id": "Q13",
        "object": "P1_SNE_COMPATIBILITY_ANCHOR",
        "mathematical_home": "low_redshift_observer_pair_profile",
        "required_for": "cross_anchor_after_a_CMB_pair_profile_exists",
        "current_owner": "CONDITIONAL_SNE_PAIR_ROLE_ONLY",
        "what_is_banked": "must_not_be_copied_into_centered_CMB_lapse",
        "status": "CONDITIONAL",
    },
]


OBSERVABLE_ROWS = [
    {
        "observable": "FD1_RA2_AFFINE_TT_POSITION_DIAGNOSTIC",
        "definition": "fit_conditional_scalar_frequencies_to_seven_attributed_TT_peak_locations",
        "endpoint_pair": "NOT_OWNED",
        "screen_Jacobi": "REPLACED_BY_TWO_FITTED_AFFINE_FREEDOMS",
        "ambient_transport": "NOT_READ",
        "normal_transport": "NOT_READ",
        "operator_modes": "C0_CONDITIONAL_10080_ROOT_ATLAS",
        "source_population": "ABSENT",
        "maximum_status": "ATTRIBUTED_COMPATIBILITY_ONLY",
    },
    {
        "observable": "PHYSICAL_TT_PEAK_POSITIONS",
        "definition": "local_maxima_of_observed_scalar_angular_power_spectrum",
        "endpoint_pair": "REQUIRED_CONTEXT_NOT_SUFFICIENT",
        "screen_Jacobi": "REQUIRED_FOR_NATIVE_REMOTE_TO_SKY_MAP",
        "ambient_transport": "CONDITIONAL_NOT_DIRECT_SCALAR_ROTATION_READ",
        "normal_transport": "PURE_SO2_ROTATION_NOT_DIRECTLY_READ_BY_SCALAR_TT",
        "operator_modes": "REQUIRED_IF_CAVITY_MODE_INTERPRETATION_IS_USED",
        "source_population": "REQUIRED_TO_DECIDE_WHICH_MODES_FORM_PEAKS",
        "maximum_status": "OPEN",
    },
    {
        "observable": "PHYSICAL_TT_HEIGHTS_AND_OVERALL_AMPLITUDE",
        "definition": "nonzero_values_of_observed_scalar_angular_power",
        "endpoint_pair": "REQUIRED_CONTEXT_NOT_SUFFICIENT",
        "screen_Jacobi": "REQUIRED_FOR_ANGULAR_MAP",
        "ambient_transport": "CONDITIONAL_RESPONSE_CONTEXT",
        "normal_transport": "NOT_DIRECT_FOR_SCALAR_TT",
        "operator_modes": "NOT_SUFFICIENT",
        "source_population": "REQUIRED_WITH_NORMALIZATION",
        "maximum_status": "OPEN_SOURCE_SIDE",
    },
    {
        "observable": "PHYSICAL_TE_EE_BB_POLARIZATION",
        "definition": "orientation_sensitive_angular_correlations",
        "endpoint_pair": "REQUIRED_CONTEXT_NOT_SUFFICIENT",
        "screen_Jacobi": "REQUIRED",
        "ambient_transport": "REQUIRED_OR_EQUIVALENT_CARRY",
        "normal_transport": "REQUIRED_OR_EQUIVALENT_SCREEN_CONNECTION",
        "operator_modes": "SCALAR_OPERATOR_INSUFFICIENT",
        "source_population": "REQUIRED_SPIN_SENSITIVE_SOURCE",
        "maximum_status": "OPEN",
    },
]


def angular_status(fid: str) -> str:
    if fid == "F00":
        return "PARTIAL_EQUATORIAL_SLICE_ONLY"
    if fid == "F01":
        return "ROUND_SO3_CONTROL"
    if fid == "F02":
        return "CONDITIONAL_COMPLETE_C1_SCREEN"
    if fid in {"F03", "F04"}:
        return "GENERAL_SCREEN_ENVELOPE_NO_SELECTED_PROFILE"
    if fid in {f"F{i:02d}" for i in range(5, 15)}:
        return "CONDITIONAL_S3_CONTROL_NO_WRL_SPLICE"
    if fid == "F15":
        return "DEGENERATE_SCREEN_NO_INVERSE"
    if fid == "F16":
        return "GLOBAL_NON_TORIC_AVAILABILITY_COUNTERCONTROL"
    if fid == "F17":
        return "GENERAL_POSITIVE_SCREEN_ALGEBRA_ENVELOPE"
    raise KeyError(fid)


def spectral_status(fid: str) -> str:
    if fid == "F00":
        return "C0_SCALAR_ROOTS_SOLVED_CONDITIONALLY"
    if fid == "F01":
        return "ROUND_CONTROL_OPERATOR_NO_SELECTED_BOUNDARY"
    if fid == "F02":
        return "C1_COUPLING_MATRICES_ONLY_NO_EIGENSOLVE"
    if fid in {"F03", "F04"}:
        return "OPERATOR_FORM_ONLY_NO_PROFILE_OR_SOLVE"
    if fid in {f"F{i:02d}" for i in range(5, 17)}:
        return "NO_AUTHORIZED_WRL_S3_CMB_OPERATOR_SPLICE"
    if fid == "F17":
        return "ALGEBRA_ONLY_NO_PHYSICAL_COMPLETION"
    raise KeyError(fid)


def build_family_rows(source_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    family_source = next(row for row in source_rows if row["role"] == "frozen_F00_F17_universe")
    families = read_tsv(ROOT / family_source["path"])
    ids = [row["family_id"] for row in families]
    expected = [f"F{i:02d}" for i in range(18)]
    if ids != expected:
        raise RuntimeError(f"family universe is not exact F00-F17: {ids}")

    result = []
    for row in families:
        fid = row["family_id"]
        result.append(
            {
                "family_id": fid,
                "name": row["name"],
                "source_provenance": row["provenance"],
                "source_disposition": row["disposition"],
                "ambient_regular_geometry": (
                    "NOT_REGULAR_DEGENERATE" if fid == "F15" else "CONDITIONAL_OR_CONTROL_ONLY"
                ),
                "physical_CMB_pair_query": "OPEN_NOT_SUPPLIED",
                "terminal_kappa_phi_beta": "OPEN_UNTIL_CMB_PAIR_IMMERSION_IS_SUPPLIED",
                "angular_screen_geometry": angular_status(fid),
                "observer_sky_Jacobi_map": "OPEN_NOT_SUPPLIED",
                "ambient_transport": "CONDITIONAL_AFTER_PATH_NOT_SELECTED",
                "normal_transport": "OPEN_UNTIL_PAIR_IMMERSION_IS_SUPPLIED",
                "spectral_operator": spectral_status(fid),
                "mode_population_or_source": "OPEN_NONE_FROM_METRIC_ALONE",
                "TT_position_readout": (
                    "ATTRIBUTED_TWO_PARAMETER_COMPATIBILITY_ONLY" if fid == "F00" else "NOT_PERFORMED"
                ),
                "TT_power_prediction": "OPEN",
                "polarization_prediction": "OPEN",
                "Xmax_role": "ASYMPTOTIC_GUARD_ONLY_NOT_SELECTOR",
                "family_rank": "UNRANKED",
            }
        )
    return result


def main() -> None:
    sources = verify_source_manifest()
    family_rows = build_family_rows(sources)

    write_tsv(HERE / "QUERY_LAYER_ATLAS.tsv", list(QUERY_LAYERS[0]), QUERY_LAYERS)
    write_tsv(HERE / "OBSERVABLE_CHANNEL_REQUIREMENTS.tsv", list(OBSERVABLE_ROWS[0]), OBSERVABLE_ROWS)
    write_tsv(HERE / "FAMILY_REALIZATION_ATLAS.tsv", list(family_rows[0]), family_rows)

    result = {
        "status": "COMPLETE_CMB_QUERY_ARCHITECTURE_MAPPED__NO_COMPLETE_PHYSICAL_REALIZATION_OWNED",
        "source_count": len(sources),
        "source_hashes_verified": True,
        "family_count": len(family_rows),
        "family_ids": [row["family_id"] for row in family_rows],
        "query_layer_count": len(QUERY_LAYERS),
        "observable_class_count": len(OBSERVABLE_ROWS),
        "complete_physical_CMB_query_count": sum(
            row["physical_CMB_pair_query"] != "OPEN_NOT_SUPPLIED" for row in family_rows
        ),
        "families_ranked": 0,
        "families_with_TT_power_prediction": 0,
        "families_with_polarization_prediction": 0,
        "historical_position_diagnostic_families": ["F00"],
        "c0_root_count_banked": 10080,
        "c1_matrix_element_count_banked": 15420,
        "smallest_next_calculation": (
            "construct_one_declared_CMB_observer_sky_query_on_each_of_the_round_F01_and_"
            "axis_regular_F02_controls_and_derive_the_same_querys_screen_Jacobi_map_before_any_eigensolve"
        ),
        "maximum_conclusion": (
            "architecture_and_ownership_map_only_no_CMB_prediction_screen_selection_FD2_restart_"
            "bootstrap_local_signalling_or_native_dynamics"
        ),
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
