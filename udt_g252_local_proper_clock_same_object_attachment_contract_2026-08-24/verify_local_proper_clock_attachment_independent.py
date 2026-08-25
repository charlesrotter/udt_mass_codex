#!/usr/bin/env python3
"""Independent standard-library exact replay for G252.

Imports neither production code nor production output.
"""

from __future__ import annotations

import argparse
import csv
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import random


ROOT = Path(__file__).resolve().parent.parent
PKG = Path(__file__).resolve().parent
EXPECTED = (
    "ONE_BLINDED_INDEPENDENT_PROPER_CLOCK_RECORD_ON_ONE_FROZEN_IDENTIFIED_TIMELIKE_SEGMENT_"
    "CONDITIONALLY_FIXES_THE_SINGLE_G249_SCALE"
    "__CE_CONVERTS_THE_ATTACHED_DURATION_TO_LENGTH_WITHOUT_ADDING_A_SCALE_PARAMETER"
    "__A_SECOND_FROZEN_CLOCK_ATTACHMENT_TESTS_THE_SUPPLIED_DIMENSIONLESS_HISTORY_BY_EQUAL_SCALE_RECOVERY"
    "__EVENT_IDENTITY_AND_INDEPENDENT_CALIBRATION_ARE_SUPPLIED_OPERATIONAL_INPUTS_NOT_METRIC_DERIVATIONS"
    "__NO_CLOCK_VALUE_HISTORY_BRANCH_POPULATION_FIT_OUTCOME_OR_NEW_KERNEL_MECHANISM_SELECTED"
)


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            block = handle.read(131072)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def independent_resolve(relative: str, expected: str) -> Path:
    repository_candidate = ROOT.joinpath(*Path(relative).parts)
    sealed_candidate = ROOT.joinpath("sources", *Path(relative).parts)
    present = tuple(
        candidate
        for candidate in (repository_candidate, sealed_candidate)
        if candidate.is_file()
    )
    if len(present) != 1:
        raise AssertionError(f"independent source resolution ambiguity: {relative}")
    if digest(present[0]) != expected:
        raise AssertionError(f"independent source digest failure: {relative}")
    return present[0]


def source_gate() -> int:
    with (PKG / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        rows = tuple(csv.DictReader(handle, delimiter="\t"))
    if len(rows) != 6:
        raise AssertionError("unexpected source universe")
    for row in rows:
        independent_resolve(row["path"], row["sha256"])
    return len(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=int, default=12000)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    sources = source_gate()
    rng = random.Random(914252)
    assertions = 0
    rejected_inconsistent = 0
    for _ in range(args.cases):
        scale = F(rng.randrange(1, 73), rng.randrange(1, 67))
        model_a = F(rng.randrange(1, 79), rng.randrange(1, 71))
        model_b = F(rng.randrange(1, 83), rng.randrange(1, 73))
        clock_a = model_a * scale
        clock_b = model_b * scale
        recovered_a = clock_a / model_a
        recovered_b = clock_b / model_b
        assert recovered_a == scale
        assert recovered_b == scale
        assert recovered_a == recovered_b
        assertions += 3

        change = F(rng.randrange(1, 47), rng.randrange(1, 43))
        assert (change * clock_a) / (change * model_a) == scale
        assertions += 1

        # Independent reconstruction of a piecewise parameter change.
        speed = F(rng.randrange(1, 41), rng.randrange(1, 37))
        increment = F(rng.randrange(1, 31), rng.randrange(1, 29))
        parameter_change = F(rng.randrange(1, 23), rng.randrange(1, 19))
        assert speed * increment == (speed / parameter_change) * (parameter_change * increment)
        assertions += 1

        bad_clock_b = clock_b + F(1, rng.randrange(2, 29))
        if bad_clock_b / model_b != recovered_a:
            rejected_inconsistent += 1

    result = {
        "status": "PASS" if rejected_inconsistent == args.cases else "FAIL",
        "expected_landing": EXPECTED,
        "cases": args.cases,
        "assertions": assertions,
        "inconsistent_second_attachments_rejected": rejected_inconsistent,
        "source_count_verified": sources,
        "implementation": "standard_library_fraction_no_production_import_or_output_read",
        "observational_values_used": 0,
        "fitted_coefficients": 0,
        "history_selected": False,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
