#!/usr/bin/env python3
"""Build the base-pinned source inventory for the bootstrap/CSN selector audit."""

from __future__ import annotations

import csv
import hashlib
import pathlib
import subprocess


BASE = "58a3fa8dbc7b4cb7de55313efc361194fdc65114"
SOURCES = [
    ("UDT_NATIVE_ACTION_COLD_PACKET.md", "FOUNDATION", "exact C0/C1 and open action/domain ledger"),
    ("UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md", "FOUNDATION", "local common-scale equivalence and explicit non-conclusions"),
    ("UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md", "WORKING_PRINCIPLE", "on-shell closure and density-window wording"),
    ("UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md", "SELECTOR_AUDIT", "open locality, fields, derivative order, and variation domain"),
    ("UDT_SCIENTIFIC_FRONTIER_2026-07-19.md", "FRONTIER", "controlling pre-audit scientific status"),
    ("CANON.md", "LIMITED_AUTHORITY_AND_SCOPE_EXCEPTION", "static phi seal used; pre-July C-2026-06-10-3 weld disclosed but excluded from affirmative use by the July-1 firewall and not selector-adjudicated"),
    ("bootstrap_variation_selector_2026-07-18/DERIVATION_REPORT.md", "PRIOR_AUDIT", "three bootstrap placements and selector obstruction"),
    ("bootstrap_variation_selector_2026-07-18/STATUS_LEDGER.tsv", "PRIOR_LEDGER", "bootstrap placement statuses"),
    ("bootstrap_variation_selector_2026-07-18/PREMISE_LEDGER.tsv", "PRIOR_LEDGER", "bootstrap premise audit"),
    ("bootstrap_variation_selector_2026-07-18/DERIVATION_RESULT.json", "PRIOR_ALGEBRA", "exact formal placement algebra"),
    ("native_action_final_adjudication_2026-07-18/FINAL_ADJUDICATION_REPORT.md", "ADJUDICATION", "action and source status"),
    ("native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv", "ADJUDICATION_LEDGER", "reciprocal, Bach, EH, and open-action labels"),
    ("projective_transport_section_selector_2026-07-19/AUDIT_REPORT.md", "PRIOR_AUDIT", "propagation versus null-line selection"),
    ("projective_transport_section_selector_2026-07-19/STATUS_LEDGER.tsv", "PRIOR_LEDGER", "Petrov and projective transport statuses"),
    ("projective_transport_section_selector_2026-07-19/DERIVATION_RESULT.json", "PRIOR_ALGEBRA", "conformal transport and Petrov root checks"),
    ("reciprocal_metric_null_line_selector_2026-07-19/AUDIT_REPORT.md", "PRIOR_AUDIT", "exact eikonal/Petrov obstruction"),
    ("reciprocal_metric_null_line_selector_2026-07-19/STATUS_LEDGER.tsv", "PRIOR_LEDGER", "reciprocal causal and Petrov statuses"),
    ("reciprocal_metric_null_line_selector_2026-07-19/DERIVATION_RESULT.json", "PRIOR_ALGEBRA", "exact causal-gradient and Petrov evidence"),
    ("native_hopfion_topology_audit_2026-07-19/AUDIT_REPORT.md", "CARRIER_BOUNDARY", "conditional fiber-versus-section obstruction"),
    ("native_hopfion_topology_audit_2026-07-19/TOPOLOGY_STATUS_LEDGER.tsv", "CARRIER_LEDGER", "carrier remains conditional"),
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
