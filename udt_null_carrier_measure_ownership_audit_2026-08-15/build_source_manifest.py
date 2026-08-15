#!/usr/bin/env python3
"""Hash the exact repository sources consulted by this bounded audit."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
SOURCES = (
    ("CURRENT_SCIENTIFIC_PREMISES.tsv", "current premise authority"),
    ("udt_native_radiative_current_energy_owner_audit_2026-08-15/EXTERNAL_REVIEW_ADJUDICATION.md", "G95 immediate parent"),
    ("udt_native_flux_luminosity_law_ownership_audit_2026-08-15/EXACT_DERIVATION.md", "G94 flux parent"),
    ("udt_uncompressed_pair_kernel_reconstruction_2026-08-14/EXACT_DERIVATION.md", "complete pair kernel"),
    ("udt_common_query_pair_immersion_reconstruction_2026-08-11/AUDIT_REPORT.md", "query geometry authority"),
    ("udt_complete_coframe_calibration_transport_from_scratch_2026-08-10/AUDIT_REPORT.md", "calibration transport authority"),
    ("udt_conceptual_object_type_dependency_audit_2026-08-05/AUDIT_REPORT.md", "source carrier type guard"),
)


def main() -> None:
    with (PACKAGE / "SOURCE_MANIFEST.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(("path", "sha256", "role"))
        for relative, role in SOURCES:
            path = ROOT / relative
            writer.writerow((relative, hashlib.sha256(path.read_bytes()).hexdigest(), role))


if __name__ == "__main__":
    main()
