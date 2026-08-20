#!/usr/bin/env python3
"""Freeze the exact repository sources made load-bearing by G190."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
SOURCES = [
    "CURRENT_SCIENTIFIC_PREMISES.tsv",
    "udt_g116_calibrated_frequency_terminal_pair_junction_2026-08-16/EXACT_DERIVATION.md",
    "udt_g119_finite_radius_timelive_spherical_screen_theorem_2026-08-16/EXACT_DERIVATION.md",
    "udt_g178_completed_pair_kernel_fresh_adversarial_review_2026-08-19/AUDIT_REPORT.md",
    "udt_g179_complete_coframe_pair_pullback_extension_2026-08-19/EXACT_DERIVATION.md",
    "udt_g180_completed_pair_smooth_family_descent_2026-08-19/EXACT_DERIVATION.md",
    "udt_g188_complete_coframe_null_jacobi_extension_2026-08-20/EXACT_DERIVATION.md",
    "udt_g188_complete_coframe_null_jacobi_extension_2026-08-20/AUDIT_REPORT.md",
    "udt_g189_p1_free_metric_flux_interface_2026-08-20/EXACT_DERIVATION.md",
    "udt_g189_p1_free_metric_flux_interface_2026-08-20/AUDIT_REPORT.md",
]


def digest(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    rows = ["path\tsha256\tbytes"]
    for relative in SOURCES:
        path = ROOT / relative
        if not path.is_file():
            raise FileNotFoundError(relative)
        rows.append(f"{relative}\t{digest(path)}\t{path.stat().st_size}")
    rendered = "\n".join(rows) + "\n"
    manifest = PACKAGE / "SOURCE_MANIFEST.tsv"
    if os.environ.get("G190_NO_WRITE") == "1":
        if manifest.read_text(encoding="utf-8") != rendered:
            raise AssertionError("sealed source manifest mismatch")
        print(f"verified {len(SOURCES)} source rows without writing")
    else:
        manifest.write_text(rendered, encoding="utf-8")
        print(f"wrote {len(SOURCES)} source rows")


if __name__ == "__main__":
    main()
