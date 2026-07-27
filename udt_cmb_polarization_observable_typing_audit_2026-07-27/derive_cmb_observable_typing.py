#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
MAP_LEVEL = {"O01", "O02", "O03", "O09", "O10", "O11", "O12"}
ISOTROPIC_SPECTRA = {"O04", "O05", "O06", "O07", "O08"}
DIRECTION_RETAINED = MAP_LEVEL


def write_table(name: str, rows: list[dict[str, str]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def observable_gate_status(observable_id: str, gate_id: str) -> tuple[str, str]:
    if gate_id == "G01":
        return "DEFINED_EXTERNAL_MATHEMATICAL_TYPE", "spin_field_map_correlation_or_spectrum_definition_is_available_as_readout_math"
    if gate_id == "G02":
        return "AVAILABLE_CONDITIONAL_GIVEN_TYPED_SCREEN", "metric_supplies_screen_geometry_only_after_observer_path_and_screen_inputs"
    if gate_id == "G03":
        return "AVAILABLE_CONDITIONAL_GEOMETRIC_ACTION", "screen_transport_can_act_upstream_but_is_not_physical_polarization_transport"
    if gate_id == "G04":
        return "OPEN_UNSELECTED_EXTENSION", "seven_direction_registered_extension_tangent_has_no_active_selector"
    if gate_id == "G05":
        return "OPEN_PHYSICAL_DOMAIN", "observer_event_path_and_screen_basis_are_not_selected"
    if gate_id == "G06":
        return "OPEN_PHYSICAL_CARRIER", "geometric_screen_tensor_is_not_automatically_native_polarization"
    if gate_id == "G07":
        return "OPEN_NATIVE_SOURCE", "no_native_matter_polarization_generation_or_initial_data_law"
    if gate_id == "G08":
        return "OPEN_GLOBAL_SKY", "whole_sky_patches_topology_boundary_and_transition_law_are_unselected"
    if gate_id == "G09":
        if observable_id in {"O01", "O12"}:
            return "BASIS_COVARIANT_NOT_INVARIANT", "Q_U_require_declared_screen_basis_and_calibration"
        if observable_id in {"O02", "O03", "O04", "O05", "O06", "O07", "O08", "O10"}:
            return "AVAILABLE_CONDITIONAL_GLOBAL_DECOMPOSITION", "E_B_or_harmonic_readout_descends_only_after_global_sky_mask_and_basis_rules"
        if observable_id == "O09":
            return "OPEN_REFERENCE_AND_CALIBRATION", "rotation_requires_source_reference_and_instrument_angle_control"
        if observable_id == "O11":
            return "AVAILABLE_CONDITIONAL_PARALLEL_BASIS", "real_space_spin_correlation_requires_a_declared_basis_transport_rule"
    if gate_id == "G10":
        return "OPEN_NATIVE_STATISTICAL_OR_SINGLE_SKY_RULE", "observed_single_sky_does_not_supply_a_UDT_ensemble_or_deterministic_prediction"
    if gate_id == "G11":
        return "EXTERNAL_SEPARATION_REQUIRED", "frequency_noise_mask_foreground_and_calibration_controls_remain_external"
    if gate_id == "G12":
        return "NOT_SELECTED_UNIQUE_SIGNATURE", "unresolved_extension_carrier_source_and_global_chain_prevent_uniqueness"
    if gate_id == "G13":
        if observable_id in DIRECTION_RETAINED:
            if observable_id == "O11":
                return "DIRECTIONAL_INFORMATION_RETAINED", "only_full_unaveraged_pair_and_orientation_dependent_spin_correlation_retains_direction__isotropic_xi_theta_is_compressed"
            return "DIRECTIONAL_INFORMATION_RETAINED", "map_off_diagonal_rotation_or_real_space_object_retains_location_or_m_structure"
        return "DIRECTIONAL_INFORMATION_COMPRESSED", "isotropic_C_ell_sum_over_m_discards_phase_and_direction"
    if gate_id == "G14":
        return "NOT_AVAILABLE_UDT_PREDICTION", "at_least_extension_domain_carrier_source_and_completion_are_open"
    raise AssertionError((observable_id, gate_id))


def capability_status(extension_id: str, observable_id: str) -> tuple[str, str]:
    if extension_id == "E01":
        return "INCOMPLETE_BASE", "founded_two_channel_action_has_no_complete_screen_action"
    if extension_id == "E10":
        return "INACTIVE_PREMISE", "strong_local_CSN_reading_is_not_active_authority"
    if extension_id == "E11":
        return "DESCENT_LAYER_OPEN", "local_Lorentz_physical_operation_is_unselected"
    if extension_id == "E12":
        return "GLOBAL_LAYER_OPEN", "profile_path_boundary_and_sky_completion_are_unselected"
    if observable_id in ISOTROPIC_SPECTRA:
        return "DOWNSTREAM_SOURCE_AND_COMPRESSION_BLOCKED", "spectrum_requires_source_statistical_rule_and_loses_directional_extension_information"
    if extension_id == "E06":
        return "POINTWISE_SPECTATOR_CONTROL_ONLY", "conditional_pointwise_witness_only__local_Lorentz_descent_path_and_global_sky_open"
    if extension_id in {"E07", "E08"}:
        return "POINTWISE_COUNTERFAMILY_CONTROL_ONLY", "exact_pointwise_nonuniqueness_control_only__local_Lorentz_descent_path_and_global_sky_open"
    return "POINTWISE_UPSTREAM_GEOMETRIC_POTENTIAL_ONLY", "pointwise_complete_extension_class_only__local_Lorentz_descent_path_and_global_sky_open"


def exact_controls() -> dict[str, object]:
    a, b = sp.symbols("a b", real=True)

    def rotation(angle):
        return sp.Matrix([[sp.cos(2 * angle), -sp.sin(2 * angle)], [sp.sin(2 * angle), sp.cos(2 * angle)]])

    group_residual = sp.simplify(rotation(a) * rotation(b) - rotation(a + b))
    reverse_residual = sp.simplify(rotation(a) * rotation(-a) - sp.eye(2))

    # Two distinct real-harmonic coefficient vectors have the same isotropic C_l.
    map_a = [sp.Integer(1), 0, 0, 0, 0]
    map_b = [0, sp.Integer(1), 0, 0, 0]
    cl_a = sum(x * x for x in map_a) / sp.Integer(5)
    cl_b = sum(x * x for x in map_b) / sp.Integer(5)

    # Observed rotation is unchanged when physical and calibration pieces trade equally.
    physical_1, calibration_1 = sp.Integer(1), sp.Integer(2)
    physical_2, calibration_2 = sp.Integer(2), sp.Integer(1)

    # One measured B amplitude admits multiple source/geometry/foreground decompositions.
    b_decomposition_1 = (sp.Integer(3), sp.Integer(0), sp.Integer(0))
    b_decomposition_2 = (sp.Integer(1), sp.Integer(1), sp.Integer(1))

    return {
        "spin2_rotation_composition_exact": group_residual == sp.zeros(2),
        "spin2_rotation_reversal_exact": reverse_residual == sp.zeros(2),
        "power_spectrum_noninjective_witness": map_a != map_b and sp.simplify(cl_a - cl_b) == 0,
        "power_spectrum_witness_C_l": str(cl_a),
        "calibration_rotation_degeneracy_witness": physical_1 + calibration_1 == physical_2 + calibration_2,
        "schematic_B_component_sum_nonuniqueness_sanity_check": sum(b_decomposition_1) == sum(b_decomposition_2),
        "uniform_rotation_EB_matrix": [["cos(2a)", "-sin(2a)"], ["sin(2a)", "cos(2a)"]],
    }


def main() -> int:
    with (HERE / "OBSERVABLE_UNIVERSE.tsv").open(newline="", encoding="utf-8") as handle:
        observables = list(csv.DictReader(handle, delimiter="\t"))
    with (HERE / "GATE_SCHEMA.tsv").open(newline="", encoding="utf-8") as handle:
        gates = list(csv.DictReader(handle, delimiter="\t"))
    with (HERE / "EXTENSION_ROW_UNIVERSE.tsv").open(newline="", encoding="utf-8") as handle:
        extensions = list(csv.DictReader(handle, delimiter="\t"))
    assert len(observables) == len(extensions) == 12 and len(gates) == 14

    observable_gate_rows = []
    for observable in observables:
        for gate in gates:
            status, reason = observable_gate_status(observable["observable_id"], gate["gate_id"])
            observable_gate_rows.append({
                "observable_id": observable["observable_id"], "gate_id": gate["gate_id"],
                "status": status, "reason": reason,
            })
    assert len(observable_gate_rows) == 168
    write_table("OBSERVABLE_GATE_MATRIX.tsv", observable_gate_rows)

    capability_rows = []
    for extension in extensions:
        for observable in observables:
            status, reason = capability_status(extension["extension_id"], observable["observable_id"])
            capability_rows.append({
                "extension_id": extension["extension_id"], "observable_id": observable["observable_id"],
                "status": status, "reason": reason,
            })
    assert len(capability_rows) == 144
    write_table("EXTENSION_OBSERVABLE_CAPABILITY.tsv", capability_rows)

    dependency_rows = [
        {"link_id": "D01", "object": "complete_metric_and_coframe_atlas", "status": "DERIVED_CLASSIFICATION_OPEN_SELECTION", "layer": "L1", "depends_on": "founded_pair", "blocks": "D03"},
        {"link_id": "D02", "object": "physical_observer_event_path_screen_variation_domain", "status": "OPEN", "layer": "L1", "depends_on": "complete_metric", "blocks": "D03"},
        {"link_id": "D03", "object": "geometric_screen_transport_and_holonomy", "status": "AVAILABLE_CONDITIONAL_GIVEN_D01_D02", "layer": "L1", "depends_on": "D01;D02", "blocks": "D05"},
        {"link_id": "D04", "object": "native_physical_polarization_carrier", "status": "OPEN", "layer": "L3", "depends_on": "native_field_identification", "blocks": "D05"},
        {"link_id": "D05", "object": "native_polarization_source_and_propagation_law", "status": "OPEN", "layer": "L3", "depends_on": "D03;D04;native_matter_source", "blocks": "D06"},
        {"link_id": "D06", "object": "native_global_sky_Q_U_section", "status": "OPEN", "layer": "L3", "depends_on": "D05;global_completion", "blocks": "D09"},
        {"link_id": "D07", "object": "observed_external_Q_U_maps", "status": "OBSERVED_EXTERNAL_READOUT", "layer": "L2", "depends_on": "instrument_component_separation", "blocks": "comparison_requires_D10"},
        {"link_id": "D08", "object": "E_B_and_spin_correlation_mathematical_transforms", "status": "DEFINED_EXTERNAL_MATHEMATICAL_TYPE", "layer": "L0", "depends_on": "supplied_Q_U_and_global_analysis_domain", "blocks": "none_as_math"},
        {"link_id": "D09", "object": "native_statistical_or_single_sky_prediction", "status": "OPEN", "layer": "L3", "depends_on": "D06;native_ensemble_or_deterministic_rule", "blocks": "D10"},
        {"link_id": "D10", "object": "instrument_foreground_calibrated_comparison", "status": "OBSERVED_EXTERNAL_READOUT_ONLY", "layer": "L2", "depends_on": "D07;D08;D09;frequency_noise_mask_calibration", "blocks": "UDT_prediction_until_D01_D09_close"},
    ]
    write_table("DEPENDENCY_CHAIN.tsv", dependency_rows)

    ranking_rows = [
        {"rank": "1", "observable_ids": "O09;O10;O11", "tier": "GEOMETRY_RICH_FUTURE_GUIDEPOST_TIED", "why": "retains_direction_path_screen_or_holonomy_information__O11_only_if_unaveraged_pair_orientation_dependent", "current_use": "TYPE_AND_FALSIFICATION_CONTRACT_ONLY"},
        {"rank": "2", "observable_ids": "O01;O02;O03;O12", "tier": "MAP_LEVEL_CONDITIONAL_GUIDEPOST", "why": "retains_more_structure_than_C_l_but_needs_carrier_global_basis_and_calibration", "current_use": "EXTERNAL_MAP_COMPARISON_ONLY"},
        {"rank": "3", "observable_ids": "O07;O08;O05", "tier": "ROTATION_OR_B_MODE_SPECTRAL_GUIDEPOST", "why": "sensitive_but_degenerate_with_source_lensing_foregrounds_and_angle_calibration", "current_use": "DO_NOT_ATTRIBUTE_TO_UDT"},
        {"rank": "4", "observable_ids": "O04;O06", "tier": "SOURCE_TRANSFER_DOMINATED_SPECTRA", "why": "peak_phase_and_amplitude_need_native_source_history_and_isotropic_compression_loses_direction", "current_use": "LATE_STAGE_CONSILIENCE_ONLY"},
    ]
    write_table("DISCRIMINATOR_RANKING.tsv", ranking_rows)

    controls = exact_controls()
    assert all(value is True for key, value in controls.items() if key.endswith("_exact") or key.endswith("_witness"))
    result = {
        "schema": "udt.cmb_polarization_observable_typing.derivation.v1",
        "status": "PASS_GUIDEPOST_CONDITIONAL_NO_NATIVE_PREDICTION",
        "observable_types": 12,
        "observable_gates": 14,
        "observable_gate_cells": 168,
        "extension_rows": 12,
        "extension_observable_cells": 144,
        "observable_gate_status_counts": dict(sorted(Counter(row["status"] for row in observable_gate_rows).items())),
        "capability_status_counts": dict(sorted(Counter(row["status"] for row in capability_rows).items())),
        "exact_controls": controls,
        "highest_priority_future_guideposts": ["O09", "O10", "O11"],
        "power_spectra_alone_for_directional_holonomy": "INSUFFICIENT_NONINJECTIVE_COMPRESSION",
        "CMB_polarization_guidepost_status": "PROMISING_FUTURE_GUIDEPOST_ONLY_AFTER_NATIVE_EXTENSION_DOMAIN_CARRIER_SOURCE_PROPAGATION_GLOBAL_SKY_STATISTICAL_RULE_AND_EXTERNAL_CALIBRATION_FOREGROUND_CONTROLS",
        "current_UDT_CMB_prediction": "ABSENT_OPEN_CHAIN",
        "unique_extension_selected": False,
        "physical_path_selected": False,
        "physical_polarization_carrier_derived": False,
        "native_polarization_source_derived": False,
        "E_B_are_local_basis_components": False,
        "zero_TB_EB_metric_only_prediction": False,
        "BB_unique_holonomy_signature": False,
        "rotation_unique_without_calibration_control": False,
        "source_peak_phase_amplitude_derived_from_metric_only": False,
        "statistical_isotropy_UDT_theorem": False,
        "map_level_anomaly_equated_to_power_spectrum": False,
        "Maxwell_Thomson_imported_as_native": False,
        "standard_cosmology_imported_as_UDT": False,
        "fit_performed": False,
        "strong_local_CSN_activated": False,
        "cross_branch_splice_used": False,
        "Xmax_bootstrap_action_source_boundary_mass_changed": False,
        "maximum_conclusion": "CMB_POLARIZATION_CHAIN_CLASSIFIED;_MAP_OFFDIAGONAL_AND_REAL_SPACE_GUIDEPOSTS_RANKED_CONDITIONALLY;_NO_NATIVE_PREDICTION_OR_VALIDATION",
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
