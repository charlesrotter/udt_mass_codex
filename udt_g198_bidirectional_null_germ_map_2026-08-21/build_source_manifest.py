#!/usr/bin/env python3
"""Build the frozen upstream-source manifest for G198."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
SOURCES = (
    ("udt_g196_longitudinal_screen_mixing_descent_2026-08-20/AUDIT_REPORT.md", "parent bounded theorem"),
    ("udt_g196_longitudinal_screen_mixing_descent_2026-08-20/EXACT_DERIVATION.md", "parent exact conventions"),
    ("udt_g196_longitudinal_screen_mixing_descent_2026-08-20/PREMISE_LEDGER.tsv", "parent premise typing"),
    ("udt_g196_longitudinal_screen_mixing_descent_2026-08-20/PREREGISTRATION.md", "parent declared family"),
    ("udt_g196_longitudinal_screen_mixing_descent_2026-08-20/derive_longitudinal_screen_mixing.py", "parent direct implementation"),
    ("udt_g197_native_kernel_provenance_and_startup_integrity_audit_2026-08-21/AUDIT_REPORT.md", "native-provenance boundary"),
    ("udt_g197_native_kernel_provenance_and_startup_integrity_audit_2026-08-21/RESTART.md", "authorized restart gate"),
)


def main():
    rows = ["sha256\tpath\trole"]
    for relative, role in SOURCES:
        payload = (ROOT / relative).read_bytes()
        rows.append(f"{hashlib.sha256(payload).hexdigest()}\t{relative}\t{role}")
    content = "\n".join(rows) + "\n"
    if os.environ.get("G198_NO_WRITE") != "1":
        (PACKAGE / "SOURCE_MANIFEST.tsv").write_text(content, encoding="utf-8")
    print(f"verified {len(SOURCES)} source rows")


if __name__ == "__main__":
    main()
