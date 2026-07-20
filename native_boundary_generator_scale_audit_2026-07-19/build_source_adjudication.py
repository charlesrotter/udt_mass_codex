#!/usr/bin/env python3
"""Adjudicate every explicit load-bearing source in the frozen candidate census."""

from __future__ import annotations

import csv
from pathlib import Path


HERE = Path(__file__).resolve().parent


def classify(path: str) -> tuple[str, str, str, str]:
    if path == "LIVE.md":
        return "CONTROL", "CURRENT_NAVIGATION", "Current caveated boundary ruling and authority limit", "YES_CONTROL"
    if path == "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md":
        return "OWNER_FOUNDATION", "FOUNDING", "Local common scale is calibrational; scale must emerge, but no emergence equation is supplied", "YES_STRUCTURE"
    if path == "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md":
        return "OWNER_WORKING", "WORKING", "Matter-bearing complete solutions occupy a narrow total-density window; center and width are not supplied", "YES_WORKING_ONLY"
    if path == "UDT_XMAX_STATUS_CLARIFICATION_2026-07-15.md":
        return "OWNER_CLARIFICATION", "WORKING_LEAD", "Xmax=alpha*G*M/c^2 is dimensional only and needs an independent native closure", "YES_STATUS_ONLY"
    if path == "UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md":
        return "CURRENT_SELECTOR", "CONDITIONAL_OPEN", "Action, variation, and boundary selectors remain open", "YES_STATUS_ONLY"
    if path.startswith("asymptotic_boundary_lineage_audit_2026-07-19/"):
        grade = "DERIVED_METRIC" if path.endswith(("DERIVATION_RESULT.json", "QUANTITY_LIMIT_LEDGER.tsv")) else "VERIFIED_WITH_CAVEATS"
        return "CURRENT_BOUNDARY_AUDIT", grade, "WR-L raw wall flux and limits exact; normalized mass and global Xmax join open", "YES_BOUNDED"
    if path.startswith("bootstrap_variation_selector_2026-07-18/"):
        return "CURRENT_BOOTSTRAP_AUDIT", "UNDERDETERMINED", "Bootstrap is on-shell admissibility and does not select variation placement or action", "YES_STATUS_ONLY"
    if path.startswith("native_action_final_adjudication_2026-07-18/"):
        return "FINAL_ABC_ADJUDICATION", "CURRENT_STATUS", "Normalized finite-cell charge and complete action remain open", "YES_STATUS_ONLY"
    if path.startswith("native_action_arm_c_2026-07-18/"):
        return "FROZEN_ARM_C", "ADVERSARIAL_EVIDENCE", "Boundary/action ambiguities and mass-priority challenge", "YES_CHALLENGE"
    if path.startswith("native_action_stage1_2026-07-18/"):
        return "FROZEN_STAGE_I", "COLD_DERIVATION_EVIDENCE", "Action countermodels and branch-relative fluxes show non-uniqueness", "YES_CONDITIONAL"
    if path.startswith("native_action_stage2_2026-07-18/"):
        return "FROZEN_STAGE_II", "HISTORICAL_CHALLENGE_RESPONSE", "Conditional mass/virial and boundary findings under disclosed packet", "YES_CONDITIONAL"
    if path.endswith("verify_udt_wrl_solution_space_closure.py"):
        return "ARCHIVED_WRL_EXECUTABLE", "RERUN_ONLY", "Exact WR-L flux/curvature algebra; no physical authority", "YES_ALGEBRA_ONLY"
    if path.endswith("verify_udt_finite_cell_boundary.py"):
        return "ARCHIVED_BOUNDARY_EXECUTABLE", "RERUN_ONLY", "Exact total-derivative and boundary-shift algebra; no action selection", "YES_ALGEBRA_ONLY"
    if "UDT_WRL_SOLUTION_SPACE_CLOSURE" in path:
        return "ARCHIVED_WRL_REPORT", "POST_JULY_CONDITIONAL", "Finite raw lapse flux is radius-dependent and unnormalized", "YES_CONDITIONAL"
    if "UDT_FINITE_CELL_BOUNDARY" in path:
        return "ARCHIVED_BOUNDARY_REPORT", "POST_JULY_CONDITIONAL", "Boundary primitive and normalized mass are not fixed by fold values", "YES_CONDITIONAL"
    if "UDT_FOUNDING_TO_DYNAMICS" in path:
        return "ARCHIVED_DYNAMICS_REPORT", "POST_JULY_CONDITIONAL", "Action rescaling/total derivatives preserve bulk equations while shifting generators", "YES_COUNTEREXAMPLE"
    if "UDT_GLOBAL_BOOTSTRAP_DERIVATION" in path:
        return "ARCHIVED_BOOTSTRAP_REPORT", "POST_JULY_CONDITIONAL", "Earlier attempted closure remains premise-scoped and non-authoritative", "CONTEXT_ONLY"
    raise AssertionError(f"unclassified load-bearing source: {path}")


def main() -> None:
    with (HERE / "CANDIDATE_UNIVERSE.tsv").open(encoding="utf-8", newline="") as handle:
        candidates = [row for row in csv.DictReader(handle, delimiter="\t") if row["initial_disposition"] == "LOAD_BEARING"]
    if len(candidates) != 27:
        raise AssertionError(f"expected 27 load-bearing sources, got {len(candidates)}")
    output = HERE / "SOURCE_ADJUDICATION.tsv"
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow([
            "path", "sha256", "provenance_era", "source_family", "evidence_grade",
            "extracted_ruling", "current_use",
        ])
        for row in candidates:
            family, grade, ruling, use = classify(row["path"])
            writer.writerow([row["path"], row["sha256"], row["provenance_era"], family, grade, ruling, use])
    print(f"PASS sources={len(candidates)} families={len({classify(row['path'])[0] for row in candidates})}")


if __name__ == "__main__":
    main()
