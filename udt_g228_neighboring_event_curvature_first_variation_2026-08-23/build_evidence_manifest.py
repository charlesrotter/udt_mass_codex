#!/usr/bin/env python3
"""Build the final G228 evidence manifest after every other artifact."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "EVIDENCE_MANIFEST.tsv"
INCLUDE = (
    "AUDIT_REPORT.md",
    "DERIVATION_RESULT.json",
    "EVIDENCE_GATES.md",
    "EXACT_DERIVATION.md",
    "FULL_INDEX_ANCHOR.json",
    "HOSTILE_CATCH_RESULT.json",
    "INDEPENDENT_VERIFICATION.json",
    "MAP.md",
    "MULTI_AGENT_ADVERSARIAL_REVIEW.md",
    "PONDER.md",
    "PREMISE_LEDGER.tsv",
    "PREREGISTRATION.md",
    "PREREGISTRATION_HASHES.tsv",
    "REPAIR_VERIFICATION.md",
    "RUN_LOG.txt",
    "SOURCE_MANIFEST.tsv",
    "SUBSET_CENSUS.tsv",
    "SYZYGY_BASIS.json",
    "VERIFICATION_RESULT.json",
    "build_evidence_manifest.py",
    "derive_neighboring_curvature_first_variation.py",
    "run_hostile_catches.py",
    "verify_evidence_manifest.py",
    "verify_full_index_anchor.py",
    "verify_neighboring_curvature_independent.py",
    "verify_package.py",
)


def main() -> None:
    lines = ["path\tbytes\tsha256"]
    for name in INCLUDE:
        path = ROOT / name
        data = path.read_bytes()
        lines.append(f"{name}\t{len(data)}\t{hashlib.sha256(data).hexdigest()}")
    OUTPUT.write_text("\n".join(lines) + "\n")
    print(f"wrote {OUTPUT} with {len(INCLUDE)} entries")


if __name__ == "__main__":
    main()
