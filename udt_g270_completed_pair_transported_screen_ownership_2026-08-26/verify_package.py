#!/usr/bin/env python3
"""Fail-closed no-write G270 package verifier."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
LANDING = (
    "FULL_SUPPLIED_REALIZATION_EVALUATES_TRANSPORTED_SCREEN_MISMATCH__"
    "COMPLETED_PAIR_DUAL_RECIPROCITY_NORMALIZES_ONLY_THE_INTRINSIC_PULLBACK__"
    "EXACT_SAME_PULLBACK_TILTED_NULL_RIBBONS_HAVE_DIFFERENT_W__"
    "NO_UNIVERSAL_W_VALUE_POPULATION_HISTORY_DISTANCE_OR_XMAX_SELECTION"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_json(name: str) -> dict:
    completed = subprocess.run(
        [sys.executable, str(ROOT / name), "--no-write"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def resolve_source(relative: str, expected: str) -> Path:
    for candidate in (REPO / relative, REPO / "private_sources" / relative):
        if candidate.is_file() and sha256(candidate) == expected:
            return candidate
    raise AssertionError(f"sealed source absent or changed: {relative}")


def main() -> None:
    required = (
        "ADVERSARIAL_REVIEW_REQUEST.md",
        "AUDIT_REPORT.md",
        "CATCH_PROOF_RESULT.json",
        "DERIVATION_RESULT.json",
        "EVIDENCE_GATES.md",
        "EXACT_DERIVATION.md",
        "INDEPENDENT_VERIFICATION.json",
        "LAY_REPORT.md",
        "MAP.md",
        "PREMISE_LEDGER.tsv",
        "PREREGISTRATION.md",
        "RUN_RECORD.md",
        "SOURCE_MANIFEST.tsv",
        "STATUS_LEDGER.tsv",
        "build_review_intake.py",
        "derive_screen_ownership.py",
        "run_catch_proofs.py",
        "verify_package.py",
        "verify_screen_ownership_independent.py",
    )
    assert all((ROOT / name).is_file() for name in required)

    with (ROOT / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        sources = list(csv.DictReader(handle, delimiter="\t"))
    assert len(sources) == 13
    for row in sources:
        resolve_source(row["path"], row["sha256"])

    recorded = (
        ROOT / "DERIVATION_RESULT.json",
        ROOT / "INDEPENDENT_VERIFICATION.json",
        ROOT / "CATCH_PROOF_RESULT.json",
    )
    before = {path.name: sha256(path) for path in recorded}
    production = run_json("derive_screen_ownership.py")
    independent = run_json("verify_screen_ownership_independent.py")
    catches = run_json("run_catch_proofs.py")
    after = {path.name: sha256(path) for path in recorded}
    assert before == after

    assert production == json.loads((ROOT / "DERIVATION_RESULT.json").read_text())
    assert independent == json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text())
    assert catches == json.loads((ROOT / "CATCH_PROOF_RESULT.json").read_text())
    assert production["status"] == independent["status"] == catches["status"] == "PASS"
    assert production["landing"] == independent["expected_landing"] == LANDING
    assert production["selected_alternative"] == (
        "C__REALIZATION_EVALUATES_W__INTRINSIC_COMPLETED_PAIR_DOES_NOT_SELECT_IT"
    )
    assert production["exact_checks"] == 36
    assert production["ownership"] == {
        "completed_pair_dual_reciprocity": "DOES_NOT_SELECT_W",
        "full_supplied_realization": "EVALUATES_W_UNIQUELY",
        "intrinsic_completed_pair_metric": "DOES_NOT_DETERMINE_W",
    }
    assert production["fixed_r_separator"] == {
        "r": "2",
        "planar_W2": "0",
        "planar_M_PT": "4/5",
        "tilted_W2": "1",
        "tilted_M_PT": "4/9",
        "intrinsic_pullback_equal": True,
    }
    assert production["w_is_jacobi_screen"] is False
    assert production["query_population"] == "OPEN_NOT_SELECTED"
    assert production["history_distance_xmax"] == "OPEN_NOT_TESTED"

    assert independent["cases"] == 12000
    assert independent["assertions"] == 208005
    assert independent["smooth_ribbon_axis_cases"] == 1001
    assert independent["fixed_r_distinct_transport_values"] == 101
    assert independent["production_imported"] is False
    assert independent["production_result_read"] is False

    assert catches["baseline_failures"] == []
    assert catches["catches"] == 11 and catches["missed"] == []
    assert catches["shared_validator_exercised"] is True
    assert all(item["targeted_caught"] for item in catches["mutations"].values())

    assert "a75d71bf" in (ROOT / "EVIDENCE_GATES.md").read_text()
    assert "INTERNALLY_VERIFIED_AWAITING_FRESH_EXTERNAL_REVIEW" in (
        ROOT / "EVIDENCE_GATES.md"
    ).read_text()
    premise_text = (ROOT / "PREMISE_LEDGER.tsv").read_text()
    assert "SEPARATE_DERIVED_CONDITIONAL_CHANNELS" in premise_text
    assert "OPEN_OMITTED" in premise_text

    print(json.dumps({
        "status": "PASS",
        "grade": "INTERNALLY_VERIFIED_AWAITING_FRESH_EXTERNAL_REVIEW",
        "landing": LANDING,
        "selected_alternative": production["selected_alternative"],
        "exact_checks": production["exact_checks"],
        "independent_cases": independent["cases"],
        "independent_assertions": independent["assertions"],
        "smooth_ribbon_axis_cases": independent["smooth_ribbon_axis_cases"],
        "mutation_catches": catches["catches"],
        "source_count": len(sources),
        "fixed_r_separator": production["fixed_r_separator"],
        "recorded_artifacts_unchanged": before == after,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
