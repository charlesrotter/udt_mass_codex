#!/usr/bin/env python3
"""Build the deterministic sealed-review manifest for G83."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PACKAGE_FILES = (
    "AUDIT_REPORT.md",
    "CATCH_PROOF_RESULT.json",
    "CONTINUED_PATH_ATLAS.tsv",
    "DERIVATION_RESULT.json",
    "DERIVATION_STDOUT.txt",
    "EXACT_DERIVATION.md",
    "FALSIFICATION_CONTRACT.tsv",
    "INDEPENDENT_RADAU_REPLAY.tsv",
    "INDEPENDENT_VERIFICATION.json",
    "LAPSE_FAMILY_CONTINUATION.tsv",
    "LAY_REPORT.md",
    "PREMISE_LEDGER.tsv",
    "PREREGISTRATION.md",
    "RECENTERED_ENDPOINT_LIMIT_ATLAS.tsv",
    "REPOSITORY_GATES.json",
    "REVIEW_DISPATCH.md",
    "SOURCE_MANIFEST.tsv",
    "STATUS_LEDGER.tsv",
    "STRICT_DOMAIN_ATLAS.tsv",
    "VERIFICATION_RESULT.json",
    "build_review_manifest.py",
    "derive_endpoint_asymptote_atlas.py",
    "run_catch_proofs.py",
    "verify_independent.py",
    "verify_package.py",
    "verify_repository_gates.py",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    rows: list[dict[str, str]] = []
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream, delimiter="\t"):
            path = ROOT / row["path"]
            assert path.is_file() and digest(path) == row["sha256"]
            rows.append({"path": row["path"], "sha256": row["sha256"], "role": "frozen_source"})
    for name in PACKAGE_FILES:
        path = HERE / name
        assert path.is_file(), path
        rows.append({"path": str(path.relative_to(ROOT)), "sha256": digest(path), "role": "G83_package"})
    assert len(rows) == 40
    assert len({row["path"] for row in rows}) == 40
    with (HERE / "REVIEW_MANIFEST.tsv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=("path", "sha256", "role"), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print({"manifest_rows": len(rows), "sealed_files_including_manifest": len(rows) + 1})


if __name__ == "__main__":
    main()
