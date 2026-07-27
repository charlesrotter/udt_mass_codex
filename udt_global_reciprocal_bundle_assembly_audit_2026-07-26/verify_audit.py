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


def exact(table, key, expected):
    values = [r[key] for r in table]
    if len(values) != len(expected) or len(values) != len(set(values)) or set(values) != set(expected):
        raise AssertionError(f"identity:{key}")


def validate_sources(corrupt=False):
    scope = rows("SOURCE_SCOPE.tsv")
    manifest = rows("SOURCE_MANIFEST.tsv")
    if [r["source_path"] for r in scope] != [r["source_path"] for r in manifest]:
        raise AssertionError("source order")
    for i, row in enumerate(manifest):
        path = ROOT / row["source_path"]
        digest = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else ""
        expected = "0" * 64 if corrupt and i == 0 else row["sha256"]
        if not path.is_file() or path.stat().st_size != int(row["size"]) or digest != expected:
            raise AssertionError("source identity")


def validate_model(completion, controls, strata, gates, holonomy, variation, production, independent):
    fc = [
        "FC01_BOUNDARY_BOUNDARY", "FC02_ONE_CAP_BOUNDARY", "FC03_TWO_CAP_P0", "FC04_TWO_CAP_P1",
        "FC05_TWO_CAP_P_GT1", "FC06_NONPRIMITIVE_CAP", "FC07_PERIODIC_TORUS_BUNDLE",
        "FC08_MIRROR_DOUBLE", "FC09_NONORIENTABLE_GLUE", "FC10_STRATIFIED_PROJECTOR",
        "FC11_NONINTEGRABLE_DISTRIBUTION", "FC12_RECIPROCAL_TORIC_DIAGONAL",
    ]
    exact(completion, "completion_id", fc)
    exact(controls, "control_id", [f"Q{i:02d}" for i in range(1, 5)])
    exact(strata, "stratum_id", [f"L{i:02d}" for i in range(1, 5)])
    exact(gates, "gate_id", [f"G{i:02d}" for i in range(1, 13)])
    exact(variation, "variation_id", [f"V{i:02d}" for i in range(1, 9)])
    if len(holonomy) != 3 or len({r["control"] for r in holonomy}) != 3:
        raise AssertionError("holonomy coverage")

    c = {r["completion_id"]: r for r in completion}
    q = {r["control_id"]: r for r in controls}
    s = {r["stratum_id"]: r for r in strata}
    g = {r["gate_id"]: r for r in gates}
    h = {r["control"]: r for r in holonomy}
    v = {r["variation_id"]: r for r in variation}

    if sum(row["pair_bundle_status"].startswith("PASS_") for row in completion) != 1 or not c["FC04_TWO_CAP_P1"]["pair_bundle_status"].startswith("PASS_"):
        raise AssertionError("taxonomy promoted")
    if c["FC02_ONE_CAP_BOUNDARY"]["global_join_status"] != "CAP_COORDINATE_COLLAPSE_NOT_AUTOMATIC_FRAME_FAILURE":
        raise AssertionError("cap degeneration")
    if c["FC06_NONPRIMITIVE_CAP"]["pair_bundle_status"] != "REGULAR_STRATUM_ONLY":
        raise AssertionError("singular promotion")
    if "MONODROMY" not in c["FC07_PERIODIC_TORUS_BUNDLE"]["global_join_status"] or "UNSELECTED_LIFT" not in c["FC08_MIRROR_DOUBLE"]["global_join_status"]:
        raise AssertionError("join data hidden")
    if "RANK_CHANGE" not in c["FC10_STRATIFIED_PROJECTOR"]["global_join_status"]:
        raise AssertionError("rank transition hidden")

    expected_dims = {"L01": "1", "L02": "3", "L03": "1", "L04": "3"}
    if {key: s[key]["connected_lorentz_centralizer_dimension"] for key in expected_dims} != expected_dims:
        raise AssertionError("centralizer dimensions")
    if "ruler" not in s["L02"]["connected_stabilizer"].lower() or "requires_n_only" not in s["L02"]["section_data"]:
        raise AssertionError("minus one collapse")
    if any(row["pair_bundle_overlap"] != "YES" or row["typed_path_groupoid"] != "YES" for row in strata):
        raise AssertionError("all-lambda groupoid")
    if s["L04"]["parallel_endpoint_on_concrete_S3_controls"] != "YES_ON_Q01_Q02" or any(s[key]["parallel_endpoint_on_concrete_S3_controls"] != "NO_ON_Q01_Q02" for key in ["L01", "L02", "L03"]):
        raise AssertionError("parallel strata")
    if any(row["signed_depth"] != "NO_FOUNDED_DEPTH" for row in strata):
        raise AssertionError("depth invented")

    if "CHOSEN_NOT_SELECTED" not in q["Q01"]["chosen_global_section"] or not q["Q01"]["metric_natural_X"].startswith("L04_ONLY"):
        raise AssertionError("round ruler promoted")
    if not q["Q02"]["metric_natural_X"].startswith("ALL_LAMBDA_GIVEN_UNORIENTED"):
        raise AssertionError("squashed orientation promoted")
    if q["Q01"]["parallel_X"] != "L04_ONLY" or q["Q02"]["parallel_X"] != "L04_ONLY":
        raise AssertionError("naturality/parallelism confusion")
    if q["Q02"]["scope"] != "OFF_SHELL_CONTROL":
        raise AssertionError("squashed on shell")
    if q["Q03"]["scope"] != "INCOMPLETE_DO_NOT_SPLICE" or q["Q04"]["pair_frame_bundle"] != "ABSENT":
        raise AssertionError("control splice")

    if any(h[key]["spatial_holonomy_lie_rank"] != "3" for key in ["Q01", "Q02", "GENERIC_HOMOGENEOUS"]):
        raise AssertionError("holonomy rank")
    if any(h[key]["parallel_X_lambda"] != "lambda=1" for key in h):
        raise AssertionError("parallel algebra")

    if g["G02"]["status"] != "DERIVED" or g["G03"]["status"] != "DERIVED_GIVEN_TYPED_PATH_AND_VERTICAL_RESETS":
        raise AssertionError("assembly demoted")
    if g["G04"]["status"] != "DERIVED_AS_ASSOCIATED_QUERY_BUNDLE_ON_REGULAR_METRIC":
        raise AssertionError("bundle/section confusion")
    if g["G07"]["scope"] != "Q01_Q02_L04_ONLY" or "CONDITIONAL" not in g["G07"]["status"]:
        raise AssertionError("endpoint selection")
    if "multiple arrows" not in g["G09"]["ruling"]:
        raise AssertionError("cut locus failure")
    if g["G10"]["status"] != "NOT_APPLICABLE_UNLESS_PAIR_DERIVED_FROM_DPHI":
        raise AssertionError("causal type imported")
    if g["G11"]["status"] != "OPEN_ABSENT" or g["G12"]["status"] != "OPEN_UNSELECTED":
        raise AssertionError("downstream promotion")

    if v["V01"]["status"] != "RETAIN_OPEN_CANDIDATE" or v["V03"]["status"] != "NOT_AUTHORIZED":
        raise AssertionError("variation promotion")
    if v["V05"]["status"] != "CONDITIONAL_EXTRA_RESTRICTION":
        raise AssertionError("parallelism premise hidden")

    if production.get("result") != "PASS" or production.get("algebra", {}).get("centralizer_dimensions") != {"L01": 1, "L02": 3, "L03": 1, "L04": 3}:
        raise AssertionError("production algebra")
    if production.get("algebra", {}).get("round_holonomy_rank") != 3 or production.get("algebra", {}).get("parallel_lambda") != 1:
        raise AssertionError("production holonomy")
    if any(production.get("authority_boundary", {}).values()) or production.get("rulings", {}).get("endpoint_premise") != "OPEN_NOT_FOUNDED":
        raise AssertionError("authority escape")
    if independent.get("result") != "PASS" or independent.get("counts", {}).get("checks") != 57:
        raise AssertionError("independent mismatch")
    if independent.get("rulings", {}).get("endpoint_requirement") != "CONDITIONAL_NOT_SELECTED":
        raise AssertionError("independent authority")


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
    completion = rows("COMPLETION_ASSEMBLY_ATLAS.tsv")
    controls = rows("CONCRETE_CONTROL_ASSEMBLY.tsv")
    strata = rows("LAMBDA_STRATUM_OUTCOMES.tsv")
    gates = rows("ASSEMBLY_GATE_OUTCOMES.tsv")
    holonomy = rows("HOMOGENEOUS_HOLONOMY_ATLAS.tsv")
    variation = rows("VARIATION_CONSEQUENCE_LEDGER.tsv")
    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
    contract = rows("FALSIFICATION_CONTRACT.tsv")
    validate_model(completion, controls, strata, gates, holonomy, variation, production, independent)
    validate_sources()
    if {r["catch_id"] for r in contract} != {f"C{i:02d}" for i in range(1, 27)}:
        raise AssertionError("contract coverage")

    def model(c=completion, q=controls, s=strata, g=gates, h=holonomy, v=variation, p=production, i=independent):
        return lambda: validate_model(c, q, s, g, h, v, p, i)

    catches = {}
    catches["C01"] = expect_failure(model(c=completion[:-1]))
    catches["C02"] = expect_failure(model(s=strata + [copy.deepcopy(strata[0])]))
    catches["C03"] = expect_failure(model(c=changed(completion, "completion_id", "FC01_BOUNDARY_BOUNDARY", "pair_bundle_status", "PASS_CONCRETE_METRIC")))
    catches["C04"] = expect_failure(model(g=changed(gates, "gate_id", "G02", "status", "FAIL_NONCOVARIANT")))
    catches["C05"] = expect_failure(model(g=changed(gates, "gate_id", "G04", "status", "DERIVED_GLOBAL_SELECTED_SECTION")))
    catches["C06"] = expect_failure(model(q=changed(controls, "control_id", "Q02", "parallel_X", "ALL_LAMBDA")))
    catches["C07"] = expect_failure(model(g=changed(gates, "gate_id", "G03", "status", "ENDPOINT_PATH_INDEPENDENT_ALL_LAMBDA")))
    bad_production = copy.deepcopy(production)
    bad_production["authority_boundary"]["lambda_selected"] = True
    catches["C08"] = expect_failure(model(p=bad_production))
    catches["C09"] = expect_failure(model(s=changed(strata, "stratum_id", "L02", "connected_stabilizer", "SO2_screen")))
    catches["C10"] = expect_failure(model(s=changed(strata, "stratum_id", "L01", "connected_lorentz_centralizer_dimension", "2")))
    catches["C11"] = expect_failure(model(s=changed(strata, "stratum_id", "L04", "connected_lorentz_centralizer_dimension", "1")))
    catches["C12"] = expect_failure(model(s=changed(strata, "stratum_id", "L02", "connected_lorentz_centralizer_dimension", "1")))
    catches["C13"] = expect_failure(model(h=changed(holonomy, "control", "Q01", "spatial_holonomy_lie_rank", "2")))
    catches["C14"] = expect_failure(model(s=changed(strata, "stratum_id", "L01", "parallel_endpoint_on_concrete_S3_controls", "YES_ON_Q01_Q02")))
    catches["C15"] = expect_failure(model(q=changed(controls, "control_id", "Q01", "metric_natural_X", "ALL_LAMBDA_METRIC_SELECTED")))
    catches["C16"] = expect_failure(model(q=changed(controls, "control_id", "Q02", "metric_natural_X", "ALL_LAMBDA_GIVEN_ORIENTED_RICCI_VECTOR")))
    catches["C17"] = expect_failure(model(q=changed(controls, "control_id", "Q02", "scope", "ON_SHELL_NATIVE")))
    catches["C18"] = expect_failure(model(g=changed(gates, "gate_id", "G09", "ruling", "Cut locus destroys bundle.")))
    catches["C19"] = expect_failure(model(c=changed(completion, "completion_id", "FC02_ONE_CAP_BOUNDARY", "global_join_status", "CAP_TANGENT_METRIC_DEGENERATES")))
    catches["C20"] = expect_failure(model(g=changed(gates, "gate_id", "G10", "status", "TYPED_PAIR_FAILS_AT_DPHI_NULL")))
    catches["C21"] = expect_failure(model(g=changed(gates, "gate_id", "G11", "status", "DERIVED_FROM_TRANSPORT")))
    catches["C22"] = expect_failure(model(g=changed(gates, "gate_id", "G12", "status", "SELECTED")))
    catches["C23"] = expect_failure(model(q=changed(controls, "control_id", "Q03", "scope", "COMPLETE_S3_CLOCK_BRANCH")))
    catches["C24"] = expect_failure(model(c=changed(completion, "completion_id", "FC07_PERIODIC_TORUS_BUNDLE", "pair_bundle_status", "PASS_SELECTED")))
    bad_independent = copy.deepcopy(independent)
    bad_independent["counts"]["checks"] = 56
    catches["C25"] = expect_failure(model(i=bad_independent))
    catches["C26"] = expect_failure(lambda: validate_sources(True))
    if len(catches) != 26 or set(catches.values()) != {"PASS"}:
        raise AssertionError("catch coverage")

    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(["catch_id", "result"])
        writer.writerows(sorted(catches.items()))

    result = {
        "schema": "udt-global-reciprocal-bundle-assembly-verification-1.0",
        "result": "PASS",
        "grade": production["grade"],
        "completion_classes": len(completion), "concrete_controls": len(controls),
        "lambda_strata": len(strata), "assembly_gates": len(gates), "holonomy_rows": len(holonomy),
        "variation_rows": len(variation), "production_checks": len(production["checks"]),
        "independent_checks": len(independent["checks"]), "catch_count": len(catches),
        "catch_proofs": catches, "maximum_conclusion": production["maximum_conclusion"],
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
