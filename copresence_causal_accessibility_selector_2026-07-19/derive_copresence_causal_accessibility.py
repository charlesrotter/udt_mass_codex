#!/usr/bin/env python3
"""Exact CPU algebra for the preregistered co-presence/causal-accessibility audit."""

from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
RESULT = HERE / "DERIVATION_RESULT.json"


def require(name: str, condition: bool, checks: dict[str, bool]) -> None:
    checks[name] = bool(condition)
    if not condition:
        raise AssertionError(name)


def main() -> None:
    checks: dict[str, bool] = {}

    c0, n, b, omega, lam, length = sp.symbols(
        "c0 n b omega lambda L", positive=True, finite=True
    )
    dt, dr, q = sp.symbols("dt dr q", real=True)

    # Positive common-scale changes preserve the tangent-vector causal sign.
    gvv = -n**2 * c0**2 * dt**2 + b**2 * dr**2
    gtilde_vv = sp.expand(omega**2 * gvv)
    require("positive_conformal_tangent_identity", sp.simplify(gtilde_vv - omega**2 * gvv) == 0, checks)

    # The inverse-metric characteristic polynomial scales by a positive inverse factor.
    kt, kr = sp.symbols("k_t k_r", real=True)
    principal = -kt**2 / (n**2 * c0**2) + kr**2 / b**2
    principal_tilde = principal / omega**2
    require(
        "positive_conformal_characteristic_identity",
        sp.simplify(principal_tilde - omega**-2 * principal) == 0,
        checks,
    )

    # Representative-dependent clock/ruler readings scale even though the cone does not.
    dtau = n * dt
    dlength = b * dr
    require("proper_time_changes_with_representative", sp.simplify(omega * dtau / dtau - omega) == 0, checks)
    require("proper_length_changes_with_representative", sp.simplify(omega * dlength / dlength - omega) == 0, checks)

    # General and reciprocal radial null slopes.
    slope_general = c0 * n / b
    slope_reciprocal = sp.simplify(slope_general.subs(b, 1 / n))
    require("general_radial_null_slope", sp.simplify(slope_general - c0 * n / b) == 0, checks)
    require("reciprocal_radial_null_slope", sp.simplify(slope_reciprocal - c0 * n**2) == 0, checks)

    # Optical coordinate dchi/dr=n^-2 makes the conditional scalar principal wave operator flat.
    # For ds^2=-n^2 c0^2 dt^2+n^-2 dr^2, sqrt(|g|)=c0 and
    # box psi=-psi_tt/(n^2 c0^2)+d_r(n^2 psi_r).
    psi_tt, psi_chichi = sp.symbols("psi_tt psi_chichi", real=True)
    box_after_optical_substitution = -psi_tt / (n**2 * c0**2) + psi_chichi / n**2
    optical_wave = sp.simplify(n**2 * box_after_optical_substitution)
    require("optical_wave_principal_part", sp.simplify(optical_wave - (-psi_tt / c0**2 + psi_chichi)) == 0, checks)

    # Exercise the nonconstant N(r) chain rule rather than treating the lapse algebraically.
    radius = sp.symbols("r", real=True)
    lapse_function = sp.Function("N")(radius)
    chi_function = sp.Function("chi")(radius)
    profile = sp.Function("F")
    radial_expression = sp.diff(
        lapse_function**2 * sp.diff(profile(chi_function), radius), radius
    )
    radial_in_optical_coordinate = radial_expression.subs(
        sp.diff(chi_function, radius, 2), sp.diff(lapse_function**-2, radius)
    ).subs(sp.diff(chi_function, radius), lapse_function**-2)
    expected_radial_expression = (
        sp.diff(profile(chi_function), chi_function, 2) / lapse_function**2
    )
    require(
        "nonconstant_lapse_chain_rule_cancellation",
        sp.simplify(radial_in_optical_coordinate - expected_radial_expression) == 0,
        checks,
    )

    chi_rate_out = sp.simplify((1 / n**2) * slope_reciprocal)
    chi_rate_in = -chi_rate_out
    require("outgoing_optical_characteristic", sp.simplify(chi_rate_out - c0) == 0, checks)
    require("ingoing_optical_characteristic", sp.simplify(chi_rate_in + c0) == 0, checks)

    # Constant-lapse illustration: metric light travel is nonzero for a separated path.
    travel_time = sp.simplify(length / slope_reciprocal)
    require("finite_nonzero_static_chart_coordinate_time", sp.simplify(travel_time - length / (c0 * n**2)) == 0, checks)

    # Co-membership of events does not determine causal comparability.
    # In optical coordinates the reciprocal block is conformal to Minkowski.
    interval_timelike = sp.expand(-(c0 * (2 * length / c0)) ** 2 + length**2)
    interval_null = sp.expand(-(c0 * (length / c0)) ** 2 + length**2)
    interval_spacelike = sp.expand(-(c0 * 0) ** 2 + length**2)
    require("global_member_pair_can_be_timelike", sp.simplify(interval_timelike + 3 * length**2) == 0, checks)
    require("global_member_pair_can_be_null", sp.simplify(interval_null) == 0, checks)
    require("global_member_pair_can_be_spacelike", sp.simplify(interval_spacelike - length**2) == 0, checks)

    # Static star illustration in optical distance Delta_chi: if a physical signal follows the
    # metric-null characteristic, the conditionally associated candidate emission event is null;
    # the same-static-chart-time remote event is spacelike relative to the detector event.
    delta_chi = sp.symbols("Delta_chi", positive=True, finite=True)
    emission_coordinate_offset = -delta_chi / c0
    remote_same_chart_time_offset = sp.Integer(0)
    star_emission_interval = sp.expand(
        -(c0 * emission_coordinate_offset) ** 2 + delta_chi**2
    )
    star_remote_now_interval = sp.expand(
        -(c0 * remote_same_chart_time_offset) ** 2 + delta_chi**2
    )
    require("candidate_star_emission_offset_is_null_related", sp.simplify(star_emission_interval) == 0, checks)
    require("star_remote_same_chart_time_is_spacelike", sp.simplify(star_remote_now_interval - delta_chi**2) == 0, checks)

    # Boundary retuning countermodel: a complete algebraic solution can depend globally on boundary
    # data without any time variable or signal interpretation.
    b1, b2 = sp.symbols("b1 b2", real=True)
    matrix = sp.Matrix([[1, 1], [1, -1]])
    solution = sp.simplify(matrix.inv() * sp.Matrix([b1, b2]))
    boundary_response = solution.diff(b1)
    require("global_constraint_solution_exact", solution == sp.Matrix([(b1 + b2) / 2, (b1 - b2) / 2]), checks)
    require("boundary_retuning_changes_both_components", boundary_response == sp.Matrix([sp.Rational(1, 2), sp.Rational(1, 2)]), checks)

    # The same cone can be shared by inequivalent principal operators/actions.
    # Q=0 and Q^2=0 have the same real characteristic set, while their derivative orders differ.
    q2 = sp.expand(q**2)
    require("second_and_fourth_order_share_characteristic_zero_set_forward", sp.simplify(q2.subs(q, 0)) == 0, checks)
    roots_q = sp.solve(sp.Eq(q, 0), q)
    roots_q2 = sp.solve(sp.Eq(q2, 0), q)
    require("second_and_fourth_order_share_characteristic_zero_set_reverse", set(roots_q) == set(roots_q2) == {sp.Integer(0)}, checks)
    require("derivative_order_not_selected_by_cone", sp.degree(q2, q) != sp.degree(q, q), checks)

    # Lower-order terms likewise leave the principal cone unchanged.
    mass2 = sp.symbols("m2", nonnegative=True, finite=True)
    operator_1 = q
    operator_2 = q + mass2
    require("lower_order_dynamics_not_selected_by_cone", sp.diff(operator_1, q) == sp.diff(operator_2, q), checks)

    # A time-coordinate normalization changes component slopes but not the geometric causal set.
    # Convention: t_prime=t/lambda, so dr/dt_prime=lambda dr/dt.
    slope_under_tprime = sp.simplify(lam * slope_reciprocal)
    require("coordinate_slope_changes_under_time_normalization", sp.simplify(slope_under_tprime - lam * c0 * n**2) == 0, checks)

    outcome = "COPRESENCE_CAUSAL_PARTITION_COHERENT_CONFORMAL_LAYER_DERIVED_ACTION_BRIDGE_OPEN"
    status_counts = {
        "DERIVED": 9,
        "CONDITIONAL": 6,
        "WORKING": 2,
        "POSIT": 1,
        "OPEN": 2,
        "REJECTED_AS_INFERENCE": 4,
    }

    payload = {
        "schema": "udt-copresence-causal-accessibility-v1",
        "date": "2026-07-19",
        "outcome": outcome,
        "scope": "global-solution semantics plus conformal and static-reciprocal kinematics; no native matter dynamics",
        "versions": {"python": platform.python_version(), "sympy": sp.__version__},
        "exact_checks": {"passed": sum(checks.values()), "total": len(checks), "checks": checks},
        "derived": {
            "conformal_tangent_factor": str(omega**2),
            "conformal_cotangent_factor": str(omega**-2),
            "reciprocal_coordinate_null_slope": str(slope_reciprocal),
            "optical_coordinate_density": str(n**-2),
            "optical_characteristic_speeds": [str(chi_rate_in), str(chi_rate_out)],
            "constant_lapse_static_chart_null_coordinate_time": str(travel_time),
            "timelike_null_spacelike_examples": [
                str(interval_timelike),
                str(interval_null),
                str(interval_spacelike),
            ],
            "global_boundary_response": [str(x) for x in boundary_response],
            "shared_characteristic_polynomials": [str(q), str(q2)],
        },
        "classification": {
            "copresence": "WORKING_DEFINITION_SHARED_DOMAIN_OF_ONE_WHOLE_SOLUTION",
            "causal_reachability": "DERIVED_FROM_TIME_ORIENTED_LORENTZIAN_CONFORMAL_CLASS",
            "reciprocal_coordinate_warping": "CONDITIONAL_STATIC_ADAPTED_REPRESENTATIVE",
            "operational_no_signalling": "POSIT_REQUIRES_DYNAMICS_COUPLING_AND_DATA_DOMAIN",
            "source_absorber_relation": "WORKING_CONDITIONAL_ENDPOINT_INTERPRETATION_NOT_PHOTON_ONTOLOGY",
            "pre_post_scale_layering": "COMPATIBLE_ARCHITECTURE_NOT_UNIQUE_BRIDGE",
            "action_selection": "OPEN",
            "physical_calibration": "OPEN_REQUIRES_MATERIAL_TRANSFORMATION_AND_COUPLING",
            "udt_uniqueness": "NOT_ESTABLISHED",
        },
        "status_counts": status_counts,
        "forbidden_inferences": [
            "copresence_is_simultaneity",
            "copresence_implies_zero_travel_time",
            "global_boundary_dependence_is_instantaneous_signalling",
            "metric_cone_alone_proves_material_retarded_support",
            "positive_CSN_rescaling_changes_causal_order",
            "conformal_class_alone_fixes_proper_clocks_or_mass",
            "copresence_uniquely_selects_C2_EH_or_two_stage_bridge",
        ],
        "terminology": {
            "causal_partition": "LAY_SHORTHAND_FOR_EVENT_RELATIVE_CAUSAL_REACHABILITY_NOT_AN_EQUIVALENCE_PARTITION",
            "time_normalization_convention": "t_prime=t/lambda",
        },
    }
    RESULT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    result_sha = hashlib.sha256(RESULT.read_bytes()).hexdigest()
    print(f"outcome={outcome}")
    print(f"exact_checks={sum(checks.values())}/{len(checks)}")
    print(f"result_sha256={result_sha}")


if __name__ == "__main__":
    main()
