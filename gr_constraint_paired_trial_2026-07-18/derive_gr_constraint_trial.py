#!/usr/bin/env python3
"""CPU-only exact anchors for the preregistered GR-constraint paired trial."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def generic_kkt_test() -> dict[str, object]:
    x, y, lam = sp.symbols("x y lambda")
    s0 = sp.Function("S_0")(x, y)
    constraint = sp.Function("C")(x, y)
    augmented = s0 + lam * constraint
    equations = [
        sp.diff(augmented, x),
        sp.diff(augmented, y),
        sp.diff(augmented, lam),
    ]
    expected = [
        sp.diff(s0, x) + lam * sp.diff(constraint, x),
        sp.diff(s0, y) + lam * sp.diff(constraint, y),
        constraint,
    ]
    require(all(sp.simplify(a - b) == 0 for a, b in zip(equations, expected)), "KKT drift")
    metric_only = [sp.diff(s0, x), sp.diff(s0, y)]
    require(equations != metric_only, "constraint equation was erased")
    return {
        "result": "PASS",
        "metric_only_equations": [str(item) for item in metric_only],
        "metric_plus_constraint_equations": [str(item) for item in equations],
        "off_shell_equivalence": False,
        "equivalence_requires": "C=0 plus proof that lambda*grad(C) is redundant",
    }


def paired_anchor_test() -> dict[str, object]:
    x, y, lam = sp.symbols("x y lambda")

    aligned_action = (x - 1) ** 2 + (y - 2) ** 2
    aligned_constraint = x + y - 3
    aligned_augmented = aligned_action + lam * aligned_constraint
    aligned_equations = [
        sp.diff(aligned_augmented, x),
        sp.diff(aligned_augmented, y),
        sp.diff(aligned_augmented, lam),
    ]
    aligned_solutions = sp.solve(aligned_equations, (x, y, lam), dict=True)
    require(aligned_solutions == [{lam: 0, x: 1, y: 2}], "aligned solution drift")
    aligned_metric_root = sp.solve(
        [sp.diff(aligned_action, x), sp.diff(aligned_action, y)], (x, y), dict=True
    )
    require(aligned_metric_root == [{x: 1, y: 2}], "aligned metric-only root drift")
    require(
        aligned_constraint.subs(aligned_metric_root[0]) == 0,
        "aligned metric root violates constraint",
    )

    reactive_action = x**2 + y**2
    reactive_constraint = x + y - 1
    reactive_augmented = reactive_action + lam * reactive_constraint
    reactive_equations = [
        sp.diff(reactive_augmented, x),
        sp.diff(reactive_augmented, y),
        sp.diff(reactive_augmented, lam),
    ]
    reactive_solutions = sp.solve(reactive_equations, (x, y, lam), dict=True)
    require(
        reactive_solutions == [{lam: -1, x: sp.Rational(1, 2), y: sp.Rational(1, 2)}],
        "reactive solution drift",
    )
    reactive_metric_root = sp.solve(
        [sp.diff(reactive_action, x), sp.diff(reactive_action, y)], (x, y), dict=True
    )
    require(reactive_metric_root == [{x: 0, y: 0}], "reactive metric-only root drift")
    require(
        reactive_constraint.subs(reactive_metric_root[0]) == -1,
        "reactive metric-only violation disappeared",
    )

    return {
        "result": "PASS",
        "aligned": {
            "S0": str(aligned_action),
            "C": str(aligned_constraint),
            "metric_only_root": {"x": "1", "y": "2"},
            "constrained_root": {"x": "1", "y": "2", "lambda": "0"},
            "classification": "REDUNDANT_AT_REALIZED_ROOT_ONLY",
        },
        "reactive": {
            "S0": str(reactive_action),
            "C": str(reactive_constraint),
            "metric_only_root": {"x": "0", "y": "0"},
            "metric_only_constraint_residual": "-1",
            "constrained_root": {"x": "1/2", "y": "1/2", "lambda": "-1"},
            "classification": "NONZERO_NORMAL_REACTION",
        },
        "inference": "shared roots can occur, but reactive constraints change the variational problem",
    }


def penalty_and_elimination_test() -> dict[str, object]:
    x, y, alpha = sp.symbols("x y alpha", positive=True)
    constraint = x + y - 1
    penalty_action = x**2 + y**2 + alpha * constraint**2 / 2
    penalty_equations = [sp.diff(penalty_action, x), sp.diff(penalty_action, y)]
    penalty_solution = sp.solve(penalty_equations, (x, y), dict=True)
    expected_root = alpha / (2 * (alpha + 1))
    require(
        penalty_solution == [{x: expected_root, y: expected_root}],
        "finite penalty root drift",
    )
    residual = sp.simplify(constraint.subs(penalty_solution[0]))
    require(residual == -1 / (alpha + 1), "finite penalty residual drift")
    require(residual != 0, "finite penalty falsely imposed exact constraint")
    require(sp.limit(residual, alpha, sp.oo) == 0, "penalty limit failed")
    reaction = sp.simplify(alpha * residual)
    require(sp.limit(reaction, alpha, sp.oo) == -1, "reaction limit failed")

    reduced_action = sp.expand((x**2 + y**2).subs(y, 1 - x))
    tangent_equation = sp.diff(reduced_action, x)
    reduced_root = sp.solve(tangent_equation, x)
    require(reduced_root == [sp.Rational(1, 2)], "hard elimination root drift")
    return {
        "result": "PASS",
        "finite_penalty": {
            "action": str(penalty_action),
            "root": {"x": str(expected_root), "y": str(expected_root)},
            "constraint_residual": str(residual),
            "effective_reaction": str(reaction),
            "exact_for_finite_positive_alpha": False,
            "singular_limit": "alpha -> infinity",
        },
        "hard_elimination": {
            "substitution": "y=1-x",
            "reduced_action": str(reduced_action),
            "tangent_equation": str(tangent_equation),
            "root": "1/2",
            "equals_branch_A": False,
            "reason": "variation is restricted to the constraint tangent space",
        },
    }


def covariance_identity_test() -> dict[str, object]:
    # A finite gauge analogue checks the field-census point algebraically: an invariant
    # action can contain two transforming fields without violating its Noether identity.
    u, v = sp.symbols("u v")
    action = (u - v) ** 2
    e_u = sp.diff(action, u)
    e_v = sp.diff(action, v)
    noether_identity = sp.simplify(e_u + e_v)
    require(noether_identity == 0, "finite Noether identity failed")

    # Illustrative 4D bulk witness, not a proposed UDT action.  Let c denote a
    # component-level Weyl-curvature amplitude, so W=C_abcd C^abcd is represented
    # by c**2.  Both the metric-only C^2 density and its scalar-multiplier extension
    # have the flat reciprocal root c=0.  The weight and tensor interpretation are
    # audited separately; this algebra checks the common stationary root.
    c, lam = sp.symbols("c lambda")
    branch_a_density = c**2
    branch_b_density = (1 + lam) * c**2
    branch_a_equation = sp.diff(branch_a_density, c)
    branch_b_equations = [sp.diff(branch_b_density, c), sp.diff(branch_b_density, lam)]
    require(branch_a_equation.subs(c, 0) == 0, "4D witness A lost flat root")
    require(
        all(equation.subs(c, 0) == 0 for equation in branch_b_equations),
        "4D witness B lost flat constrained root",
    )

    metric_identity = "2*nabla_mu(E_g^{mu}{}_{nu}) = 0"
    metric_scalar_identity = (
        "2*nabla_mu(E_g^{mu}{}_{nu}) = E_lambda*nabla_nu(lambda)"
    )
    return {
        "result": "PASS",
        "finite_gauge_analogue": {
            "action": str(action),
            "delta_u": "epsilon",
            "delta_v": "epsilon",
            "identity": str(noether_identity),
        },
        "metric_only_noether_identity": metric_identity,
        "metric_plus_scalar_noether_identity": metric_scalar_identity,
        "on_auxiliary_shell": "E_lambda=0 restores the metric-only divergence identity",
        "field_census_selected_by_covariance": False,
        "illustrative_4D_bulk_witness": {
            "W": "C_abcd*C^abcd (represented by curvature amplitude c**2)",
            "branch_A": "integral_M sqrt(|g|) W",
            "branch_B": "integral_M sqrt(|g|) (1+lambda) W",
            "lambda_equation": "W=0",
            "shared_bulk_root": "flat reciprocal metric (phi=0, W=0) on a finite cell",
            "CSN_weights": "w_W=-4; w_lambda=0",
            "classification": "CATEGORY_A_EXISTENCE_WITNESS_NOT_NATIVE_ACTION",
            "complete_UDT_universe": False,
        },
        "scope": "bulk diffeomorphism identity; boundary differentiability remains separate",
    }


def csn_weight_test() -> dict[str, object]:
    w_c = sp.symbols("w_C")
    dimension = 4
    w_sqrt_g = dimension
    w_lambda = -dimension - w_c
    total = sp.simplify(w_sqrt_g + w_lambda + w_c)
    require(total == 0, "CSN compensation failed")
    return {
        "result": "PASS",
        "dimension": dimension,
        "sqrt_g_weight": w_sqrt_g,
        "constraint_scalar_weight": str(w_c),
        "required_multiplier_weight": str(w_lambda),
        "total_integrand_weight": str(total),
        "classification_only": True,
        "caveat": "C must transform homogeneously; local inhomogeneous terms require a separate audit",
        "constraint_or_multiplier_derived": False,
    }


def finite_cell_boundary_test() -> dict[str, object]:
    z = sp.symbols("z")
    q = sp.Function("q")(z)
    lam = sp.Function("lambda")(z)
    lagrangian = sp.diff(q, z) ** 2 / 2 + lam * sp.diff(q, z)
    e_q = sp.simplify(sp.diff(lagrangian, q) - sp.diff(sp.diff(lagrangian, sp.diff(q, z)), z))
    e_lambda = sp.diff(lagrangian, lam)
    boundary_momentum = sp.diff(lagrangian, sp.diff(q, z))
    require(e_q == -sp.diff(q, z, 2) - sp.diff(lam, z), "boundary anchor q equation drift")
    require(e_lambda == sp.diff(q, z), "boundary anchor constraint drift")
    require(boundary_momentum == sp.diff(q, z) + lam, "boundary momentum drift")
    return {
        "result": "PASS",
        "one_dimensional_anchor": {
            "L": str(lagrangian),
            "E_q": str(e_q),
            "E_lambda": str(e_lambda),
            "endpoint_variation": f"({boundary_momentum})*delta(q)",
            "added_constraint_boundary_piece": "lambda(z)*delta(q)",
        },
        "inference": "a covariant bulk constraint can alter the finite-cell differentiability problem",
        "boundary_completion_selected": False,
    }


def build_result() -> dict[str, object]:
    tests = {
        "T2_generic_KKT": generic_kkt_test(),
        "T3_redundant_and_reactive": paired_anchor_test(),
        "T4_penalty_and_elimination": penalty_and_elimination_test(),
        "T5_covariance_field_census": covariance_identity_test(),
        "T6_CSN_weight": csn_weight_test(),
        "T7_finite_cell_boundary": finite_cell_boundary_test(),
    }
    require(all(item["result"] == "PASS" for item in tests.values()), "load-bearing test failed")
    return {
        "result": "PASS",
        "mode": "CPU_ONLY_EXACT_SYMBOLIC",
        "sympy_version": sp.__version__,
        "top_level_outcome": "BOTH_CONDITIONALLY_ADMISSIBLE",
        "common_trial": {
            "four_dimensions": "INHERITED",
            "diffeomorphism_covariance": "RETAIN_TRIAL_CONDITIONAL",
            "full_finite_cell_diffeomorphism_group": "UNRESOLVED_TRIAL",
            "finite_mirrored_cell": "CANONIZED_BINDING",
            "unrestricted_variation_of_declared_fields": "RETAIN_TRIAL",
        },
        "branch_A_metric_only": "UNRESOLVED_TRIAL",
        "branch_B_auxiliary_constraint": "UNRESOLVED_TRIAL",
        "field_census_selected": False,
        "bootstrap_selects_branch": False,
        "metric_is_theory_excludes_auxiliary_bookkeeping": "NOT_ESTABLISHED",
        "locality": "OPEN_NOT_ADOPTED",
        "derivative_order": "OPEN_NOT_ADOPTED",
        "invariant_inventory": "OPEN_NOT_ADOPTED",
        "complete_action": "OPEN",
        "native_source": "OPEN",
        "boundary_completion": "OPEN",
        "next_missing_selector": (
            "native off-shell field/constraint authority: a theorem excluding auxiliary varied "
            "constraints, or a derived constraint functional requiring one"
        ),
        "promoted_action": "NONE",
        "matter_or_carrier_assumed": False,
        "density_normalization_invented": False,
        "gpu_used": False,
        "tests": tests,
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
