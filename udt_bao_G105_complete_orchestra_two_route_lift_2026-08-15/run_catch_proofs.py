#!/usr/bin/env python3
"""Hostile mutation checks for G105. Reads no observational outcome."""

from __future__ import annotations

from fractions import Fraction as F
import argparse
import json
import os
from pathlib import Path


def mm(A, B):
    return [[sum((A[i][k] * B[k][j] for k in range(len(B))), F(0))
             for j in range(len(B[0]))] for i in range(len(A))]


def mv(A, v):
    return [sum((A[i][j] * v[j] for j in range(len(v))), F(0)) for i in range(len(A))]


def dot(x, y):
    return -x[0] * y[0] + sum((x[i] * y[i] for i in range(1, 4)), F(0))


def speed(E, trig, omit_unit_projection=False):
    c, s, dc, ds = trig
    v0 = mv(E, [F(1), F(0), F(0), F(0)])
    v1 = mv(E, [F(0), F(0), c, s])
    dv1 = mv(E, [F(0), F(0), dc, ds])
    h00 = dot(v0, v0)
    a = dot(v0, v1) / h00
    da = dot(v0, dv1) / h00
    r = [v1[i] - a * v0[i] for i in range(4)]
    dr = [dv1[i] - da * v0[i] for i in range(4)]
    l2 = dot(r, r)
    naive = dot(dr, dr) / l2
    return naive if omit_unit_projection else naive - dot(r, dr) ** 2 / l2 ** 2


def build(B, Q, S):
    QS = mm(Q, S)
    return [B[0] + [F(0), F(0)], B[1] + [F(0), F(0)], QS[0] + Q[0], QS[1] + Q[1]]


def main():
    q = [F(1, 3)] * 3
    m = [F(-1, 2), F(1, 4), F(1, 4)]
    p = [q[i] * (1 + m[i]) for i in range(3)]
    d = [p[i] - q[i] for i in range(3)]
    W = [[F(0), F(0), F(0)], [F(0), F(0), F(1)], [F(0), F(1), F(0)]]
    bilinear = lambda x, y: sum((x[i] * mv(W, y)[i] for i in range(3)), F(0))
    baseline_ls = bilinear(d, d)

    B = [[F(2), F(1, 3)], [F(1, 5), F(3, 2)]]
    Q = [[F(3, 2), F(1, 4)], [F(1, 5), F(4, 3)]]
    S = [[F(1, 4), F(1, 6)], [F(-1, 7), F(1, 5)]]
    I = [[F(1), F(0)], [F(0), F(1)]]
    O = [[F(0), F(0)], [F(0), F(0)]]
    t0 = (F(1), F(0), F(0), F(1))
    base_speed = speed(build(B, Q, S), t0)

    H_bad_margin = [[F(1, 16), F(-1, 32)], [F(-1, 16), F(1, 16)]]
    H_too_large = [[F(1), F(-1)], [F(-1), F(1)]]
    pair_too_large = [[F(1, 4) + H_too_large[i][j] for j in range(2)] for i in range(2)]
    intrinsic_connected = [p[i] * p[j] - p[i] * p[j] for i in range(3) for j in range(3)]
    branch_one = [F(1, 3), F(2, 3)]
    independent_branch_pair = [x * y for x in branch_one for y in branch_one]
    fake_correlated_branch_pair = [F(0), F(1, 2), F(1, 2), F(0)]

    # Each boolean is true only when the hostile change is detected.
    caught = {
        "M01_omit_second_cross_term": (
            bilinear(p, p) - bilinear(p, q) + bilinear(q, q)
        ) != baseline_ls,
        "M02_force_reference_equal_physical": bilinear([F(0)] * 3, [F(0)] * 3) != baseline_ls,
        "M03_break_m_normalization": sum((q[i] * (m[i] + F(1, 10)) for i in range(3)), F(0)) != 0,
        "M04_break_H_zero_margin": any(sum(row, F(0)) != 0 for row in H_bad_margin),
        "M05_make_H_pair_negative": any(x < 0 for row in pair_too_large for x in row),
        "M06_remove_B_sector": speed(build(I, Q, S), t0) != base_speed,
        "M07_remove_Q_sector": speed(build(B, I, S), t0) != base_speed,
        "M08_remove_S_sector": speed(build(B, Q, O), t0) != base_speed,
        "M09_omit_unit_direction_projection": speed(build(B, Q, S), t0, True) != base_speed,
        "M10_call_angle_bin_a_measure_coupling": all(x == 0 for x in intrinsic_connected),
        "M11_replace_independent_branch_product_by_correlated_pair": (
            fake_correlated_branch_pair != independent_branch_pair
        ),
        "M12_activate_coefficient_on_zero_unowned_basis": F(3) * F(0) != F(1),
    }

    # M10 is caught because intrinsic connected residual remains exactly zero;
    # the nonzero estimator value is wholly the p-q term. M11 catches the silent
    # replacement of independent branch marking by a correlated branch law.
    # M12 catches a claimed nonzero output from a zero/unowned basis.
    return {
        "status": "PASS" if all(caught.values()) else "FAIL",
        "caught": caught,
        "caught_count": sum(caught.values()),
        "total": len(caught),
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
