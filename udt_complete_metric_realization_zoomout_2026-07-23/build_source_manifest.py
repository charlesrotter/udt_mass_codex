#!/usr/bin/env python3
"""Freeze the exact sources used by the complete-metric realization map."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCES = (
    "UDT_NATIVE_ACTION_COLD_PACKET.md",
    "native_action_final_adjudication_2026-07-18/FINAL_ADJUDICATION_REPORT.md",
    "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv",
    "udt_metric_to_frontier_reference_2026-07-22/REFERENCE.md",
    "udt_metric_to_frontier_reference_2026-07-22/REFERENCE_CORRECTION_LAYER.md",
    "udt_metric_to_frontier_reference_2026-07-22/CLAIM_DEPENDENCY_LEDGER.tsv",
    "udt_metric_to_frontier_reference_2026-07-22/OPEN_JOIN_LEDGER.tsv",
    "udt_metric_to_frontier_reference_2026-07-22/PONDER_READOUT.md",
    "udt_global_metric_assembly_atlas_2026-07-22/AUDIT_REPORT.md",
    "udt_global_metric_assembly_atlas_2026-07-22/STATUS_LEDGER.tsv",
    "udt_global_metric_assembly_atlas_2026-07-22/SELECTOR_MATRIX.tsv",
    "udt_global_metric_assembly_atlas_2026-07-22/STAGE_GATE_LEDGER.tsv",
    "udt_native_coframe_composition_law_audit_2026-07-23/AUDIT_REPORT.md",
    "udt_native_coframe_composition_law_audit_2026-07-23/RESULT.json",
    "udt_native_coframe_composition_law_audit_2026-07-23/STATUS_LEDGER.tsv",
    "udt_native_coframe_composition_law_audit_2026-07-23/derive_composition_audit.py",
    "udt_coframe_hopf_bridge_audit_2026-07-23/AUDIT_REPORT.md",
    "udt_coframe_hopf_bridge_audit_2026-07-23/RESULT.json",
    "udt_coframe_hopf_bridge_audit_2026-07-23/BRIDGE_DEPENDENCY_MATRIX.tsv",
    "udt_coframe_hopf_bridge_audit_2026-07-23/STATUS_LEDGER.tsv",
    "udt_reciprocal_subbundle_ownership_audit_2026-07-22/AUDIT_REPORT.md",
    "udt_reciprocal_subbundle_ownership_audit_2026-07-22/DERIVATION_RESULT.json",
    "udt_reciprocal_subbundle_ownership_audit_2026-07-22/STATUS_LEDGER.tsv",
    "udt_phi_metric_ontology_audit_2026-07-22/AUDIT_REPORT.md",
    "udt_phi_metric_ontology_audit_2026-07-22/DEDUCTIVE_SPINE.tsv",
    "udt_phi_metric_ontology_audit_2026-07-22/STATUS_LEDGER.tsv",
    "udt_local_selector_holonomy_closure_2026-07-22/AUDIT_REPORT.md",
    "udt_local_selector_holonomy_closure_2026-07-22/STATUS_LEDGER.tsv",
    "udt_motif_hopf_correspondence_audit_2026-07-22/AUDIT_REPORT.md",
    "udt_motif_hopf_correspondence_audit_2026-07-22/SCIENTIFIC_SUMMARY.json",
    "udt_motif_hopf_correspondence_audit_2026-07-22/TORIC_STATUS_LEDGER.tsv",
    "native_hopfion_topology_audit_2026-07-19/AUDIT_REPORT.md",
    "native_hopfion_topology_audit_2026-07-19/TOPOLOGY_STATUS_LEDGER.tsv",
    "bootstrap_csn_phi_angular_selector_2026-07-19/AUDIT_REPORT.md",
    "bootstrap_csn_phi_angular_selector_2026-07-19/CANDIDATE_OPERATOR.tsv",
    "bootstrap_csn_phi_angular_selector_2026-07-19/STATUS_LEDGER.tsv",
    "boundary_bootstrap_representative_selector_audit_2026-07-19/AUDIT_REPORT.md",
    "boundary_bootstrap_representative_selector_audit_2026-07-19/STATUS_LEDGER.tsv",
    "boundary_bootstrap_representative_selector_audit_2026-07-19/SELECTOR_REQUIREMENT_MATRIX.tsv",
    "null_section_hopfion_metric_audit_2026-07-19/AUDIT_REPORT.md",
    "null_section_hopfion_metric_audit_2026-07-19/DERIVATION_RESULT.json",
    "null_section_hopfion_metric_audit_2026-07-19/STATUS_LEDGER.tsv",
    "angular_toric_closure_selector_2026-07-19/AUDIT_REPORT.md",
    "angular_toric_closure_selector_2026-07-19/DERIVATION_RESULT.json",
    "angular_toric_closure_selector_2026-07-19/STATUS_LEDGER.tsv",
    "udt_global_coframe_cocycle_audit_2026-07-20/AUDIT_REPORT.md",
    "udt_global_coframe_cocycle_audit_2026-07-20/STATUS_LEDGER.tsv",
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(131072), b""):
            value.update(block)
    return value.hexdigest()


def main() -> None:
    if len(SOURCES) != 47 or len(set(SOURCES)) != 47:
        raise AssertionError("source list identity/count")
    lines = []
    for relative in SOURCES:
        path = ROOT / relative
        if not path.is_file():
            raise FileNotFoundError(relative)
        lines.append(f"{digest(path)}  {relative}")
    (HERE / "SOURCE_MANIFEST.sha256").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    print(f"froze {len(lines)} exact source files")


if __name__ == "__main__":
    main()
