#!/usr/bin/env python3
"""Freeze the exact source bytes used by the three-observer overlap audit."""

from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
SOURCE_COMMIT = "ea243c7c"
SOURCES = (
    "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md",
    "udt_founding_observer_comparison_semantics_audit_2026-07-27/EXACT_ADJUDICATION.md",
    "udt_native_reciprocal_comparison_bundle_audit_2026-07-27/EXACT_DERIVATION.md",
    "udt_complete_pair_phi_orchestra_audit_2026-08-05/EXACT_DERIVATION.md",
    "udt_global_phi_ownership_overlap_audit_2026-08-05/AUDIT_REPORT.md",
    "udt_global_phi_ownership_overlap_audit_2026-08-05/EXACT_DERIVATION.md",
    "udt_reciprocal_flag_foundation_ownership_audit_2026-08-09/EXACT_DERIVATION.md",
    "udt_reciprocal_calibration_state_solder_audit_2026-08-09/EXACT_DERIVATION.md",
    "udt_terminal_reciprocal_ce_positional_derivation_2026-08-09/EXACT_DERIVATION.md",
    "udt_terminal_reciprocal_ce_positional_derivation_2026-08-09/STATUS_LEDGER.tsv",
    "udt_calibrated_pair_map_owner_atlas_2026-08-09/EXACT_DERIVATION.md",
    "udt_calibrated_pair_map_owner_atlas_2026-08-09/PAIR_MAP_ATLAS.tsv",
    "udt_calibrated_pair_map_owner_atlas_2026-08-09/STATUS_LEDGER.tsv",
    "udt_founding_pair_relation_functor_ownership_audit_2026-08-09/EXACT_DERIVATION.md",
    "udt_founding_pair_relation_functor_ownership_audit_2026-08-09/STATUS_LEDGER.tsv",
    "CURRENT_SCIENTIFIC_PREMISES.tsv",
    "CURRENT_RESEARCH_PROGRAM.md",
)


def main() -> None:
    rows = ["sha256\tpath\tsource_ref"]
    for relative in SOURCES:
        source_ref = f"{SOURCE_COMMIT}:{relative}"
        data = subprocess.check_output(["git", "show", source_ref], cwd=ROOT)
        rows.append(f"{hashlib.sha256(data).hexdigest()}\t{relative}\t{source_ref}")
    output = HERE / "SOURCE_MANIFEST.tsv"
    output.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"PASS: froze {len(SOURCES)} sources from {SOURCE_COMMIT}")


if __name__ == "__main__":
    main()
