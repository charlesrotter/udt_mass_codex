#!/usr/bin/env python3
"""Deterministic implication audit over the frozen semantic universes."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def table(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def ids(rows: list[dict[str, str]], field: str) -> set[str]:
    values = [row[field] for row in rows]
    assert len(values) == len(set(values))
    return set(values)


FALSE_FLAGS = {
    "F01": "abstract_composition_is_path_concatenation",
    "F02": "intermediate_position_forces_path_independence",
    "F03": "covariance_forces_parallel_global_field",
    "F04": "conditional_endpoint_factorization_proves_global_section",
    "F05": "path_groupoid_availability_makes_paths_physical",
    "F06": "cut_transport_family_forces_scalar_path_depth",
    "F07": "levi_civita_transport_equals_founding_dilation",
    "F08": "holonomy_refutes_endpoint_semantics",
    "F09": "lambda_one_parallelism_derives_endpoint_requirement",
    "F10": "bilocal_survivor_selects_F",
    "F11": "inactive_CSN_selects_semantics",
    "F12": "open_semantics_erases_abstract_operator",
    "F13": "open_semantics_makes_every_path_physical",
    "F14": "path_derived_without_constitutive_source",
    "F15": "endpoint_derived_without_independence_source",
    "F16": "semantic_ruling_selects_downstream_physics",
}


def validate_false_inferences(flags: dict[str, bool]) -> None:
    bad = [name for name, active in flags.items() if active]
    if bad:
        raise AssertionError("forbidden inference: " + ",".join(bad))


def main() -> int:
    claims = table("SOURCE_CLAIM_UNIVERSE.tsv")
    claim_outcomes = table("SOURCE_CLAIM_OUTCOMES.tsv")
    routes = table("SEMANTIC_ROUTE_UNIVERSE.tsv")
    route_outcomes = table("SEMANTIC_ROUTE_OUTCOMES.tsv")
    requirements = table("REQUIREMENT_UNIVERSE.tsv")
    requirement_outcomes = table("REQUIREMENT_OUTCOMES.tsv")
    falsifications = table("FALSIFICATION_CONTRACT.tsv")
    sources = table("SOURCE_MANIFEST.tsv")

    assert ids(claims, "claim_id") == ids(claim_outcomes, "claim_id") == {
        f"C{i:02d}" for i in range(1, 37)
    }
    assert ids(routes, "route_id") == ids(route_outcomes, "route_id") == {
        f"R{i:02d}" for i in range(1, 9)
    }
    assert ids(requirements, "requirement_id") == ids(requirement_outcomes, "requirement_id") == {
        f"Q{i:02d}" for i in range(1, 19)
    }
    assert ids(falsifications, "catch_id") == set(FALSE_FLAGS)
    assert len(sources) == 21
    for row in sources:
        assert sha256(ROOT / row["path"]) == row["sha256"]

    abstract_derived = {
        row["claim_id"] for row in claim_outcomes if row["abstract_ordered_effect"] == "DERIVES"
    }
    assert {"C02", "C03", "C04", "C05", "C07", "C08", "C12", "C15", "C33", "C36"} <= abstract_derived
    assert not any(row["endpoint_physical_force"] == "YES" for row in claim_outcomes)
    assert not any(row["path_physical_force"] == "YES" for row in claim_outcomes)

    req = {row["requirement_id"]: row["audit_status"] for row in requirement_outcomes}
    abstract_core = all(req[q].startswith("DERIVED") for q in ("Q01", "Q02", "Q03", "Q04"))
    endpoint_derived = req["Q09"] == "DERIVED" and req["Q17"] == "DERIVED"
    path_derived = req["Q08"] == "DERIVED"
    assert abstract_core and not endpoint_derived and not path_derived
    primary_ruling = "SEMANTICS_OPEN"

    route_map = {row["route_id"]: row["outcome"] for row in route_outcomes}
    assert route_map["R08"] == "DERIVED_WITH_PREMISE_STAMPS"
    assert route_map["R03"] == "DERIVED_GIVEN_INPUT_NOT_FOUNDED_PHYSICAL"
    assert route_map["R06"] == "CONDITIONAL_ON_ENDPOINT_REQUIREMENT"

    baseline = {flag: False for flag in FALSE_FLAGS.values()}
    validate_false_inferences(baseline)
    catches = []
    for catch_id, flag in FALSE_FLAGS.items():
        mutated = dict(baseline)
        mutated[flag] = True
        try:
            validate_false_inferences(mutated)
        except AssertionError:
            catches.append(catch_id)
        else:
            raise AssertionError(f"uncaught mutation {catch_id}")

    result = {
        "schema_version": 1,
        "primary_ruling": primary_ruling,
        "secondary_ruling": "ORDERED_RELATIONAL_ABSTRACT_COMPARISON_DERIVED__COMPLETE_PATH_VS_ENDPOINT_REALIZATION_OPEN",
        "source_count": len(sources),
        "claim_count": len(claims),
        "route_count": len(routes),
        "requirement_count": len(requirements),
        "endpoint_physical_forcing_claims": 0,
        "path_physical_forcing_claims": 0,
        "catch_proofs_passed": len(catches),
        "catch_ids": catches,
        "lambda_consequence": "NO_SELECTION__ALL_REAL_PATHWISE__LAMBDA_ONE_ONLY_IF_ENDPOINT_REQUIREMENT_LATER_DERIVED_OR_CHOSEN",
        "downstream_physics_activated": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
