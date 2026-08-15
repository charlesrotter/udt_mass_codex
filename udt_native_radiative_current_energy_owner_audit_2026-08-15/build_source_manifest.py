#!/usr/bin/env python3
"""Build the exact source manifest for this bounded audit."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent / "SOURCE_MANIFEST.tsv"
SOURCES = [
    ("CURRENT_SCIENTIFIC_PREMISES.tsv", "current premise authority"),
    ("angular_toric_closure_selector_2026-07-19/AUDIT_REPORT.md", "conditional toric connection authority"),
    ("udt_global_functional_dof_constraint_rank_audit_2026-07-26/EXACT_DERIVATION.md", "Maxwell identity correction"),
    ("udt_r17_stationary_local_one_form_selection_audit_2026-08-10/EXACT_DERIVATION.md", "metric natural one-form nonselection"),
    ("udt_uncompressed_pair_kernel_reconstruction_2026-08-14/EXACT_DERIVATION.md", "complete coframe and pair typing"),
    ("udt_reciprocal_kernel_release_candidate_interface_audit_2026-08-15/EXACT_DERIVATION.md", "current complete kernel interface"),
    ("udt_native_flux_luminosity_law_ownership_audit_2026-08-15/EXTERNAL_REVIEW_ADJUDICATION.md", "G94 flux ownership boundary"),
    ("luminosity_distance_n2_optics_results.md", "historical Maxwell and flux provenance"),
]


def main():
    lines = ["path\tsha256\trole"]
    for relative, role in SOURCES:
        path = ROOT / relative
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        lines.append(f"{relative}\t{digest}\t{role}")
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()

