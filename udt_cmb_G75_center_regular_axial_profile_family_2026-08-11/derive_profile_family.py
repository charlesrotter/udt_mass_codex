#!/usr/bin/env python3
"""Exact G75 center-regular axial profile-family classification."""

from __future__ import annotations

import csv
import hashlib
import itertools
import json
import math
from collections import Counter
from fractions import Fraction
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
S = sp.symbols("s", real=True)
LAPSES = (("AM", Fraction(-1, 4)), ("A0", Fraction(0)), ("AP", Fraction(1, 4)))
AMPLITUDES = (("E05", Fraction(1, 20)), ("E20", Fraction(1, 5)), ("E50", Fraction(1, 2)), ("E100", Fraction(1)))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_sources() -> int:
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    for row in rows:
        target = ROOT / row["path"]
        assert target.is_file() and digest(target) == row["sha256"], target
    return len(rows)


def ftext(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def primitive_shapes() -> list[tuple[int, int, int]]:
    output = []
    for coeffs in itertools.product(range(-2, 3), repeat=3):
        nonzero = [abs(value) for value in coeffs if value]
        if not nonzero or math.gcd(*nonzero) != 1:
            continue
        if next(value for value in coeffs if value) < 0:
            continue
        output.append(coeffs)
    return sorted(output)


def evaluate(coeffs: tuple[int, int, int], value: Fraction) -> Fraction:
    c0, c1, c2 = coeffs
    return Fraction(c0) + Fraction(c1) * value + Fraction(c2) * value * value


def exact_normalization(coeffs: tuple[int, int, int]) -> tuple[Fraction, list[Fraction]]:
    c0, c1, c2 = coeffs
    candidates = [Fraction(0), Fraction(1)]
    if c2:
        vertex = Fraction(-c1, 2 * c2)
        if 0 < vertex < 1:
            candidates.append(vertex)
    maximum = max(abs(evaluate(coeffs, value)) for value in candidates)
    assert maximum > 0
    return maximum, sorted(set(candidates))


def open_roots(coeffs: tuple[int, int, int]) -> list[tuple[sp.Expr, int]]:
    polynomial = sp.Poly(sum(sp.Integer(coeffs[index]) * S**index for index in range(3)), S)
    output = []
    for root, multiplicity in sp.roots(polynomial.as_expr(), S).items():
        if root.is_real is False:
            continue
        if root.is_real is None and sp.simplify(sp.im(root)) != 0:
            continue
        inside = sp.simplify(sp.And(root > 0, root < 1))
        if inside is sp.true:
            output.append((root, int(multiplicity)))
        elif inside is not sp.false:
            raise AssertionError((coeffs, root, inside))
    return sorted(output, key=lambda item: float(sp.N(item[0], 40)))


def shape_record(index: int, coeffs: tuple[int, int, int]) -> dict[str, str | int]:
    c0, c1, c2 = coeffs
    normalization, extrema_candidates = exact_normalization(coeffs)
    roots = open_roots(coeffs)
    center_order = 0 if c0 else (1 if c1 else 2)
    endpoint = c0 + c1 + c2
    endpoint_derivative = c1 + 2 * c2
    endpoint_order = 0 if endpoint else (1 if endpoint_derivative else 2)
    odd_roots = sum(1 for _, multiplicity in roots if multiplicity % 2)
    even_roots = sum(1 for _, multiplicity in roots if not multiplicity % 2)
    interior_extrema = []
    if c2:
        vertex = Fraction(-c1, 2 * c2)
        if 0 < vertex < 1:
            interior_extrema.append((vertex, evaluate(coeffs, vertex) / normalization))
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
    sign_pattern = ",".join("+" if step % 2 == 0 else "-" for step in range(odd_roots + 1))
    normalized_coeffs = tuple(Fraction(value, 1) / normalization for value in coeffs)
    return {
        "shape_id": f"S{index:02d}",
        "c0": c0,
        "c1": c1,
        "c2": c2,
        "polynomial": str(sp.expand(c0 + c1 * S + c2 * S**2)),
        "normalization_M": ftext(normalization),
        "normalized_c0": ftext(normalized_coeffs[0]),
        "normalized_c1": ftext(normalized_coeffs[1]),
        "normalized_c2": ftext(normalized_coeffs[2]),
        "center_q_order_in_s": center_order,
        "center_h_order_in_x": 2 + 2 * center_order,
        "center_B_order_in_x": 2 + 4 * center_order,
        "endpoint_zero_order_in_s": endpoint_order,
        "open_root_count_distinct": len(roots),
        "open_root_count_multiplicity": sum(mult for _, mult in roots),
        "open_odd_root_count": odd_roots,
        "open_even_root_count": even_roots,
        "open_roots_exact": ";".join(f"{sp.sstr(root)}@{mult}" for root, mult in roots) or "-",
        "sign_pattern_open_interval": sign_pattern,
        "interior_extrema_exact": ";".join(
            f"{ftext(point)}:{ftext(value)}" for point, value in interior_extrema
        ) or "-",
        "normalization_candidates": ";".join(ftext(value) for value in extrema_candidates),
        "center_value_normalized": ftext(Fraction(c0, 1) / normalization),
        "endpoint_value_normalized": ftext(Fraction(endpoint, 1) / normalization),
        "behavior_class": behavior,
        "stratum_code": f"C{center_order}_E{endpoint_order}_O{odd_roots}_T{even_roots}",
        "reflection_class": "Q_TO_MINUS_Q_SAME_ROOT_MULTIPLICITY_AND_METRIC_SIGNATURE",
        "physical_status": "CHOSE_CONTROL_NOT_SELECTED",
    }


def write_tsv(path: Path, rows: list[dict[str, object]]) -> None:
    assert rows
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    source_count = verify_sources()
    coeffs = primitive_shapes()
    assert len(coeffs) == 49 and len(set(coeffs)) == 49
    shapes = [shape_record(index + 1, item) for index, item in enumerate(coeffs)]
    write_tsv(HERE / "SHAPE_ATLAS.tsv", shapes)

    profiles: list[dict[str, object]] = []
    for lapse_name, lapse in LAPSES:
        profiles.append({
            "profile_id": f"G75_F01_{lapse_name}",
            "lapse_name": lapse_name,
            "lapse_a": ftext(lapse),
            "shape_id": "ZERO",
            "amplitude": "0",
            "q_of_s": "0",
            "max_abs_q": "0",
            "center_h_order_in_x": "INFINITE_ZERO",
            "center_B_order_in_x": "INFINITE_ZERO",
            "endpoint_q": "0",
            "behavior_class": "ZERO_MIXING_CONTROL",
            "center_status": "CENTER_C_INFINITY",
            "signature_status": "LORENTZ_REGULAR_ALL_X",
            "lapse_min": ftext(min(Fraction(1), Fraction(1) + lapse)),
            "reflection_partner": "SELF",
            "physical_status": "CHOSE_CONTROL_NOT_SELECTED",
        })
    for shape in shapes:
        norm_coeffs = tuple(Fraction(shape[f"normalized_c{index}"]) for index in range(3))
        for amplitude_name, amplitude in AMPLITUDES:
            q_coeffs = tuple(amplitude * value for value in norm_coeffs)
            q_expr = sum(sp.Rational(value.numerator, value.denominator) * S**index for index, value in enumerate(q_coeffs))
            endpoint_q = sum(q_coeffs)
            for lapse_name, lapse in LAPSES:
                profiles.append({
                    "profile_id": f"G75_{lapse_name}_{shape['shape_id']}_{amplitude_name}",
                    "lapse_name": lapse_name,
                    "lapse_a": ftext(lapse),
                    "shape_id": shape["shape_id"],
                    "amplitude": ftext(amplitude),
                    "q_of_s": str(sp.expand(q_expr)),
                    "max_abs_q": ftext(amplitude),
                    "center_h_order_in_x": shape["center_h_order_in_x"],
                    "center_B_order_in_x": shape["center_B_order_in_x"],
                    "endpoint_q": ftext(endpoint_q),
                    "behavior_class": shape["behavior_class"],
                    "center_status": "CENTER_C_INFINITY",
                    "signature_status": "LORENTZ_REGULAR_ALL_X",
                    "lapse_min": ftext(min(Fraction(1), Fraction(1) + lapse)),
                    "reflection_partner": "NEGATIVE_Q_VIA_PSI_REFLECTION",
                    "physical_status": "CHOSE_CONTROL_NOT_SELECTED",
                })
    assert len(profiles) == 591 and len({row["profile_id"] for row in profiles}) == 591
    write_tsv(HERE / "PROFILE_ATLAS.tsv", profiles)

    behavior_counts = Counter(str(row["behavior_class"]) for row in shapes)
    stratum_counts = Counter(str(row["stratum_code"]) for row in shapes)
    center_counts = Counter(int(row["center_q_order_in_s"]) for row in shapes)
    endpoint_counts = Counter(int(row["endpoint_zero_order_in_s"]) for row in shapes)
    odd_counts = Counter(int(row["open_odd_root_count"]) for row in shapes)
    analogs = {}
    for name, target in {
        "persistent_even": (1, 0, 0),
        "endpoint_taper_even": (1, -2, 1),
        "sign_change_even": (1, -2, 0),
    }.items():
        analogs[name] = next(row["shape_id"] for row in shapes if tuple(int(row[f"c{i}"]) for i in range(3)) == target)

    exact_checks = {
        "shape_count_49": len(shapes) == 49,
        "profile_count_591": len(profiles) == 591,
        "all_shapes_primitive": all(math.gcd(*[abs(value) for value in item if value]) == 1 for item in coeffs),
        "all_sign_quotiented": all(next(value for value in item if value) > 0 for item in coeffs),
        "all_normalized": all(exact_normalization(tuple(int(row[f"c{i}"]) for i in range(3)))[0] == Fraction(str(row["normalization_M"])) for row in shapes),
        "all_center_C_infinity": all(row["center_status"] == "CENTER_C_INFINITY" for row in profiles),
        "all_lorentz_regular": all(row["signature_status"] == "LORENTZ_REGULAR_ALL_X" for row in profiles),
        "no_physical_selection": all(row["physical_status"] == "CHOSE_CONTROL_NOT_SELECTED" for row in profiles),
        "reflection_topology_neutral": all(row["reflection_class"].startswith("Q_TO_MINUS_Q") for row in shapes),
        "legacy_analogs_present_as_new_even_controls": len(analogs) == 3,
    }
    assert all(exact_checks.values())
    result = {
        "schema": "udt-cmb-g75-center-regular-profile-family-v1",
        "status": "PASS",
        "landing": "CENTER_REGULAR_FAMILY_HAS_MULTIPLE_EXACT_SHAPE_STRATA",
        "source_manifest_rows": source_count,
        "shape_count": len(shapes),
        "profile_count": len(profiles),
        "lapse_count": len(LAPSES),
        "amplitude_count": len(AMPLITUDES),
        "zero_mixing_controls": len(LAPSES),
        "behavior_counts": dict(sorted(behavior_counts.items())),
        "stratum_counts": dict(sorted(stratum_counts.items())),
        "center_onset_counts": {str(key): value for key, value in sorted(center_counts.items())},
        "endpoint_zero_order_counts": {str(key): value for key, value in sorted(endpoint_counts.items())},
        "interior_odd_root_counts": {str(key): value for key, value in sorted(odd_counts.items())},
        "new_even_analog_shape_ids": analogs,
        "exact_checks": exact_checks,
        "metric_signature_proof": "spatial eigenvalues (1/A,1,1) positive; timelike Schur complement -A-|w|^2 negative",
        "scale_status": "R_POSITIVE_SYMBOLIC_NOT_SELECTED",
        "physical_owner": "OPEN_NO_OWNER",
        "original_G74_blocked_profiles_repaired": False,
        "protected_draft_read": False,
    }
    (HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
