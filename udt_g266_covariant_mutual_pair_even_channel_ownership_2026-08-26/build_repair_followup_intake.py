#!/usr/bin/env python3
"""Build a self-contained sealed G266 repair-only follow-up intake."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path


PACKAGE_NAME = "udt_g266_covariant_mutual_pair_even_channel_ownership_2026-08-26"
SOURCE_COMMIT = "f17ba07f5253365dde1b80128872b31aa4092e18"


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def frozen_source(repo: Path, relative: str, expected: str) -> bytes:
    live = repo / relative
    if live.is_file() and sha(live) == expected:
        return live.read_bytes()
    data = subprocess.check_output(["git", "show", f"{SOURCE_COMMIT}:{relative}"], cwd=repo)
    if sha_bytes(data) != expected:
        raise AssertionError(f"frozen source mismatch: {relative}")
    return data


def main() -> None:
    package = Path(__file__).resolve().parent
    repo = package.parent
    target = Path(tempfile.mkdtemp(prefix="udt_g266_repair_followup_", dir="/tmp"))

    with (package / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        source_rows = list(csv.DictReader(handle, delimiter="\t"))

    package_names = (
        "ADVERSARIAL_REVIEW_REQUEST.md",
        "AUDIT_REPORT.md",
        "CATCH_PROOF_RESULT.json",
        "DERIVATION_RESULT.json",
        "EVIDENCE_GATES.md",
        "EXACT_DERIVATION.md",
        "EXTERNAL_REVIEW_GPT54.md",
        "EXTERNAL_REVIEW_REPAIR_PREREGISTRATION.md",
        "INDEPENDENT_VERIFICATION.json",
        "LAY_REPORT.md",
        "MAP.md",
        "PREMISE_LEDGER.tsv",
        "PREREGISTRATION.md",
        "PREREGISTRATION_EXECUTION_NOTE.md",
        "REPAIR_FOLLOWUP_REQUEST.md",
        "REPAIR_IMPLEMENTATION.md",
        "RUN_RECORD.md",
        "SOURCE_MANIFEST.tsv",
        "STATUS_LEDGER.tsv",
        "WITNESS_ATLAS.tsv",
        "build_repair_followup_intake.py",
        "build_review_intake.py",
        "derive_even_channel.py",
        "derive_even_channel_stdlib.py",
        "run_catch_proofs.py",
        "verify_independent.py",
        "verify_package.py",
    )

    payloads: dict[str, bytes] = {}
    for row in source_rows:
        relative = row["path"]
        payloads[f"private_sources/{relative}"] = frozen_source(
            repo, relative, row["sha256"]
        )
    for name in package_names:
        path = package / name
        if not path.is_file():
            raise FileNotFoundError(path)
        payloads[f"{PACKAGE_NAME}/{name}"] = path.read_bytes()

    manifest_rows = []
    for relative, data in sorted(payloads.items()):
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
        manifest_rows.append((relative, sha_bytes(data), len(data)))

    manifest = target / "REVIEW_MANIFEST.tsv"
    with manifest.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("path", "sha256", "bytes"))
        writer.writerows(manifest_rows)

    scope = {
        "purpose": "read-only repair-only G266 follow-up review",
        "payload_count": len(manifest_rows),
        "total_file_count_including_manifest_and_scope": len(manifest_rows) + 2,
        "review_manifest_sha256": sha(manifest),
        "permissions": {
            "inspect_only_this_intake": True,
            "verify_only_preregistered_repairs_r1_r4_and_unchanged_landing": True,
            "run_registered_no_write_replays_or_bounded_checks_in_ephemeral_copy": True,
            "edit_evidence_files": False,
            "continue_research": False,
            "inspect_observational_outcomes_or_protected_packages": False,
        },
    }
    scope_path = target / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "intake": str(target),
        "payload_count": len(manifest_rows),
        "file_count": len(manifest_rows) + 2,
        "manifest_sha256": sha(manifest),
        "scope_sha256": sha(scope_path),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
