#!/usr/bin/env python3
"""Fail-closed, standard-library verifier for the complete-metric map package."""

from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent

TABLE_SPECS = {
    "SOURCE_LINEAGE.tsv": (28, "S", 1),
    "COMPLETE_METRIC_DOF_LEDGER.tsv": (24, None, None),
    "REDUNDANCY_AND_REALIZATION_LEDGER.tsv": (10, "G", 1),
    "OFFSHELL_CONFIGURATION_BRANCHES.tsv": (7, "C", 1),
    "GEOMETRIC_COUPLING_MAP.tsv": (12, "K", 1),
    "PREMISE_AND_REDUCTION_LEDGER.tsv": (36, "P", 1),
    "FUTURE_ATLAS_PROTOCOL.tsv": (14, "P", 0),
    "ALGEBRA_ODE_TIME_DESIGN.tsv": (16, None, None),
    "BRANCH_RECORD_SCHEMA.tsv": (34, "B", 1),
    "BRANCH_OUTCOME_VOCABULARY.tsv": (16, "V", 1),
    "TEN_CRITERION_COMPLETENESS.tsv": (10, "Q", 1),
    "ANTI_MYOPIA_AUDIT.tsv": (24, "X", 1),
    "COMPUTE_AND_STOP_CONTRACT.tsv": (14, "P", 0),
    "REGRADING_AND_ROLLBACK_RULES.tsv": (12, "R", 1),
}

ID_FIELDS = {
    "SOURCE_LINEAGE.tsv": "id",
    "COMPLETE_METRIC_DOF_LEDGER.tsv": "id",
    "REDUNDANCY_AND_REALIZATION_LEDGER.tsv": "id",
    "OFFSHELL_CONFIGURATION_BRANCHES.tsv": "branch_id",
    "GEOMETRIC_COUPLING_MAP.tsv": "id",
    "PREMISE_AND_REDUCTION_LEDGER.tsv": "id",
    "FUTURE_ATLAS_PROTOCOL.tsv": "stage_id",
    "ALGEBRA_ODE_TIME_DESIGN.tsv": "design_id",
    "BRANCH_RECORD_SCHEMA.tsv": "field_id",
    "BRANCH_OUTCOME_VOCABULARY.tsv": "outcome_id",
    "TEN_CRITERION_COMPLETENESS.tsv": "criterion_id",
    "ANTI_MYOPIA_AUDIT.tsv": "audit_id",
    "COMPUTE_AND_STOP_CONTRACT.tsv": "stage_id",
    "REGRADING_AND_ROLLBACK_RULES.tsv": "rule_id",
}

ALLOWED_PREMISE_STAMPS = {
    "free-and-explored",
    "pinned-by-THEORY",
    "pinned-by-OWNER_CLARIFICATION",
    "CONDITIONAL_BRANCH",
    "COMPARISON_READOUT_ONLY",
    "pinned-by-HABIT / BLOCKED",
}

REQUIRED_OUTCOMES = {
    "TRIVIAL",
    "REGULAR",
    "SINGULAR",
    "DEGENERATE",
    "HORIZON_OR_CAUSAL_BOUNDARY",
    "TYPE_CHANGE",
    "OSCILLATORY",
    "DIVERGENT_BRANCH",
    "DISCONNECTED",
    "BIFURCATION_OR_FOLD",
    "BOUNDARY_CONTROLLED",
    "GAUGE_OR_REPRESENTATIVE_ORBIT",
    "UNRESOLVED_NUMERICAL",
    "SOLVER_FAILURE_OR_BUG_SUSPECT",
    "TIMEOUT_OR_RESOURCE_BOUND",
    "NO_GLOBAL_COMPLETION_FOUND_WITHIN_BOUNDS",
}

REQUIRED_SCHEMA_FIELDS = {
    "record_id",
    "atlas_stage",
    "offshell_branch_id",
    "dynamics_law_id",
    "representation_and_split",
    "live_fields_and_slots",
    "frozen_or_omitted_fields",
    "dependence_set",
    "symmetry_stratum",
    "boundary_and_corner_class",
    "raw_equation_residual",
    "constraint_and_boundary_residuals",
    "backward_error_and_conditioning",
    "outcome_labels",
    "solver_disposition",
    "premise_row_ids",
    "raw_artifact_paths_and_hashes",
    "comparison_state",
    "interpretation_status",
    "unresolved_scope",
}

SOURCE_NEEDLES = {
    "UDT_COMMON_SCALE_NEUTRALITY_POSTULATE_2026-07-15.md": "derivative order and time-live degrees of freedom",
    "UDT_GLOBAL_BOOTSTRAP_PRINCIPLE_2026-07-15.md": "No nonlocal insertion",
    "UDT_NATIVE_ACTION_COLD_PACKET.md": "staticity, spherical symmetry, diagonality",
    "metric_cartan_holonomy_audit_2026-07-19/AUDIT_REPORT.md": "No current UDT premise sets `A^A_i=0`",
    "rung2_weld_postjuly_regrade_2026-07-19/AUDIT_REPORT.md": "A geometric coupling is not a law setting the component to zero.",
    "udt_premise_reset_audit_2026-07-19/AUDIT_REPORT.md": "`phi(p)` is a signed dilation field belonging to a location.",
    "c2_transverse_coframe_closure_2026-07-20/AUDIT_REPORT.md": "restricted shear equation",
    "native_action_final_adjudication_2026-07-18/FINAL_STATUS_LEDGER.tsv": "UNIQUE-CONDITIONAL",
}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def load_model() -> dict[str, Any]:
    tables = {name: read_tsv(PACKAGE / name) for name in TABLE_SPECS}
    graph = json.loads((PACKAGE / "LAYER_AND_STAGE_GRAPH.json").read_text(encoding="utf-8"))
    return {"tables": tables, "graph": graph}


def expected_ids(prefix: str, start: int, count: int) -> list[str]:
    return [f"{prefix}{number:02d}" for number in range(start, start + count)]


def validate(model: dict[str, Any], check_disk_sources: bool = True) -> set[str]:
    errors: set[str] = set()
    tables = model["tables"]
    graph = model["graph"]

    for name, (count, prefix, start) in TABLE_SPECS.items():
        rows = tables.get(name, [])
        if len(rows) != count:
            errors.add(f"COUNT:{name}")
        field = ID_FIELDS[name]
        ids = [row.get(field, "") for row in rows]
        if len(ids) != len(set(ids)) or any(not value for value in ids):
            errors.add(f"ID_UNIQUE:{name}")
        if prefix is not None and start is not None and ids != expected_ids(prefix, start, count):
            errors.add(f"ID_SEQUENCE:{name}")

    sources = tables["SOURCE_LINEAGE.tsv"]
    if check_disk_sources:
        for row in sources:
            if not (ROOT / row["path"]).exists():
                errors.add("SOURCE_PATH_MISSING")
        for path, needle in SOURCE_NEEDLES.items():
            source_path = ROOT / path
            if not source_path.exists() or needle not in source_path.read_text(encoding="utf-8"):
                errors.add(f"SOURCE_SEMANTIC_NEEDLE:{path}")
    for row in sources:
        if row["authority_class"] == "PRE_JULY_HISTORICAL" and not any(
            token in row["permitted_use"] for token in ("FAILURE", "CANDIDATE", "TOOLING")
        ):
            errors.add("SOURCE_FIREWALL")
        if row["id"] == "S28" and row["permitted_use"] != "AUDIT_CONTROL":
            errors.add("GENERATED_FEEDBACK")

    dofs = tables["COMPLETE_METRIC_DOF_LEDGER.tsv"]
    metric = [row for row in dofs if row["id"].startswith("M")]
    if [row["id"] for row in metric] != expected_ids("M", 1, 10):
        errors.add("METRIC_SECTOR_SET")
    try:
        slot_sum = sum(int(row["metric_slot_count"]) for row in metric)
    except (TypeError, ValueError):
        slot_sum = -1
    if slot_sum != 10 or any(row["metric_slot_count"] != "1" for row in metric):
        errors.add("METRIC_SLOT_COUNT")
    if any(row["layer"] != "CONDITIONAL_2_PLUS_2_METRIC" for row in metric):
        errors.add("SPLIT_CONDITIONALITY")
    if any(row["dependence"] != "x0 x1 y2 y3" for row in metric):
        errors.add("ALL_COORDINATE_DEPENDENCE")
    if not any(row["id"] == "O01" and row["layer"] == "ABSTRACT_WHOLE_FRAME" for row in dofs):
        errors.add("ABSTRACT_PARENT_MISSING")

    redundancies = {row["id"]: row for row in tables["REDUNDANCY_AND_REALIZATION_LEDGER.tsv"]}
    if redundancies.get("G06", {}).get("status") != "CONDITIONAL_REALIZATION":
        errors.add("SPLIT_CONDITIONALITY")
    if "identified with distance" not in redundancies.get("G05", {}).get("failure_if_confused", ""):
        errors.add("PHI_DISTANCE_GUARD")

    branches = tables["OFFSHELL_CONFIGURATION_BRANCHES.tsv"]
    if {row["current_status"] for row in branches} & {"NATIVE", "DERIVED", "DEFAULT"}:
        errors.add("OFFSHELL_PROMOTION")
    if {row["branch_id"] for row in branches} != set(expected_ids("C", 1, 7)):
        errors.add("OFFSHELL_BRANCH_SET")

    premises = tables["PREMISE_AND_REDUCTION_LEDGER.tsv"]
    if any(row["premise_stamp"] not in ALLOWED_PREMISE_STAMPS for row in premises):
        errors.add("PREMISE_STAMP")
    premise_by_id = {row["id"]: row for row in premises}
    if any(premise_by_id.get(pid, {}).get("premise_stamp") != "pinned-by-HABIT / BLOCKED" for pid in ("P27", "P28", "P33")):
        errors.add("HABIT_PINS")
    if premise_by_id.get("P19", {}).get("premise_stamp") != "CONDITIONAL_BRANCH":
        errors.add("CONDITIONAL_ACTION")
    if premise_by_id.get("P20", {}).get("premise_stamp") != "COMPARISON_READOUT_ONLY":
        errors.add("GR_SELECTION_FIREWALL")

    protocol = tables["FUTURE_ATLAS_PROTOCOL.tsv"]
    stage_ids = [row["stage_id"] for row in protocol]
    if stage_ids != expected_ids("P", 0, 14):
        errors.add("STAGE_SEQUENCE")
    if protocol and protocol[0]["maximum_conclusion"] != "EXECUTION_PLAN_READY_FOR_OWNER_REVIEW":
        errors.add("MAP_MAXIMUM")
    if "full" not in next(((row["work_design"] + " " + row["required_outputs"]).lower() for row in protocol if row["stage_id"] == "P05"), ""):
        errors.add("FULL_VARIATION_BEFORE_REDUCTION")
    if "p06" not in next((row["entry_gate"].lower() for row in protocol if row["stage_id"] == "P07"), ""):
        errors.add("FULL_VARIATION_BEFORE_REDUCTION")
    if "immutable" not in next((row["entry_gate"].lower() for row in protocol if row["stage_id"] == "P13"), ""):
        errors.add("COMPARISON_AFTER_FREEZE")

    compute = tables["COMPUTE_AND_STOP_CONTRACT.tsv"]
    if [row["stage_id"] for row in compute] != stage_ids:
        errors.add("COMPUTE_STAGE_ALIGNMENT")
    if "no equation solve" not in compute[0]["processor_and_bound"].lower():
        errors.add("MAP_NO_SOLVE")

    designs = {row["design_id"]: row for row in tables["ALGEBRA_ODE_TIME_DESIGN.tsv"]}
    if "Complete metric" not in designs.get("O01", {}).get("cannot_conclude", ""):
        errors.add("ODE_WHOLE_GUARD")
    if "Physical history" not in designs.get("T01", {}).get("cannot_conclude", ""):
        errors.add("TIME_LIVE_GUARD")
    if "full three plus one" not in designs.get("T03", {}).get("object", "").replace("_", " "):
        errors.add("FULL_PDE_STRATUM")

    labels = {row["label"] for row in tables["BRANCH_OUTCOME_VOCABULARY.tsv"]}
    if labels != REQUIRED_OUTCOMES:
        errors.add("OUTCOME_SET")
    if any(not row["retention_rule"].lower().startswith(("retain", "always retain")) for row in tables["BRANCH_OUTCOME_VOCABULARY.tsv"]):
        errors.add("OUTCOME_RETENTION")

    schema_rows = tables["BRANCH_RECORD_SCHEMA.tsv"]
    schema_fields = {row["field_name"] for row in schema_rows}
    if not REQUIRED_SCHEMA_FIELDS <= schema_fields or any(row["required"] != "YES" for row in schema_rows):
        errors.add("RESULT_SCHEMA")

    criteria = tables["TEN_CRITERION_COMPLETENESS.tsv"]
    expected_criteria = {
        "FIELDS", "ACTION_TERMS", "FULL_EQUATIONS", "DOMAIN_COORDINATES", "BOUNDARY_REGULARITY",
        "TOPOLOGICAL_SECTOR", "DYNAMICAL_CHARACTER", "BRANCH_BIFURCATION", "STABILITY_SPECTRUM", "REGIME_VALIDITY",
    }
    if {row["criterion"] for row in criteria} != expected_criteria:
        errors.add("COMPLETENESS_CRITERIA")
    if any(not row["currently_dropped_or_open"].strip() or "COMPLETE" in row["current_map_coverage"].upper() for row in criteria):
        errors.add("COMPLETENESS_OPEN")

    anti = tables["ANTI_MYOPIA_AUDIT.tsv"]
    if any(row["audit_status"] not in {"PASS", "OPEN_BLOCKER_VISIBLE"} for row in anti):
        errors.add("ANTI_MYOPIA_STATUS")
    if not any(row["audit_status"] == "OPEN_BLOCKER_VISIBLE" for row in anti):
        errors.add("OPEN_BLOCKERS_HIDDEN")

    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    node_ids = [node.get("id", "") for node in nodes]
    if len(nodes) != 18 or len(set(node_ids)) != 18:
        errors.add("GRAPH_NODE_SET")
    if len(edges) != 22:
        errors.add("GRAPH_EDGE_COUNT")
    if graph.get("current_executed_stage") != "P00_MAP_ONLY":
        errors.add("MAP_NO_SOLVE")
    node_map = {node["id"]: node for node in nodes if "id" in node}
    if node_map.get("D00_NATIVE_DYNAMICS", {}).get("status") != "OPEN_NOT_SELECTED":
        errors.add("NATIVE_DYNAMICS_OPEN")
    if node_map.get("D01_C2_BACH", {}).get("status") != "UNIQUE_CONDITIONAL_BULK_BRANCH":
        errors.add("CONDITIONAL_ACTION")
    if node_map.get("D02_EH_POST_SCALE", {}).get("status") != "CONDITIONAL_BRANCH":
        errors.add("CONDITIONAL_ACTION")
    edge_pairs = {(edge.get("from"), edge.get("to")) for edge in edges}
    for readout in ("R00_GR_READOUT", "R01_EMPIRICAL_READOUT", "R02_CARRIER_TOPOLOGY_READOUT"):
        incoming = [edge for edge in edges if edge.get("to") == readout]
        if len(incoming) != 1 or incoming[0].get("from") != "F00_FROZEN_ATLAS":
            errors.add("READOUT_FIREWALL")
    if ("S00_ALGEBRAIC_EOM_BRANCHES", "S01_ODE_STRATA") not in edge_pairs:
        errors.add("ODE_AFTER_FULL_EOM")
    if ("S00_ALGEBRAIC_EOM_BRANCHES", "S02_TIME_LIVE_PDE") not in edge_pairs:
        errors.add("PDE_AFTER_FULL_EOM")

    # DAG proof.
    indegree = {node_id: 0 for node_id in node_ids}
    outgoing = {node_id: [] for node_id in node_ids}
    for edge in edges:
        source, target = edge.get("from"), edge.get("to")
        if source not in indegree or target not in indegree:
            errors.add("GRAPH_DANGLING_EDGE")
            continue
        outgoing[source].append(target)
        indegree[target] += 1
    queue = [node_id for node_id, degree in indegree.items() if degree == 0]
    visited = 0
    while queue:
        node_id = queue.pop()
        visited += 1
        for target in outgoing[node_id]:
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)
    if visited != len(node_ids):
        errors.add("GRAPH_CYCLE")

    return errors


def exercise_catches(base: dict[str, Any]) -> list[dict[str, str]]:
    cases = []

    def run(name: str, expected: str, mutate) -> None:
        model = copy.deepcopy(base)
        mutate(model)
        found = validate(model, check_disk_sources=False)
        cases.append({"catch": name, "expected_error": expected, "status": "PASS" if expected in found else "FAIL"})

    run("missing_metric_sector", "METRIC_SECTOR_SET", lambda m: m["tables"]["COMPLETE_METRIC_DOF_LEDGER.tsv"].pop(9))
    run("duplicated_degree_of_freedom", "ID_UNIQUE:COMPLETE_METRIC_DOF_LEDGER.tsv", lambda m: m["tables"]["COMPLETE_METRIC_DOF_LEDGER.tsv"].append(copy.deepcopy(m["tables"]["COMPLETE_METRIC_DOF_LEDGER.tsv"][0])))
    run("wrong_metric_slot_total", "METRIC_SLOT_COUNT", lambda m: m["tables"]["COMPLETE_METRIC_DOF_LEDGER.tsv"][0].update(metric_slot_count="2"))
    run("unconditional_2_plus_2", "SPLIT_CONDITIONALITY", lambda m: m["tables"]["COMPLETE_METRIC_DOF_LEDGER.tsv"][0].update(layer="AUTHORITATIVE_COMPLETE_METRIC"))
    run("offshell_branch_promoted", "OFFSHELL_PROMOTION", lambda m: m["tables"]["OFFSHELL_CONFIGURATION_BRANCHES.tsv"][0].update(current_status="NATIVE"))
    run("habit_pin_authorized", "HABIT_PINS", lambda m: m["tables"]["PREMISE_AND_REDUCTION_LEDGER.tsv"][26].update(premise_stamp="free-and-explored"))
    run("conditional_action_called_native", "CONDITIONAL_ACTION", lambda m: next(node for node in m["graph"]["nodes"] if node["id"] == "D01_C2_BACH").update(status="NATIVE"))
    run("ode_presented_as_whole", "ODE_WHOLE_GUARD", lambda m: m["tables"]["ALGEBRA_ODE_TIME_DESIGN.tsv"][7].update(cannot_conclude="Nothing omitted."))
    run("configuration_time_called_evolution", "TIME_LIVE_GUARD", lambda m: m["tables"]["ALGEBRA_ODE_TIME_DESIGN.tsv"][12].update(cannot_conclude="Only stability."))
    run("readout_before_freeze", "READOUT_FIREWALL", lambda m: next(edge for edge in m["graph"]["edges"] if edge["to"] == "R00_GR_READOUT").update(**{"from": "L05_CONSTRAINED_CONFIGURATION_ATLAS"}))
    run("singular_outcome_dropped", "OUTCOME_SET", lambda m: m["tables"]["BRANCH_OUTCOME_VOCABULARY.tsv"].pop(2))
    run("unresolved_outcome_dropped", "OUTCOME_SET", lambda m: m["tables"]["BRANCH_OUTCOME_VOCABULARY.tsv"].pop(12))
    run("completeness_gap_hidden", "COMPLETENESS_OPEN", lambda m: m["tables"]["TEN_CRITERION_COMPLETENESS.tsv"][0].update(currently_dropped_or_open=""))
    run("pre_july_affirmative_use", "SOURCE_FIREWALL", lambda m: m["tables"]["SOURCE_LINEAGE.tsv"][24].update(permitted_use="AFFIRMATIVE_UDT_PHYSICS"))
    run("generated_evidence_feedback", "GENERATED_FEEDBACK", lambda m: m["tables"]["SOURCE_LINEAGE.tsv"][27].update(permitted_use="AFFIRMATIVE_SELECTOR"))
    run("stage_removed", "STAGE_SEQUENCE", lambda m: m["tables"]["FUTURE_ATLAS_PROTOCOL.tsv"].pop(8))
    run("reduced_before_full_variation", "FULL_VARIATION_BEFORE_REDUCTION", lambda m: next(row for row in m["tables"]["FUTURE_ATLAS_PROTOCOL.tsv"] if row["stage_id"] == "P07").update(entry_gate="Symmetry chosen", work_design="Vary the reduced ansatz."))
    run("gr_metric_selector", "GR_SELECTION_FIREWALL", lambda m: m["tables"]["PREMISE_AND_REDUCTION_LEDGER.tsv"][19].update(premise_stamp="pinned-by-THEORY"))
    return cases


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--transcript", type=Path)
    args = parser.parse_args()

    model = load_model()
    errors = sorted(validate(model))
    catches = exercise_catches(model)
    catch_failures = [case["catch"] for case in catches if case["status"] != "PASS"]
    result = {
        "schema": "udt-complete-metric-map-verification-1.0",
        "status": "PASS" if not errors and not catch_failures else "FAIL",
        "maximum_conclusion": "EXECUTION_PLAN_READY_FOR_OWNER_REVIEW",
        "scientific_solve_executed": False,
        "counts": {
            "source_rows": len(model["tables"]["SOURCE_LINEAGE.tsv"]),
            "dof_rows": len(model["tables"]["COMPLETE_METRIC_DOF_LEDGER.tsv"]),
            "metric_slots": sum(int(row["metric_slot_count"]) for row in model["tables"]["COMPLETE_METRIC_DOF_LEDGER.tsv"] if row["id"].startswith("M")),
            "premise_rows": len(model["tables"]["PREMISE_AND_REDUCTION_LEDGER.tsv"]),
            "stages": len(model["tables"]["FUTURE_ATLAS_PROTOCOL.tsv"]),
            "graph_nodes": len(model["graph"]["nodes"]),
            "graph_edges": len(model["graph"]["edges"]),
            "result_schema_fields": len(model["tables"]["BRANCH_RECORD_SCHEMA.tsv"]),
            "outcome_classes": len(model["tables"]["BRANCH_OUTCOME_VOCABULARY.tsv"]),
            "completeness_criteria": len(model["tables"]["TEN_CRITERION_COMPLETENESS.tsv"]),
            "anti_myopia_checks": len(model["tables"]["ANTI_MYOPIA_AUDIT.tsv"]),
            "catch_proofs": len(catches),
        },
        "input_sha256": {name: sha256(PACKAGE / name) for name in sorted(TABLE_SPECS)} | {
            "LAYER_AND_STAGE_GRAPH.json": sha256(PACKAGE / "LAYER_AND_STAGE_GRAPH.json"),
            "PREREGISTRATION.md": sha256(PACKAGE / "PREREGISTRATION.md"),
        },
        "errors": errors,
        "catch_proofs": catches,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    if args.transcript:
        args.transcript.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
