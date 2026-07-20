#!/usr/bin/env python3
"""Freeze the preregistered base-tree angular derivative-weight source census."""

from __future__ import annotations

import csv
import hashlib
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "f571842106f0a341e2b8db4e7dd64fc3e4ac03cc"
PACKAGE = "angular_derivative_weight_selector_2026-07-20/"
SUFFIXES = {".md", ".tsv", ".txt", ".py", ".json"}
TOKENS = {
    "CSN": r"\bCSN\b|Common[- ]Scale|conformal|Weyl",
    "DERIVATIVE_ORDER": r"two[- ]derivative|four[- ]derivative|derivative order|\bL2\b|\bL4\b|\bE2\b|\bE4\b",
    "ACTION": r"action|variation|Euler|Bach|Einstein.Hilbert|\bEH\b|curvature.square",
    "ANGULAR": r"angular|transverse|toric|circle|Hopf|quotient|fiber|fibration|S.?2|S.?3",
    "INVARIANT": r"invariant|scalar|Ricci|Riemann|Pontryagin|Gauss.Bonnet|area.form|two.form",
    "COEFFICIENT": r"coefficient|coupling|normalization|weight|kappa|xi",
    "BOUNDARY": r"finite.?cell|boundary|seal|cap|corner|mirror",
    "BOOTSTRAP": r"bootstrap|self.consisten|density window|total density",
    "XMAX": r"X_?max|X\\_\\{\\max\\}|maximum (?:distance|reach)|reciprocity",
    "SCALE": r"absolute scale|scale.break|scale selection|representative|compensator|dilaton",
}

LOAD_BEARING = {
    "CANON.md",
    "LIVE.md",
    "UDT_NATIVE_ACTION_COLD_ARM_DISPATCH.md",
    "UDT_NATIVE_ACTION_COLD_PACKET.md",
    "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md",
    "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md",
    "UDT_XMAX_STATUS_CLARIFICATION_2026-07-15.md",
    "UDT_S2_CARRIER_STATUS_CLARIFICATION_2026-07-15.md",
    "UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md",
    "native_action_final_adjudication_2026-07-18/FINAL_ADJUDICATION_REPORT.md",
    "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv",
    "native_action_final_adjudication_2026-07-18/COUNTERMODEL_COMPLETENESS_FINAL.tsv",
    "matter_bootstrap_dimensional_inventory_2026-07-20/AUDIT_REPORT.md",
    "matter_bootstrap_dimensional_inventory_2026-07-20/STATUS_LEDGER.tsv",
    "matter_bootstrap_dimensional_inventory_2026-07-20/DIMENSIONAL_OBJECT_LEDGER.tsv",
    "matter_bootstrap_dimensional_inventory_2026-07-20/NEXT_SCIENTIFIC_DECISION.md",
    "scale_breaking_closure_census_2026-07-20/AUDIT_REPORT.md",
    "scale_breaking_closure_census_2026-07-20/STATUS_LEDGER.tsv",
    "native_hopfion_topology_audit_2026-07-19/AUDIT_REPORT.md",
    "native_hopfion_topology_audit_2026-07-19/TOPOLOGY_STATUS_LEDGER.tsv",
    "null_section_hopfion_metric_audit_2026-07-19/AUDIT_REPORT.md",
    "null_section_hopfion_metric_audit_2026-07-19/STATUS_LEDGER.tsv",
    "null_section_hopfion_metric_audit_2026-07-19/DERIVATION_RESULT.json",
    "angular_toric_closure_selector_2026-07-19/AUDIT_REPORT.md",
    "angular_toric_closure_selector_2026-07-19/STATUS_LEDGER.tsv",
    "angular_toric_closure_selector_2026-07-19/DERIVATION_RESULT.json",
    "bootstrap_csn_phi_angular_selector_2026-07-19/AUDIT_REPORT.md",
    "bootstrap_csn_phi_angular_selector_2026-07-19/STATUS_LEDGER.tsv",
    "bootstrap_csn_phi_angular_selector_2026-07-19/CANDIDATE_OPERATOR.tsv",
    "boundary_bootstrap_representative_selector_audit_2026-07-19/AUDIT_REPORT.md",
    "boundary_bootstrap_representative_selector_audit_2026-07-19/STATUS_LEDGER.tsv",
    "matter_carrier_provenance_audit_results.md",
    "noNull_energy.py",
}


def tracked() -> list[tuple[str, str]]:
    raw = subprocess.check_output(["git", "ls-tree", "-r", BASE], cwd=ROOT, text=True)
    return [(line.split("\t", 1)[1], line.split()[2]) for line in raw.splitlines()]


def source_class(path: str) -> str:
    if path.startswith(("native_action_stage1_2026-07-18/", "native_action_stage2_2026-07-18/",
                        "native_action_arm_c_2026-07-18/", "native_action_final_adjudication_2026-07-18/")):
        return "HARD_FROZEN"
    if path.startswith("reorganization_r") or path.startswith("research/_registry/"):
        return "ORGANIZATION_RECORD"
    if path.startswith(("archive/", "legacy/", "rescued_workspaces/")):
        return "HISTORICAL_OR_ARCHIVED"
    if "2026-07-20/" in path or "2026-07-20" in path:
        return "CURRENT_JULY20_EVIDENCE"
    if "2026-07-19/" in path or "2026-07-19" in path:
        return "CURRENT_JULY19_EVIDENCE"
    if path.endswith(("_out.txt", ".npz", ".log")):
        return "GENERATED_OR_RAW"
    if "/" not in path and path in {"LIVE.md", "HANDOFF.md", "INDEX.md", "CANON.md", "AGENTS.md", "CLAUDE.md"}:
        return "CONTROL_OR_CANON"
    return "OTHER_TRACKED_CONTEXT"


def main() -> None:
    fields = ["path", "blob", "sha256", "size_bytes", "matched_tokens", "source_class", "initial_disposition"]
    records: list[dict[str, str]] = []
    for path, blob in tracked():
        if path.startswith(PACKAGE) or Path(path).suffix.lower() not in SUFFIXES:
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
            disposition = "PROVENANCE_OR_COUNTEREXAMPLE_ONLY"
        elif klass == "ORGANIZATION_RECORD":
            disposition = "EXCLUDED_GENERATED_ORGANIZATION"
        elif path.endswith(("TEST_TRANSCRIPT.txt", "VERIFICATION_TRANSCRIPT.txt", "REPOSITORY_GATES.json")):
            disposition = "EXCLUDED_DUPLICATE_RAW_RECORD"
        else:
            disposition = "CONTEXT_CANDIDATE"
        records.append({"path": path, "blob": blob, "sha256": hashlib.sha256(data).hexdigest(),
                        "size_bytes": str(len(data)), "matched_tokens": ";".join(matches),
                        "source_class": klass, "initial_disposition": disposition})
    missing = LOAD_BEARING - {row["path"] for row in records}
    if missing:
        raise AssertionError(f"load-bearing sources missed: {sorted(missing)}")
    records.sort(key=lambda row: row["path"])
    with (HERE / "SOURCE_CENSUS.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(records)
    counts: dict[str, int] = {}
    for row in records:
        counts[row["initial_disposition"]] = counts.get(row["initial_disposition"], 0) + 1
    print(f"PASS rows={len(records)} load_bearing={len(LOAD_BEARING)} dispositions={counts}")


if __name__ == "__main__":
    main()
