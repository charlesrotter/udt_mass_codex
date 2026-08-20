#!/usr/bin/env python3
"""Build a sealed G190 review intake from exactly the registered package and sources."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import shutil
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PACKAGE_FILES = (
    "PREREGISTRATION.md",
    "PONDER_MAP.md",
    "PREMISE_LEDGER.tsv",
    "SOURCE_MANIFEST.tsv",
    "ADVERSARIAL_REVIEW_REQUEST.md",
    "EXACT_DERIVATION.md",
    "AUDIT_REPORT.md",
    "LAY_REPORT.md",
    "EVIDENCE_GATES.md",
    "STATUS_LEDGER.tsv",
    "COMMANDS.md",
    "derive_timelive_frequency_screen.py",
    "verify_timelive_frequency_screen_independent.py",
    "run_catch_proofs.py",
    "build_source_manifest.py",
    "verify_package.py",
    "build_review_intake.py",
    "PRODUCTION_RESULT.json",
    "INDEPENDENT_VERIFICATION.json",
    "CATCH_PROOF_RESULT.json",
    "PACKAGE_VERIFICATION_RESULT.json",
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
    intake = Path(tempfile.mkdtemp(prefix="udt_g190_review_"))
    target_package = intake / HERE.name
    for name in PACKAGE_FILES:
        source = HERE / name
        if not source.is_file():
            raise FileNotFoundError(name)
        copy_file(source, target_package / name)

    with (HERE / "SOURCE_MANIFEST.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    for row in rows:
        source = ROOT / row["path"]
        if sha256(source) != row["sha256"] or source.stat().st_size != int(row["bytes"]):
            raise RuntimeError(f"source mismatch: {row['path']}")
        copy_file(source, intake / row["path"])

    entries = []
    for path in sorted(item for item in intake.rglob("*") if item.is_file()):
        entries.append(
            {
                "path": str(path.relative_to(intake)),
                "sha256": sha256(path),
                "bytes": path.stat().st_size,
            }
        )
    scope = {
        "audit": "G190_EXTERNAL_REVIEW_INTAKE",
        "file_count_excluding_scope": len(entries),
        "files": entries,
        "restrictions": [
            "read-only",
            "inspect only this intake",
            "do not edit files",
            "do not continue the research",
        ],
        "replay": (
            "python3 "
            "udt_g190_completed_pair_timelive_frequency_screen_join_2026-08-20/verify_package.py --no-write"
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
