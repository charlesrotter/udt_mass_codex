#!/usr/bin/env python3
"""Hostile mutation checks for the bounded G310 conclusion."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path

from derive_ddr_tracefree import (
    diagonal,
    lorentz_orbit,
    nullspace,
    pair_row,
    rank,
    symmetric_vector,
)


def build_result() -> dict[str, object]:
    orbit, _, generator_count = lorentz_orbit()
    rows = [pair_row(vector) for vector in orbit]
    eta = symmetric_vector(diagonal(-1, 1, 1, 1))

    cases = [
        {
            "mutation": "opposite_sign_ruler_tangent_called_reciprocal",
            "caught": sum(x * y for x, y in zip(eta, symmetric_vector(diagonal(2, -2, 0, 0)))) != 0,
        },
        {
            "mutation": "one_pair_plane_called_complete",
            "caught": rank(rows[:1]) < 9,
        },
        {
            "mutation": "uncomposed_generators_called_complete",
            "caught": rank(rows[:generator_count]) == 8,
        },
        {
            "mutation": "scalar_only_a_zero_called_nonidentity_shape_law",
            "caught": all(sum(x * y for x, y in zip(row, eta)) == 0 for row in rows),
        },
        {
            "mutation": "ddr_called_full_E_zero",
            "caught": any(eta) and all(sum(x * y for x, y in zip(row, eta)) == 0 for row in rows),
        },
        {
            "mutation": "common_trace_magnitude_called_fixed",
            "caught": all(sum(x * y for x, y in zip(row, [Fraction(7) * item for item in eta])) == 0 for row in rows),
        },
        {
            "mutation": "annihilator_called_two_dimensional",
            "caught": len(nullspace(rows)) == 1,
        },
    ]
    assert all(case["caught"] for case in cases)
    return {"status": "PASS", "hostile_cases": len(cases), "cases": cases}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build_result()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
