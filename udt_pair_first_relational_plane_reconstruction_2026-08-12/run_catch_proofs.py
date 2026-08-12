#!/usr/bin/env python3
"""Hostile finite-dimensional mutations for the pair-first package."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def changed(a, b):
    return any(sp.simplify(x) != 0 for x in (a - b))


def main():
    eta2 = sp.diag(-1, 1)
    B = sp.Matrix([[2, sp.Rational(2, 3)], [0, 3]])
    Q = sp.Matrix([[2, 0], [1, 1]])
    q = Q.T * Q
    S = sp.Matrix([[sp.Rational(1, 2), sp.Rational(-1, 3)], [sp.Rational(1, 4), sp.Rational(2, 5)]])
    Y = sp.Matrix([[1, sp.Rational(1, 5)], [sp.Rational(-1, 7), 1]])
    Z = sp.Matrix([[sp.Rational(2, 3), sp.Rational(1, 6)], [sp.Rational(-1, 8), sp.Rational(3, 7)]])
    K = S * Y + Z
    correct = Y.T * B.T * eta2 * B * Y + K.T * q * K

    catches = {}
    catches["omit_embedding_Z"] = changed(correct, Y.T * B.T * eta2 * B * Y + (S * Y).T * q * (S * Y))
    catches["omit_metric_mixing_S"] = changed(correct, Y.T * B.T * eta2 * B * Y + Z.T * q * Z)
    catches["omit_screen_metric_Q"] = changed(correct, Y.T * B.T * eta2 * B * Y + K.T * K)
    catches["wrong_base_signature"] = changed(correct, Y.T * B.T * sp.eye(2) * B * Y + K.T * q * K)
    catches["drop_gram_cross_term"] = changed(correct, Y.T * B.T * eta2 * B * Y + sp.diag(*(K.T * q * K).diagonal()))

    R = sp.Matrix([[1, sp.Rational(1, 2)], [sp.Rational(1, 3), 1]])
    covariant = R.T * correct * R
    catches["forget_pair_tensor_congruence"] = changed(covariant, correct)

    T, L, beta = sp.Integer(2), sp.Integer(3), sp.Rational(1, 4)
    a, d, e = sp.Rational(1, 3), sp.Rational(-1, 5), sp.Rational(2, 7)
    h = sp.Matrix([[-T**2 + a, -T**2 * beta + d],
                   [-T**2 * beta + d, L**2 - T**2 * beta**2 + e]])
    beta_correct = sp.simplify(h[0, 1] / h[0, 0])
    catches["wrong_beta_sign"] = sp.simplify(beta_correct + h[0, 1] / h[0, 0]) != 0
    L2_correct = sp.simplify(h[1, 1] - h[0, 1] ** 2 / h[0, 0])
    catches["omit_shift_square_in_L"] = sp.simplify(L2_correct - h[1, 1]) != 0

    k, ell = sp.Rational(2, 3), sp.Rational(5, 2)
    hk = sp.Matrix([[-1, -k / ell], [-k / ell, 1 - k**2 / ell**2]])
    catches["terminal_phi_cannot_recover_pairing_k"] = (
        sp.simplify((-hk.det()) / hk[0, 0] ** 2) == 1 and hk[0, 1] != 0
    )

    C = sp.Matrix([[2, -1], [1, 3]])
    P = C.T * q * C
    catches["gram_term_not_indefinite"] = all(
        sp.simplify((sp.Matrix(v).T * P * sp.Matrix(v))[0]) >= 0
        for v in [(1, 0), (0, 1), (1, 1), (2, -3)]
    )

    catches["founding_does_not_own_F_guard"] = "physical F or event pairing from founding postulates\tOPEN" in (
        HERE / "STATUS_LEDGER.tsv"
    ).read_text(encoding="utf-8")
    catches["global_integrability_not_promoted_guard"] = "no arbitrary pointwise plane field" in (
        HERE / "AUDIT_REPORT.md"
    ).read_text(encoding="utf-8")

    status = "PASS" if all(catches.values()) else "FAIL"
    result = {
        "schema": "udt-pair-first-catch-proofs-v1",
        "status": status,
        "caught": sum(bool(x) for x in catches.values()),
        "catch_count": len(catches),
        "catches": catches,
    }
    (HERE / "CATCH_PROOF_RESULTS.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if status != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
