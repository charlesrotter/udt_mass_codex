#!/usr/bin/env python3
"""Freeze the preregistered base-wide scale-closure token census."""

from __future__ import annotations

import csv
import hashlib
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "ff1df31c10303ae8deb8438f36ce66f76130c819"
PACKAGE = "scale_breaking_closure_census_2026-07-20/"
SUFFIXES = {".md", ".tsv", ".txt", ".py", ".json"}
TOKENS = {
    "XMAX": r"X_?max|X\\_\\{\\max\\}|maximum (?:distance|reach)",
    "HOMOTHETY": r"homothet|common scaling|absolute scale|scale[- ]breaking|scale eigenvalue",
    "CSN": r"\\bCSN\\b|Common[- ]Scale|common scale|conformal representative",
    "BOOTSTRAP": r"bootstrap|self-consisten(?:t|cy)|density window|density center",
    "DENSITY": r"rho_?tot|rho\\_\\{\\rm tot\\}|total (?:proper )?density|mass density",
    "MASS": r"mass|M_?tot|M\\_\\{\\rm tot\\}",
    "CHARGE_FLUX": r"charge|flux|generator|boundary primitive",
    "BOUNDARY": r"boundary|finite[- ]cell|finite cell|causal horizon|wall",
    "GEOMETRY": r"surface gravity|curvature|proper volume|proper length|angular area|wall area",
    "TOPOLOGY": r"topolog|winding|Hopf|\\bQ\\b",
    "ANCHORS": r"c_?E|c\\_\\{E\\}|G_?obs|G\\_\\{\\rm obs\\}",
    "RECIPROCITY": r"reciproc",
}

LOAD_BEARING = {
    "CANON.md",
    "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md",
    "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md",
    "UDT_XMAX_STATUS_CLARIFICATION_2026-07-15.md",
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md",
    "udt_premise_reset_audit_2026-07-19/AUDIT_REPORT.md",
    "udt_premise_reset_audit_2026-07-19/OWNER_MEANING_LEDGER.tsv",
    "udt_premise_reset_audit_2026-07-19/PACKAGE_REGRADE.tsv",
    "udt_premise_reset_audit_2026-07-19/POST_PREREG_C_G_SCALE_CLARIFICATION.md",
    "asymptotic_boundary_lineage_audit_2026-07-19/AUDIT_REPORT.md",
    "asymptotic_boundary_lineage_audit_2026-07-19/GLOBAL_CLOSURE_EQUATION_LEDGER.tsv",
    "asymptotic_boundary_lineage_audit_2026-07-19/MASS_PROVENANCE_LEDGER.tsv",
    "asymptotic_boundary_lineage_audit_2026-07-19/QUANTITY_LIMIT_LEDGER.tsv",
    "native_boundary_generator_scale_audit_2026-07-19/AUDIT_REPORT.md",
    "native_boundary_generator_scale_audit_2026-07-19/CHARGE_REQUIREMENT_LEDGER.tsv",
    "native_boundary_generator_scale_audit_2026-07-19/SCALE_CLOSURE_LEDGER.tsv",
    "clock_curvature_selector_audit_2026-07-19/AUDIT_REPORT.md",
    "clock_curvature_selector_audit_2026-07-19/STATUS_LEDGER.tsv",
    "boundary_bootstrap_representative_selector_audit_2026-07-19/AUDIT_REPORT.md",
    "boundary_bootstrap_representative_selector_audit_2026-07-19/SELECTOR_CANDIDATE_LEDGER.tsv",
    "boundary_bootstrap_representative_selector_audit_2026-07-19/SELECTOR_REQUIREMENT_MATRIX.tsv",
    "boundary_bootstrap_representative_selector_audit_2026-07-19/DERIVATION_RESULT.json",
    "xmax_reciprocity_audit_2026-07-19/AUDIT_REPORT.md",
    "xmax_reciprocity_audit_2026-07-19/STATUS_LEDGER.tsv",
    "xmax_reciprocity_audit_2026-07-19/DERIVATION_RESULT.json",
    "bootstrap_variation_selector_2026-07-18/DERIVATION_REPORT.md",
    "bootstrap_variation_selector_2026-07-18/STATUS_LEDGER.tsv",
    "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv",
    "native_action_final_adjudication_2026-07-18/FINAL_ADJUDICATION_REPORT.md",
    "angular_toric_closure_selector_2026-07-19/STATUS_LEDGER.tsv",
    "noNull_phaseG_mass_results.md",
    "noNull_boundary_virial_results.md",
    "stability_branch_follow_256_DECISION.md",
}


def tracked() -> list[tuple[str, str]]:
    raw = subprocess.check_output(["git", "ls-tree", "-r", BASE], cwd=ROOT, text=True)
    return [(line.split("\t", 1)[1], line.split()[2]) for line in raw.splitlines()]


def source_class(path: str) -> str:
    hard_frozen = (
        "native_action_stage1_2026-07-18/", "native_action_stage2_2026-07-18/",
        "native_action_arm_c_2026-07-18/", "native_action_final_adjudication_2026-07-18/",
    )
    if path.startswith(hard_frozen):
        return "HARD_FROZEN"
    if path.startswith("reorganization_r") or path.startswith("research/_registry/"):
        return "ORGANIZATION_RECORD"
    if path.startswith(("archive/", "legacy/", "rescued_workspaces/")):
        return "HISTORICAL_OR_ARCHIVED"
    if "2026-07-19/" in path or "2026-07-19" in path:
        return "CURRENT_JULY19_EVIDENCE"
    if "2026-07-18/" in path or "2026-07-18" in path:
        return "POST_FIREWALL_EVIDENCE"
    if "/TEST_TRANSCRIPT" in path or path.endswith(("_out.txt", ".npz")):
        return "GENERATED_OR_RAW"
    if "/" not in path and path in {"LIVE.md", "HANDOFF.md", "INDEX.md", "CANON.md", "AGENTS.md", "CLAUDE.md"}:
        return "CONTROL_OR_CANON"
    return "OTHER_TRACKED_CONTEXT"


def main() -> None:
    output = HERE / "SOURCE_CENSUS.tsv"
    fields = ["path", "blob", "sha256", "size_bytes", "matched_tokens", "source_class", "initial_disposition"]
    records: list[dict[str, str]] = []
    for path, blob in tracked():
        if path.startswith(PACKAGE):
            continue
        local = ROOT / path
        if local.suffix.lower() not in SUFFIXES:
            continue
        data = subprocess.check_output(["git", "show", f"{BASE}:{path}"], cwd=ROOT)
        if b"\0" in data:
            continue
        content = data.decode("utf-8", "replace")
        matches = [name for name, pattern in TOKENS.items() if re.search(pattern, content, re.IGNORECASE)]
        if not matches:
            continue
        klass = source_class(path)
        if path in LOAD_BEARING:
            disposition = "LOAD_BEARING_CANDIDATE"
        elif klass in {"HARD_FROZEN", "HISTORICAL_OR_ARCHIVED"}:
            disposition = "PROVENANCE_OR_CONTEXT_ONLY"
        elif klass == "ORGANIZATION_RECORD":
            disposition = "EXCLUDED_GENERATED_ORGANIZATION"
        elif path.endswith(("TEST_TRANSCRIPT.txt", "VERIFICATION_TRANSCRIPT.txt", "REPOSITORY_GATES.json")):
            disposition = "EXCLUDED_DUPLICATE_RAW_RECORD"
        else:
            disposition = "CONTEXT_CANDIDATE"
        records.append({
            "path": path,
            "blob": blob,
            "sha256": hashlib.sha256(data).hexdigest(),
            "size_bytes": str(len(data)),
            "matched_tokens": ";".join(matches),
            "source_class": klass,
            "initial_disposition": disposition,
        })
    missing = LOAD_BEARING - {row["path"] for row in records}
    if missing:
        raise AssertionError(f"load-bearing sources missed by tokens: {sorted(missing)}")
    records.sort(key=lambda row: row["path"])
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)
    counts: dict[str, int] = {}
    for row in records:
        counts[row["initial_disposition"]] = counts.get(row["initial_disposition"], 0) + 1
    print(f"PASS rows={len(records)} load_bearing={len(LOAD_BEARING)} dispositions={counts}")


if __name__ == "__main__":
    main()
