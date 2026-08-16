#!/usr/bin/env python3
"""Exact G105 algebra. This script reads no observational outcome."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import sympy as sp


LANDING = (
    "COMPLETE_ORCHESTRA_ONE_POINT_OBSERVER_ARTIFACT_CHANNEL_DERIVED_CONDITIONALLY"
    "__FACTORIZED_INTRINSIC_CONNECTED_EXCESS_ZERO"
    "__LOCAL_COMMON_OBSERVER_H_NOT_OWNED"
    "__PHYSICAL_HISTORY_REFERENCE_PROJECTION_AND_GLOBAL_BRANCH_LAW_OPEN"
    "__BOSS_AND_CMB_OUTCOMES_UNREAD"
)


def qstr(value: sp.Expr) -> str:
    return str(sp.factor(sp.simplify(value)))


def main() -> dict:
    # Factorized pushforward witness, including a noninjective stochastic K1.
    K = sp.Matrix(
        [
            [sp.Rational(1), 0, sp.Rational(1, 2)],
            [0, sp.Rational(1), sp.Rational(1, 2)],
        ]
    )
    lam = sp.Matrix([sp.Rational(1, 6), sp.Rational(1, 3), sp.Rational(1, 2)])
    p_k = K * lam
    lhs = sp.kronecker_product(K, K) * sp.kronecker_product(lam, lam)
    rhs = sp.kronecker_product(p_k, p_k)

    # Exact estimator-visible one-point modulation witness.
    q = sp.Matrix([sp.Rational(1, 3)] * 3)
    m = sp.Matrix([sp.Rational(-1, 2), sp.Rational(1, 4), sp.Rational(1, 4)])
    p = sp.Matrix([q[i] * (1 + m[i]) for i in range(3)])
    d = p - q
    W = sp.Matrix([[0, 0, 0], [0, 0, 1], [0, 1, 0]])
    ls_direct = (d.T * W * d)[0]
    ls_expanded = (
        (p.T * W * p)[0]
        - (p.T * W * q)[0]
        - (q.T * W * p)[0]
        + (q.T * W * q)[0]
    )
    rr = (q.T * W * q)[0]

    # Exact irreducible H witness: zero marginals, positive total pair measure.
    p2 = sp.Matrix([sp.Rational(1, 2), sp.Rational(1, 2)])
    H = sp.Rational(1, 16) * sp.Matrix([[1, -1], [-1, 1]])
    pair_h = p2 * p2.T + H
    h_row_marginal = pair_h * sp.ones(2, 1)

    # A complete-coframe local angular-Jacobian witness. B, Q, S, the top
    # embedding Y and lower embedding Zeta are all nonzero in the assembled
    # clock/ruler pair. No post-readout correction is used.
    eta = sp.diag(-1, 1, 1, 1)
    B = sp.Matrix([[2, sp.Rational(1, 3)], [sp.Rational(1, 5), sp.Rational(3, 2)]])
    Q = sp.Matrix([[sp.Rational(3, 2), sp.Rational(1, 4)], [sp.Rational(1, 5), sp.Rational(4, 3)]])
    S = sp.Matrix([[sp.Rational(1, 4), sp.Rational(1, 6)], [sp.Rational(-1, 7), sp.Rational(1, 5)]])
    E = B.row_join(sp.zeros(2, 2)).col_join((Q * S).row_join(Q))

    # The common clock column has Y!=0. The varying ruler has Zeta!=0.
    j0 = sp.Matrix([1, 0, 0, 0])
    c, s = sp.symbols("c s", real=True)
    dc, ds = sp.symbols("dc ds", real=True)
    j1 = sp.Matrix([0, 0, c, s])
    dj1 = sp.Matrix([0, 0, dc, ds])
    v0 = E * j0
    v1 = E * j1
    dv1 = E * dj1

    def inner(x: sp.Matrix, y: sp.Matrix) -> sp.Expr:
        return sp.expand((x.T * eta * y)[0])

    h00 = inner(v0, v0)
    alpha = inner(v0, v1) / h00
    dalpha = inner(v0, dv1) / h00
    r = sp.simplify(v1 - alpha * v0)
    dr = sp.simplify(dv1 - dalpha * v0)
    l2 = sp.simplify(inner(r, r))
    rdr = sp.simplify(inner(r, dr))
    speed2 = sp.factor(inner(dr, dr) / l2 - rdr**2 / l2**2)

    at_zero = {c: 1, s: 0, dc: 0, ds: 1}
    at_quarter = {c: 0, s: 1, dc: -1, ds: 0}
    l2_zero = sp.factor(l2.subs(at_zero))
    l2_quarter = sp.factor(l2.subs(at_quarter))
    speed2_zero = sp.factor(speed2.subs(at_zero))
    speed2_quarter = sp.factor(speed2.subs(at_quarter))

    def endpoint_speed(E_alt: sp.Matrix, substitutions: dict) -> sp.Expr:
        w0 = E_alt * j0
        w1 = E_alt * j1
        dw1 = E_alt * dj1
        w00 = inner(w0, w0)
        wa = inner(w0, w1) / w00
        dwa = inner(w0, dw1) / w00
        wr = sp.simplify(w1 - wa * w0)
        dwr = sp.simplify(dw1 - dwa * w0)
        wl2 = inner(wr, wr)
        value = inner(dwr, dwr) / wl2 - inner(wr, dwr) ** 2 / wl2**2
        return sp.factor(value.subs(substitutions))

    ident2 = sp.eye(2)
    zero2 = sp.zeros(2, 2)

    def assemble(B_alt: sp.Matrix, Q_alt: sp.Matrix, S_alt: sp.Matrix) -> sp.Matrix:
        return B_alt.row_join(zero2).col_join((Q_alt * S_alt).row_join(Q_alt))

    no_B_speed = endpoint_speed(assemble(ident2, Q, S), at_zero)
    no_Q_speed = endpoint_speed(assemble(B, ident2, S), at_zero)
    no_S_speed = endpoint_speed(assemble(B, Q, zero2), at_zero)

    checks = {
        "factorized_pushforward_exact": lhs == rhs,
        "K_columns_normalized": all(sum(K[:, j]) == 1 for j in range(K.cols)),
        "lambda_normalized": sum(lam) == 1,
        "modulated_p_normalized": sum(p) == 1,
        "q_weighted_m_zero": sum(q[i] * m[i] for i in range(3)) == 0,
        "ls_identity_exact": sp.simplify(ls_direct - ls_expanded) == 0,
        "ls_witness_nonzero": ls_direct != 0,
        "H_zero_row_marginals": H * sp.ones(2, 1) == sp.zeros(2, 1),
        "H_zero_column_marginals": sp.ones(1, 2) * H == sp.zeros(1, 2),
        "H_pair_nonnegative": all(x >= 0 for x in pair_h),
        "H_pair_marginal_preserved": h_row_marginal == p2,
        "complete_clock_timelike": h00 < 0,
        "pair_regular_at_zero": l2_zero > 0,
        "pair_regular_at_quarter": l2_quarter > 0,
        "angular_jacobian_nonconstant": speed2_zero != speed2_quarter,
        "B_sector_changes_jacobian": speed2_zero != no_B_speed,
        "Q_sector_changes_jacobian": speed2_zero != no_Q_speed,
        "S_sector_changes_jacobian": speed2_zero != no_S_speed,
        "all_complete_blocks_nonzero": all(M != sp.zeros(*M.shape) for M in (B, Q, S)),
        "pair_top_and_lower_embeddings_used": any(j0[:2, :]) and any(j1[2:, :]),
    }

    checks = {key: bool(value) for key, value in checks.items()}

    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "landing": LANDING,
        "checks": checks,
        "factorized_witness": {
            "p": [qstr(x) for x in p_k],
            "connected_residual": [qstr(x) for x in lhs - rhs],
        },
        "one_point_witness": {
            "q": [qstr(x) for x in q],
            "m": [qstr(x) for x in m],
            "p": [qstr(x) for x in p],
            "ls_numerator": qstr(ls_direct),
            "rr_denominator": qstr(rr),
            "normalized_estimator": qstr(ls_direct / rr),
        },
        "irreducible_H_witness": {
            "H": [[qstr(x) for x in H.row(i)] for i in range(H.rows)],
            "pair_measure": [[qstr(x) for x in pair_h.row(i)] for i in range(pair_h.rows)],
        },
        "complete_orchestra_jacobian_witness": {
            "h00": qstr(h00),
            "L2_theta_0": qstr(l2_zero),
            "L2_theta_pi_over_2": qstr(l2_quarter),
            "angular_speed2_theta_0": qstr(speed2_zero),
            "angular_speed2_theta_pi_over_2": qstr(speed2_quarter),
            "speed2_difference": qstr(speed2_zero - speed2_quarter),
            "speed2_without_B": qstr(no_B_speed),
            "speed2_without_Q": qstr(no_Q_speed),
            "speed2_without_S": qstr(no_S_speed),
        },
        "outcome_paths_read": [],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = main()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output and os.environ.get("UDT_READ_ONLY_REPLAY") != "1":
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    raise SystemExit(0 if result["status"] == "PASS" else 1)
