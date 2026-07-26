#!/usr/bin/env python3
"""Fail-closed verifier for calibrated reciprocal-readout descent."""

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


def exact_ids(values, key, expected):
    actual = [row[key] for row in values]
    if len(actual) != len(set(actual)) or set(actual) != expected:
        raise AssertionError(f"identity coverage {key}")


def validate_sources(corrupt=False):
    scope, manifest, capability = rows("SOURCE_SCOPE.tsv"), rows("SOURCE_MANIFEST.tsv"), rows("SOURCE_CAPABILITY_LEDGER.tsv")
    if [row["path"] for row in scope] != [row["path"] for row in manifest]:
        raise AssertionError("source order")
    if {row["path"] for row in capability} != {row["path"] for row in scope} or len(capability) != len(scope):
        raise AssertionError("source capability")
    for index, row in enumerate(manifest):
        expected = "0" * 64 if corrupt and index == 0 else row["sha256"]
        path = ROOT / row["path"]
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected or path.stat().st_size != int(row["bytes"]):
            raise AssertionError("source identity")


def validate_model(routes, strata, status, pair_classes, blocks, forks):
    exact_ids(routes, "route_id", {f"R{i:02d}" for i in range(1, 13)})
    exact_ids(strata, "stratum_id", {f"Q{i:02d}" for i in range(1, 18)})
    exact_ids(status, "id", {f"S{i:02d}" for i in range(1, 16)})
    exact_ids(forks, "fork_id", {f"A{i:02d}" for i in range(1, 5)})
    if len(pair_classes) != 5 or len({row["class"] for row in pair_classes}) != 5:
        raise AssertionError("pair class coverage")
    if {row["lambda_class"] for row in blocks} != {"GENERIC_NOT_PLUS_OR_MINUS_ONE", "ZERO", "PLUS_ONE", "MINUS_ONE"} or len(blocks) != 4:
        raise AssertionError("complete block coverage")
    route = {row["route_id"]: row for row in routes}
    state = {row["id"]: row for row in status}
    fork = {row["fork_id"]: row for row in forks}
    stratum = {row["stratum_id"]: row for row in strata}
    if route["R01"]["status"] != "DERIVED_GIVEN_FOUNDING_LOCAL_READOUT":
        raise AssertionError("founding scope")
    if route["R06"]["status"] != "DERIVED_NO_GO" or state["S05"]["status"] != "OBSTRUCTED_NO_LORENTZIAN_SOLUTION":
        raise AssertionError("simultaneous solution invented")
    if route["R05"]["status"] != "DERIVED_NO_REPAIR" or state["S04"]["status"] != "NO_ENLARGEMENT":
        raise AssertionError("conformal repair")
    if route["R07"]["status"] != "CONDITIONAL" or state["S06"]["status"] != "CONDITIONAL_EXISTS":
        raise AssertionError("mixed promotion")
    if route["R09"]["status"] != "DERIVED_NONSELECTION" or state["S09"]["status"] != "OBSERVED_SCALE_NONSELECTING":
        raise AssertionError("calibration alignment conflation")
    if route["R10"]["status"] != "OPEN_GLOBAL" or "ALL_LAMBDA" not in route["R10"]["outcome"]:
        raise AssertionError("ordinary family removed")
    if route["R11"]["status"] != "CONDITIONAL_NONMETRIC_OR_MIXED" or "NOT_ALIGNED_PHYSICAL_LEVI_CIVITA" not in state["S11"]["exact_scope_or_premises"].upper():
        raise AssertionError("internal normalizer promoted")
    if route["R12"]["status"] != "NO_TYPED_SELECTOR" or state["S13"]["status"] != "NO_SOLDER_SELECTOR":
        raise AssertionError("scalar selector")
    if state["S14"]["status"] != "OPEN_UNCHANGED":
        raise AssertionError("physics import")
    if stratum["Q17"]["status"] != "DERIVED_ZERO_DEPTH_GUARD":
        raise AssertionError("zero depth selection")
    if fork["A01"]["current_authority"] != "DERIVED_IN_FOUNDING_LOCAL_SLICE;GLOBAL_COMPLETE_EXTENSION_OPEN":
        raise AssertionError("founding promoted globally")
    if fork["A02"]["current_authority"] != "CONDITIONAL_MIXED_READOUT;PHYSICAL_SOLDER_OPEN":
        raise AssertionError("mixed promoted")


def expect_failure(callback):
    try:
        callback()
    except (AssertionError, KeyError):
        return "PASS"
    raise AssertionError("catch accepted corruption")


def main():
    exact_ids(rows("ROUTE_UNIVERSE.tsv"), "route_id", {f"R{i:02d}" for i in range(1, 13)})
    exact_ids(rows("READOUT_STRATUM_UNIVERSE.tsv"), "stratum_id", {f"Q{i:02d}" for i in range(1, 18)})
    routes, strata = rows("ROUTE_OUTCOMES.tsv"), rows("READOUT_OUTCOMES.tsv")
    status, pair_classes = rows("STATUS_LEDGER.tsv"), rows("PAIR_READOUT_CLASSIFICATION.tsv")
    blocks, forks = rows("COMPLETE_READOUT_BLOCKS.tsv"), rows("READOUT_AUTHORITY_FORK.tsv")
    validate_model(routes, strata, status, pair_classes, blocks, forks)
    validate_sources()
    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
    if production["result"] != "PASS" or production["check_count"] != 43 or set(production["checks"].values()) != {"PASS"}:
        raise AssertionError("production")
    if independent["result"] != "PASS" or independent["check_count"] != 23 or set(independent["checks"].values()) != {"PASS"}:
        raise AssertionError("independent")
    census = independent["bounded_integer_census"]
    if (census["self_adjoint_Lorentzian"], census["inverting_isometric_Lorentzian"], census["simultaneous"]) != (18, 18, 0):
        raise AssertionError("independent census")

    catches = {}
    catches["missing_route"] = expect_failure(lambda: validate_model(routes[:-1], strata, status, pair_classes, blocks, forks))
    catches["duplicate_route"] = expect_failure(lambda: validate_model(routes + [copy.deepcopy(routes[0])], strata, status, pair_classes, blocks, forks))
    catches["missing_stratum"] = expect_failure(lambda: validate_model(routes, strata[:-1], status, pair_classes, blocks, forks))

    def corrupt_route(rid, field, value):
        changed = copy.deepcopy(routes)
        next(row for row in changed if row["route_id"] == rid)[field] = value
        validate_model(changed, strata, status, pair_classes, blocks, forks)

    def corrupt_status(sid, field, value):
        changed = copy.deepcopy(status)
        next(row for row in changed if row["id"] == sid)[field] = value
        validate_model(routes, strata, changed, pair_classes, blocks, forks)

    catches["calibration_as_alignment"] = expect_failure(lambda: corrupt_route("R09", "status", "DERIVED_ALIGNMENT"))
    catches["c_cross_selector"] = expect_failure(lambda: corrupt_status("S09", "status", "SELECTS_B_ZERO"))
    catches["mixed_self_adjoint"] = expect_failure(lambda: corrupt_status("S06", "status", "DERIVED_SELF_ADJOINT"))
    catches["simultaneous_solution"] = expect_failure(lambda: corrupt_route("R06", "status", "DERIVED_EXISTS"))
    catches["conformal_repair"] = expect_failure(lambda: corrupt_route("R05", "status", "DERIVED_REPAIR"))
    changed_strata = copy.deepcopy(strata)
    next(row for row in changed_strata if row["stratum_id"] == "Q17")["status"] = "SELECTS_TWIST"
    catches["zero_depth"] = expect_failure(lambda: validate_model(routes, changed_strata, status, pair_classes, blocks, forks))
    catches["internal_as_LC"] = expect_failure(lambda: corrupt_route("R11", "status", "DERIVED_LEVI_CIVITA_HOLONOMY"))
    catches["ordinary_removed"] = expect_failure(lambda: corrupt_route("R10", "outcome", "ONLY_PLUS_MINUS"))
    catches["plus_minus_forced"] = expect_failure(lambda: corrupt_route("R10", "status", "DERIVED_SELECTED"))
    changed_forks = copy.deepcopy(forks)
    next(row for row in changed_forks if row["fork_id"] == "A02")["current_authority"] = "FOUNDING_FRAME"
    catches["mixed_promoted"] = expect_failure(lambda: validate_model(routes, strata, status, pair_classes, blocks, changed_forks))
    catches["scalar_selector"] = expect_failure(lambda: corrupt_route("R12", "status", "SELECTS_SOLDER"))
    catches["physics"] = expect_failure(lambda: corrupt_status("S14", "status", "DERIVED_ACTION"))
    bad_production = copy.deepcopy(production)
    bad_production["checks"][next(iter(bad_production["checks"]))] = "FAIL"
    catches["production"] = expect_failure(lambda: (_ for _ in ()).throw(AssertionError()) if set(bad_production["checks"].values()) != {"PASS"} else None)
    bad_independent = copy.deepcopy(independent)
    bad_independent["result"] = "FAIL"
    catches["independent"] = expect_failure(lambda: (_ for _ in ()).throw(AssertionError()) if bad_independent["result"] != "PASS" else None)
    catches["source"] = expect_failure(lambda: validate_sources(True))
    if len(catches) != 18 or set(catches.values()) != {"PASS"}:
        raise AssertionError("catch count")
    output = {
        "schema": "udt-calibrated-reciprocal-readout-verification-1.0",
        "result": "PASS", "grade": "VERIFIED_WITH_CAVEATS",
        "routes": len(routes), "readout_strata": len(strata),
        "production_checks": production["check_count"], "independent_checks": independent["check_count"],
        "independent_census": census, "source_identities": len(rows("SOURCE_MANIFEST.tsv")),
        "catch_count": len(catches), "catch_proofs": catches,
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
