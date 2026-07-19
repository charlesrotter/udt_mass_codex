#!/usr/bin/env python3
"""Build the base-pinned source inventory for the transverse selector audit."""

from __future__ import annotations

import csv
import hashlib
import pathlib
import subprocess


BASE = "4f5cb5d18b4f3658789a0b0e5f88d1f9439e811a"
SOURCES = [
    ("UDT_NATIVE_ACTION_COLD_PACKET.md", "FOUNDATION", "exact C0/C1 slot and global limits"),
    ("UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md", "FOUNDATION", "positive common-scale equivalence"),
    ("UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md", "FOUNDATION", "global admissibility wording and limits"),
    ("CANON.md", "FINITE_CELL_AUTHORITY", "finite mirrored cell and static phi seal data only"),
    ("UDT_SCIENTIFIC_FRONTIER_2026-07-19.md", "FRONTIER", "controlling pre-audit status"),
    ("native_hopfion_topology_audit_2026-07-19/AUDIT_REPORT.md", "PRIOR_AUDIT", "celestial S2 fiber and section gate"),
    ("null_section_hopfion_metric_audit_2026-07-19/AUDIT_REPORT.md", "PRIOR_AUDIT", "reciprocal Hopf block and soldering counterexample"),
    ("null_section_hopfion_metric_audit_2026-07-19/DERIVATION_RESULT.json", "PRIOR_ALGEBRA", "exact Hopf coordinate identities"),
    ("angular_toric_closure_selector_2026-07-19/AUDIT_REPORT.md", "PRIOR_AUDIT", "conditional toric theorem and ordered gates"),
    ("angular_toric_closure_selector_2026-07-19/STATUS_LEDGER.tsv", "PRIOR_LEDGER", "premise-stamped current theorem"),
    ("angular_toric_closure_selector_2026-07-19/CANDIDATE_FAMILY.tsv", "PRIOR_CENSUS", "toric counterfamilies"),
    ("reciprocal_line_realization_selector_2026-07-18/DERIVATION_REPORT.md", "PRIOR_SELECTOR", "metric-only line naturality theorem"),
    ("reciprocal_line_realization_selector_2026-07-18/STATUS_LEDGER.tsv", "PRIOR_LEDGER", "type and realization statuses"),
]


def git(repo: pathlib.Path, *args: str, binary: bool = False):
    result = subprocess.run(
        ["git", *args], cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=not binary, check=True,
    )
    return result.stdout


def main() -> None:
    package = pathlib.Path(__file__).resolve().parent
    repo = package.parent
    output = package / "SOURCE_INVENTORY.tsv"
    fields = ["current_path", "blob_oid", "sha256", "size_bytes", "last_commit", "role", "load_bearing_use"]
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for path, role, use in SOURCES:
            payload = bytes(git(repo, "show", f"{BASE}:{path}", binary=True))
            writer.writerow({
                "current_path": path,
                "blob_oid": str(git(repo, "rev-parse", f"{BASE}:{path}")).strip(),
                "sha256": hashlib.sha256(payload).hexdigest(),
                "size_bytes": len(payload),
                "last_commit": str(git(repo, "log", "-1", "--format=%H", BASE, "--", path)).strip(),
                "role": role,
                "load_bearing_use": use,
            })
    print(f"SOURCE INVENTORY BUILT rows={len(SOURCES)} base={BASE}")


if __name__ == "__main__":
    main()
