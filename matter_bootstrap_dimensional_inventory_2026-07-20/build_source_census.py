#!/usr/bin/env python3
"""Freeze the preregistered base-tree matter/scale source census."""

from __future__ import annotations

import csv
import hashlib
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "ab099c9c642d68049cfc4810fd709df638ce591c"
PACKAGE = "matter_bootstrap_dimensional_inventory_2026-07-20/"
SUFFIXES = {".md", ".tsv", ".txt", ".py", ".json"}
TOKENS = {
    "NONULL": r"noNull|no-null",
    "HOPFION": r"hopfion|Hopf|Q_H",
    "CARRIER": r"carrier|target S.?2|unit.3.vector",
    "L2_L4": r"L2.?\+.?L4|E2|E4|Faddeev|Skyrme",
    "COEFFICIENT": r"coefficient|coupling|normalization|xi|kappa",
    "MASS": r"mass|M_N|Komar|ADM",
    "VIRIAL": r"virial|Derrick|dilat(?:ion|ional)",
    "INERTIA": r"inertia|frequency|omega|fixed.?Q|isorotation",
    "DOMAIN": r"finite.?box|half.?width|grid|spacing|boundary|mask",
    "BOOTSTRAP": r"bootstrap|self-consisten(?:t|cy)|emergence",
    "GLOBAL_SCALE": r"X_?max|X\\_\\{\\max\\}|absolute scale|scale breaker|common scale|CSN",
    "ANCHORS": r"c_?E|c\\_\\{E\\}|G_?obs|G\\_\\{\\rm obs\\}",
}

LOAD_BEARING = {
    "LIVE.md",
    "INDEX.md",
    "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md",
    "UDT_S2_CARRIER_STATUS_CLARIFICATION_2026-07-15.md",
    "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md",
    "matter_carrier_provenance_audit_results.md",
    "native_hopfion_topology_audit_2026-07-19/AUDIT_REPORT.md",
    "native_hopfion_topology_audit_2026-07-19/TOPOLOGY_STATUS_LEDGER.tsv",
    "native_action_final_adjudication_2026-07-18/FINAL_ADJUDICATION_REPORT.md",
    "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv",
    "scale_breaking_closure_census_2026-07-20/AUDIT_REPORT.md",
    "scale_breaking_closure_census_2026-07-20/SCALE_WEIGHT_LEDGER.tsv",
    "scale_breaking_closure_census_2026-07-20/STATUS_LEDGER.tsv",
    "stability_branch_follow_256_DECISION.md",
    "noNull_energy.py",
    "noNull_resolve.py",
    "noNull_boxscout_build.py",
    "noNull_boxscout_build.json",
    "noNull_behavioral_F.py",
    "noNull_behavioral_F_results.md",
    "noNull_stability_evidence.json",
    "noNull_schur_inertia.py",
    "noNull_phaseG_mass.py",
    "noNull_phaseG_mass_ALL.json",
    "noNull_phaseG_mass_results.md",
    "noNull_boundary_virial.py",
    "noNull_boundary_virial_ALL.json",
    "noNull_boundary_virial_results.md",
    "noNull_virial_identity_derivation.md",
    "hopfion_arc_scripts_2026-07-05/fs_hopfion.py",
    "hopfion_fixedQ_collective_phase0.py",
    "hopfion_fixedQ_collective_phase0_out.json",
    "hopfion_fixedQ_collective_phase0_results.md",
    "hopfion_fixedQ_phase1_isorotation.py",
    "hopfion_fixedQ_phase1_isorotation_out.json",
    "hopfion_fixedQ_phase1_isorotation_results.md",
    "hopfion_fixedQ_phase1b_production.py",
    "hopfion_fixedQ_phase1b_production_out.json",
    "hopfion_fixedQ_phase1b_production_results.md",
    "hopfion_static_mass_common.py",
    "hopfion_mass_background_coupling_MAP.md",
}


def tracked() -> list[tuple[str, str]]:
    raw = subprocess.check_output(["git", "ls-tree", "-r", BASE], cwd=ROOT, text=True)
    return [(line.split("\t", 1)[1], line.split()[2]) for line in raw.splitlines()]


def source_class(path: str) -> str:
    if path.startswith((
        "native_action_stage1_2026-07-18/", "native_action_stage2_2026-07-18/",
        "native_action_arm_c_2026-07-18/", "native_action_final_adjudication_2026-07-18/",
    )):
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
    missing = LOAD_BEARING - {row["path"] for row in records}
    if missing:
        raise AssertionError(f"load-bearing sources missed: {sorted(missing)}")
    records.sort(key=lambda row: row["path"])
    with (HERE / "SOURCE_CENSUS.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)
    counts: dict[str, int] = {}
    for row in records:
        counts[row["initial_disposition"]] = counts.get(row["initial_disposition"], 0) + 1
    print(f"PASS rows={len(records)} load_bearing={len(LOAD_BEARING)} dispositions={counts}")


if __name__ == "__main__":
    main()
