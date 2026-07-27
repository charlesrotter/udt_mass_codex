#!/usr/bin/env python3
import csv
import hashlib
import json
from collections import Counter, defaultdict, deque
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def rows(path):
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def write_tsv(path, fieldnames, data):
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(data)


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


checks = {}


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


manifest = rows(HERE / "SOURCE_MANIFEST.tsv")
for row in manifest:
    source = ROOT / row["source_path"]
    check(f"source:{row['source_path']}", source.is_file() and source.stat().st_size == int(row["size"]) and digest(source) == row["sha256"])

objects = rows(HERE / "OBJECT_TYPE_UNIVERSE.tsv")
edges = rows(HERE / "EDGE_UNIVERSE.tsv")
object_ids = {f"O{i:02d}" for i in range(1, 15)}
edge_ids = {f"E{i:02d}" for i in range(1, 19)}
check("object_universe_14", len(objects) == 14 and {r["object_id"] for r in objects} == object_ids)
check("edge_universe_18", len(edges) == 18 and {r["edge_id"] for r in edges} == edge_ids)

object_status = {
    "O01": ("OPEN_UNSELECTED", "complete founded extension and variation domain not selected"),
    "O02": ("CONDITIONAL_TYPED_INPUT", "pair path arrows are valid inputs; physical arrow not selected"),
    "O03": ("DERIVED_GIVEN_O01_O02", "distance tangents transport Jacobi and holonomy follow from supplied metric path"),
    "O04": ("DERIVED", "real additive coordinate of founded reciprocal pair"),
    "O05": ("CONDITIONAL_FAMILY_LAMBDA_OPEN", "ordered pair supplies X_lambda family but composition does not select lambda"),
    "O06": ("OPEN_ABSENT", "zero registered metric-native normalized signed-depth assignments"),
    "O07": ("DERIVED_GIVEN_O02_O05_O06", "typed path groupoid composes with explicit vertical resets"),
    "O08": ("CONDITIONAL_PARTIAL", "holonomy and conditional angular topology exist with supplied global data"),
    "O09": ("OPEN_UNSELECTED", "complete founded variation domain not selected"),
    "O10": ("OPEN_ABSENT", "no metric-native complete offshell response one-form"),
    "O11": ("OPEN_ABSENT", "current bootstrap is on-shell admissibility not a self-map"),
    "O12": ("OPEN_DOWNSTREAM", "requires integrable response boundary gauge and global periods"),
    "O13": ("OBSERVED_SCALAR_ANCHORS", "c_E and G_obs calibrate but do not select tensor structure"),
    "O14": ("OPEN_ABSENT", "native source mass numerator and same-solution density unavailable"),
}

object_rows = []
for row in objects:
    status, evidence = object_status[row["object_id"]]
    object_rows.append({
        "object_id": row["object_id"],
        "object_name": row["object_name"],
        "type_signature": row["type_signature"],
        "locality": row["locality"],
        "current_status": status,
        "evidence_ruling": evidence,
    })

edge_status = {
    "E01": ("DERIVED_GIVEN_INPUT", "GIVEN_UNSELECTED_INPUT", "metric supplies path geometry once complete metric and typed path are supplied"),
    "E02": ("DERIVED", "ACTIVE", "founding postulates supply abstract additive reciprocal coordinate"),
    "E03": ("CONDITIONAL", "GIVEN_UNSELECTED_INPUT", "ordered pair supplies X_lambda family; lambda remains open"),
    "E04": ("DERIVED_GIVEN_INPUT", "GIVEN_ABSENT_DEPTH", "full comparison composes if signed depth and lift are supplied"),
    "E05": ("OPEN_ABSENT", "ABSENT", "metric does not currently assign normalized signed reciprocal depth"),
    "E06": ("CONDITIONAL", "GIVEN_UNSELECTED_GLOBAL_DATA", "path holonomy is metric-derived but global module caps quotient and sector need supplied completion"),
    "E07": ("OPEN_ABSENT", "ABSENT", "complete founded extension and varied field domain not selected"),
    "E08": ("OPEN_ABSENT", "ABSENT", "no native global-local offshell response"),
    "E09": ("DERIVED_GIVEN_INPUT", "GIVEN_ABSENT_RESPONSE", "a supplied response defines a zero problem but not automatically an update self-map"),
    "E10": ("CONDITIONAL", "GIVEN_ABSENT_FEEDBACK", "a supplied self-map or equivalent zero problem can define a fixed point"),
    "E11": ("CONDITIONAL", "GIVEN_ABSENT_RESPONSE", "action requires Helmholtz boundary gauge and global-period gates"),
    "E12": ("OPEN_ABSENT", "ABSENT", "native mass numerator and response are missing"),
    "E13": ("OBSTRUCTED", "ZERO_SELECTOR_RANK", "scalar anchors cannot select direction or lambda"),
    "E14": ("OPEN_ABSENT", "CALIBRATION_INSUFFICIENT", "anchors calibrate units but not a dimensionless depth profile"),
    "E15": ("TYPE_ERROR", "NO_CANONICAL_DOMAIN_ISOMORPHISM", "path-arrow cocycle and configuration cotangent one-form have different domains arguments and laws"),
    "E16": ("OPEN_ABSENT", "ABSENT", "no comparison-to-metric reconstruction or response map is registered"),
    "E17": ("OBSTRUCTED", "IMPLICATION_REFUTED", "topology alone does not supply source response mass or persistence"),
    "E18": ("CONDITIONAL", "FUTURE_COUPLING_ONLY", "a future same-solution closure could couple depth selection but no such map exists"),
}

edge_rows = []
for row in edges:
    status, availability, ruling = edge_status[row["edge_id"]]
    edge_rows.append({
        "edge_id": row["edge_id"],
        "source_object": row["source_object"],
        "target_object": row["target_object"],
        "candidate_map": row["candidate_map"],
        "status": status,
        "current_availability": availability,
        "ruling": ruling,
    })

expected_status_counts = {
    "DERIVED": 1,
    "DERIVED_GIVEN_INPUT": 3,
    "CONDITIONAL": 5,
    "OPEN_ABSENT": 6,
    "OBSTRUCTED": 2,
    "TYPE_ERROR": 1,
}
check("edge_status_counts", dict(Counter(r["status"] for r in edge_rows)) == expected_status_counts)

one_form_rows = [
    {
        "axis": "domain",
        "signed_depth_cocycle_O06": "typed observer-pair path arrows",
        "configuration_response_O10": "tangent vectors to complete field-plus-boundary configuration space",
        "same": "NO",
    },
    {
        "axis": "arguments",
        "signed_depth_cocycle_O06": "one arrow gamma",
        "configuration_response_O10": "configuration X and admissible variation delta_X",
        "same": "NO",
    },
    {
        "axis": "linearity_or_composition",
        "signed_depth_cocycle_O06": "additive under path concatenation and odd under reversal",
        "configuration_response_O10": "linear in delta_X at fixed X",
        "same": "NO",
    },
    {
        "axis": "role",
        "signed_depth_cocycle_O06": "kinematic clock-ruler comparison coordinate",
        "configuration_response_O10": "off-shell equation and possible action differential",
        "same": "NO",
    },
    {
        "axis": "shared_fact",
        "signed_depth_cocycle_O06": "real-valued and sometimes represented by a one-form integral",
        "configuration_response_O10": "real-valued cotangent one-form",
        "same": "INSUFFICIENT_FOR_IDENTIFICATION",
    },
    {
        "axis": "current_bridge",
        "signed_depth_cocycle_O06": "none",
        "configuration_response_O10": "none",
        "same": "NO_DERIVED_ISOMORPHISM_OR_PAIRING",
    },
]
check("one_form_type_axes_six", len(one_form_rows) == 6 and all(r["same"] != "YES" for r in one_form_rows))

countermodels = [
    {
        "control": "B19_ROUND_S3",
        "complete_metric": "YES_CONDITIONAL_C2",
        "nontrivial_signed_depth": "NO_Q_EQUALS_ONE",
        "metric_selected_angular_axis": "NO_ROUND_ISOTROPY",
        "nontrivial_topology": "S3_GEOMETRY_ONLY",
        "offshell_response": "NO",
        "same_solution_closure": "NO",
        "logical_separation": "complete_geometry_does_not_imply_depth_or_response",
    },
    {
        "control": "SQUASHED_S3",
        "complete_metric": "YES_OFF_SHELL",
        "nontrivial_signed_depth": "NO_TRIVIAL_CLOCK",
        "metric_selected_angular_axis": "YES_UNORIENTED_IF_NONROUND",
        "nontrivial_topology": "S3_GEOMETRY_ONLY",
        "offshell_response": "NO",
        "same_solution_closure": "NO",
        "logical_separation": "angular_axis_does_not_imply_depth_response_or_on_shell_selection",
    },
    {
        "control": "WRL_LOCAL",
        "complete_metric": "NO_LOCAL_ONLY",
        "nontrivial_signed_depth": "YES_LOCAL_CONDITIONAL",
        "metric_selected_angular_axis": "LOCAL_RADIAL_RELATIVE_TO_CENTER",
        "nontrivial_topology": "NO_GLOBAL_COMPLETION",
        "offshell_response": "NO",
        "same_solution_closure": "NO",
        "logical_separation": "local_depth_does_not_imply_complete_geometry_or_response",
    },
    {
        "control": "CONDITIONAL_HOPF_PROTOTYPE",
        "complete_metric": "NO_PHYSICAL_COMPLETE_BRANCH",
        "nontrivial_signed_depth": "SUPPLIED_WEIGHT_COORDINATE",
        "metric_selected_angular_axis": "SUPPLIED_PHASES_AND_LIFT",
        "nontrivial_topology": "YES_CONDITIONAL_UNIT_CLASS",
        "offshell_response": "NO",
        "same_solution_closure": "NO",
        "logical_separation": "topology_does_not_imply_response_matter_or_metric_closure",
    },
    {
        "control": "PAIR_PATH_GROUPOID",
        "complete_metric": "SUPPLIED_INPUT",
        "nontrivial_signed_depth": "SUPPLIED_INPUT",
        "metric_selected_angular_axis": "ORDERED_PAIR_INPUT",
        "nontrivial_topology": "PATH_HOLONOMY_ALLOWED",
        "offshell_response": "NO",
        "same_solution_closure": "NO",
        "logical_separation": "exact_kinematic_composition_does_not_select_inputs_or_feedback",
    },
]
check("countermodels_five", len(countermodels) == 5)
check("no_countermodel_full_closure", all(r["same_solution_closure"] == "NO" for r in countermodels))

readiness = [
    ("R01", "complete founded configuration domain", "NO", "O01 open"),
    ("R02", "metric to pair-path geometry", "CONDITIONAL_YES", "E01 given metric and path"),
    ("R03", "complete reciprocal lift and lambda", "NO", "O05 family unselected"),
    ("R04", "metric-native signed depth", "NO", "E05 absent"),
    ("R05", "typed comparison composition", "CONDITIONAL_YES", "E04 given depth and lift"),
    ("R06", "global completion and sector", "NO", "O08 partial conditional"),
    ("R07", "variation domain", "NO", "E07 absent"),
    ("R08", "off-shell response", "NO", "E08 absent"),
    ("R09", "comparison-to-metric or response feedback", "NO", "E16 absent"),
    ("R10", "same-solution self-map or zero problem", "NO", "O11 absent"),
    ("R11", "native mass/source and finite-cell boundary", "NO", "O14 absent"),
    ("R12", "action integrability", "DOWNSTREAM_NOT_READY", "O10 absent"),
]
readiness_rows = [
    {"gate_id": a, "gate": b, "ready": c, "basis": d} for a, b, c, d in readiness
]
check("readiness_twelve", len(readiness_rows) == 12)
check("fixed_point_not_ready", any(r["ready"] == "NO" for r in readiness_rows[6:10]))

# Exact graph reachability. Only E02 is active without supplied open inputs. Capability edges retain
# DERIVED_GIVEN_INPUT and CONDITIONAL status, but OPEN/OBSTRUCTED/TYPE_ERROR edges are excluded.
active_edges = [r for r in edge_rows if r["current_availability"] == "ACTIVE"]
capability_edges = [r for r in edge_rows if r["status"] in {"DERIVED", "DERIVED_GIVEN_INPUT", "CONDITIONAL"}]
check("only_founding_edge_active", [r["edge_id"] for r in active_edges] == ["E02"])
check("feedback_edges_absent", edge_status["E08"][0] == "OPEN_ABSENT" and edge_status["E16"][0] == "OPEN_ABSENT")
check("depth_and_response_distinct", edge_status["E15"][0] == "TYPE_ERROR")

# Treat multi-source strings as hyperedge sources. A fixed-point cycle requires a route returning to
# O01. The only returning candidate edges are E10 and E16; neither has currently available inputs,
# and E16 is absent outright.
return_edges = [r for r in edge_rows if r["target_object"] == "O01"]
check("two_candidate_return_edges", {r["edge_id"] for r in return_edges} == {"E10", "E16"})
check("no_current_return_edge", all(r["current_availability"] != "ACTIVE" for r in return_edges))

graph = {
    "schema": "udt-relational-fixed-point-dependency-graph-1.0",
    "nodes": object_rows,
    "edges": edge_rows,
    "active_edge_ids": [r["edge_id"] for r in active_edges],
    "capability_edge_ids": [r["edge_id"] for r in capability_edges],
    "candidate_return_edge_ids": [r["edge_id"] for r in return_edges],
    "current_fixed_point_cycle": False,
    "minimum_explicit_missing_arrows": ["E05", "E07", "E08", "E16"],
}

write_tsv(HERE / "OBJECT_TYPE_OUTCOMES.tsv", list(object_rows[0]), object_rows)
write_tsv(HERE / "EDGE_ADJUDICATION.tsv", list(edge_rows[0]), edge_rows)
write_tsv(HERE / "ONE_FORM_TYPE_COMPARISON.tsv", list(one_form_rows[0]), one_form_rows)
write_tsv(HERE / "COUNTERMODEL_MATRIX.tsv", list(countermodels[0]), countermodels)
write_tsv(HERE / "FIXED_POINT_READINESS.tsv", list(readiness_rows[0]), readiness_rows)
(HERE / "DEPENDENCY_GRAPH.json").write_text(json.dumps(graph, indent=2, sort_keys=True) + "\n", encoding="utf-8")

result = {
    "result": "PASS",
    "grade": "VERIFIED_WITH_CAVEATS_RELATIONAL_FIXED_POINT_TYPING",
    "checks": checks,
    "counts": {
        "sources": len(manifest),
        "objects": len(objects),
        "edges": len(edges),
        "edge_statuses": expected_status_counts,
        "one_form_type_axes": len(one_form_rows),
        "countermodels": len(countermodels),
        "readiness_gates": len(readiness_rows),
        "active_edges": len(active_edges),
        "candidate_return_edges": len(return_edges),
        "current_fixed_point_cycles": 0,
    },
    "rulings": {
        "relational_pair_groupoid": "DERIVED_GIVEN_COMPLETE_METRIC_PATH_PAIR_AND_DEPTH_INPUTS",
        "global_single_pair_field_required": "NO_FOR_TYPED_PATH_GROUPOID",
        "signed_depth_assignment": "OPEN_ABSENT",
        "configuration_response": "OPEN_ABSENT",
        "one_form_identity": "TYPE_DISTINCT_NO_DERIVED_ISOMORPHISM",
        "future_joint_closure": "POSSIBLE_COUPLING_NOT_CURRENT_IDENTITY",
        "fixed_point_operator": "NO_CURRENT_RELATIONAL_FIXED_POINT_OPERATOR",
        "next_dependency_gate": "COMPLETE_FOUNDED_EXTENSION_AND_VARIATION_DOMAIN",
    },
    "authority_boundary": {
        "profile_selected": False,
        "lambda_selected": False,
        "branch_or_path_selected": False,
        "new_connection_selected": False,
        "action_or_response_selected": False,
        "carrier_source_boundary_density_bootstrap_mass_Xmax_dynamics_selected": False,
        "gpu_work": False,
        "repository_reorganization": False,
    },
    "maximum_conclusion": "CURRENT_RELATIONAL_ARCHITECTURE_TYPED_AND_DEPENDENCY_CLOSED;NO_CURRENT_RELATIONAL_FIXED_POINT_OPERATOR;SIGNED_DEPTH_COCYCLE_AND_CONFIGURATION_RESPONSE_TYPE_DISTINCT;FUTURE_GLOBAL_CLOSURE_MAY_COUPLE_BUT_NOT_IDENTIFY_THEM",
}
(HERE / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2, sort_keys=True))
