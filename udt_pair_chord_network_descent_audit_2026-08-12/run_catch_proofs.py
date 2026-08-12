#!/usr/bin/env python3
"""Fail-closed controls for chord-network category errors."""

from __future__ import annotations

import json
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def h(x):
    T, L, b = x
    return (-T * T, -T * T * b, L * L - T * T * b * b)


def diff(x, y):
    a, b = h(x), h(y)
    return b[0] - a[0], b[1] - a[1], b[2] - a[2]


def rank_psd(p):
    a, m, n = p
    d = a * n - m * m
    if a < 0 or n < 0 or d < 0:
        return -1
    if a == m == n == 0:
        return 0
    return 1 if d == 0 else 2


def arrow(x, y):
    Ti, Li, bi = x
    Tj, Lj, bj = y
    return Tj / Ti, Tj * (bj - bi) / Li, Lj / Li


def compose(left, right):
    e, f, g = left
    a, b, d = right
    return e * a, e * b + f * d, g * d


def inverse(r):
    a, b, d = r
    return F(1) / a, -b / (a * d), F(1) / d


def main():
    A = (F(4), F(1), F(0))
    B = (F(3), F(2), F(0))
    C = (F(2), F(4), F(1, 2))
    catches = {}

    catches["PSD_order_is_not_reciprocity"] = rank_psd(diff(A, B)) > 0 and rank_psd(diff(B, A)) < 0

    r_ab = arrow(A, B)
    r_ba = arrow(B, A)
    catches["calibrated_transition_does_reverse"] = compose(r_ba, r_ab) == (F(1), F(0), F(1)) and inverse(r_ab) == r_ba

    r_bc = arrow(B, C)
    r_ac = arrow(A, C)
    catches["matched_middle_composes"] = compose(r_bc, r_ab) == r_ac
    catches["upper_shear_is_not_additive"] = r_ac[1] != r_ab[1] + r_bc[1]

    reciprocal = lambda r: r[0] / r[2]
    catches["reciprocal_character_composes"] = reciprocal(r_ac) == reciprocal(r_bc) * reciprocal(r_ab)
    catches["raw_beta_difference_telescopes_only_in_common_calibration"] = (
        (B[2] - A[2]) + (C[2] - B[2]) == C[2] - A[2]
        and r_ac[1] != C[2] - A[2]
    )

    Bin = (F(3), F(2), F(1, 3))
    Bout = (F(5, 2), F(3), F(-1, 2))
    D = (F(1), F(5), F(1))
    with_middle = compose(arrow(Bout, D), compose(arrow(Bin, Bout), arrow(A, Bin)))
    without_middle = compose(arrow(Bout, D), arrow(A, Bin))
    catches["independent_middle_transition_required"] = with_middle == arrow(A, D) and without_middle != arrow(A, D)

    p_same_1, p_same_2 = (F(1), F(0), F(0)), (F(2), F(0), F(0))
    p_diff = (F(0), F(0), F(1))
    add = lambda p, q: tuple(p[i] + q[i] for i in range(3))
    catches["rank1_same_direction_stays_rank1"] = rank_psd(add(p_same_1, p_same_2)) == 1
    catches["rank1_distinct_directions_make_rank2"] = rank_psd(add(p_same_1, p_diff)) == 2

    p = (F(1), F(0), F(1))
    catches["nontrivial_PSD_loop_impossible"] = rank_psd(p) == 2 and rank_psd(tuple(-x for x in p)) < 0

    # The chosen A clock can become null while the two-form remains Lorentzian.
    h_clock_null = ((F(0), F(1)), (F(1), F(10)))
    catches["A_chart_boundary_not_geometric_or_Xmax_boundary"] = (
        h_clock_null[0][0] == 0
        and h_clock_null[0][0] * h_clock_null[1][1] - h_clock_null[0][1] ** 2 < 0
    )

    assert all(catches.values()), catches
    result = {"status": "PASS", "catch_count": len(catches), "catches": catches}
    (ROOT / "CATCH_PROOFS.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
