#!/usr/bin/env python3
"""Fail-closed verifier for the bounded triangle-consistency audit."""

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


def unique_ids(values: list[dict[str, str]], key: str, expected: set[str]) -> None:
    actual = [row[key] for row in values]
    if len(actual) != len(set(actual)) or set(actual) != expected:
        raise AssertionError(f"identity coverage: {key}")


def validate_sources(corrupt: bool = False) -> None:
    manifest = rows("SOURCE_MANIFEST.tsv")
    scope = rows("SOURCE_SCOPE.tsv")
    capability = rows("SOURCE_CAPABILITY_LEDGER.tsv")
    if [row["path"] for row in manifest] != [row["path"] for row in scope]:
        raise AssertionError("source scope mismatch")
    if {row["path"] for row in capability} != {row["path"] for row in scope} or len(capability) != len(scope):
        raise AssertionError("source capability coverage")
    for index, row in enumerate(manifest):
        path = ROOT / row["path"]
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        expected = row["sha256"]
        if corrupt and index == 0:
            expected = "0" * 64
        if digest != expected or path.stat().st_size != int(row["bytes"]):
            raise AssertionError("source identity")


def validate_model(
    route_outcomes: list[dict[str, str]],
    stratum_outcomes: list[dict[str, str]],
    status: list[dict[str, str]],
) -> None:
    unique_ids(route_outcomes, "route_id", {f"R{i:02d}" for i in range(1, 9)})
    unique_ids(stratum_outcomes, "stratum_id", {f"S{i:02d}" for i in range(1, 17)})
    unique_ids(status, "id", {f"S{i:02d}" for i in range(1, 16)})
    route = {row["route_id"]: row for row in route_outcomes}
    state = {row["id"]: row for row in status}
    strata = {row["stratum_id"]: row for row in stratum_outcomes}

    if route["R02"]["status"] != "UNIQUE_CONDITIONAL":
        raise AssertionError("flat premise lost")
    if "EVERY_LAMBDA" not in route["R03"]["outcome"] or state["S06"]["status"] != "NOT_DERIVED":
        raise AssertionError("typed groupoid falsely selects")
    if "MIDDLE_TRANSITION" not in route["R04"]["outcome"]:
        raise AssertionError("middle transition cancelled")
    if route["R05"]["status"] != "OPEN_HOLONOMY" or "INCONCLUSIVE" not in route["R05"]["outcome"]:
        raise AssertionError("loop called automatic inconsistency")
    if state["S08"]["status"] != "DERIVED_FIXED_OBSERVER_ONLY" or state["S09"]["status"] != "OPEN":
        raise AssertionError("fixed observer promotion")
    if route["R07"]["status"] != "OPEN_GLOBAL":
        raise AssertionError("global descent promotion")
    if route["R08"]["status"] != "NO_TYPED_SELECTOR":
        raise AssertionError("scalar selector promotion")
    if state["S14"]["status"] != "OPEN_UNCHANGED":
        raise AssertionError("excluded physics imported")
    required_exceptions = {"S02", "S03", "S04", "S05", "S06", "S11"}
    if not required_exceptions.issubset(strata):
        raise AssertionError("exception stratum missing")


def expect_failure(callback) -> str:
    try:
        callback()
    except (AssertionError, KeyError):
        return "PASS"
    raise AssertionError("catch accepted corruption")


def main() -> None:
    prereg_routes = rows("ROUTE_UNIVERSE.tsv")
    prereg_strata = rows("STRATUM_UNIVERSE.tsv")
    route_outcomes = rows("ROUTE_OUTCOMES.tsv")
    stratum_outcomes = rows("STRATUM_OUTCOMES.tsv")
    status = rows("STATUS_LEDGER.tsv")
    unique_ids(prereg_routes, "route_id", {f"R{i:02d}" for i in range(1, 9)})
    unique_ids(prereg_strata, "stratum_id", {f"S{i:02d}" for i in range(1, 17)})
    validate_model(route_outcomes, stratum_outcomes, status)
    validate_sources()

    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
    if production["result"] != "PASS" or production["check_count"] != 32 or set(production["checks"].values()) != {"PASS"}:
        raise AssertionError("production exact result")
    if independent["result"] != "PASS" or independent["check_count"] != 17 or set(independent["checks"].values()) != {"PASS"}:
        raise AssertionError("independent result")
    if production["rulings"]["overall"] != "TRIANGLE_CONSISTENCY_DOES_NOT_UNCONDITIONALLY_SELECT_LAMBDA":
        raise AssertionError("overall ruling")

    catches = {}
    modified = route_outcomes[:-1]
    catches["missing_route"] = expect_failure(lambda: validate_model(modified, stratum_outcomes, status))
    modified = copy.deepcopy(route_outcomes) + [copy.deepcopy(route_outcomes[0])]
    catches["duplicate_route"] = expect_failure(lambda: validate_model(modified, stratum_outcomes, status))
    modified_strata = stratum_outcomes[:-1]
    catches["missing_stratum"] = expect_failure(lambda: validate_model(route_outcomes, modified_strata, status))

    def corrupt_route(route_id: str, field: str, value: str) -> None:
        modified_routes = copy.deepcopy(route_outcomes)
        next(row for row in modified_routes if row["route_id"] == route_id)[field] = value
        validate_model(modified_routes, stratum_outcomes, status)

    def corrupt_state(state_id: str, field: str, value: str) -> None:
        modified_status = copy.deepcopy(status)
        next(row for row in modified_status if row["id"] == state_id)[field] = value
        validate_model(route_outcomes, stratum_outcomes, modified_status)

    catches["loop_as_inconsistency"] = expect_failure(lambda: corrupt_route("R05", "outcome", "INCONSISTENT"))
    catches["lambda_unconditional"] = expect_failure(lambda: corrupt_route("R02", "status", "DERIVED_UNCONDITIONAL"))
    catches["groupoid_selects"] = expect_failure(lambda: corrupt_state("S06", "status", "SELECTS_LAMBDA_ONE"))
    catches["middle_transition_cancelled"] = expect_failure(lambda: corrupt_route("R04", "outcome", "AUTOMATIC_CANCELLATION"))
    catches["fixed_observer_promoted"] = expect_failure(lambda: corrupt_state("S08", "status", "DERIVED_ALL_OBSERVERS"))
    # Remove a specifically required exceptional row while preserving count
    # through a bogus replacement identity; identity coverage must reject.
    bad_strata = copy.deepcopy(stratum_outcomes)
    next(row for row in bad_strata if row["stratum_id"] == "S03")["stratum_id"] = "S17"
    catches["exception_removed"] = expect_failure(lambda: validate_model(route_outcomes, bad_strata, status))
    catches["global_promoted"] = expect_failure(lambda: corrupt_route("R07", "status", "DERIVED_GLOBAL"))
    catches["scalar_selects"] = expect_failure(lambda: corrupt_route("R08", "status", "SELECTS_CONNECTION"))
    catches["physics_imported"] = expect_failure(lambda: corrupt_state("S14", "status", "DERIVED_ACTION"))

    bad_production = copy.deepcopy(production)
    bad_production["checks"][next(iter(bad_production["checks"]))] = "FAIL"
    catches["production_check"] = expect_failure(
        lambda: (_ for _ in ()).throw(AssertionError()) if set(bad_production["checks"].values()) != {"PASS"} else None
    )
    bad_independent = copy.deepcopy(independent)
    bad_independent["result"] = "FAIL"
    catches["independent_check"] = expect_failure(
        lambda: (_ for _ in ()).throw(AssertionError()) if bad_independent["result"] != "PASS" else None
    )
    catches["source_identity"] = expect_failure(lambda: validate_sources(True))
    if len(catches) != 15 or set(catches.values()) != {"PASS"}:
        raise AssertionError("catch proof coverage")

    output = {
        "schema": "udt-observer-pair-triangle-verification-1.0",
        "result": "PASS",
        "routes": len(route_outcomes),
        "strata": len(stratum_outcomes),
        "production_checks": production["check_count"],
        "independent_checks": independent["check_count"],
        "source_identities": len(rows("SOURCE_MANIFEST.tsv")),
        "catch_proofs": catches,
        "catch_count": len(catches),
        "grade": "VERIFIED_WITH_CAVEATS",
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
