#!/usr/bin/env python3
"""Build the exact sealed-review manifest for G85."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PACKAGE = (
    "PREREGISTRATION.md", "PREMISE_LEDGER.tsv", "FALSIFICATION_CONTRACT.tsv",
    "COMPLETION_ARCHETYPES.tsv", "SOURCE_MANIFEST.tsv", "AUDIT_REPORT.md",
    "EXACT_DERIVATION.md", "STATUS_LEDGER.tsv", "COMPLETENESS_SCOPE.md", "RUN_RECORD.md",
    "DERIVATION_RESULT.json", "PROFILE_ARCHETYPE_ATLAS.tsv", "SEAM_CHANNEL_ATLAS.tsv",
    "INDEPENDENT_VERIFICATION.json", "CATCH_PROOF_RESULT.json", "PACKAGE_VERIFICATION.json",
    "REPOSITORY_GATES.json", "derive_completion_atlas.py", "verify_independent.py",
    "run_catch_proofs.py", "verify_package.py", "verify_repository_gates.py", "REVIEW_DISPATCH.md",
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_rows() -> list[dict[str, str]]:
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def main() -> None:
    records: list[dict[str, str]] = []
    for name in PACKAGE:
        path = HERE / name
        assert path.is_file()
        relative = path.relative_to(ROOT).as_posix()
        records.append({"path": relative, "sha256": sha(path), "role": "g85_package"})
    for row in source_rows():
        path = ROOT / row["path"]
        assert path.is_file() and sha(path) == row["sha256"]
        records.append({"path": row["path"], "sha256": row["sha256"], "role": "frozen_source"})
    assert len(records) == len({row["path"] for row in records}) == 34
    with (HERE / "REVIEW_MANIFEST.tsv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=("path", "sha256", "role"), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)
    print(f"PASS: {len(records)} payloads; manifest_sha256={sha(HERE / 'REVIEW_MANIFEST.tsv')}")


if __name__ == "__main__":
    main()
