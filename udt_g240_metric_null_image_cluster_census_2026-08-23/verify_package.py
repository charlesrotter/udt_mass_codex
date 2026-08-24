#!/usr/bin/env python3
"""Package verifier for G240."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

from derive_null_image_cluster_census import LANDING, build_result, validate_result
from run_catch_proofs import build_result_set
from verify_cluster_census_independent import build_result as build_independent


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
OUTPUT = ROOT / "VERIFICATION_RESULT.json"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def resolve_source_root() -> tuple[Path, str]:
    sealed_scope = REPO / "REVIEW_SCOPE.json"
    if sealed_scope.is_file():
        sealed_sources = REPO / "sources"
        if not sealed_sources.is_dir():
            raise AssertionError("sealed source root missing: sources")
        return sealed_sources, "SEALED_SOURCES_ROOT"
    return REPO, "REPOSITORY_ROOT"


def verify_sources() -> tuple[int, str]:
    rows = read_tsv(ROOT / "SOURCE_MANIFEST.tsv")
    if len(rows) != 11:
        raise AssertionError("source manifest count changed")
    source_root, source_layout = resolve_source_root()
    for row in rows:
        path = source_root / row["path"]
        if not path.is_file():
            raise AssertionError(f"missing source: {row['path']}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != row["sha256"]:
            raise AssertionError(f"source hash mismatch: {row['path']}")
    return len(rows), source_layout


def build_verification() -> dict[str, Any]:
    required = (
        "AUDIT_REPORT.md",
        "CATCH_PROOF_RESULT.json",
        "COMMANDS.md",
        "DERIVATION_RESULT.json",
        "EVIDENCE_GATES.md",
        "EXACT_DERIVATION.md",
        "EXTERNAL_REPAIR_FOLLOWUP.md",
        "EXTERNAL_REPAIR_FOLLOWUP_RAW.md",
        "EXTERNAL_REVIEW.md",
        "EXTERNAL_REVIEW_RAW.md",
        "INDEPENDENT_VERIFICATION.json",
        "LAY_REPORT.md",
        "OPERATOR_LEDGER.tsv",
        "PREMISE_LEDGER.tsv",
        "PREREGISTRATION.md",
        "REVIEW_REQUEST.md",
        "REPAIR_FOLLOWUP_REQUEST.md",
        "REPAIR_PREREGISTRATION.md",
        "SOURCE_MANIFEST.tsv",
        "STATUS_LEDGER.tsv",
        "TRANSMISSION_RECORD.md",
        "build_review_intake.py",
        "derive_null_image_cluster_census.py",
        "run_catch_proofs.py",
        "verify_cluster_census_independent.py",
        "verify_package.py",
    )
    for name in required:
        if not (ROOT / name).is_file():
            raise AssertionError(f"required evidence missing: {name}")

    saved = json.loads((ROOT / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    fresh = build_result()
    validate_result(saved)
    if saved != fresh:
        raise AssertionError("saved derivation differs from fresh replay")

    saved_independent = json.loads((ROOT / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    fresh_independent = build_independent()
    if saved_independent != fresh_independent:
        raise AssertionError("saved independent replay differs from fresh replay")

    saved_catches = json.loads((ROOT / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    fresh_catches = build_result_set()
    if saved_catches != fresh_catches:
        raise AssertionError("saved catch proofs differ from fresh replay")

    source_count, source_layout = verify_sources()
    checks = {
        "required_files": True,
        "eleven_source_hashes": source_count == 11,
        "saved_equals_fresh": True,
        "independent_exact_configuration_enumeration": (
            saved_independent["status"] == "PASS"
            and saved_independent["cases"] == 2003
            and saved_independent["multi_image_cases"] > 0
            and saved_independent["one_image_cases"] > 0
        ),
        "fifteen_hostile_mutations": (
            saved_catches["status"] == "PASS"
            and len(saved_catches["cases"]) == 15
            and all(case["caught"] for case in saved_catches["cases"])
        ),
        "all_image_query_scoped": saved["query"] == "ALL_REGULAR_NULL_IMAGES_COUNTED_ONCE",
        "arbitrary_branch_weights_absent": saved["uses_arbitrary_branch_weights"] is False,
        "single_image_zero_sibling": saved["one_image_control"]["S"]["exact"] == "0/1",
        "multibranch_positive_sibling": saved["witness"]["S"]["numerator"] > 0,
        "g239_exact_gamma": saved["g239_two_cell_control"]["Gamma"][0][1]["exact"] == "1/12",
        "regular_stratum_ceiling": (
            saved["general_theorem_scope"] == "MEASURABLE_LOCALLY_FINITE_PROPER_REGULAR_IMAGE_RELATION"
        ),
        "history_anchor_and_outcomes_open": (
            saved["physical_history_selected"] is False
            and saved["observational_anchor_used"] is False
            and saved["boss_outcomes_opened"] is False
        ),
        "landing_exact": saved["landing"] == LANDING,
        "typed_ledgers": len(read_tsv(ROOT / "PREMISE_LEDGER.tsv")) == 11
        and len(read_tsv(ROOT / "STATUS_LEDGER.tsv")) == 8
        and len(read_tsv(ROOT / "OPERATOR_LEDGER.tsv")) == 13,
    }
    if not all(checks.values()):
        raise AssertionError("one or more package checks failed")
    return {
        "audit": "G240_PACKAGE_VERIFICATION",
        "status": "PASS",
        "source_layout": source_layout,
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    result = build_verification()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.no_write:
        print(payload, end="")
    else:
        OUTPUT.write_text(payload, encoding="utf-8")
        print(payload, end="")


if __name__ == "__main__":
    main()
