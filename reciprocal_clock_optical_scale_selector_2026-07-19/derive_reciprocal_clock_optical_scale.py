#!/usr/bin/env python3
"""Exact CPU derivation for the reciprocal clock–optical–scale selector."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path

import sympy as sp


OUTCOME = "RECIPROCAL_CLOCK_OPTICAL_LINK_DERIVED_SCALE_REALIZATION_AND_MASS_OPEN"


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--transcript", type=Path, required=True)
    args = parser.parse_args()

    c0, N, B = sp.symbols("c_0 N B", positive=True, finite=True)
    dt, dr = sp.symbols("dt dr", positive=True, finite=True)

    proper_time = N * dt
    proper_length = B * dr
    coordinate_null_slope = sp.simplify(c0 * N / B)
    local_metric_null_speed = sp.simplify(B * coordinate_null_slope / N)
    optical_stretch = sp.simplify(B / N)
    arrival_density = sp.simplify(optical_stretch / c0)

    # Static emitter/observer redshift. The conserved Killing frequency E
    # gives omega_local=E/N, hence 1+z=omega_e/omega_o=N_o/N_e.
    N_e, N_o, B_e, B_o = sp.symbols(
        "N_e N_o B_e B_o", positive=True, finite=True
    )
    redshift_factor = sp.simplify(N_o / N_e)
    clock_rate_ratio = sp.simplify(N_e / N_o)
    slope_e = sp.simplify(c0 * N_e / B_e)
    slope_o = sp.simplify(c0 * N_o / B_o)
    general_slope_ratio = sp.simplify(slope_e / slope_o)
    general_redshift_relation = sp.simplify((1 / redshift_factor) * (B_o / B_e))

    # UDT reciprocal representative B=1/N.
    reciprocal_slope = sp.simplify(coordinate_null_slope.subs(B, 1 / N))
    reciprocal_optical_stretch = sp.simplify(optical_stretch.subs(B, 1 / N))
    reciprocal_slope_ratio = sp.simplify(
        general_slope_ratio.subs({B_e: 1 / N_e, B_o: 1 / N_o})
    )
    reciprocal_optical_ratio = sp.simplify(
        (B_e / N_e) / (B_o / N_o)
    ).subs({B_e: 1 / N_e, B_o: 1 / N_o})
    reciprocal_optical_ratio = sp.simplify(reciprocal_optical_ratio)
    J_e, J_o = sp.symbols("J_e J_o", positive=True, finite=True)
    transformed_reciprocal_slope_ratio = sp.simplify(
        reciprocal_slope_ratio * J_o / J_e
    )
    transformed_reciprocal_optical_ratio = sp.simplify(
        reciprocal_optical_ratio * J_e / J_o
    )

    # Same clock factor N, three distinct ruler responses.
    time_only_slope = sp.simplify(coordinate_null_slope.subs(B, 1))
    time_only_optical = sp.simplify(optical_stretch.subs(B, 1))
    common_scale_slope = sp.simplify(coordinate_null_slope.subs(B, N))
    common_scale_optical = sp.simplify(optical_stretch.subs(B, N))

    # General ruler exponent B=N^p displays the discriminator compactly.
    p = sp.symbols("p", real=True, finite=True)
    exponent_slope = sp.simplify(coordinate_null_slope.subs(B, N**p))
    exponent_optical = sp.simplify(optical_stretch.subs(B, N**p))

    # Common-scale neutrality, radial reparameterization, and time
    # normalization checks.
    Omega, Omega_e, Omega_o, J, lambda_t = sp.symbols(
        "Omega Omega_e Omega_o J lambda_t", positive=True, finite=True
    )
    csn_slope = sp.simplify(c0 * (Omega * N) / (Omega * B))
    csn_optical = sp.simplify((Omega * B) / (Omega * N))
    radial_slope = sp.simplify(coordinate_null_slope / J)
    radial_arrival_density = sp.simplify(J * arrival_density)
    time_rescaled_N = sp.simplify(N / lambda_t)
    time_rescaled_slope = sp.simplify(c0 * time_rescaled_N / B)
    time_rescaled_optical = sp.simplify(B / time_rescaled_N)
    normalized_redshift = sp.simplify((N_o / lambda_t) / (N_e / lambda_t))
    locally_CSN_rescaled_redshift = sp.simplify(
        (Omega_o * N_o) / (Omega_e * N_e)
    )
    reciprocal_constraint = sp.simplify(N * (1 / N))
    radial_reparametrized_constraint = sp.simplify(N * (J / N))
    time_reparametrized_constraint = sp.simplify((N / lambda_t) * (1 / N))
    CSN_rescaled_constraint = sp.simplify((Omega * N) * (Omega / N))

    # Operational energy/mass readouts in the static class.
    mass, hbar = sp.symbols("m hbar", positive=True, finite=True)
    local_rest_energy = sp.simplify(mass * c0**2)
    local_compton_frequency = sp.simplify(local_rest_energy / hbar)
    killing_rest_energy_e = sp.simplify(N_e * local_rest_energy)
    observer_assigned_rest_energy = sp.simplify(killing_rest_energy_e / N_o)
    photon_energy_e = sp.symbols("E_gamma_e", positive=True, finite=True)
    photon_energy_o = sp.simplify(photon_energy_e * N_e / N_o)
    reconstructed_source_energy = sp.simplify(photon_energy_o * redshift_factor)

    # Relational-scale kinematics. No scale profile or pivot is selected.
    phi_scale = sp.symbols("phi_x_sigma", real=True, finite=True)
    scale_lapse = sp.exp(-phi_scale)
    scale_ruler = sp.exp(phi_scale)
    scale_slope = sp.simplify(c0 * scale_lapse / scale_ruler)
    scale_optical = sp.simplify(scale_ruler / scale_lapse)
    dual_slope = sp.simplify(scale_slope.subs(phi_scale, -phi_scale))
    dual_lapse = sp.simplify(scale_lapse.subs(phi_scale, -phi_scale))
    dual_optical = sp.simplify(scale_optical.subs(phi_scale, -phi_scale))
    plateau_values = {
        "N": sp.simplify(scale_lapse.subs(phi_scale, 0)),
        "B": sp.simplify(scale_ruler.subs(phi_scale, 0)),
        "c_eff": sp.simplify(scale_slope.subs(phi_scale, 0)),
        "q_opt": sp.simplify(scale_optical.subs(phi_scale, 0)),
    }
    scale_limits = {
        "UV_phi_to_negative_infinity": sp.limit(scale_slope, phi_scale, -sp.oo),
        "IR_phi_to_positive_infinity": sp.limit(scale_slope, phi_scale, sp.oo),
        "one_sided_phi_zero_speed": scale_slope.subs(phi_scale, 0),
        "one_sided_phi_zero_optical": scale_optical.subs(phi_scale, 0),
    }
    speed_phi_derivative = sp.simplify(sp.diff(scale_slope, phi_scale))
    optical_phi_derivative = sp.simplify(sp.diff(scale_optical, phi_scale))

    checks = {
        "T1_clock_factor": proper_time == N * dt,
        "T1_ruler_factor": proper_length == B * dr,
        "T1_coordinate_null_slope": coordinate_null_slope == c0 * N / B,
        "T1_local_metric_null_speed": local_metric_null_speed == c0,
        "T1_optical_arrival_density": arrival_density == B / (c0 * N),
        "T2_static_redshift_factor": redshift_factor == N_o / N_e,
        "T2_clock_rate_ratio_is_inverse_redshift": clock_rate_ratio == 1 / redshift_factor,
        "T3_general_slope_redshift_relation": general_slope_ratio == general_redshift_relation,
        "T4_reciprocal_slope": reciprocal_slope == c0 * N**2,
        "T4_reciprocal_optical_stretch": reciprocal_optical_stretch == N**-2,
        "T4_reciprocal_slope_ratio_is_inverse_redshift_squared": reciprocal_slope_ratio == redshift_factor**-2,
        "T4_reciprocal_optical_ratio_is_redshift_squared": reciprocal_optical_ratio == redshift_factor**2,
        "T4_slope_ratio_is_clock_ratio_squared": reciprocal_slope_ratio == clock_rate_ratio**2,
        "T4_slope_ratio_requires_pinned_radial_standard": transformed_reciprocal_slope_ratio == reciprocal_slope_ratio * J_o / J_e,
        "T4_optical_component_ratio_requires_pinned_radial_standard": transformed_reciprocal_optical_ratio == reciprocal_optical_ratio * J_e / J_o,
        "T5_time_only_slope": time_only_slope == c0 * N,
        "T5_time_only_optical": time_only_optical == 1 / N,
        "T5_common_scale_slope_unchanged": common_scale_slope == c0,
        "T5_common_scale_optical_unchanged": common_scale_optical == 1,
        "T5_same_clock_three_ruler_response_functions_distinct": len({str(time_only_slope), str(common_scale_slope), str(reciprocal_slope)}) == 3,
        "T5_general_ruler_exponent_slope": exponent_slope == c0 * N**(1 - p),
        "T5_general_ruler_exponent_optical": exponent_optical == N**(p - 1),
        "T6_CSN_null_slope_invariant": csn_slope == coordinate_null_slope,
        "T6_CSN_optical_stretch_invariant": csn_optical == optical_stretch,
        "T6_radial_coordinate_slope_density_inverse": sp.simplify(radial_slope * radial_arrival_density) == 1,
        "T6_time_normalization_rescales_slope": time_rescaled_slope == coordinate_null_slope / lambda_t,
        "T6_time_normalization_rescales_optical": time_rescaled_optical == lambda_t * optical_stretch,
        "T6_redshift_ratio_normalization_invariant": normalized_redshift == redshift_factor,
        "T6_endpoint_dependent_CSN_rescales_lapse_redshift": locally_CSN_rescaled_redshift == (Omega_o / Omega_e) * redshift_factor,
        "T6_NB_one_radial_coordinate_pinned": reciprocal_constraint == 1 and radial_reparametrized_constraint == J,
        "T6_NB_one_time_normalization_pinned": time_reparametrized_constraint == 1 / lambda_t,
        "T6_NB_one_not_local_CSN_invariant": CSN_rescaled_constraint == Omega**2,
        "T7_fixed_mass_comparison_rest_energy": local_rest_energy == mass * c0**2,
        "T7_fixed_mass_comparison_compton_frequency": local_compton_frequency == mass * c0**2 / hbar,
        "T7_static_Killing_rest_energy": killing_rest_energy_e == N_e * mass * c0**2,
        "T7_observer_assigned_energy_is_redshifted": observer_assigned_rest_energy == local_rest_energy / redshift_factor,
        "T7_photon_received_energy_is_redshifted": photon_energy_o == photon_energy_e / redshift_factor,
        "T7_source_energy_reconstruction": reconstructed_source_energy == photon_energy_e,
        "T8_dual_scale_slope_product": sp.simplify(scale_slope * dual_slope) == c0**2,
        "T8_dual_scale_lapse_product": sp.simplify(scale_lapse * dual_lapse) == 1,
        "T8_dual_scale_optical_product": sp.simplify(scale_optical * dual_optical) == 1,
        "T8_exact_neutral_anchor": plateau_values == {"N": 1, "B": 1, "c_eff": c0, "q_opt": 1},
        "T9_UV_and_IR_endpoint_slopes": scale_limits["UV_phi_to_negative_infinity"] == sp.oo and scale_limits["IR_phi_to_positive_infinity"] == 0,
        "T9_speed_decreases_with_phi": speed_phi_derivative == -2 * scale_slope,
        "T9_optical_stretch_increases_with_phi": optical_phi_derivative == 2 * scale_optical,
    }
    if not all(checks.values()):
        raise RuntimeError(f"exact clock-optical-scale check failed: {checks}")

    class_results = {
        "J0_GENERAL_CLOCK_RULER_DECOMPOSITION": "TIME_DILATION_ALONE_INSUFFICIENT",
        "J1_UDT_RECIPROCAL_STATIC_BLOCK": "INVERSE_SQUARE_REDSHIFT_OPTICAL_LINK_DERIVED_CONDITIONAL",
        "J2_COUNTERMODELS": "SAME_CLOCK_FACTOR_THREE_DISTINCT_OPTICAL_RESPONSES",
        "J3_OPERATIONAL_ENERGY_AND_MASS": "STATIC_REDSHIFT_DOES_NOT_DERIVE_MASS_CHANGE_NATIVE_MASS_OPEN",
        "J4_RELATIONAL_SCALE_REALIZATION": "KINEMATIC_IDENTITIES_CONDITIONAL_ARCHITECTURE_AND_PROFILE_OPEN",
        "J5_ONE_SIDED_FALLBACK": "PINNED_ADAPTED_COORDINATE_SLOPE_CEILING_AND_OPTICAL_DENSITY_FLOOR",
    }
    result = {
        "schema": "udt.reciprocal-clock-optical-scale-selector.v1",
        "top_level_outcome": OUTCOME,
        "checks": checks,
        "check_count": len(checks),
        "class_results": class_results,
        "exact_algebra": {
            "general": {
                "proper_time": str(proper_time),
                "proper_length": str(proper_length),
                "coordinate_null_slope": str(coordinate_null_slope),
                "local_metric_null_speed": str(local_metric_null_speed),
                "optical_stretch": str(optical_stretch),
            },
            "redshift": {
                "one_plus_z": str(redshift_factor),
                "clock_rate_ratio": str(clock_rate_ratio),
                "general_slope_ratio": str(general_slope_ratio),
                "reciprocal_slope_ratio": str(reciprocal_slope_ratio),
                "reciprocal_optical_ratio": str(reciprocal_optical_ratio),
                "radially_reparameterized_ratios": {
                    "slope": str(transformed_reciprocal_slope_ratio),
                    "optical": str(transformed_reciprocal_optical_ratio),
                },
                "endpoint_CSN_rescaled_one_plus_z": str(locally_CSN_rescaled_redshift),
            },
            "same_clock_countermodels": {
                "time_only": {"slope": str(time_only_slope), "optical": str(time_only_optical)},
                "common_scale": {"slope": str(common_scale_slope), "optical": str(common_scale_optical)},
                "reciprocal": {"slope": str(reciprocal_slope), "optical": str(reciprocal_optical_stretch)},
                "general_B_equals_N_to_p": {"slope": str(exponent_slope), "optical": str(exponent_optical)},
            },
            "energy_mass_readouts": {
                "local_rest_energy": str(local_rest_energy),
                "local_compton_frequency": str(local_compton_frequency),
                "Killing_rest_energy_at_emitter": str(killing_rest_energy_e),
                "observer_assigned_rest_energy": str(observer_assigned_rest_energy),
                "received_photon_energy": str(photon_energy_o),
                "reconstructed_source_energy": str(reconstructed_source_energy),
            },
            "relational_scale": {
                "N": str(scale_lapse),
                "B": str(scale_ruler),
                "c_eff": str(scale_slope),
                "q_opt": str(scale_optical),
                "dual_products": {
                    "speed": str(sp.simplify(scale_slope * dual_slope)),
                    "lapse": str(sp.simplify(scale_lapse * dual_lapse)),
                    "optical": str(sp.simplify(scale_optical * dual_optical)),
                },
                "plateau": {key: str(value) for key, value in plateau_values.items()},
                "limits": {key: str(value) for key, value in scale_limits.items()},
                "derivatives": {"speed": str(speed_phi_derivative), "optical": str(optical_phi_derivative)},
            },
        },
        "adjudication": {
            "time_dilation_and_effective_speed_share_one_dilation_field_in_reciprocal_block": True,
            "time_dilation_alone_uniquely_determines_effective_speed": False,
            "redshift_and_effective_speed_are_numerically_identical": False,
            "reciprocal_speed_ratio_is_inverse_redshift_squared": True,
            "boxed_square_relations_are_pinned_adapted_component_identities": True,
            "boxed_square_relations_are_CSN_class_physical_redshift_theorems": False,
            "NB_equals_one_is_coordinate_time_normalization_or_local_CSN_invariant": False,
            "common_scale_dilation_changes_null_slope": False,
            "coordinate_effective_speed_is_local_scalar_constant": False,
            "local_rest_mass_increase_derived_from_redshift": False,
            "received_energy_redshift_derived_in_static_class": True,
            "native_mass_emergence_or_mass_increase_derived": False,
            "native_invariant_mass_constancy_derived": False,
            "fixed_mass_compton_branch_is_native_UDT": False,
            "material_photon_emission_propagation_detection_coupling_derived": False,
            "coordinate_position_and_relational_scale_identical": False,
            "scale_indexed_metric_architecture_selected": False,
            "scale_realization_unique_minimum_architecture_selected": False,
            "UV_speedup_selected_by_current_foundation": False,
            "IR_slowdown_profile_selected_by_current_foundation": False,
            "ordinary_scale_plateau_thresholds_selected": False,
            "broad_ordinary_scale_plateau_tested": False,
            "dual_scale_pivot_selected": False,
            "operational_scale_involution_and_domain_selected": False,
            "same_scale_endpoint_or_cross_scale_coupling_rule_selected": False,
            "observable_superluminal_signalling_authorized": False,
            "one_sided_c0_is_speed_floor": False,
            "one_sided_c0_is_pinned_adapted_coordinate_slope_ceiling": True,
            "one_sided_unity_is_pinned_optical_density_floor": True,
            "one_sided_c0_is_invariant_material_signal_speed_ceiling": False,
            "one_sided_unity_is_invariant_optical_scalar_floor": False,
            "prior_observer_line_representative_normalization_gap_closed": False,
            "static_result_promoted_to_time_live_or_CMB": False,
            "action_source_carrier_boundary_or_substrate_selected": False,
        },
        "conditional_obligation_set": {
            "status": "NO_UNIQUE_MINIMUM_ARCHITECTURE_SELECTED",
            "existing_open_pins": [
                "observer_clock_flow",
                "parallel_spatial_line",
                "post_scale_representative",
                "Killing_and_radial_normalization",
            ],
            "scale_extension_obligations": [
                "operational_relational_scale_selector_sigma",
                "geometric_or_readout_law_single_metric_nonlocal_or_multiscale",
                "same_sigma_endpoint_rule_or_sigma_e_sigma_o_coupling",
                "matter_signal_coupling_if_physical_universality_is_claimed",
                "hyperbolicity_common_causal_order_and_intervention_no_signalling",
            ],
            "literal_many_cones_note": "Literal different cones at one event require multiscale, Finsler, constitutive, bilocal, or effective geometry; effective optics may instead arise from a single metric plus a scale-dependent observer, line, readout, or nonlocal travel kernel.",
            "not_selected": [
                "scale_profile_phi_of_x_sigma",
                "operational_scale_involution_and_domain",
                "UV_IR_pivot_or_fixed_point",
                "ordinary_plateau_boundaries_or_error_bounds",
                "material_coupling_and_causal_completion",
            ],
        },
        "environment": {
            "python": platform.python_version(),
            "sympy": sp.__version__,
            "cpu_only": True,
        },
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    args.output.write_text(rendered, encoding="utf-8")
    transcript = [
        f"top_level_outcome={OUTCOME}",
        f"python={platform.python_version()}",
        f"sympy={sp.__version__}",
        f"checks={sum(checks.values())}/{len(checks)}",
        f"general_coordinate_slope={coordinate_null_slope}",
        f"local_metric_null_speed={local_metric_null_speed}",
        f"one_plus_z={redshift_factor}",
        f"reciprocal_slope_ratio={reciprocal_slope_ratio}",
        f"reciprocal_optical_ratio={reciprocal_optical_ratio}",
        f"same_clock_slopes=time_only:{time_only_slope},common:{common_scale_slope},reciprocal:{reciprocal_slope}",
        f"observer_assigned_rest_energy={observer_assigned_rest_energy}",
        f"received_photon_energy={photon_energy_o}",
        f"scale_speed={scale_slope}",
        f"scale_dual_speed_product={sp.simplify(scale_slope * dual_slope)}",
        f"scale_limits=UV:{scale_limits['UV_phi_to_negative_infinity']},IR:{scale_limits['IR_phi_to_positive_infinity']}",
        f"result_sha256={digest(rendered)}",
    ]
    args.transcript.write_text("\n".join(transcript) + "\n", encoding="utf-8")
    print("\n".join(transcript))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
