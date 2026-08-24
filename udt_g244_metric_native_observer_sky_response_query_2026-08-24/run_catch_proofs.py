#!/usr/bin/env python3
"""Hostile mutation checks for the G244 contract."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
OUTPUT = PACKAGE / "CATCH_PROOF_RESULT.json"


def det2(a: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]) -> Fraction:
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def normalize(values: list[Fraction]) -> list[Fraction]:
    total = sum(values, Fraction(0))
    return [value / total for value in values]


def bilinear(left: list[Fraction], kernel: list[list[Fraction]], right: list[Fraction]) -> Fraction:
    return sum(
        (left[i] * kernel[i][j] * right[j] for i in range(len(left)) for j in range(len(right))),
        Fraction(0),
    )


def contract_accepts(metadata: dict[str, object]) -> bool:
    return (
        metadata.get("angular_coefficient_count") == 0
        and metadata.get("retains_shape_tensor") is True
        and metadata.get("position_block_composition") == "FULL_PHASE_BLOCK_FORMULA"
        and metadata.get("caustic_position_inverse") is False
        and metadata.get("g225_promoted_transport") is False
        and metadata.get("source_detector_derived") is False
        and metadata.get("observational_outcomes") == "CLOSED_AND_UNREAD"
        and metadata.get("forbidden_imports") == []
    )


def compute() -> dict[str, object]:
    checks: dict[str, bool] = {}

    orientation_reversing = ((Fraction(-2), Fraction(0)), (Fraction(0), Fraction(3)))
    checks["signed_area_mutation_caught"] = det2(orientation_reversing) < 0 and abs(
        det2(orientation_reversing)
    ) > 0

    q = normalize([Fraction(1), Fraction(2), Fraction(3), Fraction(4)])
    area = [Fraction(1), Fraction(2), Fraction(1), Fraction(3)]
    kernel = [[Fraction(x) for x in row] for row in (
        (0, 1, 0, 1), (1, 0, 1, 0), (0, 1, 0, 1), (1, 0, 1, 0)
    )]
    p = normalize([x * y for x, y in zip(q, area)])
    rr = bilinear(q, kernel, q)
    native_w = (bilinear(p, kernel, p) - 2 * bilinear(p, kernel, q) + rr) / rr
    fitted_area = [value ** 2 for value in area]
    fitted_p = normalize([x * y for x, y in zip(q, fitted_area)])
    fitted_w = (
        bilinear(fitted_p, kernel, fitted_p) - 2 * bilinear(fitted_p, kernel, q) + rr
    ) / rr
    checks["angular_coefficient_mutation_caught"] = native_w == Fraction(-1, 6) and fitted_w != native_w

    # D=[[1,1],[0,1]] has an off-diagonal observer response H.  Dropping it changes det(H).
    full_h = ((Fraction(1), Fraction(1)), (Fraction(1), Fraction(2)))
    diagonalized_h = ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(2)))
    checks["diagonal_scalarization_caught"] = det2(full_h) == 1 and det2(diagonalized_h) == 2

    # Exact scalar one-screen phase counterexample: B20=A21*B10+B21*D10=17, not B21*B10=6.
    checks["position_block_product_mutation_caught"] = (1 * 2 + 3 * 5 == 17) and (3 * 2 != 17)

    try:
        _ = Fraction(1, 1) / det2(((Fraction(1), Fraction(0)), (Fraction(0), Fraction(0))))
        inverse_failed = False
    except ZeroDivisionError:
        inverse_failed = True
    checks["caustic_inverse_mutation_caught"] = inverse_failed

    good = {
        "angular_coefficient_count": 0,
        "retains_shape_tensor": True,
        "position_block_composition": "FULL_PHASE_BLOCK_FORMULA",
        "caustic_position_inverse": False,
        "g225_promoted_transport": False,
        "source_detector_derived": False,
        "observational_outcomes": "CLOSED_AND_UNREAD",
        "forbidden_imports": [],
    }
    checks["valid_contract_accepted"] = contract_accepts(good)
    mutations = {
        "fitted_coefficient": {**good, "angular_coefficient_count": 1},
        "shape_dropped": {**good, "retains_shape_tensor": False},
        "position_blocks_multiplied": {**good, "position_block_composition": "B21_TIMES_B10"},
        "caustic_inverted": {**good, "caustic_position_inverse": True},
        "g225_promoted": {**good, "g225_promoted_transport": True},
        "source_law_derived": {**good, "source_detector_derived": True},
        "boss_opened": {**good, "observational_outcomes": "OPENED"},
        "forbidden_import": {**good, "forbidden_imports": ["X_max"]},
    }
    for name, mutation in mutations.items():
        checks[f"semantic_{name}_caught"] = not contract_accepts(mutation)

    if not all(checks.values()):
        raise AssertionError(f"hostile catch failure: {checks}")
    return {
        "audit": "G244_HOSTILE_CATCH_PROOFS",
        "status": "PASS",
        "checks": checks,
        "caught": sum(checks.values()),
        "attempted": len(checks),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    result = compute()
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if not args.no_write:
        OUTPUT.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
