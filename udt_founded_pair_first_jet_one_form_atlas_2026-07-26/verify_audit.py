#!/usr/bin/env python3
"""Fail-closed verifier for the founded-pair first-jet atlas."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXPECTED_IDS = {f"W{i:02d}" for i in range(1, 7)} | {f"U{i:02d}" for i in range(1, 9)} | {f"N{i:02d}" for i in range(1, 9)}


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def exact_ids(values, key, expected):
    actual = [row[key] for row in values]
    if len(actual) != len(set(actual)) or set(actual) != expected:
        raise AssertionError(f"identity coverage:{key}")


def validate_sources(corrupt=False):
    scope = rows("SOURCE_SCOPE.tsv")
    manifest = rows("SOURCE_MANIFEST.tsv")
    capability = rows("SOURCE_CAPABILITY_LEDGER.tsv")
    if [row["path"] for row in scope] != [row["path"] for row in manifest]:
        raise AssertionError("source order")
    if len(capability) != len(scope) or {row["path"] for row in capability} != {row["path"] for row in scope}:
        raise AssertionError("source capability")
    for index, row in enumerate(manifest):
        expected = "0" * 64 if corrupt and index == 0 else row["sha256"]
        path = ROOT / row["path"]
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected or path.stat().st_size != int(row["size"]):
            raise AssertionError("source identity")


def validate_model(basis, outcomes, reductions, status, production, independent):
    exact_ids(basis, "id", EXPECTED_IDS)
    exact_ids(outcomes, "id", EXPECTED_IDS)
    exact_ids(reductions, "id", {f"R{i:02d}" for i in range(1, 13)})
    if len(status) != 17 or len({row["object"] for row in status}) != 17:
        raise AssertionError("status coverage")
    basis_by_id = {row["id"]: row for row in basis}
    outcome = {row["id"]: row for row in outcomes}
    reduction = {row["id"]: row for row in reductions}
    state = {row["object"]: row for row in status}

    for identity in EXPECTED_IDS:
        if outcome[identity]["uses_screen_orientation"] != basis_by_id[identity]["uses_screen_orientation"]:
            raise AssertionError("orientation mismatch")
        if outcome[identity]["generic_closure"] != "NOT_UNIVERSALLY_CLOSED":
            raise AssertionError("false closure")
    if reduction["R02"]["dimension_or_rank"] != "22" or reduction["R03"]["dimension_or_rank"] != "13":
        raise AssertionError("basis ranks")
    if reduction["R04"]["dimension_or_rank"] != "11" or reduction["R05"]["dimension_or_rank"] != "6":
        raise AssertionError("discrete ranks")
    if reduction["R07"]["dimension_or_rank"] != "0" or reduction["R07"]["status"] != "REFUTED_IN_FROZEN_LINEAR_CLASS":
        raise AssertionError("closure promotion")
    if reduction["R08"]["status"] != "AVAILABLE_CONDITIONAL" or reduction["R09"]["status"] != "NOT_DERIVED":
        raise AssertionError("boost promotion")
    if reduction["R10"]["status"] != "CONDITIONAL_INACTIVE":
        raise AssertionError("CSN reactivation")
    if reduction["R11"]["dimension_or_rank"] != "0" or reduction["R11"]["status"] != "NO_ACTIVE_SELECTION":
        raise AssertionError("coefficient selected")
    if state["founded_phi_identity"]["status"] != "DERIVED_UNCHANGED":
        raise AssertionError("phi demoted")
    if state["boost_connection_omega"]["status"] != "METRIC_SKEW_PAIR_RAPIDITY_CONNECTION":
        raise AssertionError("boost identity")
    if state["historical_CSN_reciprocal_connection"]["status"] != "CONDITIONAL_INACTIVE_CURRENTLY":
        raise AssertionError("historical route")
    if state["lambda_Xmax_action_carrier_source_boundary_density_bootstrap_mass_dynamics"]["status"] != "OPEN_UNCHANGED":
        raise AssertionError("physics imported")

    required = {
        "candidate_map_rank_22",
        "SO2_representation_count_6_plus_8_plus_8",
        "O2_basis_rank_13",
        "n_flip_even_rank_11",
        "O2_and_n_even_rank_6",
        "closure_witness_rank_22",
        "closure_universal_nullity_zero",
        "omega_reconstructed_from_W01_W04_W05",
        "boost_generator_is_metric_skew",
        "founded_generator_is_metric_self_adjoint",
        "boost_and_founded_generators_are_distinct",
    }
    if production.get("result") != "PASS" or production.get("summary_check_count") != 42 or production.get("census_check_count") != 180:
        raise AssertionError("production result")
    if not required.issubset(production["checks"]) or set(production["checks"].values()) != {"PASS"}:
        raise AssertionError("production checks")
    expected_counts = {
        "pair_jet_components": 20,
        "SO2_one_form_basis": 22,
        "O2_one_form_basis": 13,
        "n_flip_even_basis": 11,
        "O2_and_n_flip_even_basis": 6,
        "closure_witness_samples": 4,
        "closure_matrix_rows": 24,
        "closure_rank": 22,
        "universally_closed_nonzero_combinations_in_witness_class": 0,
        "Taylor_constraint_checks": 168,
    }
    if production.get("counts") != expected_counts:
        raise AssertionError("production counts")
    expected_independent = {
        "basis_rank": 22,
        "O2_rank": 13,
        "n_flip_even_rank": 11,
        "O2_n_flip_even_rank": 6,
        "parity_checks": 22,
        "closure_samples": 6,
        "closure_rows": 36,
        "closure_rank": 22,
        "Taylor_constraint_checks": 252,
    }
    if independent.get("result") != "PASS" or independent.get("summary_check_count") != 29:
        raise AssertionError("independent result")
    if independent.get("counts") != expected_independent or set(independent["checks"].values()) != {"PASS"}:
        raise AssertionError("independent counts")
    for identity in EXPECTED_IDS:
        if production["parity"][identity] != outcome[identity]["n_flip_parity"]:
            raise AssertionError("parity table")


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
    basis = rows("ONE_FORM_BASIS.tsv")
    outcomes = rows("ONE_FORM_OUTCOMES.tsv")
    reductions = rows("REDUCTION_OUTCOMES.tsv")
    status = rows("STATUS_LEDGER.tsv")
    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    independent = json.loads((HERE / "INDEPENDENT_RESULT.json").read_text())
    validate_model(basis, outcomes, reductions, status, production, independent)
    validate_sources()

    def model(b=basis, o=outcomes, r=reductions, s=status, p=production, i=independent):
        return lambda: validate_model(b, o, r, s, p, i)

    catches = {}
    catches["missing_basis"] = expect_failure(model(b=basis[:-1]))
    catches["duplicate_basis"] = expect_failure(model(b=basis + [copy.deepcopy(basis[0])]))
    catches["bad_basis_rank"] = expect_failure(model(r=changed(reductions, "id", "R02", "dimension_or_rank", "21")))
    catches["bad_O2_rank"] = expect_failure(model(r=changed(reductions, "id", "R03", "dimension_or_rank", "14")))
    catches["bad_parity"] = expect_failure(model(o=changed(outcomes, "id", "W01", "n_flip_parity", "EVEN")))
    catches["false_closure"] = expect_failure(model(o=changed(outcomes, "id", "U01", "generic_closure", "UNIVERSALLY_CLOSED")))
    catches["closure_rank"] = expect_failure(model(r=changed(reductions, "id", "R07", "dimension_or_rank", "1")))
    catches["boost_promotion"] = expect_failure(model(r=changed(reductions, "id", "R09", "status", "DERIVED_FOUNDED_DEPTH")))
    catches["CSN_reactivation"] = expect_failure(model(r=changed(reductions, "id", "R10", "status", "ACTIVE_NATIVE")))
    catches["phi_demotion"] = expect_failure(model(s=changed(status, "object", "founded_phi_identity", "status", "OPEN_PLACEHOLDER")))
    catches["physics_promotion"] = expect_failure(model(s=changed(status, "object", "lambda_Xmax_action_carrier_source_boundary_density_bootstrap_mass_dynamics", "status", "DERIVED")))
    bad_production = copy.deepcopy(production)
    bad_production["counts"]["closure_rank"] = 21
    catches["production_witness"] = expect_failure(model(p=bad_production))
    bad_independent = copy.deepcopy(independent)
    bad_independent["counts"]["Taylor_constraint_checks"] = 251
    catches["independent_witness"] = expect_failure(model(i=bad_independent))
    catches["source_identity"] = expect_failure(lambda: validate_sources(True))
    catches["coefficient_selection"] = expect_failure(model(r=changed(reductions, "id", "R11", "status", "UNIQUE_SELECTED")))

    if len(catches) != 15 or set(catches.values()) != {"PASS"}:
        raise AssertionError("catch count")
    with (HERE / "CATCH_PROOFS.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["catch", "result"])
        writer.writerows(sorted(catches.items()))
    result = {
        "schema": "udt-founded-pair-first-jet-verification-1.0",
        "result": "PASS",
        "grade": "VERIFIED_WITH_CAVEATS_BOUNDED_FIRST_JET_ATLAS",
        "basis_rows": len(basis),
        "outcome_rows": len(outcomes),
        "reduction_rows": len(reductions),
        "status_rows": len(status),
        "source_identities": len(rows("SOURCE_MANIFEST.tsv")),
        "production_summary_checks": production["summary_check_count"],
        "production_census_checks": production["census_check_count"],
        "independent_checks": independent["summary_check_count"],
        "production_closure_rank": production["counts"]["closure_rank"],
        "independent_closure_rank": independent["counts"]["closure_rank"],
        "catch_count": len(catches),
        "catch_proofs": catches,
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
