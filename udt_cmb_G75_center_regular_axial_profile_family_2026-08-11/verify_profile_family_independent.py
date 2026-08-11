#!/usr/bin/env python3
"""Independent standard-library/SymPy-Sturm verification of the G75 exact atlas."""

from __future__ import annotations

import csv
import itertools
import json
import math
from collections import Counter
from fractions import Fraction
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
S = sp.symbols("s", real=True)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def candidates() -> set[tuple[int, int, int]]:
    output = set()
    for item in itertools.product(range(-2, 3), repeat=3):
        nz = [abs(value) for value in item if value]
        if nz and math.gcd(*nz) == 1 and next(value for value in item if value) > 0:
            output.add(item)
    return output


def max_abs(coeffs: tuple[int, int, int]) -> Fraction:
    c0, c1, c2 = coeffs
    points = {Fraction(0), Fraction(1)}
    if c2 and 0 < Fraction(-c1, 2 * c2) < 1:
        points.add(Fraction(-c1, 2 * c2))
    return max(abs(Fraction(c0) + Fraction(c1) * x + Fraction(c2) * x * x) for x in points)


def main() -> None:
    shapes = read_tsv(HERE / "SHAPE_ATLAS.tsv")
    profiles = read_tsv(HERE / "PROFILE_ATLAS.tsv")
    expected = candidates()
    observed = {tuple(int(row[f"c{i}"]) for i in range(3)) for row in shapes}
    assert observed == expected and len(shapes) == 49
    assert len(profiles) == len({row["profile_id"] for row in profiles}) == 591

    checks = {
        "exact_shape_universe": observed == expected,
        "shape_count_49": len(shapes) == 49,
        "profile_count_591": len(profiles) == 591,
        "normalization_exact": True,
        "root_multiplicity_sturm_replay": True,
        "endpoint_order_replay": True,
        "center_order_replay": True,
        "all_center_smooth": all(row["center_status"] == "CENTER_C_INFINITY" for row in profiles),
        "all_signature_regular": all(Fraction(row["lapse_min"]) > 0 and row["signature_status"] == "LORENTZ_REGULAR_ALL_X" for row in profiles),
        "no_physical_selection": all(row["physical_status"] == "CHOSE_CONTROL_NOT_SELECTED" for row in profiles),
    }
    behavior = Counter()
    for row in shapes:
        coeffs = tuple(int(row[f"c{i}"]) for i in range(3))
        checks["normalization_exact"] &= Fraction(row["normalization_M"]) == max_abs(coeffs)
        poly = sp.Poly(sum(sp.Integer(coeffs[i]) * S**i for i in range(3)), S)
        p1 = sum(coeffs)
        dp1 = coeffs[1] + 2 * coeffs[2]
        endpoint_order = 0 if p1 else (1 if dp1 else 2)
        checks["endpoint_order_replay"] &= endpoint_order == int(row["endpoint_zero_order_in_s"])
        center_order = 0 if coeffs[0] else (1 if coeffs[1] else 2)
        checks["center_order_replay"] &= center_order == int(row["center_q_order_in_s"])
        # Use a separate exact real-root-isolation route; discard only point intervals at 0 or 1.
        counted = 0
        for (lower, upper), multiplicity in poly.intervals():
            if lower == upper and lower in (0, 1):
                continue
            if lower >= 0 and upper <= 1:
                counted += int(multiplicity)
        checks["root_multiplicity_sturm_replay"] &= counted == int(row["open_root_count_multiplicity"])
        behavior[row["behavior_class"]] += 1
    assert all(checks.values()), [name for name, value in checks.items() if not value]
    payload = {
        "schema": "udt-cmb-g75-independent-v1",
        "status": "PASS",
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
        "behavior_counts": dict(sorted(behavior.items())),
        "protected_draft_read": False,
    }
    (HERE / "INDEPENDENT_VERIFICATION_RESULT.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
