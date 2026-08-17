#!/usr/bin/env python3
"""Independent Fraction/finite-jet replay for G131."""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def bilinear(metric, left, right):
    return sum(metric[i][j] * left[i] * right[j] for i in range(4) for j in range(4))


def q(metric, clock, ruler):
    aa = bilinear(metric, clock, clock)
    ab = bilinear(metric, clock, ruler)
    bb = bilinear(metric, ruler, ruler)
    return (ab * ab - aa * bb) / (aa * aa)


def scaled(metric, factor):
    return [[factor * metric[i][j] for j in range(4)] for i in range(4)]


def candidate(a, b):
    spatial = [[b[i] * b[j] / a - (a if i == j else 0) for j in range(3)] for i in range(3)]
    return [[a, *b]] + [[b[i], *spatial[i]] for i in range(3)]


def q_derivative(metric, clock, velocity, ruler):
    aa = bilinear(metric, clock, clock)
    ab = bilinear(metric, clock, ruler)
    bb = bilinear(metric, ruler, ruler)
    daa = 2 * bilinear(metric, velocity, clock)
    dab = bilinear(metric, velocity, ruler)
    numerator = ab * ab - aa * bb
    return (2 * ab * dab - daa * bb) / (aa * aa) - 2 * numerator * daa / (aa * aa * aa)


def scalar_from_jet(metric, first, second):
    n = 4
    inverse = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        inverse[i][i] = 1 / metric[i][i]
    derivative_inverse = [[[Fraction(0) for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                derivative_inverse[k][i][j] = -sum(
                    inverse[i][p] * first[k][p][q_] * inverse[q_][j]
                    for p in range(n) for q_ in range(n)
                )
    gamma = [[[Fraction(0) for _ in range(n)] for _ in range(n)] for _ in range(n)]
    derivative_gamma = [[[[Fraction(0) for _ in range(n)] for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for upper in range(n):
        for i in range(n):
            for j in range(n):
                gamma[upper][i][j] = Fraction(1, 2) * sum(
                    inverse[upper][ell]
                    * (first[i][ell][j] + first[j][ell][i] - first[ell][i][j])
                    for ell in range(n)
                )
                for k in range(n):
                    derivative_gamma[k][upper][i][j] = Fraction(1, 2) * sum(
                        derivative_inverse[k][upper][ell]
                        * (first[i][ell][j] + first[j][ell][i] - first[ell][i][j])
                        + inverse[upper][ell]
                        * (
                            second[k][i][ell][j]
                            + second[k][j][ell][i]
                            - second[k][ell][i][j]
                        )
                        for ell in range(n)
                    )
    ricci = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            ricci[i][j] = sum(
                derivative_gamma[k][k][i][j]
                - derivative_gamma[j][k][i][k]
                + sum(
                    gamma[k][k][ell] * gamma[ell][i][j]
                    - gamma[k][j][ell] * gamma[ell][i][k]
                    for ell in range(n)
                )
                for k in range(n)
            )
    return sum(inverse[i][j] * ricci[i][j] for i in range(n) for j in range(n))


def main() -> None:
    zero = Fraction(0)
    eta = [
        [Fraction(-1), zero, zero, zero],
        [zero, Fraction(1), zero, zero],
        [zero, zero, Fraction(1), zero],
        [zero, zero, zero, Fraction(1)],
    ]
    e0 = [Fraction(1), zero, zero, zero]
    a = Fraction(-2)
    b = [Fraction(1), Fraction(2), Fraction(-1)]
    shifted = candidate(a, b)
    rulers = [
        [zero, Fraction(1), zero, zero],
        [zero, zero, Fraction(1), zero],
        [zero, Fraction(2), Fraction(-1), Fraction(3)],
    ]
    fixed_matches = all(q(shifted, e0, ruler) == q(eta, e0, ruler) for ruler in rulers)

    derivative_matches = []
    derivative_nonzero = []
    for index in range(3):
        spatial = [Fraction(int(j == index)) for j in range(3)]
        vector = [zero, *spatial]
        got = q_derivative(shifted, e0, vector, vector)
        expected = -4 * b[index] / a
        derivative_matches.append(got == expected)
        derivative_nonzero.append(got != 0)

    samples = [
        ([Fraction(1), Fraction(1, 10), zero, zero], [zero, Fraction(1), Fraction(2), zero]),
        ([Fraction(2), zero, Fraction(1, 5), zero], [zero, Fraction(3), zero, Fraction(1)]),
        ([Fraction(1), zero, zero, Fraction(1, 7)], [zero, Fraction(-2), Fraction(1), Fraction(4)]),
    ]
    conformal = scaled(eta, Fraction(7, 3))
    conformal_matches = all(q(conformal, t, r) == q(eta, t, r) for t, r in samples)
    complete_pullback_differs = conformal != eta

    # Direct finite-jet curvature of (1+x^2)^2 eta at x=0.
    first = [[[zero for _ in range(4)] for _ in range(4)] for _ in range(4)]
    second = [[[[zero for _ in range(4)] for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for i in range(4):
        second[1][1][i][i] = 4 * eta[i][i]
    conformal_curvature_origin = scalar_from_jet(eta, first, second)

    nonconformal_tilt = [Fraction(1), Fraction(1, 10), zero, zero]
    nonconformal_ruler = [zero, Fraction(1), zero, zero]
    tilted_mismatch = q(shifted, nonconformal_tilt, nonconformal_ruler) != q(
        eta, nonconformal_tilt, nonconformal_ruler
    )

    checks = {
        "independent_fixed_clock_nonconformal_family_matches": fixed_matches,
        "independent_three_tilt_derivatives_match_formula": all(derivative_matches),
        "independent_three_nonzero_shift_components_detected": all(derivative_nonzero),
        "independent_tilted_clock_breaks_nonconformal_match": tilted_mismatch,
        "independent_positive_conformal_scaling_matches_all_samples": conformal_matches,
        "independent_conformal_metrics_have_different_full_pullbacks": complete_pullback_differs,
        "independent_nonconstant_conformal_curvature_minus_twelve": conformal_curvature_origin == -12,
        "independent_scalar_ratio_has_no_absolute_scale_slot": q(scaled(eta, 11), *samples[0]) == q(eta, *samples[0]),
    }
    if not all(checks.values()):
        raise SystemExit(f"failed independent checks: {[key for key, value in checks.items() if not value]}")
    result = {
        "status": "PASS",
        "landing": "ALL_PLANE_TERMINAL_SCALAR_CONFORMAL_FAITHFUL_ONLY__COMMON_SCALE_OPEN",
        "independent_check_count": len(checks),
        "checks": checks,
        "conformal_curvature_at_origin": str(conformal_curvature_origin),
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
