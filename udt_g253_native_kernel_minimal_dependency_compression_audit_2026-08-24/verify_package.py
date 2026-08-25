#!/usr/bin/env python3
"""Strict package and no-write replay verifier for G253."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path


PKG = Path(__file__).resolve().parent
ROOT = PKG.parent
REQUIRED = {
    "MAP.md",
    "PREREGISTRATION.md",
    "SOURCE_MANIFEST.tsv",
    "PREMISE_LEDGER.tsv",
    "NODE_LEDGER.tsv",
    "LOAD_BEARING_EDGE_LEDGER.tsv",
    "MINIMAL_SOURCE_CUT.tsv",
    "HISTORICAL_CONTROL_DISPOSITION.tsv",
    "EXACT_DERIVATION.md",
    "AUDIT_REPORT.md",
    "LAY_REPORT.md",
    "EVIDENCE_GATES.md",
    "STATUS_LEDGER.tsv",
    "COMMANDS.md",
    "RUN_RECORD.md",
    "DERIVATION_RESULT.json",
    "INDEPENDENT_VERIFICATION.json",
    "CATCH_PROOF_RESULT.json",
    "derive_native_kernel_compression.py",
    "verify_native_kernel_compression_independent.py",
    "run_catch_proofs.py",
    "verify_package.py",
    "build_review_intake.py",
    "REVIEW_REQUEST.md",
    "EXTERNAL_REVIEW_GPT54.md",
    "EXTERNAL_REPAIR_FOLLOWUP_GPT54.md",
    "REPAIR_PREREGISTRATION.md",
    "REPAIR_IMPLEMENTATION.md",
    "REPAIR_SEALED_REPLAY.md",
    "REPAIR_FOLLOWUP_REQUEST.md",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve_source(relpath: str, expected_sha256: str) -> Path:
    candidates = (ROOT / relpath, ROOT / "sources" / relpath)
    existing = [path for path in candidates if path.is_file()]
    assert existing, ("missing_source", relpath)
    actual = {path: sha256(path) for path in existing}
    assert all(value == expected_sha256 for value in actual.values()), (
        "source_hash_mismatch",
        relpath,
        {str(path): value for path, value in actual.items()},
    )
    return existing[0]


def replay(script: str) -> dict[str, object]:
    completed = subprocess.run(
        [sys.executable, str(PKG / script), "--no-write"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def main() -> None:
    present = {path.name for path in PKG.iterdir() if path.is_file()}
    missing = sorted(REQUIRED - present)
    assert not missing, missing

    with (PKG / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        manifest = list(csv.DictReader(handle, delimiter="\t"))
    assert len(manifest) == 21
    for row in manifest:
        resolve_source(row["path"], row["sha256"])

    before = {
        name: sha256(PKG / name)
        for name in ("DERIVATION_RESULT.json", "INDEPENDENT_VERIFICATION.json", "CATCH_PROOF_RESULT.json")
    }
    production = replay("derive_native_kernel_compression.py")
    independent = replay("verify_native_kernel_compression_independent.py")
    catches = replay("run_catch_proofs.py")
    after = {name: sha256(PKG / name) for name in before}
    assert before == after

    assert production == json.loads((PKG / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    assert independent == json.loads((PKG / "INDEPENDENT_VERIFICATION.json").read_text(encoding="utf-8"))
    assert catches == json.loads((PKG / "CATCH_PROOF_RESULT.json").read_text(encoding="utf-8"))
    assert production["unsupported_edges"] == 0
    assert independent["production_module_imported"] is False
    assert independent["production_output_read"] is False
    assert catches["caught_count"] == 23
    assert catches["path_resolution_positive_controls"] == 2

    report = (PKG / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    for term in (
        "MIXED_STATUS_NATIVE_CHAIN_COMPRESSES",
        "DIRECT_RECIPROCAL_REDSHIFT_IS_CONDITIONAL",
        "ANGULAR_RESPONSE_IS_A_DISTINCT_SIBLING",
        "ABSOLUTE_SCALE_ATTACHMENT_IS_DOWNSTREAM",
        "external repair-only follow-up accepted",
    ):
        assert term in report

    print(json.dumps({
        "verdict": "PACKAGE_PASS",
        "required_files": len(REQUIRED),
        "manifest_sources": len(manifest),
        "no_write_replay": True,
        "production_result_match": True,
        "independent_result_match": True,
        "catch_result_match": True,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
