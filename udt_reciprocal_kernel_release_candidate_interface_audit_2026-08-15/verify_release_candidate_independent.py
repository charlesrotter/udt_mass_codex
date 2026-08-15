#!/usr/bin/env python3
"""Independent exact-Fraction/Decimal replay; imports no primary derivation code."""

from __future__ import annotations

import json
from decimal import Decimal, getcontext
from fractions import Fraction as F
from typing import TypeVar


T = TypeVar("T")
getcontext().prec = 90


def zeros(rows: int, cols: int, zero: T) -> list[list[T]]:
    return [[zero for _ in range(cols)] for _ in range(rows)]


def eye(n: int, zero: T, one: T) -> list[list[T]]:
    out = zeros(n, n, zero)
    for i in range(n):
        out[i][i] = one
    return out


def transpose(a: list[list[T]]) -> list[list[T]]:
    return [list(row) for row in zip(*a)]


def add(a: list[list[T]], b: list[list[T]]) -> list[list[T]]:
    return [[x + y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def sub(a: list[list[T]], b: list[list[T]]) -> list[list[T]]:
    return [[x - y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def mul(a: list[list[T]], b: list[list[T]]) -> list[list[T]]:
    bt = transpose(b)
    return [[sum((x * y for x, y in zip(row, col)), row[0] * 0) for col in bt] for row in a]


def inverse(a: list[list[T]]) -> list[list[T]]:
    n = len(a)
    zero = a[0][0] * 0
    one = zero + 1
    aug = [row[:] + ident[:] for row, ident in zip(a, eye(n, zero, one))]
    for col in range(n):
        pivot = next(row for row in range(col, n) if aug[row][col] != zero)
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [value / scale for value in aug[col]]
        for row in range(n):
            if row == col:
                continue
            factor = aug[row][col]
            aug[row] = [x - factor * y for x, y in zip(aug[row], aug[col])]
    return [row[n:] for row in aug]


def block(upper_left: list[list[F]], lower_left: list[list[F]], lower_right: list[list[F]]) -> list[list[F]]:
    out = zeros(4, 4, F(0))
    for i in range(2):
        for j in range(2):
            out[i][j] = upper_left[i][j]
            out[2 + i][j] = lower_left[i][j]
            out[2 + i][2 + j] = lower_right[i][j]
    return out


def vstack(top: list[list[F]], bottom: list[list[F]]) -> list[list[F]]:
    return top + bottom


def states() -> list[dict[str, list[list[F]]]]:
    return [
        {
            "B": [[F(2), F(1, 3)], [F(0), F(3, 2)]],
            "Q": [[F(3, 2), F(1, 5)], [F(0), F(4, 3)]],
            "S": [[F(1, 5), -F(1, 7)], [F(2, 9), F(1, 6)]],
            "Y": [[F(1), F(1, 10)], [-F(1, 8), F(1)]],
            "Z": [[F(1, 12), -F(1, 11)], [F(1, 13), F(1, 14)]],
        },
        {
            "B": [[F(9, 5), -F(1, 4)], [F(0), F(8, 5)]],
            "Q": [[F(7, 5), -F(1, 6)], [F(0), F(5, 4)]],
            "S": [[-F(1, 6), F(2, 11)], [F(1, 8), -F(1, 5)]],
            "Y": [[F(9, 10), -F(1, 9)], [F(1, 7), F(11, 10)]],
            "Z": [[-F(1, 15), F(1, 12)], [F(1, 10), -F(1, 16)]],
        },
        {
            "B": [[F(11, 5), F(2, 7)], [F(0), F(7, 5)]],
            "Q": [[F(5, 4), F(1, 7)], [F(0), F(3, 2)]],
            "S": [[F(2, 9), F(1, 10)], [-F(1, 6), F(2, 13)]],
            "Y": [[F(11, 10), F(1, 12)], [-F(1, 9), F(9, 10)]],
            "Z": [[F(1, 18), F(1, 13)], [-F(1, 11), F(1, 17)]],
        },
    ]


ETA2 = [[F(-1), F(0)], [F(0), F(1)]]
ETA4 = [[F(-1), F(0), F(0), F(0)], [F(0), F(1), F(0), F(0)], [F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)]]
E00 = [[F(1), F(0)], [F(0), F(0)]]
ZERO2 = [[F(0), F(0)], [F(0), F(0)]]


def coframe(state: dict[str, list[list[F]]]) -> list[list[F]]:
    return block(state["B"], mul(state["Q"], state["S"]), state["Q"])


def jacobian(state: dict[str, list[list[F]]]) -> list[list[F]]:
    return vstack(state["Y"], state["Z"])


def pair_metric(state: dict[str, list[list[F]]]) -> tuple[list[list[F]], list[list[F]]]:
    b, q, s, y, z = (state[key] for key in ("B", "Q", "S", "Y", "Z"))
    u = mul(b, y)
    a = mul(q, add(mul(s, y), z))
    factored = add(mul(mul(transpose(u), ETA2), u), mul(transpose(a), a))
    e, j = coframe(state), jacobian(state)
    direct = mul(mul(mul(mul(transpose(j), transpose(e)), ETA4), e), j)
    return factored, direct


def det2(h: list[list[F]]) -> F:
    return h[0][0] * h[1][1] - h[0][1] * h[1][0]


def terminal_data(h: list[list[F]]) -> dict[str, F]:
    t2 = -h[0][0]
    beta = h[0][1] / h[0][0]
    l2 = h[1][1] - h[0][1] * h[0][1] / h[0][0]
    return {"T2": t2, "L2": l2, "beta": beta, "ceff2": t2 / l2, "opz4": l2 / t2}


def dphi_for_channel(state: dict[str, list[list[F]]], channel: str) -> tuple[list[list[F]], F]:
    b, q, s, y, z = (state[key] for key in ("B", "Q", "S", "Y", "Z"))
    db = E00 if channel == "B" else ZERO2
    dq = E00 if channel == "Q" else ZERO2
    ds = E00 if channel == "S" else ZERO2
    dy = E00 if channel == "Y" else ZERO2
    dz = E00 if channel == "Z" else ZERO2
    u = mul(b, y)
    rleg = add(mul(s, y), z)
    a = mul(q, rleg)
    du = add(mul(db, y), mul(b, dy))
    dr = add(add(mul(ds, y), mul(s, dy)), dz)
    da = add(mul(dq, rleg), mul(q, dr))
    dh = add(add(mul(mul(transpose(du), ETA2), u), mul(mul(transpose(u), ETA2), du)), add(mul(transpose(da), a), mul(transpose(a), da)))
    h = pair_metric(state)[0]
    hinv = inverse(h)
    tr = mul(hinv, dh)[0][0] + mul(hinv, dh)[1][1]
    value = tr / 4 - dh[0][0] / (2 * h[0][0])
    return dh, value


def decimal(value: F) -> Decimal:
    return Decimal(value.numerator) / Decimal(value.denominator)


def terminal_b_decimal(data: dict[str, F]) -> list[list[Decimal]]:
    t = decimal(data["T2"]).sqrt()
    l = decimal(data["L2"]).sqrt()
    beta = decimal(data["beta"])
    return [[t, t * beta], [Decimal(0), l]]


def max_abs(a: list[list[Decimal]]) -> Decimal:
    return max(abs(value) for row in a for value in row)


def main() -> None:
    ss = states()
    es = [coframe(state) for state in ss]
    metrics = [pair_metric(state) for state in ss]
    hs = [item[0] for item in metrics]
    terminal = [terminal_data(h) for h in hs]
    regular = [h[0][0] < 0 and det2(h) < 0 for h in hs]

    a01 = mul(es[1], inverse(es[0]))
    a12 = mul(es[2], inverse(es[1]))
    a02 = mul(es[2], inverse(es[0]))

    bp = [terminal_b_decimal(data) for data in terminal]
    r01 = mul(bp[1], inverse(bp[0]))
    r12 = mul(bp[2], inverse(bp[1]))
    r02 = mul(bp[2], inverse(bp[0]))
    terminal_composition_residual = max_abs(sub(mul(r12, r01), r02))
    terminal_reversal_residual = max_abs(sub(inverse(r01), mul(bp[0], inverse(bp[1]))))

    sensitivities = {}
    for channel in ("B", "Q", "S", "Y", "Z"):
        dh, value = dphi_for_channel(ss[0], channel)
        sensitivities[channel] = {"dh_nonzero": dh != ZERO2, "dphi": str(value), "dphi_nonzero": value != 0}

    d = [[F(2, 5), F(1, 11)], [-F(1, 13), F(3, 7)]]
    alt = {key: [row[:] for row in value] for key, value in ss[1].items()}
    alt["S"] = add(ss[1]["S"], d)
    alt["Z"] = sub(ss[1]["Z"], mul(d, ss[1]["Y"]))
    h_alt = pair_metric(alt)[0]
    e_alt = coframe(alt)
    a01_alt = mul(e_alt, inverse(es[0]))

    ceff2_ratio_01 = terminal[1]["ceff2"] / terminal[0]["ceff2"]
    ceff2_ratio_12 = terminal[2]["ceff2"] / terminal[1]["ceff2"]
    ceff2_ratio_02 = terminal[2]["ceff2"] / terminal[0]["ceff2"]

    checks = {
        "three_states_regular": all(regular),
        "direct_factored_metrics_equal": all(factored == direct for factored, direct in metrics),
        "ambient_composition_exact": mul(a12, a01) == a02,
        "ambient_reversal_exact": inverse(a01) == mul(es[0], inverse(es[1])),
        "terminal_composition_high_precision": terminal_composition_residual < Decimal("1e-75"),
        "terminal_reversal_high_precision": terminal_reversal_residual < Decimal("1e-75"),
        "terminal_character_exact": ceff2_ratio_12 * ceff2_ratio_01 == ceff2_ratio_02,
        "redshift_ceff_squared_identity_exact": all(data["ceff2"] * data["opz4"] == 1 for data in terminal),
        "all_channel_dh_nonzero": all(value["dh_nonzero"] for value in sensitivities.values()),
        "all_channel_dphi_nonzero": all(value["dphi_nonzero"] for value in sensitivities.values()),
        "SZ_fiber_preserves_h_exact": h_alt == hs[1],
        "SZ_fiber_changes_ambient_transition": a01_alt != a01,
    }
    result = {
        "all_checks_pass": all(checks.values()),
        "checks": checks,
        "regular": regular,
        "sensitivities": sensitivities,
        "terminal_composition_residual": str(terminal_composition_residual),
        "terminal_reversal_residual": str(terminal_reversal_residual),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
