#!/usr/bin/env python3
"""Exact metric-led reciprocal comparison-bundle algebra."""

from __future__ import annotations

import json
import sympy as sp


def zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(value) == 0 for value in matrix)


def flatten(matrix: sp.Matrix) -> sp.Matrix:
    return matrix.reshape(matrix.rows * matrix.cols, 1)


def lorentz_generators() -> dict[str, sp.Matrix]:
    result: dict[str, sp.Matrix] = {}
    for i in range(1, 4):
        value = sp.zeros(4)
        value[0, i] = value[i, 0] = 1
        result[f"K0{i}"] = value
    for i, j in ((1, 2), (1, 3), (2, 3)):
        value = sp.zeros(4)
        value[i, j] = 1
        value[j, i] = -1
        result[f"J{i}{j}"] = value
    return result


def constraint_ranks(equations: list[sp.Expr], variables: tuple[sp.Symbol, ...]) -> tuple[int, int]:
    a, b = sp.linear_eq_to_matrix(equations, variables)
    return a.rank(), a.row_join(b).rank()


def main() -> None:
    eta = sp.diag(-1, 1, 1, 1)
    generators = lorentz_generators()
    checks: dict[str, str] = {}

    def check(name: str, condition: bool) -> None:
        if not condition:
            raise AssertionError(name)
        checks[name] = "PASS"

    # Full endomorphism -> symmetric metric-response quotient.
    xvars = sp.symbols("x0:16", real=True)
    Xfull = sp.Matrix(4, 4, xvars)
    response_full = sp.simplify(Xfull.T * eta + eta * Xfull)
    response_map, _ = sp.linear_eq_to_matrix(list(response_full), xvars)
    check("endomorphism_to_metric_response_rank_ten", response_map.rank() == 10)
    check("metric_response_kernel_dimension_six", 16 - response_map.rank() == 6)
    lorentz_columns = sp.Matrix.hstack(*(flatten(value) for value in generators.values()))
    check("lorentz_algebra_rank_six", lorentz_columns.rank() == 6)
    check(
        "lorentz_algebra_is_exact_response_kernel",
        all(zero(value.T * eta + eta * value) for value in generators.values()),
    )

    # Unique metric-self-adjoint representative of an infinitesimal response.
    Xdag = sp.simplify(eta.inv() * Xfull.T * eta)
    A = sp.simplify((Xfull + Xdag) / 2)
    Omega = sp.simplify((Xfull - Xdag) / 2)
    check("self_adjoint_part_is_self_adjoint", zero(eta.inv() * A.T * eta - A))
    check("skew_part_is_lorentz_algebra", zero(Omega.T * eta + eta * Omega))
    check("response_depends_only_on_self_adjoint_part", zero(response_full - (A.T * eta + eta * A)))

    # Exact seven-dimensional founded extension response fiber.
    extension_entries = [(2, 2), (2, 3), (3, 3), (2, 0), (2, 1), (3, 0), (3, 1)]
    extension_basis = []
    for i, j in extension_entries:
        value = sp.zeros(4)
        value[i, j] = 1
        extension_basis.append(value)
    extension_responses = [sp.simplify(value.T * eta + eta * value) for value in extension_basis]
    check("extension_generator_tangent_rank_seven", sp.Matrix.hstack(*(flatten(value) for value in extension_basis)).rank() == 7)
    check("extension_metric_response_rank_seven", sp.Matrix.hstack(*(flatten(value) for value in extension_responses)).rank() == 7)

    # Coordinate-free version: symmetric tensors with the three pair-plane components fixed.
    sym_entries = [(i, j) for i in range(4) for j in range(i, 4)]
    restriction = sp.zeros(3, len(sym_entries))
    for row, entry in enumerate(((0, 0), (0, 1), (1, 1))):
        restriction[row, sym_entries.index(entry)] = 1
    check("pair_plane_restriction_rank_three", restriction.rank() == 3)
    check("affine_response_fiber_dimension_seven", len(sym_entries) - restriction.rank() == 7)

    a, b, c, d, e, f, h = sp.symbols("a b c d e f h", real=True)
    response = sp.Matrix([[2, 0, a, b], [0, 2, c, d], [a, c, e, f], [b, d, f, h]])
    variables = (a, b, c, d, e, f, h)

    # Stabilizer strata: ordered pair SO(2), observer-only SO(3), ruler-only SO+(1,2), full Lorentz.
    def invariance_equations(names: tuple[str, ...]) -> list[sp.Expr]:
        equations: list[sp.Expr] = []
        for name in names:
            equations.extend(list(sp.simplify(generators[name].T * response + response * generators[name])))
        return equations

    pair_eq = invariance_equations(("J23",))
    pair_rank, pair_aug = constraint_ranks(pair_eq, variables)
    pair_solution = sp.linsolve(pair_eq, variables)
    check("ordered_pair_SO2_constraint_consistent", pair_rank == pair_aug)
    check("ordered_pair_SO2_invariant_dimension_one", 7 - pair_rank == 1)
    check("ordered_pair_SO2_invariant_family", pair_solution == sp.FiniteSet((0, 0, 0, 0, h, 0, h)))

    observer_eq = invariance_equations(("J12", "J13", "J23"))
    observer_rank, observer_aug = constraint_ranks(observer_eq, variables)
    observer_solution = sp.linsolve(observer_eq, variables)
    check("observer_SO3_constraint_unique", observer_rank == observer_aug == 7)
    check("observer_SO3_forces_plus_one_extension", observer_solution == sp.FiniteSet((0, 0, 0, 0, 2, 0, 2)))

    ruler_eq = invariance_equations(("K02", "K03", "J23"))
    ruler_rank, ruler_aug = constraint_ranks(ruler_eq, variables)
    ruler_solution = sp.linsolve(ruler_eq, variables)
    check("ruler_SO12_constraint_unique", ruler_rank == ruler_aug == 7)
    check("ruler_SO12_forces_minus_one_extension", ruler_solution == sp.FiniteSet((0, 0, 0, 0, -2, 0, -2)))

    full_eq = invariance_equations(tuple(generators))
    full_rank, full_aug = constraint_ranks(full_eq, variables)
    check("full_Lorentz_constraint_inconsistent_with_founded_pair", full_aug > full_rank)
    check("full_Lorentz_has_no_founded_affine_response", sp.linsolve(full_eq, variables) is sp.EmptySet)

    # Pair-query covariance for X_lambda=-P_u+P_n+lambda(I-P_u-P_n).
    lam = sp.symbols("lambda", real=True)
    u = sp.Matrix([1, 0, 0, 0])
    n = sp.Matrix([0, 1, 0, 0])
    P_u = -u * (u.T * eta)
    P_n = n * (n.T * eta)
    X_lam = sp.simplify(-P_u + P_n + lam * (sp.eye(4) - P_u - P_n))
    boost = sp.eye(4)
    boost[0, 0] = boost[2, 2] = sp.Rational(5, 3)
    boost[0, 2] = boost[2, 0] = sp.Rational(4, 3)
    check("rational_boost_is_Lorentz", zero(boost.T * eta * boost - eta))
    up, np = boost * u, boost * n
    P_up = -up * (up.T * eta)
    P_np = np * (np.T * eta)
    X_lam_p = sp.simplify(-P_up + P_np + lam * (sp.eye(4) - P_up - P_np))
    check("pair_query_transition_is_conjugation", zero(X_lam_p - boost * X_lam * boost.inv()))

    # Exact endpoint-frame covariance and path composition.
    rotation23 = sp.eye(4)
    rotation23[2, 2] = rotation23[3, 3] = sp.Rational(3, 5)
    rotation23[2, 3] = -sp.Rational(4, 5)
    rotation23[3, 2] = sp.Rational(4, 5)
    rotation12 = sp.eye(4)
    rotation12[1, 1] = rotation12[2, 2] = sp.Rational(3, 5)
    rotation12[1, 2] = -sp.Rational(4, 5)
    rotation12[2, 1] = sp.Rational(4, 5)
    check("rational_rotations_are_Lorentz", zero(rotation23.T * eta * rotation23 - eta) and zero(rotation12.T * eta * rotation12 - eta))
    U1, U2 = boost, rotation23
    Lp, Lq, Lr = rotation12, rotation23 * boost, boost * rotation12
    U1p = sp.simplify(Lq * U1 * Lp.inv())
    U2p = sp.simplify(Lr * U2 * Lq.inv())
    check("transport_composition_covariant", zero(U2p * U1p - Lr * U2 * U1 * Lp.inv()))
    source_generator = sp.diag(-1, 1, 0, 0)
    source_generator[2, 0] = sp.Rational(2)
    transformed_source = sp.simplify(Lp * source_generator * Lp.inv())
    transported_transformed = sp.simplify(U1p * transformed_source * U1p.inv())
    check(
        "generator_transport_covariant",
        zero(transported_transformed - Lq * (U1 * source_generator * U1.inv()) * Lq.inv()),
    )
    check("path_reversal_is_inverse", zero(U1.inv() * U1 - sp.eye(4)))

    # Tangent response does not determine a constant-generator finite continuation.
    q = sp.symbols("q", real=True)
    triangular = sp.diag(-1, 1, 0, 0)
    triangular[2, 0] = q
    triangular_dag = sp.simplify(eta.inv() * triangular.T * eta)
    symmetric_lift = sp.simplify((triangular + triangular_dag) / 2)

    def second_metric_jet(value: sp.Matrix) -> sp.Matrix:
        return sp.simplify(value.T * value.T * eta + 2 * value.T * eta * value + eta * value * value)

    check(
        "two_lifts_have_same_first_metric_jet",
        zero(triangular.T * eta + eta * triangular - (symmetric_lift.T * eta + eta * symmetric_lift)),
    )
    second_difference = sp.simplify(second_metric_jet(triangular) - second_metric_jet(symmetric_lift))
    check("two_lifts_differ_at_second_metric_jet", not zero(second_difference.subs(q, 1)))
    check("triangular_and_symmetric_lifts_are_distinct", not zero((triangular - symmetric_lift).subs(q, 1)))

    # The separately supplied clock/ruler swap is not an ordinary Lorentz transition.
    swap = sp.eye(4)
    swap[0, 0] = swap[1, 1] = 0
    swap[0, 1] = swap[1, 0] = 1
    check("reciprocal_swap_is_not_Lorentz", not zero(swap.T * eta * swap - eta))

    expected_check_count = 31
    check("registered_check_count_before_count_check", len(checks) == expected_check_count - 1)
    if len(checks) != expected_check_count:
        raise AssertionError(f"unexpected check count {len(checks)}")

    result = {
        "schema": "udt.native_reciprocal_comparison_bundle.derivation.v1",
        "result": "PASS",
        "sympy_version": sp.__version__,
        "check_count": len(checks),
        "ranks": {
            "endomorphism_space": 16,
            "metric_response": response_map.rank(),
            "Lorentz_kernel": 16 - response_map.rank(),
            "founded_pair_plane_constraints": restriction.rank(),
            "founded_affine_response_fiber": len(sym_entries) - restriction.rank(),
            "registered_extension_response": 7,
            "ordered_pair_SO2_invariant_subfamily": 7 - pair_rank,
            "observer_SO3_invariant_subfamily": 7 - observer_rank,
            "ruler_SO12_invariant_subfamily": 7 - ruler_rank,
        },
        "invariant_strata": {
            "ordered_pair_SO2": "ONE_PARAMETER_SCREEN_TRACE_FAMILY_LAMBDA_UNSELECTED",
            "observer_only_SO3": "UNIQUE_PLUS_ONE_RESPONSE_GIVEN_THIS_REDUCTION",
            "ruler_only_SO12": "UNIQUE_MINUS_ONE_RESPONSE_GIVEN_THIS_REDUCTION",
            "full_Lorentz": "NO_RESPONSE_COMPATIBLE_WITH_FIXED_FOUNDED_MINUS_PLUS_PAIR",
        },
        "derived_objects": {
            "fixed_metric_coframe_equivalence": "REPRESENTATIVE_FREEDOM",
            "ordered_pair_query_bundle": "METRIC_CANONICAL_MATHEMATICS_GIVEN_REGULAR_LORENTZ_METRIC_AND_ORIENTATION_SCOPE",
            "seven_dimensional_affine_metric_response_bundle": "UDT_DERIVED_OVER_ORDERED_PAIR_QUERY_BUNDLE_AT_INFINITESIMAL_LEVEL",
            "Levi_Civita_induced_transport": "METRIC_CANONICAL_MATHEMATICS_PHYSICAL_ROLE_OPEN",
            "path_labelled_transport": "EXACT_FOR_EVERY_SUPPLIED_PATH",
        },
        "open_objects": {
            "physical_observer_pair_section": True,
            "physical_path_family": True,
            "finite_constant_generator_lift": True,
            "complete_extension_section": True,
            "physical_comparison_functor": True,
            "variation_domain": True,
        },
        "finite_lift_control": {
            "same_first_metric_jet": True,
            "different_second_metric_jet_for_nonzero_mixing": True,
            "second_jet_difference": str(second_difference),
            "ruling": "INFINITESIMAL_RESPONSE_BUNDLE_DOES_NOT_SELECT_FINITE_COMPLETE_COFRAME_LIFT",
        },
        "maximum_conclusion": "NATIVE_AFFINE_RECIPROCAL_METRIC_RESPONSE_QUERY_BUNDLE_AND_METRIC_CANONICAL_TRANSPORT_DERIVED;_FINITE_LIFT_PHYSICAL_BASE_PATH_SECTION_AND_VARIATION_REMAIN_OPEN",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
