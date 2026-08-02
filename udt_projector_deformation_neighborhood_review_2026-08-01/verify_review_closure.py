#!/usr/bin/env python3
"""Fail-closed verification of the frozen external semantic-review layer."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "udt_projector_deformation_neighborhood_audit_2026-08-01"
TARGET_COMMIT = "514f6ad"
TARGET_MANIFEST_SHA = "58dd9b3f272119db42757d5c66f00efd1ac26b6e2288bf92a479e547fe2bfeab"
REVIEW_SHA = "d11264704b5a2e892fffb6e8f903f53111a3dc9104377ad5f85ed1f05c5591c9"
TRANSCRIPT_SHA = "b6735c697092a987fb1e8f839a090583bb062a837f00c149d79b8d7c18a1fe4f"
MAXIMUM = (
    "DERIVED_CONDITIONAL_ON_THE_REGISTERED_STATIONARY_COMPLETE_OFFSHELL_FAMILY:\n"
    "EACH_C01_C06_CENTER_LIES_IN_AN_OPEN_CONFIGURATION_NEIGHBORHOOD_WITH_THE\n"
    "INTRINSIC_CLOCK_RULER_PROJECTOR_GATES_AND_NONZERO_RELATIVE_CURVATURE_SOMEWHERE."
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def validate_review(review: bytes, result: dict[str, object]) -> None:
    text = review.decode("utf-8")
    assert digest(review) == REVIEW_SHA
    assert text.startswith("`PASS`\n")
    assert "**Mandatory repairs**\n- None." in text
    assert MAXIMUM in text
    assert text.rstrip().endswith("Nothing stronger is justified from this package.")
    assert result["status"] == "PASS"
    assert result["mandatory_repairs"] == 0
    assert result["claim_rulings_sustained"] == 10
    assert result["target_manifest_sha256_before"] == TARGET_MANIFEST_SHA
    assert result["target_manifest_sha256_after"] == TARGET_MANIFEST_SHA


def target_manifest_checks() -> int:
    manifest_path = TARGET / "PACKAGE_MANIFEST.sha256"
    assert digest(manifest_path.read_bytes()) == TARGET_MANIFEST_SHA
    count = 0
    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        expected, name = line.split(None, 1)
        path = TARGET / name.strip()
        assert path.is_file() and digest(path.read_bytes()) == expected
        count += 1
    diff = subprocess.run(
        ["git", "diff", "--quiet", TARGET_COMMIT, "--", TARGET.name],
        cwd=ROOT,
        check=False,
    )
    assert diff.returncode == 0
    return count


def source_scope_checks() -> int:
    with (TARGET / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    assert len(rows) == len({row["path"] for row in rows}) == 15
    assert all(row["unchanged_at_freeze"] == "YES" for row in rows)
    transmission = (HERE / "TRANSMISSION_SCOPE.tsv").read_text(encoding="utf-8")
    assert "15_rows_in_target_SOURCE_MANIFEST.tsv\tREAD_ONLY" in transmission
    return len(rows)


def mutation_catches(review: bytes, result: dict[str, object]) -> int:
    caught = 0
    mutations = [
        review.replace(b"`PASS`", b"`FAIL`", 1),
        review.replace(b"- None.", b"- Rewrite the theorem.", 1),
        review.replace(b"Nothing stronger", b"A stability theorem stronger", 1),
        review.replace(b"C01_C06", b"C01_C99", 1),
    ]
    for mutation in mutations:
        try:
            validate_review(mutation, result)
        except AssertionError:
            caught += 1
    altered = dict(result)
    altered["target_manifest_sha256_after"] = "0" * 64
    try:
        validate_review(review, altered)
    except AssertionError:
        caught += 1
    altered = dict(result)
    altered["mandatory_repairs"] = 1
    try:
        validate_review(review, altered)
    except AssertionError:
        caught += 1
    assert caught == 6
    return caught


def main() -> int:
    review = (HERE / "EXTERNAL_REVIEW.md").read_bytes()
    transcript = (HERE / "EXTERNAL_REVIEW_TRANSCRIPT.txt").read_bytes()
    result = json.loads((HERE / "EXTERNAL_REVIEW_RESULT.json").read_text(encoding="utf-8"))
    validate_review(review, result)
    assert len(review) == 4938
    assert len(transcript) == 208379 and digest(transcript) == TRANSCRIPT_SHA
    assert result["accepted_review_sha256"] == REVIEW_SHA
    assert result["transcript_sha256"] == TRANSCRIPT_SHA
    target_files = target_manifest_checks()
    source_rows = source_scope_checks()
    catches = mutation_catches(review, result)
    verification = {
        "schema": "udt.projector_deformation_neighborhood.external_review.v1",
        "status": "PASS",
        "review_verdict": "PASS",
        "mandatory_repairs": 0,
        "review_sha256": REVIEW_SHA,
        "transcript_sha256": TRANSCRIPT_SHA,
        "target_manifest_sha256": TARGET_MANIFEST_SHA,
        "target_manifest_files": target_files,
        "frozen_source_rows": source_rows,
        "mutation_catches": catches,
        "target_package_unchanged_since_evidence_commit": True,
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(
        json.dumps(verification, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(verification, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
