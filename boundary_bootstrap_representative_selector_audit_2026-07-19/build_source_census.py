#!/usr/bin/env python3
"""Freeze the base repository-wide boundary/bootstrap representative token census."""

from __future__ import annotations

import csv
import hashlib
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "77e29de0f41e27e1837fe8d93ce5d3aa730bf838"
SUFFIXES = {".md", ".tsv", ".txt", ".py", ".json"}
TOKENS = {
    "CSN": r"\bCSN\b|Common[- ]Scale|common scale|conformal representative",
    "REPRESENTATIVE": r"physical representative|representative[- ]selection|selection map|\bSigma:\[g\]|\[g\]_CSN",
    "BOOTSTRAP": r"bootstrap|self-consisten(?:t|cy)|density window|total density",
    "FINITE_CELL": r"finite[- ]cell|finite cell|mirrored cell|odd fold|causal horizon",
    "BOUNDARY_ACTION": r"boundary functional|boundary action|boundary primitive|boundary charge|normalized charge|generator",
    "CLOCK": r"clock direction|clock normalization|clock congruence|lapse|clock.curvature",
    "WRL": r"WR-L|A\s*=\s*1\s*-\s*r\s*/\s*X|residual re.center|residual composition|wall regularity",
    "ANGULAR": r"angular sector|areal radius|angular geometry|r\^2d(?:Omega|\\Omega)|complete coframe",
    "SCALE": r"scale setting|scale-setting|homothet|absolute scale|scale eigenvalue|density center",
    "XMAX_RECIPROCITY": r"X_?max|X\\_\\{\\max\\}|maximum distance|positional reciprocity|reciprocity.*position",
}
LOAD_BEARING = {
    "CANON.md",
    "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md",
    "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md",
    "UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md",
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md",
    "bootstrap_variation_selector_2026-07-18/DERIVATION_REPORT.md",
    "bootstrap_variation_selector_2026-07-18/STATUS_LEDGER.tsv",
    "bootstrap_csn_phi_angular_selector_2026-07-19/AUDIT_REPORT.md",
    "reciprocity_offshell_constraint_selector_2026-07-18/DERIVATION_REPORT.md",
    "asymptotic_boundary_lineage_audit_2026-07-19/AUDIT_REPORT.md",
    "asymptotic_boundary_lineage_audit_2026-07-19/GLOBAL_CLOSURE_EQUATION_LEDGER.tsv",
    "native_boundary_generator_scale_audit_2026-07-19/AUDIT_REPORT.md",
    "clock_curvature_selector_audit_2026-07-19/AUDIT_REPORT.md",
    "clock_curvature_selector_audit_2026-07-19/STATUS_LEDGER.tsv",
    "udt_premise_reset_audit_2026-07-19/AUDIT_REPORT.md",
    "udt_premise_reset_audit_2026-07-19/OWNER_MEANING_LEDGER.tsv",
    "archive/native_action_chat_2026-07-14_15/UDT_CSN_GLOBAL_SCALE_SELECTION_DERIVATION_RESULTS.md",
    "archive/native_action_chat_2026-07-14_15/UDT_FINITE_CELL_BOUNDARY_DERIVATION_RESULTS.md",
    "archive/native_action_chat_2026-07-14_15/UDT_GLOBAL_BOOTSTRAP_DERIVATION_RESULTS.md",
    "archive/native_action_chat_2026-07-14_15/UDT_WRL_SOLUTION_SPACE_CLOSURE_DERIVATION_RESULTS.md",
    "simple_metric_L_wall_regularity_closure_results.md",
    "simple_metric_WR_L_center_recenter_exclusion_results.md",
    "UDT_XMAX_STATUS_CLARIFICATION_2026-07-15.md",
    "xmax_reciprocity_audit_2026-07-19/AUDIT_REPORT.md",
    "xmax_reciprocity_audit_2026-07-19/STATUS_LEDGER.tsv",
    "xmax_full_frame_realization_2026-07-19/AUDIT_REPORT.md",
    "xmax_dynamic_observer_frame_2026-07-19/AUDIT_REPORT.md",
    "xmax_accelerating_finite_cell_cartan_2026-07-19/AUDIT_REPORT.md",
    "udt_premise_reset_audit_2026-07-19/PACKAGE_REGRADE.tsv",
}


def tracked() -> list[tuple[str, str]]:
    raw = subprocess.check_output(["git", "ls-tree", "-r", BASE], cwd=ROOT, text=True)
    return [(line.split("\t", 1)[1], line.split()[2]) for line in raw.splitlines()]


def source_class(path: str) -> str:
    frozen = (
        "native_action_stage1_2026-07-18/", "native_action_stage2_2026-07-18/",
        "native_action_arm_c_2026-07-18/", "native_action_final_adjudication_2026-07-18/",
    )
    if path.startswith(frozen):
        return "HARD_FROZEN"
    if path.startswith("reorganization_r") or path.startswith("research/_registry/"):
        return "ORGANIZATION_RECORD"
    if path.startswith(("archive/", "legacy/", "rescued_workspaces/")):
        return "HISTORICAL_OR_ARCHIVED"
    if "2026-07-19/" in path:
        return "CURRENT_JULY19_EVIDENCE"
    if "2026-07-18/" in path or "2026-07-18" in path:
        return "POST_FIREWALL_EVIDENCE"
    if "/TEST_TRANSCRIPT" in path or path.endswith(("_out.txt", ".json")):
        return "GENERATED_OR_RAW"
    if "/" not in path and path in {"LIVE.md", "HANDOFF.md", "INDEX.md", "CANON.md", "AGENTS.md", "CLAUDE.md"}:
        return "CONTROL_OR_CANON"
    return "OTHER_TRACKED_CONTEXT"


def main() -> None:
    output = HERE / "SOURCE_CENSUS.tsv"
    fields = ["path", "blob", "sha256", "size_bytes", "matched_tokens", "source_class", "initial_disposition"]
    records = []
    for path, blob in tracked():
        local = ROOT / path
        if local.suffix.lower() not in SUFFIXES or not local.is_file():
            continue
        data = local.read_bytes()
        if b"\0" in data:
            continue
        text = data.decode("utf-8", "replace")
        matches = [name for name, pattern in TOKENS.items() if re.search(pattern, text, re.IGNORECASE)]
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
    records.sort(key=lambda row: row["path"])
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(records)
    counts: dict[str, int] = {}
    for row in records:
        counts[row["initial_disposition"]] = counts.get(row["initial_disposition"], 0) + 1
    print(f"PASS rows={len(records)} load_bearing={len(LOAD_BEARING)} dispositions={counts}")


if __name__ == "__main__":
    main()
