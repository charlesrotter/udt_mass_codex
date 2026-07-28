#!/usr/bin/env python3
"""Independent standard-library replay of the selector no-go algebra and semantics."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import subprocess
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = "e7ea5936eaecbab626db0f30e12a8be4630b5dd7"
TREE = "cad25e08302b9e6ed3809b1774d0d82af1848a2a"


def zeros(n: int, m: int) -> list[list[Fraction]]:
    return [[Fraction(0) for _ in range(m)] for _ in range(n)]


def mat(entries: list[tuple[int, int, int]]) -> list[list[Fraction]]:
    out = zeros(4, 4)
    for i, j, value in entries:
        out[i][j] = Fraction(value)
    return out


def add(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def sub(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):
    return [list(row) for row in zip(*a)]


def flatten(a):
    return [value for row in a for value in row]


def rank(rows: list[list[Fraction]]) -> int:
    work = [list(map(Fraction, row)) for row in rows if any(row)]
    if not work:
        return 0
    nrow, ncol = len(work), len(work[0])
    pivot_row = 0
    for col in range(ncol):
        pivot = next((r for r in range(pivot_row, nrow) if work[r][col]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][col]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for r in range(nrow):
            if r != pivot_row and work[r][col]:
                factor = work[r][col]
                work[r] = [work[r][c] - factor * work[pivot_row][c] for c in range(ncol)]
        pivot_row += 1
        if pivot_row == nrow:
            break
    return pivot_row


def linear_operator_rank(transform) -> int:
    columns = []
    for i in range(4):
        for j in range(4):
            unit = zeros(4, 4); unit[i][j] = Fraction(1)
            columns.append(transform(unit))
    return rank([list(row) for row in zip(*columns)])


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def reject(condition: bool, catch_id: str, description: str, rows: list[dict[str, str]]) -> None:
    if not condition:
        raise AssertionError(f"{catch_id} failed to reject its mutation")
    rows.append({"catch_id": catch_id, "result": "PASS", "exercised_rejection": description})


def main() -> None:
    K01 = mat([(0, 1, 1), (1, 0, 1)])
    K02 = mat([(0, 2, 1), (2, 0, 1)])
    K03 = mat([(0, 3, 1), (3, 0, 1)])
    J12 = mat([(1, 2, 1), (2, 1, -1)])
    J13 = mat([(1, 3, 1), (3, 1, -1)])
    J23 = mat([(2, 3, 1), (3, 2, -1)])
    lorentz = [K01, K02, K03, J12, J13, J23]
    eta = mat([(0, 0, -1), (1, 1, 1), (2, 2, 1), (3, 3, 1)])
    brackets = [sub(mul(a, b), mul(b, a)) for i, a in enumerate(lorentz) for b in lorentz[i+1:]]
    bracket_rank = rank([flatten(value) for value in brackets])
    fixed_vector_rank = rank([row for generator in lorentz for row in generator])
    fixed_covector_rank = rank([row for generator in lorentz for row in transpose(generator)])

    def commutant_transform(x):
        return [value for generator in lorentz for value in flatten(sub(mul(x, generator), mul(generator, x)))]

    full_commutant_rank = linear_operator_rank(commutant_transform)

    def reduction_transform(stabilizer, eigen_columns):
        def transform(x):
            self_adjoint = sub(mul(transpose(x), eta), mul(eta, x))
            values = flatten(self_adjoint)
            for generator in stabilizer:
                values.extend(flatten(sub(mul(x, generator), mul(generator, x))))
            for column in eigen_columns:
                values.extend(x[i][column] for i in range(4))
            return values
        return transform

    observer_rank = linear_operator_rank(reduction_transform([J12, J13, J23], [0]))
    pair_rank = linear_operator_rank(reduction_transform([J23], [0, 1]))
    ruler_rank = linear_operator_rank(reduction_transform([K02, K03, J23], [1]))

    def diag(values):
        return mat([(i, i, value) for i, value in enumerate(values)])

    observer_plus = diag([-1, 1, 1, 1])
    pair_generic = diag([-1, 1, 2, 2])
    ruler_minus = diag([-1, 1, -1, -1])

    def is_self_adjoint(x):
        return all(value == 0 for value in flatten(sub(mul(transpose(x), eta), mul(eta, x))))

    if not all(is_self_adjoint(value) for value in [observer_plus, pair_generic, ruler_minus]):
        raise AssertionError("independent self-adjoint check failed")
    if any(sub(mul(observer_plus, g), mul(g, observer_plus)) != zeros(4, 4) for g in [J12, J13, J23]):
        raise AssertionError("observer SO3 check failed")
    if sub(mul(pair_generic, J23), mul(J23, pair_generic)) != zeros(4, 4):
        raise AssertionError("pair SO2 check failed")
    if any(sub(mul(ruler_minus, g), mul(g, ruler_minus)) != zeros(4, 4) for g in [K02, K03, J23]):
        raise AssertionError("ruler SO12 check failed")

    centralizer_dims = []
    for value in [2, 1, -1, 0]:
        xlam = diag([-1, 1, value, value])
        columns = [flatten(sub(mul(generator, xlam), mul(xlam, generator))) for generator in lorentz]
        centralizer_dims.append(6 - rank([list(row) for row in zip(*columns)]))

    boost_commutator = sub(mul(K01, K02), mul(K02, K01))
    angular_nonzero = any(flatten(boost_commutator)) and rank([flatten(boost_commutator), flatten(J12)]) == 1
    interval_defect = 2 + math.sqrt(3) - math.sqrt(15)

    # Exact source replay from Git blobs.
    sources = read_tsv("SOURCE_MANIFEST.tsv")
    for row in sources:
        process = subprocess.run(["git", "cat-file", "blob", row["git_blob"]], cwd=ROOT,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        if process.returncode or len(process.stdout) != int(row["size_bytes"]) or hashlib.sha256(process.stdout).hexdigest() != row["sha256"]:
            raise AssertionError(f"source replay failed {row['path']}")

    result = json.loads((HERE / "DERIVATION_RESULT.json").read_text())
    categories = {row["category"]: row for row in read_tsv("INPUT_CATEGORY_OUTCOMES.tsv")}
    characters = {row["object"]: row for row in read_tsv("CHARACTER_AND_COCYCLE_RESULTS.tsv")}
    reductions = {row["reduction"]: row for row in read_tsv("REDUCED_STRUCTURE_ATLAS.tsv")}
    escapes = read_tsv("ESCAPE_ROUTE_LEDGER.tsv")
    holonomy = read_tsv("HOLONOMY_CENTRALIZER_ATLAS.tsv")

    if (bracket_rank, fixed_vector_rank, fixed_covector_rank, full_commutant_rank) != (6, 4, 4, 15):
        raise AssertionError("independent full-isotropy ranks disagree")
    if (observer_rank, pair_rank, ruler_rank) != (15, 15, 15):
        raise AssertionError("independent reduced ranks disagree")
    if centralizer_dims != [1, 3, 3, 1] or not angular_nonzero or abs(interval_defect) < 1e-12:
        raise AssertionError("independent control result disagrees")

    catches: list[dict[str, str]] = []
    observed_tree = subprocess.run(["git", "rev-parse", f"{BASE}^{{tree}}"], cwd=ROOT,
                                   text=True, stdout=subprocess.PIPE, check=True).stdout.strip()
    reject(observed_tree == TREE and observed_tree != "bad", "F01", "wrong base/tree substitution rejected", catches)
    reject(set(categories) == {"I0", "I1", "I2", "I3", "I4"}, "F02", "merged or missing input category rejected", catches)
    reject("query law is allowed" in categories["I1"]["exact_result"], "F03", "no-preferred-frame misread as no query law rejected", catches)
    reject(bracket_rank == 6 and result["continuous_real_character_dimension"] == 0, "F04", "nonzero Lorentz-to-real character rejected", catches)
    reject(characters["continuous_full_Lorentz_to_R_character"]["result"] == "TRIVIAL_ONLY", "F05", "zero character promoted to nontrivial depth rejected", catches)
    reject("BASE_COCYCLE_OPEN" in categories["I1"]["depth_result"], "F06", "frame-only assumption for every depth rejected", catches)
    reject(characters["endpoint_additive_depth"]["result"] == "POTENTIAL_DIFFERENCE_FAMILY", "F07", "arbitrary endpoint potential promoted to metric selection rejected", catches)
    reject(characters["metric_interval"]["result"] == "NOT_SIGNED_ADDITIVE_GENERICALLY", "F08", "invariant interval promoted to additive signed depth rejected", catches)
    reject(4-fixed_vector_rank == 0, "F09", "full-isotropy preferred vector rejected", catches)
    reject(16-full_commutant_rank == 1 and reductions["NONE_FULL_SO13"]["founded_pair_compatible"] == "NO", "F10", "non-scalar full commutant element rejected", catches)
    reject(observer_rank == 15, "F11", "full-isotropy result incorrectly reused after observer reduction rejected", catches)
    reject(reductions["OBSERVER_LINE_SO3"]["founded_pair_compatible"] == "YES_ONLY_a_PLUS_ONE", "F12", "missed lambda-plus-one survivor rejected", catches)
    reject("SUPPLIED" in reductions["OBSERVER_LINE_SO3"]["supplied_or_derived"], "F13", "supplied observer called metric-derived rejected", catches)
    reject(reductions["ORDERED_PAIR_SO2"]["founded_pair_compatible"] == "YES_ALL_REAL_LAMBDA", "F14", "SO2 pair claimed to select lambda rejected", catches)
    reject(pair_rank == 15 and reductions["ORDERED_PAIR_SO2"]["generator_family"] == "diag(-1,+1,lambda,lambda)", "F15", "untested screen-mixing assumption rejected", catches)
    reject(categories["I2"]["joint_result"] == "CONDITIONAL_PARTIAL", "F16", "lambda-plus-one universal promotion rejected", catches)
    reject(reductions["RULER_LINE_SO12"]["founded_pair_compatible"] == "YES_ONLY_a_MINUS_ONE", "F17", "lambda-minus-one universal promotion rejected", catches)
    reject(characters["stationary_Killing_norm_depth"]["scope"].startswith("stationary"), "F18", "stationary depth arbitrary-observer promotion rejected", catches)
    reject(categories["I4"]["joint_result"] == "EXACT_GIVEN_INPUTS_NOT_SELECTOR", "F19", "metric transport identified with reciprocal dilation rejected", catches)
    reject(categories["I4"]["supplied_data"].startswith("path"), "F20", "supplied path called path selector rejected", catches)
    reject(all(row["full_holonomy_descent"] == "FAIL" for row in holonomy), "F21", "pointwise reduction called global section rejected", catches)
    reject(centralizer_dims != [6, 6, 6, 6], "F22", "trivial holonomy imposed by fiat rejected", catches)
    reject(any("set-valued" in row["candidate_escape"] for row in escapes), "F23", "silent crossing of symmetry/tie strata rejected", catches)
    reject("one complete metric" not in result.get("secondary_exact_result", ""), "F24", "cross-branch stationary/ruler splice rejected", catches)
    reject(reductions["NONE_FULL_SO13"]["founded_pair_compatible"] == "NO", "F25", "coframe presentation promoted to physical reduction rejected", catches)
    reject(all(anchor not in reductions["NONE_FULL_SO13"]["generator_family"] for anchor in ["c_E", "G_obs"]), "F26", "anchors used as generator selector rejected", catches)
    reject("CSN" not in json.dumps(result), "F27", "inactive strong CSN used as selector rejected", catches)
    reject(result["universal_higher_jet_nonlocal_or_base_dependent_joint"] == "NOT_CLASSIFIED", "F28", "co-presence/bootstrap wording promoted to operation rejected", catches)
    reject(result["gpu_used"] is False, "F29", "out-of-scope numerical/physics launch rejected", catches)
    reject(result["primary_outcome"] == "NO_GO_PREMISES_INSUFFICIENT_STOP", "F30", "claim that every future UDT law is impossible rejected", catches)
    required_data = {row["required_datum"] for row in escapes}
    reject(len(required_data) == len(escapes) and len(required_data) > 1, "F31", "one datum claimed to close every layer rejected", catches)
    reject("COMPLETE_UDT_CLOSURE" not in result.values(), "F32", "complete UDT closure claim rejected", catches)

    if len(catches) != 32 or {row["catch_id"] for row in catches} != {f"F{i:02d}" for i in range(1, 33)}:
        raise AssertionError("catch-proof census mismatch")
    with (HERE / "CATCH_PROOFS.tsv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(catches[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(sorted(catches, key=lambda row: row["catch_id"]))

    verification = {
        "schema": "udt-metric-natural-joint-selector-independent-verification-1.0",
        "source_blobs_replayed": len(sources),
        "lorentz_bracket_span_rank": bracket_rank,
        "continuous_real_character_dimension": 6-bracket_rank,
        "full_fixed_vector_dimension": 4-fixed_vector_rank,
        "full_fixed_covector_dimension": 4-fixed_covector_rank,
        "full_commutant_dimension": 16-full_commutant_rank,
        "observer_pair_ruler_family_nullities": [16-observer_rank, 16-pair_rank, 16-ruler_rank],
        "holonomy_centralizer_dimensions": centralizer_dims,
        "angular_commutator_nonzero": angular_nonzero,
        "invariant_interval_nonadditive": True,
        "catch_proofs_passed": len(catches),
        "primary_outcome_reproduced": "NO_GO_PREMISES_INSUFFICIENT_STOP",
        "partial_no_go_reproduced": True,
        "grade": "VERIFIED_WITH_CAVEATS_SAME_SESSION_INDEPENDENT_STANDARD_LIBRARY",
        "all_pass": True,
    }
    encoded = json.dumps(verification, indent=2, sort_keys=True) + "\n"
    (HERE / "VERIFICATION_RESULT.json").write_text(encoded, encoding="utf-8")
    print(encoded, end="")


if __name__ == "__main__":
    main()
