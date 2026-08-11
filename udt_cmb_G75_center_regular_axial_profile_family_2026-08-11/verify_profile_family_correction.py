#!/usr/bin/env python3
"""Additions-only strengthened local replay required by the G75 external review."""

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


def ftext(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def exact_shape_fields(coeffs: tuple[int, int, int]) -> dict[str, str]:
    """Reconstruct the load-bearing algebraic fields without calling the production generator."""
    c0, c1, c2 = coeffs
    normalization = max_abs(coeffs)
    candidates_set = {Fraction(0), Fraction(1)}
    interior_extrema: list[tuple[Fraction, Fraction]] = []
    if c2:
        vertex = Fraction(-c1, 2 * c2)
        if 0 < vertex < 1:
            candidates_set.add(vertex)
            value = Fraction(c0) + Fraction(c1) * vertex + Fraction(c2) * vertex * vertex
            interior_extrema.append((vertex, value / normalization))

    expression = sp.expand(c0 + c1 * S + c2 * S**2)
    roots: list[tuple[sp.Expr, int]] = []
    for root, multiplicity in sp.roots(expression, S).items():
        if root.is_real is False:
            continue
        if root.is_real is None and sp.simplify(sp.im(root)) != 0:
            continue
        inside = sp.simplify(sp.And(root > 0, root < 1))
        if inside is sp.true:
            roots.append((root, int(multiplicity)))
        elif inside is not sp.false:
            raise AssertionError((coeffs, root, inside))
    roots.sort(key=lambda item: float(sp.N(item[0], 40)))

    center_order = 0 if c0 else (1 if c1 else 2)
    endpoint_value = c0 + c1 + c2
    endpoint_derivative = c1 + 2 * c2
    endpoint_order = 0 if endpoint_value else (1 if endpoint_derivative else 2)
    odd_roots = sum(1 for _, multiplicity in roots if multiplicity % 2)
    even_roots = sum(1 for _, multiplicity in roots if not multiplicity % 2)
    if odd_roots:
        behavior = "INTERIOR_SIGN_CHANGE"
    elif even_roots:
        behavior = "INTERIOR_TOUCH_NO_SIGN_CHANGE"
    elif center_order and endpoint_order:
        behavior = "ZERO_BOTH_BOUNDARIES_NO_INTERIOR_ROOT"
    elif center_order:
        behavior = "CENTER_OFF_NO_INTERIOR_ROOT"
    elif endpoint_order:
        behavior = "ENDPOINT_TAPER_NO_INTERIOR_ROOT"
    else:
        behavior = "PERSISTENT_SIGN_NO_INTERIOR_ROOT"

    return {
        "polynomial": str(expression),
        "normalization_M": ftext(normalization),
        "normalized_c0": ftext(Fraction(c0, 1) / normalization),
        "normalized_c1": ftext(Fraction(c1, 1) / normalization),
        "normalized_c2": ftext(Fraction(c2, 1) / normalization),
        "center_q_order_in_s": str(center_order),
        "center_h_order_in_x": str(2 + 2 * center_order),
        "center_B_order_in_x": str(2 + 4 * center_order),
        "endpoint_zero_order_in_s": str(endpoint_order),
        "open_root_count_distinct": str(len(roots)),
        "open_root_count_multiplicity": str(sum(multiplicity for _, multiplicity in roots)),
        "open_odd_root_count": str(odd_roots),
        "open_even_root_count": str(even_roots),
        "open_roots_exact": ";".join(f"{sp.sstr(root)}@{multiplicity}" for root, multiplicity in roots) or "-",
        "sign_pattern_open_interval": ",".join("+" if step % 2 == 0 else "-" for step in range(odd_roots + 1)),
        "interior_extrema_exact": ";".join(f"{ftext(point)}:{ftext(value)}" for point, value in interior_extrema) or "-",
        "normalization_candidates": ";".join(ftext(value) for value in sorted(candidates_set)),
        "center_value_normalized": ftext(Fraction(c0, 1) / normalization),
        "endpoint_value_normalized": ftext(Fraction(endpoint_value, 1) / normalization),
        "behavior_class": behavior,
        "stratum_code": f"C{center_order}_E{endpoint_order}_O{odd_roots}_T{even_roots}",
    }


def validate_shape_rows(shapes: list[dict[str, str]]) -> bool:
    if len(shapes) != 49:
        return False
    for row in shapes:
        coeffs = tuple(int(row[f"c{i}"]) for i in range(3))
        expected = exact_shape_fields(coeffs)
        if any(row[field] != value for field, value in expected.items()):
            return False
    return True


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
        "exact_root_identity_replay": True,
        "distinct_root_count_replay": True,
        "exact_extrema_replay": True,
        "behavior_label_replay": True,
        "stratum_label_replay": True,
        "complete_algebraic_row_replay": validate_shape_rows(shapes),
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
        expected_fields = exact_shape_fields(coeffs)
        checks["exact_root_identity_replay"] &= row["open_roots_exact"] == expected_fields["open_roots_exact"]
        checks["distinct_root_count_replay"] &= row["open_root_count_distinct"] == expected_fields["open_root_count_distinct"]
        checks["exact_extrema_replay"] &= row["interior_extrema_exact"] == expected_fields["interior_extrema_exact"]
        checks["behavior_label_replay"] &= row["behavior_class"] == expected_fields["behavior_class"]
        checks["stratum_label_replay"] &= row["stratum_code"] == expected_fields["stratum_code"]
        behavior[row["behavior_class"]] += 1
    assert all(checks.values()), [name for name, value in checks.items() if not value]
    payload = {
        "schema": "udt-cmb-g75-corrected-local-replay-v1",
        "status": "PASS",
        "checks": checks,
        "passed": sum(checks.values()),
        "total": len(checks),
        "behavior_counts": dict(sorted(behavior.items())),
        "protected_draft_read": False,
    }
    (HERE / "CORRECTED_INDEPENDENT_VERIFICATION_RESULT.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
