#!/usr/bin/env python3
"""Independent standard-library verifier for the mixed-readout anchor audit."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def matrix(rows):
    return [[Q(value) for value in row] for row in rows]


def transpose(value):
    return [list(row) for row in zip(*value)]


def multiply(left, right):
    return [
        [
            sum(left[row][middle] * right[middle][column] for middle in range(len(right)))
            for column in range(len(right[0]))
        ]
        for row in range(len(left))
    ]


def inverse2(value):
    determinant = value[0][0] * value[1][1] - value[0][1] * value[1][0]
    if determinant == 0:
        raise AssertionError("singular matrix")
    return matrix(
        [
            [value[1][1] / determinant, -value[0][1] / determinant],
            [-value[1][0] / determinant, value[0][0] / determinant],
        ]
    )


def trace(value):
    return sum(value[index][index] for index in range(len(value)))


def determinant2(value):
    return value[0][0] * value[1][1] - value[0][1] * value[1][0]


def add(left, right, factor=Q(1)):
    return [
        [left[row][column] + factor * right[row][column] for column in range(len(left[0]))]
        for row in range(len(left))
    ]


def pair_invariant(metric, generator):
    return trace(
        multiply(
            multiply(multiply(inverse2(metric), transpose(generator)), metric),
            generator,
        )
    )


def transform_pair(metric, generator, basis):
    return (
        multiply(multiply(transpose(basis), metric), basis),
        multiply(multiply(inverse2(basis), generator), basis),
    )


def rows(name):
    with (HERE / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def digest(name):
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def expect_failure(label, callback, catches):
    try:
        callback()
    except AssertionError:
        catches[label] = "PASS"
        return
    raise AssertionError(f"catch did not fail: {label}")


EXPECTED_OUTCOMES = {
    "OBSERVATIONAL_ANCHOR_LEAVES_MU_OPEN",
    "MU_IS_INVARIANT_OF_METRIC_RECIPROCITY_PAIR",
    "FIXED_Q_AND_ORTHONORMALIZABLE_ANCHOR_BRANCHES_DIVERGE",
    "TEMPORAL_MIRROR_COMPONENT_SOLDERING_REMAINS_OPEN",
    "PHYSICAL_CLOCK_RULER_SOLDERING_RULE_ABSENT",
}
FORBIDDEN_OUTCOMES = {
    "OBSERVATIONAL_ANCHOR_REJECTS_MIXED_READOUT",
    "OBSERVATIONAL_ANCHOR_SELECTS_UNIQUE_MU",
    "MU_IS_SIMULTANEOUS_BASIS_ARTIFACT",
    "TEMPORAL_MIRROR_SELECTS_OR_REJECTS_MIXED_READOUT",
    "AUDIT_INCONCLUSIVE",
}


def validate_model(model):
    result = model["result"]
    branch = model["branch"]
    status = model["status"]
    source = model["source"]
    require(set(result["outcomes"]) == EXPECTED_OUTCOMES, "outcomes")
    require(not (set(result["outcomes"]) & FORBIDDEN_OUTCOMES), "forbidden outcome")
    require(result["maximum_conclusion"] == "UDT_MIXED_READOUT_ANCHOR_SOLDERING_STATUS_CHARACTERIZED", "maximum")
    require(result["pair_invariant"]["value"] == "2*(1+mu)/(1-mu)", "invariant formula")
    require(result["pair_invariant"]["inverse"] == "mu=(I-2)/(I+2)", "inverse formula")
    require(result["witnesses"]["MU4"]["pair_invariant"] == "-10/3", "mu4 invariant")
    require(result["witnesses"]["MU9"]["pair_invariant"] == "-5/2", "mu9 invariant")
    require(result["witnesses"]["MU4"]["pair_invariant"] != result["witnesses"]["MU9"]["pair_invariant"], "distinct witnesses")
    branch_by_name = {row["branch"]: row for row in branch}
    require(len(branch_by_name) == len(branch) == 3, "branch coverage")
    require(branch_by_name["FIXED_Q_ANCHOR"]["udt_status"] == "CONDITIONAL_REJECTION_PINNED_BY_HABIT", "fixed q status")
    require(branch_by_name["ORTHONORMALIZABLE_ANCHOR"]["udt_status"] == "CONDITIONAL_COMPATIBILITY_NOT_A_SOLDERING_THEOREM", "weak status")
    require(branch_by_name["CURRENT_SOURCE_RULING"]["udt_status"] == "OBSERVATIONAL_ANCHOR_LEAVES_MU_OPEN", "current ruling")
    status_by_object = {row["object"]: row for row in status}
    require(len(status_by_object) == len(status) == 11, "status coverage")
    require(status_by_object["Mixing modulus mu"]["status"] == "INVARIANT_OPEN", "mu promotion")
    require(status_by_object["Temporal mirror component action"]["status"] == "OPEN", "temporal promotion")
    require(status_by_object["Clock-ruler soldering rule"]["status"] == "OPEN", "soldering promotion")
    require(status_by_object["Finite observed c_E"]["status"] == "OBSERVED_ANCHOR", "c status")
    source_by_id = {row["id"]: row for row in source}
    require(len(source_by_id) == len(source) == 14, "source coverage")
    require("dimension-matched" in source_by_id["S01"]["audit_use"], "q source")
    require("non-derived" in source_by_id["S03"]["audit_use"], "slot source")
    require("calibration remain open" in source_by_id["S09"]["audit_use"], "frontier source")


def main():
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    model = {
        "result": result,
        "branch": rows("ANCHOR_BRANCH_CLASSIFICATION.tsv"),
        "status": rows("STATUS_LEDGER.tsv"),
        "source": rows("SOURCE_LINEAGE.tsv"),
    }
    validate_model(model)

    L = matrix([[-1, 0], [0, 1]])
    F = matrix([[0, 1], [1, 0]])
    T_literal = matrix([[-1, 0], [0, 1]])
    S = matrix([[2, 1], [1, 1]])
    H4 = matrix([[1, -2], [-2, 1]])
    H9 = matrix([[1, -3], [-3, 1]])
    I4 = pair_invariant(H4, L)
    I9 = pair_invariant(H9, L)
    H4_prime, L_prime = transform_pair(H4, L, S)
    H9_prime, L9_prime = transform_pair(H9, L, S)
    S_had = matrix([[1, 1], [1, -1]])
    H_had, F_had = transform_pair(H4, F, S_had)
    _, T_had = transform_pair(H4, T_literal, S_had)
    temporal_in_q = multiply(multiply(S_had, matrix([[-1, 0], [0, 1]])), inverse2(S_had))
    spatial_in_q = multiply(multiply(S_had, matrix([[1, 0], [0, -1]])), inverse2(S_had))

    independent = {
        "mu4_invariant_exact": I4 == Q(-10, 3),
        "mu9_invariant_exact": I9 == Q(-5, 2),
        "inequivalent_witnesses": I4 != I9,
        "mu4_reconstruction": (I4 - 2) / (I4 + 2) == 4,
        "mu9_reconstruction": (I9 - 2) / (I9 + 2) == 9,
        "general_rational_basis_mu4": pair_invariant(H4_prime, L_prime) == I4,
        "general_rational_basis_mu9": pair_invariant(H9_prime, L9_prime) == I9,
        "witnesses_Lorentz": determinant2(H4) < 0 and determinant2(H9) < 0,
        "spatial_seal_H4": multiply(multiply(transpose(F), H4), F) == H4,
        "spatial_seal_H9": multiply(multiply(transpose(F), H9), F) == H9,
        "fixed_q_null_odd_term_nonzero": Q(-4) * H4[0][1] != 0,
        "fixed_q_B0_definite": determinant2(matrix([[1, 0], [0, 1]])) > 0,
        "hadamard_diagonalizes": H_had == matrix([[-2, 0], [0, 6]]),
        "hadamard_metric_rescalable_to_eta": H_had[0][0] < 0 < H_had[1][1],
        "spatial_reflection_standard_in_anchor": F_had == matrix([[1, 0], [0, -1]]),
        "literal_q_time_not_H4_isometry": multiply(multiply(transpose(T_literal), H4), T_literal) != H4,
        "literal_time_non_diagonal_in_anchor": T_had == matrix([[0, -1], [-1, 0]]),
        "orth_temporal_conjugates_to_minus_F": temporal_in_q == matrix([[0, -1], [-1, 0]]),
        "orth_spatial_conjugates_to_F": spatial_in_q == F,
        "source_meaning_present": "ordinary clock-length baseline" in (ROOT / "udt_premise_reset_audit_2026-07-19/OWNER_MEANING_LEDGER.tsv").read_text(encoding="utf-8"),
        "readout_stamp_present": "any slot identification retain their separately ledgered non-derived statuses" in (ROOT / "UDT_NATIVE_ACTION_COLD_PACKET.md").read_text(encoding="utf-8"),
        "frontier_calibration_open": "material clock/ruler calibration remain open" in (ROOT / "UDT_SCIENTIFIC_FRONTIER_2026-07-19.md").read_text(encoding="utf-8"),
        "all_derivation_checks_pass": result["check_count"] == 45 and set(result["checks"].values()) == {"PASS"},
    }
    require(all(independent.values()), [key for key, value in independent.items() if not value])

    catches = {}
    mutation = copy.deepcopy(model); mutation["result"]["outcomes"].remove("MU_IS_INVARIANT_OF_METRIC_RECIPROCITY_PAIR")
    expect_failure("missing_invariant_outcome", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); mutation["result"]["outcomes"].append("MU_IS_SIMULTANEOUS_BASIS_ARTIFACT")
    expect_failure("basis_artifact_promotion", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); mutation["result"]["outcomes"].append("OBSERVATIONAL_ANCHOR_SELECTS_UNIQUE_MU")
    expect_failure("unique_mu_promotion", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); mutation["result"]["outcomes"].append("OBSERVATIONAL_ANCHOR_REJECTS_MIXED_READOUT")
    expect_failure("unconditional_rejection", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); mutation["result"]["pair_invariant"]["value"] = "2"
    expect_failure("invariant_formula_mutation", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); mutation["result"]["witnesses"]["MU9"]["pair_invariant"] = "-10/3"
    expect_failure("collapsed_witness_invariants", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); mutation["branch"][0]["udt_status"] = "DERIVED_UDT_REJECTION"
    expect_failure("fixed_q_habit_promoted", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); mutation["branch"] = mutation["branch"][:-1]
    expect_failure("missing_current_source_ruling", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); mutation["branch"][1]["udt_status"] = "SOLDERING_DERIVED"
    expect_failure("weak_chart_made_soldering_theorem", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); next(row for row in mutation["status"] if row["object"] == "Mixing modulus mu")["status"] = "DERIVED"
    expect_failure("mu_status_promotion", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); next(row for row in mutation["status"] if row["object"] == "Temporal mirror component action")["status"] = "DERIVED"
    expect_failure("temporal_status_promotion", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); next(row for row in mutation["status"] if row["object"] == "Clock-ruler soldering rule")["status"] = "DERIVED"
    expect_failure("soldering_status_promotion", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); next(row for row in mutation["status"] if row["object"] == "Finite observed c_E")["status"] = "DERIVED_FROM_METRIC"
    expect_failure("c_anchor_status_mutation", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); mutation["status"].append(copy.deepcopy(mutation["status"][0]))
    expect_failure("duplicate_status_object", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); mutation["source"] = mutation["source"][:-1]
    expect_failure("missing_source_lineage", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); next(row for row in mutation["source"] if row["id"] == "S03")["audit_use"] = "slot identification derived"
    expect_failure("nonderived_slot_stamp_lost", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); mutation["result"]["maximum_conclusion"] = "COMPLETE_PHYSICAL_FRAME_DERIVED"
    expect_failure("maximum_conclusion_overreach", lambda: validate_model(mutation), catches)
    expect_failure("wrong_fixed_q_evenness", lambda: require(Q(-4) * Q(-2) == 0, "odd term"), catches)
    expect_failure("literal_equals_conjugated_temporal", lambda: require(T_literal == temporal_in_q, "temporal frames"), catches)

    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    lay = (HERE / "LAY_DECISION_TREE.md").read_text(encoding="utf-8")
    next_decision = (HERE / "NEXT_SCIENTIFIC_DECISION.md").read_text(encoding="utf-8")
    require("mu = (I-2)/(I+2)" in report, "report invariant")
    require("not a physical soldering theorem" in report, "report caveat")
    require("current evidence puts us in the third case" in lay, "lay ruling")
    require("angular sector" in next_decision and "soldered" in next_decision, "next decision")

    output = {
        "schema": "udt-mixed-readout-anchor-independent-verification-1.0",
        "result": "PASS_VERIFIED_WITH_CAVEATS",
        "counts": {
            "derivation_checks": result["check_count"],
            "independent_checks": len(independent),
            "catch_proofs": len(catches),
        },
        "independent_checks": {key: "PASS" for key in independent},
        "catch_proofs": catches,
        "hashes": {
            name: digest(name)
            for name in (
                "PREREGISTRATION.md",
                "DERIVATION_RESULT.json",
                "SOURCE_LINEAGE.tsv",
                "ANCHOR_BRANCH_CLASSIFICATION.tsv",
                "PAIR_INVARIANTS.tsv",
                "STATUS_LEDGER.tsv",
                "AUDIT_REPORT.md",
            )
        },
        "maximum_conclusion": result["maximum_conclusion"],
        "caveats": [
            "bounded constant symmetric 2x2 readout class",
            "no physical observer transformation derived",
            "no angular/global completion tested",
            "no action, source, carrier, or mass conclusion",
        ],
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("verification=PASS_VERIFIED_WITH_CAVEATS")
    print(f"derivation_checks={result['check_count']}")
    print(f"independent_checks={len(independent)}")
    print(f"catch_proofs={len(catches)}")


if __name__ == "__main__":
    main()
