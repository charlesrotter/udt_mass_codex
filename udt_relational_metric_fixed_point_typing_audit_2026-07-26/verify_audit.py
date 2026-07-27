#!/usr/bin/env python3
import copy
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OBJECTS = {f"O{i:02d}" for i in range(1, 15)}
EDGES = {f"E{i:02d}" for i in range(1, 19)}


def rows(name):
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def exact(values, key, expected):
    actual = [r[key] for r in values]
    if len(actual) != len(set(actual)) or set(actual) != expected:
        raise AssertionError(f"identity:{key}")


def validate_sources(corrupt=False):
    scope = rows("SOURCE_SCOPE.tsv")
    manifest = rows("SOURCE_MANIFEST.tsv")
    if [r["source_path"] for r in scope] != [r["source_path"] for r in manifest]:
        raise AssertionError("source order")
    for i, row in enumerate(manifest):
        path = ROOT / row["source_path"]
        expected = "0" * 64 if corrupt and i == 0 else row["sha256"]
        if not path.is_file() or path.stat().st_size != int(row["size"]) or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise AssertionError("source identity")


def validate_model(objects, edges, forms, controls, readiness, graph, production, independent):
    exact(objects, "object_id", OBJECTS)
    exact(edges, "edge_id", EDGES)
    if len(forms) != 6 or len({r["axis"] for r in forms}) != 6:
        raise AssertionError("one-form axes")
    if len(controls) != 5 or len({r["control"] for r in controls}) != 5:
        raise AssertionError("countermodels")
    if len(readiness) != 12 or {r["gate_id"] for r in readiness} != {f"R{i:02d}" for i in range(1, 13)}:
        raise AssertionError("readiness")

    o = {r["object_id"]: r for r in objects}
    e = {r["edge_id"]: r for r in edges}
    f = {r["axis"]: r for r in forms}
    c = {r["control"]: r for r in controls}
    r = {x["gate_id"]: x for x in readiness}

    if o["O04"]["current_status"] != "DERIVED":
        raise AssertionError("phi demoted")
    if o["O06"]["current_status"] != "OPEN_ABSENT" or e["E05"]["status"] != "OPEN_ABSENT":
        raise AssertionError("depth promoted")
    if o["O05"]["current_status"] != "CONDITIONAL_FAMILY_LAMBDA_OPEN" or e["E03"]["ruling"].find("lambda remains open") < 0:
        raise AssertionError("lambda selected")
    if o["O09"]["current_status"] != "OPEN_UNSELECTED" or o["O10"]["current_status"] != "OPEN_ABSENT":
        raise AssertionError("response order")
    if e["E15"]["status"] != "TYPE_ERROR" or any(x["same"] == "YES" for x in forms):
        raise AssertionError("one-forms identified")
    if f["domain"]["same"] != "NO" or f["current_bridge"]["same"] != "NO_DERIVED_ISOMORPHISM_OR_PAIRING":
        raise AssertionError("one-form bridge")
    if e["E13"]["status"] != "OBSTRUCTED" or e["E17"]["status"] != "OBSTRUCTED":
        raise AssertionError("false selector")
    if o["O11"]["current_status"] != "OPEN_ABSENT" or e["E16"]["status"] != "OPEN_ABSENT":
        raise AssertionError("fixed point promoted")
    if e["E18"]["current_availability"] != "FUTURE_COUPLING_ONLY":
        raise AssertionError("future coupling promoted")
    if any(x["same_solution_closure"] != "NO" for x in controls):
        raise AssertionError("countermodel spliced")
    if c["B19_ROUND_S3"]["nontrivial_signed_depth"] != "NO_Q_EQUALS_ONE":
        raise AssertionError("B19 splice")
    if c["CONDITIONAL_HOPF_PROTOTYPE"]["offshell_response"] != "NO":
        raise AssertionError("topology promoted")
    if any(r[g]["ready"] != "NO" for g in ["R07", "R08", "R09", "R10"]):
        raise AssertionError("fixed-point readiness")

    expected_status = {"DERIVED": 1, "DERIVED_GIVEN_INPUT": 3, "CONDITIONAL": 5, "OPEN_ABSENT": 6, "OBSTRUCTED": 2, "TYPE_ERROR": 1}
    if dict(Counter(x["status"] for x in edges)) != expected_status:
        raise AssertionError("edge status counts")
    if graph.get("current_fixed_point_cycle") is not False or graph.get("active_edge_ids") != ["E02"]:
        raise AssertionError("graph closure")
    if set(graph.get("candidate_return_edge_ids", [])) != {"E10", "E16"} or set(graph.get("minimum_explicit_missing_arrows", [])) != {"E05", "E07", "E08", "E16"}:
        raise AssertionError("graph return")

    if production.get("result") != "PASS" or production.get("grade") != "VERIFIED_WITH_CAVEATS_RELATIONAL_FIXED_POINT_TYPING":
        raise AssertionError("production status")
    if production.get("counts", {}).get("objects") != 14 or production.get("counts", {}).get("edges") != 18 or production.get("counts", {}).get("current_fixed_point_cycles") != 0:
        raise AssertionError("production counts")
    if set(production.get("checks", {}).values()) != {"PASS"} or any(production.get("authority_boundary", {}).values()):
        raise AssertionError("production authority")
    if production.get("rulings", {}).get("fixed_point_operator") != "NO_CURRENT_RELATIONAL_FIXED_POINT_OPERATOR":
        raise AssertionError("fixed point ruling")
    if production.get("rulings", {}).get("one_form_identity") != "TYPE_DISTINCT_NO_DERIVED_ISOMORPHISM":
        raise AssertionError("type ruling")
    if "UNIVERSAL_NO_GO" in production.get("maximum_conclusion", ""):
        raise AssertionError("scope promotion")

    if independent.get("result") != "PASS" or independent.get("counts", {}).get("checks") != 46:
        raise AssertionError("independent status")
    if independent.get("rulings", {}).get("fixed_point") != "NO_CURRENT_RELATIONAL_FIXED_POINT_OPERATOR" or independent.get("rulings", {}).get("one_forms") != "TYPE_DISTINCT":
        raise AssertionError("independent rulings")
    if set(independent.get("checks", {}).values()) != {"PASS"}:
        raise AssertionError("independent checks")


def changed(table, key, identity, field, value):
    output = copy.deepcopy(table)
    next(r for r in output if r[key] == identity)[field] = value
    return output


def expect_failure(callback):
    try:
        callback()
    except (AssertionError, KeyError):
        return "PASS"
    raise AssertionError("catch accepted corruption")


def main():
    objects = rows("OBJECT_TYPE_OUTCOMES.tsv")
    edges = rows("EDGE_ADJUDICATION.tsv")
    forms = rows("ONE_FORM_TYPE_COMPARISON.tsv")
    controls = rows("COUNTERMODEL_MATRIX.tsv")
    readiness = rows("FIXED_POINT_READINESS.tsv")
    graph = json.loads((HERE / "DEPENDENCY_GRAPH.json").read_text())
    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
    validate_model(objects, edges, forms, controls, readiness, graph, production, independent)
    validate_sources()

    def model(o=objects, e=edges, f=forms, c=controls, r=readiness, g=graph, p=production, i=independent):
        return lambda: validate_model(o, e, f, c, r, g, p, i)

    catches = {}
    catches["missing_object"] = expect_failure(model(o=objects[:-1]))
    catches["duplicate_edge"] = expect_failure(model(e=edges + [copy.deepcopy(edges[0])]))
    catches["phi_demotion"] = expect_failure(model(o=changed(objects, "object_id", "O04", "current_status", "OPEN_PLACEHOLDER")))
    catches["depth_promotion"] = expect_failure(model(o=changed(objects, "object_id", "O06", "current_status", "DERIVED")))
    catches["lambda_selection"] = expect_failure(model(o=changed(objects, "object_id", "O05", "current_status", "LAMBDA_ONE_SELECTED")))
    catches["one_form_identification"] = expect_failure(model(e=changed(edges, "edge_id", "E15", "status", "DERIVED")))
    bad_graph = copy.deepcopy(graph)
    bad_graph["current_fixed_point_cycle"] = True
    catches["fixed_point_without_return"] = expect_failure(model(g=bad_graph))
    catches["response_before_variation"] = expect_failure(model(o=changed(objects, "object_id", "O10", "current_status", "DERIVED")))
    catches["cross_branch_splice"] = expect_failure(model(c=changed(controls, "control", "B19_ROUND_S3", "nontrivial_signed_depth", "YES_WRL_PROFILE")))
    catches["topology_as_response"] = expect_failure(model(c=changed(controls, "control", "CONDITIONAL_HOPF_PROTOTYPE", "offshell_response", "YES")))
    catches["anchors_as_selector"] = expect_failure(model(e=changed(edges, "edge_id", "E13", "status", "DERIVED")))
    catches["bootstrap_as_map"] = expect_failure(model(o=changed(objects, "object_id", "O11", "current_status", "DERIVED_FIXED_POINT_MAP")))
    bad_independent = copy.deepcopy(independent)
    bad_independent["counts"]["checks"] = 45
    catches["independent_graph"] = expect_failure(model(i=bad_independent))
    bad_scope = copy.deepcopy(production)
    bad_scope["maximum_conclusion"] += ";UNIVERSAL_NO_GO"
    catches["universal_scope_promotion"] = expect_failure(model(p=bad_scope))
    bad_action = copy.deepcopy(production)
    bad_action["authority_boundary"]["action_or_response_selected"] = True
    catches["action_escape"] = expect_failure(model(p=bad_action))
    catches["source_identity"] = expect_failure(lambda: validate_sources(True))

    if len(catches) != 16 or set(catches.values()) != {"PASS"}:
        raise AssertionError("catch coverage")
    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(["catch", "result"])
        writer.writerows(sorted(catches.items()))
    result = {
        "schema": "udt-relational-fixed-point-typing-verification-1.0",
        "result": "PASS",
        "grade": production["grade"],
        "objects": len(objects), "edges": len(edges), "one_form_axes": len(forms),
        "countermodels": len(controls), "readiness_gates": len(readiness),
        "production_checks": len(production["checks"]),
        "independent_checks": len(independent["checks"]),
        "catch_count": len(catches), "catch_proofs": catches,
        "fixed_point_cycles": 0,
        "maximum_conclusion": production["maximum_conclusion"],
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
