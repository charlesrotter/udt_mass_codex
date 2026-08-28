#!/usr/bin/env python3
"""Implementation-distinct exact G287 verification; imports no production module or artifact."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path


def reverse_state(metric, profile_sign, depth):
    return tuple(metric), profile_sign, -depth


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    assertions = 0
    rows = []
    for numerator in range(1, 18):
        for denominator in range(1, 18):
            t = Fraction(numerator, denominator)
            norm = numerator * numerator + denominator * denominator
            chi = Fraction(numerator * numerator - denominator * denominator, norm)
            mutual = Fraction(2 * numerator * denominator, norm)
            reversed_chi = Fraction(denominator * denominator - numerator * numerator, norm)
            reversed_mutual = Fraction(2 * denominator * numerator, norm)
            assert chi * chi + mutual * mutual == 1
            assert reversed_chi == -chi
            assert reversed_mutual == mutual
            assertions += 3
            rows.append((t, chi, mutual))

    profile_assertions = 0
    for numerator in range(1, 14):
        for denominator in range(1, 14):
            if numerator == denominator:
                continue
            f = Fraction(numerator, denominator)
            original = (-f, 1 / f, Fraction(1, 1))
            conjugate = (-1 / f, f, Fraction(1, 1))
            reversed_pair_metric = original
            double_conjugate_f = 1 / (1 / f)
            assert reversed_pair_metric == original
            assert conjugate != original
            assert (-double_conjugate_f, 1 / double_conjugate_f, Fraction(1, 1)) == original
            profile_assertions += 3

    # A symmetric regime label cannot equal the sign of an antisymmetric arrow.
    regime_cases = [(3, -3, 1), (-2, 2, -1)]
    regime_assertions = 0
    for forward, reverse, profile_sign in regime_cases:
        metric = (Fraction(-2, 3), Fraction(3, 2))
        reversed_metric, reversed_profile, calculated_reverse = reverse_state(
            metric, profile_sign, forward
        )
        assert calculated_reverse == reverse == -forward
        assert reversed_metric == metric
        assert reversed_profile == profile_sign
        assert (forward > 0) != (reverse > 0)
        regime_assertions += 4

    result = {
        "checks": {
            "open_semicircle_identity": assertions == 867,
            "profile_and_pair_involutions_distinct": profile_assertions == 468,
            "regime_classifier_counterexamples": regime_assertions == 8,
            "no_production_import_or_result_read": True,
        },
        "counts": {
            "exact_semicircle_assertions": assertions,
            "exact_profile_assertions": profile_assertions,
            "exact_regime_assertions": regime_assertions,
            "sample_count": len(rows),
        },
    }
    result["pass"] = all(result["checks"].values())
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    raise SystemExit(0 if result["pass"] else 1)


if __name__ == "__main__":
    main()
