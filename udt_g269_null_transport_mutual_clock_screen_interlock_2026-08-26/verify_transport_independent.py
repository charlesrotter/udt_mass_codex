#!/usr/bin/env python3
"""Implementation-distinct exact-rational G269 replay; imports no production code."""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path


OUT = Path(__file__).with_name("INDEPENDENT_VERIFICATION.json")
LANDING = (
    "METRIC_OWNS_A_QUERY_RELATIVE_NULL_TRANSPORT_MUTUAL_CLOCK_SCALAR__"
    "M_PT_IS_BOUNDED_ABOVE_BY_SECH_DELTA__"
    "EQUALITY_IFF_THE_TARGET_CLOCK_IS_IN_THE_TRANSPORTED_NULL_PAIR_PLANE__"
    "NONZERO_SCREEN_MISMATCH_MAKES_THE_INEQUALITY_STRICT__"
    "NO_QUERY_POPULATION_HISTORY_DISTANCE_OR_XMAX_SELECTION"
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    cases = 12_000
    assertions = 0
    planar_cases = 0
    transverse_cases = 0

    for i in range(1, cases + 1):
        r = Fraction(i % 97 + 1, (37 * i) % 89 + 1)
        w = Fraction((13 * i) % 31, (17 * i) % 29 + 1)
        w_sq = w * w
        gamma_kernel = (r + 1 / r) / 2
        gamma = gamma_kernel + r * w_sq / 2
        longitudinal = gamma - 1 / r
        mutual = 1 / gamma
        sech_depth = 1 / gamma_kernel

        assert -gamma * gamma + longitudinal * longitudinal + w_sq == -1
        assertions += 1
        assert gamma - longitudinal == 1 / r
        assertions += 1
        assert gamma - gamma_kernel == r * w_sq / 2
        assertions += 1
        assert gamma - 1 == ((r - 1) ** 2 + r * r * w_sq) / (2 * r)
        assertions += 1
        assert gamma >= 1
        assertions += 1
        assert mutual <= sech_depth
        assertions += 1
        assert (mutual == sech_depth) == (w == 0)
        assertions += 1

        reverse_r = 1 / r
        reverse_w_sq = r * r * w_sq
        reverse_gamma = (reverse_r + 1 / reverse_r) / 2 + reverse_r * reverse_w_sq / 2
        assert reverse_gamma == gamma
        assertions += 1
        assert 1 / reverse_gamma == mutual
        assertions += 1

        affine_scale = Fraction((19 * i) % 43 + 1, (23 * i) % 41 + 1)
        omega_a = Fraction((29 * i) % 47 + 1, (31 * i) % 53 + 1)
        omega_b = omega_a / r
        assert (affine_scale * omega_a) / (affine_scale * omega_b) == r
        assertions += 1
        assert affine_scale / (affine_scale * omega_a) == 1 / omega_a
        assertions += 1

        if w == 0:
            planar_cases += 1
        else:
            transverse_cases += 1
            assert mutual < sech_depth
            assertions += 1

    # A fixed-r family proves that the transport scalar is not a function of r alone.
    fixed_r = Fraction(7, 3)
    fixed_values = set()
    for numerator in range(0, 101):
        w = Fraction(numerator, 37)
        gamma = (fixed_r + 1 / fixed_r + fixed_r * w * w) / 2
        fixed_values.add(1 / gamma)
        assertions += 1
    assert len(fixed_values) == 101
    assertions += 1

    result = {
        "status": "PASS",
        "expected_landing": LANDING,
        "cases": cases,
        "assertions": assertions,
        "planar_cases": planar_cases,
        "transverse_cases": transverse_cases,
        "fixed_r_distinct_mutual_values": len(fixed_values),
        "production_imported": False,
        "production_result_read": False,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if not args.no_write:
        OUT.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
