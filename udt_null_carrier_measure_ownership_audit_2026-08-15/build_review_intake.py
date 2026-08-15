#!/usr/bin/env python3
"""Build a sealed review intake containing only G96 and its exact manifest-owned sources."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import shutil
import tempfile


REPO = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
PACKAGE_FILES = (
    "PREREGISTRATION.md",
    "PREMISE_LEDGER.tsv",
    "CANDIDATE_MEASURE_ATLAS.tsv",
    "SOURCE_CENSUS.tsv",
    "EXACT_DERIVATION.md",
    "AUDIT_REPORT.md",
    "LAY_REPORT.md",
    "STATUS_LEDGER.tsv",
    "derive_null_carrier_measure.py",
    "DERIVATION_RESULT.json",
    "verify_null_carrier_measure_independent.py",
    "INDEPENDENT_VERIFICATION.json",
    "verify_package.py",
    "VERIFICATION_RESULT.json",
    "run_catch_proofs.py",
    "CATCH_PROOF_RESULT.json",
    "SOURCE_MANIFEST.tsv",
    "REVIEW_DISPATCH.md",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    destination = Path(tempfile.mkdtemp(prefix="udt_null_carrier_review_", dir="/tmp"))
    package_destination = destination / PACKAGE.name
    package_destination.mkdir()
    records: list[dict[str, str]] = []

    for name in PACKAGE_FILES:
        source = PACKAGE / name
        target = package_destination / name
        shutil.copy2(source, target)
        records.append({"path": str(target.relative_to(destination)), "sha256": digest(target)})

    with (PACKAGE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            source = REPO / row["path"]
            target = destination / row["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            if digest(target) != row["sha256"]:
                raise SystemExit(f"source hash mismatch after copy: {row['path']}")
            records.append({"path": row["path"], "sha256": row["sha256"]})

    records.sort(key=lambda row: row["path"])
    scope = {
        "purpose": "fresh read-only adversarial G96 null-carrier measure review",
        "file_count_including_scope": len(records) + 1,
        "files": records,
        "forbidden": [
            "repository access outside intake",
            "internet access",
            "file edits",
            "research continuation",
            "protected package access",
        ],
    }
    scope_path = destination / "REVIEW_SCOPE.json"
    scope_path.write_text(json.dumps(scope, indent=2) + "\n", encoding="utf-8")
    print(destination)
    print(f"files={len(records)+1}")
    print(f"scope_sha256={digest(scope_path)}")


if __name__ == "__main__":
    main()
