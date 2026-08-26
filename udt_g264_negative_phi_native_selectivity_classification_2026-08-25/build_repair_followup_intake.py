#!/usr/bin/env python3
"""Build a sealed repair-only G264 follow-up intake."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import tempfile
from pathlib import Path


PACKAGE_NAME = "udt_g264_negative_phi_native_selectivity_classification_2026-08-25"
ORIGINAL_INTAKE = Path("/tmp/udt_g264_review_tme4dog9")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    package = Path(__file__).resolve().parent
    target = Path(tempfile.mkdtemp(prefix="udt_g264_repair_followup_"))
    if sha(ORIGINAL_INTAKE / "REVIEW_SCOPE.json") != (
        "1617c8f36792472db11e26a1d657e60dc0fc8195ee1c2181828b9e15d77650d2"
    ):
        raise AssertionError("original scope changed")
    if sha(ORIGINAL_INTAKE / "REVIEW_MANIFEST.tsv") != (
        "22b44394fe9d8bd75a2e9b17e8e2e1c65b9e0d89da897253084d8f2da00c9693"
    ):
        raise AssertionError("original manifest changed")

    payloads: list[tuple[str, Path]] = []
    for source in sorted(path for path in ORIGINAL_INTAKE.rglob("*") if path.is_file()):
        payloads.append((f"original_intake/{source.relative_to(ORIGINAL_INTAKE)}", source))

    repair_names = (
        "AUDIT_REPORT.md",
        "CATCH_PROOF_RESULT.json",
        "DERIVATION_RESULT.json",
        "EVIDENCE_GATES.md",
        "EXACT_DERIVATION.md",
        "EXTERNAL_REVIEW_GPT54.md",
        "INDEPENDENT_VERIFICATION.json",
        "METRIC_FIRST_VERIFICATION.json",
        "OWNERSHIP_ATLAS.tsv",
        "REPAIR_CATCH_RESULT.json",
        "REPAIR_FOLLOWUP_REQUEST.md",
        "REPAIR_PREREGISTRATION.md",
        "REPAIR_RESULT.md",
        "RUN_RECORD.md",
        "STATUS_LEDGER.tsv",
        "TRANSMISSION_RECORD.md",
        "VERIFICATION_RESULT.json",
        "derive_selectivity.py",
        "run_catch_proofs.py",
        "verify_independent.py",
        "verify_metric_first.py",
        "verify_package.py",
        "verify_repair_catches.py",
    )
    for name in repair_names:
        source = package / name
        if not source.is_file():
            raise FileNotFoundError(source)
        payloads.append((f"repaired/{PACKAGE_NAME}/{name}", source))

    rows: list[tuple[str, str, int]] = []
    for relative, source in sorted(payloads):
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        rows.append((relative, sha(destination), destination.stat().st_size))

    manifest = target / "REVIEW_MANIFEST.tsv"
    with manifest.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("path", "sha256", "bytes"))
        writer.writerows(rows)

    scope = {
        "purpose": "read-only G264 R1-R3 repair-only follow-up review",
        "payload_count": len(rows),
        "total_file_count_including_manifest_and_scope": len(rows) + 2,
        "review_manifest_sha256": sha(manifest),
        "original_scope_sha256": (
            "1617c8f36792472db11e26a1d657e60dc0fc8195ee1c2181828b9e15d77650d2"
        ),
        "original_manifest_sha256": (
            "22b44394fe9d8bd75a2e9b17e8e2e1c65b9e0d89da897253084d8f2da00c9693"
        ),
        "permissions": {
            "verify_only_registered_repairs_and_unchanged_landing": True,
            "run_checks_in_writable_ephemeral_copy": True,
            "edit_evidence_files": False,
            "continue_research": False,
        },
    }
    scope_path = target / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n")
    print(target)
    print(f"payload_count={len(rows)}")
    print(f"total_file_count={len(rows) + 2}")
    print(f"manifest_sha256={sha(manifest)}")
    print(f"scope_sha256={sha(scope_path)}")


if __name__ == "__main__":
    main()
