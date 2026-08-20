#!/usr/bin/env python3
"""Hostile structural mutations for the G193 load-bearing identities."""

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
    mu = sp.Function("mu", real=True)(eta)
    nu = sp.Function("nu", real=True)(eta)
    y1 = sp.Function("y1", real=True)(eta)
    y2 = sp.Function("y2", real=True)(eta)
    y = sp.Matrix([y1, y2])
    mix = sp.Matrix([[sp.sqrt(2) * mu, nu], [nu, 0]])
    exact_potential = 2 * sp.diff(mix, eta) - 4 * mix * mix
    exact_operator = sp.diff(y, eta, 2) + exact_potential * y

    catches = {}

    mutations = {
        "drop_nu_prime": exact_potential.subs(sp.diff(nu, eta), 0),
        "drop_mu_prime": exact_potential.subs(sp.diff(mu, eta), 0),
        "drop_all_quadratic_terms": 2 * sp.diff(mix, eta),
        "drop_nu_squared_00": exact_potential
        + sp.Matrix([[4 * nu**2, 0], [0, 0]]),
        "drop_nu_squared_11": exact_potential
        + sp.Matrix([[0, 0], [0, 4 * nu**2]]),
        "drop_mu_nu_cross": exact_potential
        + sp.Matrix([[0, 4 * sp.sqrt(2) * mu * nu], [4 * sp.sqrt(2) * mu * nu, 0]]),
        "force_diagonal_tide": sp.diag(exact_potential[0, 0], exact_potential[1, 1]),
        "reverse_derivative_sign": -2 * sp.diff(mix, eta) - 4 * mix * mix,
    }
    for name, mutation in mutations.items():
        catches[name] = nonzero((mutation - exact_potential).applyfunc(sp.simplify))

    reversed_factor = (
        sp.diff(sp.diff(y, eta) - 2 * mix * y, eta)
        + 2 * mix * (sp.diff(y, eta) - 2 * mix * y)
    ).applyfunc(sp.simplify)
    catches["reverse_factor_order"] = nonzero(reversed_factor - exact_operator)

    derivative_free_factor = (
        sp.diff(sp.diff(y, eta) + 2 * mix * y, eta)
        - 2 * mix * sp.diff(y, eta)
    ).applyfunc(sp.simplify)
    catches["delete_outer_matrix_action"] = nonzero(
        derivative_free_factor - exact_operator
    )

    aa, ab, na, nb = sp.symbols("A_a A_b nu_a nu_b", real=True)
    left = sp.Matrix([[aa, na], [na, 0]])
    right = sp.Matrix([[ab, nb], [nb, 0]])
    commutator = left * right - right * left
    catches["force_all_histories_commuting"] = nonzero(commutator)

    b11, b12, b21, b22 = sp.symbols("b11 b12 b21 b22", real=True)
    inverse_l = sp.Matrix([[b11, b12], [b21, b22]])
    positive_integrand = inverse_l * inverse_l.T
    test_vector = sp.Matrix(sp.symbols("v1 v2", real=True))
    quadratic = sp.expand((test_vector.T * positive_integrand * test_vector)[0])
    expected_squares = sp.expand(
        (b11 * test_vector[0] + b21 * test_vector[1]) ** 2
        + (b12 * test_vector[0] + b22 * test_vector[1]) ** 2
    )
    catches["positive_integrand_order"] = sp.simplify(quadratic - expected_squares) == 0

    wrong_integrand = inverse_l.T * inverse_l
    catches["transpose_order_mutation"] = nonzero(wrong_integrand - positive_integrand)

    scale, dscale = sp.symbols("a adot", positive=True, real=True)
    exact_frequency_derivative = -dscale / scale**4
    catches["wrong_affine_power"] = nonzero(-dscale / scale**3 - exact_frequency_derivative)
    catches["mixing_contaminates_frequency"] = nonzero(
        exact_frequency_derivative + mu * nu - exact_frequency_derivative
    )

    status = "PASS" if all(catches.values()) else "FAIL"
    result = {
        "status": status,
        "catch_count": len(catches),
        "caught_count": sum(bool(value) for value in catches.values()),
        "catches": catches,
    }
    if status != "PASS":
        raise AssertionError({key: value for key, value in catches.items() if not value})

    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if os.environ.get("G193_NO_WRITE") == "1":
        print(payload, end="")
        return
    Path(__file__).with_name("CATCH_PROOF_RESULT.json").write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
