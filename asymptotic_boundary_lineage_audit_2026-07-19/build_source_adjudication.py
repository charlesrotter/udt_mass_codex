#!/usr/bin/env python3
"""Generate one adjudication row for every preregistered load-bearing source."""

from __future__ import annotations

import csv
from pathlib import Path


HERE = Path(__file__).resolve().parent


GROUPS: dict[str, tuple[set[str], str, str, str, str, str]] = {
    "CURRENT_FOUNDATION": ({
        "CANON.md",
        "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md",
        "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md",
        "UDT_RECIPROCAL_C_FOUNDING_POSTULATE_DERIVATION_RESULTS.md",
        "UDT_XMAX_STATUS_CLARIFICATION_2026-07-15.md",
    }, "CANONICAL_STRUCTURE_OR_BOUNDARY_DECLARATION", "CONDITIONAL", "MULTIPLE_OR_OPEN",
       "owner/canon structure; no complete action", "Supplies current meanings and working targets, not a boundary equation."),
    "PREMISE_RESET": ({
        "udt_premise_reset_audit_2026-07-19/AUDIT_REPORT.md",
        "udt_premise_reset_audit_2026-07-19/OWNER_MEANING_LEDGER.tsv",
        "udt_premise_reset_audit_2026-07-19/RERUN_PRIORITY.md",
    }, "CANONICAL_STRUCTURE_OR_BOUNDARY_DECLARATION", "YES", "MULTIPLE_OR_OPEN",
       "current correction overlay", "Controls signed phi, observational c/G, derived X_max, and the audit question."),
    "WRL_SELECTION": ({
        "simple_metric_L_P_selection_derive.py",
        "simple_metric_L_P_selection_derive_out.json",
        "simple_metric_L_P_selection_derive_results.md",
        "simple_metric_L_principle_closure_attack_results.md",
        "simple_metric_L_wall_regularity_closure_out.json",
        "simple_metric_L_wall_regularity_closure_results.md",
        "simple_metric_WR_L_external_triple_blind_audit_results.md",
        "research/macro/verify_wrl_canon.py",
    }, "DERIVED_CONDITIONAL_ON_STATED_PREMISES", "YES", "WRL_WALL",
       "simple reciprocal metric plus residual re-centering and accepted WR-L wall axioms",
       "Selects alpha=1 inside the residual family; X remains supplied/free and the wall is not a terminal universe boundary."),
    "WRL_METRIC_LIMIT": ({
        "SIMPLE_METRIC_MACRO.md",
        "simple_metric_FE_rederive.py",
        "simple_metric_L_native_optical_derive.py",
        "simple_metric_L_native_optical_derive_out.json",
        "simple_metric_L_native_optical_derive_results.md",
        "simple_metric_HL_unification.py",
        "simple_metric_HL_unification_out.json",
        "simple_metric_HL_unification_results.md",
        "simple_metric_timelive_AP_exact_derive_results.md",
        "simple_metric_timelive_AP_intermediate_out.json",
        "simple_metric_timelive_AP_intermediate_results.md",
        "simple_metric_timelive_AP_out.json",
        "simple_metric_timelive_AP_results.md",
        "simple_metric_angular_timelive_L.py",
        "simple_metric_angular_timelive_L_out.json",
        "simple_metric_angular_timelive_L_results.md",
    }, "DERIVED_METRIC_LIMIT", "CONDITIONAL", "WRL_WALL",
       "declared reciprocal WR-L representative; time-live specializations add working diagonal premises",
       "Exact proper/optical/clock/redshift behavior survives; native dynamics and terminality do not."),
    "MACRO_MASS_READOUT": ({
        "simple_metric_J1_build_results.md",
        "simple_metric_J1_honesty_skeleton_results.md",
        "simple_metric_mass_xmax_cascade.md",
        "simple_metric_Pell_mass_lock_derive.md",
        "simple_metric_sphere_ceiling.py",
        "simple_metric_sphere_ceiling_build.py",
        "simple_metric_sphere_ceiling_build_out.json",
        "simple_metric_sphere_ceiling_build_results.md",
        "simple_metric_sphere_ceiling_select_results.md",
    }, "INTERPRETATION_NOT_DERIVED", "NO", "WRL_OR_HYPERBOLIC_ENDPOINT",
       "chosen areal/composition joins plus GR-form Misner-Sharp/Einstein readout",
       "Retains dimensional/conditional reference algebra only; no native mass or X_max relation."),
    "WITHDRAWN_MACRO": ({
        "simple_metric_S3_native_dust_ceiling.py",
        "simple_metric_S3_native_dust_ceiling_out.json",
        "simple_metric_S3_native_dust_ceiling_results.md",
    }, "COUNTEREXAMPLE_OR_NEGATIVE_CONTROL", "NO", "WRL_WALL",
       "superseded wrong G^r_r dust selector",
       "Failure provenance only; profile survives from other premises, dust selection does not."),
    "XMAX_OLD_FRAME": ({
        "simple_metric_xmax_POSTULATE.md",
    }, "CONFLICTED_SEMANTICS", "NO", "HYPERBOLIC_CHART_ENDPOINT",
       "working input maximum and hyperbolic composition chart",
       "Algebraic chart history only; premise reset withdraws its physical-frame authority."),
    "FOLD_CONDITIONAL": ({
        "derive_universe_fold_d1.py",
        "universe_cell_fold_jc_sigma_results.md",
        "universe_cell_T2_identities_results.md",
        "universe_cell_T3_closure_results.md",
        "universe_cell_vacuum_impossibility_results.md",
        "node05_seal_parity_regrade_results.md",
        "F4_seal_boundary_MAP.md",
    }, "DERIVED_CONDITIONAL_ON_STATED_PREMISES", "CONDITIONAL", "CMB_FOLD",
       "historical round-static Branch-P/G reduced action, mirror and variation-class premises",
       "Exact fold pins and conditional budgets survive; complete action, scale, and native mass do not."),
    "ARCHIVED_BOUNDARY_AUDIT": ({
        "archive/native_action_chat_2026-07-14_15/UDT_FINITE_CELL_BOUNDARY_DERIVATION_RESULTS.md",
        "archive/native_action_chat_2026-07-14_15/verify_udt_finite_cell_boundary.py",
        "archive/native_action_chat_2026-07-14_15/verify_udt_finite_cell_boundary_out.txt",
        "archive/native_action_chat_2026-07-14_15/UDT_WRL_SCAFFOLD_NATIVE_ACTION_SEPARATION_DERIVATION_RESULTS.md",
        "archive/native_action_chat_2026-07-14_15/verify_udt_wrl_scaffold_separation.py",
        "archive/native_action_chat_2026-07-14_15/verify_udt_wrl_scaffold_separation_out.txt",
        "archive/native_action_chat_2026-07-14_15/UDT_WRL_SOLUTION_SPACE_CLOSURE_DERIVATION_RESULTS.md",
        "archive/native_action_chat_2026-07-14_15/verify_udt_wrl_solution_space_closure.py",
        "archive/native_action_chat_2026-07-14_15/verify_udt_wrl_solution_space_closure_out.txt",
        "archive/native_action_chat_2026-07-14_15/UDT_WRL_OFFSHELL_PROVENANCE_DERIVATION_RESULTS.md",
        "archive/native_action_chat_2026-07-14_15/UDT_WRL_CONFORMAL_CARRIER_SCALE_CLOSURE_DERIVATION_RESULTS.md",
    }, "DERIVED_CONDITIONAL_ON_STATED_PREMISES", "CONDITIONAL", "MULTIPLE_OR_OPEN",
       "disclosed non-cold archived inverse-action/boundary classes; independent verification was open",
       "Exact algebra may be rerun; supplies counterexamples and object distinctions, not current action authority."),
    "CURRENT_ACTION_ADJUDICATION": ({
        "native_action_final_adjudication_2026-07-18/FINAL_ADJUDICATION_REPORT.md",
        "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv",
    }, "COUNTEREXAMPLE_OR_NEGATIVE_CONTROL", "YES", "OPEN",
       "post-firewall A/B/C adjudication",
       "Current authority that complete action, source, differentiable boundary, and normalized mass remain open."),
    "PRE_FIREWALL": ({
        "archive/B1_mass_dilation_cost_results.md",
        "native_dilation_weight_derivation_results.md",
    }, "COUNTEREXAMPLE_OR_NEGATIVE_CONTROL", "NO", "OPEN",
       "pre-2026-07-01 material",
       "May expose old assumptions or failures only; cannot supply affirmative UDT mass dilation."),
}


def main() -> None:
    with (HERE / "CANDIDATE_UNIVERSE.tsv").open(encoding="utf-8", newline="") as handle:
        candidates = [row for row in csv.DictReader(handle, delimiter="\t") if row["initial_disposition"] == "LOAD_BEARING"]
    registered = {path for paths, *_ in GROUPS.values() for path in paths}
    actual = {row["path"] for row in candidates}
    if actual != registered:
        raise AssertionError(f"source adjudication coverage mismatch: {sorted(actual ^ registered)}")

    group_for: dict[str, tuple[str, str, str, str, str, str]] = {}
    for family, (paths, grade, affirmative, surface, provenance, summary) in GROUPS.items():
        for path in paths:
            if path in group_for:
                raise AssertionError(f"duplicate source group: {path}")
            group_for[path] = (family, grade, affirmative, surface, provenance, summary)

    with (HERE / "SOURCE_ADJUDICATION.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow([
            "path", "first_date", "provenance_era", "family", "primary_evidence_grade",
            "affirmative_current_use", "surface_identity", "action_or_source_provenance", "ruling",
        ])
        for row in sorted(candidates, key=lambda item: item["path"]):
            family, grade, affirmative, surface, provenance, summary = group_for[row["path"]]
            writer.writerow([
                row["path"], row["first_date"], row["provenance_era"], family, grade,
                affirmative, surface, provenance, summary,
            ])
    print(f"PASS load_bearing_sources={len(candidates)} groups={len(GROUPS)}")


if __name__ == "__main__":
    main()
