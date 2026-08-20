#!/usr/bin/env python3
"""Hostile structural mutations for the G194 load-bearing identities."""

from __future__ import annotations

import json
import os
from pathlib import Path

import sympy as sp


def nonzero(expression):
    if isinstance(expression, sp.MatrixBase):
        return any(sp.simplify(entry) != 0 for entry in expression)
    return sp.simplify(expression) != 0


def main():
    eta = sp.symbols("eta", real=True)
    entry_a = sp.Function("A", real=True)(eta)
    entry_n = sp.Function("N", real=True)(eta)
    entry_b = sp.Function("B", real=True)(eta)
    y1 = sp.Function("y1", real=True)(eta)
    y2 = sp.Function("y2", real=True)(eta)
    y = sp.Matrix([y1, y2])
    mix = sp.Matrix([[entry_a, entry_n], [entry_n, entry_b]])
    exact_potential = 2 * sp.diff(mix, eta) - 4 * mix * mix
    exact_operator = sp.diff(y, eta, 2) + exact_potential * y

    catches = {}
    mutations = {
        "drop_A_prime": exact_potential.subs(sp.diff(entry_a, eta), 0),
        "drop_N_prime": exact_potential.subs(sp.diff(entry_n, eta), 0),
        "drop_B_prime": exact_potential.subs(sp.diff(entry_b, eta), 0),
        "drop_all_quadratic_terms": 2 * sp.diff(mix, eta),
        "drop_A_squared": exact_potential + sp.Matrix([[4 * entry_a**2, 0], [0, 0]]),
        "drop_B_squared": exact_potential + sp.Matrix([[0, 0], [0, 4 * entry_b**2]]),
        "drop_N_squared_00": exact_potential + sp.Matrix([[4 * entry_n**2, 0], [0, 0]]),
        "drop_N_squared_11": exact_potential + sp.Matrix([[0, 0], [0, 4 * entry_n**2]]),
        "drop_N_A_plus_B_cross": exact_potential
        + sp.Matrix(
            [
                [0, 4 * entry_n * (entry_a + entry_b)],
                [4 * entry_n * (entry_a + entry_b), 0],
            ]
        ),
        "force_B_zero": exact_potential.subs(
            {entry_b: 0, sp.diff(entry_b, eta): 0}
        ),
        "force_trace_free": exact_potential.subs(
            {entry_b: -entry_a, sp.diff(entry_b, eta): -sp.diff(entry_a, eta)}
        ),
        "force_scalar_matrix": exact_potential.subs(
            {
                entry_b: entry_a,
                sp.diff(entry_b, eta): sp.diff(entry_a, eta),
                entry_n: 0,
                sp.diff(entry_n, eta): 0,
            }
        ),
        "reverse_derivative_sign": -2 * sp.diff(mix, eta) - 4 * mix * mix,
    }
    for name, mutation in mutations.items():
        catches[name] = nonzero((mutation - exact_potential).applyfunc(sp.simplify))

    reversed_factor = (
        sp.diff(sp.diff(y, eta) - 2 * mix * y, eta)
        + 2 * mix * (sp.diff(y, eta) - 2 * mix * y)
    ).applyfunc(sp.simplify)
    catches["reverse_factor_order"] = nonzero(reversed_factor - exact_operator)

    deleted_outer_action = (
        sp.diff(sp.diff(y, eta) + 2 * mix * y, eta)
        - 2 * mix * sp.diff(y, eta)
    ).applyfunc(sp.simplify)
    catches["delete_outer_matrix_action"] = nonzero(deleted_outer_action - exact_operator)

    a1, n1, b1, a2, n2, b2 = sp.symbols("A1 N1 B1 A2 N2 B2", real=True)
    left = sp.Matrix([[a1, n1], [n1, b1]])
    right = sp.Matrix([[a2, n2], [n2, b2]])
    commutator = left * right - right * left
    catches["force_ordered_history_commuting"] = nonzero(commutator)

    l11, l12, l21, l22 = sp.symbols("l11 l12 l21 l22", real=True)
    inverse_l = sp.Matrix([[l11, l12], [l21, l22]])
    positive_integrand = inverse_l * inverse_l.T
    wrong_transpose_order = inverse_l.T * inverse_l
    catches["transpose_order_in_gram"] = nonzero(wrong_transpose_order - positive_integrand)

    k11, k12, k21, k22 = sp.symbols("k11 k12 k21 k22", real=True)
    fundamental = sp.Matrix([[l11, l12], [l21, l22]])
    integral = sp.Matrix([[k11, k12], [k21, k22]])
    catches["drop_outer_L_action"] = nonzero(fundamental * integral - integral)

    v1, v2 = sp.symbols("v1 v2", real=True)
    vector = sp.Matrix([v1, v2])
    exact_quadratic = sp.expand((vector.T * positive_integrand * vector)[0])
    square_quadratic = sp.expand(
        (l11 * v1 + l21 * v2) ** 2 + (l12 * v1 + l22 * v2) ** 2
    )
    catches["positive_gram_square_identity"] = sp.simplify(
        exact_quadratic - square_quadratic
    ) == 0

    indefinite_integrand = inverse_l * sp.diag(1, -1) * inverse_l.T
    negative_witness = sp.simplify(
        (sp.Matrix([0, 1]).T * indefinite_integrand * sp.Matrix([0, 1]))[0].subs(
            {l11: 1, l12: 0, l21: 0, l22: 1}
        )
    )
    catches["indefinite_gram_mutation"] = negative_witness < 0

    scale, dscale = sp.symbols("a adot", positive=True, real=True)
    exact_frequency_derivative = -dscale / scale**4
    catches["wrong_affine_power"] = nonzero(
        -dscale / scale**3 - exact_frequency_derivative
    )
    catches["mixing_contaminates_frequency"] = nonzero(
        exact_frequency_derivative + entry_a * entry_b - exact_frequency_derivative
    )

    status = "PASS" if all(catches.values()) else "FAIL"
    serialized_catches = {key: bool(value) for key, value in catches.items()}
    result = {
        "status": status,
        "catch_count": len(catches),
        "caught_count": sum(bool(value) for value in catches.values()),
        "catches": serialized_catches,
    }
    if status != "PASS":
        raise AssertionError({key: value for key, value in catches.items() if not value})

    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if os.environ.get("G194_NO_WRITE") == "1":
        print(payload, end="")
        return
    Path(__file__).with_name("CATCH_PROOF_RESULT.json").write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
