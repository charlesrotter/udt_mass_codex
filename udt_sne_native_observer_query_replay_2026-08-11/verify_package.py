#!/usr/bin/env python3
"""Mechanical package verification; semantic external review remains a separate gate."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RAW_REVIEW_REPOSITORY_SHA256 = (
    "f7b04fe9a916c28f2485019a11f570a98b6dabc94d83cc374c6dad15142dc503"
)
MUTABLE_SOURCE_SNAPSHOT_COMMIT = "307144b5"


def require(checks: dict[str, str], name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def run() -> dict[str, object]:
    checks: dict[str, str] = {}
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        source_rows = list(csv.DictReader(handle, delimiter="\t"))
    require(checks, "source_count", len(source_rows) == 19)
    for row in source_rows:
        source_bytes = (ROOT / row["path"]).read_bytes()
        digest = hashlib.sha256(source_bytes).hexdigest()
        if digest != row["sha256"] and row["path"] == "CURRENT_SCIENTIFIC_PREMISES.tsv":
            snapshot = subprocess.run(
                ["git", "show", f"{MUTABLE_SOURCE_SNAPSHOT_COMMIT}:{row['path']}"],
                cwd=ROOT,
                check=True,
                capture_output=True,
            ).stdout
            digest = hashlib.sha256(snapshot).hexdigest()
        require(checks, f"source_hash::{row['path']}", digest == row["sha256"])

    replay = json.loads((HERE / "REPLAY_RESULT.json").read_text(encoding="utf-8"))
    equivalence = json.loads((HERE / "QUERY_EQUIVALENCE.json").read_text(encoding="utf-8"))
    independent = json.loads((HERE / "INDEPENDENT_PRIMARY.json").read_text(encoding="utf-8"))
    catches = json.loads((HERE / "CATCH_PROOF_RESULTS.json").read_text(encoding="utf-8"))
    require(checks, "replay_pass", replay["status"] == "PASS")
    require(checks, "all_18_fits", replay["fit_count"] == 18)
    require(checks, "all_443_fields", replay["compared_leaf_fields"] == 443)
    require(checks, "bit_exact_replay", replay["maximum_absolute_numeric_difference"] == 0.0)
    require(checks, "equivalence_pass", equivalence["status"] == "PASS")
    require(checks, "equivalence_count", equivalence["check_count"] == 9)
    require(
        checks,
        "no_formula_change",
        equivalence["interpretation"]["formula_change_from_retyping"] is False,
    )
    require(checks, "independent_pass", independent["status"] == "PASS")
    for name, difference in independent["absolute_differences"].items():
        require(
            checks,
            f"independent_tolerance::{name}",
            float(difference) <= float(independent["tolerances"][name]),
        )
    require(checks, "catch_count", catches["catch_count"] == 14)
    require(
        checks,
        "all_catches_reject",
        all(value == "PASS_REJECTED" for value in catches["catches"].values()),
    )
    require(checks, "type_catch_count", catches["type_catch_count"] == 3)
    require(
        checks,
        "stringified_float_rejected",
        catches["type_catches"]["stringified_float_leaf"] == "PASS_REJECTED",
    )
    require(
        checks,
        "boolean_float_rejected",
        catches["type_catches"]["boolean_in_float_leaf"] == "PASS_REJECTED",
    )
    require(
        checks,
        "integer_numeric_float_accepted",
        catches["type_catches"]["integer_numeric_float_leaf"] == "PASS_ACCEPTED",
    )
    require(
        checks,
        "external_review_raw_hash",
        hashlib.sha256((HERE / "EXTERNAL_REVIEW_RAW.md").read_bytes()).hexdigest()
        == RAW_REVIEW_REPOSITORY_SHA256,
    )

    with (HERE / "CORRECTION_OWNER_LEDGER.tsv").open(newline="", encoding="utf-8") as handle:
        owner_rows = list(csv.DictReader(handle, delimiter="\t"))
    require(checks, "owner_row_count", len(owner_rows) == 11)
    owner = {row["object"]: row for row in owner_rows}
    require(
        checks,
        "no_owned_complete_correction",
        owner["native_complete_SNe_correction"]["status"]
        == "NO_OWNED_COMPLETE_FORMULA",
    )
    require(
        checks,
        "orchestra_not_zeroed",
        owner["complete_pair_orchestra"]["status"].startswith("STRUCTURAL_MODULATION_OWNED"),
    )
    require(
        checks,
        "P1_role_guard",
        owner["P1_profile"]["status"] == "CONDITIONAL_OBSERVER_PAIR_SNE_PROFILE",
    )

    result = {
        "schema": "udt-sne-native-query-package-verification-1.0",
        "status": "PASS",
        "check_count": len(checks),
        "checks": checks,
        "external_semantic_review": "VERIFIED_WITH_CAVEATS",
    }
    (HERE / "FINAL_VERIFICATION.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"PASS package_checks={len(checks)} external_review=VERIFIED_WITH_CAVEATS")
    return result


if __name__ == "__main__":
    run()
