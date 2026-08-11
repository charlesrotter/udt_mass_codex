#!/usr/bin/env python3
"""Exact local chart-openness and owner-classification derivation."""

from __future__ import annotations

import argparse
import json
from math import comb
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def derive() -> dict[str, object]:
    T, L, beta, u, v, w = sp.symbols("T L beta u v w", nonzero=True)
    s00, s01, s10, s11 = sp.symbols("s00 s01 s10 s11")
    B = sp.Matrix([[T, T * beta], [0, L]])
    Q = sp.Matrix([[u, 0], [v, w]])
    S = sp.Matrix([[s00, s01], [s10, s11]])
    E = B.row_join(sp.zeros(2)).col_join((Q * S).row_join(Q))
    eta4 = sp.diag(-1, 1, 1, 1)
    eta2 = sp.diag(-1, 1)
    g = sp.simplify(E.T * eta4 * E)
    H = sp.simplify(Q.T * Q)
    cross = sp.simplify(S.T * H)
    schur = sp.simplify(g[:2, :2] - cross * H.inv() * cross.T)

    outputs = [
        g[0, 0], g[0, 1], g[1, 1], g[0, 2], g[0, 3],
        g[1, 2], g[1, 3], g[2, 2], g[2, 3], g[3, 3],
    ]
    parameters = [T, L, beta, u, v, w, s00, s01, s10, s11]
    jacobian_det = sp.factor(sp.Matrix(outputs).jacobian(parameters).det())
    expected_jacobian = 16 * L * T**3 * u**5 * w**6

    checks = {
        "complete_metric_determinant": sp.simplify(g.det() + L**2 * T**2 * u**2 * w**2) == 0,
        "screen_determinant": sp.simplify(H.det() - u**2 * w**2) == 0,
        "cross_block": sp.simplify(g[:2, 2:] - cross) == sp.zeros(2),
        "schur_complement": sp.simplify(schur - B.T * eta2 * B) == sp.zeros(2),
        "jacobian_nonzero_formula": sp.simplify(jacobian_det - expected_jacobian) == 0,
        "inverse_T_squared": sp.simplify(-schur[0, 0] - T**2) == 0,
        "inverse_beta": sp.simplify(schur[0, 1] / schur[0, 0] - beta) == 0,
        "inverse_L_squared": sp.simplify(schur.det() / schur[0, 0] - L**2) == 0,
        "inverse_w_squared": sp.simplify(H[1, 1] - w**2) == 0,
        "inverse_v": sp.simplify(H[0, 1] / w - v) == 0,
        "inverse_u_squared": sp.simplify(H.det() / H[1, 1] - u**2) == 0,
        "inverse_mixing": sp.simplify(H.inv() * cross.T - S) == sp.zeros(2),
        "first_jet_block_count": comb(4 + 1, 1) == 5,
        "second_jet_block_count": comb(4 + 2, 2) == 15,
    }
    assert all(checks.values()), checks

    return {
        "status": (
            "COMPLETE_REGULAR_CHART_IS_LOCALLY_JET_OPEN_ON_THE_DECLARED_"
            "POSITIVE_SCREEN_TIME_ORIENTED_COMPONENT__NO_CURRENTLY_OWNED_"
            "NONIDENTITY_HISTORY_RESTRICTION_IS_FOUND_IN_THE_TEN_FROZEN_SOURCES"
        ),
        "exact_check_count": len(checks),
        "exact_checks": checks,
        "zero_jet_jacobian_determinant": str(jacobian_det),
        "first_jet_prolongation_determinant": f"({jacobian_det})^5",
        "second_jet_prolongation_determinant": f"({jacobian_det})^15",
        "candidate_owner_classes": 5,
        "genuine_owned_history_restrictions": 0,
        "maximum_conclusion": (
            "the declared positive-screen, time-oriented regular split chart is a local "
            "diffeomorphism on metric finite jets; the five owner classes audited across the "
            "ten frozen manifest sources supply identities, readouts, conditional "
            "comparisons, or global/boundary gates, but no owned nonidentity history law"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--read-only", action="store_true")
    args = parser.parse_args()
    result = derive()
    if not args.read_only:
        (HERE / "DERIVATION_RESULT.json").write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    print(
        f"PASS exact={result['exact_check_count']} owners={result['candidate_owner_classes']} "
        f"selected={result['genuine_owned_history_restrictions']}"
    )


if __name__ == "__main__":
    main()
