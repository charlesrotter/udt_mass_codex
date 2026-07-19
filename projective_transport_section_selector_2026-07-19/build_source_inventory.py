#!/usr/bin/env python3
"""Build the base-pinned source inventory for the projective transport audit."""

from __future__ import annotations

import csv
import hashlib
import pathlib
import subprocess


BASE = "75c62d1a357821d4957588e640ba03f0bc0f285e"
SOURCES = [
    ("UDT_NATIVE_ACTION_COLD_PACKET.md", "FOUNDATION", "exact C0/C1 and open-slot ledger"),
    ("UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md", "FOUNDATION", "positive conformal equivalence"),
    ("UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md", "FOUNDATION", "on-shell admissibility wording and limits"),
    ("CANON.md", "FINITE_CELL_AUTHORITY", "finite cell and static phi seal entries only"),
    ("UDT_SCIENTIFIC_FRONTIER_2026-07-19.md", "FRONTIER", "controlling pre-audit scientific status"),
    ("transverse_reciprocal_realization_selector_2026-07-19/AUDIT_REPORT.md", "PRIOR_AUDIT", "conditional reciprocal projective theorem and physical gate"),
    ("transverse_reciprocal_realization_selector_2026-07-19/STATUS_LEDGER.tsv", "PRIOR_LEDGER", "premise-stamped reciprocal realization status"),
    ("transverse_reciprocal_realization_selector_2026-07-19/DERIVATION_RESULT.json", "PRIOR_ALGEBRA", "exact spin projective identities and counterfamilies"),
    ("null_section_hopfion_metric_audit_2026-07-19/AUDIT_REPORT.md", "PRIOR_AUDIT", "null fiber Hopf witness and section caveats"),
    ("null_section_hopfion_metric_audit_2026-07-19/STATUS_LEDGER.tsv", "PRIOR_LEDGER", "null section status distinctions"),
    ("native_hopfion_topology_audit_2026-07-19/AUDIT_REPORT.md", "PRIOR_AUDIT", "celestial S2 and carrier type distinction"),
    ("native_hopfion_topology_audit_2026-07-19/TOPOLOGY_STATUS_LEDGER.tsv", "PRIOR_LEDGER", "topology and section statuses"),
    ("angular_toric_closure_selector_2026-07-19/AUDIT_REPORT.md", "PRIOR_AUDIT", "conditional toric theorem and cap gate"),
    ("angular_toric_closure_selector_2026-07-19/STATUS_LEDGER.tsv", "PRIOR_LEDGER", "angular premise and closure statuses"),
    ("copresence_causal_accessibility_selector_2026-07-19/DERIVATION_REPORT.md", "PRIOR_SELECTOR", "co-presence and causal-accessibility status"),
    ("copresence_causal_accessibility_selector_2026-07-19/STATUS_LEDGER.tsv", "PRIOR_LEDGER", "causal propagation distinctions"),
    ("reciprocal_clock_optical_scale_selector_2026-07-19/DERIVATION_REPORT.md", "PRIOR_SELECTOR", "conditional optical/null behavior"),
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
