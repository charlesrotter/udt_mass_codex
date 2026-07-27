#!/usr/bin/env python3
"""Fail-closed semantic/mechanical verifier and exercised catch-proofs."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def unique(items: list[dict[str, str]], key: str, count: int) -> dict[str, dict[str, str]]:
    values = [row[key] for row in items]
    if len(items) != count or len(set(values)) != count:
        raise AssertionError(f"{key} coverage {len(items)}/{len(set(values))}, expected {count}")
    return {row[key]: row for row in items}


def load() -> dict[str, object]:
    return {
        "candidates": rows("CANDIDATE_UNIVERSE.tsv"),
        "outcomes": rows("CANDIDATE_OUTCOMES.tsv"),
        "layers": rows("BUNDLE_LAYER_OUTCOMES.tsv"),
        "directions": rows("SEVEN_DIRECTION_CLASSIFICATION.tsv"),
        "status": rows("STATUS_LEDGER.tsv"),
        "manifest": rows("SOURCE_MANIFEST.tsv"),
        "production": json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8")),
        "independent": json.loads((HERE / "INDEPENDENT_RESULT.json").read_text(encoding="utf-8")),
    }


def verify(data: dict[str, object], *, check_files: bool = True) -> dict[str, int]:
    candidates = unique(data["candidates"], "candidate_id", 24)
    outcomes = unique(data["outcomes"], "candidate_id", 24)
    layers = unique(data["layers"], "layer_id", 10)
    directions = unique(data["directions"], "direction_id", 7)
    status = unique(data["status"], "object", 15)
    manifest = unique(data["manifest"], "source_id", 16)
    production = data["production"]
    independent = data["independent"]

    if set(candidates) != set(outcomes):
        raise AssertionError("candidate outcome coverage mismatch")
    if any(row["representative_classification"] != "INEQUIVALENT_METRIC_DATA_AT_FIRST_JET" for row in directions.values()):
        raise AssertionError("extension direction silently gauged away")
    if any(row["finite_status"] != "FINITE_LIFT_OPEN" for row in directions.values()):
        raise AssertionError("finite lift silently selected")

    expected_ranks = {
        "metric_response": 10,
        "Lorentz_kernel": 6,
        "founded_affine_response_fiber": 7,
    }
    for key, value in expected_ranks.items():
        if production["ranks"][key] != value or independent["ranks"][key] != value:
            raise AssertionError(f"rank disagreement: {key}")
    if production["check_count"] != 31 or independent["check_count"] != 27:
        raise AssertionError("exact check count changed")
    if not production["finite_lift_control"]["different_second_metric_jet_for_nonzero_mixing"]:
        raise AssertionError("finite-lift countercontrol lost")
    if not independent["finite_lift_same_first_different_second"]:
        raise AssertionError("independent finite-lift countercontrol lost")

    required_outcomes = {
        "C03": "NOT_DERIVED",
        "C05": "SET_VALUED_OR_BRANCH_DEPENDENT",
        "C10": "UDT_DERIVED_AFFINE_RESPONSE_QUERY_BUNDLE",
        "C13": "CONDITIONAL_TWISTED_TRANSITION_NOT_LORENTZ",
        "C16": "METRIC_CANONICAL_MATHEMATICS_PHYSICAL_ROLE_OPEN",
        "C18": "AVAILABLE_CONDITIONAL_EXACT",
        "C22": "NOT_DERIVED",
        "C24": "NOT_DERIVED",
    }
    for candidate, expected in required_outcomes.items():
        if outcomes[candidate]["outcome"] != expected:
            raise AssertionError(f"candidate promotion/regression: {candidate}")

    if layers["L05"]["physical_UDT_status"] != "FINITE_COMPLETE_EXTENSION_OPEN":
        raise AssertionError("response bundle promoted to finite extension")
    if layers["L07"]["physical_UDT_status"] != "OPEN_PHYSICAL_COMPARISON_ROLE":
        raise AssertionError("Levi-Civita mathematics promoted to physical law")
    if layers["L10"]["physical_UDT_status"] != "OPEN":
        raise AssertionError("variation domain promoted")

    exact_statuses = {
        "finite_constant_generator_lift": "OPEN_NONUNIQUE_FROM_FIRST_RESPONSE",
        "complete_extension_section": "OPEN",
        "physical_comparison_functor": "OPEN",
        "variation_domain": "OPEN",
        "strong_local_CSN": "INACTIVE_CHALLENGED_NOT_DERIVED",
        "carrier_bootstrap_Xmax_action_source_boundary_mass_dynamics": "UNCHANGED_REGISTERED_LEVELS",
    }
    for item, expected in exact_statuses.items():
        if status[item]["status"] != expected:
            raise AssertionError(f"status promotion: {item}")

    if production["invariant_strata"]["ordered_pair_SO2"] != "ONE_PARAMETER_SCREEN_TRACE_FAMILY_LAMBDA_UNSELECTED":
        raise AssertionError("SO2 family falsely selected")
    if production["invariant_strata"]["full_Lorentz"] != "NO_RESPONSE_COMPATIBLE_WITH_FIXED_FOUNDED_MINUS_PLUS_PAIR":
        raise AssertionError("full Lorentz compatibility falsely claimed")

    if check_files:
        for row in manifest.values():
            path = ROOT / row["path"]
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != row["sha256"]:
                raise AssertionError(f"source manifest mismatch: {row['source_id']}")

    return {
        "candidates": len(candidates),
        "layers": len(layers),
        "directions": len(directions),
        "statuses": len(status),
        "sources": len(manifest),
    }


def catches(base: dict[str, object]) -> list[dict[str, str]]:
    results = []

    def exercise(name: str, mutate) -> None:
        trial = copy.deepcopy(base)
        mutate(trial)
        try:
            verify(trial, check_files=False)
        except AssertionError:
            results.append({"catch": name, "result": "REJECTED_AS_REQUIRED"})
            return
        raise AssertionError(f"catch escaped: {name}")

    exercise("missing_candidate", lambda d: d["outcomes"].pop())
    exercise("duplicate_candidate", lambda d: d["outcomes"].append(copy.deepcopy(d["outcomes"][0])))
    exercise("gauge_away_one_extension_direction", lambda d: d["directions"][0].update(representative_classification="REPRESENTATIVE_FREEDOM"))
    exercise("select_one_finite_lift", lambda d: d["directions"][0].update(finite_status="SELECTED"))
    exercise("erase_second_jet_countercontrol", lambda d: d["production"]["finite_lift_control"].update(different_second_metric_jet_for_nonzero_mixing=False))
    exercise("promote_Levi_Civita_to_physical_law", lambda d: next(r for r in d["layers"] if r["layer_id"] == "L07").update(physical_UDT_status="UDT_DERIVED_PHYSICAL_LAW"))
    exercise("select_geodesic_path", lambda d: next(r for r in d["outcomes"] if r["candidate_id"] == "C05").update(outcome="SELECTED_UNIQUE_PATH"))
    exercise("call_swap_Lorentz", lambda d: next(r for r in d["outcomes"] if r["candidate_id"] == "C13").update(outcome="FIXED_METRIC_LORENTZ_TRANSITION"))
    exercise("select_global_section", lambda d: next(r for r in d["outcomes"] if r["candidate_id"] == "C22").update(outcome="UDT_DERIVED"))
    exercise("promote_variation_domain", lambda d: next(r for r in d["status"] if r["object"] == "variation_domain").update(status="DERIVED"))
    exercise("promote_downstream_physics", lambda d: next(r for r in d["status"] if r["object"] == "carrier_bootstrap_Xmax_action_source_boundary_mass_dynamics").update(status="DERIVED"))
    exercise("select_SO2_lambda", lambda d: d["production"]["invariant_strata"].update(ordered_pair_SO2="UNIQUE_PLUS_ONE"))
    exercise("make_full_Lorentz_compatible", lambda d: d["production"]["invariant_strata"].update(full_Lorentz="COMPATIBLE"))
    exercise("lose_independent_rank", lambda d: d["independent"]["ranks"].update(founded_affine_response_fiber=6))
    exercise("lose_source_manifest_row", lambda d: d["manifest"].pop())
    return results


def main() -> None:
    data = load()
    counts = verify(data)
    catch_results = catches(data)
    print(json.dumps({
        "schema": "udt.native_reciprocal_comparison_bundle.verification.v1",
        "result": "PASS",
        "grade_ceiling": "VERIFIED_WITH_CAVEATS_NO_FRESH_MODEL_CONTEXT",
        "counts": counts,
        "production_checks": 31,
        "independent_checks": 27,
        "catch_proofs": len(catch_results),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
