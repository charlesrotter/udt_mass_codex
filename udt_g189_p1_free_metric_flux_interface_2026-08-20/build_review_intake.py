#!/usr/bin/env python3
"""Build a sealed G189 review intake from exactly the registered package and sources."""

from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DES_ROOT = Path(os.environ["G189_DES_ROOT"])
PACKAGE_FILES = (
    "PREREGISTRATION.md",
    "SCOPE_CORRECTION_PREREGISTRATION.md",
    "EXTERNAL_REVIEW_REPAIR_PREREGISTRATION.md",
    "TRANSMISSION_RECORD.md",
    "EXTERNAL_REVIEW_RAW.md",
    "EXTERNAL_REVIEW_TRANSCRIPT.txt.gz",
    "EXTERNAL_REVIEW_ADJUDICATION.md",
    "EXTERNAL_REVIEW_FOLLOWUP_REQUEST.md",
    "EXTERNAL_REVIEW_FOLLOWUP_RAW.md",
    "EXTERNAL_REVIEW_FOLLOWUP_TRANSCRIPT.txt.gz",
    "EXTERNAL_REVIEW_FOLLOWUP_TRANSMISSION_RECORD.md",
    "SOURCE_MANIFEST.tsv",
    "ADVERSARIAL_REVIEW_REQUEST.md",
    "EXACT_DERIVATION.md",
    "AUDIT_REPORT.md",
    "LAY_REPORT.md",
    "EVIDENCE_GATES.md",
    "STATUS_LEDGER.tsv",
    "derive_p1_free_flux_interface.py",
    "verify_p1_free_flux_independent.py",
    "run_catch_proofs.py",
    "verify_package.py",
    "build_review_intake.py",
    "PRODUCTION_RESULT.json",
    "INDEPENDENT_VERIFICATION.json",
    "CATCH_PROOF_RESULT.json",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def main() -> None:
    intake = Path(tempfile.mkdtemp(prefix="udt_g189_review_"))
    package_target = intake / HERE.name
    for name in PACKAGE_FILES:
        copy_file(HERE / name, package_target / name)

    with (HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    for row in rows:
        registered = Path(row["path"])
        if registered.parts and registered.parts[0] == "external_data":
            source = DES_ROOT / registered.name
        else:
            source = ROOT / registered
        if sha256(source) != row["sha256"]:
            raise RuntimeError(f"source hash mismatch: {registered}")
        target = intake / registered
        copy_file(source, target)

    entries = []
    for path in sorted(candidate for candidate in intake.rglob("*") if candidate.is_file()):
        entries.append(
            {
                "path": str(path.relative_to(intake)),
                "sha256": sha256(path),
                "bytes": path.stat().st_size,
            }
        )
    scope = {
        "audit": "G189_EXTERNAL_REVIEW_INTAKE",
        "file_count_excluding_scope": len(entries),
        "files": entries,
        "restrictions": [
            "read-only",
            "inspect only this intake",
            "do not edit files",
            "do not continue the research",
        ],
        "replay": (
            'G189_DES_ROOT="$PWD/external_data" '
            "python3 udt_g189_p1_free_metric_flux_interface_2026-08-20/verify_package.py"
        ),
    }
    scope_path = intake / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "intake": str(intake),
                "file_count_total": len(entries) + 1,
                "review_scope_sha256": sha256(scope_path),
                "bytes_total": sum(item["bytes"] for item in entries) + scope_path.stat().st_size,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
