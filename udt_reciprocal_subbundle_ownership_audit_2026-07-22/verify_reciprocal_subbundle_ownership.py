#!/usr/bin/env python3
"""Independent exact-rational verifier for the reciprocal-subbundle audit.

This implementation imports neither the SymPy production derivation nor any
prior audit code.  It separately reconstructs the finite-dimensional controls,
source identities, table contract, and exercised corruption catches.
"""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import subprocess
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
BASE = "14b06fdc1434301de1516cd2dbc226ad3fa1a3e1"
PREREG_COMMIT = "8682669"


class ContractError(RuntimeError):
    pass


def require(condition: bool, label: str) -> None:
    if not condition:
        raise ContractError(label)


def run(*args: str, binary: bool = False):
    return subprocess.check_output(args, cwd=ROOT, text=not binary)


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def matrix(values):
    return [[F(value) for value in row] for row in values]


def shape(a):
    return len(a), len(a[0])


def transpose(a):
    return [list(row) for row in zip(*a)]


def add(a, b):
    return [[left + right for left, right in zip(arow, brow)] for arow, brow in zip(a, b)]


def sub(a, b):
    return [[left - right for left, right in zip(arow, brow)] for arow, brow in zip(a, b)]


def scale(value, a):
    return [[value * item for item in row] for row in a]


def mul(a, b):
    rows_a, cols_a = shape(a)
    rows_b, cols_b = shape(b)
    require(cols_a == rows_b, "matrix_shape")
    return [
        [sum((a[i][k] * b[k][j] for k in range(cols_a)), F(0)) for j in range(cols_b)]
        for i in range(rows_a)
    ]


def eye(size):
    return [[F(int(i == j)) for j in range(size)] for i in range(size)]


def diag(*entries):
    return [[F(entries[i]) if i == j else F(0) for j in range(len(entries))] for i in range(len(entries))]


def flatten(a):
    return [value for row in a for value in row]


def is_zero(a):
    return all(value == 0 for value in flatten(a))


def rank(a):
    work = [list(row) for row in a]
    row_count = len(work)
    col_count = len(work[0]) if work else 0
    pivot_row = 0
    for col in range(col_count):
        pivot = next((row for row in range(pivot_row, row_count) if work[row][col]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        divisor = work[pivot_row][col]
        work[pivot_row] = [value / divisor for value in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not work[row][col]:
                continue
            factor = work[row][col]
            work[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def inverse(a):
    size, cols = shape(a)
    require(size == cols, "inverse_square")
    work = [row + identity for row, identity in zip([list(row) for row in a], eye(size))]
    for col in range(size):
        pivot = next((row for row in range(col, size) if work[row][col]), None)
        require(pivot is not None, "inverse_nonsingular")
        work[col], work[pivot] = work[pivot], work[col]
        divisor = work[col][col]
        work[col] = [value / divisor for value in work[col]]
        for row in range(size):
            if row == col:
                continue
            factor = work[row][col]
            work[row] = [value - factor * pivot_value for value, pivot_value in zip(work[row], work[col])]
    return [row[size:] for row in work]


def determinant(a):
    size, cols = shape(a)
    require(size == cols, "det_square")
    work = [list(row) for row in a]
    result = F(1)
    for col in range(size):
        pivot = next((row for row in range(col, size) if work[row][col]), None)
        if pivot is None:
            return F(0)
        if pivot != col:
            work[col], work[pivot] = work[pivot], work[col]
            result *= -1
        value = work[col][col]
        result *= value
        for row in range(col + 1, size):
            factor = work[row][col] / value
            work[row] = [entry - factor * pivot_entry for entry, pivot_entry in zip(work[row], work[col])]
    return result


def basis_matrix(index: int, size: int = 4):
    result = [[F(0) for _ in range(size)] for _ in range(size)]
    result[index // size][index % size] = F(1)
    return result


def linear_operator_rank(generators, *, anticommutant: bool = False):
    columns = []
    size = len(generators[0])
    for index in range(size * size):
        unit = basis_matrix(index, size)
        values = []
        for generator in generators:
            if anticommutant:
                image = add(mul(mul(generator, unit), generator), unit)
            else:
                image = sub(mul(unit, generator), mul(generator, unit))
            values.extend(flatten(image))
        columns.append(values)
    coefficient = [list(row) for row in zip(*columns)]
    return rank(coefficient)


def algebra_basis(generators):
    size = len(generators[0])
    basis = []

    def add_independent(candidate):
        old = rank([flatten(value) for value in basis])
        new = rank([flatten(value) for value in basis + [candidate]])
        if new > old:
            basis.append(candidate)
            return True
        return False

    add_independent(eye(size))
    for generator in generators:
        add_independent(generator)
    changed = True
    while changed:
        changed = False
        snapshot = list(basis)
        for left in snapshot:
            for right in snapshot:
                if add_independent(mul(left, right)):
                    changed = True
    return basis


def projector(g, columns):
    gram = mul(mul(transpose(columns), g), columns)
    return mul(mul(mul(columns, inverse(gram)), transpose(columns)), g)


def independent_algebra() -> dict[str, object]:
    g = diag(-1, 1, 1, 1)
    seal = diag(1, -1, 1, 1)
    boost = matrix([[F(5, 3), 0, F(4, 3), 0], [0, 1, 0, 0], [F(4, 3), 0, F(5, 3), 0], [0, 0, 0, 1]])
    boost_inverse = matrix([[F(5, 3), 0, F(-4, 3), 0], [0, 1, 0, 0], [F(-4, 3), 0, F(5, 3), 0], [0, 0, 0, 1]])
    solder_0 = matrix([[1, 0], [0, 1], [0, 0], [0, 0]])
    solder_1 = mul(boost, solder_0)
    p0 = projector(g, solder_0)
    p1 = projector(g, solder_1)

    b02 = matrix([[0, 0, 1, 0], [0, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0]])
    b03 = matrix([[0, 0, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0], [1, 0, 0, 0]])
    r23 = matrix([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, -1], [0, 0, 1, 0]])
    boundary_nullity = 16 - linear_operator_rank([b02, b03, r23])
    boundary_a = diag(1, 0, 1, 1)
    boundary_b = diag(0, 1, 0, 0)

    r12 = matrix([[0, 0, 0, 0], [0, 0, -1, 0], [0, 1, 0, 0], [0, 0, 0, 0]])
    r13 = matrix([[0, 0, 0, 0], [0, 0, 0, -1], [0, 0, 0, 0], [0, 1, 0, 0]])
    timelike_nullity = 16 - linear_operator_rank([r12, r13, r23])
    timelike_a = diag(1, 0, 0, 0)
    timelike_b = diag(0, 1, 1, 1)

    null_metric = matrix([[0, -1, 0, 0], [-1, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    n1 = matrix([[0, 0, 1, 0], [0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]])
    n2 = matrix([[0, 0, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 0, 0]])
    nr = matrix([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, -1], [0, 0, 1, 0]])
    null_nullity = 16 - linear_operator_rank([n1, n2, nr])
    null_nilpotent = matrix([[0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    null_identity = eye(4)

    ricci = diag(1, 2, 3, 4)
    ricci_planes = [diag(1, 1, 0, 0), diag(1, 0, 1, 0), diag(1, 0, 0, 1)]
    dense = matrix([[1, 1, 1, 1]] * 4)
    full_basis = algebra_basis([ricci, dense])
    full_commutant_nullity = 16 - linear_operator_rank([ricci, dense])

    plus = diag(1, 1)
    minus = diag(-1, -1)
    reflection = diag(1, -1)
    hodge = matrix([[0, -1], [1, 0]])
    complement = mul(hodge, reflection)

    k = matrix([[0, 1], [1, 0]])
    reciprocal = diag(2, F(1, 2))
    scaled_projector = projector(scale(F(7), g), solder_0)

    checks = {
        "reciprocal_pairing": is_zero(sub(mul(mul(transpose(reciprocal), k), reciprocal), k)),
        "boost_metric": is_zero(sub(mul(mul(transpose(boost), g), boost), g)),
        "boost_inverse": mul(boost, boost_inverse) == eye(4),
        "boost_proper": determinant(boost) == 1,
        "boost_seal": is_zero(sub(mul(boost, seal), mul(seal, boost))),
        "projector_0": is_zero(sub(mul(p0, p0), p0)) and rank(p0) == 2 and is_zero(sub(mul(transpose(p0), g), mul(g, p0))),
        "projector_1": is_zero(sub(mul(p1, p1), p1)) and rank(p1) == 2 and is_zero(sub(mul(transpose(p1), g), mul(g, p1))),
        "projectors_distinct_and_related": p0 != p1 and p1 == mul(mul(boost, p0), boost_inverse),
        "same_induced_pair": mul(mul(transpose(solder_0), g), solder_0) == diag(-1, 1)
        and mul(mul(transpose(solder_1), g), solder_1) == diag(-1, 1),
        "same_seal_intertwining": mul(seal, solder_0) == mul(solder_0, diag(1, -1))
        and mul(seal, solder_1) == mul(solder_1, diag(1, -1)),
        "boundary_stabilizer_commutant": boundary_nullity == 2
        and all(is_zero(sub(mul(candidate, generator), mul(generator, candidate))) for candidate in (boundary_a, boundary_b) for generator in (b02, b03, r23)),
        "boundary_no_rank_two_invariant": sorted({0, rank(boundary_b), rank(boundary_a), 4}) == [0, 1, 3, 4],
        "timelike_no_rank_two_invariant": timelike_nullity == 2
        and rank([flatten(timelike_a), flatten(timelike_b)]) == 2
        and all(is_zero(sub(mul(candidate, generator), mul(generator, candidate))) for candidate in (timelike_a, timelike_b) for generator in (r12, r13, r23))
        and sorted({0, rank(timelike_a), rank(timelike_b), 4}) == [0, 1, 3, 4],
        "null_little_algebra": null_nullity == 2
        and all(is_zero(add(mul(mul(transpose(generator), null_metric), eye(4)), mul(null_metric, generator))) for generator in (n1, n2, nr))
        and rank([flatten(null_identity), flatten(null_nilpotent)]) == 2
        and all(is_zero(sub(mul(candidate, generator), mul(generator, candidate))) for candidate in (null_identity, null_nilpotent) for generator in (n1, n2, nr))
        and is_zero(mul(null_nilpotent, null_nilpotent)),
        # Every commutant element is a*I+b*N.  Idempotence gives a^2=a and
        # (2a-1)b=0, hence exactly (a,b)=(0,0),(1,0), with ranks 0 and 4.
        "null_no_rank_two_idempotent": all(
            is_zero(sub(mul(add(scale(F(a), null_identity), scale(F(b), null_nilpotent)), add(scale(F(a), null_identity), scale(F(b), null_nilpotent))), add(scale(F(a), null_identity), scale(F(b), null_nilpotent))))
            for a, b in ((0, 0), (1, 0))
        ) and [rank(matrix_value) for matrix_value in (scale(F(0), null_identity), null_identity)] == [0, 4],
        "ricci_three_pairings": len(ricci_planes) == 3 and all(is_zero(sub(mul(p, ricci), mul(ricci, p))) and rank(p) == 2 for p in ricci_planes),
        "full_algebra": len(full_basis) == 16 and full_commutant_nullity == 1,
        "flat_ambiguity": is_zero(mul(matrix([[0] * 4] * 4), p0)) and is_zero(mul(matrix([[0] * 4] * 4), p1)),
        "seal_lifts": 4 - linear_operator_rank([plus], anticommutant=True) == 0
        and 4 - linear_operator_rank([minus], anticommutant=True) == 0
        and 4 - linear_operator_rank([reflection], anticommutant=True) == 2,
        "reflection_complement": mul(complement, complement) == eye(2)
        and sum(complement[i][i] for i in range(2)) == 0
        and transpose(complement) == complement
        and is_zero(add(mul(mul(reflection, complement), reflection), complement)),
        "orientation_hodge_not_involution": mul(hodge, hodge) == scale(F(-1), eye(2)),
        "csn_projector_invariance": scaled_projector == p0,
    }
    require(all(checks.values()), "independent_exact_algebra")
    return {
        "checks": checks,
        "exact_checks": len(checks),
        "boundary_invariant_ranks": [0, 1, 3, 4],
        "timelike_invariant_ranks": [0, 1, 3, 4],
        "null_invariant_ranks": [0, 4],
        "full_algebra_dimension": len(full_basis),
        "angular_anticommutant_dimensions": {"PLUS_IDENTITY": 0, "MINUS_IDENTITY": 0, "AXIS_REFLECTION": 2},
    }


EXPECTED_SELECTOR = {
    "SC01": "DERIVED_ABSTRACT_REPRESENTATION",
    "SC02": "NOT_DERIVED_TYPE_GAP",
    "SC06": "NOT_A_RANK_TWO_SELECTOR_EXACT",
    "SC07": "NOT_A_RANK_TWO_SELECTOR_EXACT",
    "SC08": "NOT_A_RANK_TWO_SELECTOR_EXACT",
    "SC09": "NOT_A_RANK_TWO_SELECTOR_EXACT",
    "SC11": "ABSENT_IN_REGISTERED_METRIC_ACTIVE_ENSEMBLE",
    "SC12": "MAXIMALLY_AMBIGUOUS_IN_REGISTERED_ENSEMBLE",
    "SC14": "NEUTRAL_NOT_DIRECTION_SELECTING",
    "SC15": "MULTIPLE_COMPLETIONS",
    "SC16": "DERIVED_CONDITIONAL_AT_SEAL",
    "SC18": "UNIQUE_IF_A_SUPPLIED_REDUCTION_EXISTS",
    "SC20": "NO_OPERATIONAL_SELECTOR_PRESENT",
    "SC21": "RECIPROCAL_SUBBUNDLE_AND_SOLDERING_NOT_DERIVED",
}

EXPECTED_STATUS = {
    "S02": "NOT_DERIVED",
    "S03": "REFUTED_AS_CURRENT_PREMISE_ENTAILMENT",
    "S04": "REFUTED_AS_CURRENT_PREMISE_ENTAILMENT",
    "S09": "DERIVED_CONDITIONAL_AT_SEAL",
    "S11": "REFUTED_LOGICAL_REVERSAL",
    "S12": "NOT_PRESENT",
    "S13": "NOT_DERIVED",
    "S14": "NOT_DERIVED",
    "S15": "NOT_DERIVED",
    "S16": "NOT_DERIVED",
    "S17": "NOT_DERIVED",
    "S18": "NOT_CLAIMED",
    "S19": "VERIFIED_WITH_CAVEATS",
}


def validate_contract(selector, witnesses, spine, status, lineage) -> None:
    require(len(selector) == 21 and len({row["id"] for row in selector}) == 21, "selector_21_unique")
    require({row["id"] for row in selector} == {f"SC{i:02d}" for i in range(1, 22)}, "selector_ids")
    by_selector = {row["id"]: row for row in selector}
    for item, expected in EXPECTED_SELECTOR.items():
        require(by_selector[item]["status"] == expected, f"selector_status:{item}")
    require(len(witnesses) == 12 and len({row["witness_id"] for row in witnesses}) == 12, "witness_12_unique")
    require({row["witness_id"] for row in witnesses} == {
        "W01_BOUNDARY_PLANE_0", "W02_BOUNDARY_PLANE_BOOSTED", "W03_BOUNDARY_STABILIZER",
        "W04_TIMELIKE_DPHI", "W05_NULL_DPHI", "W06_SIMPLE_RICCI", "W07_FULL_ALGEBRA",
        "W08_FLAT", "W09_SEAL_PLUS_IDENTITY", "W10_SEAL_MINUS_IDENTITY",
        "W11_SEAL_REFLECTION", "W12_CSN",
    }, "witness_ids")
    require(len(spine) == 10 and {row["step"] for row in spine} == {f"D{i:02d}" for i in range(1, 11)}, "spine_10")
    require({row["step"]: row for row in spine}["D08"]["status"] == "CONDITIONAL_INTEGRABILITY_REQUIREMENT", "global_continuation_conditional")
    require(len(status) == 19 and {row["id"] for row in status} == {f"S{i:02d}" for i in range(1, 20)}, "status_19")
    by_status = {row["id"]: row for row in status}
    for item, expected in EXPECTED_STATUS.items():
        require(by_status[item]["status"] == expected, f"status_value:{item}")
    require(len(lineage) == 15 and {row["source_id"] for row in lineage} == {f"S{i:02d}" for i in range(1, 16)}, "lineage_15")
    source_ids = {row["source_id"] for row in lineage}
    for row in selector:
        refs = set(row["sources"].split(";"))
        require(refs and refs.issubset(source_ids), f"selector_sources:{row['id']}")


def verify_lineage(lineage) -> None:
    for row in lineage:
        path = row["path"]
        data = run("git", "show", f"{BASE}:{path}", binary=True)
        require(run("git", "rev-parse", f"{BASE}:{path}").strip() == row["git_blob"], f"lineage_blob:{path}")
        require(hashlib.sha256(data).hexdigest() == row["sha256"], f"lineage_sha:{path}")
        require(str(len(data)) == row["bytes"], f"lineage_bytes:{path}")
        lines = data.decode("utf-8").splitlines()
        anchor = lines[int(row["anchor_line"]) - 1]
        require(hashlib.sha256(anchor.encode()).hexdigest() == row["anchor_sha256"], f"lineage_anchor:{path}")
        require(row["firewall"] == "POST_FIREWALL_AFFIRMATIVE_ELIGIBLE", f"lineage_firewall:{path}")


def compare_production(independent, production) -> None:
    require(production["status"] == "PASS", "production_status")
    require(production["counts"]["exact_checks"] == 27, "production_27")
    require(all(production["checks"].values()), "production_all_checks")
    require(production["counts"]["stabilizer_invariant_projector_ranks"] == independent["boundary_invariant_ranks"], "boundary_rank_agreement")
    require(production["counts"]["timelike_dphi_invariant_projector_ranks"] == independent["timelike_invariant_ranks"], "timelike_rank_agreement")
    require(production["counts"]["null_dphi_invariant_projector_ranks"] == independent["null_invariant_ranks"], "null_rank_agreement")
    require(production["counts"]["full_algebra_dimension"] == independent["full_algebra_dimension"], "full_algebra_agreement")
    require(production["counts"]["angular_lift_anticommutant_dimensions"] == independent["angular_anticommutant_dimensions"], "lift_agreement")


def verify_scope() -> list[str]:
    require(run("git", "merge-base", BASE, "HEAD").strip() == BASE, "base_ancestry")
    prereg_paths = run("git", "diff-tree", "--no-commit-id", "--name-only", "-r", PREREG_COMMIT).strip().splitlines()
    require(prereg_paths == [f"{HERE.name}/PREREGISTRATION.md"], "prereg_commit_scope")
    changed = []
    for line in run("git", "status", "--porcelain").splitlines():
        path = line[3:].split(" -> ")[-1]
        require(path.startswith(HERE.name + "/"), f"out_of_scope:{path}")
        changed.append(path)
    return changed


def catches(selector, witnesses, spine, status, lineage, production) -> list[dict[str, str]]:
    result = []

    def expect(label, mutation):
        values = [copy.deepcopy(value) for value in (selector, witnesses, spine, status, lineage)]
        mutation(*values)
        try:
            validate_contract(*values)
        except ContractError as exc:
            result.append({"catch_id": label, "result": "PASS_REJECTED", "caught_by": str(exc)})
        else:
            raise ContractError(f"mutation_false_pass:{label}")

    expect("C01_MISSING_SELECTOR", lambda s,w,d,t,l: s.pop())
    expect("C02_DUPLICATE_SELECTOR", lambda s,w,d,t,l: s.append(copy.deepcopy(s[0])))
    expect("C03_PROMOTE_COMPLETE_SELECTION", lambda s,w,d,t,l: next(r for r in s if r["id"]=="SC21").update(status="DERIVED"))
    expect("C04_PROMOTE_SPACELIKE_DPHI", lambda s,w,d,t,l: next(r for r in s if r["id"]=="SC06").update(status="DERIVED"))
    expect("C05_DROP_NULL_STRATUM", lambda s,w,d,t,l: s.remove(next(r for r in s if r["id"]=="SC08")))
    expect("C06_PROMOTE_REFLECTION_UNIVERSALLY", lambda s,w,d,t,l: next(r for r in s if r["id"]=="SC16").update(status="DERIVED_UNIVERSAL"))
    expect("C07_INVENT_BOOTSTRAP_SELECTOR", lambda s,w,d,t,l: next(r for r in s if r["id"]=="SC20").update(status="DERIVED_SELECTOR"))
    expect("C08_DROP_IDENTITY_LIFT_WITNESS", lambda s,w,d,t,l: w.remove(next(r for r in w if r["witness_id"]=="W09_SEAL_PLUS_IDENTITY")))
    expect("C09_DROP_REFLECTION_WITNESS", lambda s,w,d,t,l: w.remove(next(r for r in w if r["witness_id"]=="W11_SEAL_REFLECTION")))
    expect("C10_PROMOTE_GLOBAL_CONTINUATION", lambda s,w,d,t,l: next(r for r in d if r["step"]=="D08").update(status="DERIVED"))
    expect("C11_PROMOTE_METRIC_DERIVED_PHI", lambda s,w,d,t,l: next(r for r in t if r["id"]=="S16").update(status="DERIVED"))
    expect("C12_CLAIM_FUTURE_NO_GO", lambda s,w,d,t,l: next(r for r in t if r["id"]=="S18").update(status="PROVED_IMPOSSIBLE"))
    expect("C13_PROMOTE_ACTION", lambda s,w,d,t,l: next(r for r in t if r["id"]=="S17").update(status="DERIVED"))
    expect("C14_DROP_SOURCE", lambda s,w,d,t,l: l.pop())
    expect("C15_BAD_SELECTOR_SOURCE", lambda s,w,d,t,l: next(r for r in s if r["id"]=="SC01").update(sources="S99"))

    bad_lineage = copy.deepcopy(lineage)
    bad_lineage[0]["sha256"] = "0" * 64
    try:
        verify_lineage(bad_lineage)
    except ContractError as exc:
        result.append({"catch_id": "C16_SOURCE_HASH_MUTATION", "result": "PASS_REJECTED", "caught_by": str(exc)})
    else:
        raise ContractError("mutation_false_pass:C16")

    bad_production = copy.deepcopy(production)
    bad_production["counts"]["full_algebra_dimension"] = 15
    try:
        compare_production(independent_algebra(), bad_production)
    except ContractError as exc:
        result.append({"catch_id": "C17_FULL_ALGEBRA_MUTATION", "result": "PASS_REJECTED", "caught_by": str(exc)})
    else:
        raise ContractError("mutation_false_pass:C17")

    bad_production = copy.deepcopy(production)
    bad_production["counts"]["stabilizer_invariant_projector_ranks"] = [0, 1, 2, 3, 4]
    try:
        compare_production(independent_algebra(), bad_production)
    except ContractError as exc:
        result.append({"catch_id": "C18_FAKE_RANK_TWO_STABILIZER_PROJECTOR", "result": "PASS_REJECTED", "caught_by": str(exc)})
    else:
        raise ContractError("mutation_false_pass:C18")
    return result


def main() -> None:
    selector = rows("SELECTOR_CLASS_LEDGER.tsv")
    witnesses = rows("EXACT_WITNESS_LEDGER.tsv")
    spine = rows("DEDUCTIVE_SPINE.tsv")
    status = rows("STATUS_LEDGER.tsv")
    lineage = rows("SOURCE_LINEAGE.tsv")
    production = json.loads((HERE / "DERIVATION_RESULT.json").read_text(encoding="utf-8"))

    validate_contract(selector, witnesses, spine, status, lineage)
    verify_lineage(lineage)
    independent = independent_algebra()
    compare_production(independent, production)
    changed = verify_scope()
    caught = catches(selector, witnesses, spine, status, lineage, production)
    require(len(caught) == 18 and all(row["result"] == "PASS_REJECTED" for row in caught), "all_18_catches")

    with (HERE / "CATCH_PROOFS.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["catch_id", "result", "caught_by"], delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(caught)

    result = {
        "schema": "udt-reciprocal-subbundle-ownership-verification-1.0",
        "base": BASE,
        "status": "PASS",
        "grade_ceiling": "VERIFIED-WITH-CAVEATS_NO_FRESH_EXTERNAL_MODEL_SEMANTIC_REVIEW",
        "sources": len(lineage),
        "selector_rows": len(selector),
        "witness_rows": len(witnesses),
        "status_rows": len(status),
        "production_exact_checks": len(production["checks"]),
        "independent_exact_checks": independent["exact_checks"],
        "catch_proofs": {"passed": len(caught), "total": 18},
        "scope_only_package_changes": True,
        "changed_paths_observed": len(changed),
        "maximum_conclusion": "CURRENT_REGISTERED_PREMISES_DO_NOT_DERIVE_E_S_OR_T",
        "claims_not_made": [
            "future_no_go", "complete_metric_solution", "action", "source", "carrier",
            "boundary_charge", "mass", "scale", "physical_time", "topology_selection",
        ],
    }
    (HERE / "VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
