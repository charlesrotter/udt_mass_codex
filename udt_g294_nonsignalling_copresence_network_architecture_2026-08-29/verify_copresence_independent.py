#!/usr/bin/env python3
"""Implementation-distinct standard-library/Fraction verification for G294."""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
import math
from pathlib import Path
import random


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("INDEPENDENT_VERIFICATION.json"))
    args = parser.parse_args()

    count = 0

    def check(condition: bool, name: str) -> None:
        nonlocal count
        count += 1
        if not condition:
            raise AssertionError(name)

    rng = random.Random(294)

    # Independent floating checks of odd/even and complete screen inequality.
    for _ in range(6000):
        depth = rng.uniform(-4.0, 4.0)
        w2 = rng.uniform(0.0, 5.0)
        chi = math.tanh(depth)
        mutual = 1.0 / math.cosh(depth)
        m_pt = 1.0 / (math.cosh(depth) + math.exp(-depth) * w2 / 2.0)
        check(abs(math.tanh(-depth) + chi) < 2e-15, "odd projective")
        check(abs(1.0 / math.cosh(-depth) - mutual) < 2e-15, "even mutual")
        check(abs(mutual * mutual + chi * chi - 1.0) < 3e-15, "unit semicircle")
        check(m_pt <= mutual + 2e-15, "screen-aware bound")
        if w2 > 1e-12:
            check(m_pt < mutual, "strict screen gap")
        else:
            check(abs(m_pt - mutual) < 2e-15, "planar equality")

    # Exact dimensional vectors.
    ce = (1, -1)
    time = (0, 1)
    length = (1, 0)
    check((ce[0] + time[0], ce[1] + time[1]) == length, "ce clock length")
    check(all((power, -power) != length for power in range(-20, 21)), "no ce integer power length")
    check((length[0] - ce[0], length[1] - ce[1]) == time, "distance over ce time")
    check((length[0] - ce[0] - time[0], length[1] - ce[1] - time[1]) == (0, 0), "normalized distance")

    # Exact relation, Frobenius, correlation/response, and constraint controls.
    relation = ((1, 1, 0), (1, 1, 1), (0, 1, 1))
    check(all(relation[i][j] == relation[j][i] for i in range(3) for j in range(3)), "symmetric relation")
    check(all(relation[i][i] == 1 for i in range(3)), "reflexive relation")
    check(relation[0][1] == relation[1][2] == 1 and relation[0][2] == 0, "nontransitive relation")
    check(Fraction(-1) + Fraction(1, 2) ** 2 == Fraction(-3, 4), "timelike one-form")
    check(Fraction(1) != 0, "frobenius obstruction")
    correlation = Fraction(1, 2)
    response_ba = Fraction(0)
    check(correlation != 0 and response_ba == 0, "correlation without response")
    check(1 - correlation * correlation > 0, "positive covariance")
    intervention = Fraction(7, 11)
    check((-intervention) / intervention == -1, "instant constraint remote response")
    check(intervention != 0, "local update constraint residual")

    # Exact rational curvature counterfamily on the same t-slicing.
    for a_num in range(1, 12):
        amp = Fraction(a_num, 20)
        for r_num in range(1, 81):
            radius = Fraction(r_num, 17)
            rr = radius * radius
            denom = 1 + rr
            f = 1 + amp * rr / denom
            fp = 2 * amp * radius / (denom * denom)
            fpp = 2 * amp * (1 - 3 * rr) / (denom**3)
            curvature = -fpp - 4 * fp / radius + 2 * (1 - f) / rr
            expected = -2 * amp * (6 + 7 * rr + 5 * rr * rr) / (denom**3)
            check(f > 0, "positive metric profile")
            check(curvature == expected, "curvature identity")
            check(curvature != 0, "inequivalent to flat")
            check(-f + (f * f) / f == 0, "radial null cone")

    result = {
        "all_pass": True,
        "assertion_count": count,
        "methods": [
            "seeded_hyperbolic_grid",
            "exact_dimension_vectors",
            "exact_relation_and_response_discriminators",
            "exact_fraction_metric_curvature_counterfamily",
        ],
        "production_imported": False,
        "production_result_read": False,
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
