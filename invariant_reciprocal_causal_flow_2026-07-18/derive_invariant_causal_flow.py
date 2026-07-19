#!/usr/bin/env python3
"""Exact CPU derivation of the invariant content of reciprocal causal flow."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path

import sympy as sp


OUTCOME = "STATIC_OPTICAL_REALIZATION_CONDITIONAL_UNIVERSAL_REALIZATION_OPEN"


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--transcript", type=Path, required=True)
    args = parser.parse_args()

    c0, omega, jacobian, kappa, time_scale = sp.symbols(
        "c_0 Omega J kappa lambda_t", positive=True, finite=True
    )
    phi = sp.symbols("phi", real=True, finite=True)

    # Conditional reciprocal static block.
    lapse = sp.exp(-phi)
    spatial_rr = sp.exp(2 * phi)
    optical_rr = sp.simplify(spatial_rr / lapse**2)
    optical_stretch = sp.sqrt(optical_rr)
    coordinate_slope = sp.simplify(c0 * lapse / sp.sqrt(spatial_rr))
    reversed_slope = sp.simplify(coordinate_slope.subs(phi, -phi))
    reversed_stretch = sp.simplify(optical_stretch.subs(phi, -phi))
    local_proper_speed = sp.simplify(sp.sqrt(spatial_rr) * coordinate_slope / lapse)

    # A common Weyl/CSN scaling cancels from the static optical metric. This
    # statement assumes the supplied static flow remains a symmetry.
    scaled_lapse = omega * lapse
    scaled_spatial_rr = omega**2 * spatial_rr
    scaled_optical_rr = sp.simplify(scaled_spatial_rr / scaled_lapse**2)

    # A constant reparameterization t'=lambda_t t rescales the lapse and the
    # optical metric component. The conformal cone is unchanged, but numerical
    # arrival times require a clock/boundary normalization.
    time_rescaled_lapse = sp.simplify(lapse / time_scale)
    time_rescaled_optical_rr = sp.simplify(spatial_rr / time_rescaled_lapse**2)
    time_rescaled_slope = sp.simplify(coordinate_slope / time_scale)

    # A radial coordinate change dr=J dq changes the pointwise slope and
    # optical density inversely, leaving the integrated arrival functional.
    transformed_optical_qq = sp.simplify(optical_rr * jacobian**2)
    transformed_slope = sp.simplify(coordinate_slope / jacobian)
    transformed_arrival_density = sp.simplify(sp.sqrt(transformed_optical_qq) / c0)
    original_arrival_density = sp.simplify(optical_stretch / c0)
    transformed_reciprocal_stretch_product = sp.simplify(
        sp.sqrt(transformed_optical_qq)
        * sp.sqrt(transformed_optical_qq.subs(phi, -phi))
    )
    time_rescaled_stretch = sp.sqrt(time_rescaled_optical_rr)
    time_rescaled_reciprocal_stretch_product = sp.simplify(
        time_rescaled_stretch * time_rescaled_stretch.subs(phi, -phi)
    )

    # Conditional WR-L profile A=1-r/X.
    radius, wall = sp.symbols("r X", positive=True, finite=True)
    A = 1 - radius / wall
    wrl_phi = -sp.log(A) / 2
    wrl_lapse = sp.simplify(lapse.subs(phi, wrl_phi))
    wrl_spatial_rr = sp.simplify(spatial_rr.subs(phi, wrl_phi))
    wrl_optical_rr = sp.simplify(optical_rr.subs(phi, wrl_phi))
    wrl_coordinate_slope = sp.simplify(coordinate_slope.subs(phi, wrl_phi))
    wrl_proper_distance = sp.simplify(2 * wall * (1 - sp.sqrt(A)))
    wrl_optical_distance = sp.simplify(-wall * sp.log(A))
    wrl_arrival_time = sp.simplify(wrl_optical_distance / c0)
    wrl_proper_integrand = sp.simplify(sp.diff(wrl_proper_distance, radius))
    wrl_optical_integrand = sp.simplify(sp.diff(wrl_optical_distance, radius))
    wrl_limits = {
        "coordinate_slope_center": sp.limit(wrl_coordinate_slope, radius, 0, dir="+"),
        "coordinate_slope_wall": sp.limit(wrl_coordinate_slope, radius, wall, dir="-"),
        "proper_distance_wall": sp.limit(wrl_proper_distance, radius, wall, dir="-"),
        "optical_distance_wall": sp.limit(wrl_optical_distance, radius, wall, dir="-"),
        "arrival_time_wall": sp.limit(wrl_arrival_time, radius, wall, dir="-"),
    }
    start = sp.symbols("r_0", positive=True, finite=True)
    A_start = 1 - start / wall
    wrl_proper_from_start = sp.simplify(
        2 * wall * (sp.sqrt(A_start) - sp.sqrt(A))
    )
    wrl_optical_from_start = sp.simplify(wall * sp.log(A_start / A))
    wrl_from_start_limits = {
        "proper_to_wall": sp.limit(wrl_proper_from_start, radius, wall, dir="-"),
        "optical_to_wall": sp.limit(wrl_optical_from_start, radius, wall, dir="-"),
    }

    # The radial WR-L block is exactly a Rindler wedge. With
    # rho=2X sqrt(A), r=X-rho^2/(4X).
    rho = sp.symbols("rho", positive=True, finite=True)
    radius_of_rho = wall - rho**2 / (4 * wall)
    A_of_rho = sp.simplify(A.subs(radius, radius_of_rho))
    dr_drho = sp.diff(radius_of_rho, rho)
    radial_metric_rho = sp.simplify((1 / A_of_rho) * dr_drho**2)
    temporal_metric_rho = sp.simplify(-A_of_rho * c0**2)
    wrl_kappa = sp.simplify(c0 / (2 * wall))
    rindler_temporal = sp.simplify(-(wrl_kappa * rho / c0) ** 2 * c0**2)

    # Ingoing Eddington-Finkelstein form is finite and nondegenerate at A=0.
    ef_block = sp.Matrix([[-A * c0**2, c0], [c0, 0]])
    ef_wall_block = sp.simplify(ef_block.subs(radius, wall))
    ef_determinant = sp.simplify(ef_block.det())
    theta = sp.symbols("theta", real=True, finite=True)
    ef_full_determinant = sp.simplify(ef_determinant * radius**4 * sp.sin(theta) ** 2)
    ef_full_wall_determinant = sp.simplify(ef_full_determinant.subs(radius, wall))

    # Full 4D SSS metric curvature invariants for f=A. These identities are
    # standard consequences of the metric, not an assumed field equation.
    f = A
    ricci_scalar_formula = sp.simplify(
        -sp.diff(f, radius, 2)
        - 4 * sp.diff(f, radius) / radius
        + 2 * (1 - f) / radius**2
    )
    kretschmann_formula = sp.simplify(
        sp.diff(f, radius, 2) ** 2
        + 4 * (sp.diff(f, radius) / radius) ** 2
        + 4 * ((1 - f) / radius**2) ** 2
    )
    curvature_limits = {
        "ricci_wall": sp.limit(ricci_scalar_formula, radius, wall, dir="-"),
        "kretschmann_wall": sp.limit(kretschmann_formula, radius, wall, dir="-"),
        "ricci_center": sp.limit(ricci_scalar_formula, radius, 0, dir="+"),
        "kretschmann_center": sp.limit(kretschmann_formula, radius, 0, dir="+"),
    }

    # Flat-spacetime observer counterexample. In the Rindler wedge, the same
    # Minkowski geometry has a position-dependent coordinate null slope.
    rho_r = sp.symbols("rho_R", positive=True, finite=True)
    rindler_lapse = kappa * rho_r / c0
    rindler_optical_rr = sp.simplify(1 / rindler_lapse**2)
    rindler_coordinate_slope = sp.simplify(c0 * rindler_lapse)
    rindler_local_speed = sp.simplify(rindler_coordinate_slope / rindler_lapse)
    inertial_lapse = sp.Integer(1)
    inertial_optical_rr = sp.Integer(1)
    rindler_time = sp.symbols("t_R", real=True, finite=True)
    minkowski_T = rho_r * sp.sinh(kappa * rindler_time)
    minkowski_X = rho_r * sp.cosh(kappa * rindler_time)
    coordinate_jacobian = sp.Matrix(
        [
            [sp.diff(minkowski_T, rindler_time), sp.diff(minkowski_T, rho_r)],
            [sp.diff(minkowski_X, rindler_time), sp.diff(minkowski_X, rho_r)],
        ]
    )
    minkowski_metric = sp.diag(-1, 1)
    rindler_pullback = sp.simplify(coordinate_jacobian.T * minkowski_metric * coordinate_jacobian)

    checks = {
        "T1_coordinate_slope_from_metric_ratio": coordinate_slope == c0 * sp.exp(-2 * phi),
        "T1_local_orthonormal_speed_is_anchor": local_proper_speed == c0,
        "T2_static_optical_metric": optical_rr == sp.exp(4 * phi),
        "T2_optical_arrival_density": original_arrival_density == sp.exp(2 * phi) / c0,
        "T3_CSN_static_optical_metric_invariant": scaled_optical_rr == optical_rr,
        "T3_time_reparameterization_rescales_optical_metric": time_rescaled_optical_rr == time_scale**2 * optical_rr,
        "T3_time_reparameterization_rescales_coordinate_slope": time_rescaled_slope == coordinate_slope / time_scale,
        "T4_reciprocal_coordinate_slope_product": sp.simplify(coordinate_slope * reversed_slope) == c0**2,
        "T4_reciprocal_optical_stretch_product": sp.simplify(optical_stretch * reversed_stretch) == 1,
        "T5_coordinate_slope_changes_under_radial_reparametrization": transformed_slope == coordinate_slope / jacobian,
        "T5_optical_density_transforms_as_line_element": transformed_arrival_density == jacobian * original_arrival_density,
        "T5_slope_density_inverse_relation": sp.simplify(transformed_slope * transformed_arrival_density) == 1,
        "T5_reciprocal_stretch_product_radial_coordinate_pinned": transformed_reciprocal_stretch_product == jacobian**2,
        "T5_reciprocal_stretch_product_time_normalization_pinned": time_rescaled_reciprocal_stretch_product == time_scale**2,
        "T6_WRL_lapse": sp.simplify(wrl_lapse / sp.sqrt(A)) == 1,
        "T6_WRL_spatial_metric": sp.simplify(wrl_spatial_rr - 1 / A) == 0,
        "T6_WRL_optical_metric": sp.simplify(wrl_optical_rr - 1 / A**2) == 0,
        "T6_WRL_coordinate_slope": sp.simplify(wrl_coordinate_slope - c0 * A) == 0,
        "T7_WRL_proper_antiderivative": sp.simplify(wrl_proper_integrand * sp.sqrt(A)) == 1,
        "T7_WRL_optical_antiderivative": sp.simplify(wrl_optical_integrand - 1 / A) == 0,
        "T7_WRL_wall_finite_proper_distance": wrl_limits["proper_distance_wall"] == 2 * wall,
        "T7_WRL_wall_infinite_optical_distance": wrl_limits["optical_distance_wall"] == sp.oo,
        "T7_WRL_wall_infinite_static_arrival_time": wrl_limits["arrival_time_wall"] == sp.oo,
        "T7_WRL_center_slope_is_anchor": wrl_limits["coordinate_slope_center"] == c0,
        "T7_WRL_wall_slope_is_zero": wrl_limits["coordinate_slope_wall"] == 0,
        "T7_WRL_regular_start_finite_remaining_proper_distance": sp.simplify(wrl_from_start_limits["proper_to_wall"] / (2 * wall * sp.sqrt(A_start))) == 1,
        "T7_WRL_regular_start_infinite_remaining_optical_distance": wrl_from_start_limits["optical_to_wall"] == sp.oo,
        "T8_WRL_radial_block_is_Rindler": temporal_metric_rho == rindler_temporal and radial_metric_rho == 1,
        "T8_WRL_EF_extension_nondegenerate": ef_determinant == -c0**2 and ef_wall_block.det() == -c0**2,
        "T8_WRL_full4D_EF_determinant_regular_at_wall": ef_full_determinant == -c0**2 * radius**4 * sp.sin(theta) ** 2 and ef_full_wall_determinant == -c0**2 * wall**4 * sp.sin(theta) ** 2,
        "T8_WRL_full4D_Ricci_scalar": ricci_scalar_formula == 6 / (wall * radius),
        "T8_WRL_full4D_Kretschmann": kretschmann_formula == 8 / (wall**2 * radius**2),
        "T8_WRL_wall_curvature_finite": curvature_limits["ricci_wall"] == 6 / wall**2 and curvature_limits["kretschmann_wall"] == 8 / wall**4,
        "T8_WRL_center_curvature_singular": curvature_limits["ricci_center"] == sp.oo and curvature_limits["kretschmann_center"] == sp.oo,
        "T9_explicit_Minkowski_to_Rindler_pullback": rindler_pullback == sp.diag(-kappa**2 * rho_r**2, 1),
        "T9_Rindler_coordinate_slope_varies_in_flat_metric": rindler_coordinate_slope == kappa * rho_r,
        "T9_Rindler_local_speed_is_anchor": rindler_local_speed == c0,
        "T9_inertial_and_Rindler_optical_components_differ": inertial_optical_rr != rindler_optical_rr,
    }
    if not all(checks.values()):
        raise RuntimeError(f"exact causal-flow check failed: {checks}")

    class_results = {
        "I0_UNIVERSAL_METRIC_ONLY_LOCAL_CAUSAL_SCALAR_OR_FLOW": "NULL_CONE_DERIVED_SPEED_DECOMPOSITION_NOT_UNIVERSAL",
        "I1_STATIC_OPTICAL_REALIZATION": "DERIVED_CONDITIONAL_ON_STATIC_FLOW_QUOTIENT_AND_NORMALIZATION",
        "I2_STATIONARY_REALIZATION": "FERMAT_RANDERS_EXTENSION_CONDITIONAL_NOT_EXECUTED",
        "I3_GENERAL_TIME_LIVE_REALIZATION": "OPEN_FULL_NULL_ARRIVAL_MAP_REQUIRED",
        "I4_FINITE_CELL_GLOBAL_COMPLETION": "OPEN_BOUNDARY_MATCHING_AND_NORMALIZATION_REQUIRED",
        "I5_SUBSTRATE_RECYCLING_FALLBACK": "OPEN_SEPARATE_ONTOLOGY_AND_DYNAMICS_NOT_USED",
    }
    result = {
        "schema": "udt.invariant-reciprocal-causal-flow.v1",
        "top_level_outcome": OUTCOME,
        "checks": checks,
        "check_count": len(checks),
        "class_results": class_results,
        "exact_algebra": {
            "reciprocal_static_block": {
                "lapse": str(lapse),
                "spatial_rr": str(spatial_rr),
                "optical_rr": str(optical_rr),
                "optical_stretch": str(optical_stretch),
                "coordinate_null_slope": str(coordinate_slope),
                "local_proper_speed": str(local_proper_speed),
                "reversed_slope_product": str(sp.simplify(coordinate_slope * reversed_slope)),
                "reversed_stretch_product": str(sp.simplify(optical_stretch * reversed_stretch)),
            },
            "CSN_and_coordinate_change": {
                "scaled_optical_rr": str(scaled_optical_rr),
                "time_rescaled_optical_rr": str(time_rescaled_optical_rr),
                "time_rescaled_coordinate_slope": str(time_rescaled_slope),
                "transformed_optical_qq": str(transformed_optical_qq),
                "transformed_coordinate_slope": str(transformed_slope),
                "transformed_arrival_density": str(transformed_arrival_density),
                "transformed_reciprocal_stretch_products": {
                    "radial_coordinate": str(transformed_reciprocal_stretch_product),
                    "time_normalization": str(time_rescaled_reciprocal_stretch_product),
                },
            },
            "WRL": {
                "A": str(A),
                "coordinate_null_slope": str(wrl_coordinate_slope),
                "proper_distance": str(wrl_proper_distance),
                "optical_distance": str(wrl_optical_distance),
                "arrival_time": str(wrl_arrival_time),
                "limits": {key: str(value) for key, value in wrl_limits.items()},
                "from_regular_start": {
                    "proper_distance": str(wrl_proper_from_start),
                    "optical_distance": str(wrl_optical_from_start),
                    "limits": {key: str(value) for key, value in wrl_from_start_limits.items()},
                },
                "Rindler_radius_map": str(radius_of_rho),
                "Rindler_block": [str(temporal_metric_rho), str(radial_metric_rho)],
                "EF_block": str(ef_block),
                "EF_determinant": str(ef_determinant),
                "EF_full4D_determinant": str(ef_full_determinant),
                "Ricci_scalar_4D": str(ricci_scalar_formula),
                "Kretschmann_4D": str(kretschmann_formula),
                "curvature_limits": {key: str(value) for key, value in curvature_limits.items()},
            },
            "flat_observer_counterexample": {
                "inertial_lapse": str(inertial_lapse),
                "inertial_optical_rr": str(inertial_optical_rr),
                "Rindler_lapse": str(rindler_lapse),
                "Rindler_optical_rr": str(rindler_optical_rr),
                "Rindler_coordinate_slope": str(rindler_coordinate_slope),
                "Rindler_local_speed": str(rindler_local_speed),
                "Minkowski_to_Rindler_Jacobian": str(coordinate_jacobian),
                "Minkowski_metric_pullback": str(rindler_pullback),
            },
        },
        "adjudication": {
            "metric_determines_null_cone": True,
            "physical_matter_clocks_signals_proven_to_follow_metric_cone": False,
            "static_optical_metric_CSN_invariant_given_static_flow": True,
            "integrated_static_optical_arrival_is_coordinate_invariant": True,
            "coordinate_null_slope_is_scalar": False,
            "local_orthonormal_light_speed_varies_with_phi": False,
            "metric_universally_selects_observer_and_parallel_line": False,
            "Killing_normalization_selected_without_reference_data": False,
            "WRL_wall_is_finite_proper_distance": True,
            "WRL_wall_is_infinite_static_optical_distance": True,
            "WRL_wall_is_curvature_singularity": False,
            "WRL_metric_alone_proves_material_wall_or_substrate": False,
            "WRL_full4D_center_is_regular": False,
            "WRL_static_wall_identified_with_CMB": False,
            "static_result_establishes_time_live_cosmology": False,
            "optical_reciprocity_proves_internal_K_pairing": False,
            "line_realization_gap_closed": False,
            "native_action_source_carrier_or_boundary_charge_selected": False,
            "substrate_recycling_mechanism_derived": False,
        },
        "next_discriminator": {
            "question": "What native structure selects the timelike flow, parallel direction, normalization, and global matching that turn the conformal null cone into a UDT causal-arrival map?",
            "required_evidence": [
                "native_observer_or_clock_congruence_selector",
                "native_parallel_line_realization",
                "normalization_or_boundary_matching_rule",
                "time_live_4D_null_arrival_derivation",
                "CMB_to_metric_surface_identification",
                "separate_boundary_substrate_action_and_recycling_map_if_pursued",
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
        f"optical_rr={optical_rr}",
        f"coordinate_null_slope={coordinate_slope}",
        f"local_proper_speed={local_proper_speed}",
        f"CSN_scaled_optical_rr={scaled_optical_rr}",
        f"reciprocal_optical_stretch_product={sp.simplify(optical_stretch * reversed_stretch)}",
        f"WRL_proper_distance={wrl_proper_distance}",
        f"WRL_optical_distance={wrl_optical_distance}",
        f"WRL_wall_limits=proper:{wrl_limits['proper_distance_wall']},optical:{wrl_limits['optical_distance_wall']},arrival:{wrl_limits['arrival_time_wall']}",
        f"WRL_regular_start_wall_limits=proper:{wrl_from_start_limits['proper_to_wall']},optical:{wrl_from_start_limits['optical_to_wall']}",
        f"WRL_Rindler_block=({temporal_metric_rho},{radial_metric_rho})",
        f"WRL_EF_determinant={ef_determinant}",
        f"WRL_full4D_EF_determinant={ef_full_determinant}",
        f"WRL_4D_curvature=R:{ricci_scalar_formula},K:{kretschmann_formula}",
        f"WRL_wall_curvature=R:{curvature_limits['ricci_wall']},K:{curvature_limits['kretschmann_wall']}",
        f"Rindler_flat_coordinate_slope={rindler_coordinate_slope}",
        f"Minkowski_to_Rindler_pullback={rindler_pullback}",
        f"result_sha256={digest(rendered)}",
    ]
    args.transcript.write_text("\n".join(transcript) + "\n", encoding="utf-8")
    print("\n".join(transcript))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
