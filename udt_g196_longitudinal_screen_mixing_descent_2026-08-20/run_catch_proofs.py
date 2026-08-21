#!/usr/bin/env python3
"""Exact hostile-mutation catches for G196."""

from __future__ import annotations

import json
import os
from pathlib import Path

import sympy as sp


def nonzero_matrix(matrix):
    return any(sp.simplify(entry) != 0 for entry in matrix)


def main():
    A, N, B, R = sp.symbols("A N B R", real=True)
    Ae, Ne, Be, Re = sp.symbols("Ae Ne Be Re", real=True)
    Az, Nz, Bz, Rz = sp.symbols("Az Nz Bz Rz", real=True)
    M = sp.Matrix([[A, N + R], [N - R, B]])
    S = sp.Matrix([[A, N], [N, B]])
    Omega = sp.Matrix([[0, R], [-R, 0]])
    DeM = sp.Matrix([[Ae, Ne + Re], [Ne - Re, Be]])
    DzM = sp.Matrix([[Az, Nz + Rz], [Nz - Rz, Bz]])
    DpM = DeM + DzM
    DmM = DeM - DzM

    first_correct = 2 * (M - M.T)
    zero_correct = 2 * DpM - 4 * M.T * M
    sample = {
        A: sp.Rational(2, 5), N: sp.Rational(-1, 7), B: sp.Rational(1, 3),
        R: sp.Rational(3, 11), Ae: sp.Rational(1, 13), Ne: sp.Rational(-2, 17),
        Be: sp.Rational(3, 19), Re: sp.Rational(1, 23), Az: sp.Rational(4, 29),
        Nz: sp.Rational(-3, 31), Bz: sp.Rational(2, 37), Rz: sp.Rational(-5, 41),
    }

    drop_z = 2 * DeM - 4 * M.T * M
    reverse_null = 2 * DmM - 4 * M.T * M
    symmetric_first = sp.zeros(2)
    symmetric_zero = 2 * (DeM + DzM).applyfunc(
        lambda entry: entry.subs({Re: 0, Rz: 0})
    ) - 4 * S.T * S
    reverse_order_zero = -2 * DpM.T - 4 * M * M.T

    M0 = sp.Matrix([[1, 1], [0, 0]])
    M1 = sp.Matrix([[0, 0], [1, 1]])
    commuting_error = M0 * M1 - M1 * M0

    connection_correct = 2 * Omega
    connection_wrong = -2 * Omega

    s = sp.symbols("s", real=True)
    fake_positive = (s - sp.Rational(1, 8)) ** 2
    sample_points = [sp.Rational(0), sp.Rational(1, 4), sp.Rational(1, 2),
                     sp.Rational(3, 4), sp.Rational(1)]
    finite_samples_positive = all(fake_positive.subs(s, point) > 0 for point in sample_points)
    hidden_zero = sp.simplify(fake_positive.subs(s, sp.Rational(1, 8))) == 0

    eta, z = sp.symbols("eta z", real=True)
    alias_difference = sp.Rational(7, 10) * (eta - z) ** 2
    dplus_alias = sp.diff(alias_difference, eta) + sp.diff(alias_difference, z)
    alias_on_ray = sp.simplify(alias_difference.subs(z, eta)) == 0
    alias_dplus_on_ray = sp.simplify(dplus_alias.subs(z, eta)) == 0
    alias_off_ray = sp.simplify(
        alias_difference.subs({eta: sp.Rational(31, 100), z: sp.Rational(7, 100)})
    )

    pure_rotation_correct = sp.zeros(2)
    pure_rotation_mutant = -4 * Omega.T * Omega

    catches = {
        "drop_partial_z": nonzero_matrix((zero_correct - drop_z).subs(sample)),
        "reverse_null_derivative": nonzero_matrix((zero_correct - reverse_null).subs(sample)),
        "force_symmetric_mixing": (
            nonzero_matrix((first_correct - symmetric_first).subs(sample))
            and nonzero_matrix((zero_correct - symmetric_zero).subs(sample))
        ),
        "reverse_factor_order": nonzero_matrix((zero_correct - reverse_order_zero).subs(sample)),
        "commuting_exponential": nonzero_matrix(commuting_error),
        "wrong_connection_sign": nonzero_matrix((connection_correct - connection_wrong).subs(sample)),
        "sampled_positivity_as_proof": finite_samples_positive and hidden_zero,
        "one_ray_equality_as_global": alias_on_ray and alias_dplus_on_ray and alias_off_ray != 0,
        "rotation_as_independent_focusing": nonzero_matrix(
            (pure_rotation_correct - pure_rotation_mutant).subs(sample)
        ),
    }
    if not all(catches.values()):
        raise AssertionError({key: value for key, value in catches.items() if not value})

    result = {
        "status": "PASS",
        "landing": "ALL_PREREGISTERED_HOSTILE_MUTATIONS_CAUGHT",
        "catch_count": len(catches),
        "caught_count": sum(bool(value) for value in catches.values()),
        "catches": catches,
        "alias_off_ray_difference": str(alias_off_ray),
        "commutator": [[str(entry) for entry in row] for row in commuting_error.tolist()],
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if os.environ.get("G196_NO_WRITE") == "1":
        print(payload, end="")
        return
    Path(__file__).with_name("CATCH_PROOF_RESULT.json").write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
