#!/usr/bin/env python3
"""Dependency-free exact-rational G268 verification; imports no production module/result."""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path
import random


OUT = Path(__file__).with_name("INDEPENDENT_VERIFICATION.json")
LANDING = (
    "FINITE_REGULAR_SECH_STATE_IS_EXACTLY_EQUIVALENT_TO_THE_RECIPROCAL_RELATION_SPACE__"
    "COMPACT_ENDPOINTS_FORM_ONLY_A_PARTIAL_NONGROUP_CLOSURE__"
    "INDEPENDENT_M_WOULD_GIVE_A_CONDITIONAL_CROSS_READOUT_LAW__"
    "NO_RELATION_NETWORK_HISTORY_DISTANCE_OR_XMAX_SELECTION"
)


def state(r: Fraction) -> tuple[Fraction, Fraction]:
    assert r > 0
    return 2 * r / (1 + r * r), (1 - r * r) / (1 + r * r)


def compose(
    a: tuple[Fraction, Fraction], b: tuple[Fraction, Fraction]
) -> tuple[Fraction, Fraction]:
    ma, xa = a
    mb, xb = b
    den = 1 + xa * xb
    assert den > 0
    return ma * mb / den, (xa + xb) / den


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    rng = random.Random(268)
    assertions = 0

    ratios: list[Fraction] = []
    for i in range(1, 1101):
        r = Fraction((37 * i) % 997 + 1, (91 * i) % 991 + 1)
        ratios.append(r)
        m, x = state(r)
        assert m > 0
        assertions += 1
        assert -1 < x < 1
        assertions += 1
        assert m * m + x * x == 1
        assertions += 1
        assert (1 - x) / m == r
        assertions += 1
        assert (1 + x) / m == 1 / r
        assertions += 1
        mi, xi = state(1 / r)
        assert mi == m and xi == -x
        assertions += 2

    composition_cases = 6000
    for _ in range(composition_cases):
        r1 = ratios[rng.randrange(len(ratios))]
        r2 = ratios[rng.randrange(len(ratios))]
        joined = compose(state(r1), state(r2))
        assert joined == state(r1 * r2)
        assertions += 2
        inverse_join = compose(state(r1), state(1 / r1))
        assert inverse_join == (Fraction(1), Fraction(0))
        assertions += 2

    associativity_cases = 2000
    for _ in range(associativity_cases):
        states = [state(ratios[rng.randrange(len(ratios))]) for _ in range(3)]
        assert compose(compose(states[0], states[1]), states[2]) == compose(
            states[0], compose(states[1], states[2])
        )
        assertions += 2

    network_cases = 1200
    edge_checks = 0
    for case in range(network_cases):
        size = 2 + case % 7
        q = [Fraction(rng.randrange(1, 200), rng.randrange(1, 200)) for _ in range(size)]
        states: dict[tuple[int, int], tuple[Fraction, Fraction]] = {}
        for i in range(size):
            for j in range(size):
                states[i, j] = state(q[j] / q[i])
                m, x = states[i, j]
                assert m * m + x * x == 1
                assertions += 1
                edge_checks += 1
        for i in range(size - 2):
            assert compose(states[i, i + 1], states[i + 1, i + 2]) == states[i, i + 2]
            assertions += 2
        for i in range(size):
            assert compose(states[0, i], states[i, 0]) == (Fraction(1), Fraction(0))
            assertions += 2
            reconstructed_ratio = (1 - states[0, i][1]) / states[0, i][0]
            assert reconstructed_ratio == q[i] / q[0]
            assertions += 1

    # An independent M datum can violate the candidate without invalidating r itself.
    off_r = Fraction(2)
    off_m = Fraction(1, 2)
    candidate_m = state(off_r)[0]
    assert candidate_m == Fraction(4, 5)
    assertions += 1
    assert off_m - candidate_m == Fraction(-3, 10)
    assertions += 1

    plus = (Fraction(0), Fraction(1))
    minus = (Fraction(0), Fraction(-1))
    assert 1 + plus[1] * plus[1] == 2
    assertions += 1
    assert 1 + minus[1] * minus[1] == 2
    assertions += 1
    assert 1 + plus[1] * minus[1] == 0
    assertions += 1

    result = {
        "status": "PASS",
        "expected_landing": LANDING,
        "ratio_cases": len(ratios),
        "composition_cases": composition_cases,
        "associativity_cases": associativity_cases,
        "network_cases": network_cases,
        "network_edge_checks": edge_checks,
        "assertions": assertions,
        "regular_relation_rejections": 0,
        "finite_network_rejections": 0,
        "opposite_endpoint_denominator": "0",
        "off_law_residual": "-3/10",
        "production_imported": False,
        "production_result_read": False,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if not args.no_write:
        OUT.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
