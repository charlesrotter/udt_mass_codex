#!/usr/bin/env python3
"""Build the fixed provenance inventory for the metric-wide Cartan audit."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent / "SOURCE_INVENTORY.tsv"

SOURCES = [
    ("UDT_NATIVE_ACTION_COLD_PACKET.md", "CURRENT_FOUNDATION", "exact C0/C1 and missing-law ledger"),
    ("UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md", "CURRENT_FOUNDATION", "CSN statement and limits"),
    ("UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md", "CURRENT_FOUNDATION", "global complete-solution principle and limits"),
    ("native_action_final_adjudication_2026-07-18/FINAL_ADJUDICATION_REPORT.md", "CURRENT_ADJUDICATION", "action, source, variation, boundary status"),
    ("native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv", "CURRENT_ADJUDICATION", "machine-readable action statuses"),
    ("native_action_final_adjudication_2026-07-18/PROVENANCE_FIREWALL.tsv", "CURRENT_FIREWALL", "July-1 affirmative-physics restriction"),
    ("UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md", "CURRENT_SELECTOR_AUDIT", "conditional C2/EH routes and missing selector"),
    ("reciprocity_offshell_constraint_selector_2026-07-18/STATUS_LEDGER.tsv", "CURRENT_SELECTOR_AUDIT", "reciprocity/off-shell status"),
    ("reciprocal_line_realization_selector_2026-07-18/STATUS_LEDGER.tsv", "CURRENT_SELECTOR_AUDIT", "reciprocal line realization status"),
    ("transverse_reciprocal_realization_selector_2026-07-19/AUDIT_REPORT.md", "CURRENT_SELECTOR_AUDIT", "full transverse realization and freedoms"),
    ("transverse_reciprocal_realization_selector_2026-07-19/STATUS_LEDGER.tsv", "CURRENT_SELECTOR_AUDIT", "transverse machine-readable statuses"),
    ("angular_toric_closure_selector_2026-07-19/AUDIT_REPORT.md", "CURRENT_SELECTOR_AUDIT", "conditional Hopf-orbit compatibility and open selection"),
    ("angular_toric_closure_selector_2026-07-19/STATUS_LEDGER.tsv", "CURRENT_SELECTOR_AUDIT", "angular closure statuses"),
    ("projective_transport_section_selector_2026-07-19/AUDIT_REPORT.md", "CURRENT_SELECTOR_AUDIT", "connection, transport, holonomy fixed-set limits"),
    ("projective_transport_section_selector_2026-07-19/STATUS_LEDGER.tsv", "CURRENT_SELECTOR_AUDIT", "projective transport statuses"),
    ("native_hopfion_topology_audit_2026-07-19/AUDIT_REPORT.md", "CURRENT_PARTICLE_AUDIT", "full 3D Hopf capability and conditional carrier"),
    ("null_section_hopfion_metric_audit_2026-07-19/AUDIT_REPORT.md", "CURRENT_SELECTOR_AUDIT", "null fiber versus selected section"),
    ("rung2_weld_postjuly_regrade_2026-07-19/AUDIT_REPORT.md", "CURRENT_SELECTOR_AUDIT", "exact phi-angular geometry and absent native weld law"),
    ("rung2_weld_postjuly_regrade_2026-07-19/STATUS_LEDGER.tsv", "CURRENT_SELECTOR_AUDIT", "rung-2 status distinctions"),
    ("UDT_SCIENTIFIC_FRONTIER_2026-07-19.md", "CURRENT_FRONTIER", "current checkpoint and open selector seam"),
    ("archive/native_action_chat_2026-07-14_15/UDT_RECIPROCAL_LOOP_CLOSURE_MATTER_DERIVATION_RESULTS.md", "POST_JULY_PROVISIONAL_CANDIDATE", "candidate/test target only; self-graded provisional, unbanked, and independent verification open"),
]


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def main() -> None:
    rows = []
    for relative, source_class, permitted_use in SOURCES:
        path = ROOT / relative
        if not path.is_file():
            raise FileNotFoundError(relative)
        data = path.read_bytes()
        history = git("log", "--follow", "--format=%H%x09%aI", "--", relative).splitlines()
        if not history:
            raise AssertionError(f"no Git history for {relative}")
        last_commit, last_date = history[0].split("\t", 1)
        first_commit, first_date = history[-1].split("\t", 1)
        rows.append({
            "path": relative,
            "git_blob": git("hash-object", relative),
            "sha256": hashlib.sha256(data).hexdigest(),
            "bytes": str(len(data)),
            "first_commit": first_commit,
            "first_date": first_date,
            "last_commit": last_commit,
            "last_date": last_date,
            "source_class": source_class,
            "permitted_use": permitted_use,
        })
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"PASS sources={len(rows)} output={OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
