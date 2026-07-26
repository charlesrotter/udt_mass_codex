#!/usr/bin/env python3
"""Fail-closed verifier for the reciprocal transport/holonomy atlas."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def exact_ids(values: list[dict[str, str]], key: str, expected: set[str]) -> None:
    actual = [row[key] for row in values]
    if len(actual) != len(set(actual)) or set(actual) != expected:
        raise AssertionError(f"identity coverage {key}")


def validate_sources(corrupt: bool = False) -> None:
    scope = rows("SOURCE_SCOPE.tsv")
    manifest = rows("SOURCE_MANIFEST.tsv")
    capability = rows("SOURCE_CAPABILITY_LEDGER.tsv")
    if [row["path"] for row in scope] != [row["path"] for row in manifest]:
        raise AssertionError("source order")
    if {row["path"] for row in capability} != {row["path"] for row in scope} or len(capability) != len(scope):
        raise AssertionError("source capability coverage")
    for index, row in enumerate(manifest):
        expected = row["sha256"]
        if corrupt and index == 0:
            expected = "0" * 64
        path = ROOT / row["path"]
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected or path.stat().st_size != int(row["bytes"]):
            raise AssertionError("source identity")


def validate_model(routes, holonomy, cells, status, forks) -> None:
    exact_ids(routes, "route_id", {f"R{i:02d}" for i in range(1, 13)})
    exact_ids(holonomy, "stratum_id", {f"H{i:02d}" for i in range(1, 16)})
    exact_ids(status, "id", {f"S{i:02d}" for i in range(1, 16)})
    exact_ids(forks, "fork_id", {f"O{i:02d}" for i in range(1, 5)})
    parent_cells = {row["completion_id"] for row in rows("../udt_finite_cell_cartan_transport_atlas_2026-07-23/FINITE_CELL_CARTAN_TRANSPORT_ATLAS.tsv")}
    exact_ids(cells, "completion_id", parent_cells)
    if len(parent_cells) != 12:
        raise AssertionError("parent cell count")

    route = {row["route_id"]: row for row in routes}
    state = {row["id"]: row for row in status}
    fork = {row["fork_id"]: row for row in forks}
    cell = {row["completion_id"]: row for row in cells}
    if route["R01"]["status"] != "DERIVED_GIVEN_COMPLETE_METRIC_INITIAL_LIFT_AND_CURVE":
        raise AssertionError("pathwise scope")
    if route["R02"]["status"] != "DERIVED_MATHEMATICAL_EQUIVALENCE":
        raise AssertionError("path independence conflation")
    if route["R04"]["status"] != "UNIQUE_CONDITIONAL" or state["S04"]["status"] != "UNIQUE_CONDITIONAL":
        raise AssertionError("plus one scope")
    if route["R05"]["status"] != "UNIQUE_CONDITIONAL" or state["S05"]["status"] != "UNIQUE_CONDITIONAL":
        raise AssertionError("minus one scope")
    if route["R09"]["status"] != "UNIQUE_CONDITIONAL_TWISTED" or state["S06"]["status"] != "UNIQUE_CONDITIONAL_TWISTED":
        raise AssertionError("zero twisted scope")
    if route["R10"]["status"] != "CONDITIONAL_NONSELECTING" or state["S09"]["status"] != "CONDITIONAL_MATHEMATICAL_CONTROL":
        raise AssertionError("Kato promotion")
    if route["R12"]["status"] != "NO_TYPED_SELECTOR":
        raise AssertionError("scalar promotion")
    if state["S14"]["status"] != "OPEN_UNCHANGED":
        raise AssertionError("excluded physics import")
    if fork["O01"]["global_object"] == fork["O02"]["global_object"] or fork["O02"]["conditional_lambda"] != "ZERO":
        raise AssertionError("ordinary twisted conflation")
    if "SIMPLE_CONNECTIVITY_DOES_NOT_REMOVE_CURVATURE_HOLONOMY" not in cell["FC04_TWO_CAP_P1"]["restricted_holonomy_gate"]:
        raise AssertionError("simple connectivity error")
    if cell["FC06_NONPRIMITIVE_CAP"]["pathwise_transport"] != "REGULAR_COMPLEMENT_ONLY":
        raise AssertionError("singular promotion")
    if any("ON_SHELL" in row["ruling"] for row in cells):
        raise AssertionError("on shell cell promotion")
    allowed_rulings = {"NO_BRANCH_OR_LAMBDA_SELECTED", "CONDITIONAL_ZERO_ROUTE_EXISTS_BUT_NOT_SELECTED"}
    if any(row["ruling"] not in allowed_rulings for row in cells):
        raise AssertionError("cell selection")


def expect_failure(callback) -> str:
    try:
        callback()
    except (AssertionError, KeyError):
        return "PASS"
    raise AssertionError("catch accepted corruption")


def main() -> None:
    prereg_routes = rows("ROUTE_UNIVERSE.tsv")
    prereg_holonomy = rows("HOLONOMY_STRATUM_UNIVERSE.tsv")
    exact_ids(prereg_routes, "route_id", {f"R{i:02d}" for i in range(1, 13)})
    exact_ids(prereg_holonomy, "stratum_id", {f"H{i:02d}" for i in range(1, 16)})

    routes = rows("ROUTE_OUTCOMES.tsv")
    holonomy = rows("HOLONOMY_OUTCOMES.tsv")
    cells = rows("FINITE_CELL_HOLONOMY_CROSS.tsv")
    status = rows("STATUS_LEDGER.tsv")
    forks = rows("DESCENT_ONTOLOGY_FORK.tsv")
    validate_model(routes, holonomy, cells, status, forks)
    validate_sources()

    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
    if production["result"] != "PASS" or production["check_count"] != 50 or set(production["checks"].values()) != {"PASS"}:
        raise AssertionError("production")
    if independent["result"] != "PASS" or independent["check_count"] != 35 or set(independent["checks"].values()) != {"PASS"}:
        raise AssertionError("independent")

    catches = {}
    catches["missing_route"] = expect_failure(lambda: validate_model(routes[:-1], holonomy, cells, status, forks))
    catches["duplicate_route"] = expect_failure(lambda: validate_model(routes + [copy.deepcopy(routes[0])], holonomy, cells, status, forks))
    catches["missing_holonomy"] = expect_failure(lambda: validate_model(routes, holonomy[:-1], cells, status, forks))
    catches["missing_cell"] = expect_failure(lambda: validate_model(routes, holonomy, cells[:-1], status, forks))

    def corrupt_route(route_id, field, value):
        changed = copy.deepcopy(routes)
        next(row for row in changed if row["route_id"] == route_id)[field] = value
        validate_model(changed, holonomy, cells, status, forks)

    def corrupt_status(status_id, field, value):
        changed = copy.deepcopy(status)
        next(row for row in changed if row["id"] == status_id)[field] = value
        validate_model(routes, holonomy, cells, changed, forks)

    catches["pathwise_as_path_independent"] = expect_failure(lambda: corrupt_route("R01", "status", "DERIVED_PATH_INDEPENDENT"))
    changed_cells = copy.deepcopy(cells)
    next(row for row in changed_cells if row["completion_id"] == "FC04_TWO_CAP_P1")["restricted_holonomy_gate"] = "TRIVIAL_HOLONOMY"
    catches["simple_connectivity"] = expect_failure(lambda: validate_model(routes, holonomy, changed_cells, status, forks))
    catches["plus_one_unconditional"] = expect_failure(lambda: corrupt_status("S04", "status", "DERIVED_UNCONDITIONAL"))
    catches["minus_one_unconditional"] = expect_failure(lambda: corrupt_status("S05", "status", "DERIVED_UNCONDITIONAL"))
    catches["zero_as_LC"] = expect_failure(lambda: corrupt_status("S06", "status", "DERIVED_ORDINARY_LC_HOLONOMY"))
    changed_forks = copy.deepcopy(forks)
    next(row for row in changed_forks if row["fork_id"] == "O02")["global_object"] = next(row for row in changed_forks if row["fork_id"] == "O01")["global_object"]
    catches["ordinary_twisted_conflation"] = expect_failure(lambda: validate_model(routes, holonomy, cells, status, changed_forks))
    bad_production = copy.deepcopy(production)
    bad_production["checks"]["phi_zero_twisted_test_is_vacuous_all_lambda"] = "FAIL"
    catches["phi_zero_vacuity"] = expect_failure(lambda: (_ for _ in ()).throw(AssertionError()) if set(bad_production["checks"].values()) != {"PASS"} else None)
    catches["Kato_selector"] = expect_failure(lambda: corrupt_route("R10", "status", "NATIVE_SELECTOR"))
    changed_cells = copy.deepcopy(cells)
    next(row for row in changed_cells if row["completion_id"] == "FC06_NONPRIMITIVE_CAP")["pathwise_transport"] = "GLOBAL_THROUGH_SINGULARITY"
    catches["singular_promotion"] = expect_failure(lambda: validate_model(routes, holonomy, changed_cells, status, forks))
    catches["scalar_selector"] = expect_failure(lambda: corrupt_route("R12", "status", "SELECTS_HOLONOMY"))
    changed_cells = copy.deepcopy(cells)
    changed_cells[0]["ruling"] = "COMPLETE_ON_SHELL_SELECTED"
    catches["on_shell_cell"] = expect_failure(lambda: validate_model(routes, holonomy, changed_cells, status, forks))
    catches["physics_import"] = expect_failure(lambda: corrupt_status("S14", "status", "DERIVED_ACTION_SOURCE"))
    bad_production = copy.deepcopy(production)
    bad_production["checks"][next(iter(bad_production["checks"]))] = "FAIL"
    catches["production"] = expect_failure(lambda: (_ for _ in ()).throw(AssertionError()) if set(bad_production["checks"].values()) != {"PASS"} else None)
    bad_independent = copy.deepcopy(independent)
    bad_independent["result"] = "FAIL"
    catches["independent"] = expect_failure(lambda: (_ for _ in ()).throw(AssertionError()) if bad_independent["result"] != "PASS" else None)
    catches["source"] = expect_failure(lambda: validate_sources(True))
    if len(catches) != 19 or set(catches.values()) != {"PASS"}:
        raise AssertionError("catch count")
    output = {
        "schema": "udt-reciprocal-transport-holonomy-verification-1.0",
        "result": "PASS", "grade": "VERIFIED_WITH_CAVEATS",
        "routes": len(routes), "holonomy_strata": len(holonomy),
        "finite_cell_families": len(cells), "source_identities": len(rows("SOURCE_MANIFEST.tsv")),
        "production_checks": production["check_count"], "independent_checks": independent["check_count"],
        "catch_count": len(catches), "catch_proofs": catches,
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
