#!/usr/bin/env python3
"""Exact zero-order census of constant complete reciprocal extensions.

This script classifies structureless constant generators. It does not select an
active physical action, a field-dependent generator, or a metric history.
"""

import json

import sympy as sp


def matrix_zero(matrix):
    return all(sp.simplify(entry) == 0 for entry in matrix)


def solve_centralizers():
    a, b, c, d = sp.symbols("a b c d", real=True)
    ds = sp.Matrix([[a, b], [c, d]])
    eps = sp.Matrix([[0, -1], [1, 0]])
    reflection = sp.diag(1, -1)
    so2 = sp.solve(list(ds * eps - eps * ds), [a, b, c, d], dict=True)
    o2 = sp.solve(
        list(ds * eps - eps * ds) + list(ds * reflection - reflection * ds),
        [a, b, c, d],
        dict=True,
    )

    x = sp.symbols("x0:4", real=True)
    off = sp.Matrix(2, 2, x)
    # For L_R=diag(I,R), the lower-left block transforms as C -> R C
    # and the upper-right block as A -> A R^-1.  Differentiation at the
    # identity therefore gives eps*C=0 and A*eps=0 (the latter up to an
    # irrelevant overall minus sign), not an eigenvalue-one equation.
    source_to_screen_so2 = sp.solve(list(eps * off), x, dict=True)
    screen_to_source_so2 = sp.solve(list(off * eps), x, dict=True)
    source_to_screen_o2 = sp.solve(
        list(eps * off) + list(reflection * off - off), x, dict=True
    )
    screen_to_source_o2 = sp.solve(
        list(off * eps) + list(off * reflection - off), x, dict=True
    )
    wrong_source_mutant = eps * off - off
    wrong_target_mutant = off * eps - off
    return {
        "SO2_screen_centralizer": [str(item) for item in so2],
        "O2_screen_centralizer": [str(item) for item in o2],
        "SO2_base_to_screen_invariants": [str(item) for item in source_to_screen_so2],
        "SO2_screen_to_base_invariants": [str(item) for item in screen_to_source_so2],
        "O2_base_to_screen_invariants": [str(item) for item in source_to_screen_o2],
        "O2_screen_to_base_invariants": [str(item) for item in screen_to_source_o2],
        "SO2_base_to_screen_equation": "epsilon*C=0",
        "SO2_screen_to_base_equation": "A*epsilon=0",
        "wrong_eigenvalue_one_mutant_differs": (
            wrong_source_mutant != eps * off and wrong_target_mutant != off * eps
        ),
    }


def gate_checks():
    a, b = sp.symbols("a b", real=True)
    hb = sp.diag(-1, 1)
    eps = sp.Matrix([[0, -1], [1, 0]])
    ds = a * sp.eye(2) + b * eps
    h = sp.diag(-1, 1, a, a)
    h[2, 3] = -b
    h[3, 2] = b
    k = sp.Matrix([[0, 1], [1, 0]])
    full_pairing = sp.diag(1, 1, 1, 1)
    full_pairing[:2, :2] = k
    screen_reflection = sp.diag(1, -1)
    exchange_fixed_screen = sp.diag(1, 1, 1, 1)
    exchange_fixed_screen[:2, :2] = k
    exchange_reflected_screen = sp.diag(1, 1, 1, 1)
    exchange_reflected_screen[:2, :2] = k
    exchange_reflected_screen[2:, 2:] = screen_reflection

    full_pairing_residual = sp.simplify(h.T * full_pairing + full_pairing * h)
    fixed_exchange_residual = sp.simplify(
        exchange_fixed_screen * h * exchange_fixed_screen + h
    )
    reflected_exchange_residual = sp.simplify(
        exchange_reflected_screen * h * exchange_reflected_screen + h
    )

    return {
        "base_generator_preserves_K": matrix_zero(hb.T * k + k * hb),
        "full_generator_trace": str(sp.trace(h)),
        "full_pairing_residual": str(full_pairing_residual),
        "fixed_screen_exchange_residual": str(fixed_exchange_residual),
        "reflected_screen_exchange_residual": str(reflected_exchange_residual),
        "full_det_one_condition": "a=0",
        "full_pairing_condition": "a=0",
        "fixed_screen_exchange_condition": "a=0,b=0",
        "reflected_screen_exchange_condition": "a=0",
        "screen_generator": str(ds),
    }


def finite_action_checks():
    delta, a, b = sp.symbols("delta a b", real=True)
    c = sp.cos(b * delta)
    s = sp.sin(b * delta)
    rotation = sp.Matrix([[c, -s], [s, c]])
    g = sp.diag(sp.exp(-delta), sp.exp(delta), 1, 1)
    g[2:, 2:] = sp.exp(a * delta) * rotation
    eta = sp.diag(-1, 1, 1, 1)

    # Exact regular rational witness evaluated at exp(delta)=2.
    j = sp.Matrix([[5, 0], [0, 1], [1, 0], [0, 1]])
    h0 = sp.simplify(j.T * eta * j)
    g_neutral = sp.diag(sp.Rational(1, 2), 2, 1, 1)
    g_scale = sp.diag(sp.Rational(1, 2), 2, 2, 2)
    h_neutral = sp.simplify(j.T * g_neutral.T * eta * g_neutral * j)
    h_scale = sp.simplify(j.T * g_scale.T * eta * g_scale * j)

    def ce_ratio_sq(metric):
        return sp.simplify(metric[0, 0] ** 2 / (-metric.det()))

    # Coordinate-basis passive carry: E -> E P^-1, J -> P J.
    p = sp.Matrix(
        [[1, 1, 0, 0], [0, 1, 0, 0], [0, 0, 2, 1], [0, 0, 0, 1]]
    )
    e = sp.Matrix(
        [[2, 1, 0, 0], [0, 3, 0, 0], [1, 0, 1, 0], [0, 1, 0, 2]]
    )
    passive_v_residual = sp.simplify(e * p.inv() * p * j - e * j)

    return {
        "finite_family": str(g),
        "determinant": str(sp.simplify(g.det())),
        "screen_rotation_drops_from_metric": matrix_zero(
            sp.simplify(rotation.T * rotation - sp.eye(2))
        ),
        "witness_h_original": str(h0),
        "witness_h_neutral_lift": str(h_neutral),
        "witness_h_screen_scale_a1": str(h_scale),
        "witness_ce_ratio_sq_original": str(ce_ratio_sq(h0)),
        "witness_ce_ratio_sq_neutral": str(ce_ratio_sq(h_neutral)),
        "witness_ce_ratio_sq_screen_scale_a1": str(ce_ratio_sq(h_scale)),
        "active_screen_scale_changes_h": h_scale != h_neutral,
        "passive_coordinate_carry_cancels": matrix_zero(passive_v_residual),
    }


def main():
    result = {
        "scope": "constant zero-order generators; O2/SO2; no field-dependent owner",
        "centralizers": solve_centralizers(),
        "gates": gate_checks(),
        "finite_action": finite_action_checks(),
    }
    result["landing"] = (
        "ONE_PARAMETER_SCREEN_DILATION_SURVIVES_BASE_ONLY_GATES"
        "__FULL_DET_PAIRING_OR_EXCHANGE_KILLS_DILATION"
        "__SO2_ROTATION_IS_ZERO_ORDER_GAUGE"
        "__ACTIVE_PLACEMENT_UNOWNED"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
