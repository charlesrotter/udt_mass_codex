#!/usr/bin/env python3
"""Fail-closed verification of the additions-only G78 external-review correction."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CORRECTION_PREREG = "2a78b8f6bb1e5ab8619dffd46ba180b92ddc13aa"
EXPECTED_REVIEW_MANIFEST = "bd86fbc470c9115f44c35e35f1d42b821e7fc885be7eb14752579b3192c3a1e4"
EXPECTED_REVIEW = "1a4be37909944fc86d70901b1891612ec6553bd8c4311ef35e3cc3d1403ff0b3"
EXPECTED_TRANSCRIPT = "149f598b7dd564e5c12a37b595a1f1f6c0efefeb6bea0712b7bdbf32eeb5920c"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def catches_fail(mutant: dict[str, object]) -> bool:
    try:
        assert mutant["review_manifest_sha256"] == EXPECTED_REVIEW_MANIFEST
        assert mutant["external_review_sha256"] == EXPECTED_REVIEW
        assert mutant["reviewed_source_rows"] == 20
        assert mutant["reviewed_route_rows"] == 7
        assert mutant["owned_native_routes"] == 0
        assert mutant["internal_independent_semantic_ownership_grade"] == (
            "REGRESSION_ONLY_NOT_INDEPENDENT_SEMANTIC_DERIVATION"
        )
        assert mutant["package_verifier_grade"] == "REPOSITORY_REGRESSION_NOT_SEALED_INTAKE_EVIDENCE"
        return False
    except AssertionError:
        return True


def main() -> None:
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", CORRECTION_PREREG, "HEAD"],
        cwd=ROOT,
        check=False,
    )
    assert ancestor.returncode == 0

    assert digest(HERE / "REVIEW_MANIFEST.tsv") == EXPECTED_REVIEW_MANIFEST
    assert digest(HERE / "EXTERNAL_REVIEW_RAW.md") == EXPECTED_REVIEW
    assert digest(HERE / "EXTERNAL_REVIEW_TRANSCRIPT.txt") == EXPECTED_TRANSCRIPT

    reviewed = table(HERE / "REVIEW_MANIFEST.tsv")
    assert len(reviewed) == len({row["path"] for row in reviewed}) == 38
    for row in reviewed:
        assert digest(ROOT / row["path"]) == row["sha256"]

    routes = table(HERE / "OWNER_ROUTE_LEDGER.tsv")
    assert len(routes) == len({row["route"] for row in routes}) == 7
    counts = Counter(row["status"] for row in routes)
    assert counts == Counter({
        "OPEN_NO_OWNER": 4,
        "COMPATIBILITY_ANCHOR_ONLY": 1,
        "NECESSARY_REQUIREMENT_ONLY": 1,
        "CONDITIONAL_IDENTIFIABILITY_ONLY": 1,
    })

    scope = table(HERE / "VERIFICATION_SCOPE_LEDGER.tsv")
    assert len(scope) == len({row["item"] for row in scope}) == 8
    grades = {row["item"]: row["grade"] for row in scope}
    assert grades["seven_route_status_regression"] == "REGRESSION_ONLY"
    assert grades["package_repository_gates"] == "REPOSITORY_REGRESSION_ONLY"
    assert grades["external_semantic_owner_challenge"] == "COLD_REVIEW_NO_CONTRADICTORY_OWNER_FOUND"
    assert grades["owner_join_landing"] == "VERIFIED_WITH_CAVEATS"

    result = json.loads((HERE / "EXTERNAL_REVIEW_RESULT.json").read_text(encoding="utf-8"))
    assert result["external_landing"] == "VERIFIED_WITH_CAVEATS"
    assert result["review_manifest_sha256"] == EXPECTED_REVIEW_MANIFEST
    assert result["external_review_sha256"] == EXPECTED_REVIEW
    assert result["external_transcript_sha256"] == EXPECTED_TRANSCRIPT
    assert result["correction_preregistration_commit"] == CORRECTION_PREREG
    assert result["reviewed_source_rows"] == 20
    assert result["reviewed_profile_rows"] == 591
    assert result["reviewed_route_rows"] == 7
    assert result["owned_native_routes"] == 0

    raw = (HERE / "EXTERNAL_REVIEW_RAW.md").read_text(encoding="utf-8")
    adjudication = (HERE / "EXTERNAL_REVIEW_ADJUDICATION.md").read_text(encoding="utf-8")
    assert "VERIFIED_WITH_CAVEATS" in raw
    for token in (
        "REGRESSION_ONLY_NOT_INDEPENDENT_SEMANTIC_DERIVATION",
        "REPOSITORY_REGRESSION_NOT_SEALED_INTAKE_EVIDENCE",
    ):
        assert token in json.dumps(result, sort_keys=True)
    for token in (
        "not an exhaustive theorem",
        "before comparing with P1",
        "CSN and does not make UDT scale-free",
        "No profile was ranked",
    ):
        assert token in adjudication

    mutations: dict[str, dict[str, object]] = {}
    for name, field, value in (
        ("wrong_review_manifest_hash", "review_manifest_sha256", "0" * 64),
        ("wrong_external_review_hash", "external_review_sha256", "0" * 64),
        ("source_scope_promotion", "reviewed_source_rows", 21),
        ("missing_route", "reviewed_route_rows", 6),
        ("owned_route_promotion", "owned_native_routes", 1),
        (
            "internal_semantic_independence_promotion",
            "internal_independent_semantic_ownership_grade",
            "INDEPENDENTLY_DERIVED",
        ),
        ("sealed_package_gate_promotion", "package_verifier_grade", "SEALED_INTAKE_EVIDENCE"),
    ):
        mutant = dict(result)
        mutant[field] = value
        mutations[name] = mutant
    catch_results = {name: catches_fail(mutant) for name, mutant in mutations.items()}
    assert len(catch_results) == 7 and all(catch_results.values())

    output = {
        "schema": "udt-cmb-g78-external-review-verification-v1",
        "status": "PASS",
        "reviewed_payload_files": len(reviewed),
        "reviewed_payload_bytes_unchanged": True,
        "source_rows": result["reviewed_source_rows"],
        "profile_rows": result["reviewed_profile_rows"],
        "route_rows": result["reviewed_route_rows"],
        "route_status_counts": dict(sorted(counts.items())),
        "owned_native_routes": result["owned_native_routes"],
        "scope_ledger_rows": len(scope),
        "catch_count": len(catch_results),
        "catch_proofs": catch_results,
        "external_landing": result["external_landing"],
    }
    (HERE / "EXTERNAL_REVIEW_VERIFICATION.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
