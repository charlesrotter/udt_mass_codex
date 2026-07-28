#!/usr/bin/env python3
"""Freeze load-bearing sources from the preregistered Git base."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path

BASE = "ace0699fc145c935c16cd283f393c18e654d5b74"
HERE = Path(__file__).resolve().parent
SOURCES = [
    ("CURRENT_SCIENTIFIC_PREMISES.md", "current_premise_controller"),
    ("CURRENT_SCIENTIFIC_PREMISES.tsv", "current_premise_controller"),
    ("UDT_SCIENTIFIC_FRONTIER_2026-07-19.md", "current_frontier"),
    ("udt_general_screen_dependency_regrade_2026-07-28/AUDIT_REPORT.md", "rerun_authority"),
    ("udt_general_screen_dependency_regrade_2026-07-28/CORRECTION_LAYER.md", "rerun_authority"),
    ("udt_general_screen_dependency_regrade_2026-07-28/CURRENT_LOAD_BEARING_CLAIM_REGRADING.tsv", "rerun_authority"),
    ("null_section_hopfion_metric_audit_2026-07-19/AUDIT_REPORT.md", "N22_owner"),
    ("null_section_hopfion_metric_audit_2026-07-19/STATUS_LEDGER.tsv", "N22_owner"),
    ("null_section_hopfion_metric_audit_2026-07-19/derive_null_section_hopfion.py", "N22_algebra"),
    ("null_section_hopfion_metric_audit_2026-07-19/DERIVATION_RESULT.json", "N22_algebra"),
    ("angular_toric_closure_selector_2026-07-19/AUDIT_REPORT.md", "T18_owner"),
    ("angular_toric_closure_selector_2026-07-19/LAY_DECISION_TREE.md", "T18_decision_logic"),
    ("angular_toric_closure_selector_2026-07-19/STATUS_LEDGER.tsv", "T18_owner"),
    ("angular_toric_closure_selector_2026-07-19/CANDIDATE_FAMILY.tsv", "T18_completion_family"),
    ("angular_toric_closure_selector_2026-07-19/derive_angular_toric_selector.py", "T18_algebra"),
    ("angular_toric_closure_selector_2026-07-19/DERIVATION_RESULT.json", "T18_algebra"),
    ("udt_general_screen_complete_cell_atlas_2026-07-28/AUDIT_REPORT.md", "full_screen_owner"),
    ("udt_general_screen_complete_cell_atlas_2026-07-28/EXACT_DERIVATION.md", "full_screen_owner"),
    ("udt_general_screen_complete_cell_atlas_2026-07-28/STATUS_LEDGER.tsv", "full_screen_owner"),
    ("udt_general_screen_complete_cell_atlas_2026-07-28/BLOCK_PRESERVATION_CONDITIONS.tsv", "full_screen_contact"),
    ("udt_general_screen_complete_cell_atlas_2026-07-28/derive_general_screen.py", "full_screen_algebra"),
    ("udt_general_screen_complete_cell_atlas_2026-07-28/GENERAL_CARTAN_RESULT.json", "full_screen_algebra"),
    ("udt_twisted_s3_intrinsic_pair_witness_audit_2026-07-27/AUDIT_REPORT.md", "intrinsic_pair_scope"),
    ("udt_twisted_s3_intrinsic_pair_witness_audit_2026-07-27/EXACT_DERIVATION.md", "intrinsic_pair_scope"),
    ("udt_twisted_s3_intrinsic_pair_witness_audit_2026-07-27/STATUS_LEDGER.tsv", "intrinsic_pair_scope"),
    ("udt_twisted_s3_intrinsic_screen_cocycle_audit_2026-07-27/AUDIT_REPORT.md", "same_metric_screen_scope"),
    ("udt_twisted_s3_intrinsic_screen_cocycle_audit_2026-07-27/EXACT_DERIVATION.md", "same_metric_screen_scope"),
    ("udt_twisted_s3_intrinsic_screen_cocycle_audit_2026-07-27/STATUS_LEDGER.tsv", "same_metric_screen_scope"),
    ("udt_coframe_hopf_bridge_audit_2026-07-23/AUDIT_REPORT.md", "conditional_chart_bridge"),
    ("udt_coframe_hopf_bridge_audit_2026-07-23/STATUS_LEDGER.tsv", "conditional_chart_bridge"),
    ("udt_hopf_realization_deformation_audit_2026-07-23/AUDIT_REPORT.md", "carrier_deformation_boundary"),
    ("udt_hopf_realization_deformation_audit_2026-07-23/STATUS_LEDGER.tsv", "carrier_deformation_boundary"),
    ("udt_finite_cell_completion_atlas_2026-07-21/GROUP_ACTION_QUOTIENT_ATLAS.tsv", "quotient_taxonomy"),
    ("udt_global_metric_assembly_atlas_2026-07-22/COMPLETION_CLASS_REGISTRY.tsv", "completion_taxonomy"),
    ("udt_complete_branch_founded_pair_pullback_audit_2026-07-26/EXACT_DERIVATION.md", "complete_branch_pair_history"),
    ("udt_complete_branch_founded_pair_pullback_audit_2026-07-26/STATUS_LEDGER.tsv", "complete_branch_pair_history"),
    ("native_hopfion_topology_audit_2026-07-19/AUDIT_REPORT.md", "carrier_status_boundary"),
    ("native_hopfion_topology_audit_2026-07-19/TOPOLOGY_STATUS_LEDGER.tsv", "carrier_status_boundary"),
]


def git(*args: str, binary: bool = False):
    out = subprocess.check_output(["git", *args], cwd=HERE.parent)
    return out if binary else out.decode().strip()


def main() -> None:
    rows = []
    for path, role in SOURCES:
        blob = git("rev-parse", f"{BASE}:{path}")
        data = git("show", f"{BASE}:{path}", binary=True)
        rows.append(
            {
                "path": path,
                "role": role,
                "blob": blob,
                "sha256": hashlib.sha256(data).hexdigest(),
                "bytes": len(data),
            }
        )
    out = HERE / "SOURCE_MANIFEST.tsv"
    with out.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["path", "role", "blob", "sha256", "bytes"], delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    identity = hashlib.sha256("\n".join(row["path"] + "\t" + row["blob"] for row in rows).encode()).hexdigest()
    print(f"base={BASE}")
    print(f"sources={len(rows)}")
    print(f"identity_sha256={identity}")


if __name__ == "__main__":
    main()
