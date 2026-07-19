#!/usr/bin/env python3
"""Build the fixed-source inventory for the rung-2 weld regrade."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent / "SOURCE_INVENTORY.tsv"

SOURCES = [
    ("CANON.md", "HISTORICAL_CANON_TEXT", "C-2026-06-10-3 claim; no affirmative post-firewall physics"),
    ("grok/quarantine_free_DA/macro_sector_fork_resolution.md", "HISTORICAL_SUPERSEDED", "June-10 macro synthesis and later supersession banner"),
    ("AUDIT.md", "HISTORICAL_CONDITIONS_CHANGED", "S116 imported Einstein/CMB pipeline and stale-header warning"),
    ("legacy/root_oneoffs_2026-07-01/native_weld_status_derivation.py", "HISTORICAL_REPLAY", "June-10 implementation reproduced unchanged"),
    ("weld_status_results.md", "HISTORICAL_SUPERSEDED", "June-10 result and July-6 pre-native banner"),
    ("archive/pre_2026-07-01/weld_discriminator_results.md", "HISTORICAL_SUPERSEDED", "June-10 CMB comparison; failure/provenance only"),
    ("macro_spine_provenance_2026-07-06.md", "POST_JULY_PROVENANCE", "classifies weld family pre-native and superseded"),
    ("UDT_NATIVE_ACTION_COLD_PACKET.md", "CURRENT_FOUNDATION", "complete C0/C1 owner ledger and explicit missing action/EOM"),
    ("UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md", "CURRENT_FOUNDATION", "CSN statement and limits"),
    ("UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md", "CURRENT_FOUNDATION", "global solution-selection statement and limits"),
    ("native_action_final_adjudication_2026-07-18/FINAL_ADJUDICATION_REPORT.md", "CURRENT_ADJUDICATION", "complete action/off-shell/source remain open"),
    ("native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv", "CURRENT_ADJUDICATION", "machine-readable current action/source statuses"),
    ("native_action_final_adjudication_2026-07-18/PROVENANCE_FIREWALL.tsv", "CURRENT_FIREWALL", "source-date use restrictions"),
    ("UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md", "CURRENT_SELECTOR_AUDIT", "GR constraints conditional and smallest missing selector"),
    ("bootstrap_csn_phi_angular_selector_2026-07-19/AUDIT_REPORT.md", "CURRENT_SELECTOR_AUDIT", "current bounded null/PND source-set conclusion"),
    ("bootstrap_csn_phi_angular_selector_2026-07-19/STATUS_LEDGER.tsv", "CURRENT_SELECTOR_AUDIT", "current exact status distinctions"),
    ("UDT_SCIENTIFIC_FRONTIER_2026-07-19.md", "CURRENT_FRONTIER", "current scientific checkpoint and open selector seam"),
]


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def main() -> None:
    rows = []
    for relative, source_class, use in SOURCES:
        path = ROOT / relative
        if not path.is_file():
            raise FileNotFoundError(relative)
        data = path.read_bytes()
        history = git("log", "--follow", "--format=%H%x09%aI", "--", relative).splitlines()
        if not history:
            raise AssertionError(f"no Git history for {relative}")
        last_commit, last_date = history[0].split("\t", 1)
        first_commit, first_date = history[-1].split("\t", 1)
        rows.append(
            {
                "path": relative,
                "git_blob": git("hash-object", relative),
                "sha256": hashlib.sha256(data).hexdigest(),
                "bytes": str(len(data)),
                "first_commit": first_commit,
                "first_date": first_date,
                "last_commit": last_commit,
                "last_date": last_date,
                "source_class": source_class,
                "permitted_use": use,
            }
        )
    fieldnames = list(rows[0])
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"PASS sources={len(rows)} output={OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
