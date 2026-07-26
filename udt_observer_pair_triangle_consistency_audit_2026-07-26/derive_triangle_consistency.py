#!/usr/bin/env python3
"""Exact algebra for the observer-pair triangle-consistency audit."""

from __future__ import annotations

import json
import sympy as sp


def check(name: str, condition: bool, checks: dict[str, str]) -> None:
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def comm(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.simplify(left * right - right * left)


def unit(index: int) -> sp.Matrix:
    value = sp.zeros(4)
    value[index, index] = 1
    return value


def finite_directional(
    q: sp.Expr, screen_weight: sp.Expr, direction: sp.Matrix,
    P0: sp.Matrix, Pspace: sp.Matrix,
) -> sp.Matrix:
    """Finite exp(delta X_lambda(n)), with q=exp(delta)."""
    return sp.simplify(q ** -1 * P0 + screen_weight * Pspace + (q - screen_weight) * direction)


def clock_democratic(q: sp.Expr, projector: sp.Matrix, identity: sp.Matrix) -> sp.Matrix:
    return sp.simplify(q ** -1 * projector + q * (identity - projector))


def main() -> None:
    checks: dict[str, str] = {}
    I = sp.eye(4)
    eta = sp.diag(-1, 1, 1, 1)
    P0, P1, P2, P3 = (unit(i) for i in range(4))
    Pspace = I - P0

    # R01: founded abstract reciprocal character is a scalar cocycle.
    a, b = sp.symbols("a b", real=True)
    D2 = lambda value: sp.diag(sp.exp(-value), sp.exp(value))
    check("abstract_pair_additive_cocycle", sp.simplify(D2(b) * D2(a) - D2(a + b)) == sp.zeros(2), checks)
    check("abstract_pair_reversal", sp.simplify(D2(-a) - D2(a).inv()) == sp.zeros(2), checks)

    # R02: common fixed-observer frame, arbitrary spatial directions.
    q, r, s, t = sp.symbols("q r s t", positive=True)
    Pn = P1
    m = sp.Matrix([0, sp.Rational(3, 5), sp.Rational(4, 5), 0])
    Pm = sp.simplify(m * m.T)
    A = finite_directional(q, s, Pn, P0, Pspace)
    B = finite_directional(r, t, Pm, P0, Pspace)
    expected = (q - s) * (r - t) * comm(Pn, Pm)
    check("finite_direction_commutator_factorization", sp.simplify(comm(A, B) - expected) == sp.zeros(4), checks)
    check("generic_direction_projectors_do_not_commute", comm(Pn, Pm) != sp.zeros(4), checks)

    # Every preregistered zero factor is explicit.
    check("lambda_one_first_factor_zero", comm(A.subs(s, q), B) == sp.zeros(4), checks)
    check("lambda_one_second_factor_zero", comm(A, B.subs(t, r)) == sp.zeros(4), checks)
    check("first_zero_depth_factor_zero", comm(A.subs({q: 1, s: 1}), B) == sp.zeros(4), checks)
    check("second_zero_depth_factor_zero", comm(A, B.subs({r: 1, t: 1})) == sp.zeros(4), checks)
    check("parallel_direction_factor_zero", comm(Pn, Pn) == sp.zeros(4), checks)
    check("orthogonal_direction_factor_zero", comm(P1, P2) == sp.zeros(4), checks)

    # Explicit finite group loop. Noncommuting invertible maps give a
    # nonidentity group commutator; it is an obstruction only on R02.
    A0 = finite_directional(sp.Rational(2), sp.Rational(1), Pn, P0, Pspace)
    B0 = finite_directional(sp.Rational(3), sp.Rational(1), Pm, P0, Pspace)
    loop0 = sp.simplify(A0 * B0 * A0.inv() * B0.inv())
    check("generic_lambda_zero_group_loop_nonidentity", loop0 != I, checks)
    A1 = finite_directional(sp.Rational(2), sp.Rational(2), Pn, P0, Pspace)
    B1 = finite_directional(sp.Rational(3), sp.Rational(3), Pm, P0, Pspace)
    check("lambda_one_group_loop_identity", sp.simplify(A1 * B1 * A1.inv() * B1.inv()) == I, checks)
    Aminus = finite_directional(sp.Rational(2), sp.Rational(1, 2), Pn, P0, Pspace)
    Bminus = finite_directional(sp.Rational(3), sp.Rational(1, 3), Pm, P0, Pspace)
    check("lambda_minus_one_group_loop_nonidentity", sp.simplify(Aminus * Bminus * Aminus.inv() * Bminus.inv()) != I, checks)
    Ahalf = finite_directional(sp.Rational(4), sp.Rational(1, 2), Pn, P0, Pspace)
    Bhalf = finite_directional(sp.Rational(9), sp.Rational(1, 3), Pm, P0, Pspace)
    check("lambda_minus_half_group_loop_nonidentity", sp.simplify(Ahalf * Bhalf * Ahalf.inv() * Bhalf.inv()) != I, checks)

    # Universal q^lambda=q for all positive q fixes lambda=1 in the real
    # exponential family. One nontrivial positive q already does so.
    lam = sp.symbols("lam", real=True)
    lambda_solutions = sp.solve(sp.Eq(sp.Pow(2, lam), 2), lam)
    check("real_exponential_factor_selects_lambda_one", lambda_solutions == [1], checks)

    # R03: properly typed endpoint factorization. The frames can differ;
    # one frame per endpoint is what makes the middle type cancel.
    phi_a, phi_b, phi_c = sp.symbols("phi_a phi_b phi_c", real=True)

    def D4(delta: sp.Expr) -> sp.Matrix:
        return sp.diag(
            sp.exp(-delta), sp.exp(delta),
            sp.exp(lam * delta), sp.exp(lam * delta),
        )

    FA = I
    FB = sp.eye(4)
    FB[0, 0] = FB[1, 1] = sp.Rational(5, 4)
    FB[0, 1] = FB[1, 0] = sp.Rational(3, 4)
    FC = sp.eye(4)
    FC[0, 0] = FC[2, 2] = sp.Rational(5, 4)
    FC[0, 2] = FC[2, 0] = sp.Rational(3, 4)
    check("endpoint_frame_B_is_Lorentz", FB.T * eta * FB == eta, checks)
    check("endpoint_frame_C_is_Lorentz", FC.T * eta * FC == eta, checks)

    TAB = sp.simplify(FB * D4(phi_b - phi_a) * FA.inv())
    TBC = sp.simplify(FC * D4(phi_c - phi_b) * FB.inv())
    TAC = sp.simplify(FC * D4(phi_c - phi_a) * FA.inv())
    check("typed_endpoint_triangle_all_lambda", sp.simplify(TBC * TAB - TAC) == sp.zeros(4), checks)
    check("typed_endpoint_reversal_all_lambda", sp.simplify(TAB.inv() - FA * D4(phi_a - phi_b) * FB.inv()) == sp.zeros(4), checks)
    loop_typed = sp.simplify((FA * D4(phi_a - phi_c) * FC.inv()) * TBC * TAB)
    check("typed_endpoint_closed_loop_identity", loop_typed == I, checks)

    # R04: pair-dependent frames. Unlike endpoint frames do not cancel.
    R = sp.eye(4)
    R[1, 1] = 0
    R[1, 2] = -1
    R[2, 1] = 1
    R[2, 2] = 0
    check("middle_spatial_transition_is_Lorentz", R.T * eta * R == eta, checks)
    F_B_given_A = I
    F_B_given_C = R
    middle_mismatch = sp.simplify(F_B_given_C.inv() * F_B_given_A)
    check("pair_dependent_middle_mismatch_nonidentity", middle_mismatch != I, checks)
    D_lambda0 = sp.diag(sp.Rational(1, 2), 2, 1, 1)
    D_lambda1 = sp.diag(sp.Rational(1, 2), 2, 2, 2)
    check("lambda_zero_sensitive_to_spatial_direction_frame", comm(D_lambda0, middle_mismatch) != sp.zeros(4), checks)
    check("lambda_one_dilation_commutes_with_spatial_frame_mismatch", comm(D_lambda1, middle_mismatch) == sp.zeros(4), checks)
    check("lambda_one_does_not_delete_middle_transition", middle_mismatch != I, checks)

    # R06: lambda=1 removes n-dependence only for fixed u. A different
    # timelike observer projector generically does not commute.
    u = sp.Matrix([1, 0, 0, 0])
    v = sp.Matrix([sp.Rational(5, 4), sp.Rational(3, 4), 0, 0])
    Pu = sp.simplify(-u * (u.T * eta))
    Pv = sp.simplify(-v * (v.T * eta))
    check("u_timelike_unit", (u.T * eta * u)[0] == -1, checks)
    check("v_timelike_unit", (v.T * eta * v)[0] == -1, checks)
    check("timelike_projectors_idempotent", Pu**2 == Pu and Pv**2 == Pv, checks)
    Eu = clock_democratic(q, Pu, I)
    Ev = clock_democratic(r, Pv, I)
    observer_expected = (q ** -1 - q) * (r ** -1 - r) * comm(Pu, Pv)
    check("changing_observer_commutator_factorization", sp.simplify(comm(Eu, Ev) - observer_expected) == sp.zeros(4), checks)
    check("noncollinear_observer_projectors_do_not_commute", comm(Pu, Pv) != sp.zeros(4), checks)
    check("changing_observer_lambda_one_maps_noncommute", comm(Eu.subs(q, 2), Ev.subs(r, 3)) != sp.zeros(4), checks)
    check("same_observer_lambda_one_maps_commute", comm(Eu.subs(q, 2), clock_democratic(3, Pu, I)) == sp.zeros(4), checks)

    result = {
        "schema": "udt-observer-pair-triangle-consistency-1.0",
        "result": "PASS",
        "sympy_version": sp.__version__,
        "check_count": len(checks),
        "checks": checks,
        "exact_data": {
            "common_frame_commutator": "(q-q^lambda)(r-r^lambda)[P_n,P_m]",
            "fixed_observer_universal_flat_selection": "lambda=1",
            "endpoint_groupoid_selection": "none; exact for every lambda",
            "pair_frame_middle_mismatch": "F_(B|C)^-1 F_(B|A)",
            "changing_observer_commutator": "(q^-1-q)(r^-1-r)[P_u,P_v]",
        },
        "rulings": {
            "R01": "DERIVED_ABSTRACT_ADDITIVE_PAIR_COCYCLE",
            "R02": "LAMBDA_ONE_UNIQUE_CONDITIONAL_UNDER_UNIVERSAL_COMMON_FRAME_FLAT_PATH_INDEPENDENCE",
            "R03": "TYPED_ENDPOINT_FACTORIZATION_COMPOSES_FOR_ALL_LAMBDA_AND_DOES_NOT_SELECT",
            "R04": "PAIR_DEPENDENT_FRAMES_REQUIRE_EXPLICIT_MIDDLE_TRANSITION_OR_CONNECTION",
            "R05": "NONIDENTITY_LOOP_MAY_BE_HOLONOMY; LOCAL_ALGEBRA_ALONE_CANNOT_REJECT",
            "R06": "LAMBDA_ONE_SOLVES_FIXED_OBSERVER_DIRECTION_DEPENDENCE_NOT_CHANGING_OBSERVER_COMPOSITION",
            "R07": "GLOBAL_DESCENT_NOT_DERIVED_BY_LOCAL_TRIANGLE_ALGEBRA",
            "R08": "SCALAR_ANCHORS_SUPPLY_NO_FRAME_SECTION_OR_CONNECTION",
            "overall": "TRIANGLE_CONSISTENCY_DOES_NOT_UNCONDITIONALLY_SELECT_LAMBDA",
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
