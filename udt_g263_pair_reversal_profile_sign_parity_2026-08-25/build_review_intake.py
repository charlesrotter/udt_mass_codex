#!/usr/bin/env python3
"""Build the fresh sealed G263 adversarial-review intake."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import tempfile
from pathlib import Path


PACKAGE_NAME = "udt_g263_pair_reversal_profile_sign_parity_2026-08-25"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    package = Path(__file__).resolve().parent
    repo = package.parent
    target = Path(tempfile.mkdtemp(prefix="udt_g263_review_"))

    source_paths: set[str] = set()
    with (package / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            source = repo / row["path"]
            if sha(source) != row["sha256"]:
                raise AssertionError(f"source hash changed: {row['path']}")
            source_paths.add(row["path"])

    package_names = (
        "ADVERSARIAL_REVIEW_REQUEST.md",
        "AUDIT_REPORT.md",
        "CATCH_PROOF_RESULT.json",
        "DERIVATION_RESULT.json",
        "EVIDENCE_GATES.md",
        "EXACT_DERIVATION.md",
        "INDEPENDENT_VERIFICATION.json",
        "LAY_REPORT.md",
        "MAP.md",
        "OWNERSHIP_ATLAS.tsv",
        "PREMISE_LEDGER.tsv",
        "PREREGISTRATION.md",
        "RUN_RECORD.md",
        "SOURCE_MANIFEST.tsv",
        "STATUS_LEDGER.tsv",
        "VERIFICATION_RESULT.json",
        "build_review_intake.py",
        "derive_parity.py",
        "run_catch_proofs.py",
        "verify_independent.py",
        "verify_package.py",
    )
    package_files = {f"{PACKAGE_NAME}/{name}" for name in package_names}
    payloads = sorted(source_paths | package_files)
    manifest_rows: list[tuple[str, str, int]] = []
    for relative in payloads:
        source = repo / relative
        if not source.is_file():
            raise FileNotFoundError(relative)
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        manifest_rows.append((relative, sha(destination), destination.stat().st_size))

    manifest = target / "REVIEW_MANIFEST.tsv"
    with manifest.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("path", "sha256", "bytes"))
        writer.writerows(manifest_rows)

    scope = {
        "purpose": "fresh read-only adversarial G263 parity review",
        "payload_count": len(manifest_rows),
        "total_file_count_including_manifest_and_scope": len(manifest_rows) + 2,
        "review_manifest_sha256": sha(manifest),
        "permissions": {
            "inspect_only_this_intake": True,
            "run_registered_replays_or_bounded_checks_in_ephemeral_copy": True,
            "edit_evidence_files": False,
            "continue_research": False,
            "access_repository_or_protected_packages": False,
        },
    }
    scope_path = target / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(target)
    print(f"payload_count={len(manifest_rows)}")
    print(f"total_file_count={len(manifest_rows) + 2}")
    print(f"manifest_sha256={sha(manifest)}")
    print(f"scope_sha256={sha(scope_path)}")


if __name__ == "__main__":
    main()
