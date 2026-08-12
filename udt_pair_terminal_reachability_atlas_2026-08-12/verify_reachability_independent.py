#!/usr/bin/env python3
"""Hermetic stdlib Fraction replay; imports no production module or artifact."""

from __future__ import annotations

import itertools
import json
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def matmul(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)) for i in range(2))


def transpose(a):
    return ((a[0][0], a[1][0]), (a[0][1], a[1][1]))


def add(a, b):
    return tuple(tuple(a[i][j] + b[i][j] for j in range(2)) for i in range(2))


def det(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def classify_signature(h):
    value = det(h)
    if value < 0:
        return "LORENTZIAN"
    if value == 0:
        return "DEGENERATE"
    assert h[1][1] > 0
    return "POSITIVE_DEFINITE"


def shifted_to_original_gram(p, m, n, beta0):
    return (
        (p, p * beta0 + m),
        (p * beta0 + m, p * beta0 * beta0 + 2 * beta0 * m + n),
    )


def original_base(t, ell, beta0):
    return (
        (-t, -t * beta0),
        (-t * beta0, ell - t * beta0 * beta0),
    )


def terminal_from_original(h):
    assert h[0][0] < 0 and det(h) < 0
    T2 = -h[0][0]
    beta = h[0][1] / h[0][0]
    L2 = h[1][1] - h[0][1] * h[0][1] / h[0][0]
    assert T2 > 0 and L2 > 0 and det(h) == -T2 * L2
    return T2, L2, beta


def reconstruct_shifted_gram(t, ell, beta0, T2, L2, beta):
    delta = beta - beta0
    return (
        (t - T2, -T2 * delta),
        (-T2 * delta, L2 - ell - T2 * delta * delta),
    )


def rank_psd(p, m, n):
    assert p >= 0 and n >= 0 and m * m <= p * n
    if p == 0 and m == 0 and n == 0:
        return 0
    return 1 if p * n == m * m else 2


def replay_forward_cases():
    # Verification controls are dimensionless rational probes, not physical values.
    t, ell, beta0 = F(9), F(4), F(-3, 5)
    entries = [F(-3, 2), F(-1), F(-1, 3), F(0), F(1, 3), F(1), F(3, 2)]
    grams = set()
    for a, c, d, e in itertools.product(entries, repeat=4):
        grams.add((a * a + c * c, a * d + c * e, d * d + e * e))
    grams.update(
        {
            (F(9), F(0), F(1)),
            (F(9), F(3), F(2)),
            (F(10), F(0), F(5)),
            (F(10), F(3), F(5)),
            (F(10), F(7), F(5)),
            (F(10), F(5), F(5)),
        }
    )

    counts = {"cases": 0, "terminal": 0, "nonterminal": 0, "rank0": 0, "rank1": 0, "rank2": 0,
              "LORENTZIAN": 0, "DEGENERATE": 0, "POSITIVE_DEFINITE": 0}
    h0 = original_base(t, ell, beta0)
    for p, m, n in sorted(grams):
        rank = rank_psd(p, m, n)
        gram_original = shifted_to_original_gram(p, m, n, beta0)
        h = add(h0, gram_original)
        expected_det = (p - t) * (ell + n) - m * m
        assert det(h) == expected_det
        label = classify_signature(h)
        counts["cases"] += 1
        counts[f"rank{rank}"] += 1
        counts[label] += 1
        if p < t:
            counts["terminal"] += 1
            T2, L2, beta = terminal_from_original(h)
            assert T2 == t - p
            assert beta - beta0 == -m / T2
            assert L2 == ell + n + m * m / T2
            reconstructed = reconstruct_shifted_gram(t, ell, beta0, T2, L2, beta)
            assert reconstructed == ((p, m), (m, n))
            lhs = (t - T2) * (L2 - ell)
            rhs = t * T2 * (beta - beta0) ** 2
            assert lhs >= rhs and T2 <= t and L2 >= ell
        else:
            counts["nonterminal"] += 1
    return counts


def replay_inverse_targets():
    t, ell, beta0 = F(9), F(4), F(-3, 5)
    T2_values = [F(1, 4), F(1), F(9, 4), F(4), F(25, 4), F(8), F(9)]
    L2_values = [F(4), F(5), F(8), F(13), F(25), F(49)]
    deltas = [F(-2), F(-1), F(-1, 2), F(0), F(1, 2), F(1), F(2)]
    checked = 0
    equality = 0
    strict = 0
    for T2, L2, delta in itertools.product(T2_values, L2_values, deltas):
        lhs = (t - T2) * (L2 - ell)
        rhs = t * T2 * delta * delta
        if not (0 < T2 <= t and L2 >= ell and lhs >= rhs):
            continue
        beta = beta0 + delta
        gram = reconstruct_shifted_gram(t, ell, beta0, T2, L2, beta)
        p, m, n = gram[0][0], gram[0][1], gram[1][1]
        rank_psd(p, m, n)
        h = add(original_base(t, ell, beta0), shifted_to_original_gram(p, m, n, beta0))
        assert terminal_from_original(h) == (T2, L2, beta)
        assert det(h) == -T2 * L2
        checked += 1
        if lhs == rhs:
            equality += 1
            assert rank_psd(p, m, n) in (0, 1)
        else:
            strict += 1
            assert rank_psd(p, m, n) == 2
    assert checked >= 100 and equality > 0 and strict > 0
    return {"cases": checked, "rank_boundary": equality, "rank_interior": strict}


def boundary_controls():
    t, ell = F(9), F(4)
    controls = {
        "base": (F(0), F(0), F(0)),
        "pure_clock_rank1": (F(1), F(0), F(0)),
        "pure_ruler_rank1": (F(0), F(0), F(1)),
        "mixed_rank1": (F(1), F(2), F(4)),
        "rank2": (F(2), F(1), F(3)),
        "clock_null_degenerate": (F(9), F(0), F(1)),
        "clock_null_lorentzian": (F(9), F(3), F(2)),
        "outside_chart_positive": (F(10), F(0), F(5)),
        "outside_chart_degenerate": (F(10), F(3), F(5)),
        "outside_chart_lorentzian": (F(10), F(5), F(5)),
    }
    result = {}
    for name, (p, m, n) in controls.items():
        rank_psd(p, m, n)
        h = ((p - t, m), (m, ell + n))
        result[name] = {"signature": classify_signature(h), "terminal": p < t}
    assert result["clock_null_degenerate"]["signature"] == "DEGENERATE"
    assert result["clock_null_lorentzian"]["signature"] == "LORENTZIAN"
    assert result["outside_chart_positive"]["signature"] == "POSITIVE_DEFINITE"
    assert result["outside_chart_degenerate"]["signature"] == "DEGENERATE"
    assert result["outside_chart_lorentzian"]["signature"] == "LORENTZIAN"
    return result


def covariance_controls():
    h = ((F(-3), F(2)), (F(2), F(5)))
    change = ((F(1), F(2)), (F(1), F(3)))
    transformed = matmul(transpose(change), matmul(h, change))
    assert det(transformed) == det(change) ** 2 * det(h)

    screen = ((F(2), F(1)), (F(0), F(1)))
    relative = ((F(1), F(2)), (F(-1), F(3)))
    rotation = ((F(0), F(-1)), (F(1), F(0)))
    original_factor = matmul(screen, relative)
    rotated_factor = matmul(rotation, original_factor)
    original_gram = matmul(transpose(original_factor), original_factor)
    rotated_gram = matmul(transpose(rotated_factor), rotated_factor)
    assert original_gram == rotated_gram
    return {"pair_congruence": True, "screen_rotation": True}


def main():
    forward = replay_forward_cases()
    inverse = replay_inverse_targets()
    boundaries = boundary_controls()
    covariance = covariance_controls()
    required = ["LORENTZIAN", "DEGENERATE", "POSITIVE_DEFINITE", "rank0", "rank1", "rank2"]
    assert forward["cases"] >= 250 and all(forward[key] > 0 for key in required)
    result = {
        "status": "INDEPENDENT_EXACT_FRACTION_REPLAY_PASS",
        "implementation": "stdlib Fraction; no production imports or artifact reads",
        "forward": forward,
        "inverse": inverse,
        "boundary_controls": boundaries,
        "covariance_controls": covariance,
    }
    (ROOT / "INDEPENDENT_VERIFICATION.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
