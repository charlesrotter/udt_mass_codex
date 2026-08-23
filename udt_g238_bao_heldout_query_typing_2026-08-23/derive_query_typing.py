#!/usr/bin/env python3
"""Exact finite-state witness and structural G238 contract checks."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from decimal import Decimal
from fractions import Fraction
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent


def multiply_linear(coefficients: list[Fraction], root: Fraction) -> list[Fraction]:
    result = [Fraction(0)] * (len(coefficients) + 1)
    for index, value in enumerate(coefficients):
        result[index] -= root * value
        result[index + 1] += value
    return result


def derivative(coefficients: list[Fraction]) -> list[Fraction]:
    return [Fraction(index) * coefficients[index] for index in range(1, len(coefficients))]


def evaluate(coefficients: list[Fraction], point: Fraction) -> Fraction:
    value = Fraction(0)
    for coefficient in reversed(coefficients):
        value = value * point + coefficient
    return value


def fraction_record(value: Fraction) -> dict[str, object]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "float": float(value),
    }


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def exact_normalized_knots(state_path: Path) -> list[Fraction]:
    """Read the frozen JSON decimal spellings exactly and affinely normalize them."""

    exact_state = json.loads(state_path.read_text(), parse_float=Decimal)
    exact_knots = [Fraction(value) for value in exact_state["state"]["knots"]]
    first = exact_knots[0]
    span = exact_knots[-1] - first
    if span <= 0:
        raise RuntimeError("frozen knot span is not positive")
    roots = [(value - first) / span for value in exact_knots]
    if any(roots[index + 1] <= roots[index] for index in range(len(roots) - 1)):
        raise RuntimeError("exact normalized knots are not strictly increasing")
    return roots


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_sources() -> int:
    rows = list(csv.DictReader((PACKAGE / "SOURCE_MANIFEST.tsv").open(), delimiter="\t"))
    for row in rows:
        path = ROOT / row["path"]
        if not path.is_file():
            raise RuntimeError(f"missing source: {row['path']}")
        actual = sha256(path)
        if actual != row["sha256"]:
            raise RuntimeError(f"source hash mismatch: {row['path']}")
    return len(rows)


def derive() -> dict[str, object]:
    source_count = verify_sources()
    state_path = ROOT / (
        "udt_g237_dual_sne_joint_relational_state_freeze_2026-08-23/"
        "FROZEN_PRIMARY_K12_STATE.json"
    )
    state = json.loads(state_path.read_text())
    values = state["state"]
    knots = values["knots"]
    relative_r = values["relative_R"]
    if state["resolution"] != 12 or len(knots) != 12 or len(relative_r) != 11:
        raise RuntimeError("frozen state shape mismatch")
    if any(knots[index + 1] <= knots[index] for index in range(11)):
        raise RuntimeError("knots are not strictly increasing")
    if any(value <= 0 for value in relative_r):
        raise RuntimeError("relative R values are not positive")
    forbidden_fields = {"interpolation", "derivatives", "absolute_scale", "metric_history"}
    present_fields = forbidden_fields.intersection(state) | forbidden_fields.intersection(values)
    if present_fields:
        raise RuntimeError(f"unexpected profile fields: {sorted(present_fields)}")

    coefficients = [Fraction(1)]
    roots = exact_normalized_knots(state_path)
    for root in roots:
        coefficients = multiply_linear(coefficients, root)
    if any(evaluate(coefficients, root) != 0 for root in roots):
        raise RuntimeError("counterfamily polynomial does not vanish at every knot")
    first = derivative(coefficients)
    second = derivative(first)
    midpoint = (roots[0] + roots[1]) / 2
    q0 = evaluate(coefficients, midpoint)
    q1 = evaluate(first, midpoint)
    q2 = evaluate(second, midpoint)
    if 0 in (q0, q1, q2):
        raise RuntimeError("counterfamily witness is degenerate at the registered midpoint")

    ledger_rows = list(csv.DictReader((PACKAGE / "OPERATOR_TYPE_LEDGER.tsv").open(), delimiter="\t"))
    open_rows = [row["stage"] for row in ledger_rows if row["status"] in {"OPEN", "QUERY_TYPING_INCOMPLETE"}]
    required_open = {"Q02", "Q03", "Q04", "Q09", "Q10", "Q11", "Q15"}
    if not required_open.issubset(open_rows):
        raise RuntimeError("operator ledger omits a registered open gate")

    return {
        "landing": (
            "QUERY_TYPING_INCOMPLETE__NO_OUTCOME_OPENING"
            "__FROZEN_SNE_STATE_DOES_NOT_DETERMINE_CONTINUOUS_METRIC_OR_SCREEN_HISTORY"
            "__COMPLETE_METRIC_EVALUATORS_REMAIN_LIVE_CONDITIONALLY"
            "__TWO_SOURCE_POPULATION_AND_REFERENCE_FORWARD_MAP_OPEN"
        ),
        "source_hashes_verified": source_count,
        "frozen_state": {
            "resolution": state["resolution"],
            "knot_count": len(knots),
            "relative_r_count": len(relative_r),
            "strictly_increasing_knots": True,
            "positive_relative_r": True,
            "interpolation_present": False,
            "derivatives_present": False,
            "absolute_scale_present": False,
            "metric_history_present": False,
        },
        "counterfamily": {
            "root_source": "exact frozen JSON decimal spellings, affinely normalized",
            "normalized_roots": [fraction_text(root) for root in roots],
            "evaluation_point": fraction_text(midpoint),
            "q": fraction_record(q0),
            "q_prime": fraction_record(q1),
            "q_second": fraction_record(q2),
            "all_knot_values_zero": True,
        },
        "operator_ledger_rows": len(ledger_rows),
        "open_stages": open_rows,
        "boss_outcomes_opened": False,
        "profile_or_feature_fit_performed": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    arguments = parser.parse_args()
    result = derive()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if arguments.write:
        (PACKAGE / "DERIVATION_RESULT.json").write_text(encoded)
    print(encoded, end="")


if __name__ == "__main__":
    main()
