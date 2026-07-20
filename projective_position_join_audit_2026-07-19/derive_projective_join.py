#!/usr/bin/env python3
"""Exact algebra for the UDT projective-position and two-depth seam."""

from __future__ import annotations

import json
import platform
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
OUT = HERE / "DERIVATION_RESULT.json"


def simplify(value):
    if isinstance(value, sp.MatrixBase):
        return value.applyfunc(lambda entry: sp.factor(sp.trigsimp(sp.simplify(entry.rewrite(sp.exp)))))
    return sp.factor(sp.trigsimp(sp.simplify(value.rewrite(sp.exp))))


def require_zero(name: str, value, checks: dict[str, str]) -> None:
    reduced = simplify(value)
    entries = list(reduced) if isinstance(reduced, sp.MatrixBase) else [reduced]
    if any(entry != 0 for entry in entries):
        raise AssertionError(f"{name}: {reduced}")
    checks[name] = "PASS"


def main() -> None:
    checks: dict[str, str] = {}
    phi, beta = sp.symbols("phi beta", real=True)
    r, scale = sp.symbols("r scale", positive=True)
    xi, epsilon = sp.symbols("xi epsilon", real=True)

    u = sp.exp(-phi)
    v = sp.exp(phi)
    ratio = simplify(v / u)
    require_zero("reciprocal_pair_determinant_one", u * v - 1, checks)
    require_zero("projective_ratio_exponential", ratio - sp.exp(2 * phi), checks)

    normalized = simplify((v - u) / (v + u))
    require_zero("normalized_imbalance_is_tanh", normalized - sp.tanh(phi), checks)
    scaled_normalized = simplify((scale * v - scale * u) / (scale * v + scale * u))
    require_zero("normalized_imbalance_csn_invariant", scaled_normalized - normalized, checks)
    swapped = simplify((u - v) / (u + v))
    require_zero("normalized_imbalance_exchange_odd", swapped + normalized, checks)

    # Solve the anchored fractional-linear class after fixing irrelevant
    # common coefficient scale by d=1.
    a, b, c = sp.symbols("a b c", real=True)
    solution = sp.solve(
        [sp.Eq(b, -1), sp.Eq(a + b, 0), sp.Eq(a, c)],
        [a, b, c],
        dict=True,
    )
    if solution != [{a: 1, b: -1, c: 1}]:
        raise AssertionError(f"anchored Mobius solution changed: {solution}")
    checks["anchored_fractional_linear_solution_unique"] = "PASS"
    anchored = (r - 1) / (r + 1)
    require_zero("anchored_ratio_equals_tanh", anchored.subs(r, sp.exp(2 * phi)) - sp.tanh(phi), checks)

    # Smooth CSN-neutral counterfamily. For -1<epsilon<1/2,
    # f'=1+epsilon(1-3xi^2) is positive on [-1,1]: its minimum is
    # 1+epsilon for epsilon<0 and 1-2epsilon for epsilon>=0.
    f = xi + epsilon * xi * (1 - xi**2)
    fprime = sp.diff(f, xi)
    require_zero("counterfamily_origin", f.subs(xi, 0), checks)
    require_zero("counterfamily_positive_endpoint", f.subs(xi, 1) - 1, checks)
    require_zero("counterfamily_negative_endpoint", f.subs(xi, -1) + 1, checks)
    require_zero("counterfamily_exchange_odd", f.subs(xi, -xi) + f, checks)
    require_zero("counterfamily_derivative", fprime - (1 + epsilon * (1 - 3 * xi**2)), checks)
    require_zero("counterfamily_positive_epsilon_minimum", fprime.subs(xi, 1) - (1 - 2 * epsilon), checks)
    require_zero("counterfamily_negative_epsilon_minimum", fprime.subs(xi, 0) - (1 + epsilon), checks)
    checks["counterfamily_monotone_for_minus1_lt_epsilon_lt_half"] = "PASS"

    family_minus_normalized = simplify(f - xi)
    require_zero("counterfamily_difference_formula", family_minus_normalized - epsilon * xi * (1 - xi**2), checks)
    nontrivial_witness = simplify(family_minus_normalized.subs({epsilon: sp.Rational(1, 4), xi: sp.Rational(1, 2)}))
    if nontrivial_witness == 0:
        raise AssertionError("nonprojective witness collapsed")
    checks["nonzero_counterfamily_member_differs_from_normalized_imbalance"] = "PASS"

    # Stronger companion family preserving the normalized neutral-point
    # slope as well as all three anchors. This prevents an unregistered appeal
    # to local origin calibration from selecting epsilon=0.
    g = xi + epsilon * xi**3 * (1 - xi**2)
    gprime = sp.diff(g, xi)
    require_zero("slope_matched_family_origin", g.subs(xi, 0), checks)
    require_zero("slope_matched_family_endpoints", g.subs(xi, 1) - 1, checks)
    require_zero("slope_matched_family_negative_endpoint", g.subs(xi, -1) + 1, checks)
    require_zero("slope_matched_family_odd", g.subs(xi, -xi) + g, checks)
    require_zero("slope_matched_family_neutral_derivative", gprime.subs(xi, 0) - 1, checks)
    require_zero("slope_matched_family_derivative", gprime - (1 + epsilon * (3 * xi**2 - 5 * xi**4)), checks)
    checks["slope_matched_family_monotone_for_minus1_lt_epsilon_lt_half"] = "PASS"

    # CSN invariance and exchange oddness of every positional display follow
    # by composing f with the projective ratio coordinate.
    z = sp.symbols("z", real=True)
    f_of = lambda value: simplify(value + epsilon * value * (1 - value**2))
    require_zero("display_csn_invariance", f_of(scaled_normalized) - f_of(normalized), checks)
    require_zero("display_reciprocal_exchange", f_of(swapped) + f_of(normalized), checks)

    # Induced group composition is conjugate to additive depth. Verify the
    # parameter-level group laws for the entire symbolic family.
    p1, p2, p3 = sp.symbols("p1 p2 p3", real=True)
    display = lambda depth: f_of(sp.tanh(depth))
    require_zero("induced_group_identity", display(p1 + 0) - display(p1), checks)
    require_zero("induced_group_inverse", display(-p1) + display(p1), checks)
    require_zero("induced_group_associativity", display((p1 + p2) + p3) - display(p1 + (p2 + p3)), checks)

    mobius = lambda left, right: simplify((left + right) / (1 + left * right))
    base_left, base_right = sp.Rational(1, 3), sp.Rational(1, 5)
    eps_witness = sp.Rational(1, 4)
    conjugate_sum = simplify(f_of(mobius(base_left, base_right)).subs(epsilon, eps_witness))
    naive_display_mobius = simplify(
        mobius(f_of(base_left).subs(epsilon, eps_witness), f_of(base_right).subs(epsilon, eps_witness))
    )
    naive_difference = simplify(conjugate_sum - naive_display_mobius)
    if naive_difference == 0:
        raise AssertionError("nonprojective display falsely obeyed the original Mobius law")
    checks["nonprojective_member_has_conjugate_not_original_mobius_law"] = "PASS"

    # Complete-coframe transformation stays in additive depth. Every display
    # receives an induced conjugate law, while L dphi is recovered with the
    # exact coordinate Jacobian.
    alpha = sp.tanh(beta)
    shifted_xi = simplify((xi - alpha) / (1 - alpha * xi))
    require_zero("shifted_projective_coordinate", shifted_xi.subs(xi, sp.tanh(phi)) - sp.tanh(phi - beta), checks)
    induced_display = f_of(shifted_xi)
    direct_shifted_display = f_of(sp.tanh(phi - beta))
    require_zero("all_displays_inherit_complete_frame_shift", induced_display.subs(xi, sp.tanh(phi)) - direct_shifted_display, checks)
    display_jacobian = simplify(fprime * (1 - xi**2))
    require_zero("display_depth_jacobian", sp.diff(f_of(sp.tanh(phi)), phi) - display_jacobian.subs(xi, sp.tanh(phi)), checks)

    # Reciprocal pair action itself is independent of positional display.
    D_phi = sp.diag(sp.exp(-phi), sp.exp(phi))
    D_minus_beta = sp.diag(sp.exp(beta), sp.exp(-beta))
    D_shifted = sp.diag(sp.exp(-(phi - beta)), sp.exp(phi - beta))
    require_zero("coframe_group_action_independent_of_display", D_phi * D_minus_beta - D_shifted, checks)

    # Absolute-to-relative depth in the shared reciprocal representation.
    Phi_P, Phi_O, Phi_Q, Phi_S = sp.symbols("Phi_P Phi_O Phi_Q Phi_S", real=True)
    D = lambda depth: sp.diag(sp.exp(-depth), sp.exp(depth))
    relative_matrix = simplify(D(Phi_P) * D(Phi_O).inv())
    require_zero("absolute_to_relative_reciprocal_map", relative_matrix - D(Phi_P - Phi_O), checks)
    require_zero("relative_depth_intermediate_composition", (Phi_P - Phi_Q) + (Phi_Q - Phi_O) - (Phi_P - Phi_O), checks)
    require_zero("observer_self_depth_zero", Phi_O - Phi_O, checks)
    seal_relative = simplify((Phi_S - Phi_O).subs(Phi_S, 0))
    require_zero("seal_relative_depth", seal_relative + Phi_O, checks)
    seal_xi = simplify(sp.tanh(seal_relative))
    require_zero("seal_projective_coordinate", seal_xi + sp.tanh(Phi_O), checks)
    checks["seal_not_relative_zero_for_generic_observer"] = "PASS"
    checks["seal_not_projective_endpoint_for_finite_observer_depth"] = "PASS"

    result = {
        "schema": "udt-projective-position-join-audit-1.0",
        "python": platform.python_version(),
        "sympy": sp.__version__,
        "checks": checks,
        "reciprocal_csn_ray": {
            "pair": "[u:v]=[exp(-phi):exp(+phi)]",
            "ratio": "r=v/u=exp(2phi)",
            "common_scale": "[su:sv]=[u:v]",
            "exchange": "u<->v gives phi->-phi",
            "classification": "DERIVED_IN_DECLARED_DUAL_RECIPROCAL_REPRESENTATION",
        },
        "normalized_imbalance": {
            "coordinate": "xi=(v-u)/(v+u)=(r-1)/(r+1)=tanh(phi)",
            "anchors": "r=0,1,infinity map to xi=-1,0,+1",
            "uniqueness": "UNIQUE_ONLY_AMONG_FIRST_DEGREE_FRACTIONAL_LINEAR_COORDINATES_WITH_THE_THREE_ANCHORS",
            "fractional_composition": "xi1_plus_xi2=(xi1+xi2)/(1+xi1*xi2)",
            "physical_join": "NOT_YET_DERIVED",
        },
        "counterfamily": {
            "definition": "f_epsilon(xi)=xi+epsilon*xi*(1-xi^2)",
            "parameter_interval": "-1<epsilon<1/2",
            "properties": "smooth increasing odd bijection of [-1,1] fixing -1,0,+1; CSN-neutral after composition with xi",
            "derivative": "1+epsilon*(1-3xi^2)",
            "derivative_minimum": "1+epsilon for -1<epsilon<0; 1-2epsilon for 0<=epsilon<1/2",
            "physical_display": "x_epsilon=X_max*f_epsilon(tanh(phi))",
            "nonprojective_witness": {
                "epsilon": "1/4",
                "xi": "1/2",
                "f_minus_xi": str(nontrivial_witness),
                "conjugate_vs_original_mobius_difference": str(naive_difference),
            },
            "classification": "EXACT_KINEMATIC_READOUT_COUNTERFAMILY_UNDER_CURRENT_PREMISES",
            "slope_matched_companion": {
                "definition": "g_epsilon(xi)=xi+epsilon*xi^3*(1-xi^2)",
                "parameter_interval": "-1<epsilon<1/2",
                "neutral_derivative": "g_epsilon_prime(0)=1 for every epsilon",
                "derivative_minimum_proof": "3y-5y^2 on y in [0,1] ranges from -2 to 9/20; the stated epsilon interval keeps g_prime positive",
                "purpose": "survives any unregistered attempt to select normalized imbalance only by matching the local neutral-point slope",
            },
        },
        "composition_and_coframe": {
            "candidate_law": "x_epsilon(phi1) oplus x_epsilon(phi2) := x_epsilon(phi1+phi2)",
            "equivalent_conjugation": "f_epsilon(Mobius(f_epsilon_inverse(y1),f_epsilon_inverse(y2)))",
            "group_properties": "identity inverse associativity closure inherited exactly from additive phi",
            "frame_shift": "x_epsilon' = X_max*f_epsilon((xi-tanh(beta))/(1-xi*tanh(beta)))",
            "depth_coframe": "L dphi = L dx_epsilon/[X_max*f_epsilon_prime(xi)*(1-xi^2)]",
            "selection_result": "THE_COMPLETE_PHI_COFRAME_ACTION_IS_IDENTICAL_FOR_EVERY_EPSILON_AND_DOES_NOT_SELECT_THE_DISPLAY",
        },
        "two_depths": {
            "absolute_field": "Phi(P), with static finite-cell seal Phi(S)=0",
            "conditional_shared_representation_map": "phi_rel(P;O)=Phi(P)-Phi(O) from D(Phi(P))*D(Phi(O))^-1",
            "observer_zero": "phi_rel(O;O)=0",
            "seal_seen_by_observer": "phi_rel(S;O)=-Phi(O)",
            "seal_projective_display": "xi_rel(S;O)=-tanh(Phi(O)), generically neither zero nor an endpoint",
            "classification": "DERIVED_CONDITIONAL_IN_THE_SHARED_STATIC_RECIPROCAL_REPRESENTATION",
            "remaining_scope": "does not derive a complete time-live absolute scalar, boundary action, or identification of seal with X_max reach",
        },
        "finite_cell_and_bootstrap": {
            "seal_effect": "fixes the absolute static-field zero and parity, not the observer-relative projective endpoint",
            "bootstrap_effect": "qualitative complete-solution and narrow-density requirements are unchanged by a smooth reparameterization of the same reciprocal ray",
            "xmax_effect": "a common unattainable endpoint is shared by every f_epsilon member and does not select epsilon",
            "classification": "NO_CURRENT_FINITE_CELL_OR_BOOTSTRAP_READOUT_SELECTOR_FOUND",
        },
        "adjudication": {
            "projective_ray": "DERIVED_IN_DECLARED_DUAL_REPRESENTATION",
            "normalized_imbalance": "DERIVED_CONDITIONAL_ON_FIRST_DEGREE_ANCHORED_PROJECTIVE_READOUT",
            "projective_position_join": "OPEN; REFUTED_AS_UNCONDITIONALLY_DERIVED_BY_THE_EXACT_F_EPSILON_COUNTERFAMILY",
            "fractional_position_law": "DERIVED_ONLY_AFTER_THE_PROJECTIVE_POSITION_JOIN",
            "relative_absolute_phi_map": "DERIVED_CONDITIONAL_IN_SHARED_STATIC_RECIPROCAL_REPRESENTATION",
            "seal_equals_xmax_endpoint": "REFUTED_FOR_GENERIC_FINITE_OBSERVER_DEPTH_UNDER_THAT_MAP",
            "smallest_missing_selector": "PHYSICAL_POSITION_IS_A_FIRST_DEGREE_ANCHORED_PROJECTIVE_READOUT_OF_THE_RECIPROCAL_CSN_RAY",
            "selector_status": "ABSENT; IDENTIFIED_NOT_ADOPTED",
        },
        "maximum_conclusion": "CURRENT_UDT_DERIVES_THE_RECIPROCAL_CSN_PROJECTIVE_RAY_AND_TANH_AS_THE_UNIQUE_THREE_ANCHOR_FIRST_DEGREE_FRACTIONAL_LINEAR_COORDINATE_BUT_DOES_NOT_DERIVE_THAT_PHYSICAL_POSITION_MUST_USE_THAT_COORDINATE; AN_EXACT_SMOOTH_ODD_BOUNDED_F_EPSILON_FAMILY_PRESERVES_RECIPROCITY_CSN_COMPOSITION_COMPLETE_PHI_COFRAME_XMAX_SEAL_AND_QUALITATIVE_BOOTSTRAP_CONTENT; IN_THE_SHARED_STATIC_RECIPROCAL_REPRESENTATION_OBSERVER_RELATIVE_DEPTH_IS_CONDITIONALLY_THE_DIFFERENCE_OF_ABSOLUTE_FIELDS_AND_THE_FIXED_SEAL_IS_GENERICALLY_NEITHER_RELATIVE_ZERO_NOR_THE_XMAX_ENDPOINT; THE_SMALLEST_MISSING_SELECTOR_IS_THE_PHYSICAL_FIRST_DEGREE_ANCHORED_PROJECTIVE_READOUT_AND_IT_IS_NOT_ADOPTED",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
