#!/usr/bin/env python3
import csv
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent


def rows(name):
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


checks = {}


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks[name] = "PASS"


objects_u = rows("OBJECT_TYPE_UNIVERSE.tsv")
edges_u = rows("EDGE_UNIVERSE.tsv")
objects = rows("OBJECT_TYPE_OUTCOMES.tsv")
edges = rows("EDGE_ADJUDICATION.tsv")
forms = rows("ONE_FORM_TYPE_COMPARISON.tsv")
controls = rows("COUNTERMODEL_MATRIX.tsv")
readiness = rows("FIXED_POINT_READINESS.tsv")
graph = json.loads((HERE / "DEPENDENCY_GRAPH.json").read_text())

check("object_identity", [r["object_id"] for r in objects_u] == [r["object_id"] for r in objects])
check("edge_identity", [r["edge_id"] for r in edges_u] == [r["edge_id"] for r in edges])
check("object_count", len(objects) == 14)
check("edge_count", len(edges) == 18)
check("object_unique", len({r["object_id"] for r in objects}) == 14)
check("edge_unique", len({r["edge_id"] for r in edges}) == 18)

status_counts = Counter(r["status"] for r in edges)
check("derived_count", status_counts["DERIVED"] == 1)
check("derived_given_count", status_counts["DERIVED_GIVEN_INPUT"] == 3)
check("conditional_count", status_counts["CONDITIONAL"] == 5)
check("open_count", status_counts["OPEN_ABSENT"] == 6)
check("obstructed_count", status_counts["OBSTRUCTED"] == 2)
check("type_error_count", status_counts["TYPE_ERROR"] == 1)

by_object = {r["object_id"]: r for r in objects}
by_edge = {r["edge_id"]: r for r in edges}
check("founded_coordinate_derived", by_object["O04"]["current_status"] == "DERIVED")
check("depth_absent", by_object["O06"]["current_status"] == "OPEN_ABSENT")
check("response_absent", by_object["O10"]["current_status"] == "OPEN_ABSENT")
check("bootstrap_map_absent", by_object["O11"]["current_status"] == "OPEN_ABSENT")
check("depth_edge_absent", by_edge["E05"]["status"] == "OPEN_ABSENT")
check("response_edge_absent", by_edge["E08"]["status"] == "OPEN_ABSENT")
check("reconstruction_edge_absent", by_edge["E16"]["status"] == "OPEN_ABSENT")
check("one_form_identification_type_error", by_edge["E15"]["status"] == "TYPE_ERROR")
check("anchors_zero_selector", by_edge["E13"]["status"] == "OBSTRUCTED")
check("topology_not_matter", by_edge["E17"]["status"] == "OBSTRUCTED")
check("future_coupling_only", by_edge["E18"]["current_availability"] == "FUTURE_COUPLING_ONLY")

check("six_type_axes", len(forms) == 6)
check("no_type_axis_equal", all(r["same"] != "YES" for r in forms))
form_by_axis = {r["axis"]: r for r in forms}
check("domains_differ", form_by_axis["domain"]["same"] == "NO")
check("composition_laws_differ", form_by_axis["linearity_or_composition"]["same"] == "NO")
check("no_bridge", form_by_axis["current_bridge"]["same"] == "NO_DERIVED_ISOMORPHISM_OR_PAIRING")

check("five_countermodels", len(controls) == 5)
check("countermodels_unique", len({r["control"] for r in controls}) == 5)
check("all_countermodels_unclosed", all(r["same_solution_closure"] == "NO" for r in controls))
control = {r["control"]: r for r in controls}
check("B19_separates_complete_from_depth", control["B19_ROUND_S3"]["complete_metric"].startswith("YES_") and control["B19_ROUND_S3"]["nontrivial_signed_depth"].startswith("NO_"))
check("squashed_separates_axis_from_depth", control["SQUASHED_S3"]["metric_selected_angular_axis"].startswith("YES_") and control["SQUASHED_S3"]["nontrivial_signed_depth"].startswith("NO_"))
check("WRL_separates_depth_from_complete", control["WRL_LOCAL"]["nontrivial_signed_depth"].startswith("YES_") and control["WRL_LOCAL"]["complete_metric"].startswith("NO_"))
check("Hopf_separates_topology_from_response", control["CONDITIONAL_HOPF_PROTOTYPE"]["nontrivial_topology"].startswith("YES_") and control["CONDITIONAL_HOPF_PROTOTYPE"]["offshell_response"] == "NO")

check("twelve_readiness_gates", len(readiness) == 12)
ready = {r["gate_id"]: r["ready"] for r in readiness}
check("variation_not_ready", ready["R07"] == "NO")
check("response_not_ready", ready["R08"] == "NO")
check("feedback_not_ready", ready["R09"] == "NO")
check("self_map_not_ready", ready["R10"] == "NO")

check("graph_node_count", len(graph["nodes"]) == 14)
check("graph_edge_count", len(graph["edges"]) == 18)
check("only_E02_active", graph["active_edge_ids"] == ["E02"])
check("return_edges", set(graph["candidate_return_edge_ids"]) == {"E10", "E16"})
check("no_fixed_point_cycle", graph["current_fixed_point_cycle"] is False)
check("missing_arrows", set(graph["minimum_explicit_missing_arrows"]) == {"E05", "E07", "E08", "E16"})

result = {
    "result": "PASS",
    "checks": checks,
    "counts": {
        "checks": len(checks),
        "objects": len(objects),
        "edges": len(edges),
        "one_form_axes": len(forms),
        "countermodels": len(controls),
        "readiness_gates": len(readiness),
        "active_edges": len(graph["active_edge_ids"]),
        "fixed_point_cycles": 0,
    },
    "rulings": {
        "fixed_point": "NO_CURRENT_RELATIONAL_FIXED_POINT_OPERATOR",
        "one_forms": "TYPE_DISTINCT",
        "future_relation": "COUPLING_POSSIBLE_IDENTIFICATION_NOT_DERIVED",
    },
}
(HERE / "INDEPENDENT_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2, sort_keys=True))
