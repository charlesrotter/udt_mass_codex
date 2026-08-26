#!/usr/bin/env python3
"""Build the sealed G263 repair-only external follow-up intake."""

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
    target = Path(tempfile.mkdtemp(prefix="udt_g263_repair_followup_"))

    source_paths: set[str] = set()
    with (package / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            source = repo / row["path"]
            if sha(source) != row["sha256"]:
                raise AssertionError(f"source hash changed: {row['path']}")
            source_paths.add(row["path"])

    package_names = (
        "AUDIT_REPORT.md",
        "CATCH_PROOF_RESULT.json",
        "DERIVATION_RESULT.json",
        "EVIDENCE_GATES.md",
        "EXACT_DERIVATION.md",
        "EXTERNAL_REVIEW_GPT54.md",
        "INDEPENDENT_VERIFICATION.json",
        "LAY_REPORT.md",
        "OWNERSHIP_ATLAS.tsv",
        "PREMISE_LEDGER.tsv",
        "PREREGISTRATION.md",
        "REPAIR_FOLLOWUP_REQUEST.md",
        "REPAIR_PREREGISTRATION.md",
        "REPAIR_RESULT.md",
        "REPAIR_CATCH_RESULT.json",
        "RUN_RECORD.md",
        "SEALED_REPLAY_RESULT.json",
        "SOURCE_MANIFEST.tsv",
        "STATUS_LEDGER.tsv",
        "TRANSMISSION_RECORD.md",
        "VERIFICATION_RESULT.json",
        "run_catch_proofs.py",
        "verify_package.py",
        "verify_repair_catches.py",
        "verify_sealed_replay.py",
    )
    package_files = {f"{PACKAGE_NAME}/{name}" for name in package_names}
    payloads = sorted(source_paths | package_files)
    rows: list[tuple[str, str, int]] = []
    for relative in payloads:
        source = repo / relative
        if not source.is_file():
            raise FileNotFoundError(relative)
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
        "purpose": "read-only repair-only G263 follow-up review",
        "repairs": ["R1_dependency_free_sealed_replay", "R2_mutation_escape_closure", "R3_independence_qualification"],
        "payload_count": len(rows),
        "total_file_count_including_manifest_and_scope": len(rows) + 2,
        "review_manifest_sha256": sha(manifest),
        "permissions": {
            "inspect_only_this_intake": True,
            "verify_only_registered_repairs_and_unchanged_landing": True,
            "run_registered_checks_in_writable_ephemeral_copy": True,
            "edit_evidence_files": False,
            "continue_research": False,
        },
    }
    scope_path = target / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(target)
    print(f"payload_count={len(rows)}")
    print(f"total_file_count={len(rows) + 2}")
    print(f"manifest_sha256={sha(manifest)}")
    print(f"scope_sha256={sha(scope_path)}")


if __name__ == "__main__":
    main()
