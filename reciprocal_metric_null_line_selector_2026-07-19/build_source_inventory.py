#!/usr/bin/env python3
"""Build the base-pinned source inventory for the reciprocal null-line audit."""

from __future__ import annotations

import csv
import hashlib
import pathlib
import subprocess


BASE = "e76d748881e6a091ce367a4c11db640700724bfb"
SOURCES = [
    ("UDT_NATIVE_ACTION_COLD_PACKET.md", "FOUNDATION", "exact reciprocal metric slot and open angular/time-live fields"),
    ("UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md", "FOUNDATION", "positive conformal equivalence"),
    ("UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md", "FOUNDATION", "on-shell admissibility wording"),
    ("CANON.md", "FINITE_CELL_AUTHORITY", "finite cell and static phi seal entries only"),
    ("UDT_SCIENTIFIC_FRONTIER_2026-07-19.md", "FRONTIER", "controlling pre-audit status"),
    ("projective_transport_section_selector_2026-07-19/AUDIT_REPORT.md", "PRIOR_AUDIT", "null-gradient and Petrov candidates"),
    ("projective_transport_section_selector_2026-07-19/STATUS_LEDGER.tsv", "PRIOR_LEDGER", "transport and section statuses"),
    ("projective_transport_section_selector_2026-07-19/DERIVATION_RESULT.json", "PRIOR_ALGEBRA", "exact conformal transport and root checks"),
    ("transverse_reciprocal_realization_selector_2026-07-19/AUDIT_REPORT.md", "PRIOR_AUDIT", "reciprocal projective theorem and physical type gate"),
    ("transverse_reciprocal_realization_selector_2026-07-19/STATUS_LEDGER.tsv", "PRIOR_LEDGER", "transverse realization statuses"),
    ("null_section_hopfion_metric_audit_2026-07-19/AUDIT_REPORT.md", "PRIOR_AUDIT", "null-fiber and Hopf compatibility"),
    ("null_section_hopfion_metric_audit_2026-07-19/STATUS_LEDGER.tsv", "PRIOR_LEDGER", "null-section statuses"),
    ("angular_toric_closure_selector_2026-07-19/AUDIT_REPORT.md", "PRIOR_AUDIT", "conditional angular families and cap gate"),
    ("angular_toric_closure_selector_2026-07-19/STATUS_LEDGER.tsv", "PRIOR_LEDGER", "angular closure statuses"),
    ("reciprocal_clock_optical_scale_selector_2026-07-19/DERIVATION_REPORT.md", "PRIOR_SELECTOR", "static reciprocal null behavior"),
    ("reciprocal_clock_optical_scale_selector_2026-07-19/STATUS_LEDGER.tsv", "PRIOR_LEDGER", "clock optical premise stamps"),
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
