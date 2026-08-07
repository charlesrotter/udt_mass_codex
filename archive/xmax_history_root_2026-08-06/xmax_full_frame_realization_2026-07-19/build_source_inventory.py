#!/usr/bin/env python3
"""Build the fixed source inventory for the Xmax full-frame audit."""

from __future__ import annotations

import csv
import hashlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent / "SOURCE_INVENTORY.tsv"

SOURCES = [
    ("UDT_NATIVE_ACTION_COLD_PACKET.md", "CURRENT_FOUNDATION", "reciprocity, CSN, coframe representation, Xmax, seal, and open-action ledger"),
    ("UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md", "CURRENT_FOUNDATION", "common-scale equivalence and its limits"),
    ("UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md", "CURRENT_FOUNDATION", "complete-solution closure and global-output restrictions"),
    ("simple_metric_xmax_POSTULATE.md", "POST_JULY_WORKING_LEAD", "finite invariant positional reach and observer-relational intent"),
    ("simple_metric_hyperbolic_derive.md", "POST_JULY_WORKING_DERIVATION", "historical P1-P4 ledger and fractional-linear positional law"),
    ("xmax_reciprocity_audit_2026-07-19/AUDIT_REPORT.md", "CURRENT_SELECTOR_AUDIT", "exact XR1 reciprocity, countergroup, and bounded-dx metric failure"),
    ("xmax_reciprocity_audit_2026-07-19/STATUS_LEDGER.tsv", "CURRENT_SELECTOR_AUDIT", "current Xmax reciprocity status distinctions"),
    ("metric_cartan_holonomy_audit_2026-07-19/AUDIT_REPORT.md", "CURRENT_SELECTOR_AUDIT", "complete coframe and angular/holonomy openness"),
    ("bootstrap_csn_phi_angular_selector_2026-07-19/AUDIT_REPORT.md", "CURRENT_SELECTOR_AUDIT", "bootstrap/CSN phi-angular selector limits"),
    ("reciprocal_clock_optical_scale_selector_2026-07-19/DERIVATION_REPORT.md", "CURRENT_SELECTOR_AUDIT", "reciprocal static metric and optical coordinate distinctions"),
    ("UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md", "CURRENT_SELECTOR_AUDIT", "action/variation selector limits"),
    ("UDT_SCIENTIFIC_FRONTIER_2026-07-19.md", "CURRENT_FRONTIER", "current scientific status and open selector seam"),
    ("CANON.md", "BINDING_LIMITED_CITATION", "absolute static phi seal only; no new canon interpretation"),
]


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def main() -> None:
    rows = []
    for relative, source_class, permitted_use in SOURCES:
        path = ROOT / relative
        if not path.is_file():
            raise FileNotFoundError(relative)
        history = git("log", "--follow", "--format=%H%x09%aI", "--", relative).splitlines()
        if not history:
            raise AssertionError(f"no Git history for {relative}")
        last_commit, last_date = history[0].split("\t", 1)
        first_commit, first_date = history[-1].split("\t", 1)
        data = path.read_bytes()
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
