#!/usr/bin/env python3
import copy
import csv
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def rows(name):
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def exact(table, key, prefix, count):
    expected = {f"{prefix}{i:02d}" for i in range(1, count + 1)}
    actual = [r[key] for r in table]
    if len(actual) != len(set(actual)) or set(actual) != expected:
        raise AssertionError(f"identity:{key}")


def validate_sources(corrupt=False):
    scope = rows("SOURCE_SCOPE.tsv")
    manifest = rows("SOURCE_MANIFEST.tsv")
    if [r["source_path"] for r in scope] != [r["source_path"] for r in manifest]:
        raise AssertionError("source order")
    for index, row in enumerate(manifest):
        path = ROOT / row["source_path"]
        digest = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else ""
        expected = "0" * 64 if corrupt and index == 0 else row["sha256"]
        if not path.is_file() or path.stat().st_size != int(row["size"]) or digest != expected:
            raise AssertionError("source identity")


def validate_model(objects, variations, routes, relations, stack, guards, gates, production, independent):
    exact(objects, "object_id", "O", 20)
    exact(variations, "variation_id", "V", 18)
    exact(routes, "route_id", "R", 8)
    exact(relations, "relation_id", "K", 8)
    exact(stack, "layer_id", "L", 8)
    exact(guards, "guard_id", "D", 10)
    exact(gates, "gate_id", "G", 8)

    o = {r["object_id"]: r for r in objects}
    v = {r["variation_id"]: r for r in variations}
    r = {x["route_id"]: x for x in routes}
    k = {x["relation_id"]: x for x in relations}

    if o["O06"]["primary_class"] != "DERIVED_ABSTRACT_KINEMATICS" or o["O06"]["variation_status"] != "NOT_INDEPENDENT_NATIVE_VARIATION":
        raise AssertionError("phi promotion")
    if o["O08"]["primary_class"] != "RELATIONAL_QUERY_LABEL":
        raise AssertionError("pair promotion")
    if o["O09"]["primary_class"] != "RELATIONAL_QUERY_LABEL":
        raise AssertionError("path promotion")
    if o["O12"]["primary_class"] != "OPEN_REPRESENTATION_PARAMETER" or o["O12"]["variation_status"] != "NOT_AUTHORIZED_LOCAL_FIELD":
        raise AssertionError("lambda promotion")
    if o["O13"]["primary_class"] != "PRESENTATION_GAUGE":
        raise AssertionError("screen promotion")
    if o["O20"]["primary_class"] != "COMPARISON_ONLY_NONNATIVE":
        raise AssertionError("atlas scalar promotion")
    if o["O18"]["primary_class"] != "ABSENT_DOWNSTREAM_PHYSICS" or o["O19"]["primary_class"] != "ABSENT_DOWNSTREAM_PHYSICS":
        raise AssertionError("downstream promotion")
    if o["O07"]["primary_class"] != "OPEN_RELATIONAL_FUNCTIONAL":
        raise AssertionError("depth hidden")
    if o["O02"]["primary_class"] != "OPEN_GLOBAL_CONFIGURATION_DATA" or o["O16"]["primary_class"] != "OPEN_GLOBAL_BOUNDARY_DATA":
        raise AssertionError("global gap hidden")
    if o["O05"]["variation_status"] != "OPEN_RETAIN_WITHIN_DELTA_G" or v["V01"]["domain_action"] != "RETAIN":
        raise AssertionError("metric directions dropped")
    if v["V04"]["classification"] != "FORBIDDEN_NATIVE_DOUBLE_COUNT":
        raise AssertionError("phi double count")
    if v["V08"]["classification"] != "UNAUTHORIZED_FIELD_PROMOTION":
        raise AssertionError("lambda field")
    if v["V11"]["classification"] != "GLOBAL_SECTOR_CHANGE":
        raise AssertionError("topology tangent")
    if v["V18"]["domain_action"] != "DO_NOT_COUNT_AS_FIELDS":
        raise AssertionError("mode count")
    if r["R03"]["status"] != "EXACT_SPECIAL_STRATUM_UNSELECTED":
        raise AssertionError("lambda one selected")
    if r["R05"]["status"] != "TYPE_SCAFFOLD_SUPPORTED_NOT_PHYSICALLY_SELECTED":
        raise AssertionError("stack promoted")
    if k["K01"]["relation"] != "EXACT_SUBSTRATUM" or "fixed u" not in k["K01"]["exact_meaning"]:
        raise AssertionError("stratum relation")
    if any(row["status"] == "DERIVED" for row in gates):
        raise AssertionError("gate promotion")
    if production.get("result") != "PASS" or independent.get("result") != "PASS":
        raise AssertionError("result status")
    if production.get("rulings", {}).get("container_relation") != "DEMOCRATIC_1PLUS3_IS_FIBERWISE_EXACT_LAMBDA_ONE_STRATUM_OF_PAIR_INDEXED_CONTAINER":
        raise AssertionError("production relation")
    if production.get("rulings", {}).get("variation_domain") != "OPEN_UNSELECTED":
        raise AssertionError("variation promoted")
    if any(production.get("authority_boundary", {}).values()):
        raise AssertionError("authority escape")
    if independent.get("counts", {}).get("checks") != 46 or independent.get("rulings", {}).get("container_relation") != "LAMBDA_ONE_EXACT_SPECIAL_STRATUM":
        raise AssertionError("independent mismatch")
    if "NO_NEW_FIELD_OR_MODE_COUNT" not in production.get("maximum_conclusion", ""):
        raise AssertionError("scope promotion")


def changed(table, key, identity, field, value):
    output = copy.deepcopy(table)
    next(row for row in output if row[key] == identity)[field] = value
    return output


def expect_failure(callback):
    try:
        callback()
    except (AssertionError, KeyError):
        return "PASS"
    raise AssertionError("catch accepted corruption")


def main():
    objects = rows("CONFIGURATION_OBJECT_ADJUDICATION.tsv")
    variations = rows("VARIATION_DOMAIN_ADJUDICATION.tsv")
    routes = rows("ONTOLOGY_ROUTE_ADJUDICATION.tsv")
    relations = rows("CODOMAIN_RELATION_ATLAS.tsv")
    stack = rows("RELATIONAL_CONFIGURATION_STACK.tsv")
    guards = rows("DOF_DOUBLE_COUNT_GUARDS.tsv")
    gates = rows("OPEN_GATE_MATRIX.tsv")
    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
    contract = rows("FALSIFICATION_CONTRACT.tsv")

    validate_model(objects, variations, routes, relations, stack, guards, gates, production, independent)
    validate_sources()
    if {row["catch_id"] for row in contract} != {f"C{i:02d}" for i in range(1, 21)}:
        raise AssertionError("contract coverage")

    def model(o=objects, v=variations, r=routes, k=relations, s=stack, d=guards, g=gates, p=production, i=independent):
        return lambda: validate_model(o, v, r, k, s, d, g, p, i)

    catches = {}
    catches["C01"] = expect_failure(model(o=objects[:-1]))
    catches["C02"] = expect_failure(model(v=variations + [copy.deepcopy(variations[0])]))
    catches["C03"] = expect_failure(model(o=changed(objects, "object_id", "O06", "primary_class", "PHYSICAL_SCALAR_FIELD")))
    catches["C04"] = expect_failure(model(o=changed(objects, "object_id", "O08", "primary_class", "PHYSICAL_VECTOR_FIELDS")))
    catches["C05"] = expect_failure(model(o=changed(objects, "object_id", "O09", "primary_class", "PHYSICAL_PATH_FIELD")))
    catches["C06"] = expect_failure(model(o=changed(objects, "object_id", "O12", "variation_status", "LOCAL_FIELD_VARIATION")))
    catches["C07"] = expect_failure(model(r=changed(routes, "route_id", "R03", "status", "SELECTED_UNIVERSAL")))
    catches["C08"] = expect_failure(model(o=changed(objects, "object_id", "O13", "primary_class", "PHYSICAL_METRIC_DOF")))
    catches["C09"] = expect_failure(model(v=changed(variations, "variation_id", "V01", "domain_action", "DROP_ANGULAR_MIXING")))
    catches["C10"] = expect_failure(model(v=changed(variations, "variation_id", "V11", "classification", "BULK_TANGENT")))
    catches["C11"] = expect_failure(model(r=changed(routes, "route_id", "R05", "status", "SELECTED_COMPLETE_CONFIGURATION")))
    catches["C12"] = expect_failure(model(o=changed(objects, "object_id", "O19", "primary_class", "DERIVED_NATIVE_ACTION")))
    catches["C13"] = expect_failure(model(v=changed(variations, "variation_id", "V18", "domain_action", "SEVEN_PROPAGATING_FIELDS")))
    catches["C14"] = expect_failure(model(k=changed(relations, "relation_id", "K01", "relation", "INCOMPATIBLE_ONTOLOGIES")))
    catches["C15"] = expect_failure(model(o=changed(objects, "object_id", "O20", "primary_class", "NATIVE_SCALAR_FIELD")))
    catches["C16"] = expect_failure(model(o=changed(objects, "object_id", "O18", "primary_class", "PRESENT_NATIVE_MATTER")))
    catches["C17"] = expect_failure(model(o=changed(objects, "object_id", "O07", "primary_class", "DERIVED_FROM_ABSTRACT_PHI")))
    catches["C18"] = expect_failure(model(o=changed(objects, "object_id", "O02", "primary_class", "SELECTED_GLOBAL_CONFIGURATION")))
    bad_independent = copy.deepcopy(independent)
    bad_independent["counts"]["checks"] = 45
    catches["C19"] = expect_failure(model(i=bad_independent))
    catches["C20"] = expect_failure(lambda: validate_sources(True))
    if len(catches) != 20 or set(catches.values()) != {"PASS"}:
        raise AssertionError("catch coverage")

    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(["catch_id", "result"])
        writer.writerows(sorted(catches.items()))

    result = {
        "schema": "udt-complete-relational-configuration-domain-verification-1.0",
        "result": "PASS",
        "grade": production["grade"],
        "objects": len(objects),
        "variations": len(variations),
        "routes": len(routes),
        "relations": len(relations),
        "stack_layers": len(stack),
        "double_count_guards": len(guards),
        "open_gates": len(gates),
        "production_checks": len(production["checks"]),
        "independent_checks": len(independent["checks"]),
        "catch_count": len(catches),
        "catch_proofs": catches,
        "maximum_conclusion": production["maximum_conclusion"],
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
