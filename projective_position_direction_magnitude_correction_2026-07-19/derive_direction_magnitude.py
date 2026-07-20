#!/usr/bin/env python3
"""Exact algebra for the direction–magnitude conceptual correction."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "DERIVATION_RESULT.json"


def require_zero(name: str, expression, checks: dict[str, str]) -> None:
    reduced = sp.simplify(expression)
    if isinstance(reduced, sp.MatrixBase):
        failed = any(sp.simplify(entry) != 0 for entry in reduced)
    else:
        failed = reduced != 0
    if failed:
        raise AssertionError(f"{name}: {reduced}")
    checks[name] = "PASS"


def require(name: str, condition: bool, checks: dict[str, str]) -> None:
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def main() -> None:
    checks: dict[str, str] = {}
    delta, phi_p, phi_o = sp.symbols("delta phi_p phi_o", real=True)
    rho = sp.symbols("rho", nonnegative=True)

    ordered = phi_p - phi_o
    swapped = phi_o - phi_p
    require_zero("ordered_comparison_antisymmetric", ordered + swapped, checks)
    separation = sp.Abs(ordered)
    require_zero("separation_symmetric_under_observer_exchange", separation - sp.Abs(swapped), checks)
    require("separation_nonnegative", separation.is_nonnegative is True, checks)
    require_zero("coincidence_has_zero_candidate_separation", separation.subs(phi_p, phi_o), checks)

    n1, n2, n3 = sp.symbols("n1 n2 n3", real=True)
    direction = sp.Matrix([n1, n2, n3])
    displacement = rho * direction
    reversed_displacement = rho * (-direction)
    require_zero("direction_reversal_flips_vector", reversed_displacement + displacement, checks)
    require_zero(
        "direction_reversal_preserves_magnitude_squared",
        reversed_displacement.dot(reversed_displacement) - displacement.dot(displacement),
        checks,
    )

    u = sp.exp(-delta)
    v = sp.exp(delta)
    require_zero("reciprocal_pair_product", u * v - 1, checks)
    require_zero("comparison_reversal_exchanges_u_to_v", u.subs(delta, -delta) - v, checks)
    require_zero("comparison_reversal_exchanges_v_to_u", v.subs(delta, -delta) - u, checks)
    require("ordered_u_not_direction_even", sp.simplify(u.subs(delta, -delta) - u) != 0, checks)
    require("ordered_v_not_direction_even", sp.simplify(v.subs(delta, -delta) - v) != 0, checks)

    xi = sp.tanh(delta)
    require_zero("projective_chart_is_oriented_odd", xi.subs(delta, -delta) + xi, checks)
    radial_chart = sp.tanh(rho)
    require_zero("radial_chart_at_coincidence", radial_chart.subs(rho, 0), checks)
    require_zero("radial_chart_unattainable_limit", sp.limit(radial_chart, rho, sp.oo) - 1, checks)

    epsilon, y = sp.symbols("epsilon y", real=True)
    radial_family = y + epsilon * y * (1 - y**2)
    require_zero("radial_counterfamily_zero_anchor", radial_family.subs(y, 0), checks)
    require_zero("radial_counterfamily_endpoint_anchor", radial_family.subs(y, 1) - 1, checks)
    require_zero("radial_counterfamily_witness", (radial_family - y).subs({epsilon: sp.Rational(1, 4), y: sp.Rational(1, 2)}) - sp.Rational(3, 32), checks)
    radial_derivative = sp.diff(radial_family, y)
    require_zero("radial_counterfamily_derivative", radial_derivative - (1 + epsilon * (1 - 3 * y**2)), checks)

    # Two distinct symmetric, CSN-neutral scalar clock candidates. Their
    # coexistence proves that direction-even, normalized slowing does not select
    # an observable from the reciprocal pair.
    U, V, scale = sp.symbols("U V scale", positive=True)
    clock_one = 2 * sp.sqrt(U * V) / (U + V)
    clock_two = clock_one**2
    require_zero("clock_one_csn_neutral", clock_one.subs({U: scale * U, V: scale * V}, simultaneous=True) - clock_one, checks)
    require_zero("clock_two_csn_neutral", clock_two.subs({U: scale * U, V: scale * V}, simultaneous=True) - clock_two, checks)
    require_zero("clock_one_exchange_even", clock_one.xreplace({U: V, V: U}) - clock_one, checks)
    require_zero("clock_two_exchange_even", clock_two.xreplace({U: V, V: U}) - clock_two, checks)

    clock_one_depth = sp.sech(delta)
    clock_two_depth = sp.sech(delta) ** 2
    require_zero("clock_one_direction_even", clock_one_depth.subs(delta, -delta) - clock_one_depth, checks)
    require_zero("clock_two_direction_even", clock_two_depth.subs(delta, -delta) - clock_two_depth, checks)
    require_zero("clock_candidates_normalized_at_zero", clock_one_depth.subs(delta, 0) - 1, checks)
    require_zero("clock_second_candidate_normalized_at_zero", clock_two_depth.subs(delta, 0) - 1, checks)
    require_zero("clock_one_radial_derivative", sp.diff(sp.sech(rho), rho) + sp.sech(rho) * sp.tanh(rho), checks)
    require_zero("clock_two_radial_derivative", sp.diff(sp.sech(rho) ** 2, rho) + 2 * sp.sech(rho) ** 2 * sp.tanh(rho), checks)
    require_zero("clock_one_witness", clock_one.subs({U: sp.Rational(1, 2), V: 2}) - sp.Rational(4, 5), checks)
    require_zero("clock_two_witness", clock_two.subs({U: sp.Rational(1, 2), V: 2}) - sp.Rational(16, 25), checks)
    require("clock_candidates_distinct", sp.Rational(4, 5) != sp.Rational(16, 25), checks)

    # The already-chosen local Lorentzian temporal slot supplies a narrower
    # conditional branch once depth is nonnegative. It is not an unconditional
    # extraction theorem from Reciprocity and CSN alone.
    slot_clock = sp.exp(-rho)
    require_zero("chosen_slot_clock_normalized_at_zero", slot_clock.subs(rho, 0) - 1, checks)
    require_zero("chosen_slot_clock_radial_derivative", sp.diff(slot_clock, rho) + slot_clock, checks)
    require_zero("chosen_slot_clock_non_speeding_witness", slot_clock.subs(rho, sp.log(2)) - sp.Rational(1, 2), checks)

    D = lambda depth: sp.diag(sp.exp(-depth), sp.exp(depth))
    require_zero("ordered_coframe_inverse_survives", D(delta) * D(-delta) - sp.eye(2), checks)
    require_zero("shared_static_difference_map_survives", D(phi_p) * D(phi_o).inv() - D(phi_p - phi_o), checks)

    seal_ordered = -phi_o
    seal_separation = sp.Abs(phi_o)
    require_zero("seal_ordered_comparison", ordered.subs(phi_p, 0) - seal_ordered, checks)
    require_zero("seal_candidate_separation", sp.Abs(seal_ordered) - seal_separation, checks)
    seal_radial_display = sp.tanh(seal_separation)
    require_zero("seal_radial_display_even_in_observer_side", seal_radial_display.subs(phi_o, -phi_o) - seal_radial_display, checks)

    result = {
        "schema": "udt-projective-direction-magnitude-correction-1.0",
        "python": sys.version.split()[0],
        "sympy": sp.__version__,
        "checks": checks,
        "conceptual_objects": {
            "ordered_comparison": {
                "definition": "delta(P;O)=Phi(P)-Phi(O)",
                "exchange": "delta(O;P)=-delta(P;O)",
                "classification": "DERIVED_CONDITIONAL_AS_ORDERED_RECIPROCAL_COMPARISON_NOT_DISTANCE",
            },
            "separation": {
                "minimal_candidate": "rho_candidate(P,O)=abs(delta(P;O))",
                "properties": "nonnegative symmetric and zero at coincidence",
                "classification": "CANDIDATE_NOT_A_DERIVED_GLOBAL_METRIC_DISTANCE",
            },
            "direction": {
                "representation": "displacement_candidate=rho*n_hat with rho>=0",
                "reversal": "n_hat -> -n_hat while rho is unchanged",
                "classification": "DIRECTION_REQUIRES_THE_ANGULAR_SECTOR_OR_A_CHOSEN_ONE_DIMENSIONAL_AXIS",
            },
            "projective_imbalance": {
                "signed_form": "xi=tanh(delta) is an oriented odd chart",
                "radial_form": "chi=tanh(rho) is a bounded magnitude display candidate",
                "classification": "ORIENTED_PROJECTIVE_COORDINATE_NOT_PHYSICAL_DISTANCE",
                "readout_status": "radial chart remains OPEN because the smooth f_epsilon family survives on [0,1]",
            },
            "clock_scalar": {
                "ordered_weights": "exp(-delta) and exp(+delta) exchange under ordered observer-comparison reversal; that operation is distinct from reversing angular direction at fixed rho",
                "conditional_chosen_slot": "the CHOSE local Lorentzian temporal slot gives exp(-rho) for rho>=0 and is unchanged by n_hat -> -n_hat",
                "conditional_status": "CONDITIONAL_IN_THE_CHOSEN_LOCAL_LORENTZIAN_TEMPORAL_SLOT",
                "admissible_candidate_one": "2*sqrt(u*v)/(u+v)=sech(delta)",
                "admissible_candidate_two": "[2*sqrt(u*v)/(u+v)]^2=sech(delta)^2",
                "properties": "smooth CSN-neutral exchange-even normalized and nonincreasing with rho",
                "classification": "UNCONDITIONAL_NATIVE_SCALAR_OPEN; RECIPROCITY_CSN_AND_DIRECTION_EVENNESS_ALONE_DO_NOT_SELECT_THE_READOUT",
            },
        },
        "coframe_regrade": {
            "survives": "D(delta)^-1=D(-delta), additive composition, CSN ray, and the additive L dphi seed inside the full reciprocal-weighted coframe",
            "does_not_follow": "inverse ordered comparison is not a physical clock-speed-up theorem",
            "classification": "EXACT_ALGEBRA_SURVIVES; CHOSEN_TEMPORAL_SLOT_IS_CONDITIONAL; UNCONDITIONAL_OBSERVER_CLOCK_EXTRACTION_REMAINS_OPEN",
        },
        "seal_regrade": {
            "absolute": "Phi(S)=0",
            "ordered": "delta(S;O)=-Phi(O)",
            "separation_candidate": "rho_candidate(S,O)=abs(Phi(O))",
            "projective_radial_candidate": "chi(S,O)=tanh(abs(Phi(O)))",
            "classification": "SEAL_IS_NEITHER_GENERIC_OBSERVER_COINCIDENCE_NOR_XMAX_ENDPOINT",
        },
        "revised_missing_maps": {
            "distance_map": "derive physical nonnegative separation from the complete metric including radial and angular path data",
            "clock_map": "derive why the local Lorentzian temporal slot is natively selected or derive the scalar clock observable without that slot choice",
            "projective_map": "decide whether X_max*tanh(rho) is an operational radial coordinate or only a bounded display",
            "status": "ALL_OPEN; IDENTIFIED_NOT_ADOPTED",
        },
        "adjudication": {
            "physical_signed_position": "WITHDRAWN_AS_A_CATEGORY_ERROR_FOR_DISTANCE",
            "signed_reciprocal_imbalance": "RETAINED_AS_ORIENTED_ALGEBRAIC_PROJECTIVE_COORDINATE",
            "negative_observer_distance": "REJECTED",
            "direction_induced_clock_speedup": "REJECTED_FOR_ANGULAR_REVERSAL_AT_FIXED_RHO; ORDERED_OBSERVER_COMPARISON_IS_DISTINCT",
            "global_distance": "OPEN",
            "scalar_clock_dilation": "CONDITIONAL_IN_CHOSEN_TEMPORAL_SLOT; UNCONDITIONAL_NATIVE_READOUT_OPEN",
            "angular_direction": "OPEN_BEYOND_THE_ABSTRACT_DIRECTION_SLOT",
        },
        "maximum_conclusion": "THE_PRIOR_SIGNED-POSITION LANGUAGE IS CORRECTED: SIGNED RECIPROCAL IMBALANCE IS AN ORIENTED ORDERED-COMPARISON CHART, NOT PHYSICAL DISTANCE; NONNEGATIVE SEPARATION REQUIRES A MAGNITUDE AND GLOBALLY THE COMPLETE RADIAL-ANGULAR METRIC; ANGULAR DIRECTION REVERSAL AT FIXED RHO IS DISTINCT FROM REVERSING AN ORDERED OBSERVER COMPARISON; THE CHOSEN LOCAL LORENTZIAN TEMPORAL SLOT CONDITIONALLY GIVES EXP(-RHO), BUT MULTIPLE EXACT CSN-NEUTRAL DIRECTION-EVEN READOUTS SURVIVE WITHOUT THAT SLOT, SO AN UNCONDITIONAL NATIVE CLOCK OBSERVABLE AND THE PHYSICAL RADIAL READOUT REMAIN OPEN",
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
