#!/usr/bin/env python3
"""CPU-only symbolic anchors for the preregistered bootstrap selector audit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def variation_restriction_test() -> dict[str, object]:
    x, y = sp.symbols("x y")
    a, b, c, d, e, p, r = sp.symbols("a b c d e p r")
    action = a * x**2 + b * x * y + c * y**2 + d * x + e * y
    section = p * x + r
    reduced = sp.expand(action.subs(y, section))
    restrict_then_vary = sp.diff(reduced, x)
    tangent_chain_rule = sp.expand(
        sp.diff(action, x).subs(y, section)
        + sp.diff(action, y).subs(y, section) * sp.diff(section, x)
    )
    vary_then_restrict_tangent_only = sp.expand(sp.diff(action, x).subs(y, section))
    normal_term = sp.expand(
        sp.diff(action, y).subs(y, section) * sp.diff(section, x)
    )
    require(sp.expand(restrict_then_vary - tangent_chain_rule) == 0, "chain rule failed")
    require(normal_term != 0, "generic normal term was made vacuous")
    require(
        sp.expand(restrict_then_vary - vary_then_restrict_tangent_only - normal_term) == 0,
        "restriction/variation difference was not the normal term",
    )
    return {
        "result": "PASS",
        "identity": "dS_reduced/dx = S_x|section + S_y|section * f_prime",
        "normal_term": str(normal_term),
        "equivalence_condition": "S_y*f_prime = 0 on the admitted section",
    }


def selector_countermodel_test() -> dict[str, object]:
    q, sigma = sp.symbols("q sigma")
    q_star, sigma_star = sp.symbols("q_star sigma_star")
    lam, rho_star, kappa = sp.symbols("lambda rho_star kappa")
    epsilon = sp.symbols("epsilon", positive=True)
    narrowness_contract = "0 < epsilon << 1"

    closure = sigma - sigma_star
    total_density = rho_star + kappa * closure
    fractional_density_offset = sp.simplify((total_density - rho_star) / rho_star)

    pre_action = (q - q_star) ** 2
    pre_equation = sp.diff(pre_action, q)

    # sigma_star is an output of global closure, not a primitive local scale.
    post_action_on_selected_section = (
        sigma_star**2 * (q - q_star) ** 2 + lam * (q - q_star) ** 4
    )
    post_equation = sp.diff(post_action_on_selected_section, q)

    common_root = {q: q_star, sigma: sigma_star}
    require(sp.simplify(pre_equation.subs(common_root)) == 0, "pre model lacks common root")
    require(sp.simplify(post_equation.subs(common_root)) == 0, "post model lacks common root")
    require(sp.simplify(closure.subs(common_root)) == 0, "closure fails at common root")
    require(
        sp.simplify(total_density.subs(common_root) - rho_star) == 0,
        "proper-density center fails at common root",
    )
    require(
        sp.simplify(fractional_density_offset.subs(common_root)) == 0,
        "fractional narrow-window offset fails at common root",
    )
    require(epsilon.is_positive is True, "epsilon positivity premise missing")
    require(narrowness_contract == "0 < epsilon << 1", "narrow-window contract drift")
    require(
        sp.expand(post_action_on_selected_section - pre_action) != 0,
        "countermodel actions were accidentally identical off shell",
    )
    require(rho_star not in pre_action.free_symbols, "density inserted into pre local action")
    require(
        rho_star not in post_action_on_selected_section.free_symbols,
        "density inserted into post local action",
    )

    return {
        "result": "PASS",
        "shared_realized_root": {"q": "q_star", "sigma": "sigma_star"},
        "shared_global_closure": str(closure),
        "shared_density_at_root": "rho_tot = rho_star",
        "shared_matter_admissibility": str(sp.Abs(fractional_density_offset) < epsilon),
        "fractional_width_assumption": narrowness_contract,
        "fractional_width_fitted": False,
        "pre_model": {
            "variation_placement": "VARY_ON_CSN_QUOTIENT_THEN_APPLY_GLOBAL_CLOSURE",
            "action": str(pre_action),
            "equation": str(pre_equation),
        },
        "post_model": {
            "variation_placement": "GLOBAL_SELECTION_THEN_VARY_ON_SELECTED_SECTION",
            "action": str(post_action_on_selected_section),
            "equation": str(post_equation),
        },
        "local_density_insertion": False,
        "scope": "logical selector countermodels; not complete UDT universes",
    }


def conformal_weight_test() -> dict[str, object]:
    dimension = 4
    volume_weight = dimension
    scalar_curvature_weight = -2
    weyl_squared_weight = -4
    eh_weight = volume_weight + scalar_curvature_weight
    c2_weight = volume_weight + weyl_squared_weight
    require(eh_weight == 2, "four-dimensional EH constant-Weyl weight mismatch")
    require(c2_weight == 0, "four-dimensional C2 constant-Weyl weight mismatch")
    return {
        "result": "PASS",
        "dimension": dimension,
        "sqrt_g_weight": volume_weight,
        "R_weight": scalar_curvature_weight,
        "C2_weight": weyl_squared_weight,
        "sqrt_g_R_weight": eh_weight,
        "sqrt_g_C2_weight": c2_weight,
        "scope": "constant common scaling necessary-condition anchor only",
    }


def principal_order_test() -> dict[str, object]:
    k, alpha, beta, mass_scale = sp.symbols("k alpha beta M")
    difference = sp.expand(alpha * k**4 - beta * mass_scale**2 * k**2)
    polynomial = sp.Poly(difference, k)
    coefficient_equations = [sp.Eq(value, 0) for value in polynomial.all_coeffs()]
    solutions = sp.solve(coefficient_equations, (alpha, beta), dict=True)
    require(
        sp.expand(difference.subs({alpha: 1, beta: 1, mass_scale: 1})) != 0,
        "false fourth-to-second-order identity accepted",
    )
    require(
        all(solution.get(alpha, 0) == 0 for solution in solutions),
        "nonzero fourth-order coefficient survived polynomial identity",
    )
    return {
        "result": "PASS",
        "tested_identity": "alpha*k^4 == beta*M^2*k^2 for all k",
        "difference": str(difference),
        "coefficient_conditions": [str(item) for item in coefficient_equations],
        "nontrivial_identity_exists": False,
        "inference": "representative/scale selection alone does not lower principal order",
    }


def global_placement_test() -> dict[str, object]:
    q, sigma = sp.symbols("q sigma")
    q_star, sigma_star, eta = sp.symbols("q_star sigma_star eta")
    action = (q - q_star) ** 2
    closure = sigma - sigma_star
    multiplier_action = action + eta * closure
    predicate_equations = [sp.diff(action, q), closure]
    multiplier_equations = [
        sp.diff(multiplier_action, q),
        sp.diff(multiplier_action, sigma),
        sp.diff(multiplier_action, eta),
    ]
    selected_action = action.subs(sigma, sigma_star)
    selected_equations = [sp.diff(selected_action, q)]
    require(len(predicate_equations) == 2, "predicate model equation count drift")
    require(len(multiplier_equations) == 3, "multiplier model equation count drift")
    require(len(selected_equations) == 1, "selected-section equation count drift")
    require(multiplier_equations[1] == eta, "multiplier variation not exposed")
    return {
        "result": "PASS",
        "after_solution_predicate_equations": [str(item) for item in predicate_equations],
        "off_shell_multiplier_equations": [str(item) for item in multiplier_equations],
        "selected_section_equations": [str(item) for item in selected_equations],
        "equivalence_status": "NOT_ASSUMED",
    }


def build_result() -> dict[str, object]:
    tests = {
        "T2_variation_restriction": variation_restriction_test(),
        "T3_selector_countermodels": selector_countermodel_test(),
        "T4_conformal_weights": conformal_weight_test(),
        "T5_principal_order": principal_order_test(),
        "T6_global_placement": global_placement_test(),
    }
    require(all(test["result"] == "PASS" for test in tests.values()), "test failure")
    return {
        "result": "PASS",
        "mode": "CPU_ONLY_EXACT_SYMBOLIC",
        "sympy_version": sp.__version__,
        "top_level_outcome": "UNDERDETERMINED",
        "bootstrap_variation_domain": "OPEN_NOT_SELECTED",
        "two_stage_bridge": "OPEN_NOT_DERIVED",
        "strongest_bridge_result": "CONDITIONAL_CONTRACT_ONLY",
        "smallest_missing_off_shell_object": (
            "BOOTSTRAP_ROLE_AND_PLACEMENT: admissibility predicate vs varied global constraint "
            "vs representative-selection map"
        ),
        "independent_missing_bridge_object": "DYNAMICAL_MATCHING_THEOREM",
        "tests": tests,
        "promoted_action": "NONE",
        "carrier_assumed": False,
        "density_normalization_invented": False,
        "gpu_used": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = build_result()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
