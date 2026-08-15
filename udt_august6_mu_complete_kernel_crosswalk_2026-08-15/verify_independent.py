#!/usr/bin/env python3
"""Independent exact-Fraction verification; imports no production derivation code."""

from __future__ import annotations

import json
from fractions import Fraction as F


def zeros(rows: int, cols: int) -> list[list[F]]:
    return [[F(0) for _ in range(cols)] for _ in range(rows)]


def eye(n: int) -> list[list[F]]:
    out = zeros(n, n)
    for i in range(n):
        out[i][i] = F(1)
    return out


def transpose(a: list[list[F]]) -> list[list[F]]:
    return [list(row) for row in zip(*a)]


def add(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def sub(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    return [[x - y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def mul(a: list[list[F]], b: list[list[F]]) -> list[list[F]]:
    bt = transpose(b)
    return [[sum((x * y for x, y in zip(row, col)), F(0)) for col in bt] for row in a]


def inverse(a: list[list[F]]) -> list[list[F]]:
    n = len(a)
    aug = [row[:] + ident[:] for row, ident in zip(a, eye(n))]
    for col in range(n):
        pivot = next(row for row in range(col, n) if aug[row][col] != 0)
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [value / scale for value in aug[col]]
        for row in range(n):
            if row == col:
                continue
            factor = aug[row][col]
            aug[row] = [x - factor * y for x, y in zip(aug[row], aug[col])]
    return [row[n:] for row in aug]


def block(lower_left: list[list[F]], upper_left: list[list[F]], lower_right: list[list[F]]) -> list[list[F]]:
    n_base = len(upper_left)
    n_screen = len(lower_right)
    out = zeros(n_base + n_screen, n_base + n_screen)
    for i in range(n_base):
        for j in range(n_base):
            out[i][j] = upper_left[i][j]
    for i in range(n_screen):
        for j in range(n_base):
            out[n_base + i][j] = lower_left[i][j]
        for j in range(n_screen):
            out[n_base + i][n_base + j] = lower_right[i][j]
    return out


def trace(a: list[list[F]]) -> F:
    return sum((a[i][i] for i in range(len(a))), F(0))


def det3(a: list[list[F]]) -> F:
    return (
        a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
        - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
        + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0])
    )


def inv2_coefficient(a: list[list[F]]) -> F:
    return (trace(a) ** 2 - trace(mul(a, a))) / 2


def pair_metric(b: list[list[F]], q: list[list[F]], s: list[list[F]], y: list[list[F]], z: list[list[F]]) -> list[list[F]]:
    eta2 = [[F(-1), F(0)], [F(0), F(1)]]
    u = mul(b, y)
    screen_leg = add(mul(s, y), z)
    a = mul(q, screen_leg)
    return add(mul(mul(transpose(u), eta2), u), mul(transpose(a), a))


def main() -> None:
    a, r, screen_scale, mu = F(1, 2), F(2), F(3), F(1, 4)
    eta3 = [[F(-1), F(0), F(0)], [F(0), F(1), F(0)], [F(0), F(0), F(1)]]
    upper = [[a, F(0), mu], [F(0), r, F(0)], [F(0), F(0), screen_scale]]
    lower = mul(mul(eta3, transpose(upper)), eta3)
    expected_lower = [[a, F(0), F(0)], [F(0), r, F(0)], [-mu, F(0), screen_scale]]
    cu = mul(lower, upper)
    cl = mul(upper, lower)

    b = [[a, F(0)], [F(0), r]]
    q = [[screen_scale]]
    modern_s = [[-mu / screen_scale, F(0)]]
    modern_e = block(mul(q, modern_s), b, q)
    y = eye(2)
    z = [[F(0), F(0)]]
    h = pair_metric(b, q, modern_s, y, z)

    # Same terminal h for two different full arrows with fixed physical lower mixing mu.
    screen_scale_2 = F(4)
    q2 = [[screen_scale_2]]
    modern_s2 = [[-mu / screen_scale_2, F(0)]]
    h2 = pair_metric(b, q2, modern_s2, y, z)
    upper2 = [[a, F(0), mu], [F(0), r, F(0)], [F(0), F(0), screen_scale_2]]
    lower2 = mul(mul(eta3, transpose(upper2)), eta3)
    cu2 = mul(lower2, upper2)

    # General 2+2 endpoint transition, independently evaluated with dense rational matrices.
    bp = [[F(2), F(1)], [F(1), F(1)]]
    bq = [[F(3), F(1)], [F(1), F(2)]]
    qp = [[F(1), F(1, 3)], [F(1, 2), F(2)]]
    qq = [[F(2), F(1, 4)], [F(1, 5), F(3)]]
    sp = [[F(1, 7), F(-1, 8)], [F(2, 9), F(1, 6)]]
    sq = [[F(-1, 5), F(3, 10)], [F(1, 11), F(-2, 7)]]
    ep = block(mul(qp, sp), bp, qp)
    eq = block(mul(qq, sq), bq, qq)
    direct_transition = mul(eq, inverse(ep))
    expected_transition = block(
        mul(mul(qq, sub(sq, sp)), inverse(bp)),
        mul(bq, inverse(bp)),
        mul(qq, inverse(qp)),
    )

    # Exact pullback fiber with a nonzero change in both mixing entries.
    d = [[F(2, 5), F(-3, 7)]]
    z0 = [[F(1, 9), F(4, 11)]]
    h_before = pair_metric(b, q, modern_s, y, z0)
    h_after = pair_metric(b, q, add(modern_s, d), y, sub(z0, mul(d, y)))

    # Rank-one slice does not select an extension to rank-two mixing.
    u = F(5, 6)
    p_restricted = [[mu * mu, F(0)], [F(0), F(0)]]
    p_rank_two = [[mu * mu, F(0)], [F(0), u * u]]
    f0_restricted = trace(p_restricted)
    f1_restricted = trace(p_restricted) + p_restricted[0][0] * p_restricted[1][1]
    f0_rank_two = trace(p_rank_two)
    f1_rank_two = trace(p_rank_two) + p_rank_two[0][0] * p_rank_two[1][1]

    checks = {
        "adjoint_lower_crosswalk": lower == expected_lower == modern_e,
        "strain_character_data_match": (
            trace(cu) == trace(cl)
            and inv2_coefficient(cu) == inv2_coefficient(cl)
            and det3(cu) == det3(cl)
        ),
        "august_numeric_invariants": (
            trace(cu) == r * r + F(1, r * r) + screen_scale * screen_scale - mu * mu
            and det3(cu) == screen_scale * screen_scale
        ),
        "base_pair_h_expected": h == [[-a * a + mu * mu, F(0)], [F(0), r * r]],
        "same_h_different_screen_arrow": h == h2 and trace(cu) != trace(cu2),
        "general_transition_formula": direct_transition == expected_transition,
        "pullback_fiber_exact": h_before == h_after,
        "restricted_extensions_agree": f0_restricted == f1_restricted == mu * mu,
        "rank_two_extensions_differ": f1_rank_two - f0_rank_two == mu * mu * u * u,
    }
    result = {
        "all_checks_pass": all(checks.values()),
        "checks": checks,
        "exact_witness": {
            "h": [[str(x) for x in row] for row in h],
            "old_trace_s3": str(trace(cu)),
            "old_trace_s4": str(trace(cu2)),
            "same_terminal_h": h == h2,
            "rank_two_extension_gap": str(f1_rank_two - f0_rank_two),
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
