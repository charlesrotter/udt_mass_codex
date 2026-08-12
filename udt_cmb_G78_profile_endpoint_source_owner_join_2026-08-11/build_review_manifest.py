#!/usr/bin/env python3
"""Build the sealed G78 review manifest from package files and frozen sources."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PACKAGE_FILES = (
    "AUDIT_REPORT.md", "CATCH_PROOF_RESULTS.json", "DEPENDENCY_GRAPH.tsv",
    "DERIVATION_RESULT.json", "EXACT_DERIVATION.md", "INDEPENDENT_VERIFICATION.json",
    "OWNER_ROUTE_LEDGER.tsv", "PACKAGE_VERIFICATION.json", "PREMISE_LEDGER.tsv",
    "PREREGISTRATION.md", "REVIEW_DISPATCH.md", "SOURCE_ADJUDICATION.tsv",
    "SOURCE_MANIFEST.tsv", "build_review_manifest.py", "derive_owner_join.py",
    "run_catch_proofs.py", "verify_owner_join_independent.py", "verify_package.py",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    source_rows = list(csv.DictReader((HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8"), delimiter="\t"))
    output: list[tuple[str, str, str]] = []
    for name in PACKAGE_FILES:
        path = HERE / name
        assert path.is_file(), name
        output.append((str(path.relative_to(ROOT)), digest(path), "G78_package"))
    for row in source_rows:
        path = ROOT / row["path"]
        assert path.is_file(), row["path"]
        output.append((row["path"], digest(path), f"source_{row['role']}"))
    assert len(output) == len({row[0] for row in output}) == 38
    with (HERE / "REVIEW_MANIFEST.tsv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(("path", "sha256", "role"))
        writer.writerows(output)
    print("PASS: 38 unique G78 review payload files; sealed intake count including manifest = 39")


if __name__ == "__main__":
    main()
