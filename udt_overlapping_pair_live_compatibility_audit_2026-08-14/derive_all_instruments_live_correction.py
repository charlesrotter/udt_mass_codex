#!/usr/bin/env python3
"""Exact C2 all-instruments-live correction for the G90 response classification."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "ALL_INSTRUMENTS_LIVE_DERIVATION_RESULT.json"
t = sp.symbols("t", positive=True)
eta2 = sp.diag(-1, 1)
eta4 = sp.diag(-1, 1, 1, 1)


def zmat() -> sp.Matrix:
    return sp.zeros(2)


def base_blocks() -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    sigma = 1 + t / 31
    beta = t / 37
    B = sp.Matrix([[sigma / t, sigma * beta / t], [0, sigma * t]])
    Q = sp.Matrix([[1 + t / 7, t / 11], [0, 1 + t / 13]])
    S = sp.Matrix([[t / 17, t**2 / 19], [t**3 / 23, t**4 / 29]])
    return B, Q, S


def reciprocal_columns(Tp: sp.Expr, Lp: sp.Expr, r: sp.Expr, s: sp.Expr) -> tuple[sp.Matrix, sp.Matrix]:
    # Rational parametrizations of -u0^2+a0^2=-Tp^2 and u1^2+a1^2=Lp^2.
    u0 = Tp * (1 + r**2) / (1 - r**2)
    a0 = Tp * (2 * r) / (1 - r**2)
    u1 = Lp * (1 - s**2) / (1 + s**2)
    a1 = Lp * (2 * s) / (1 + s**2)
    return sp.diag(u0, u1), sp.diag(a0, a1)


def target(kind: str) -> tuple[sp.Matrix, sp.Matrix, sp.Expr, sp.Expr, sp.Expr]:
    Tp = 1 / t
    r = sp.Rational(1, 10)
    if kind == "flat":
        Lp = t
        s = sp.Rational(1, 20)
        exp4m = sp.Integer(1)
    elif kind == "monotone":
        Lp = t**2
        s = sp.Rational(1, 20)
        exp4m = t**2
    elif kind == "quiet":
        w = (t - sp.Rational(1, 2)) * (sp.Rational(3, 2) - t)
        Lp = t / w**2
        s = sp.Rational(1, 4) + 3 * (t - 1) ** 2
        exp4m = w**-4
    else:
        raise ValueError(kind)
    U, A = reciprocal_columns(Tp, Lp, r, s)
    return U, A, Tp, Lp, exp4m


def nonzero_at_one(M: sp.Matrix) -> bool:
    return any(sp.simplify(x.subs(t, 1)) != 0 for x in M)


def exact_matrix_zero(M: sp.Matrix) -> bool:
    return all(sp.factor(sp.cancel(x)) == 0 for x in M)


def family(kind: str) -> dict[str, object]:
    B, Q, S = base_blocks()
    Ustar, Astar, Tp, Lp, exp4m_expected = target(kind)
    Y = sp.simplify(B.inv() * Ustar)
    Z = sp.simplify(Q.inv() * Astar - S * Y)
    Rpair = sp.simplify(S * Y + Z)
    U = sp.simplify(B * Y)
    A = sp.simplify(Q * Rpair)
    h = sp.simplify(U.T * eta2 * U + A.T * A)
    h_expected = sp.diag(-Tp**2, Lp**2)

    Bd, Qd, Sd, Yd, Zd = [M.diff(t) for M in (B, Q, S, Y, Z)]
    Ad_Q = Qd * Rpair
    Ad_S = Q * Sd * Y
    Ad_Y = Q * S * Yd
    Ad_Z = Q * Zd
    Ud_B = Bd * Y
    Ud_Y = B * Yd
    HB = sp.simplify(Ud_B.T * eta2 * U + U.T * eta2 * Ud_B)
    HQ = sp.simplify(Ad_Q.T * A + A.T * Ad_Q)
    HS = sp.simplify(Ad_S.T * A + A.T * Ad_S)
    HY = sp.simplify(
        Ud_Y.T * eta2 * U + U.T * eta2 * Ud_Y + Ad_Y.T * A + A.T * Ad_Y
    )
    HZ = sp.simplify(Ad_Z.T * A + A.T * Ad_Z)
    hdot = h.diff(t)

    E = B.row_join(zmat()).col_join((Q * S).row_join(Q))
    J = Y.col_join(Z)
    V = sp.simplify(E * J)
    g = sp.simplify(E.T * eta4 * E)

    # A-calibrated normalized screen loading. This is calculated from the full lift.
    W = sp.simplify(Z * Y.inv())
    C = sp.simplify(S + W)
    P = sp.simplify(C.T * Q.T * Q * C)
    Pi = sp.simplify(B.inv().T * P * B.inv())
    atrace = sp.factor(sp.trace(Pi))

    terminal_ratio = sp.factor((-h.det()) / h[0, 0] ** 2)
    exp4m = sp.factor(terminal_ratio / t**4)

    Rchart = sp.Matrix([[1, t], [0, 1]])
    Ja = sp.simplify(J * Rchart)
    ha_direct = sp.simplify(Ja.T * g * Ja)
    ha_cov = sp.simplify(Rchart.T * h * Rchart)
    live_cov_residual = sp.simplify(
        ha_direct.diff(t)
        - (
            Rchart.diff(t).T * h * Rchart
            + Rchart.T * hdot * Rchart
            + Rchart.T * h * Rchart.diff(t)
        )
    )

    checks = {
        "uncompressed_factorization": exact_matrix_zero(V - Ustar.col_join(Astar)),
        "target_metric": exact_matrix_zero(h - h_expected),
        "pair_rank_two_at_t0": J.subs(t, 1).rank() == 2,
        "pair_regular_at_t0": bool(h[0, 0].subs(t, 1) < 0 and h.det().subs(t, 1) < 0),
        "B_live": nonzero_at_one(Bd),
        "Q_live": nonzero_at_one(Qd),
        "S_live": nonzero_at_one(Sd),
        "all_four_S_entries_live": all(sp.simplify(x.subs(t, 1)) != 0 for x in Sd),
        "Y_live": nonzero_at_one(Yd),
        "Z_live": nonzero_at_one(Zd),
        "H_B_nonzero": nonzero_at_one(HB),
        "H_Q_nonzero": nonzero_at_one(HQ),
        "H_S_nonzero": nonzero_at_one(HS),
        "H_Y_nonzero": nonzero_at_one(HY),
        "H_Z_nonzero": nonzero_at_one(HZ),
        "hdot_partition": exact_matrix_zero(hdot - HB - HQ - HS - HY - HZ),
        "ambient_metric_live": nonzero_at_one(g.diff(t)),
        "both_screen_columns_present": all(Astar[:, i].subs(t, 1).norm() != 0 for i in range(2)),
        "both_base_columns_present": all(Ustar[:, i].subs(t, 1).norm() != 0 for i in range(2)),
        "nonidentity_overlap": Rchart.subs(t, 1) != sp.eye(2),
        "overlap_metric_covariance": exact_matrix_zero(ha_direct - ha_cov),
        "overlap_live_covariance": exact_matrix_zero(live_cov_residual),
        "terminal_shape_exact": sp.factor(exp4m - exp4m_expected) == 0,
    }

    if kind == "flat":
        checks["terminal_modulation_flat"] = sp.factor(exp4m - 1) == 0
        checks["trace_flat"] = sp.factor(sp.diff(atrace, t)) == 0
    elif kind == "monotone":
        checks["terminal_modulation_strictly_increasing"] = bool(sp.diff(exp4m, t).subs(t, 1) > 0)
        checks["trace_flat"] = sp.factor(sp.diff(atrace, t)) == 0
    else:
        checks["terminal_quiet_stationary"] = sp.factor(sp.diff(exp4m, t).subs(t, 1)) == 0
        checks["terminal_quiet_strict_minimum"] = bool(sp.diff(exp4m, t, 2).subs(t, 1) > 0)
        checks["trace_quiet_stationary"] = sp.factor(sp.diff(atrace, t).subs(t, 1)) == 0
        checks["trace_quiet_strict_minimum"] = bool(sp.diff(atrace, t, 2).subs(t, 1) > 0)
        checks["trace_loud_left"] = sp.limit(atrace, t, sp.Rational(1, 2), dir="+") == sp.oo
        checks["trace_loud_right"] = sp.limit(atrace, t, sp.Rational(3, 2), dir="-") == sp.oo
        checks["terminal_loud_left"] = sp.limit(exp4m, t, sp.Rational(1, 2), dir="+") == sp.oo
        checks["terminal_loud_right"] = sp.limit(exp4m, t, sp.Rational(3, 2), dir="-") == sp.oo

    return {
        "kind": kind,
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "t0": "1",
        "pair_metric_at_t0": [[str(sp.factor(x)) for x in row] for row in h.subs(t, 1).tolist()],
        "A_trace": str(atrace),
        "exp_4M_terminal": str(exp4m),
        "contribution_norms_squared_at_t0": {
            name: str(sp.factor(sum(x**2 for x in H.subs(t, 1))))
            for name, H in (("B", HB), ("Q", HQ), ("S", HS), ("Y", HY), ("Z", HZ))
        },
    }


def main() -> None:
    families = [family(kind) for kind in ("flat", "monotone", "quiet")]
    checks = {f"{item['kind']}_all_checks": bool(item["all_checks_pass"]) for item in families}
    result = {
        "schema": "udt.g90.all_instruments_live_correction.v1",
        "primary_landing": "ALL_INSTRUMENTS_ACTIVITY_ALONE_DOES_NOT_SELECT_RESPONSE_SHAPE",
        "secondary_landing": "LOUD_QUIET_LOUD_SURVIVES_DECLARED_ALL_ACTIVE_CLASS",
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "families": families,
        "maximum_conclusion": (
            "C2 activity in the declared calibrated complete-coframe/pair chart neither selects nor "
            "excludes loud-quiet-loud; physical history ownership remains open"
        ),
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
