#!/usr/bin/env python3
"""Hostile structural mutations for the G195 load-bearing identities."""

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
    rotation_r = sp.Function("R", real=True)(eta)
    y = sp.Matrix(
        [sp.Function("y1", real=True)(eta), sp.Function("y2", real=True)(eta)]
    )

    strain = sp.Matrix([[entry_a, entry_n], [entry_n, entry_b]])
    generator = sp.Matrix([[0, 1], [-1, 0]])
    omega = rotation_r * generator
    mix = strain + omega
    commutator = strain * omega - omega * strain
    exact_connection = 2 * omega
    exact_tide = 2 * sp.diff(strain, eta) - 4 * strain * strain - 4 * commutator

    inner = sp.diff(y, eta) + 2 * mix * y
    exact_factor = (sp.diff(inner, eta) - 2 * mix.T * inner).applyfunc(sp.simplify)
    exact_expanded = (
        sp.diff(y, eta, 2)
        + 2 * (mix - mix.T) * sp.diff(y, eta)
        + (2 * sp.diff(mix, eta) - 4 * mix.T * mix) * y
    ).applyfunc(sp.simplify)
    covariant_first = sp.diff(y, eta) + 2 * omega * y
    exact_covariant = (
        sp.diff(covariant_first, eta)
        + 2 * omega * covariant_first
        + exact_tide * y
    ).applyfunc(sp.simplify)

    catches = {
        "factorization_identity": not nonzero(exact_factor - exact_expanded),
        "covariant_factorization_identity": not nonzero(
            exact_factor - exact_covariant
        ),
        "force_R_zero": nonzero(exact_connection),
        "reverse_screen_connection_sign": nonzero(-exact_connection - exact_connection),
        "declare_coordinate_screen_parallel": nonzero(exact_connection),
        "omit_parallel_screen_rotation": nonzero(
            exact_tide - (2 * sp.diff(strain, eta) - 4 * strain * strain)
        ),
    }

    symmetrized_inner = sp.diff(y, eta) + 2 * strain * y
    symmetrized_factor = (
        sp.diff(symmetrized_inner, eta) - 2 * strain * symmetrized_inner
    ).applyfunc(sp.simplify)
    catches["symmetrize_M_before_reconstruction"] = nonzero(
        symmetrized_factor - exact_factor
    )

    reversed_inner = sp.diff(y, eta) - 2 * mix.T * y
    reversed_factor = (
        sp.diff(reversed_inner, eta) + 2 * mix * reversed_inner
    ).applyfunc(sp.simplify)
    catches["reverse_factor_order"] = nonzero(reversed_factor - exact_factor)

    no_rotation_derivative = exact_expanded.subs(sp.diff(rotation_r, eta), 0)
    catches["delete_R_prime_from_coordinate_operator"] = nonzero(
        no_rotation_derivative - exact_expanded
    )

    exact_potential = 2 * sp.diff(mix, eta) - 4 * mix.T * mix
    no_rotation_square = exact_potential + 4 * rotation_r**2 * sp.eye(2)
    catches["drop_quadratic_R_contribution"] = nonzero(
        no_rotation_square - exact_potential
    )
    catches["drop_S_Omega_commutator"] = nonzero(
        (2 * sp.diff(strain, eta) - 4 * strain * strain) - exact_tide
    )

    skew_mutation = exact_tide + rotation_r * generator
    catches["non_self_adjoint_tide"] = nonzero(
        skew_mutation - skew_mutation.T
    )

    m11, m12, m21, m22 = sp.symbols("m11 m12 m21 m22", real=True)
    inv_t11, inv_t12, inv_t21, inv_t22 = sp.symbols(
        "q11 q12 q21 q22", real=True
    )
    generic_mix = sp.Matrix([[m11, m12], [m21, m22]])
    inverse_transpose = sp.Matrix([[inv_t11, inv_t12], [inv_t21, inv_t22]])
    exact_inverse_transpose_derivative = 2 * generic_mix.T * inverse_transpose
    symmetric_only_derivative = 2 * generic_mix * inverse_transpose
    catches["assume_M_symmetric_in_inverse_transpose"] = nonzero(
        symmetric_only_derivative - exact_inverse_transpose_derivative
    )

    a1, n1, b1, r1, a2, n2, b2, r2 = sp.symbols(
        "A1 N1 B1 R1 A2 N2 B2 R2", real=True
    )
    left = sp.Matrix([[a1, n1 + r1], [n1 - r1, b1]])
    right = sp.Matrix([[a2, n2 + r2], [n2 - r2, b2]])
    catches["replace_ordered_transport_by_commuting_exponential"] = nonzero(
        left * right - right * left
    )

    l11, l12, l21, l22 = sp.symbols("l11 l12 l21 l22", real=True)
    inverse_l = sp.Matrix([[l11, l12], [l21, l22]])
    exact_gram = inverse_l * inverse_l.T
    wrong_gram = inverse_l.T * inverse_l
    catches["transpose_order_in_gram"] = nonzero(wrong_gram - exact_gram)

    vector = sp.Matrix(sp.symbols("v1 v2", real=True))
    exact_quadratic = sp.expand((vector.T * exact_gram * vector)[0])
    square_quadratic = sp.expand(
        (l11 * vector[0] + l21 * vector[1]) ** 2
        + (l12 * vector[0] + l22 * vector[1]) ** 2
    )
    catches["positive_gram_square_identity"] = (
        sp.simplify(exact_quadratic - square_quadratic) == 0
    )

    scale, dscale = sp.symbols("scale dscale", positive=True, real=True)
    exact_frequency_derivative = -dscale / scale**4
    catches["wrong_affine_power"] = nonzero(
        -dscale / scale**3 - exact_frequency_derivative
    )

    sample_coordinate = sp.symbols("sample_coordinate", real=True)
    finite_sample_mutant = 1 - 100 * (
        (sample_coordinate + 1) * sample_coordinate * (sample_coordinate - 1)
    ) ** 2
    sample_values = [
        finite_sample_mutant.subs(sample_coordinate, value) for value in (-1, 0, 1)
    ]
    catches["finite_sampling_not_universal_caustic_proof"] = (
        all(value > 0 for value in sample_values)
        and finite_sample_mutant.subs(sample_coordinate, sp.Rational(1, 2)) < 0
    )

    status = "PASS" if all(catches.values()) else "FAIL"
    serialized = {key: bool(value) for key, value in catches.items()}
    result = {
        "status": status,
        "catch_count": len(serialized),
        "caught_count": sum(serialized.values()),
        "catches": serialized,
    }
    if status != "PASS":
        raise AssertionError({key: value for key, value in catches.items() if not value})

    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if os.environ.get("G195_NO_WRITE") == "1":
        print(payload, end="")
        return
    Path(__file__).with_name("CATCH_PROOF_RESULT.json").write_text(
        payload, encoding="utf-8"
    )
    print(payload, end="")


if __name__ == "__main__":
    main()
