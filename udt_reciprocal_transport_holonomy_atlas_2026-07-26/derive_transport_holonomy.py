#!/usr/bin/env python3
"""Exact local algebra for reciprocal transport and holonomy strata."""

from __future__ import annotations

import json
import sympy as sp


def check(name: str, condition: bool, checks: dict[str, str]) -> None:
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def unit(i: int, j: int) -> sp.Matrix:
    value = sp.zeros(4)
    value[i, j] = 1
    return value


def boost(i: int) -> sp.Matrix:
    return unit(0, i) + unit(i, 0)


def rotation(i: int, j: int) -> sp.Matrix:
    return unit(i, j) - unit(j, i)


def comm(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.simplify(left * right - right * left)


def solves_commutant(X: sp.Matrix, generators: list[sp.Matrix]) -> bool:
    return all(comm(X, generator) == sp.zeros(4) for generator in generators)


def main() -> None:
    checks: dict[str, str] = {}
    eta = sp.diag(-1, 1, 1, 1)
    I = sp.eye(4)
    lam, phi, z = sp.symbols("lam phi z", real=True)
    X = sp.diag(-1, 1, lam, lam)
    K1, K2, K3 = boost(1), boost(2), boost(3)
    J12, J13, J23 = rotation(1, 2), rotation(1, 3), rotation(2, 3)
    lorentz_generators = [K1, K2, K3, J12, J13, J23]

    def characteristic(value: sp.Matrix) -> sp.Expr:
        polynomial = value.charpoly()
        return sp.expand(polynomial.as_expr().subs(polynomial.gen, z))

    check("lift_is_eta_self_adjoint", X.T * eta == eta * X, checks)
    check("founded_pair_eigenvalues_fixed", X[0, 0] == -1 and X[1, 1] == 1, checks)
    check("lift_characteristic_polynomial", sp.factor(characteristic(X) - (z - 1) * (z + 1) * (z - lam) ** 2) == 0, checks)

    # R01: exact pathwise metric transport for every lambda.
    L = sp.eye(4)
    L[0, 0] = L[2, 2] = sp.Rational(5, 4)
    L[0, 2] = L[2, 0] = sp.Rational(3, 4)
    R = sp.eye(4)
    R[1, 1] = 0
    R[1, 3] = -1
    R[3, 1] = 1
    R[3, 3] = 0
    U = sp.simplify(R * L)
    check("path_transport_is_Lorentz", U.T * eta * U == eta, checks)
    Xt = sp.simplify(U * X * U.inv())
    check("transported_lift_eta_self_adjoint", sp.simplify(Xt.T * eta - eta * Xt) == sp.zeros(4), checks)
    check("transport_preserves_characteristic_polynomial", sp.factor(characteristic(Xt) - characteristic(X)) == 0, checks)
    check("transport_preserves_trace", sp.trace(Xt) == sp.trace(X), checks)
    check("transport_preserves_determinant", sp.det(Xt) == sp.det(X), checks)

    U1, U2 = L, R
    sequential = sp.simplify(U2 * (U1 * X * U1.inv()) * U2.inv())
    direct = sp.simplify((U2 * U1) * X * (U2 * U1).inv())
    check("path_transport_composes", sequential == direct, checks)
    check("path_transport_reverses", sp.simplify(U.inv() * Xt * U - X) == sp.zeros(4), checks)
    alternate = R
    Hloop = sp.simplify(alternate.inv() * U)
    endpoint_difference = sp.simplify(U * X * U.inv() - alternate * X * alternate.inv())
    loop_difference = sp.simplify(Hloop * X * Hloop.inv() - X)
    check(
        "two_path_equality_exactly_matches_holonomy_centralizer",
        sp.simplify(alternate.inv() * endpoint_difference * alternate - loop_difference) == sp.zeros(4),
        checks,
    )

    # R02-R08: holonomy centralizers. Infinitesimal generator commutation is
    # the connected restricted-holonomy criterion.
    screen = [J23]
    timelike = [J12, J13, J23]
    spacelike = [K2, K3, J23]
    boost_screen = [K1, J23]
    null = [K2 + J12, K3 + J13, J23]

    check("screen_holonomy_preserves_every_lambda", solves_commutant(X, screen), checks)
    check("timelike_holonomy_preserves_lambda_plus_one", solves_commutant(X.subs(lam, 1), timelike), checks)
    check("timelike_holonomy_rejects_lambda_zero", not solves_commutant(X.subs(lam, 0), timelike), checks)
    check("timelike_holonomy_rejects_lambda_minus_one", not solves_commutant(X.subs(lam, -1), timelike), checks)
    timelike_solutions = sp.solve(list(comm(X, J12)) + list(comm(X, J13)), lam)
    check("timelike_holonomy_unique_lambda_plus_one", timelike_solutions == {lam: 1}, checks)

    check("spacelike_holonomy_preserves_lambda_minus_one", solves_commutant(X.subs(lam, -1), spacelike), checks)
    check("spacelike_holonomy_rejects_lambda_zero", not solves_commutant(X.subs(lam, 0), spacelike), checks)
    check("spacelike_holonomy_rejects_lambda_plus_one", not solves_commutant(X.subs(lam, 1), spacelike), checks)
    spacelike_solutions = sp.solve(list(comm(X, K2)) + list(comm(X, K3)), lam)
    check("spacelike_holonomy_unique_lambda_minus_one", spacelike_solutions == {lam: -1}, checks)

    check("base_boost_never_commutes", comm(X, K1) != sp.zeros(4), checks)
    check("boost_screen_holonomy_rejects_all_lambda", not solves_commutant(X, boost_screen), checks)
    check("full_Lorentz_holonomy_rejects_all_lambda", not solves_commutant(X, lorentz_generators), checks)
    check("null_holonomy_rejects_lambda_plus_one", not solves_commutant(X.subs(lam, 1), null), checks)
    check("null_holonomy_rejects_lambda_minus_one", not solves_commutant(X.subs(lam, -1), null), checks)
    null_solutions = sp.solve(list(comm(X, null[0])) + list(comm(X, null[1])), lam)
    check("null_holonomy_has_no_lambda_solution", null_solutions == [], checks)

    # Dimensions of the allowed metric-connection algebra within so(1,3).
    coefficients = sp.symbols("c0:6", real=True)

    def stabilizer_basis(value: sp.Expr) -> list[sp.Matrix]:
        general = sum((coefficient * generator for coefficient, generator in zip(coefficients, lorentz_generators)), sp.zeros(4))
        equations = list(comm(X.subs(lam, value), general))
        matrix = sp.Matrix(equations).jacobian(coefficients)
        return matrix.nullspace()

    def same_coefficient_span(left: list[sp.Matrix], right: list[sp.Matrix]) -> bool:
        left_rank = sp.Matrix.hstack(*left).rank() if left else 0
        right_rank = sp.Matrix.hstack(*right).rank() if right else 0
        both_rank = sp.Matrix.hstack(*(left + right)).rank() if left or right else 0
        return left_rank == right_rank == both_rank

    coefficient_units = [sp.eye(6).col(index) for index in range(6)]
    generic_basis = stabilizer_basis(sp.Rational(1, 2))
    zero_basis = stabilizer_basis(0)
    plus_basis = stabilizer_basis(1)
    minus_basis = stabilizer_basis(-1)
    check("generic_lambda_connection_stabilizer_dimension_one", len(generic_basis) == 1, checks)
    check("lambda_zero_connection_stabilizer_dimension_one", len(zero_basis) == 1, checks)
    check("lambda_plus_one_connection_stabilizer_dimension_three", len(plus_basis) == 3, checks)
    check("lambda_minus_one_connection_stabilizer_dimension_three", len(minus_basis) == 3, checks)
    check("generic_stabilizer_basis_is_screen_rotation", same_coefficient_span(generic_basis, [coefficient_units[5]]), checks)
    check("lambda_zero_stabilizer_basis_is_screen_rotation", same_coefficient_span(zero_basis, [coefficient_units[5]]), checks)
    check("lambda_plus_one_stabilizer_basis_is_so3", same_coefficient_span(plus_basis, [coefficient_units[3], coefficient_units[4], coefficient_units[5]]), checks)
    check("lambda_minus_one_stabilizer_basis_is_so12", same_coefficient_span(minus_basis, [coefficient_units[1], coefficient_units[2], coefficient_units[5]]), checks)

    # Explicit two-path witnesses: equality exactly means loop holonomy
    # centralizes X. Generators suffice for connected groups, while these
    # finite representatives make path dependence concrete.
    theta_rotation = sp.eye(4)
    theta_rotation[1, 1] = 0
    theta_rotation[1, 2] = -1
    theta_rotation[2, 1] = 1
    theta_rotation[2, 2] = 0
    screen_rotation = sp.eye(4)
    screen_rotation[2, 2] = 0
    screen_rotation[2, 3] = -1
    screen_rotation[3, 2] = 1
    screen_rotation[3, 3] = 0
    check("finite_screen_loop_preserves_every_lambda", comm(X, screen_rotation) == sp.zeros(4), checks)
    check("finite_spatial_loop_preserves_lambda_plus_one", comm(X.subs(lam, 1), theta_rotation) == sp.zeros(4), checks)
    check("finite_spatial_loop_changes_lambda_zero", comm(X.subs(lam, 0), theta_rotation) != sp.zeros(4), checks)
    check("finite_boost_loop_changes_lambda_plus_one", comm(X.subs(lam, 1), L) != sp.zeros(4), checks)

    # R09: the reciprocal inverting transition is a normalizer, not an
    # ordinary Lorentz holonomy in the diagonal physical readout.
    F = sp.eye(4)
    F[0, 0] = 0
    F[0, 1] = 1
    F[1, 0] = 1
    F[1, 1] = 0
    check("reciprocal_swap_is_not_diagonal_eta_Lorentz", F.T * eta * F != eta, checks)
    twisted_residual = sp.simplify(F * X * F.inv() + X)
    check("twisted_generator_residual_is_two_lambda_screen", twisted_residual == sp.diag(0, 0, 2 * lam, 2 * lam), checks)
    check("twisted_generator_descent_lambda_zero", twisted_residual.subs(lam, 0) == sp.zeros(4), checks)
    check("twisted_generator_rejects_lambda_plus_one", twisted_residual.subs(lam, 1) != sp.zeros(4), checks)
    check("twisted_generator_rejects_lambda_minus_one", twisted_residual.subs(lam, -1) != sp.zeros(4), checks)
    check("trace_obstruction_for_nonzero_lambda", sp.trace(X) - sp.trace(-X) == 4 * lam, checks)
    char_difference = sp.factor(characteristic(X) - characteristic(-X))
    check("conjugacy_characteristic_obstruction", char_difference == -4 * lam * z * (z - 1) * (z + 1), checks)

    D = sp.diag(sp.exp(-phi), sp.exp(phi), sp.exp(lam * phi), sp.exp(lam * phi))
    Dminus = D.subs(phi, -phi)
    finite_residual = sp.simplify(F * D * F.inv() - Dminus)
    check("finite_twisted_descent_lambda_zero", finite_residual.subs(lam, 0) == sp.zeros(4), checks)
    check("finite_twisted_descent_rejects_lambda_plus_one_nonzero_phi", finite_residual.subs({lam: 1, phi: 1}) != sp.zeros(4), checks)
    check("finite_twisted_descent_rejects_lambda_minus_one_nonzero_phi", finite_residual.subs({lam: -1, phi: 1}) != sp.zeros(4), checks)
    finite_solutions = sp.solve(sp.Eq(sp.exp(lam), sp.exp(-lam)), lam)
    check("finite_real_twisted_descent_unique_lambda_zero", finite_solutions == [0], checks)
    check("phi_zero_twisted_test_is_vacuous_all_lambda", finite_residual.subs(phi, 0) == sp.zeros(4), checks)

    result = {
        "schema": "udt-reciprocal-transport-holonomy-atlas-1.0",
        "result": "PASS",
        "sympy_version": sp.__version__,
        "check_count": len(checks),
        "checks": checks,
        "counts": {
            "registered_routes": 12,
            "holonomy_strata": 15,
            "finite_cell_families": 12,
            "generic_connection_stabilizer_dimension": 1,
            "lambda_plus_one_stabilizer_dimension": 3,
            "lambda_minus_one_stabilizer_dimension": 3,
        },
        "conditional_selector_atlas": {
            "trivial_holonomy": "ALL_LAMBDA",
            "ordered_pair_screen_SO2": "ALL_LAMBDA",
            "timelike_line_SO3": "LAMBDA_PLUS_ONE",
            "spacelike_line_SO_PLUS_1_2": "LAMBDA_MINUS_ONE",
            "boost_screen_SO_PLUS_1_1_TIMES_SO2": "NO_LAMBDA",
            "full_SO_PLUS_1_3": "NO_LAMBDA",
            "null_stabilizer": "NO_REGULAR_SEMISIMPLE_LAMBDA",
            "reciprocal_Z2_odd_twisted_descent": "LAMBDA_ZERO",
        },
        "rulings": {
            "pathwise_transport": "DERIVED_GIVEN_COMPLETE_METRIC_INITIAL_LIFT_AND_PATH_FOR_EVERY_LAMBDA",
            "ordinary_path_independence": "HOLONOMY_CENTRALIZER_CONDITION; BRANCH_CONDITIONAL",
            "twisted_reciprocal_descent": "LAMBDA_ZERO_UNIQUE_CONDITIONAL_FOR_COMPLETE_ODD_LIFT",
            "lambda_selection": "NO_UNCONDITIONAL_SELECTION; PLUS_ONE_MINUS_ONE_ZERO_FOLLOW_FROM_DISTINCT_UNSELECTED_GLOBAL_STRUCTURES",
            "smallest_missing": "SELECTED_COMPLETE_BRANCH_AND_ORDINARY_VERSUS_TWISTED_GLOBAL_REDUCTION_WITH_PATH_MONODROMY_DATA",
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
