#!/usr/bin/env python3
"""Build the exact G74 sealed-review manifest."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PACKAGE_FILES = (
    "AUDIT_REPORT.md", "CATCH_PROOF_RESULTS.json", "CENTER_REGULARITY_ATLAS.tsv",
    "COMPLETENESS_SCOPE.md", "DERIVATION_RESULT.json", "EXACT_DERIVATION.md",
    "EXTERNAL_REVIEW_DISPATCH.md", "FALSIFICATION_CONTRACT.tsv",
    "INDEPENDENT_VERIFICATION_RESULT.json", "LAY_REPORT.md", "OWNERSHIP_LEDGER.tsv",
    "PACKAGE_VERIFICATION_RESULT.json", "PREMISE_LEDGER.tsv", "PREREGISTRATION.md",
    "REPOSITORY_GATES.json",
    "RELATION_TOPOLOGY_LEDGER.tsv", "RUN_RECORD.md", "SKY_ENDPOINTS.npz",
    "SKY_TOPOLOGY_ATLAS.tsv", "SOURCE_MANIFEST.tsv", "TYPE_LEDGER.tsv",
    "build_review_manifest.py", "derive_topology_atlas.py", "run_catch_proofs.py",
    "verify_package.py", "verify_repository_gates.py", "verify_topology_independent.py",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    source_rows = []
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        source_rows = list(csv.DictReader(stream, delimiter="\t"))
    paths = [str((HERE / name).relative_to(ROOT)) for name in PACKAGE_FILES]
    paths.extend(row["path"] for row in source_rows)
    assert len(paths) == len(set(paths))
    output = []
    for relative in paths:
        target = ROOT / relative
        assert target.is_file(), target
        output.append({"path": relative, "sha256": digest(target)})
    with (HERE / "REVIEW_MANIFEST.tsv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=("path", "sha256"), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(output)
    print(f"review_manifest_rows={len(output)}")


if __name__ == "__main__":
    main()
