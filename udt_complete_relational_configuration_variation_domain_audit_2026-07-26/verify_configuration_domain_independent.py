#!/usr/bin/env python3
import csv
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent


def rows(name):
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def check_ids(table, key, prefix, count):
    values = [r[key] for r in table]
    return len(values) == count and len(values) == len(set(values)) and set(values) == {f"{prefix}{i:02d}" for i in range(1, count + 1)}


objects_u = rows("CONFIGURATION_OBJECT_UNIVERSE.tsv")
variations_u = rows("VARIATION_CANDIDATE_UNIVERSE.tsv")
routes_u = rows("ONTOLOGY_ROUTE_UNIVERSE.tsv")
objects = rows("CONFIGURATION_OBJECT_ADJUDICATION.tsv")
variations = rows("VARIATION_DOMAIN_ADJUDICATION.tsv")
routes = rows("ONTOLOGY_ROUTE_ADJUDICATION.tsv")
relations = rows("CODOMAIN_RELATION_ATLAS.tsv")
stack = rows("RELATIONAL_CONFIGURATION_STACK.tsv")
guards = rows("DOF_DOUBLE_COUNT_GUARDS.tsv")
gates = rows("OPEN_GATE_MATRIX.tsv")
production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())

o = {r["object_id"]: r for r in objects}
v = {r["variation_id"]: r for r in variations}
r = {x["route_id"]: x for x in routes}
k = {x["relation_id"]: x for x in relations}


def outer(n):
    return tuple(tuple(a * b for b in n) for a in n)


def x_spatial(lam, n):
    p = outer(n)
    return tuple(tuple(lam * (Fraction(int(i == j)) - p[i][j]) + p[i][j] for j in range(3)) for i in range(3))


directions = [
    (Fraction(1), Fraction(0), Fraction(0)),
    (Fraction(0), Fraction(1), Fraction(0)),
    (Fraction(0), Fraction(0), Fraction(1)),
    (Fraction(3, 5), Fraction(4, 5), Fraction(0)),
    (Fraction(0), Fraction(3, 5), Fraction(4, 5)),
    (Fraction(4, 5), Fraction(0), Fraction(3, 5)),
]

checks = {}
checks["object_universe_ids"] = check_ids(objects_u, "object_id", "O", 20)
checks["variation_universe_ids"] = check_ids(variations_u, "variation_id", "V", 18)
checks["route_universe_ids"] = check_ids(routes_u, "route_id", "R", 8)
checks["object_outcome_ids"] = check_ids(objects, "object_id", "O", 20)
checks["variation_outcome_ids"] = check_ids(variations, "variation_id", "V", 18)
checks["route_outcome_ids"] = check_ids(routes, "route_id", "R", 8)
checks["relation_ids"] = check_ids(relations, "relation_id", "K", 8)
checks["stack_ids"] = check_ids(stack, "layer_id", "L", 8)
checks["guard_ids"] = check_ids(guards, "guard_id", "D", 10)
checks["gate_ids"] = check_ids(gates, "gate_id", "G", 8)
checks["lambda_one_collapses"] = len({x_spatial(Fraction(1), n) for n in directions}) == 1
checks["lambda_zero_directional"] = len({x_spatial(Fraction(0), n) for n in directions}) == len(directions)
checks["lambda_minus_one_directional"] = len({x_spatial(Fraction(-1), n) for n in directions}) == len(directions)
checks["lambda_one_identity"] = x_spatial(Fraction(1), directions[0]) == tuple(tuple(Fraction(int(i == j)) for j in range(3)) for i in range(3))
checks["stratum_relation"] = k["K01"]["relation"] == "EXACT_SUBSTRATUM"
checks["no_reverse_relation"] = k["K02"]["relation"] == "NO_REVERSE_INCLUSION"
checks["stack_not_selected"] = r["R05"]["status"] == "TYPE_SCAFFOLD_SUPPORTED_NOT_PHYSICALLY_SELECTED"
checks["rank_two_not_selected"] = r["R02"]["status"] == "OPEN_NOT_SELECTED"
checks["democratic_not_selected"] = r["R03"]["status"] == "EXACT_SPECIAL_STRATUM_UNSELECTED"
checks["pair_container_conditional"] = r["R04"]["status"] == "CONDITIONAL_GENERAL_RELATIONAL_CONTAINER"
checks["phi_abstract"] = o["O06"]["primary_class"] == "DERIVED_ABSTRACT_KINEMATICS"
checks["phi_not_varied"] = o["O06"]["variation_status"] == "NOT_INDEPENDENT_NATIVE_VARIATION"
checks["depth_open"] = o["O07"]["primary_class"] == "OPEN_RELATIONAL_FUNCTIONAL"
checks["pair_query"] = o["O08"]["primary_class"] == "RELATIONAL_QUERY_LABEL"
checks["path_query"] = o["O09"]["primary_class"] == "RELATIONAL_QUERY_LABEL"
checks["readout_conditional"] = o["O11"]["primary_class"] == "CONDITIONAL_RELATIONAL_REPRESENTATION"
checks["lambda_parameter"] = o["O12"]["primary_class"] == "OPEN_REPRESENTATION_PARAMETER"
checks["lambda_not_local"] = o["O12"]["variation_status"] == "NOT_AUTHORIZED_LOCAL_FIELD"
checks["screen_gauge"] = o["O13"]["primary_class"] == "PRESENTATION_GAUGE"
checks["global_sector"] = o["O15"]["primary_class"] == "GLOBAL_SECTOR_LABEL"
checks["boundary_open"] = o["O16"]["variation_status"] == "OPEN_BOUNDARY_VARIATION"
checks["anchors_fixed"] = o["O17"]["variation_status"] == "FIXED_ANCHOR_NOT_VARIED"
checks["matter_absent"] = o["O18"]["variation_status"] == "ABSENT_FROM_CURRENT_DOMAIN"
checks["action_downstream"] = o["O19"]["variation_status"] == "DOWNSTREAM_NOT_DOMAIN"
checks["comparison_scalar_only"] = o["O20"]["primary_class"] == "COMPARISON_ONLY_NONNATIVE"
checks["full_metric_retained"] = v["V01"]["domain_action"] == "RETAIN"
checks["phi_double_count_rejected"] = v["V04"]["classification"] == "FORBIDDEN_NATIVE_DOUBLE_COUNT"
checks["query_changes_separate"] = all(v[x]["domain_action"] == "SEPARATE" for x in ["V06", "V07"])
checks["lambda_field_rejected"] = v["V08"]["classification"] == "UNAUTHORIZED_FIELD_PROMOTION"
checks["topology_separate"] = v["V11"]["classification"] == "GLOBAL_SECTOR_CHANGE"
checks["lift_not_mode_count"] = v["V18"]["domain_action"] == "DO_NOT_COUNT_AS_FIELDS"
checks["all_gates_open"] = all(x["status"] != "DERIVED" for x in gates)
checks["object_class_counts_replay"] = production["counts"]["object_primary_classes"] == dict(sorted(Counter(x["primary_class"] for x in objects).items()))
checks["variation_class_counts_replay"] = production["counts"]["variation_classes"] == dict(sorted(Counter(x["classification"] for x in variations).items()))
checks["authority_closed"] = not any(production["authority_boundary"].values())
checks["maximum_scoped"] = "NO_NEW_FIELD_OR_MODE_COUNT" in production["maximum_conclusion"] and "ACTION_DERIVED" not in production["maximum_conclusion"]

if not all(checks.values()):
    failed = sorted(key for key, value in checks.items() if not value)
    raise AssertionError(f"independent failures: {failed}")

result = {
    "schema": "udt-complete-relational-configuration-domain-independent-1.0",
    "result": "PASS",
    "counts": {
        "checks": len(checks),
        "objects": len(objects),
        "variations": len(variations),
        "routes": len(routes),
        "directions_tested": len(directions),
    },
    "rulings": {
        "container_relation": "LAMBDA_ONE_EXACT_SPECIAL_STRATUM",
        "variation_domain": "OPEN_FULL_METRIC_CANDIDATE_RETAINED",
        "double_count": "NO_PHI_PAIR_PATH_LAMBDA_GAUGE_OR_TOPOLOGY_PROMOTION",
    },
    "checks": {key: "PASS" for key in sorted(checks)},
}
(HERE / "INDEPENDENT_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2, sort_keys=True))
