#!/usr/bin/env python3
"""Build the fixed load-bearing source inventory for the audit."""

from __future__ import annotations

import csv
import hashlib
import pathlib
import subprocess


SOURCES = [
    ("UDT_NATIVE_ACTION_COLD_PACKET.md", "FOUNDATION", "C0/C1 status, open transverse block, slot and carrier limits"),
    ("UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md", "FOUNDATION", "CSN equivalence class and determinant-one pair"),
    ("UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md", "FOUNDATION_SUPPORT", "reciprocal exponential block and declared angular readout"),
    ("UDT_S2_CARRIER_STATUS_CLARIFICATION_2026-07-15.md", "CARRIER_STATUS", "reopened working carrier posit"),
    ("matter_carrier_provenance_audit_results.md", "PROVENANCE", "historical free angular slot and internal carrier distinction"),
    ("reciprocal_line_realization_selector_2026-07-18/DERIVATION_REPORT.md", "SELECTOR", "Lorentz isotropy and coframe nonuniqueness"),
    ("copresence_causal_accessibility_selector_2026-07-19/DERIVATION_REPORT.md", "COPRESENCE", "whole-solution versus causal reachability and conformal cones"),
    ("native_hopfion_topology_audit_2026-07-19/AUDIT_REPORT.md", "PRIOR_AUDIT", "celestial S2 fiber and upstream selector seam"),
    ("native_hopfion_topology_audit_2026-07-19/TOPOLOGY_STATUS_LEDGER.tsv", "PRIOR_LEDGER", "premise-stamped topology statuses"),
    ("hopfion_arc_scripts_2026-07-05/fs_hopfion.py", "IMPLEMENTATION", "internal triplet, Hopf seed, ordinary derivatives and charge"),
    ("noNull_energy.py", "IMPLEMENTATION", "corrected ordinary-derivative L2+L4 continuum functional"),
    ("simple_metric_angular_on_solution_space_MAP.md", "ANGULAR_HISTORY", "chosen angular-on reciprocal slice and geometric coupling map"),
    ("simple_metric_angular_on_L_multipole_results.md", "ANGULAR_EVIDENCE", "conditional wall-loud scalar multipole result"),
    ("native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv", "ACTION_STATUS", "current action/carrier/boundary status split"),
    ("UDT_SCIENTIFIC_FRONTIER_2026-07-19.md", "FRONTIER", "current controlling scientific status before this audit"),
]
BASE = "715fa57767ecc2ec370599ad18cd9f87911798d8"


def git(repo: pathlib.Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=repo, text=True).strip()


def main() -> None:
    package = pathlib.Path(__file__).resolve().parent
    repo = package.parent
    output = package / "SOURCE_INVENTORY.tsv"
    rows = []
    for path, role, use in SOURCES:
        payload = subprocess.check_output(["git", "show", f"{BASE}:{path}"], cwd=repo)
        rows.append({
            "current_path": path,
            "blob_oid": git(repo, "rev-parse", f"{BASE}:{path}"),
            "sha256": hashlib.sha256(payload).hexdigest(),
            "size_bytes": str(len(payload)),
            "last_commit": git(repo, "log", "-1", "--format=%H", BASE, "--", path),
            "role": role,
            "load_bearing_use": use,
        })
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"SOURCE INVENTORY {len(rows)}/{len(SOURCES)}")


if __name__ == "__main__":
    main()
