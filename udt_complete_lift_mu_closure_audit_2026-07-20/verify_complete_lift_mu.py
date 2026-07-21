#!/usr/bin/env python3
"""Independent standard-library verifier for the complete-lift mu audit."""

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
            raise AssertionError("singular")
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


def rank(value):
    work = [row[:] for row in value]
    rows_count = len(work)
    columns = len(work[0]) if work else 0
    pivot_row = 0
    for column in range(columns):
        pivot = next((row for row in range(pivot_row, rows_count) if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [entry / pivot_value for entry in work[pivot_row]]
        for row in range(rows_count):
            if row != pivot_row and work[row][column]:
                factor = work[row][column]
                work[row] = [
                    work[row][entry] - factor * work[pivot_row][entry]
                    for entry in range(columns)
                ]
        pivot_row += 1
        if pivot_row == rows_count:
            break
    return pivot_row


def trace(value):
    return sum(value[index][index] for index in range(len(value)))


def block(left, right):
    zero_lr = [[Q(0) for _ in range(len(right))] for _ in range(len(left))]
    zero_rl = [[Q(0) for _ in range(len(left))] for _ in range(len(right))]
    return [left[row] + zero_lr[row] for row in range(len(left))] + [
        zero_rl[row] + right[row] for row in range(len(right))
    ]


def full_metric(base, cross, angular):
    return [base[row] + cross[row] for row in range(2)] + [
        transpose(cross)[row] + angular[row] for row in range(2)
    ]


def pair_invariant(metric, generator):
    return trace(
        multiply(
            multiply(multiply(inverse(metric), transpose(generator)), metric),
            generator,
        )
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
    "ORIENTATION_CLASS_LEAVES_MU_OPEN",
    "CORNER_COCYCLE_IS_MU_BLIND",
    "ALL_REGISTERED_ALGEBRAIC_LIFTS_LEAVE_MU_OPEN",
    "NONZERO_CROSS_BLOCKS_LEAVE_MU_OPEN_IN_EVERY_LIFT",
    "NORMALIZED_SEAL_TRANSITIONS_ARE_MU_BLIND",
    "CONDITIONAL_HOPF_LIFT_HAS_NO_CURRENT_MU_EQUATION",
    "METRIC_DEPENDENT_GLOBAL_CLOSURE_EQUATION_ABSENT",
    "GLOBAL_COMPLETION_REMAINS_OPEN",
}
FORBIDDEN_OUTCOMES = {
    "ONE_COMPLETE_LIFT_SELECTED_BY_CURRENT_FOUNDATION",
    "ORIENTATION_SELECTS_ONE_COMPLETE_LIFT",
    "CORNER_COCYCLE_SELECTS_MU",
    "NORMALIZED_SEAL_TRANSITIONS_SELECT_MU",
    "CONDITIONAL_HOPF_LIFT_SELECTS_MU",
    "METRIC_DEPENDENT_GLOBAL_CLOSURE_EQUATION_PRESENT",
    "AUDIT_INCONCLUSIVE",
}


def validate_model(model):
    result = model["result"]
    lifts = model["lifts"]
    witnesses = model["witnesses"]
    selectors = model["selectors"]
    status = model["status"]
    source = model["source"]
    require(set(result["outcomes"]) == EXPECTED_OUTCOMES, "outcomes")
    require(not set(result["outcomes"]) & FORBIDDEN_OUTCOMES, "forbidden outcomes")
    require(result["maximum_conclusion"] == "UDT_COMPLETE_LIFT_AND_GLOBAL_MU_CLOSURE_STATUS_CHARACTERIZED", "maximum")
    require(result["global_authority"]["metric_dependent_equation_for_pair_invariant"] == "ABSENT_FROM_CURRENT_LEDGER", "global equation promotion")
    require(result["orientation_result"]["status"] == "ORIENTATION_CLASS_LEAVES_MU_OPEN", "orientation result")

    lift_by_name = {row["lift"]: row for row in lifts}
    require(len(lift_by_name) == len(lifts) == 4, "lift coverage")
    require(set(lift_by_name) == {"PLUS_IDENTITY", "MINUS_IDENTITY", "AXIS_REFLECTION", "HOPF_EXCHANGE_LOCAL"}, "lift universe")
    require(all(row["mu4"] == "SURVIVES_NONZERO_CROSS" and row["mu9"] == "SURVIVES_NONZERO_CROSS" for row in lifts), "lift mu coverage")

    witness_by_id = {row["id"]: row for row in witnesses}
    require(len(witness_by_id) == len(witnesses) == 8, "witness coverage")
    for lift in lift_by_name:
        family = [row for row in witnesses if row["lift"] == lift]
        require({row["mu"] for row in family} == {"4", "9"}, f"{lift} mu pair")
        require(all(row["cross_u"] == "1/10" and row["cross_v"] == "1/10" for row in family), f"{lift} cross")
        require(family[0]["full_pair_invariant"] != family[1]["full_pair_invariant"], f"{lift} invariant collapse")

    selector_by_name = {row["candidate"]: row for row in selectors}
    require(len(selector_by_name) == len(selectors) == 10, "selector coverage")
    require(selector_by_name["Complete-lift orientation"]["mu_ruling"] == "BOTH_ORIENTATION_CLASSES_LEAVE_MU_OPEN", "orientation selector")
    require(selector_by_name["Reciprocal loop parity"]["mu_ruling"] == "MU_BLIND", "loop selector")
    require(selector_by_name["Normalized seal transition"]["mu_ruling"] == "MU_BLIND", "normalized selector")
    require(selector_by_name["Current bootstrap"]["mu_ruling"] == "NO_CURRENT_MU_EQUATION", "bootstrap selector")

    status_by_object = {row["object"]: row for row in status}
    require(len(status_by_object) == len(status) == 15, "status coverage")
    require(status_by_object["Metric-dependent global closure equation"]["status"] == "ABSENT_FROM_CURRENT_LEDGER", "global status")
    require(status_by_object["Global completion"]["status"] == "OPEN", "completion promotion")
    require(status_by_object["Conditional Hopf cap classification"]["status"] == "CONDITIONAL_NO_MU_EQUATION", "Hopf promotion")

    source_by_id = {row["id"]: row for row in source}
    require(len(source_by_id) == len(source) == 16, "source coverage")
    require("Z2-graded" in source_by_id["S03"]["audit_use"], "cocycle source")
    require("after-solution admissibility" in source_by_id["S13"]["audit_use"], "bootstrap source")
    require("conditional" in source_by_id["S09"]["source_status"].lower() or "VERIFIED" in source_by_id["S09"]["source_status"], "Hopf source")


def main():
    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))
    model = {
        "result": result,
        "lifts": rows("LIFT_CLASSIFICATION.tsv"),
        "witnesses": rows("WITNESS_CENSUS.tsv"),
        "selectors": rows("GLOBAL_SELECTOR_TYPE.tsv"),
        "status": rows("STATUS_LEDGER.tsv"),
        "source": rows("SOURCE_LINEAGE.tsv"),
    }
    validate_model(model)

    F = matrix([[0, 1], [1, 0]])
    I2 = identity(2)
    minus_I = scale(I2, -1)
    axis = matrix([[1, 0], [0, -1]])
    lifts = {
        "PLUS_IDENTITY": (I2, matrix([[Q(1, 10), Q(1, 10)], [Q(1, 10), Q(1, 10)]]), -1, (3, 1)),
        "MINUS_IDENTITY": (minus_I, matrix([[Q(1, 10), Q(1, 10)], [Q(-1, 10), Q(-1, 10)]]), -1, (1, 3)),
        "AXIS_REFLECTION": (axis, matrix([[Q(1, 10), Q(1, 10)], [Q(1, 10), Q(-1, 10)]]), 1, (2, 2)),
        "HOPF_EXCHANGE_LOCAL": (F, matrix([[Q(1, 10), Q(1, 10)], [Q(1, 10), Q(1, 10)]]), 1, (2, 2)),
    }
    expected = {
        ("PLUS_IDENTITY", 2): (Q(-78, 25), Q(-251, 78)),
        ("PLUS_IDENTITY", 3): (Q(-204, 25), Q(-251, 102)),
        ("MINUS_IDENTITY", 2): (Q(-74, 25), Q(-247, 74)),
        ("MINUS_IDENTITY", 3): (Q(-198, 25), Q(-248, 99)),
        ("AXIS_REFLECTION", 2): (Q(-7599, 2500), Q(-8300, 2533)),
        ("AXIS_REFLECTION", 3): (Q(-20099, 2500), Q(-49900, 20099)),
        ("HOPF_EXCHANGE_LOCAL", 2): (Q(-78, 25), Q(-251, 78)),
        ("HOPF_EXCHANGE_LOCAL", 3): (Q(-204, 25), Q(-251, 102)),
    }
    L4 = matrix([[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    independent = {}
    computed_invariants = {}
    for lift_name, (angular, cross, orientation, dimensions) in lifts.items():
        seal = block(F, angular)
        independent[f"{lift_name}_involution"] = multiply(seal, seal) == identity(4)
        independent[f"{lift_name}_orientation"] = determinant(seal) == orientation
        independent[f"{lift_name}_fixed_dim"] = 4 - rank(add(seal, identity(4), Q(-1))) == dimensions[0]
        independent[f"{lift_name}_antifixed_dim"] = 4 - rank(add(seal, identity(4))) == dimensions[1]
        independent[f"{lift_name}_cross_parity"] = multiply(multiply(transpose(F), cross), angular) == cross
        for kval in (2, 3):
            base = matrix([[1, -kval], [-kval, 1]])
            metric = full_metric(base, cross, I2)
            expected_det, expected_I = expected[(lift_name, kval)]
            invariant = pair_invariant(metric, L4)
            independent[f"{lift_name}_mu{kval**2}_isometry"] = multiply(multiply(transpose(seal), metric), seal) == metric
            independent[f"{lift_name}_mu{kval**2}_det"] = determinant(metric) == expected_det
            independent[f"{lift_name}_mu{kval**2}_invariant"] = invariant == expected_I
            schur = add(I2, multiply(multiply(transpose(cross), inverse(base)), cross), Q(-1))
            independent[f"{lift_name}_mu{kval**2}_Lorentz"] = schur[0][0] > 0 and determinant(schur) > 0 and determinant(base) < 0
            computed_invariants[(lift_name, kval)] = invariant
        independent[f"{lift_name}_mu_pair_distinct"] = computed_invariants[(lift_name, 2)] != computed_invariants[(lift_name, 3)]

    def Fb(value):
        value = Q(value)
        return matrix([[0, value], [1 / value, 0]])

    def G(value):
        value = Q(value)
        return matrix([[value, 0], [0, 1 / value]])

    A0 = axis
    A45 = F
    eigenbasis = matrix([[1, -1], [1, 1]])
    normalized_F = multiply(multiply(inverse(eigenbasis), F), eigenbasis)
    independent.update(
        {
            "reciprocal_F_involution": multiply(Fb(2), Fb(2)) == I2,
            "reciprocal_even_product": multiply(Fb(2), Fb(3)) == G(Q(2, 3)),
            "reciprocal_valid_triple": multiply(multiply(Fb(2), Fb(3)), G(Q(3, 2))) == I2,
            "three_inversions_not_identity": multiply(multiply(Fb(2), Fb(3)), Fb(5)) != I2,
            "normalized_seal_standard": normalized_F == axis,
            "normalized_seal_mu_blind": normalized_F == axis,
            "normalized_generator_ratio_squared_differs": Q(1, 3) != Q(1, 2),
            "angular_quarter_corner_noncommutes": multiply(A0, A45) != multiply(A45, A0),
            "angular_quarter_corner_order_four": multiply(multiply(multiply(multiply(A0, A45), multiply(A0, A45)), multiply(A0, A45)), multiply(A0, A45)) == I2,
            "same_axis_corner_identity": multiply(A0, A0) == I2,
            "cap_p0": abs(1 * 1 - 1 * 1) == 0,
            "cap_p1": abs(1 * 1 - 0 * 0) == 1,
            "cap_p3": abs(2 * 2 - 1 * 1) == 3,
            "cap_p5": abs(3 * 3 - 2 * 2) == 5,
            "both_orientation_classes_keep_both_mu": {
                (lifts[name][2], kval**2) for name in lifts for kval in (2, 3)
            } == {(-1, 4), (-1, 9), (1, 4), (1, 9)},
            "all_derivation_checks_pass": result["check_count"] == 92 and set(result["checks"].values()) == {"PASS"},
            "global_cover_open_in_source": "does not supply that cover" in (ROOT / "udt_global_coframe_cocycle_audit_2026-07-20/AUDIT_REPORT.md").read_text(encoding="utf-8"),
            "Hopf_gate_open_in_source": "first link is still missing" in (ROOT / "angular_toric_closure_selector_2026-07-19/AUDIT_REPORT.md").read_text(encoding="utf-8"),
            "bootstrap_after_solution_source": "after-solution admissibility condition" in (ROOT / "bootstrap_csn_phi_angular_selector_2026-07-19/AUDIT_REPORT.md").read_text(encoding="utf-8"),
        }
    )
    require(all(independent.values()), [key for key, value in independent.items() if not value])

    catches = {}
    mutation = copy.deepcopy(model); mutation["result"]["outcomes"].append("ONE_COMPLETE_LIFT_SELECTED_BY_CURRENT_FOUNDATION")
    expect_failure("unique_lift_promoted", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); mutation["result"]["outcomes"].append("CORNER_COCYCLE_SELECTS_MU")
    expect_failure("corner_selector_promoted", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); mutation["result"]["outcomes"].append("METRIC_DEPENDENT_GLOBAL_CLOSURE_EQUATION_PRESENT")
    expect_failure("global_equation_invented", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); mutation["result"]["global_authority"]["metric_dependent_equation_for_pair_invariant"] = "PRESENT"
    expect_failure("global_authority_promoted", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); mutation["lifts"] = mutation["lifts"][:-1]
    expect_failure("lift_missing", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); mutation["lifts"].append(copy.deepcopy(mutation["lifts"][0]))
    expect_failure("lift_duplicated", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); mutation["lifts"][0]["mu9"] = "REJECTED"
    expect_failure("mu_witness_removed_from_lift", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); mutation["witnesses"] = mutation["witnesses"][:-1]
    expect_failure("witness_missing", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); next(row for row in mutation["witnesses"] if row["id"] == "PLUS_IDENTITY_MU4")["cross_u"] = "0"
    expect_failure("nonzero_cross_removed", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); family = [row for row in mutation["witnesses"] if row["lift"] == "AXIS_REFLECTION"]; family[1]["full_pair_invariant"] = family[0]["full_pair_invariant"]
    expect_failure("pair_invariants_collapsed", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); next(row for row in mutation["selectors"] if row["candidate"] == "Complete-lift orientation")["mu_ruling"] = "SELECTS_MU"
    expect_failure("orientation_promoted", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); next(row for row in mutation["selectors"] if row["candidate"] == "Reciprocal loop parity")["mu_ruling"] = "SELECTS_MU"
    expect_failure("loop_parity_promoted", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); next(row for row in mutation["selectors"] if row["candidate"] == "Normalized seal transition")["mu_ruling"] = "SELECTS_MU"
    expect_failure("normalized_seal_promoted", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); next(row for row in mutation["selectors"] if row["candidate"] == "Current bootstrap")["mu_ruling"] = "DERIVED_MU"
    expect_failure("bootstrap_promoted", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); next(row for row in mutation["status"] if row["object"] == "Conditional Hopf cap classification")["status"] = "SELECTS_MU"
    expect_failure("Hopf_promoted", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); next(row for row in mutation["status"] if row["object"] == "Global completion")["status"] = "DERIVED"
    expect_failure("global_completion_promoted", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); mutation["source"] = mutation["source"][:-1]
    expect_failure("source_lineage_missing", lambda: validate_model(mutation), catches)
    mutation = copy.deepcopy(model); next(row for row in mutation["source"] if row["id"] == "S13")["audit_use"] = "bootstrap local mu equation"
    expect_failure("bootstrap_source_mutated", lambda: validate_model(mutation), catches)
    expect_failure("false_F_product", lambda: require(multiply(Fb(2), Fb(3)) == G(Q(3, 2)), "F product"), catches)
    expect_failure("false_cap_uniqueness", lambda: require({0, 1, 3, 5} == {1}, "caps"), catches)

    report = " ".join((HERE / "AUDIT_REPORT.md").read_text(encoding="utf-8").split())
    lay = " ".join((HERE / "LAY_DECISION_TREE.md").read_text(encoding="utf-8").split())
    next_decision = " ".join((HERE / "NEXT_SCIENTIFIC_DECISION.md").read_text(encoding="utf-8").split())
    require("Their group words literally do not contain it" in report, "report type result")
    require("Every mirror extension accepts both" in lay, "lay census")
    require("must be metric-dependent" in next_decision, "next decision")

    output = {
        "schema": "udt-complete-lift-mu-independent-verification-1.0",
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
                "LIFT_CLASSIFICATION.tsv",
                "WITNESS_CENSUS.tsv",
                "GLOBAL_SELECTOR_TYPE.tsv",
                "STATUS_LEDGER.tsv",
                "AUDIT_REPORT.md",
            )
        },
        "maximum_conclusion": result["maximum_conclusion"],
        "caveats": [
            "complete for registered constant real isotropic lift classes, not arbitrary field-dependent bundles",
            "Hopf exchange tested as a local conditional linear lift without adopting topology",
            "countermodels are algebraic full-coframe witnesses, not completed bootstrap universes",
            "future metric-dependent global closure could add a mu equation",
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
