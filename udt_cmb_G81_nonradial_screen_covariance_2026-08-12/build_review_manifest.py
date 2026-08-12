#!/usr/bin/env python3
"""Build the deterministic sealed G81 review manifest."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PACKAGE_FILES = (
    "AUDIT_REPORT.md", "CATCH_PROOF_RESULTS.json", "CONTROL_UNIVERSE.tsv",
    "DERIVATION_RESULT.json", "DERIVATION_STDOUT.txt", "EXACT_ALGEBRA_RESULT.json",
    "EXACT_DERIVATION.md", "INDEPENDENT_METHOD_REGISTRATION.md", "INDEPENDENT_TRANSCRIPT.txt",
    "INDEPENDENT_VERIFICATION.json", "LAY_REPORT.md", "PACKAGE_VERIFICATION.json",
    "PATH_EVIDENCE.npz", "PREMISE_LEDGER.tsv", "PREREGISTRATION.md", "REFINEMENT_ATLAS.tsv",
    "REPOSITORY_GATES.json", "REVIEW_DISPATCH.md", "SEMANTIC_CONTRACT.json", "SOURCE_MANIFEST.tsv", "TYPE_LEDGER.tsv",
    "build_review_manifest.py", "derive_nonradial_screen_covariance.py", "run_catch_proofs.py",
    "verify_exact_algebra.py", "verify_nonradial_neighboring_rays.py", "verify_package.py",
    "verify_repository_gates.py",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    for name in PACKAGE_FILES:
        path = HERE / name
        relative = str(path.relative_to(ROOT))
        assert path.is_file() and relative not in seen
        seen.add(relative)
        rows.append({"path": relative, "sha256": digest(path), "role": "G81_package"})
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        for source in csv.DictReader(stream, delimiter="\t"):
            relative = source["path"]
            assert relative not in seen
            path = ROOT / relative
            assert path.is_file() and digest(path) == source["sha256"]
            seen.add(relative)
            rows.append({"path": relative, "sha256": source["sha256"], "role": source["role"]})
    rows.sort(key=lambda row: row["path"])
    with (HERE / "REVIEW_MANIFEST.tsv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=("path", "sha256", "role"), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    assert len(rows) == len(seen) == 37
    print("PASS: 37 unique G81 payload files; sealed intake count including manifest = 38")


if __name__ == "__main__":
    main()
