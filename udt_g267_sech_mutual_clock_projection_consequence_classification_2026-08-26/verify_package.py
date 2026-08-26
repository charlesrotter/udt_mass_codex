#!/usr/bin/env python3
"""No-write G267 package verifier."""

from __future__ import annotations

import csv
import hashlib
import json
import pathlib
import subprocess
import sys


ROOT = pathlib.Path(__file__).resolve().parent
REPO = ROOT.parent


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_json(name: str) -> dict:
    completed = subprocess.run(
        [sys.executable, str(ROOT / name)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def resolve_source(relative: str, expected: str) -> pathlib.Path:
    for candidate in (REPO / relative, REPO / "private_sources" / relative):
        if candidate.is_file() and sha256(candidate) == expected:
            return candidate
    raise AssertionError(relative)


def main() -> None:
    with (ROOT / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        source_rows = list(csv.DictReader(handle, delimiter="\t"))
    assert len(source_rows) == 7
    for row in source_rows:
        resolve_source(row["path"], row["sha256"])

    production = run_json("derive_sech_projection.py")
    independent = run_json("verify_independent.py")
    catches = run_json("run_catch_proofs.py")
    assert production == json.loads((ROOT / "DERIVATION_RESULT.json").read_text())
    assert independent == json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text())
    assert catches == json.loads((ROOT / "CATCH_PROOF_RESULT.json").read_text())
    expected_landing = (
        "SECH_PROVISIONALLY_CLOSES_A_COEFFICIENT_FREE_BOUNDED_PAIR_STATE__"
        "SIGNED_COMPANION_REQUIRED_FOR_COMPOSITION__"
        "MUTUAL_EFFECT_IS_QUADRATIC_AT_QUIET_AND_SYMMETRIC_AT_LOUD_ENDS__"
        "DISTANCE_SCALE_QUERY_POPULATION_AND_HISTORY_REMAIN_OPEN"
    )
    assert production["status"] == independent["status"] == catches["status"] == "PASS"
    assert production["landing"] == expected_landing
    assert production["selected_alternative"] == (
        "C__SECH_NEW_PREMISE_CLOSES_COMPACT_PAIR_STATE__DISTANCE_AND_HISTORY_OPEN"
    )
    assert production["candidate_status"] == (
        "SUPPLIED_PROVISIONAL_CANDIDATE_NOT_DERIVED_UNIQUE_NOT_CANON"
    )
    assert production["exact_checks"] == 37
    assert independent["assertions"] == 1067
    assert catches["catches"] == 8
    assert production["history_rejection_by_candidate_definition"] == 0
    assert production["composition"]["M_alone"] == "INSUFFICIENT_SIGNED_COMPANION_REQUIRED"
    assert production["projection_competitors"]["uniqueness"] == (
        "NOT_DERIVED_BY_F1_F4_W1_W4_G266"
    )
    assert production["separation_ownership"]["dimensionful_distance"] == (
        "OPEN_REQUIRES_INDEPENDENT_SCALE_AND_PROTOCOL"
    )
    assert "EXTERNALLY_REVIEWED_VERIFIED_WITH_CAVEATS__ACCEPT_NO_REPAIRS" in (
        ROOT / "EVIDENCE_GATES.md"
    ).read_text()
    assert "SUPPLIED_PROVISIONAL_CANDIDATE" in (ROOT / "PREMISE_LEDGER.tsv").read_text()
    external_review = (ROOT / "EXTERNAL_REVIEW.md").read_text()
    assert "ACCEPT_NO_REPAIRS" in external_review
    assert "Bounded scientific landing survives: **yes**" in external_review

    print(json.dumps({
        "status": "PASS",
        "grade": "EXTERNALLY_REVIEWED_VERIFIED_WITH_CAVEATS__ACCEPT_NO_REPAIRS",
        "landing": expected_landing,
        "selected_alternative": production["selected_alternative"],
        "exact_checks": production["exact_checks"],
        "independent_assertions": independent["assertions"],
        "mutation_catches": catches["catches"],
        "source_count": len(source_rows),
        "candidate_status": production["candidate_status"],
        "history_rejections": production["history_rejection_by_candidate_definition"],
        "recorded_results_exact": True,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
