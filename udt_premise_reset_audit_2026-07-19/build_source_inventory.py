#!/usr/bin/env python3
"""Build the fixed load-bearing source inventory."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCES = [
    ("udt_premise_reset_audit_2026-07-19/POST_PREREG_C_G_SCALE_CLARIFICATION.md", "OWNER_CLARIFICATION", "observed c and G introduce calibrated post-scale units"),
    ("UDT_NATIVE_ACTION_COLD_PACKET.md", "FOUNDATION", "frozen C0/C1 premise ledger"),
    ("UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md", "FOUNDATION", "reciprocal-c derivation and assumption ledger"),
    ("CANON.md", "AUTHORITY_CONFLICT_SOURCE", "finite-cell phi fold and WR-L historical statements; unchanged"),
    ("angular_toric_closure_selector_2026-07-19/AUDIT_REPORT.md", "PACKAGE_REPORT", "angular toric closure"),
    ("bootstrap_csn_phi_angular_selector_2026-07-19/AUDIT_REPORT.md", "PACKAGE_REPORT", "bootstrap CSN selector"),
    ("copresence_causal_accessibility_selector_2026-07-19/DERIVATION_REPORT.md", "PACKAGE_REPORT", "co-presence causal accessibility"),
    ("copresence_gr_constraint_regrade_2026-07-19/DERIVATION_REPORT.md", "PACKAGE_REPORT", "GR constraint regrade"),
    ("metric_cartan_holonomy_audit_2026-07-19/AUDIT_REPORT.md", "PACKAGE_REPORT", "Cartan holonomy"),
    ("native_hopfion_topology_audit_2026-07-19/AUDIT_REPORT.md", "PACKAGE_REPORT", "native Hopfion topology"),
    ("null_section_hopfion_metric_audit_2026-07-19/AUDIT_REPORT.md", "PACKAGE_REPORT", "null-section Hopf bridge"),
    ("projective_position_direction_magnitude_correction_2026-07-19/AUDIT_REPORT.md", "PACKAGE_REPORT", "direction magnitude correction"),
    ("projective_position_join_audit_2026-07-19/AUDIT_REPORT.md", "PACKAGE_REPORT", "projective position join"),
    ("projective_transport_section_selector_2026-07-19/AUDIT_REPORT.md", "PACKAGE_REPORT", "transport section selector"),
    ("reciprocal_c_clock_channel_correction_2026-07-19/AUDIT_REPORT.md", "PACKAGE_REPORT", "reciprocal-c clock correction"),
    ("reciprocal_clock_optical_scale_selector_2026-07-19/DERIVATION_REPORT.md", "PACKAGE_REPORT", "clock optical scale"),
    ("reciprocal_metric_null_line_selector_2026-07-19/AUDIT_REPORT.md", "PACKAGE_REPORT", "null-line selector"),
    ("rung2_weld_postjuly_regrade_2026-07-19/AUDIT_REPORT.md", "PACKAGE_REPORT", "rung2 provenance regrade"),
    ("transverse_reciprocal_realization_selector_2026-07-19/AUDIT_REPORT.md", "PACKAGE_REPORT", "transverse realization"),
    ("xmax_accelerating_finite_cell_cartan_2026-07-19/AUDIT_REPORT.md", "PACKAGE_REPORT", "accelerating Xmax Cartan"),
    ("xmax_dynamic_observer_frame_2026-07-19/AUDIT_REPORT.md", "PACKAGE_REPORT", "dynamic Xmax frame"),
    ("xmax_full_frame_realization_2026-07-19/AUDIT_REPORT.md", "PACKAGE_REPORT", "full Xmax frame"),
    ("xmax_reciprocity_audit_2026-07-19/AUDIT_REPORT.md", "PACKAGE_REPORT", "Xmax reciprocity"),
    ("LIVE.md", "CURRENT_CONTROL", "top current state"),
    ("HANDOFF.md", "CURRENT_CONTROL", "current handoff"),
    ("INDEX.md", "CURRENT_CONTROL", "startup index"),
    ("UDT_SCIENTIFIC_FRONTIER_2026-07-19.md", "CURRENT_CONTROL", "scientific frontier"),
]


def main() -> None:
    output = HERE / "SOURCE_INVENTORY.tsv"
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["path", "role", "use", "size_bytes", "sha256"])
        for name, role, use in SOURCES:
            path = ROOT / name
            data = path.read_bytes()
            writer.writerow([name, role, use, len(data), hashlib.sha256(data).hexdigest()])
    print(f"PASS sources={len(SOURCES)} output={output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
