#!/usr/bin/env python3
"""Build the sealed, self-contained G325 R1 repair-only follow-up intake."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


PACKAGE_FILES = (
    "MAP.md",
    "PREREGISTRATION.md",
    "PREMISE_LEDGER.tsv",
    "COMPLETENESS_MAP.md",
    "EXACT_DERIVATION.md",
    "LAY_REPORT.md",
    "EVIDENCE_GATES.md",
    "STATUS_LEDGER.tsv",
    "RUN_RECORD.md",
    "REPLAY_COMMANDS.txt",
    "SOURCE_SCOPE.tsv",
    "derive_modes.py",
    "verify_independent.py",
    "run_catch_proofs.py",
    "verify_package.py",
    "verify_review_intake.py",
    "build_repair_followup_intake.py",
    "DERIVATION_RESULT.json",
    "INDEPENDENT_VERIFICATION.json",
    "CATCH_PROOF_RESULT.json",
    "ADVERSARIAL_REVIEW_REQUEST.md",
    "EXTERNAL_REVIEW_RESPONSE.md",
    "EXTERNAL_REVIEW_FINAL_RESPONSE.md",
    "EXTERNAL_REVIEW_TRANSCRIPT.txt",
    "EXTERNAL_REVIEW_TRANSMISSION.md",
    "REPAIR_LEDGER.tsv",
    "REPAIR_FOLLOWUP_REQUEST.md",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    package = Path(__file__).resolve().parent
    repository = package.parent
    source_commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repository, check=True, capture_output=True, text=True
    ).stdout.strip()
    destination = Path(tempfile.mkdtemp(prefix="udt_g325_repair_followup_", dir="/tmp"))
    payloads: list[Path] = []

    for name in PACKAGE_FILES:
        source = package / name
        if not source.is_file():
            raise FileNotFoundError(source)
        target = destination / name
        shutil.copy2(source, target)
        payloads.append(target)

    with (package / "SOURCE_SCOPE.tsv").open(newline="") as handle:
        source_rows = list(csv.DictReader(handle, delimiter="\t"))
    for row in source_rows:
        source = repository / row["relative_path"]
        if not source.is_file():
            raise FileNotFoundError(source)
        target = destination / "sources" / row["relative_path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        payloads.append(target)

    scope_path = destination / "REVIEW_SCOPE.json"
    scope = {
        "schema": "udt-g325-r1-repair-followup-scope-v1",
        "source_commit": source_commit,
        "purpose": "read-only repair-only verification of G325 R1",
        "manifest_payload_count": len(payloads) + 1,
        "evidence_read_only": True,
        "research_continuation_allowed": False,
        "repository_access_allowed": False,
        "protected_package_access_allowed": False,
        "internet_browsing_allowed": False,
        "ephemeral_copy_checks_allowed": True,
        "allowed_question": "R1 removal of one vacuous production assertion and unchanged bounded G325 landing",
        "law_history_scale_selection_allowed": False,
    }
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n")
    payloads.append(scope_path)

    # Prove the corrected package replays exactly before sealing it.
    subprocess.run(
        [sys.executable, "-S", str(destination / "verify_package.py")],
        cwd=destination,
        check=True,
        capture_output=True,
        text=True,
    )

    manifest = destination / "REVIEW_MANIFEST.tsv"
    with manifest.open("w", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("relative_path", "bytes", "sha256"))
        for path in sorted(payloads, key=lambda item: item.relative_to(destination).as_posix()):
            writer.writerow((
                path.relative_to(destination).as_posix(), path.stat().st_size, digest(path)
            ))
    seal = destination / "REVIEW_MANIFEST.sha256"
    seal.write_text(digest(manifest) + "\n")

    subprocess.run(
        [sys.executable, "-S", str(destination / "verify_review_intake.py")],
        cwd=destination,
        check=True,
        capture_output=True,
        text=True,
    )

    for path in destination.rglob("*"):
        path.chmod(0o555 if path.is_dir() else 0o444)
    destination.chmod(0o555)

    print(json.dumps({
        "intake": str(destination),
        "manifest_payload_count": len(payloads),
        "total_file_count": len(payloads) + 2,
        "scope_sha256": digest(scope_path),
        "manifest_sha256": digest(manifest),
        "detached_seal_sha256": digest(seal),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
