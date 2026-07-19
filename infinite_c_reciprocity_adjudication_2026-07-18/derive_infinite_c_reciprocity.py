#!/usr/bin/env python3
"""Exact CPU algebra for the infinite-c / UDT Reciprocity adjudication."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path

import sympy as sp


OUTCOME = "LAYERED_COMPATIBILITY_METRIC_NONDISCRIMINATING"


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--transcript", type=Path, required=True)
    args = parser.parse_args()

    C, c_eff, c_star = sp.symbols("C c_eff c_star", positive=True, finite=True)
    psi = sp.symbols("psi", real=True)
    K = sp.Matrix([[0, 1], [1, 0]])

    # Finite regulated reciprocal representative.
    u_r = sp.sqrt(c_eff / C)
    v_r = sp.sqrt(C / c_eff)
    P_r = sp.diag(u_r, v_r)
    pairing_r = sp.simplify(P_r.T * K * P_r)
    metric_r = sp.diag(-C**2 * u_r**2, v_r**2)
    metric_effective = sp.diag(-c_eff**2, 1)
    reciprocal_factor = sp.simplify(C / c_eff)
    reciprocal_metric_residual = sp.simplify(metric_r - reciprocal_factor * metric_effective)

    # Nonreciprocal representative with the same effective null cone.
    u_nr = c_eff / C
    v_nr = sp.Integer(1)
    P_nr = sp.diag(u_nr, v_nr)
    pairing_nr = sp.simplify(P_nr.T * K * P_nr)
    metric_nr = sp.diag(-C**2 * u_nr**2, v_nr**2)
    csn_scale = sp.sqrt(C / c_eff)
    csn_representative_residual = sp.simplify(csn_scale * P_nr - P_r)

    # General CSN decomposition.
    u, v = sp.symbols("u v", positive=True, finite=True)
    P_general = sp.diag(u, v)
    common = sp.sqrt(u * v)
    determinant_one = sp.simplify(P_general / common)
    general_reconstruction = sp.simplify(common * determinant_one - P_general)

    # Residual field after subtracting an infinite-regulator constant.
    exp_minus_2phi = sp.simplify((c_star / C) * sp.exp(-2 * psi))
    exp_plus_2phi = sp.simplify((C / c_star) * sp.exp(2 * psi))
    metric_residual = sp.diag(-C**2 * exp_minus_2phi, exp_plus_2phi)
    residual_effective_metric = sp.diag(-c_star**2 * sp.exp(-2 * psi), sp.exp(2 * psi))
    residual_common_factor = sp.simplify(C / c_star)
    residual_metric_check = sp.simplify(metric_residual - residual_common_factor * residual_effective_metric)
    residual_causal_speed = sp.simplify(C * sp.sqrt(exp_minus_2phi / exp_plus_2phi))

    x = sp.symbols("x", real=True)
    psi_function = sp.Function("psi")(x)
    phi_regulated = sp.log(C / c_star) / 2 + psi_function
    derivative_residual = sp.simplify(sp.diff(phi_regulated, x) - sp.diff(psi_function, x))

    # Ordinary Lorentz transformation for constant effective c.
    speed = sp.symbols("w", real=True)
    gamma = 1 / sp.sqrt(1 - speed**2 / c_eff**2)
    lorentz = sp.Matrix([[gamma, -gamma * speed / c_eff**2], [-gamma * speed, gamma]])
    lorentz_residual = sp.simplify(lorentz.T * metric_effective * lorentz - metric_effective)

    # Real finite regulator limits: reciprocal components have singular but
    # opposite limits. The finite conformal metric is already exact above.
    u_limit = sp.limit(u_r, C, sp.oo)
    v_limit = sp.limit(v_r, C, sp.oo)
    determinant_nr = sp.simplify(P_nr.det())
    projective_representative = sp.simplify(sp.sqrt(c_eff / C) * P_r)
    projective_endpoint = projective_representative.applyfunc(lambda entry: sp.limit(entry, C, sp.oo))

    # Owner-clarified H6: infinite/zero are reciprocal endpoint limits of the
    # metric null slope, with finite c_anchor at phi=0.
    c_anchor = sp.symbols("c_anchor", positive=True, finite=True)
    depth = sp.symbols("depth", real=True)
    metric_endpoint_flow = sp.diag(-c_anchor**2 * sp.exp(-2 * depth), sp.exp(2 * depth))
    coordinate_null_speed = sp.simplify(sp.sqrt(-metric_endpoint_flow[0, 0] / metric_endpoint_flow[1, 1]))
    reverse_coordinate_speed = sp.simplify(coordinate_null_speed.subs(depth, -depth))
    endpoint_product = sp.simplify(coordinate_null_speed * reverse_coordinate_speed)
    proper_time_factor = sp.exp(-depth)
    proper_length_factor = sp.exp(depth)
    locally_measured_speed = sp.simplify(proper_length_factor * coordinate_null_speed / proper_time_factor)
    fast_endpoint = sp.limit(coordinate_null_speed, depth, -sp.oo)
    slow_endpoint = sp.limit(coordinate_null_speed, depth, sp.oo)
    radius, wall = sp.symbols("radius wall", positive=True, finite=True)
    wrl_depth = -sp.log(1 - radius / wall) / 2
    wrl_coordinate_speed = sp.simplify(coordinate_null_speed.subs(depth, wrl_depth))
    wrl_center_speed = sp.limit(wrl_coordinate_speed, radius, 0, dir="+")
    wrl_wall_speed = sp.limit(wrl_coordinate_speed, radius, wall, dir="-")
    fast_projective_metric = (sp.exp(2 * depth) * metric_endpoint_flow).applyfunc(
        lambda entry: sp.limit(entry, depth, -sp.oo)
    )
    slow_projective_metric = (sp.exp(-2 * depth) * metric_endpoint_flow).applyfunc(
        lambda entry: sp.limit(entry, depth, sp.oo)
    )

    checks = {
        "T2_finite_reciprocal_pairing_exact": pairing_r == K,
        "T2_finite_reciprocal_determinant_one": sp.simplify(P_r.det()) == 1,
        "T3_reciprocal_metric_conformal_limit_exact": reciprocal_metric_residual == sp.zeros(2),
        "T3_infinite_endpoint_singular": u_limit == 0 and v_limit == sp.oo,
        "T4_residual_metric_factorization_exact": residual_metric_check == sp.zeros(2),
        "T4_residual_causal_speed_finite": residual_causal_speed == c_star * sp.exp(-2 * psi),
        "T4_constant_regulator_contributes_no_derivative": derivative_residual == 0,
        "T5_nonreciprocal_metric_same_effective_cone": metric_nr == metric_effective,
        "T5_nonreciprocal_pairing_not_preserved_generically": pairing_nr == (c_eff / C) * K,
        "T5_CSN_maps_nonreciprocal_to_reciprocal_representative": csn_representative_residual == sp.zeros(2),
        "T5_general_CSN_representative_determinant_one": sp.simplify(determinant_one.det()) == 1,
        "T5_general_CSN_decomposition_reconstructs": general_reconstruction == sp.zeros(2),
        "T7_constant_effective_c_has_ordinary_lorentz_group": lorentz_residual == sp.zeros(2),
        "T8_nonreciprocal_countermodel_really_nonunit_determinant": determinant_nr == c_eff / C,
        "T3_projective_endpoint_is_finite_rank_one_not_GL2": projective_endpoint == sp.diag(0, 1) and projective_endpoint.det() == 0,
        "H6_null_slope_is_metric_ratio": coordinate_null_speed == c_anchor * sp.exp(-2 * depth),
        "H6_reversal_multiplies_coordinate_speeds_to_anchor_squared": endpoint_product == c_anchor**2,
        "H6_reciprocal_endpoint_limits_are_infinite_and_zero": fast_endpoint == sp.oo and slow_endpoint == 0,
        "H6_local_orthonormal_speed_remains_anchor": locally_measured_speed == c_anchor,
        "H6_conditional_WRL_center_speed_is_anchor_not_infinity": wrl_center_speed == c_anchor,
        "H6_conditional_WRL_wall_speed_tends_to_zero": wrl_wall_speed == 0,
        "H6_fast_projective_metric_endpoint_is_rank_one": fast_projective_metric == sp.diag(-c_anchor**2, 0) and fast_projective_metric.det() == 0,
        "H6_slow_projective_metric_endpoint_is_rank_one": slow_projective_metric == sp.diag(0, 1) and slow_projective_metric.det() == 0,
    }
    if not all(checks.values()):
        raise RuntimeError(f"exact adjudication check failed: {checks}")

    hypotheses = {
        "H0_FINITE_RECIPROCAL_EFFECTIVE": "CONSISTENT_CURRENT_FOUNDATION",
        "H1_LITERAL_INFINITY_SAME_LAYER": "INCOMPATIBLE_WITH_FINITE_INVERTIBLE_RECIPROCAL_PAIR",
        "H2_REGULATED_PROJECTIVE_INFINITY": "COMPATIBLE_LIMIT_NOT_GROUP_ENDPOINT",
        "H3_CSN_APPARENT_RECIPROCITY": "METRIC_EQUIVALENT_INTERNAL_PAIRING_NOT_DERIVED",
        "H4_GALILEAN_TO_LORENTZ_EMERGENCE": "OPEN_REPLACEMENT_REQUIRES_NEW_DYNAMICS_AND_UNIVERSAL_COUPLING",
        "H5A_ATEMPORAL_GLOBAL_CLOSURE": "CONCEPTUALLY_COMPATIBLE_NOT_DERIVED",
        "H5B_TIMED_INSTANTANEOUS_SUBSTRATE": "OPEN_REPLACEMENT_REQUIRES_PREFERRED_CAUSAL_STRUCTURE",
        "H6_RECIPROCAL_CAUSAL_ENDPOINT_FLOW": "CONDITIONALLY_COHERENT_METRIC_BLOCK_INTERPRETATION",
    }
    result = {
        "schema": "udt.infinite-c-reciprocity-adjudication.v1",
        "top_level_outcome": OUTCOME,
        "checks": checks,
        "check_count": len(checks),
        "hypotheses": hypotheses,
        "exact_algebra": {
            "reciprocal_representative": str(P_r),
            "reciprocal_pairing": str(pairing_r),
            "reciprocal_metric": str(metric_r),
            "reciprocal_common_factor": str(reciprocal_factor),
            "reciprocal_component_limits": {"u": str(u_limit), "v": str(v_limit)},
            "projective_rank_one_endpoint": str(projective_endpoint),
            "nonreciprocal_representative": str(P_nr),
            "nonreciprocal_pairing": str(pairing_nr),
            "nonreciprocal_determinant": str(determinant_nr),
            "CSN_scale_to_reciprocal": str(csn_scale),
            "residual_effective_speed": str(residual_causal_speed),
            "residual_metric": str(residual_effective_metric),
            "lorentz_residual": str(lorentz_residual),
            "H6_metric_endpoint_flow": str(metric_endpoint_flow),
            "H6_coordinate_null_speed": str(coordinate_null_speed),
            "H6_reversed_speed_product": str(endpoint_product),
            "H6_endpoint_limits": {"phi_to_negative_infinity": str(fast_endpoint), "phi_to_positive_infinity": str(slow_endpoint)},
            "H6_locally_measured_speed": str(locally_measured_speed),
            "H6_conditional_WRL_speed": str(wrl_coordinate_speed),
            "H6_conditional_WRL_limits": {"center": str(wrl_center_speed), "wall": str(wrl_wall_speed)},
            "H6_projective_metric_endpoints": {"fast": str(fast_projective_metric), "slow": str(slow_projective_metric)},
        },
        "adjudication": {
            "abandon_reciprocity_now": False,
            "adopt_literal_infinite_c_now": False,
            "regulated_infinite_c_logically_compatible_with_reciprocity": True,
            "local_time_parallel_conformal_block_discriminates_internal_reciprocity": False,
            "full_4d_metric_discrimination_established": False,
            "current_owner_foundation_changed": False,
            "owner_clarification_received_after_preregistration": True,
            "layered_atemporal_and_geometric_reciprocity_logically_compatible": True,
            "underlying_infinite_speed_well_typed_without_pregeometric_time_and_distance": False,
            "observable_superluminal_signalling_authorized": False,
            "metric_endpoint_interpretation_requires_abandoning_reciprocity": False,
            "metric_coordinate_speed_is_diffeomorphism_scalar": False,
            "local_orthonormal_speed_varies_with_phi": False,
            "distance_to_phi_endpoint_map_derived": False,
            "CMB_identified_with_phi_positive_infinity": False,
            "line_realization_gap_closed": False,
            "variation_domain_or_action_selected": False,
        },
        "next_discriminator": {
            "question": "Does positional dilation carry a native spacetime/internal pairing action beyond its CSN metric representative?",
            "required_evidence": [
                "native_pairing_or_representation_theorem",
                "finite_cell_or_bootstrap_selection_of_the_finite_residual",
                "universal_coupling_to_one_emergent_causal_cone",
                "ordered_spacetime_line_realization",
                "no_observable_superluminal_signalling_theorem",
                "native_distance_to_phi_profile_and_CMB_boundary_identification",
            ],
        },
        "environment": {"python": platform.python_version(), "sympy": sp.__version__, "cpu_only": True},
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    args.output.write_text(rendered, encoding="utf-8")
    transcript = [
        f"top_level_outcome={OUTCOME}",
        f"python={platform.python_version()}",
        f"sympy={sp.__version__}",
        f"checks={sum(checks.values())}/{len(checks)}",
        f"reciprocal_pairing={pairing_r}",
        f"reciprocal_metric_factor={reciprocal_factor}",
        f"reciprocal_component_limits=u:{u_limit},v:{v_limit}",
        f"nonreciprocal_pairing={pairing_nr}",
        f"nonreciprocal_determinant={determinant_nr}",
        f"CSN_scale_to_reciprocal={csn_scale}",
        f"residual_effective_speed={residual_causal_speed}",
        f"lorentz_residual={lorentz_residual}",
        f"projective_rank_one_endpoint={projective_endpoint}",
        f"H6_coordinate_null_speed={coordinate_null_speed}",
        f"H6_reversed_speed_product={endpoint_product}",
        f"H6_endpoint_limits=fast:{fast_endpoint},slow:{slow_endpoint}",
        f"H6_locally_measured_speed={locally_measured_speed}",
        f"H6_conditional_WRL_speed={wrl_coordinate_speed}",
        f"H6_conditional_WRL_limits=center:{wrl_center_speed},wall:{wrl_wall_speed}",
        f"H6_projective_metric_endpoints=fast:{fast_projective_metric},slow:{slow_projective_metric}",
        f"result_sha256={digest(rendered)}",
    ]
    args.transcript.write_text("\n".join(transcript) + "\n", encoding="utf-8")
    print("\n".join(transcript))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
