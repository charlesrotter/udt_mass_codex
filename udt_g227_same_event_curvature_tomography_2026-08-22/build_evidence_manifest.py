#!/usr/bin/env python3
"""Build the deterministic G227 package evidence manifest."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent
FILES = (
    "WHITEBOARD_SYNTHESIS.md",
    "PREREGISTRATION.md",
    "PREREGISTRATION_HASHES.tsv",
    "PREMISE_LEDGER.tsv",
    "SOURCE_MANIFEST.tsv",
    "AUDIT_REPORT.md",
    "EVIDENCE_GATES.md",
    "POST_OUTCOME_ADVERSARIAL_REVIEW.md",
    "REPAIR_VERIFICATION.md",
    "derive_curvature_tomography.py",
    "verify_independent.py",
    "run_hostile_catches.py",
    "verify_package.py",
    "verify_evidence_manifest.py",
    "DERIVATION_RESULT.json",
    "INDEPENDENT_VERIFICATION.json",
    "HOSTILE_CATCH_RESULT.json",
    "VERIFICATION_RESULT.json",
    "RUN_LOG.txt",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    lines = ["path\tsha256\tbytes"]
    for name in FILES:
        path = ROOT / name
        if not path.is_file():
            raise SystemExit(f"missing evidence file: {name}")
        lines.append(f"{name}\t{digest(path)}\t{path.stat().st_size}")
    (ROOT / "EVIDENCE_MANIFEST.tsv").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote EVIDENCE_MANIFEST.tsv with {len(FILES)} entries")


if __name__ == "__main__":
    main()
