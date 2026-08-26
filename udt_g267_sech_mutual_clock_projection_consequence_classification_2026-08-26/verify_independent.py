#!/usr/bin/env python3
"""Independent exact-rational G267 verification; no production import or result read."""

from __future__ import annotations

from fractions import Fraction
import json


def state_from_half_depth(t: Fraction) -> tuple[Fraction, Fraction]:
    assert -1 < t < 1
    denominator = 1 + t * t
    return (1 - t * t) / denominator, 2 * t / denominator


def compose(
    left: tuple[Fraction, Fraction], right: tuple[Fraction, Fraction]
) -> tuple[Fraction, Fraction]:
    m1, c1 = left
    m2, c2 = right
    denominator = 1 + c1 * c2
    assert denominator > 0
    return m1 * m2 / denominator, (c1 + c2) / denominator


def main() -> None:
    assertions = 0
    values = [Fraction(n, 32) for n in range(-24, 25)]
    states = [state_from_half_depth(value) for value in values]
    for t, (mutual, position) in zip(values, states):
        assert mutual > 0
        assertions += 1
        assert mutual * mutual + position * position == 1
        assertions += 1
        reversed_state = state_from_half_depth(-t)
        assert reversed_state == (mutual, -position)
        assertions += 1
        arrow = (1 - position) / mutual
        assert arrow == (1 - t) / (1 + t)
        assertions += 1
        assert (1 + position) / mutual == 1 / arrow
        assertions += 1
        assert compose((mutual, position), (mutual, -position)) == (Fraction(1), Fraction(0))
        assertions += 1

    pair_cases = 192
    for index in range(pair_cases):
        t1 = values[(7 * index + 3) % len(values)]
        t2 = values[(11 * index + 9) % len(values)]
        left = state_from_half_depth(t1)
        right = state_from_half_depth(t2)
        combined_half_depth = (t1 + t2) / (1 + t1 * t2)
        expected = state_from_half_depth(combined_half_depth)
        actual = compose(left, right)
        assert actual == expected
        assertions += 1
        assert actual[0] * actual[0] + actual[1] * actual[1] == 1
        assertions += 1
        assert compose(left, (Fraction(1), Fraction(0))) == left
        assertions += 1
        t3 = values[(13 * index + 5) % len(values)]
        third = state_from_half_depth(t3)
        assert compose(compose(left, right), third) == compose(left, compose(right, third))
        assertions += 1

    p = Fraction(4, 5)
    q = Fraction(3, 5)
    same = compose((p, q), (p, q))
    opposite = compose((p, q), (p, -q))
    assert same == (Fraction(8, 17), Fraction(15, 17))
    assertions += 1
    assert opposite == (Fraction(1), Fraction(0))
    assertions += 1
    assert same[0] != opposite[0]
    assertions += 1

    gamma = Fraction(5, 4)
    competitors = (1 / gamma, 1 / (gamma * gamma), Fraction(2) / (gamma + 1))
    assert competitors == (Fraction(4, 5), Fraction(16, 25), Fraction(8, 9))
    assertions += 1
    assert len(set(competitors)) == 3
    assertions += 1

    result = {
        "status": "PASS",
        "implementation": "python_fraction_half_depth_parameterization_no_sympy_no_production_import_no_result_read",
        "state_cases": len(states),
        "pair_cases": pair_cases,
        "assertions": assertions,
        "verified": [
            "right-semicircle constraint",
            "reversal parity",
            "signed-arrow reconstruction",
            "identity inverse and associativity",
            "two-channel composition",
            "M-alone noncomposition counterexample",
            "coefficient-free projection nonuniqueness",
        ],
    }
    assert assertions == 1067
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
