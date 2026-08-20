#!/usr/bin/env python3
"""Build the exact frozen upstream-source manifest for G192."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
SOURCES = (
    ("CURRENT_SCIENTIFIC_PREMISES.tsv", "current exact premise registry"),
    ("udt_g191_nonconformal_timelive_mixing_join_2026-08-20/AUDIT_REPORT.md", "immediate constant-control authority"),
    ("udt_g191_nonconformal_timelive_mixing_join_2026-08-20/EXACT_DERIVATION.md", "constant-control equations and limits"),
    ("udt_g191_nonconformal_timelive_mixing_join_2026-08-20/EXTERNAL_REVIEW_ADJUDICATION.md", "accepted G191 scope"),
    ("udt_g190_completed_pair_timelive_frequency_screen_join_2026-08-20/AUDIT_REPORT.md", "joint evaluator authority"),
    ("udt_g190_completed_pair_timelive_frequency_screen_join_2026-08-20/EXACT_DERIVATION.md", "frequency-screen typing"),
    ("udt_g188_complete_coframe_null_jacobi_extension_2026-08-20/AUDIT_REPORT.md", "complete-metric screen authority"),
    ("udt_g188_complete_coframe_null_jacobi_extension_2026-08-20/EXACT_DERIVATION.md", "Jacobi and curvature conventions"),
    ("udt_g176_completed_pair_dual_reciprocity_consolidation_2026-08-19/AUDIT_REPORT.md", "completed-pair normalization"),
    ("udt_g179_complete_coframe_pair_pullback_extension_2026-08-19/EXACT_DERIVATION.md", "complete-coframe pullback"),
)


def main():
    rows = ["path\tsha256\trole"]
    for relative, role in SOURCES:
        payload = (ROOT / relative).read_bytes()
        rows.append(f"{relative}\t{hashlib.sha256(payload).hexdigest()}\t{role}")
    content = "\n".join(rows) + "\n"
    if os.environ.get("G192_NO_WRITE") != "1":
        (PACKAGE / "SOURCE_MANIFEST.tsv").write_text(content, encoding="utf-8")
    print(f"verified {len(SOURCES)} source rows")


if __name__ == "__main__":
    main()
