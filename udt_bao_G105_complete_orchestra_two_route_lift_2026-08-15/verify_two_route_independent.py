#!/usr/bin/env python3
"""Independent Fraction-only replay for G105; does not import production code."""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import json
import os
from pathlib import Path


def mm(A, B):
    return [[sum((A[i][k] * B[k][j] for k in range(len(B))), F(0))
             for j in range(len(B[0]))] for i in range(len(A))]


def mv(A, v):
    return [sum((A[i][k] * v[k] for k in range(len(v))), F(0)) for i in range(len(A))]


def kron_vec(a, b):
    return [x * y for x in a for y in b]


def kron_mat(A, B):
    return [[A[i][j] * B[k][ell]
             for j in range(len(A[0])) for ell in range(len(B[0]))]
            for i in range(len(A)) for k in range(len(B))]


def dot_eta(x, y):
    return -x[0] * y[0] + sum((x[i] * y[i] for i in range(1, 4)), F(0))


def vec_sub(x, y):
    return [a - b for a, b in zip(x, y)]


def vec_scale(a, x):
    return [a * v for v in x]


def angular_speed(E, trig):
    c, s, dc, ds = trig
    v0 = mv(E, [F(1), F(0), F(0), F(0)])
    v1 = mv(E, [F(0), F(0), c, s])
    dv1 = mv(E, [F(0), F(0), dc, ds])
    h00 = dot_eta(v0, v0)
    alpha = dot_eta(v0, v1) / h00
    dalpha = dot_eta(v0, dv1) / h00
    r = vec_sub(v1, vec_scale(alpha, v0))
    dr = vec_sub(dv1, vec_scale(dalpha, v0))
    l2 = dot_eta(r, r)
    rdr = dot_eta(r, dr)
    speed2 = dot_eta(dr, dr) / l2 - rdr * rdr / (l2 * l2)
    return h00, l2, speed2


def main(production_path: Path) -> dict:
    K = [[F(1), F(0), F(1, 2)], [F(0), F(1), F(1, 2)]]
    lam = [F(1, 6), F(1, 3), F(1, 2)]
    p_k = mv(K, lam)
    factor_left = mv(kron_mat(K, K), kron_vec(lam, lam))
    factor_right = kron_vec(p_k, p_k)

    q = [F(1, 3)] * 3
    m = [F(-1, 2), F(1, 4), F(1, 4)]
    p = [q[i] * (1 + m[i]) for i in range(3)]
    d = [p[i] - q[i] for i in range(3)]
    W = [[F(0), F(0), F(0)], [F(0), F(0), F(1)], [F(0), F(1), F(0)]]
    wd = mv(W, d)
    ls = sum((d[i] * wd[i] for i in range(3)), F(0))
    wq = mv(W, q)
    rr = sum((q[i] * wq[i] for i in range(3)), F(0))

    H = [[F(1, 16), F(-1, 16)], [F(-1, 16), F(1, 16)]]
    pair_h = [[F(1, 4) + H[i][j] for j in range(2)] for i in range(2)]

    B = [[F(2), F(1, 3)], [F(1, 5), F(3, 2)]]
    Q = [[F(3, 2), F(1, 4)], [F(1, 5), F(4, 3)]]
    S = [[F(1, 4), F(1, 6)], [F(-1, 7), F(1, 5)]]
    QS = mm(Q, S)
    E = [B[0] + [F(0), F(0)], B[1] + [F(0), F(0)], QS[0] + Q[0], QS[1] + Q[1]]
    z = angular_speed(E, (F(1), F(0), F(0), F(1)))
    qtr = angular_speed(E, (F(0), F(1), F(-1), F(0)))

    production = json.loads(production_path.read_text(encoding="utf-8"))
    expected = production["complete_orchestra_jacobian_witness"]
    checks = {
        "no_production_import": True,
        "factorized_pushforward_exact": factor_left == factor_right,
        "one_point_ls_exact": ls == F(1, 72),
        "normalized_ls_exact": ls / rr == F(1, 16),
        "p_normalized": sum(p, F(0)) == 1,
        "q_weighted_m_zero": sum((q[i] * m[i] for i in range(3)), F(0)) == 0,
        "H_zero_margins": all(sum(row, F(0)) == 0 for row in H)
        and all(sum((H[i][j] for i in range(2)), F(0)) == 0 for j in range(2)),
        "H_pair_nonnegative": all(x >= 0 for row in pair_h for x in row),
        "clock_exact": str(z[0]) == expected["h00"],
        "L2_zero_exact": str(z[1]) == expected["L2_theta_0"],
        "L2_quarter_exact": str(qtr[1]) == expected["L2_theta_pi_over_2"],
        "speed_zero_exact": str(z[2]) == expected["angular_speed2_theta_0"],
        "speed_quarter_exact": str(qtr[2]) == expected["angular_speed2_theta_pi_over_2"],
        "jacobian_nonconstant": z[2] != qtr[2],
    }
    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "exact": {
            "factorized_residual": [str(x) for x in vec_sub(factor_left, factor_right)],
            "ls_numerator": str(ls),
            "ls_normalized": str(ls / rr),
            "h00": str(z[0]),
            "speed2_zero": str(z[2]),
            "speed2_quarter": str(qtr[2]),
        },
        "outcome_paths_read": [],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--production", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = main(args.production)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output and os.environ.get("UDT_READ_ONLY_REPLAY") != "1":
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    raise SystemExit(0 if result["status"] == "PASS" else 1)
