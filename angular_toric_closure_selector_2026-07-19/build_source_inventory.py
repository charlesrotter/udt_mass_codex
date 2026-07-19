#!/usr/bin/env python3
"""Build the base-pinned source inventory for the angular-toric closure audit."""

from __future__ import annotations

import csv
import hashlib
import pathlib
import subprocess


BASE = "cc7b08381281fa104661df5b6af9fb030cabac95"
SOURCES = [
    ("UDT_NATIVE_ACTION_COLD_PACKET.md", "FOUNDATION", "slot, transverse-block and finite-cell limits"),
    ("CANON.md", "FINITE_CELL_AUTHORITY", "C-2026-06-10-2 and C-2026-07-04-1 physical mirrored-cell and monotonic finite-domain scope"),
    ("UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md", "FOUNDATION", "positive common-scale scope"),
    ("UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md", "FOUNDATION", "registered on-shell global selection wording"),
    ("UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md", "FOUNDATION_SUPPORT", "reciprocal exponential derivation and readout limits"),
    ("bootstrap_variation_selector_2026-07-18/DERIVATION_REPORT.md", "SELECTOR_STATUS", "bootstrap supplies no off-shell map or bridge"),
    ("null_section_hopfion_metric_audit_2026-07-19/PREREGISTRATION.md", "PRIOR_SCOPE", "prior candidate and falsification contract"),
    ("null_section_hopfion_metric_audit_2026-07-19/AUDIT_REPORT.md", "PRIOR_AUDIT", "exact orbit-block witness and open selection seam"),
    ("null_section_hopfion_metric_audit_2026-07-19/STATUS_LEDGER.tsv", "PRIOR_LEDGER", "premise-stamped angular and topology statuses"),
    ("null_section_hopfion_metric_audit_2026-07-19/DERIVATION_RESULT.json", "PRIOR_ALGEBRA", "exact reciprocal/Hopf identities"),
    ("native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv", "ACTION_STATUS", "boundary/action/carrier remain open"),
    ("UDT_SCIENTIFIC_FRONTIER_2026-07-19.md", "FRONTIER", "controlling pre-audit scientific status"),
]


def git(repo: pathlib.Path, *args: str, binary: bool = False):
    completed = subprocess.run(
        ["git", *args], cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=not binary, check=True,
    )
    return completed.stdout


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
