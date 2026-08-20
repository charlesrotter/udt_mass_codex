#!/usr/bin/env python3
"""Build the frozen upstream-source manifest for G194."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
SOURCES = (
    ("CURRENT_SCIENTIFIC_PREMISES.tsv", "current exact premise registry"),
    (
        "udt_g193_noncommuting_transverse_mixing_extension_2026-08-20/AUDIT_REPORT.md",
        "immediate two-function family authority",
    ),
    (
        "udt_g193_noncommuting_transverse_mixing_extension_2026-08-20/EXACT_DERIVATION.md",
        "two-function equations and proof",
    ),
    (
        "udt_g193_noncommuting_transverse_mixing_extension_2026-08-20/EXTERNAL_REVIEW_ADJUDICATION.md",
        "accepted G193 scope and caveats",
    ),
    (
        "udt_g190_completed_pair_timelive_frequency_screen_join_2026-08-20/AUDIT_REPORT.md",
        "joint frequency-screen authority",
    ),
    (
        "udt_g190_completed_pair_timelive_frequency_screen_join_2026-08-20/EXACT_DERIVATION.md",
        "affine and frequency typing",
    ),
    (
        "udt_g188_complete_coframe_null_jacobi_extension_2026-08-20/AUDIT_REPORT.md",
        "complete-metric screen authority",
    ),
    (
        "udt_g188_complete_coframe_null_jacobi_extension_2026-08-20/EXACT_DERIVATION.md",
        "curvature and Jacobi convention",
    ),
    (
        "udt_g176_completed_pair_dual_reciprocity_consolidation_2026-08-19/AUDIT_REPORT.md",
        "completed-pair normalization",
    ),
    (
        "udt_g179_complete_coframe_pair_pullback_extension_2026-08-19/EXACT_DERIVATION.md",
        "complete-coframe pullback",
    ),
)


def main():
    rows = ["path\tsha256\trole"]
    for relative, role in SOURCES:
        payload = (ROOT / relative).read_bytes()
        rows.append(f"{relative}\t{hashlib.sha256(payload).hexdigest()}\t{role}")
    content = "\n".join(rows) + "\n"
    if os.environ.get("G194_NO_WRITE") != "1":
        (PACKAGE / "SOURCE_MANIFEST.tsv").write_text(content, encoding="utf-8")
    print(f"verified {len(SOURCES)} source rows")


if __name__ == "__main__":
    main()
