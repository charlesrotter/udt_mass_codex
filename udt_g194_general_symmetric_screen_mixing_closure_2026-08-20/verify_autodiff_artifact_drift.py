#!/usr/bin/env python3
"""Verify that R4 changed only declared autodiff roundoff diagnostics."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
REFERENCE = PACKAGE / "INDEPENDENT_VERIFICATION_FORWARD_AD_REFERENCE.json"
CANDIDATE = PACKAGE / "INDEPENDENT_VERIFICATION.json"
CEILING = 2.0e-8


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compare(left, right, path=""):
    differences = []
    if type(left) is not type(right):
        return [(path, left, right)]
    if isinstance(left, dict):
        if left.keys() != right.keys():
            return [(f"{path}/keys", sorted(left), sorted(right))]
        for key in left:
            differences.extend(compare(left[key], right[key], f"{path}/{key}"))
        return differences
    if isinstance(left, list):
        if len(left) != len(right):
            return [(f"{path}/length", len(left), len(right))]
        for index, (left_item, right_item) in enumerate(zip(left, right)):
            differences.extend(compare(left_item, right_item, f"{path}/{index}"))
        return differences
    if left != right:
        differences.append((path, left, right))
    return differences


def main():
    reference = json.loads(REFERENCE.read_text(encoding="utf-8"))
    candidate = json.loads(CANDIDATE.read_text(encoding="utf-8"))
    differences = compare(reference, candidate)

    implementation_differences = []
    numerical_differences = []
    forbidden_differences = []
    for path, old, new in differences:
        field = path.rsplit("/", 1)[-1]
        if path == "/implementation" and isinstance(old, str) and isinstance(new, str):
            implementation_differences.append((path, old, new))
        elif field in {"max_tide_error", "max_tide_asymmetry"} and isinstance(
            old, (int, float)
        ) and isinstance(new, (int, float)):
            numerical_differences.append((path, float(old), float(new)))
        else:
            forbidden_differences.append((path, old, new))

    assert len(implementation_differences) == 1
    assert numerical_differences
    assert not forbidden_differences
    assert all(abs(old) < CEILING and abs(new) < CEILING for _, old, new in numerical_differences)
    maximum_drift = max(abs(new - old) for _, old, new in numerical_differences)
    assert maximum_drift < CEILING

    result = {
        "status": "PASS",
        "reference_sha256": sha256(REFERENCE),
        "candidate_sha256": sha256(CANDIDATE),
        "difference_count": len(differences),
        "implementation_difference_count": len(implementation_differences),
        "numerical_difference_count": len(numerical_differences),
        "forbidden_difference_count": len(forbidden_differences),
        "changed_numeric_fields": sorted(
            {path.rsplit("/", 1)[-1] for path, _, _ in numerical_differences}
        ),
        "maximum_absolute_numeric_drift": maximum_drift,
        "ceiling": CEILING,
        "all_other_fields_exactly_identical": True,
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if os.environ.get("G194_NO_WRITE") != "1":
        (PACKAGE / "AUTODIFF_ARTIFACT_DRIFT_RESULT.json").write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
