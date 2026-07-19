#!/usr/bin/env python3
"""CPU-only exact anchors for the Reciprocity off-shell constraint selector."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def chart_component_test() -> dict[str, object]:
    a, b, alpha, beta = sp.symbols("a b alpha beta", positive=True)
    block = sp.diag(-a, b)
    # t_new=alpha*t and x_new=beta*x, hence dx/dx_new=diag(1/alpha,1/beta).
    jacobian = sp.diag(1 / alpha, 1 / beta)
    transformed = sp.simplify(jacobian.T * block * jacobian)
    old_product = sp.simplify((-block[0, 0]) * block[1, 1])
    new_product = sp.simplify((-transformed[0, 0]) * transformed[1, 1])
    require(old_product == a * b, "old component product drift")
    require(new_product == a * b / (alpha**2 * beta**2), "chart weight drift")
    require(
        sp.simplify(new_product.subs({a: 1, b: 1, alpha: 2, beta: 1}) - sp.Rational(1, 4)) == 0,
        "unit-product counterexample failed",
    )
    return {
        "result": "PASS",
        "metric_block": str(block),
        "coordinate_change": "t_new=alpha*t; x_new=beta*x",
        "old_component_product": str(old_product),
        "new_component_product": str(new_product),
        "unit_product_maps_to": "1/4 for alpha=2, beta=1",
        "component_product_is_scalar_without_carried_frame": False,
    }


def csn_decomposition_test() -> dict[str, object]:
    sigma, phi, omega = sp.symbols("sigma phi omega", real=True)
    a = sp.exp(2 * sigma - 2 * phi)
    b = sp.exp(2 * sigma + 2 * phi)
    product = sp.simplify(a * b)
    ratio = sp.simplify(b / a)
    a_scaled = sp.exp(2 * omega) * a
    b_scaled = sp.exp(2 * omega) * b
    scaled_product = sp.simplify(a_scaled * b_scaled)
    scaled_ratio = sp.simplify(b_scaled / a_scaled)
    require(product == sp.exp(4 * sigma), "scale product decomposition failed")
    require(ratio == sp.exp(4 * phi), "depth ratio decomposition failed")
    require(scaled_product == sp.exp(4 * omega + 4 * sigma), "CSN scale shift failed")
    require(scaled_ratio == sp.exp(4 * phi), "reciprocal depth changed under CSN")
    return {
        "result": "PASS",
        "a": "exp(2*sigma-2*phi)",
        "b": "exp(2*sigma+2*phi)",
        "sigma": "log(a*b)/4",
        "phi": "log(b/a)/4",
        "a_times_b": str(product),
        "b_over_a": str(ratio),
        "CSN_map": "sigma -> sigma+log(Omega); phi -> phi",
        "unit_product_equivalent_to": "sigma=0",
        "classification": "COMMON_SCALE_GAUGE_FIXING_AFTER_PAIRED_FRAME_AND_REPRESENTATIVE",
    }


def order_zero_natural_scalar_test() -> dict[str, object]:
    a0, a1, a2, a3 = sp.symbols("a0 a1 a2 a3", positive=True)
    eta = sp.diag(-1, 1, 1, 1)
    frame = sp.diag(sp.sqrt(a0), sp.sqrt(a1), sp.sqrt(a2), sp.sqrt(a3))
    metric = sp.simplify(frame.T * eta * frame)
    expected = sp.diag(-a0, a1, a2, a3)
    require(metric == expected, "Lorentz congruence orbit anchor failed")
    require(sp.det(metric) == -a0 * a1 * a2 * a3, "determinant drift")
    require(
        sp.simplify(sp.sqrt(-sp.det(metric)) - sp.det(frame)) == 0,
        "volume density congruence failed",
    )
    return {
        "result": "PASS",
        "orbit_anchor": "g=A^T eta A for every positive diagonal Lorentz block",
        "A": str(frame),
        "g": str(metric),
        "theorem": (
            "GL(4) acts transitively on nondegenerate Lorentz inner products of fixed signature; "
            "therefore every order-zero diffeomorphism-natural scalar of one metric is constant"
        ),
        "nontrivial_C_of_g_alone_exists_in_L0": False,
        "sqrt_abs_det_g": str(sp.det(frame)),
        "determinant_classification": "DENSITY_REQUIRING_A_REFERENCE_DENSITY_FOR_AN_EQUATION",
        "scope": "one metric; pointwise; algebraic; fixed dimension and Lorentz signature",
    }


def structured_candidate_test() -> dict[str, object]:
    a, b, omega = sp.symbols("a b omega", positive=True)
    # a=-g(T,T)/c^2 and b=g(N,N) after explicit T,N have been supplied.
    a_scaled = sp.simplify(omega**2 * a)
    b_scaled = sp.simplify(omega**2 * b)
    product_scaled = sp.simplify(a_scaled * b_scaled)
    ratio_scaled = sp.simplify(b_scaled / a_scaled)
    require(product_scaled == omega**4 * a * b, "structured product weight drift")
    require(ratio_scaled == b / a, "structured depth ratio lost CSN invariance")
    return {
        "result": "PASS",
        "candidate_data": ["metric g", "timelike vector T", "parallel vector N"],
        "a": "-g(T,T)/c^2",
        "b": "g(N,N)",
        "product_CSN_map": "a*b -> Omega^4*a*b",
        "depth": "phi=log(b/a)/4",
        "depth_CSN_invariant": True,
        "metric_only": False,
        "normalizing_T_and_N_makes_product": "tautologically one rather than a dynamical equation",
        "weighted_vector_escape": (
            "possible only after assigning extra Weyl weights/transformation laws to T and N"
        ),
        "native_status": "OPEN_EXTRA_STRUCTURE_NOT_DERIVED",
    }


def gauge_variation_test() -> dict[str, object]:
    phi, sigma, lam, phi_star, kappa = sp.symbols("phi sigma lambda phi_star kappa")
    invariant_action = (phi - phi_star) ** 2
    augmented = invariant_action + lam * sigma
    equations = [sp.diff(augmented, variable) for variable in (phi, sigma, lam)]
    solutions = sp.solve(equations, (phi, sigma, lam), dict=True)
    require(solutions == [{lam: 0, phi: phi_star, sigma: 0}], "gauge multiplier root drift")

    hard_action = invariant_action.subs(sigma, 0)
    hard_equation = sp.diff(hard_action, phi)
    readout_equation = sp.diff(invariant_action, phi)
    require(sp.simplify(hard_equation - readout_equation) == 0, "hard/readout gauge mismatch")

    violating_action = invariant_action + kappa * sigma + lam * sigma
    violating_equations = [sp.diff(violating_action, variable) for variable in (phi, sigma, lam)]
    violating_solutions = sp.solve(violating_equations, (phi, sigma, lam), dict=True)
    require(
        violating_solutions == [{lam: -kappa, phi: phi_star, sigma: 0}],
        "CSN-violating reaction drift",
    )
    require(
        sp.simplify((invariant_action + kappa * (sigma + 1)) - (invariant_action + kappa * sigma))
        == kappa,
        "CSN violation did not shift action",
    )
    return {
        "result": "PASS",
        "CSN_invariant_action": str(invariant_action),
        "readout_equation": str(readout_equation),
        "hard_sigma_zero_equation": str(hard_equation),
        "multiplier_equations": [str(item) for item in equations],
        "multiplier_root": {"phi": "phi_star", "sigma": "0", "lambda": "0"},
        "physical_normal_reaction_in_invariant_anchor": False,
        "reactive_corrupt_fixture": {
            "inserted_term": "kappa*sigma",
            "lambda": "-kappa",
            "classification": "CSN_VIOLATION_NOT_NATIVE_PRE_SCALE_REACTION",
        },
        "field_theory_identity": "local CSN invariance makes the conformal/scale Euler direction a Ward identity",
    }


def curvature_shortcut_test() -> dict[str, object]:
    # Constant diagonal metrics in Cartesian charts have zero connection derivatives and curvature,
    # while their raw component products can take arbitrary positive values.
    a, b = sp.symbols("a b", positive=True)
    coordinates = sp.symbols("t x")
    metric = sp.diag(-a, b)
    component_derivatives = [sp.diff(metric[i, j], coordinate) for i in range(2) for j in range(2) for coordinate in coordinates]
    require(all(item == 0 for item in component_derivatives), "constant flat metric derivative drift")
    products = {
        "unit_chart": sp.simplify((a * b).subs({a: 1, b: 1})),
        "rescaled_chart": sp.simplify((a * b).subs({a: sp.Rational(1, 4), b: 1})),
    }
    require(products == {"unit_chart": 1, "rescaled_chart": sp.Rational(1, 4)}, "flat chart products drift")
    return {
        "result": "PASS",
        "flat_metric_family": "diag(-a,b) with constant positive a,b",
        "connection_and_curvature": "zero in the displayed Cartesian charts",
        "component_products": {key: str(value) for key, value in products.items()},
        "curvature_condition_equivalent_to_component_product": False,
        "inference": "vanishing curvature cannot distinguish unit-product from rescaled flat charts",
        "all_derivative_or_nonlocal_constraints_excluded": False,
    }


def finite_cell_audit() -> dict[str, object]:
    return {
        "result": "PASS",
        "binding_input": "finite mirrored cell; static phi odd at seal, phi=0 there, normal derivative free",
        "supplies_boundary_normal": "AT_SEAL_ONLY_UP_TO_DECLARED_BOUNDARY_STRUCTURE",
        "supplies_bulk_time_parallel_two_plane": False,
        "supplies_CSN_representative_or_normalization": False,
        "boundary_or_nonlocal_selector": "OPEN_NOT_SUPPLIED",
        "complete_boundary_group_action_generator": "OPEN",
    }


def build_result() -> dict[str, object]:
    tests = {
        "T2_chart_component": chart_component_test(),
        "T3_CSN_decomposition": csn_decomposition_test(),
        "T4_order_zero_natural_scalar": order_zero_natural_scalar_test(),
        "T5_structured_candidate": structured_candidate_test(),
        "T6_gauge_variation": gauge_variation_test(),
        "T7_curvature_shortcut": curvature_shortcut_test(),
        "T8_finite_cell": finite_cell_audit(),
    }
    require(all(test["result"] == "PASS" for test in tests.values()), "load-bearing test failure")
    return {
        "result": "PASS",
        "mode": "CPU_ONLY_EXACT_SYMBOLIC_AND_NATURALITY_AUDIT",
        "sympy_version": sp.__version__,
        "top_level_outcome": "NO_L0_CONSTRAINT_REPRESENTATIVE_IDENTITY_IS_GAUGE_READOUT",
        "route_status": {
            "L0_metric_only_order_zero": "REFUTED_IN_CLASS",
            "L1_adapted_representative_product": "CSN_GAUGE_READOUT_CONDITIONAL_ON_FRAME_AND_REPRESENTATIVE",
            "L2_structured_covariant": "OPEN_EXTRA_STRUCTURE_NOT_DERIVED",
            "L3_derivative_metric_only": "OPEN_CURVATURE_SHORTCUT_NOT_EQUIVALENT",
            "L4_global_boundary": "OPEN_NOT_SUPPLIED",
        },
        "reciprocity_current_role": "DERIVED_KINEMATIC_COMPARISON_WITH_CONDITIONAL_METRIC_READOUT",
        "metric_only_off_shell_closure": "NOT_DERIVED",
        "native_auxiliary_constraint_required": False,
        "physical_multiplier_for_reciprocal_product": "NOT_DERIVED",
        "gauge_multiplier": "ALLOWED_BOOKKEEPING_WITH_ZERO_REACTION_IN_CSN_INVARIANT_ANCHOR",
        "off_shell_field_census": "OPEN_NARROWED",
        "smallest_missing_object": (
            "native natural selector/realization of the paired line directions, relative normalization, "
            "transformation law, degeneracy handling, and finite-cell extension"
        ),
        "complete_action": "OPEN",
        "boundary_completion": "OPEN",
        "promoted_action": "NONE",
        "carrier_or_source_assumed": False,
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
