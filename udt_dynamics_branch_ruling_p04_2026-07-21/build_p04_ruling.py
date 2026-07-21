#!/usr/bin/env python3
"""Build the P04 owner-authorized conditional dynamics-lane ruling."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MAXIMUM = "DYNAMICS_LANES_AUTHORIZED_OR_REMAIN_OPEN"

SOURCES = {
    "P03G_MANIFEST": ("udt_global_kinematic_assembly_p03g_2026-07-21/SHA256SUMS.txt", "62f9b3f33409b62fb841734e8a91e61d9b859247bf808c4a6cf3740b6a54b6c9"),
    "P03_MANIFEST": ("udt_founded_constraint_atlas_p03_2026-07-21/SHA256SUMS.txt", "b0ec5cbb2be404084e1b1ed4eca98d53c9712a62cf1af0a48eb340b64467c3be"),
    "COMPLETE_MAP_MANIFEST": ("udt_complete_metric_solution_space_map_2026-07-21/SHA256SUMS.txt", "1778e4dcfcf9ac0bd3574fb3ff5248f2990265fa40d0822ff964ac67c434ae38"),
    "FINAL_ACTION_MANIFEST": ("native_action_final_adjudication_2026-07-18/SHA256SUMS.txt", "57be0046432c27046e84eaafd1706959558f43170d0f1e23dc3047966e512f33"),
    "SELECTOR_AUDIT": ("UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md", "db4a426b021e375fa4bca0d870aaf973de319de3b08072195d001a056630832d"),
    "SELECTOR_PREREG": ("UDT_GR_TO_UDT_SELECTOR_AUDIT_PREREG_2026-07-18.md", "6a835388e8f7a82a4bb4b9496f99c4a5e4181f5e5ccb2637641a1b4346922cc6"),
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(name: str, fields: list[str], rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def require(name: str, condition: bool, checks: dict[str, str]) -> None:
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


def lane_rows() -> list[dict[str, str]]:
    return [
        {
            "lane_id": "L01",
            "lane": "PRE_SCALE_C2_BACH_BULK",
            "owner_authorization": "AUTHORIZED_CONDITIONAL_SPECIFICATION",
            "epistemic_status": "UNIQUE_CONDITIONAL_BULK_CLASS_NOT_COMPLETE_ACTION",
            "parent_object": "pre_scale_CSN_equivalence_class",
            "fields": "metric_only_is_an_added_class_premise; C01-C07_cross_audit_binding",
            "covariance_locality": "local_4D_diffeomorphism_covariance_added_premises",
            "derivative_order": "fourth_order_metric_equation_within_named_class",
            "variation_domain": "unrestricted_metric_variation_before_physical_scale_selection",
            "boundary_status": "OPEN_fourth_order_finite_cell_boundary_and_corner_completion",
            "source_status": "OPEN_native_matter_and_compatible_source",
            "scale_status": "pre_scale_no_physical_representative; normalization_open",
            "operator_readiness": "P05_REQUIRES_SEPARATE_DISPATCH_AND_COMPLETE_FIELD_BOUNDARY_BRANCHING",
            "solve_authority": "NONE",
        },
        {
            "lane_id": "L02",
            "lane": "POST_SCALE_EH_BULK",
            "owner_authorization": "AUTHORIZED_CONDITIONAL_SPECIFICATION",
            "epistemic_status": "CONDITIONAL_BULK_NOT_NATIVE_UDT_ACTION",
            "parent_object": "selected_physical_metric_representative",
            "fields": "metric_only_is_an_added_class_premise; C01-C07_cross_audit_binding",
            "covariance_locality": "local_4D_diffeomorphism_covariance_and_Lovelock_minimality_added_premises",
            "derivative_order": "at_most_second_order_metric_equation_within_named_class",
            "variation_domain": "unrestricted_metric_variation_after_representative_and_scale_selection",
            "boundary_status": "OPEN_finite_cell_boundary_corner_reference_and_normalization",
            "source_status": "OPEN_native_matter_and_source",
            "scale_status": "physical_representative_scale_and_dimensionful_coefficient_required_but_not_derived",
            "operator_readiness": "P05_REQUIRES_SEPARATE_DISPATCH_AND_COMPLETE_FIELD_BOUNDARY_BRANCHING",
            "solve_authority": "NONE",
        },
        {
            "lane_id": "L03",
            "lane": "TWO_STAGE_BRIDGE_OPEN",
            "owner_authorization": "AUTHORIZED_CONDITIONAL_RESEARCH_LANE",
            "epistemic_status": "OPEN_NO_ACTION_OPERATOR_OR_MATCHING_MAP",
            "parent_object": "pre_scale_class_to_post_scale_representative",
            "fields": "field_map_degree_of_freedom_and_matching_content_open; C01-C07_cross_audit_binding",
            "covariance_locality": "OPEN_at_each_stage_and_across_matching",
            "derivative_order": "OPEN_must_reconcile_fourth_and_second_order_or_change_regime_explicitly",
            "variation_domain": "OPEN_pre_scale_post_scale_and_matching_variations_must_be_distinguished",
            "boundary_status": "OPEN_stagewise_and_matching_boundary_completion",
            "source_status": "OPEN_stagewise_native_matter_and_source",
            "scale_status": "OPEN_selection_functional_and_matching_scale_rule",
            "operator_readiness": "NOT_OPERATOR_READY_BRIDGE_DEFINITION_REQUIRED_BEFORE_P05",
            "solve_authority": "NONE",
        },
    ]


def premise_rows() -> list[dict[str, str]]:
    return [
        {"id": "P01", "scope": "ALL", "premise_or_status": "No dynamics is presently derived", "stamp": "OWNER_RULING_AND_CURRENT_LEDGER", "source": "active_owner_ruling_2026-07-21; UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md", "effect": "all lanes remain conditional"},
        {"id": "P02", "scope": "ALL", "premise_or_status": "four-dimensional arena", "stamp": "INHERITED_NOT_DERIVED", "source": "UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md:selector_matrix", "effect": "conditional arena for L01 and L02"},
        {"id": "P03", "scope": "ALL", "premise_or_status": "dynamical field census", "stamp": "OPEN", "source": "udt_complete_metric_solution_space_map_2026-07-21/OFFSHELL_CONFIGURATION_BRANCHES.tsv", "effect": "cross every lane with C01-C07"},
        {"id": "P04", "scope": "ALL", "premise_or_status": "local diffeomorphism covariance", "stamp": "OPEN_FOUNDATION_ADDED_IN_L01_L02", "source": "UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md:selector_matrix", "effect": "cannot be called derived UDT"},
        {"id": "P05", "scope": "ALL", "premise_or_status": "locality", "stamp": "OPEN_FOUNDATION_ADDED_IN_L01_L02", "source": "UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md:selector_matrix", "effect": "nonlocal and global laws not ruled out"},
        {"id": "P06", "scope": "L01", "premise_or_status": "exact local CSN compatibility before scale", "stamp": "ADDED_CLASS_PREMISE", "source": "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv:S11-S13", "effect": "conditional C2 bulk classification"},
        {"id": "P07", "scope": "L01", "premise_or_status": "metric-only polynomial parity-even lowest curvature-square inventory", "stamp": "ADDED_CLASS_PREMISE", "source": "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv:S11", "effect": "conditional uniqueness class only"},
        {"id": "P08", "scope": "L01", "premise_or_status": "unrestricted variation before physical scale selection", "stamp": "ADDED_CLASS_PREMISE", "source": "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv:S13", "effect": "conditional Bach equation at P05 if fully built"},
        {"id": "P09", "scope": "L02", "premise_or_status": "physical representative and scale already selected", "stamp": "OPEN_INPUT_REQUIRED", "source": "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv:S14", "effect": "EH cannot occupy pre-scale role"},
        {"id": "P10", "scope": "L02", "premise_or_status": "metric-only unrestricted local 4D variation with at-most-second-order equations and Lovelock minimality", "stamp": "ADDED_CLASS_PREMISE", "source": "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv:S14", "effect": "conditional EH bulk class"},
        {"id": "P11", "scope": "L03", "premise_or_status": "pre-scale to post-scale selection and matching map", "stamp": "OPEN_NOT_SUPPLIED", "source": "UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md:possible_two_stage_bridge", "effect": "no operator or P05 equation build yet"},
        {"id": "P12", "scope": "L03", "premise_or_status": "dynamical order and degree-of-freedom reconciliation", "stamp": "OPEN_NOT_SUPPLIED", "source": "UDT_GR_TO_UDT_SELECTOR_AUDIT_2026-07-18.md:possible_two_stage_bridge", "effect": "scale selection alone cannot turn Bach into EH"},
        {"id": "P13", "scope": "ALL", "premise_or_status": "finite-cell differentiable boundary and corners", "stamp": "OPEN", "source": "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv:S24", "effect": "no complete action in any lane"},
        {"id": "P14", "scope": "ALL", "premise_or_status": "native matter source carrier charge and mass", "stamp": "OPEN_OR_CONDITIONAL_NOT_ADOPTED", "source": "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv:S15-S28", "effect": "no source imported"},
        {"id": "P15", "scope": "ALL", "premise_or_status": "P03G global assembly axes", "stamp": "FREE_AND_UNSELECTED", "source": "udt_global_kinematic_assembly_p03g_2026-07-21/GLOBAL_ASSEMBLY_DATA_SCHEMA.tsv", "effect": "carry all 12 into later branch builds"},
        {"id": "P16", "scope": "ALL", "premise_or_status": "observational c_E and G_obs", "stamp": "DOWNSTREAM_CALIBRATION_ONLY", "source": "udt_founded_constraint_atlas_p03_2026-07-21/CONSTRAINT_EFFECT_LEDGER.tsv:E23", "effect": "not a pre-scale selector"},
        {"id": "P17", "scope": "ALL", "premise_or_status": "comparison and merit targets", "stamp": "EXCLUDED", "source": "udt_founded_constraint_atlas_p03_2026-07-21/CONSTRAINT_EFFECT_LEDGER.tsv:E24", "effect": "no GR particle cosmology or soliton score"},
        {"id": "P18", "scope": "ALL", "premise_or_status": "solve authority", "stamp": "NONE_IN_P04", "source": "udt_complete_metric_solution_space_map_2026-07-21/FUTURE_ATLAS_PROTOCOL.tsv:P04", "effect": "stop before P05 equations or numerical work"},
    ]


BRANCHES = {
    "C01": "CONFORMAL_METRIC_ONLY",
    "C02": "CONFORMAL_METRIC_PLUS_INDEPENDENT_PHI",
    "C03": "COFRAME_PLUS_RECIPROCAL_CHARACTER",
    "C04": "METRIC_PLUS_SUPPLIED_PROJECTOR",
    "C05": "METRIC_PLUS_MULTIPLIER_OR_HARD_RECIPROCAL_CONSTRAINT",
    "C06": "TWO_STAGE_PRE_POST_SCALE_BRIDGE",
    "C07": "INDEPENDENT_CONNECTION_OR_TORSION",
}


def compatibility_rows() -> list[dict[str, str]]:
    status = {
        "L01": {
            "C01": ("CLASS_COMPATIBLE_CONDITIONAL", "global conformal metric boundary and representative bookkeeping remain"),
            "C02": ("BLOCKED_UNGOVERNED_EXTRA_FIELD", "independent phi has no equation in bare metric-only bulk"),
            "C03": ("CONDITIONAL_REFORMULATION_NOT_AUTO_EQUIVALENT", "coframe variation soldering gauge and torsion assumptions must be explicit"),
            "C04": ("BLOCKED_UNGOVERNED_EXTRA_FIELD", "supplied projector has no equation or variation rule"),
            "C05": ("BLOCKED_VARIATION_DOMAIN_MISMATCH", "multiplier or hard tangent restriction changes the unrestricted metric class"),
            "C06": ("NOT_STANDALONE_COMPLETE", "pre-scale bulk is only one side of the open bridge"),
            "C07": ("BLOCKED_UNGOVERNED_EXTRA_FIELD", "independent connection or torsion has no equation in metric-only bulk"),
        },
        "L02": {
            "C01": ("BLOCKED_POST_SCALE_REPRESENTATIVE_MISSING", "conformal class alone does not supply physical representative and scale"),
            "C02": ("BLOCKED_UNGOVERNED_EXTRA_FIELD", "independent phi has no equation in bare metric-only bulk"),
            "C03": ("CONDITIONAL_REFORMULATION_NOT_AUTO_EQUIVALENT", "coframe variation soldering gauge and torsion assumptions must be explicit"),
            "C04": ("BLOCKED_UNGOVERNED_EXTRA_FIELD", "supplied projector has no equation or variation rule"),
            "C05": ("BLOCKED_VARIATION_DOMAIN_MISMATCH", "constraint implementation changes unrestricted metric variation"),
            "C06": ("NOT_STANDALONE_COMPLETE", "post-scale bulk requires the open bridge input"),
            "C07": ("BLOCKED_UNGOVERNED_EXTRA_FIELD", "Palatini or torsion dynamics would be a different premise class"),
        },
        "L03": {
            "C01": ("BRIDGE_MUST_MAP", "map from pre-scale class to physical representative absent"),
            "C02": ("BRIDGE_MUST_GOVERN_OR_REMOVE_FIELD", "independent phi transition and equation absent"),
            "C03": ("BRIDGE_MUST_MAP", "complete coframe soldering and stagewise transport absent"),
            "C04": ("BRIDGE_MUST_GOVERN_OR_REMOVE_FIELD", "projector emergence transport and variation absent"),
            "C05": ("BRIDGE_MUST_DEFINE_VARIATION", "constraint placement before during or after scale selection absent"),
            "C06": ("NATIVE_BRANCH_MATCH_BUT_OPERATOR_OPEN", "branch name matches but no selection or matching functional exists"),
            "C07": ("BRIDGE_MUST_GOVERN_OR_REMOVE_FIELD", "connection torsion matching and equations absent"),
        },
    }
    rows = []
    for lane in ("L01", "L02", "L03"):
        for branch in ("C01", "C02", "C03", "C04", "C05", "C06", "C07"):
            ruling, gap = status[lane][branch]
            rows.append({"pair_id": f"{lane}_{branch}", "lane_id": lane, "realization_id": branch, "realization": BRANCHES[branch], "compatibility_status": ruling, "unresolved_requirement": gap, "field_removed": "NO", "globally_realized": "UNEVALUATED"})
    return rows


def p05_rows() -> list[dict[str, str]]:
    return [
        {"lane_id": "L01", "authorization": "P04_CONDITIONAL_LANE_AUTHORIZED", "entry_status": "SEPARATE_P05_DISPATCH_REQUIRED", "must_predeclare": "field_realization_subbranches; complete varied fields; unrestricted_vs_constrained_variation; fourth_order_boundary_corner_variables; normalization; all_P03G_axes", "stop_if_missing": "any_field_equation_normal_metric_equation_boundary_channel_or_global_branch", "maximum_next_conclusion": "NAMED_DYNAMICS_OPERATOR_COMPLETE_IN_EXACT_PREMISE_CLASS"},
        {"lane_id": "L02", "authorization": "P04_CONDITIONAL_LANE_AUTHORIZED", "entry_status": "SEPARATE_P05_DISPATCH_REQUIRED", "must_predeclare": "physical_representative_input; field_realization_subbranches; complete varied_fields; finite_cell_boundary_corner_reference; coefficients; all_P03G_axes", "stop_if_missing": "representative_any_field_equation_boundary_channel_or_global_branch", "maximum_next_conclusion": "NAMED_DYNAMICS_OPERATOR_COMPLETE_IN_EXACT_PREMISE_CLASS"},
        {"lane_id": "L03", "authorization": "P04_CONDITIONAL_RESEARCH_LANE_AUTHORIZED", "entry_status": "NOT_OPERATOR_READY", "must_predeclare": "selection_functional; stage_fields; matching_map; degree_of_freedom_and_order_reconciliation; stagewise_variations; boundaries; all_P03G_axes", "stop_if_missing": "bridge_definition_or_any_matching_equation", "maximum_next_conclusion": "BRIDGE_OPERATOR_DEFINED_OR_EXPLICITLY_OPEN"},
    ]


def stop_rows() -> list[dict[str, str]]:
    return [
        {"id": "S01", "object": "controlling_dynamics_status", "status": "NO_DYNAMICS_DERIVED", "limit": "owner authorization creates conditional research lanes only"},
        {"id": "S02", "object": "L01_pre_scale_C2_Bach", "status": "AUTHORIZED_UNIQUE_CONDITIONAL_BULK_CLASS", "limit": "not complete action or UDT selection"},
        {"id": "S03", "object": "L02_post_scale_EH", "status": "AUTHORIZED_CONDITIONAL_BULK_CLASS", "limit": "representative scale and minimality premises required"},
        {"id": "S04", "object": "L03_two_stage_bridge", "status": "AUTHORIZED_OPEN_RESEARCH_LANE", "limit": "no action operator selection functional or matching map"},
        {"id": "S05", "object": "field_realization_pairs", "status": "21_OF_21_ACCOUNTED_NONE_REMOVED", "limit": "compatibility is not global existence"},
        {"id": "S06", "object": "global_assembly_axes", "status": "12_OF_12_FREE_AND_UNSELECTED", "limit": "P03G carryforward"},
        {"id": "S07", "object": "boundary_completion", "status": "OPEN_ALL_LANES", "limit": "no habitual GHY C2 or asymptotic completion imported"},
        {"id": "S08", "object": "native_matter_source_carrier_charge_mass", "status": "OPEN_OR_CONDITIONAL_NOT_ADOPTED", "limit": "no source term enters P04"},
        {"id": "S09", "object": "comparison_merit", "status": "EXCLUDED", "limit": "no GR particle soliton cosmology or empirical score"},
        {"id": "S10", "object": "P05_equations", "status": "NOT_LAUNCHED", "limit": "separate dispatch required"},
        {"id": "S11", "object": "ODE_PDE_GPU", "status": "NOT_AUTHORIZED", "limit": "P06 onward remains closed"},
        {"id": "S12", "object": "canonization", "status": "NOT_AUTHORIZED", "limit": "Charles alone canonizes"},
        {"id": "S13", "object": "maximum_conclusion", "status": MAXIMUM, "limit": "authorization and premise manifest only"},
    ]


def main() -> None:
    checks: dict[str, str] = {}
    for name, (relative, expected) in SOURCES.items():
        require(f"source_{name}", digest(ROOT / relative) == expected, checks)

    lanes = lane_rows()
    premises = premise_rows()
    compat = compatibility_rows()
    p03g_axes = read_tsv(ROOT / "udt_global_kinematic_assembly_p03g_2026-07-21/GLOBAL_ASSEMBLY_DATA_SCHEMA.tsv")
    carry = [{"axis_id": row["axis_id"], "object": row["object"], "p03g_status": row["status"], "p04_disposition": "FREE_AND_UNSELECTED_IN_ALL_THREE_LANES", "selection_or_value": "NONE", "source": "udt_global_kinematic_assembly_p03g_2026-07-21/GLOBAL_ASSEMBLY_DATA_SCHEMA.tsv"} for row in p03g_axes]
    gates = p05_rows()
    stops = stop_rows()

    write_tsv("DYNAMICS_BRANCH_DISPATCH.tsv", list(lanes[0]), lanes)
    write_tsv("LAW_PREMISE_MANIFEST.tsv", list(premises[0]), premises)
    write_tsv("FIELD_REALIZATION_COMPATIBILITY.tsv", list(compat[0]), compat)
    write_tsv("GLOBAL_AXIS_CARRYFORWARD.tsv", list(carry[0]), carry)
    write_tsv("P05_ENTRY_GATES.tsv", list(gates[0]), gates)
    write_tsv("AUTHORITY_AND_STOP_LEDGER.tsv", list(stops[0]), stops)

    require("three_lanes", {row["lane_id"] for row in lanes} == {"L01", "L02", "L03"}, checks)
    require("no_derived_lane", all("DERIVED" not in row["epistemic_status"] and row["solve_authority"] == "NONE" for row in lanes), checks)
    require("bridge_not_operator_ready", next(row for row in lanes if row["lane_id"] == "L03")["operator_readiness"].startswith("NOT_OPERATOR_READY"), checks)
    require("all_21_pairs", len(compat) == 21 and len({row["pair_id"] for row in compat}) == 21, checks)
    require("all_fields_retained", all(row["field_removed"] == "NO" for row in compat), checks)
    require("no_global_realization_claim", all(row["globally_realized"] == "UNEVALUATED" for row in compat), checks)
    require("all_12_global_axes", len(carry) == 12 and {row["axis_id"] for row in carry} == {f"A{i:02d}" for i in range(1, 13)}, checks)
    require("all_axes_free", all(row["p04_disposition"] == "FREE_AND_UNSELECTED_IN_ALL_THREE_LANES" and row["selection_or_value"] == "NONE" for row in carry), checks)
    require("P05_separate", all(row["entry_status"] in {"SEPARATE_P05_DISPATCH_REQUIRED", "NOT_OPERATOR_READY"} for row in gates), checks)
    require("no_equation_or_solve_authority", next(row for row in stops if row["id"] == "S10")["status"] == "NOT_LAUNCHED" and next(row for row in stops if row["id"] == "S11")["status"] == "NOT_AUTHORIZED", checks)
    require("premise_coverage", len(premises) == 18 and {row["id"] for row in premises} == {f"P{i:02d}" for i in range(1, 19)}, checks)
    require("boundary_open", all("OPEN" in row["boundary_status"] for row in lanes), checks)
    require("source_open", all("OPEN" in row["source_status"] for row in lanes), checks)

    source_rows = [{"id": f"SRC{i:02d}", "role": role, "path": relative, "sha256": expected, "use": "immutable P04 authority input"} for i, (role, (relative, expected)) in enumerate(SOURCES.items(), 1)]
    write_tsv("SOURCE_LINEAGE.tsv", list(source_rows[0]), source_rows)

    tables = ["DYNAMICS_BRANCH_DISPATCH.tsv", "LAW_PREMISE_MANIFEST.tsv", "FIELD_REALIZATION_COMPATIBILITY.tsv", "GLOBAL_AXIS_CARRYFORWARD.tsv", "P05_ENTRY_GATES.tsv", "AUTHORITY_AND_STOP_LEDGER.tsv", "SOURCE_LINEAGE.tsv"]
    result = {
        "schema": "udt-p04-dynamics-branch-ruling-1.0",
        "status": "PASS",
        "evidence_grade": "OWNER_AUTHORIZED_CONDITIONAL_DISPATCH_VERIFIED",
        "maximum_conclusion": MAXIMUM,
        "controlling_scientific_status": "NO_DYNAMICS_DERIVED",
        "counts": {"authorized_lanes": 3, "derived_lanes": 0, "field_realization_pairs": 21, "field_realizations_removed": 0, "global_axes_carried_free": 12, "solve_authorizations": 0, "premise_rows": 18},
        "lane_rulings": {row["lane_id"]: row["epistemic_status"] for row in lanes},
        "source_sha256": {role: expected for role, (_, expected) in SOURCES.items()},
        "table_sha256": {name: digest(HERE / name) for name in tables},
        "check_count": len(checks),
        "checks": checks,
        "scope": {"CPU_only": True, "GPU_used": False, "symbolic_variation_performed": False, "equations_built": False, "ODE_or_PDE_run": False, "comparison_loaded": False, "P05_launched": False, "canon_changed": False},
    }
    (HERE / "RULING_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    transcript = [
        "P04_DYNAMICS_BRANCH_RULING=PASS",
        f"checks={len(checks)}",
        "controlling_status=NO_DYNAMICS_DERIVED",
        "conditional_lanes=3",
        "derived_lanes=0",
        "field_realization_pairs=21/21",
        "global_axes_carried_free=12/12",
        "solve_authorizations=0",
        "P05=NOT_LAUNCHED",
        f"maximum_conclusion={MAXIMUM}",
    ]
    text = "\n".join(transcript) + "\n"
    (HERE / "RULING_TRANSCRIPT.txt").write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
