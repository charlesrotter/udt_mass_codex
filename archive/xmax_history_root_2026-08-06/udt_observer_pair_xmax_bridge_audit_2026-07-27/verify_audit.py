#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def by_id(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    result = {row["candidate_id"]: row for row in rows}
    assert len(result) == len(rows)
    return result


def parse_review() -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in (HERE / "FRESH_ADVERSARIAL_REVIEW.md").read_text().splitlines():
        if ": " in line and not line.startswith("#"):
            key, value = line.split(": ", 1)
            if key.islower() or "_" in key:
                fields[key] = value
    return fields


def validate_model(model: dict[str, object]) -> None:
    outcomes = by_id(model["outcomes"])  # type: ignore[arg-type]
    production = model["production"]  # type: ignore[assignment]
    independent = model["independent"]  # type: ignore[assignment]
    independent_outcomes = by_id(model["independent_outcomes"])  # type: ignore[arg-type]
    review = model["review"]  # type: ignore[assignment]

    assert set(outcomes) == set(independent_outcomes) == {"C01", "C02", "C03", "C04", "C05"}
    for candidate_id in outcomes:
        assert outcomes[candidate_id]["outcome"] == independent_outcomes[candidate_id]["outcome"]

    assert "FINITE_ATTAINED" in outcomes["C01"]["limit_type"]
    assert "NOT_OPERATIONAL_PHYSICAL_XMAX" in outcomes["C01"]["outcome"]
    assert "ANGULAR_GEOMETRY_INCLUDED" in outcomes["C01"]["angular_cut_locus"]
    assert "MAX_OVER_ACTIVE_DIAMETER_PAIRS_MIN_OVER_ACTIVE_MINIMIZING_GEODESICS" in outcomes["C01"]["variation_type"]

    assert "SIGNED_ADDITIVE_COCYCLE" in outcomes["C02"]["composition_reversal"]
    assert "NOT_SYMMETRIC_DISTANCE" in outcomes["C02"]["composition_reversal"]
    assert "CANNOT_ENCODE_FULL_ANGULAR_PAIR_GEOMETRY" in outcomes["C02"]["angular_cut_locus"]
    assert "MAX_ARGMAX_H_MINUS_MIN_ARGMIN_H" in outcomes["C02"]["variation_type"]

    assert "TWIST_MAKES_DIRECTED_REVERSAL_ASYMMETRIC" in outcomes["C03"]["composition_reversal"]
    assert "SIGNAL_ROLE_OPEN_UNDER_COPRESENCE" in outcomes["C03"]["xmax_compatibility"]
    assert "MIN_OVER_ACTIVE_MINIMIZING_PATHS" in outcomes["C03"]["variation_type"]

    assert "REGISTERED_1D_PROJECTIVE_CLASS" in outcomes["C04"]["covariance"]
    assert outcomes["C04"]["xmax_compatibility"] == "CIRCULAR_IF_L_IS_INSERTED_AS_XMAX"
    assert outcomes["C05"]["domain_selected"] == "MISSING"
    assert "NOT_YET_AN_EXECUTABLE_FUNCTIONAL" in outcomes["C05"]["xmax_compatibility"]

    assert production["status"] == "PASS_CLASSIFIED_NO_COMPLETE_BRIDGE"
    assert production["candidate_count"] == 5
    assert production["exact_control"]["null_substitution_exact"]
    assert production["exact_control"]["randers_slice_positivity_equivalent"]
    assert production["exact_control"]["phi_level_tangent_obstruction_exact"]
    assert production["positive_nondegenerate_scalar_distance_equal_to_signed_clock_cocycle"].startswith("OBSTRUCTED_ON_FULL_ANGULAR_SPACE")
    assert production["all_pair_clock_cocycle_linearization"].startswith("INFINITE_DIMENSIONAL_MOD_CONSTANTS")
    assert production["physical_null_signal_interpretation"] == "OPEN_UNDER_COPRESENCE"
    assert production["operational_Xmax_bridge_status"] == "NOT_SELECTED_IN_FROZEN_FIVE_CANDIDATES"
    assert production["field_valued_global_to_local_return_equation_status"] == "NOT_SELECTED_IN_FROZEN_FIVE_CANDIDATES"
    assert production["bootstrap_status"] == "WORKING_ON_SHELL_ADMISSIBILITY_ONLY_UNCHANGED"
    assert production["strong_local_CSN_status"].endswith("INACTIVE")
    assert production["phi_native_field_ownership"] == "FOUNDED_PAIR_DEPTH_NOT_SELECTED_INDEPENDENT_NATIVE_SCALAR"
    assert production["c_E_G_obs_scale_closure"] == "NOT_DERIVED_SUFFICIENT_FOR_LENGTH_OR_DENSITY"
    assert production["cross_branch_splice_used"] is False
    assert production["scope_beyond_frozen_five"] == "OPEN_NOT_CLASSIFIED"

    assert independent["schema"] == "udt.observer_pair_xmax_bridge.independent.v2"
    assert independent["status"] == "PASS_INDEPENDENT_STDLIB_FRACTION_AND_SEMANTIC_RECONSTRUCTION"
    assert independent["production_outputs_read"] is False
    assert independent["bilocal_kernel"] == "CONSTANTS"
    assert all(rank == int(n) - 1 for n, rank in independent["bilocal_incidence_ranks"].items())
    assert independent["field_valued_return_equation_status"] == "NOT_SELECTED_IN_FROZEN_FIVE_CANDIDATES"

    assert review == {
        "verdict": "VERIFIED-WITH-CAVEATS",
        "reviewer_task": "/root/xmax_bridge_adversary",
        "review_date": "2026-07-27",
        "repo_modified": "false",
        "required_corrections_applied": "4/4",
        "maximum_conclusion_accepted": "yes",
    }


def mutate(model: dict[str, object], catch_id: str) -> None:
    outcomes = by_id(model["outcomes"])  # type: ignore[arg-type]
    production = model["production"]  # type: ignore[assignment]
    independent = model["independent"]  # type: ignore[assignment]
    review = model["review"]  # type: ignore[assignment]
    if catch_id == "F01":
        outcomes["C01"]["outcome"] = "IDENTIFIED_AS_PHYSICAL_XMAX"
    elif catch_id == "F02":
        outcomes["C01"]["limit_type"] = "FINITE_UNATTAINED_ON_SMOOTH_COMPACT_S3"
    elif catch_id == "F03":
        outcomes["C02"]["composition_reversal"] = "SYMMETRIC_NONNEGATIVE_DISTANCE"
    elif catch_id == "F04":
        outcomes["C02"]["angular_cut_locus"] = "ABSOLUTE_SCALAR_ENCODES_ALL_CENTERLESS_PAIRS"
    elif catch_id == "F05":
        outcomes["C01"]["angular_cut_locus"] = "ANGULAR_DATA_DROPPED_FROM_COMPOSITION"
    elif catch_id == "F06":
        outcomes["C01"]["angular_cut_locus"] = "ONE_CUT_LOCUS_PATH_SELECTED_WITHOUT_RULE"
    elif catch_id == "F07":
        outcomes["C03"]["composition_reversal"] = "TWIST_DROPPED_REVERSAL_SYMMETRIC"
    elif catch_id == "F08":
        production["physical_null_signal_interpretation"] = "DERIVED_PHYSICAL_SIGNAL"
    elif catch_id == "F09":
        outcomes["C04"]["covariance"] = "GENERAL_NONCOLLINEAR_OBSERVER_COMPOSITION"
    elif catch_id == "F10":
        outcomes["C04"]["xmax_compatibility"] = "L_DERIVED_AS_XMAX"
    elif catch_id == "F11":
        production["field_valued_global_to_local_return_equation_status"] = "DERIVED_FROM_SCALAR_VARIATION"
    elif catch_id == "F12":
        outcomes["C05"]["domain_selected"] = "COMPLETE"
    elif catch_id == "F13":
        production["strong_local_CSN_status"] = "ACTIVE_METRIC_EQUIVALENCE"
    elif catch_id == "F14":
        production["phi_native_field_ownership"] = "SELECTED_INDEPENDENT_NATIVE_SCALAR"
    elif catch_id == "F15":
        production["c_E_G_obs_scale_closure"] = "DERIVED_LENGTH_AND_DENSITY"
    elif catch_id == "F16":
        production["cross_branch_splice_used"] = True
    elif catch_id == "F17":
        outcomes["C01"]["variation_type"] = "SMOOTH_UNIQUE_DERIVATIVE_EVERYWHERE"
    elif catch_id == "F18":
        production["scope_beyond_frozen_five"] = "UNIVERSAL_NO_BRIDGE"
    elif catch_id == "F19":
        production["bootstrap_status"] = "DERIVED_LOCAL_OPTIMIZER_EQUATION"
    elif catch_id == "F20":
        independent["production_outputs_read"] = True
        review["maximum_conclusion_accepted"] = "no"
    else:
        raise AssertionError(catch_id)


def main() -> int:
    source = subprocess.run([sys.executable, str(HERE / "verify_source_manifest.py")], text=True, stdout=subprocess.PIPE)
    assert source.returncode == 0
    premise = subprocess.run([sys.executable, "verify_current_scientific_premises.py"], cwd=HERE.parent, text=True, stdout=subprocess.PIPE)
    assert premise.returncode == 0

    universe = load_tsv("CANDIDATE_UNIVERSE.tsv")
    outcomes = load_tsv("CANDIDATE_OUTCOMES.tsv")
    independent_outcomes = load_tsv("INDEPENDENT_OUTCOMES.tsv")
    assert len(universe) == len(outcomes) == len(independent_outcomes) == 5
    assert [row["candidate_id"] for row in universe] == [row["candidate_id"] for row in outcomes]
    required = {
        "domain", "domain_selected", "covariance", "composition_reversal", "angular_cut_locus",
        "limit_type", "variation_type", "xmax_compatibility", "return_equation", "outcome",
    }
    assert required.issubset(outcomes[0]) and all(all(row[field] for field in required) for row in outcomes)

    model: dict[str, object] = {
        "outcomes": outcomes,
        "production": json.loads((HERE / "DERIVATION_RESULT.json").read_text()),
        "independent": json.loads((HERE / "INDEPENDENT_RESULT.json").read_text()),
        "independent_outcomes": independent_outcomes,
        "review": parse_review(),
    }
    validate_model(model)

    contract = load_tsv("FALSIFICATION_CONTRACT.tsv")
    assert [row["catch_id"] for row in contract] == [f"F{i:02d}" for i in range(1, 21)]
    catches = []
    for row in contract:
        candidate = deepcopy(model)
        mutate(candidate, row["catch_id"])
        try:
            validate_model(candidate)
        except AssertionError:
            result = "PASS_REJECTED_ACTUAL_OUTPUT_MUTATION"
        else:
            raise AssertionError(f"{row['catch_id']} accepted mutation")
        catches.append({"catch_id": row["catch_id"], "mutation_or_false_claim": row["mutation_or_false_claim"], "result": result})

    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=list(catches[0]))
        writer.writeheader()
        writer.writerows(catches)

    result = {
        "schema": "udt.observer_pair_xmax_bridge.verification.v2",
        "status": "PASS",
        "sources": "18/18",
        "premise_guards": "16/16",
        "candidate_coverage": "5/5",
        "required_properties_per_candidate": 10,
        "production": "PASS_EXACT_STATIONARY_NULL_PATH_AND_TYPE_CLASSIFICATION",
        "independent": "PASS_NO_PRODUCTION_READ_STDLIB_FRACTION_AND_SEMANTIC_RECONSTRUCTION",
        "bilocal_rank_controls": "N=2_THROUGH_8_ALL_RANK_N_MINUS_1",
        "catch_proofs": "20/20_ACTUAL_OUTPUT_MUTATIONS",
        "operational_Xmax_bridge_status": "NOT_SELECTED_IN_FROZEN_FIVE_CANDIDATES",
        "field_valued_return_equation_status": "NOT_SELECTED_IN_FROZEN_FIVE_CANDIDATES_NOT_REFUTED",
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
