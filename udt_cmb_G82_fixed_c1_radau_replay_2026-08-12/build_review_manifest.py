#!/usr/bin/env python3
"""Build the deterministic G82 sealed-review manifest."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PACKAGE = (
    "AUDIT_REPORT.md",
    "CATCH_PROOF_RESULTS.json",
    "CONTROL_UNIVERSE.tsv",
    "DERIVATION_RESULT.json",
    "DERIVATION_STDOUT.txt",
    "INDEPENDENT_VERIFICATION.json",
    "LAY_REPORT.md",
    "PACKAGE_VERIFICATION.json",
    "PREMISE_LEDGER.tsv",
    "PREREGISTRATION.md",
    "REPOSITORY_GATES.json",
    "REVIEW_DISPATCH.md",
    "SEMANTIC_CONTRACT.json",
    "SOURCE_MANIFEST.tsv",
    "build_review_manifest.py",
    "replay_fixed_c1_radau.py",
    "run_catch_proofs.py",
    "verify_package.py",
    "verify_repository_gates.py",
    "verify_result_independent.py",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    rows: list[tuple[str, str, str]] = []
    with (HERE / "SOURCE_MANIFEST.tsv").open(newline="", encoding="utf-8") as stream:
        for source in csv.DictReader(stream, delimiter="\t"):
            path = source["path"]
            assert digest(ROOT / path) == source["sha256"]
            rows.append((path, source["sha256"], "frozen_source"))
    for name in PACKAGE:
        path = HERE / name
        assert path.is_file()
        rows.append((str(path.relative_to(ROOT)), digest(path), "G82_package"))
    assert len(rows) == len({row[0] for row in rows}) == 26
    rendered = "path\tsha256\trole\n" + "".join("\t".join(row) + "\n" for row in sorted(rows))
    (HERE / "REVIEW_MANIFEST.tsv").write_text(rendered, encoding="utf-8")
    print(f"payload_rows={len(rows)} sealed_files={len(rows)+1}")


if __name__ == "__main__":
    main()
