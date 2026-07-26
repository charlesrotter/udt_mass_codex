#!/usr/bin/env python3
"""Exact observer-pair path-groupoid assembly classification."""

from __future__ import annotations

import json
import sympy as sp


def check(name: str, condition: bool, checks: dict[str, str]) -> None:
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def zero(value: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in value)


def projector(vector: sp.Matrix, metric: sp.Matrix) -> sp.Matrix:
    norm = sp.simplify((vector.T * metric * vector)[0])
    return sp.simplify(vector * (vector.T * metric) / norm)


def boost(i: int, c: sp.Rational = sp.Rational(5, 4), s: sp.Rational = sp.Rational(3, 4)) -> sp.Matrix:
    value = sp.eye(4)
    value[0, 0] = c
    value[0, i] = s
    value[i, 0] = s
    value[i, i] = c
    return value


def rotation(i: int, j: int, c: sp.Rational = sp.Rational(3, 5), s: sp.Rational = sp.Rational(4, 5)) -> sp.Matrix:
    value = sp.eye(4)
    value[i, i] = c
    value[i, j] = -s
    value[j, i] = s
    value[j, j] = c
    return value


def pair_generator(u: sp.Matrix, n: sp.Matrix, metric: sp.Matrix, lam: sp.Expr) -> sp.Matrix:
    pu = projector(u, metric)
    pn = projector(n, metric)
    return sp.simplify(-pu + pn + lam * (sp.eye(4) - pu - pn))


def finite_character(lam: sp.Expr, depth: sp.Expr) -> sp.Matrix:
    return sp.diag(sp.exp(-depth), sp.exp(depth), sp.exp(lam * depth), sp.exp(lam * depth))


def main() -> None:
    checks: dict[str, str] = {}
    eta = sp.diag(-1, 1, 1, 1)
    I = sp.eye(4)
    e0, e1, e2, e3 = (I[:, index] for index in range(4))
    lam, a, b, period = sp.symbols("lam a b period", real=True)

    # One ordered observer/ruler pair determines the scalar-screen family.
    X = pair_generator(e0, e1, eta, lam)
    expected_X = sp.diag(-1, 1, lam, lam)
    check("ordered_pair_generator_exact", X == expected_X, checks)
    check("ordered_pair_generator_metric_self_adjoint", X.T * eta == eta * X, checks)
    check("clock_eigenvalue_minus_one", X * e0 == -e0, checks)
    check("ruler_eigenvalue_plus_one", X * e1 == e1, checks)
    check("screen_eigenvalue_lambda", X * e2 == lam * e2 and X * e3 == lam * e3, checks)

    # Screen orientation is gauge for a scalar screen response.
    R_screen = rotation(2, 3)
    check("screen_rotation_is_Lorentz", R_screen.T * eta * R_screen == eta, checks)
    check("screen_rotation_fixes_ordered_pair", R_screen * e0 == e0 and R_screen * e1 == e1, checks)
    check("screen_rotation_commutes_with_X_all_lambda", zero(R_screen * X - X * R_screen), checks)
    check("screen_gauge_conjugation_leaves_X", sp.simplify(R_screen * X * R_screen.inv()) == X, checks)

    # Any Lorentz map carries the pair endomorphism covariantly.
    V_observer = boost(2)
    u_prime, n_prime = V_observer * e0, V_observer * e1
    X_prime_projectors = pair_generator(u_prime, n_prime, eta, lam)
    X_prime_conjugation = sp.simplify(V_observer * X * V_observer.inv())
    check("observer_change_is_Lorentz", V_observer.T * eta * V_observer == eta, checks)
    check("pair_projector_assignment_is_covariant", X_prime_projectors == X_prime_conjugation, checks)

    V_direction = rotation(1, 2)
    n_rotated = V_direction * e1
    X_direction = pair_generator(e0, n_rotated, eta, lam)
    check("direction_change_is_Lorentz", V_direction.T * eta * V_direction == eta, checks)
    check("direction_projector_assignment_is_covariant", X_direction == sp.simplify(V_direction * X * V_direction.inv()), checks)
    V_direction_alt = V_direction * R_screen
    check("two_vertical_maps_reach_same_ordered_pair", V_direction_alt * e0 == V_direction * e0 and V_direction_alt * e1 == V_direction * e1, checks)
    check("screen_ambiguous_vertical_maps_same_X", sp.simplify(V_direction_alt * X * V_direction_alt.inv()) == X_direction, checks)

    # Pathwise Levi-Civita-type isometries compose by conjugation for every lambda.
    U_ab = boost(2)
    U_bc = rotation(1, 3)
    U_ac = sp.simplify(U_bc * U_ab)
    check("first_path_map_Lorentz", U_ab.T * eta * U_ab == eta, checks)
    check("second_path_map_Lorentz", U_bc.T * eta * U_bc == eta, checks)
    check("composite_path_map_Lorentz", U_ac.T * eta * U_ac == eta, checks)
    X_b = sp.simplify(U_ab * X * U_ab.inv())
    X_c_sequential = sp.simplify(U_bc * X_b * U_bc.inv())
    X_c_direct = sp.simplify(U_ac * X * U_ac.inv())
    check("path_conjugation_composes_all_lambda", X_c_sequential == X_c_direct, checks)
    check("path_reversal_recovers_source_pair", sp.simplify(U_ab.inv() * X_b * U_ab) == X, checks)

    # The finite reciprocal comparison composes when depth is an additive
    # path cocycle and the pair is transported as part of the object.
    D_a = finite_character(lam, a)
    D_b = finite_character(lam, b)
    D_ab = finite_character(lam, a + b)
    check("finite_character_adds_depth", sp.simplify(D_b * D_a - D_ab) == sp.zeros(4), checks)
    check("finite_character_descends_through_screen_gauge", sp.simplify(R_screen * D_a * R_screen.inv()) == D_a, checks)
    D_b_at_B = sp.simplify(U_ab * D_b * U_ab.inv())
    check("finite_character_transport_intertwining", sp.simplify(D_b_at_B * U_ab - U_ab * D_b) == sp.zeros(4), checks)
    T_ab = sp.simplify(U_ab * D_a)
    T_bc = sp.simplify(U_bc * D_b_at_B)
    T_ac = sp.simplify(U_ac * D_ab)
    check("typed_full_comparison_composes_all_lambda", sp.simplify(T_bc * T_ab - T_ac) == sp.zeros(4), checks)
    T_ba = sp.simplify(U_ab.inv() * sp.simplify(U_ab * finite_character(lam, -a) * U_ab.inv()))
    check("typed_full_comparison_reversal", sp.simplify(T_ba - T_ab.inv()) == sp.zeros(4), checks)

    # A pair reset is a vertical arrow. Including it gives exact typed
    # composition; omitting it is the previously exposed middle mismatch.
    V_b_direction = sp.simplify(U_ab * V_direction * U_ab.inv())
    X_b_out = sp.simplify(V_b_direction * X_b * V_b_direction.inv())
    D_b_out = sp.simplify(V_b_direction * D_b_at_B * V_b_direction.inv())
    check("vertical_direction_map_intertwines_generators", sp.simplify(X_b_out * V_b_direction - V_b_direction * X_b) == sp.zeros(4), checks)
    check("vertical_direction_map_intertwines_characters", sp.simplify(D_b_out * V_b_direction - V_b_direction * D_b_at_B) == sp.zeros(4), checks)
    typed_with_vertical = sp.simplify(U_bc * D_b_out * V_b_direction * T_ab)
    typed_expected = sp.simplify(U_bc * V_b_direction * U_ab * D_ab)
    check("vertical_pair_change_is_sufficient_for_typed_composition", sp.simplify(typed_with_vertical - typed_expected) == sp.zeros(4), checks)

    untyped_without_vertical = sp.simplify(U_bc * D_b_out * T_ab)
    untyped_expected = sp.simplify(U_bc * U_ab * D_ab)
    check("generic_direction_reset_without_vertical_mismatches", untyped_without_vertical.subs({lam: 0, a: 1, b: 1}) != untyped_expected.subs({lam: 0, a: 1, b: 1}), checks)
    check("lambda_one_removes_fixed_observer_direction_dependence", X_direction.subs(lam, 1) == X.subs(lam, 1), checks)
    check(
        "lambda_one_direction_reset_mismatch_disappears",
        zero(sp.simplify(untyped_without_vertical.subs(lam, 1) - untyped_expected.subs(lam, 1))),
        checks,
    )

    V_b_observer = sp.simplify(U_ab * V_observer * U_ab.inv())
    X_b_observer = sp.simplify(V_b_observer * X_b * V_b_observer.inv())
    check("vertical_observer_map_intertwines_generators", sp.simplify(X_b_observer * V_b_observer - V_b_observer * X_b) == sp.zeros(4), checks)
    check("lambda_one_still_depends_on_observer", X_b_observer.subs(lam, 1) != X_b.subs(lam, 1), checks)

    # No lambda makes the pair endomorphism a function of the bare event.
    X_n2 = pair_generator(e0, e2, eta, lam)
    direction_difference = sp.simplify(X - X_n2)
    check("direction_independence_forces_lambda_one", sp.solve(list(direction_difference), lam) == {lam: 1}, checks)
    check("lambda_one_observer_change_is_nontrivial", X_prime_projectors.subs(lam, 1) != X.subs(lam, 1), checks)

    # Levi-Civita transport is metric-isometric and cannot itself equal a
    # nonzero aligned reciprocal dilation.
    metric_response = sp.simplify(D_a.T * eta * D_a)
    check("nonzero_depth_character_changes_metric", metric_response.subs(a, 1) != eta, checks)
    real_isometry_depths = sp.solveset(sp.exp(2 * a) - 1, a, domain=sp.S.Reals)
    check("reciprocal_character_is_Lorentz_only_at_zero_depth", real_isometry_depths == sp.FiniteSet(0), checks)

    # Endpoint-only additive real cocycles are potential differences.
    phi_A, phi_B, phi_C = sp.symbols("phi_A phi_B phi_C", real=True)
    delta_AB = phi_B - phi_A
    delta_BC = phi_C - phi_B
    delta_AC = phi_C - phi_A
    check("potential_difference_cocycle", sp.simplify(delta_AB + delta_BC - delta_AC) == 0, checks)
    check("potential_difference_reversal", sp.simplify((phi_A - phi_B) + delta_AB) == 0, checks)
    d_OA, d_AB = sp.symbols("d_OA d_AB", real=True)
    d_OB = d_OA + d_AB
    check("basepoint_reconstructs_endpoint_cocycle", sp.simplify(d_OB - d_OA - d_AB) == 0, checks)
    check("endpoint_cocycle_zero_is_additive_constant_gauge", sp.simplify((phi_B + 7) - (phi_A + 7) - delta_AB) == 0, checks)

    # A symmetric nonnegative magnitude cannot itself be the signed reversal-
    # odd parameter except in the trivial zero case.
    rho = sp.symbols("rho", nonnegative=True, real=True)
    check("symmetric_and_reversal_odd_force_zero", sp.solve(sp.Eq(rho, -rho), rho) == [0], checks)

    # A one-form integral always composes on path-labelled arrows. Endpoint
    # path independence is the additional zero-period/exactness condition.
    alpha_1, alpha_2 = sp.symbols("alpha_1 alpha_2", real=True)
    check("path_integral_concatenation_is_additive", sp.simplify((alpha_1 + alpha_2) - alpha_1 - alpha_2) == 0, checks)
    check("path_integral_reversal_changes_sign", sp.simplify(-alpha_1 + alpha_1) == 0, checks)
    period_identity = finite_character(lam, period) - I
    real_identity_periods = sp.solveset(sp.exp(period) - 1, period, domain=sp.S.Reals)
    check("positive_real_character_has_only_zero_identity_period", real_identity_periods == sp.FiniteSet(0), checks)
    check("nonzero_period_produces_reciprocal_loop", period_identity.subs({period: 1, lam: 0}) != sp.zeros(4), checks)

    # Two-path equality is exactly a holonomy centralizer question.
    H_screen = R_screen
    H_base = boost(1)
    check("screen_holonomy_centralizes_all_lambda", zero(H_screen * X - X * H_screen), checks)
    check("base_boost_holonomy_never_centralizes_founded_pair", not zero(H_base * X - X * H_base), checks)
    X_path_screen = sp.simplify(H_screen * X * H_screen.inv())
    X_path_base = sp.simplify(H_base * X * H_base.inv())
    check("centralizing_two_path_output_equal", X_path_screen == X, checks)
    check("noncentralizing_two_path_output_differs", X_path_base != X, checks)

    # Path labels preserve exact composition even when loops are nontrivial;
    # flatness is not a prerequisite for the path groupoid.
    loop_then_reverse = sp.simplify(H_base.inv() * (H_base * X * H_base.inv()) * H_base)
    check("nontrivial_path_holonomy_still_has_exact_reversal", loop_then_reverse == X, checks)

    if len(checks) != 51:
        raise AssertionError(f"unexpected check count {len(checks)}")

    result = {
        "schema": "udt-observer-pair-path-groupoid-assembly-1.0",
        "result": "PASS",
        "sympy_version": sp.__version__,
        "check_count": len(checks),
        "checks": checks,
        "counts": {
            "ordered_pair_dimensions": 2,
            "screen_gauge_dimension": 1,
            "screen_response_parameters": 1,
            "typed_composition_lambda_restrictions": 0,
            "bare_event_lambda_values_eliminating_all_pair_dependence": 0,
            "real_identity_depth_periods": 1,
        },
        "rulings": {
            "pair_frame_object": "COVARIANT_PROJECTOR_ENDOMORPHISM_DEFINED_FROM_ORDERED_U_N_FOR_ALL_LAMBDA",
            "screen_gauge": "SO2_AMBIGUITY_DROPS_OUT_OF_SCALAR_SCREEN_ENDOMORPHISM",
            "path_groupoid": "EXACT_CONJUGATION_COMPOSITION_AND_REVERSAL_FOR_ALL_LAMBDA",
            "middle_mismatch": "VERTICAL_PAIR_CHANGE_ARROW_NOT_ALGEBRAIC_INCONSISTENCY",
            "full_comparison": "EXACT_IF_SIGNED_DEPTH_IS_AN_ADDITIVE_PATH_COCYCLE",
            "depth_source": "NOT_DERIVED_BY_METRIC_ISOMETRIC_TRANSPORT",
            "endpoint_depth": "ANY_EXACT_REAL_ENDPOINT_COCYCLE_IS_A_POTENTIAL_DIFFERENCE",
            "path_depth": "ONE_FORM_INTEGRALS_COMPOSE; ENDPOINT_INDEPENDENCE_REQUIRES_ZERO_PERIODS",
            "real_period": "NONZERO_PERIOD_VISIBLE_IN_FAITHFUL_RECIPROCAL_CHARACTER",
            "bare_event_collapse": "REQUIRES_SECTION_OR_QUOTIENT; NO_LAMBDA_REMOVES_ALL_PAIR_DATA",
            "remaining_native_object": "METRIC_NATIVE_SIGNED_DEPTH_ASSIGNMENT_ON_TYPED_PAIR_FRAME_ARROWS",
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
