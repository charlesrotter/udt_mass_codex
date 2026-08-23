#!/usr/bin/env python3
"""Build the deterministic G231 evidence manifest."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent
FILES = (
    "MAP.md",
    "PONDER.md",
    "PREMISE_LEDGER.tsv",
    "STANDARD_REFERENCES.md",
    "THEOREM_SCOPE_AUDIT.md",
    "MULTI_AGENT_ADVERSARIAL_REVIEW.md",
    "ZERO_CONTEXT_STARTUP_REHEARSAL.md",
    "SOURCE_MANIFEST.tsv",
    "PREREGISTRATION.md",
    "PREREGISTRATION_HASHES.tsv",
    "EXACT_DERIVATION.md",
    "AUDIT_REPORT.md",
    "EVIDENCE_GATES.md",
    "REPAIR_RECORD.md",
    "RUN_LOG.txt",
    "STATUS_LEDGER.tsv",
    "NEXT_GATE.md",
    "derive_cartan_regional_bridge.py",
    "verify_cartan_bridge_independent.py",
    "hostile_mutation_tests.py",
    "verify_package.py",
    "test_cartan_regional_bridge.py",
    "build_evidence_manifest.py",
    "verify_evidence_manifest.py",
    "exact_results.json",
    "independent_results.json",
    "hostile_results.json",
    "verification_results.json",
)


def rows() -> list[tuple[str, str, int]]:
    result = []
    for name in FILES:
        payload = (ROOT / name).read_bytes()
        result.append((name, hashlib.sha256(payload).hexdigest(), len(payload)))
    return result


def main() -> None:
    lines = ["path\tsha256\tbytes"]
    lines.extend(f"{name}\t{digest}\t{size}" for name, digest, size in rows())
    (ROOT / "EVIDENCE_MANIFEST.tsv").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"PASS: wrote {len(FILES)} G231 evidence rows")


if __name__ == "__main__":
    main()
