#!/usr/bin/env python3
"""Build a sealed, self-contained, read-only-review intake for G279."""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import tempfile
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
PACKAGE_NAME = PACKAGE.name

PACKAGE_FILES = [
    "MAP.md",
    "PREREGISTRATION.md",
    "PREREGISTRATION_EXECUTION_NOTE.md",
    "PREMISE_LEDGER.tsv",
    "SOURCE_SCOPE.tsv",
    "SOURCE_MANIFEST.tsv",
    "EXACT_REDERIVATION.md",
    "AUDIT_REPORT.md",
    "LAY_REPORT.md",
    "STATUS_LEDGER.tsv",
    "EVIDENCE_GATES.md",
    "COMMANDS.md",
    "REVIEW_REQUEST.md",
    "DEPENDENCY_LEDGER.tsv",
    "DERIVATION_RESULT.json",
    "INDEPENDENT_VERIFICATION.json",
    "SUBTRACTION_RESULT.json",
    "CATCH_PROOF_RESULT.json",
    "freeze_source_manifest.py",
    "derive_native_provenance.py",
    "verify_native_chain_independent.py",
    "run_dependency_subtractions.py",
    "run_catch_proofs.py",
    "verify_package.py",
    "build_review_intake.py",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="") as handle:
        source_rows = list(csv.DictReader(handle, delimiter="\t"))
    assert len(source_rows) == 31

    destination = Path(tempfile.mkdtemp(prefix="udt_g279_review_"))
    package_destination = destination / PACKAGE_NAME
    package_destination.mkdir(parents=True)

    for name in PACKAGE_FILES:
        source = PACKAGE / name
        assert source.is_file(), name
        shutil.copy2(source, package_destination / name)

    for row in source_rows:
        source = ROOT / row["path"]
        assert source.is_file(), row["path"]
        assert source.stat().st_size == int(row["bytes"])
        assert sha256(source) == row["sha256"]
        target = destination / row["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            assert sha256(target) == row["sha256"]
        else:
            shutil.copy2(source, target)

    scope = {
        "audit": "G279_NATIVE_KERNEL_OBSERVATIONAL_INTERFACE_PROVENANCE_AUDIT",
        "mode": "fresh_read_only_adversarial_review",
        "question": (
            "Does the exact bounded F1-F4/W1-to-G278 chain preserve the native reciprocal kernel "
            "while keeping transfer, finite representation, Cepheid attachment, and DES conventions "
            "explicitly downstream; and are W5/angular siblings absent from the G278 executable path?"
        ),
        "allowed_actions": [
            "inspect only sealed intake files",
            "run registered no-write replays or bounded checks in a writable ephemeral copy",
            "challenge status grades, dependency edges, subtraction logic, and conclusion ceiling",
        ],
        "forbidden_actions": [
            "edit evidence files",
            "continue the research",
            "access repository files outside the intake",
            "access protected packages",
            "inspect unsealed observational outcomes",
            "fit or select a kernel, history, scale, resolution, or X_max",
        ],
        "registered_commands": [
            f"cd {PACKAGE_NAME} && python3 freeze_source_manifest.py",
            f"cd {PACKAGE_NAME} && python3 derive_native_provenance.py",
            f"cd {PACKAGE_NAME} && python3 verify_native_chain_independent.py",
            f"cd {PACKAGE_NAME} && python3 run_dependency_subtractions.py",
            f"cd {PACKAGE_NAME} && python3 run_catch_proofs.py",
            f"cd {PACKAGE_NAME} && python3 verify_package.py",
        ],
        "maximum_conclusion": (
            "source-bounded provenance certification only; no physical history, native light law, "
            "unique scale, representation-independent SNe state, W1/W5 canonization, or X_max"
        ),
    }
    scope_path = destination / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n")

    manifest_path = destination / "REVIEW_MANIFEST.tsv"
    payloads = sorted(
        path for path in destination.rglob("*")
        if path.is_file() and path.name not in {"REVIEW_MANIFEST.tsv", "REVIEW_MANIFEST.sha256"}
    )
    with manifest_path.open("w", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["path", "bytes", "sha256"])
        for path in payloads:
            writer.writerow([path.relative_to(destination), path.stat().st_size, sha256(path)])

    seal_path = destination / "REVIEW_MANIFEST.sha256"
    seal_path.write_text(f"{sha256(manifest_path)}  REVIEW_MANIFEST.tsv\n")
    result = {
        "intake": str(destination),
        "manifest_payload_count": len(payloads),
        "total_file_count": len(payloads) + 2,
        "scope_sha256": sha256(scope_path),
        "manifest_sha256": sha256(manifest_path),
        "manifest_seal_sha256": sha256(seal_path),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
