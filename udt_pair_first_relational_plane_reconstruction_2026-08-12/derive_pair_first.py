#!/usr/bin/env python3
"""Exact symbolic derivation for the preregistered pair-first audit."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def matrix_zero(m: sp.Matrix) -> bool:
    return all(sp.simplify(x) == 0 for x in m)


def main() -> None:
    T, L, beta = sp.symbols("T L beta", positive=True, real=True)
    qa, qc = sp.symbols("qa qc", positive=True, real=True)
    qb = sp.symbols("qb", real=True)

    B = sp.Matrix([[T, T * beta], [0, L]])
    Q = sp.Matrix([[qa, 0], [qb, qc]])
    q = Q.T * Q
    eta2 = sp.diag(-1, 1)
    eta4 = sp.diag(-1, 1, 1, 1)

    s = sp.symbols("s00 s01 s10 s11", real=True)
    y = sp.symbols("y00 y01 y10 y11", real=True)
    z = sp.symbols("z00 z01 z10 z11", real=True)
    S = sp.Matrix(2, 2, s)
    Y = sp.Matrix(2, 2, y)
    Z = sp.Matrix(2, 2, z)

    E = B.row_join(sp.zeros(2)).col_join((Q * S).row_join(Q))
    J = Y.col_join(Z)
    g = E.T * eta4 * E
    h_direct = sp.expand(J.T * g * J)
    h_block = sp.expand(
        Y.T * B.T * eta2 * B * Y + (S * Y + Z).T * q * (S * Y + Z)
    )
    direct_pullback = matrix_zero(h_direct - h_block)

    # Invertible-base-projection reduction. Multiplying by adj(Y)/det(Y)
    # keeps the check exact over the rational function field.
    Yinv = Y.inv()
    C = S + Z * Yinv
    h_reduced = sp.simplify(Yinv.T * h_block * Yinv)
    h_reduced_expected = sp.simplify(B.T * eta2 * B + C.T * q * C)
    reduced_gram = matrix_zero(h_reduced - h_reduced_expected)

    # Pair-domain coordinate covariance J -> J R.
    r = sp.symbols("r00 r01 r10 r11", real=True)
    R = sp.Matrix(2, 2, r)
    h_reparam = sp.expand((J * R).T * g * (J * R))
    coordinate_covariance = matrix_zero(h_reparam - R.T * h_direct * R)

    # Exact rational O(2) screen-frame change Q -> O Q.
    O = sp.Matrix([[sp.Rational(3, 5), -sp.Rational(4, 5)],
                   [sp.Rational(4, 5), sp.Rational(3, 5)]])
    screen_covariance = matrix_zero((O * Q).T * (O * Q) - q)

    # Calibrated components after an arbitrary positive-semidefinite Gram correction.
    a, d, e = sp.symbols("a d e", real=True)
    P = sp.Matrix([[a, d], [d, e]])
    h0 = sp.expand(B.T * eta2 * B)
    h_cal = sp.expand(h0 + P)
    A = sp.expand(T**2 - a)  # T_pair^2 on the timelike calibrated stratum.
    beta_pair = sp.simplify(h_cal[0, 1] / h_cal[0, 0])
    L_pair_sq = sp.simplify(h_cal[1, 1] - h_cal[0, 1] ** 2 / h_cal[0, 0])
    determinant_identity = sp.simplify(-h_cal.det() - A * L_pair_sq) == 0
    pure_base = matrix_zero(h_cal.subs({a: 0, d: 0, e: 0}) - h0)
    beta_base = sp.simplify(beta_pair.subs({a: 0, d: 0, e: 0}) - beta) == 0
    L_base = sp.simplify(L_pair_sq.subs({a: 0, d: 0, e: 0}) - L**2) == 0

    # The flat event-pairing family from the ownership audit.
    k, ell = sp.symbols("k ell", real=True, nonzero=True)
    Jk = sp.Matrix([[1, k / ell], [0, 1]])
    hk = sp.simplify(Jk.T * eta2 * Jk)
    flat_expected = sp.Matrix([[-1, -k / ell], [-k / ell, 1 - k**2 / ell**2]])
    flat_family = matrix_zero(hk - flat_expected)
    flat_det = sp.simplify(hk.det())
    flat_phi_argument = sp.simplify((-flat_det) / hk[0, 0] ** 2)

    # A complete, unfiltered signature witness atlas for h0=diag(-1,+1), q=I.
    signature_witnesses = []
    witness_C = {
        "zero_lorentzian": sp.zeros(2),
        "small_lorentzian": sp.diag(sp.Rational(1, 2), sp.Rational(1, 2)),
        "clock_null_degenerate": sp.diag(1, 0),
        "large_positive_definite": sp.diag(2, 0),
        "rank_one_tilted_lorentzian": sp.Matrix([[sp.Rational(1, 2), sp.Rational(1, 3)], [0, 0]]),
    }
    base_control = sp.diag(-1, 1)
    for name, Cw in witness_C.items():
        hw = base_control + Cw.T * Cw
        eigs = sorted(float(v) for v in hw.eigenvals().keys())
        tol = 1.0e-12
        neg = sum(v < -tol for v in eigs)
        zero = sum(abs(v) <= tol for v in eigs)
        pos = sum(v > tol for v in eigs)
        signature_witnesses.append(
            {
                "name": name,
                "h": [[str(sp.simplify(hw[i, j])) for j in range(2)] for i in range(2)],
                "inertia": [neg, zero, pos],
            }
        )

    checks = {
        "direct_pullback_identity": direct_pullback,
        "reduced_gram_identity": reduced_gram,
        "pair_coordinate_covariance": coordinate_covariance,
        "screen_frame_covariance": screen_covariance,
        "determinant_terminal_identity": determinant_identity,
        "pure_base_metric": pure_base,
        "pure_base_beta": beta_base,
        "pure_base_L": L_base,
        "flat_counterfamily_metric": flat_family,
        "flat_counterfamily_det_minus_one": flat_det == -1,
        "flat_counterfamily_phi_argument_one": flat_phi_argument == 1,
    }
    if not all(checks.values()):
        raise SystemExit(f"failed checks: {[k for k, v in checks.items() if not v]}")

    result = {
        "schema": "udt-pair-first-relational-plane-v1",
        "status": "PASS",
        "checks": checks,
        "calibrated_components": {
            "h00": str(h_cal[0, 0]),
            "h01": str(h_cal[0, 1]),
            "h11": str(h_cal[1, 1]),
            "T_pair_squared": str(A),
            "beta_pair": str(beta_pair),
            "L_pair_squared": str(L_pair_sq),
            "minus_det_h": str(sp.factor(-h_cal.det())),
            "c_eff_over_c_E_squared": str(sp.factor(A / L_pair_sq)),
        },
        "flat_counterfamily": {
            "h": [[str(hk[i, j]) for j in range(2)] for i in range(2)],
            "det_h": str(flat_det),
            "phi_argument": str(flat_phi_argument),
        },
        "signature_witnesses": signature_witnesses,
        "claim_boundary": {
            "abstract_channel_plane": "POSIT",
            "pair_plane_given_F": "DERIVED_CONDITIONAL",
            "orthogonal_screen_given_timelike_F": "DERIVED_CONDITIONAL",
            "physical_F": "OPEN",
            "global_integrable_pair_family_without_F": "OPEN",
        },
    }
    (HERE / "DERIVATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
