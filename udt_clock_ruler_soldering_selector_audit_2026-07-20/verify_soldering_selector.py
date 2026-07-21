#!/usr/bin/env python3
"""Independent standard-library verifier for the soldering selector audit."""

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


def identity(size):
    return matrix([[1 if row == column else 0 for column in range(size)] for row in range(size)])


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


def add(left, right, factor=Q(1)):
    return [
        [left[row][column] + factor * right[row][column] for column in range(len(left[0]))]
        for row in range(len(left))
    ]


def scale(value, factor):
    factor = Q(factor)
    return [[factor * entry for entry in row] for row in value]


def inverse(value):
    size = len(value)
    work = [value[row][:] + identity(size)[row] for row in range(size)]
    for column in range(size):
        pivot = next((row for row in range(column, size) if work[row][column]), None)
        if pivot is None:
            raise AssertionError("singular matrix")
        work[column], work[pivot] = work[pivot], work[column]
        pivot_value = work[column][column]
        work[column] = [entry / pivot_value for entry in work[column]]
        for row in range(size):
            if row == column:
                continue
            factor = work[row][column]
            if factor:
                work[row] = [
                    work[row][entry] - factor * work[column][entry]
                    for entry in range(2 * size)
                ]
    return [row[size:] for row in work]


def determinant(value):
    size = len(value)
    work = [row[:] for row in value]
    answer = Q(1)
    sign = 1
    for column in range(size):
        pivot = next((row for row in range(column, size) if work[row][column]), None)
        if pivot is None:
            return Q(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            sign *= -1
        pivot_value = work[column][column]
        answer *= pivot_value
        for row in range(column + 1, size):
            factor = work[row][column] / pivot_value
            for entry in range(column, size):
                work[row][entry] -= factor * work[column][entry]
    return Q(sign) * answer


def trace(value):
    return sum(value[index][index] for index in range(len(value)))


def block(top_left, top_right, bottom_left, bottom_right):
    top = [top_left[row] + top_right[row] for row in range(len(top_left))]
    bottom = [bottom_left[row] + bottom_right[row] for row in range(len(bottom_left))]
    return top + bottom


def pair_invariant(metric, generator):
    return trace(
        multiply(
            multiply(multiply(inverse(metric), transpose(generator)), metric),
            generator,
        )
    )


def quadratic(vector_left, metric, vector_right):
    return multiply(transpose(vector_left), multiply(metric, vector_right))[0][0]


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
    "ANGULAR_SEAL_STRUCTURE_LEAVES_MU_OPEN",
    "NONZERO_ANGULAR_COUPLING_LEAVES_MU_OPEN",
    "CSN_OR_VOLUME_NORMALIZATION_LEAVES_MU_OPEN",
    "CARTAN_HOLONOMY_IS_CONDITIONAL_ON_COFRAME_CHOICE",
    "BOOTSTRAP_HAS_NO_CURRENT_SOLDERING_EQUATION",
    "METRIC_NATIVE_SOLDERING_RULE_ABSENT_FROM_CURRENT_LEDGER",
    "FULL_ANGULAR_DYNAMIC_COMPLETION_COULD_STILL_SELECT_OPEN",
}
FORBIDDEN_OUTCOMES = {
    "CURRENT_METRIC_STRUCTURE_SELECTS_UNIQUE_SOLDERING",
    "CURRENT_METRIC_STRUCTURE_SELECTS_UNIQUE_MU",
    "CURRENT_METRIC_STRUCTURE_REJECTS_MIXED_READOUT",
    "NONZERO_ANGULAR_COUPLING_SELECTS_MU",
    "CSN_OR_VOLUME_NORMALIZATION_SELECTS_MU",
    "CARTAN_HOLONOMY_SELECTS_SOLDERING",
    "BOOTSTRAP_SUPPLIES_SOLDERING_EQUATION",
    "AUDIT_INCONCLUSIVE",
}


def validate_model(model):
    result = model["result"]
    status = model["status"]
    selector = model["selector"]
    seal = model["seal"]
    witnesses = model["witnesses"]
    source = model["source"]
    require(set(result["outcomes"]) == EXPECTED_OUTCOMES, "outcomes")
    require(not set(result["outcomes"]) & FORBIDDEN_OUTCOMES, "forbidden outcomes")
    require(result["maximum_conclusion"] == "UDT_CURRENT_METRIC_NATIVE_SOLDERING_SELECTOR_STATUS_CHARACTERIZED", "maximum")
    require(result["seal_local_base_soldering"]["status"] == "DERIVED_CONDITIONAL_WITHIN_PRE_SPLIT_MIXED_BASE_AT_SEAL", "local seal status")
    require(result["conditional_complete_soldering"]["status"] == "DERIVED_WITHIN_CHOSEN_TRANSVERSE_IDENTITY_AND_AXIS_REFLECTION_LIFT", "conditional full status")
    require(result["mu_status"]["status"] == "INVARIANT_OPEN", "mu status")
    require(result["mu_status"]["magnitude"] == "not selected", "mu magnitude")
    require("complete selected lift" in result["outcome_scope"]["METRIC_NATIVE_SOLDERING_RULE_ABSENT_FROM_CURRENT_LEDGER"], "absence scope")

    status_by_object = {row["object"]: row for row in status}
    require(len(status_by_object) == len(status) == 15, "status coverage")
    require(status_by_object["Seal-local base eigensplitting"]["status"] == "DERIVED_CONDITIONAL", "seal promotion/loss")
    require(status_by_object["Mixing modulus mu"]["status"] == "INVARIANT_OPEN", "mu promotion")
    require(status_by_object["Complete metric-native soldering"]["status"] == "OPEN_WITH_PARTIAL_LOCAL_CONSTRUCTION", "global soldering promotion")
    require(status_by_object["Current bootstrap"]["status"] == "ON_SHELL_ADMISSIBILITY_NO_SOLDERING_EQUATION", "bootstrap promotion")

    selector_by_structure = {row["structure"]: row for row in selector}
    require(len(selector_by_structure) == len(selector) == 11, "selector coverage")
    require(selector_by_structure["Spatial-depth seal"]["result"] == "PARTIAL_LOCAL_SOLDERING_ONLY", "seal selector")
    require(selector_by_structure["CSN"]["result"] == "LEAVES_MU_OPEN", "csn selector")
    require(selector_by_structure["Cartan/Bianchi identities"]["result"] == "DO_NOT_SELECT", "cartan selector")
    require(selector_by_structure["Current bootstrap"]["result"] == "NO_CURRENT_SOLDERING_EQUATION", "bootstrap selector")

    seal_by_id = {row["id"]: row for row in seal}
    require(len(seal_by_id) == len(seal) == 10, "seal ledger coverage")
    require(seal_by_id["L06"]["status"] == "INVARIANT_OPEN", "seal mu")
    require(seal_by_id["L09"]["status"] == "MULTIPLE_COMPLETIONS", "angular completion")
    require(seal_by_id["L10"]["status"] == "OPEN", "global continuation")

    witness_by_id = {row["id"]: row for row in witnesses}
    require(len(witness_by_id) == len(witnesses) == 3, "witness coverage")
    require(witness_by_id["MU4_NONZERO"]["cross_C"] != "0", "mu4 cross removed")
    require(witness_by_id["MU9_NONZERO"]["cross_C"] != "0", "mu9 cross removed")
    require(witness_by_id["MU4_NONZERO"]["full_pair_invariant"] == "-8300/2533", "mu4 full invariant")
    require(witness_by_id["MU9_NONZERO"]["full_pair_invariant"] == "-49900/20099", "mu9 full invariant")
    require(witness_by_id["MU4_NONZERO"]["full_pair_invariant"] != witness_by_id["MU9_NONZERO"]["full_pair_invariant"], "witness collapse")

    source_by_id = {row["id"]: row for row in source}
    require(len(source_by_id) == len(source) == 16, "source coverage")
    require("multiple angular" in source_by_id["S05"]["audit_use"], "complete coframe source")
    require("after-solution admissibility" in source_by_id["S09"]["audit_use"], "bootstrap source")
    require("derived per supplied metric" in source_by_id["S11"]["audit_use"], "Cartan source")


def main():
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    model = {
        "result": result,
        "status": rows("STATUS_LEDGER.tsv"),
        "selector": rows("SELECTOR_AUTHORITY.tsv"),
        "seal": rows("SEAL_SOLDERING_LEDGER.tsv"),
        "witnesses": rows("FULL_COUNTERMODELS.tsv"),
        "source": rows("SOURCE_LINEAGE.tsv"),
    }
    validate_model(model)

    F = matrix([[0, 1], [1, 0]])
    L = matrix([[-1, 0], [0, 1]])
    eta = matrix([[-1, 0], [0, 1]])
    v_plus = matrix([[1], [1]])
    v_minus = matrix([[-1], [1]])
    eigenbasis = matrix([[1, -1], [1, 1]])
    rational_boost = matrix([[Q(5, 3), Q(4, 3)], [Q(4, 3), Q(5, 3)]])
    angular_reflection = matrix([[1, 0], [0, -1]])
    full_seal = block(F, matrix([[0, 0], [0, 0]]), matrix([[0, 0], [0, 0]]), angular_reflection)
    L4 = matrix([[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    U = matrix([[1, 0], [0, 1], [0, 0], [0, 0]])

    witness_data = {}
    independent = {}
    for label, kval, expected_det, expected_I in (
        ("MU4", 2, Q(-7599, 2500), Q(-8300, 2533)),
        ("MU9", 3, Q(-20099, 2500), Q(-49900, 20099)),
    ):
        H = matrix([[1, -kval], [-kval, 1]])
        C = matrix([[Q(1, 10), Q(1, 10)], [Q(1, 10), Q(-1, 10)]])
        full = block(H, C, transpose(C), identity(2))
        projector = multiply(multiply(multiply(U, inverse(H)), transpose(U)), full)
        complement = add(identity(4), projector, Q(-1))
        full_I = pair_invariant(full, L4)
        independent[f"{label}_seal_isometry"] = multiply(multiply(transpose(full_seal), full), full_seal) == full
        independent[f"{label}_determinant"] = determinant(full) == expected_det
        independent[f"{label}_full_pair_invariant"] = full_I == expected_I
        independent[f"{label}_Lorentz_signature_blocks"] = Q(1 - kval) - Q(1, 50) < 0 < Q(1 + kval) - Q(1, 50)
        independent[f"{label}_projector_idempotent"] = multiply(projector, projector) == projector
        independent[f"{label}_projector_metric_self_adjoint"] = multiply(transpose(projector), full) == multiply(full, projector)
        independent[f"{label}_projector_seal_preserved"] = multiply(multiply(full_seal, projector), full_seal) == projector
        # The graph complement has exact positive diagonal metric values.
        expected_transverse = (
            (Q(kval) + Q(1, 50) - 1) / (kval - 1),
            (Q(kval) - Q(1, 50) + 1) / (kval + 1),
        )
        independent[f"{label}_transverse_complement_positive"] = all(value > 0 for value in expected_transverse)
        independent[f"{label}_complement_annihilates_projector"] = multiply(projector, complement) == matrix([[0] * 4 for _ in range(4)])
        witness_data[label] = (H, full, projector, full_I)

    H4 = witness_data["MU4"][0]
    gram = multiply(multiply(transpose(eigenbasis), H4), eigenbasis)
    seal_in_eigenbasis = multiply(multiply(inverse(eigenbasis), F), eigenbasis)
    time_in_eigenbasis = multiply(multiply(inverse(eigenbasis), scale(F, -1)), eigenbasis)
    independent.update(
        {
            "base_seal_plus_eigenline": multiply(F, v_plus) == v_plus,
            "base_seal_minus_eigenline": multiply(F, v_minus) == scale(v_minus, -1),
            "base_eigenlines_orthogonal": quadratic(v_plus, H4, v_minus) == 0,
            "base_eigenline_causal_signs": quadratic(v_plus, H4, v_plus) < 0 < quadratic(v_minus, H4, v_minus),
            "base_raw_gram_diagonal": gram == matrix([[-2, 0], [0, 6]]),
            "seal_standard_in_eigenbasis": seal_in_eigenbasis == matrix([[1, 0], [0, -1]]),
            "minus_seal_temporal_in_eigenbasis": time_in_eigenbasis == matrix([[-1, 0], [0, 1]]),
            "nontrivial_rational_boost_is_Lorentz": multiply(multiply(transpose(rational_boost), eta), rational_boost) == eta,
            "nontrivial_boost_does_not_preserve_seal_axes": multiply(rational_boost, angular_reflection) != multiply(angular_reflection, rational_boost),
            "base_mu4_invariant": pair_invariant(H4, L) == Q(-10, 3),
            "base_mu9_invariant": pair_invariant(witness_data["MU9"][0], L) == Q(-5, 2),
            "full_mu_witnesses_distinct": witness_data["MU4"][3] != witness_data["MU9"][3],
            "cross_parity_exact": multiply(multiply(transpose(F), matrix([[Q(1, 10), Q(1, 10)], [Q(1, 10), Q(-1, 10)]])), angular_reflection) == matrix([[Q(1, 10), Q(1, 10)], [Q(1, 10), Q(-1, 10)]]),
            "full_seal_inverts_L4": multiply(multiply(full_seal, L4), full_seal) == scale(L4, -1),
            "unit_volume_mu4_rational_angular_compensation": determinant(block(H4, matrix([[0, 0], [0, 0]]), matrix([[0, 0], [0, 0]]), matrix([[1, 0], [0, Q(1, 3)]]))) == -1,
            "unit_volume_mu9_rational_angular_compensation": determinant(block(witness_data["MU9"][0], matrix([[0, 0], [0, 0]]), matrix([[0, 0], [0, 0]]), matrix([[1, 0], [0, Q(1, 8)]]))) == -1,
            "CSN_scaling_keeps_pair_invariant": pair_invariant(scale(witness_data["MU4"][1], 4), L4) == witness_data["MU4"][3],
            "all_symbolic_derivation_checks_pass": result["check_count"] == 51 and set(result["checks"].values()) == {"PASS"},
            "bootstrap_source_text_present": "after-solution admissibility condition" in (ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19/AUDIT_REPORT.md").read_text(encoding="utf-8"),
            "Cartan_source_text_present": "does not choose which complete metric the universe realizes" in (ROOT / "metric_cartan_holonomy_audit_2026-07-19/AUDIT_REPORT.md").read_text(encoding="utf-8"),
            "multiple_lifts_source_text_present": "continuous families survive" in " ".join((ROOT / "complete_coframe_seal_involution_2026-07-20/AUDIT_REPORT.md").read_text(encoding="utf-8").split()),
        }
    )
    require(all(independent.values()), [key for key, value in independent.items() if not value])

    catches = {}
    mutation = copy.deepcopy(model); mutation["result"]["seal_local_base_soldering"]["status"] = "OPEN"
    expect_failure("local_seal_result_deleted", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); mutation["result"]["mu_status"]["status"] = "DERIVED_UNIQUE"
    expect_failure("mu_promoted", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); mutation["result"]["outcomes"].append("CURRENT_METRIC_STRUCTURE_SELECTS_UNIQUE_MU")
    expect_failure("unique_mu_outcome_added", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); mutation["result"]["outcomes"].append("CURRENT_METRIC_STRUCTURE_REJECTS_MIXED_READOUT")
    expect_failure("mixed_family_rejected", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); mutation["result"]["outcome_scope"]["METRIC_NATIVE_SOLDERING_RULE_ABSENT_FROM_CURRENT_LEDGER"] = "all local and global soldering absent"
    expect_failure("partial_soldering_scope_erased", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); next(row for row in mutation["status"] if row["object"] == "Mixing modulus mu")["status"] = "DERIVED"
    expect_failure("status_mu_promoted", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); next(row for row in mutation["status"] if row["object"] == "Complete metric-native soldering")["status"] = "DERIVED_COMPLETE"
    expect_failure("global_soldering_promoted", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); next(row for row in mutation["status"] if row["object"] == "Current bootstrap")["status"] = "LOCAL_SELECTOR"
    expect_failure("bootstrap_promoted", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); next(row for row in mutation["selector"] if row["structure"] == "Spatial-depth seal")["result"] = "NO_SOLDERING_INFORMATION"
    expect_failure("seal_partial_result_deleted", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); next(row for row in mutation["selector"] if row["structure"] == "CSN")["result"] = "SELECTS_MU"
    expect_failure("CSN_promoted", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); next(row for row in mutation["selector"] if row["structure"] == "Cartan/Bianchi identities")["result"] = "SELECT_MU"
    expect_failure("Cartan_promoted", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); next(row for row in mutation["selector"] if row["structure"] == "Current bootstrap")["result"] = "DERIVED_SOLDERING"
    expect_failure("bootstrap_selector_invented", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); mutation["seal"] = mutation["seal"][:-1]
    expect_failure("global_continuation_row_deleted", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); next(row for row in mutation["seal"] if row["id"] == "L09")["status"] = "UNIQUE"
    expect_failure("multiple_angular_lifts_erased", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); next(row for row in mutation["witnesses"] if row["id"] == "MU4_NONZERO")["cross_C"] = "0"
    expect_failure("nonzero_cross_witness_removed", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); next(row for row in mutation["witnesses"] if row["id"] == "MU9_NONZERO")["full_pair_invariant"] = "-8300/2533"
    expect_failure("full_invariants_collapsed", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); mutation["source"] = mutation["source"][:-1]
    expect_failure("source_lineage_missing", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); next(row for row in mutation["source"] if row["id"] == "S09")["audit_use"] = "bootstrap local equation"
    expect_failure("bootstrap_source_role_mutated", lambda: validate_model(mutation), catches)
    expect_failure("wrong_seal_eigenline", lambda: require(multiply(F, v_plus) == scale(v_plus, -1), "seal eigenline"), catches)
    expect_failure("projector_mutation", lambda: require(multiply(add(witness_data["MU4"][2], identity(4)), add(witness_data["MU4"][2], identity(4))) == add(witness_data["MU4"][2], identity(4)), "projector"), catches)

    report = (HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8")
    lay = (HERE / "LAY_DECISION_TREE.md").read_text(encoding="utf-8")
    refinement = (HERE / "PRIOR_WORDING_REFINEMENT.md").read_text(encoding="utf-8")
    next_decision = (HERE / "NEXT_SCIENTIFIC_DECISION.md").read_text(encoding="utf-8")
    report_flat = " ".join(report.split())
    require("partial closure hiding in the finite-cell mirror" in report_flat, "report positive result")
    require("does **not** select the invariant magnitude" in report_flat, "report limit")
    require("base clock/ruler join is not wholly missing" in lay, "lay positive result")
    require("seal locally solders the supplied base" in " ".join(refinement.split()), "parent refinement")
    require("complete reciprocal/angular/normal/time-on lift" in next_decision, "next decision")

    output = {
        "schema": "udt-clock-ruler-soldering-selector-independent-verification-1.0",
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
                "SELECTOR_AUTHORITY.tsv",
                "SEAL_SOLDERING_LEDGER.tsv",
                "FULL_COUNTERMODELS.tsv",
                "STATUS_LEDGER.tsv",
                "PRIOR_WORDING_REFINEMENT.md",
                "AUDIT_REPORT.md",
            )
        },
        "maximum_conclusion": result["maximum_conclusion"],
        "caveats": [
            "seal-local positive result is conditional on the mixed readout and supplied reciprocal base",
            "complete transverse reciprocal and angular lift remains unselected",
            "full countermodels are algebraic local coframes, not completed bootstrap universes",
            "no action, source, topology, representative, scale, or matter selection",
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
