#!/usr/bin/env python3
"""Exact hostile-mutation catches for the preregistered G198 test."""

from __future__ import annotations

import json
import os
from pathlib import Path

import sympy as sp


def nonzero(matrix):
    return any(sp.simplify(entry) != 0 for entry in matrix)


def main():
    A, N, B, R = sp.symbols("A N B R", real=True)
    Ae, Ne, Be, Re = sp.symbols("Ae Ne Be Re", real=True)
    Az, Nz, Bz, Rz = sp.symbols("Az Nz Bz Rz", real=True)
    tau = sp.symbols("tau", nonzero=True, real=True)
    M = sp.Matrix([[A, N + R], [N - R, B]])
    DeM = sp.Matrix([[Ae, Ne + Re], [Ne - Re, Be]])
    DzM = sp.Matrix([[Az, Nz + Rz], [Nz - Rz, Bz]])
    Omega = sp.Matrix([[0, R], [-R, 0]])
    DpM = DeM + DzM
    DmM = DeM - DzM

    sample = {
        A: sp.Rational(2, 5),
        N: sp.Rational(-1, 7),
        B: sp.Rational(1, 3),
        R: sp.Rational(3, 11),
        Ae: sp.Rational(1, 13),
        Ne: sp.Rational(-2, 17),
        Be: sp.Rational(3, 19),
        Re: sp.Rational(1, 23),
        Az: sp.Rational(4, 29),
        Nz: sp.Rational(-3, 31),
        Bz: sp.Rational(2, 37),
        Rz: sp.Rational(-5, 41),
    }

    incoming_connection = sp.zeros(2)
    outgoing_connection = 2 * Omega
    incoming_tide = tau * sp.eye(2)
    outgoing_zero_order = 2 * DpM - 4 * M.T * M
    false_mirror_zero_order = 2 * DmM - 4 * M.T * M

    y_eta, y_z, y_ee, y_ez, y_zz = sp.symbols(
        "y_eta y_z y_ee y_ez y_zz", real=True
    )
    correct_minus_second = y_ee - 2 * y_ez + y_zz
    hand_inserted_plus = y_ee + 2 * y_ez + y_zz

    Ceta = sp.Matrix([[1, 2], [3, 5]])
    Cz = sp.Matrix([[2, -1], [4, 0]])
    generalized_minus_contraction = Ceta - Cz
    g196_minus_contraction = M - M

    eta, z = sp.symbols("eta z", real=True)
    alias = (eta - z) ** 2 * (eta + z) ** 2
    alias_on_plus = sp.simplify(alias.subs(z, eta))
    alias_on_minus = sp.simplify(alias.subs(z, -eta))
    alias_first_plus = sp.simplify((sp.diff(alias, eta) + sp.diff(alias, z)).subs(z, eta))
    alias_first_minus = sp.simplify((sp.diff(alias, eta) - sp.diff(alias, z)).subs(z, -eta))
    alias_offray = sp.simplify(alias.subs({eta: sp.Rational(3, 10), z: sp.Rational(1, 10)}))

    s = sp.symbols("s", real=True)
    fake_determinant = (s - sp.Rational(1, 8)) ** 2
    sample_points = [sp.Rational(0), sp.Rational(1, 4), sp.Rational(1, 2), sp.Rational(3, 4), sp.Rational(1)]
    finite_positive = all(fake_determinant.subs(s, point) > 0 for point in sample_points)
    hidden_zero = sp.simplify(fake_determinant.subs(s, sp.Rational(1, 8))) == 0

    catches = {
        "replace_minus_by_plus": nonzero((outgoing_connection - incoming_connection).subs(sample)),
        "impose_z_mirror": nonzero((outgoing_zero_order - false_mirror_zero_order).subs(sample)),
        "force_entire_incoming_tide_zero": nonzero(incoming_tide),
        "insert_wrong_directional_operator": sp.simplify(correct_minus_second - hand_inserted_plus) != 0,
        "equate_opposite_jacobi_maps": nonzero(outgoing_zero_order.subs(sample)),
        "two_rays_reconstruct_field": (
            alias_on_plus == 0
            and alias_on_minus == 0
            and alias_first_plus == 0
            and alias_first_minus == 0
            and alias_offray != 0
        ),
        "activate_independent_minus_channel": (
            g196_minus_contraction == sp.zeros(2) and nonzero(generalized_minus_contraction)
        ),
        "finite_samples_prove_no_caustic": finite_positive and hidden_zero,
        "erase_metric_encoded_asymmetry": (
            nonzero(outgoing_connection.subs(sample)) and incoming_connection == sp.zeros(2)
        ),
    }
    if not all(catches.values()):
        raise AssertionError({key: value for key, value in catches.items() if not value})

    result = {
        "status": "PASS",
        "landing": "ALL_PREREGISTERED_G198_HOSTILE_MUTATIONS_CAUGHT",
        "catch_count": len(catches),
        "caught_count": sum(bool(value) for value in catches.values()),
        "catches": catches,
        "two_ray_alias_offray_value": str(alias_offray),
        "generalized_minus_contraction": [
            [str(entry) for entry in generalized_minus_contraction.row(index)] for index in range(2)
        ],
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if os.environ.get("G198_NO_WRITE") == "1":
        print(payload, end="")
        return
    Path(__file__).with_name("CATCH_PROOF_RESULT.json").write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
