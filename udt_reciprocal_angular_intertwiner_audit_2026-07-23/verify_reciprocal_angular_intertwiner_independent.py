#!/usr/bin/env python3
"""Independent standard-library verifier for the reciprocal-angular audit."""

from __future__ import annotations

import copy
import csv
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
MAXIMUM = (
    "NONBLOCK_RECIPROCAL_ANGULAR_INTERTWINERS_EXIST_EXACTLY_FOR_MATCHED_"
    "REPRESENTATIONS_BUT_THE_COMPLETE_METRIC_RECIPROCITY_CSN_C_ANCHOR_"
    "SEAL_AND_FINITE_CELL_DO_NOT_SELECT_THE_MATCH__C_FIXES_CLOCK_RULER_"
    "CONVERSION_NOT_ANGULAR_NORMALIZATION"
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def matmul(a, b):
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def transpose(a):
    return [list(row) for row in zip(*a)]


def determinant2(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def negate(a):
    return [[-value for value in row] for row in a]


def determinant(matrix):
    work = [[Fraction(value) for value in row] for row in matrix]
    result = Fraction(1)
    for column in range(len(work)):
        pivot = next(
            (row for row in range(column, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            result *= -1
        value = work[column][column]
        result *= value
        for row in range(column + 1, len(work)):
            ratio = work[row][column] / value
            for inner in range(column, len(work)):
                work[row][inner] -= ratio * work[column][inner]
    return result


def rank_and_nullspace(matrix):
    work = [[Fraction(value) for value in row] for row in matrix]
    rows = len(work)
    columns = len(work[0]) if rows else 0
    pivots = []
    row = 0
    for column in range(columns):
        pivot = next((item for item in range(row, rows) if work[item][column]), None)
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        value = work[row][column]
        work[row] = [entry / value for entry in work[row]]
        for other in range(rows):
            if other == row or not work[other][column]:
                continue
            factor = work[other][column]
            work[other] = [
                work[other][index] - factor * work[row][index]
                for index in range(columns)
            ]
        pivots.append(column)
        row += 1
        if row == rows:
            break
    free = [index for index in range(columns) if index not in pivots]
    basis = []
    for free_column in free:
        vector = [Fraction(0) for _ in range(columns)]
        vector[free_column] = Fraction(1)
        for pivot_row, pivot_column in enumerate(pivots):
            vector[pivot_column] = -work[pivot_row][free_column]
        basis.append(vector)
    return len(pivots), basis


def coefficient(left_operator, right_operator):
    basis = [
        [[1, 0], [0, 0]],
        [[0, 1], [0, 0]],
        [[0, 0], [1, 0]],
        [[0, 0], [0, 1]],
    ]
    columns = []
    for candidate in basis:
        left = matmul(left_operator, candidate)
        right = matmul(candidate, right_operator)
        columns.append(
            [
                left[0][0] - right[0][0],
                left[0][1] - right[0][1],
                left[1][0] - right[1][0],
                left[1][1] - right[1][1],
            ]
        )
    return transpose(columns)


def maximum_rank(basis):
    if not basis:
        return 0
    for coefficients in itertools.product(range(-2, 3), repeat=len(basis)):
        if not any(coefficients):
            continue
        vector = [
            sum(Fraction(coefficients[j]) * basis[j][i] for j in range(len(basis)))
            for i in range(4)
        ]
        if determinant2([[vector[0], vector[1]], [vector[2], vector[3]]]):
            return 2
    return 1


L = [[-1, 0], [0, 1]]
F = [[0, 1], [1, 0]]
GENERATORS = {
    "G01_ANGULAR_IDENTITY": [[0, 0], [0, 0]],
    "G02_MATCHED_RECIPROCAL": L,
    "G03_INVERSE_RECIPROCAL": [[1, 0], [0, -1]],
    "G04_REPEATED_PLUS_WEIGHT": [[1, 0], [0, 1]],
    "G05_REPEATED_MINUS_WEIGHT": [[-1, 0], [0, -1]],
    "G06_ROTATION_GENERATOR": [[0, -1], [1, 0]],
    "G07_PLUS_JORDAN": [[1, 1], [0, 1]],
    "G08_ONE_MATCHED_ONE_GENERIC": [[-1, 0], [0, 2]],
    "G09_NO_MATCHED_REAL_WEIGHT": [[2, 0], [0, 3]],
    "G10_CONJUGATE_RECIPROCAL": [[-1, -2], [0, 1]],
}
SEALS = {
    "S01_PLUS_IDENTITY": [[1, 0], [0, 1]],
    "S02_MINUS_IDENTITY": [[-1, 0], [0, -1]],
    "S03_AXIS_REFLECTION": [[1, 0], [0, -1]],
    "S04_EXCHANGE": F,
    "S05_QUARTER_TURN": [[0, -1], [1, 0]],
}
COMBINED = {
    "C01_MATCHED_SAME_BASIS": (L, F),
    "C02_INVERSE_SAME_BASIS": ([[1, 0], [0, -1]], F),
    "C03_MATCHED_AXIS_BASIS": (F, [[1, 0], [0, -1]]),
    "C04_RECIPROCAL_PLUS_IDENTITY_SEAL": (L, [[1, 0], [0, 1]]),
    "C05_ANGULAR_SPECTATOR": ([[0, 0], [0, 0]], [[1, 0], [0, 1]]),
}


def load_bundle():
    return {
        "result": json.loads((HERE / "RESULT.json").read_text()),
        "generators": read_tsv("GENERATOR_INTERTWINER_ATLAS.tsv"),
        "bilinear": read_tsv("BILINEAR_CROSS_INVARIANT_ATLAS.tsv"),
        "seals": read_tsv("SEAL_INTERTWINER_ATLAS.tsv"),
        "combined": read_tsv("COMBINED_DIHEDRAL_INTERTWINER_ATLAS.tsv"),
        "combined_bilinear": read_tsv(
            "COMBINED_DIHEDRAL_BILINEAR_ATLAS.tsv"
        ),
        "anchor": read_tsv("C_ANCHOR_LEDGER.tsv"),
        "naturality": read_tsv("METRIC_NATURALITY_LEDGER.tsv"),
        "witnesses": read_tsv("CONDITIONAL_NONBLOCK_WITNESSES.tsv"),
        "completions": read_tsv("COMPLETION_SOLDERING_ATLAS.tsv"),
        "joins": read_tsv("JOIN_LEDGER.tsv"),
        "sources": read_tsv("SOURCE_LINEAGE.tsv"),
        "catches": read_tsv("CATCH_PROOFS.tsv"),
    }


def unique(rows, field, expected):
    values = [row[field] for row in rows]
    if len(rows) != expected or len(set(values)) != expected:
        raise AssertionError(field)
    return {row[field]: row for row in rows}


def validate(bundle):
    result = bundle["result"]
    if (
        result["maximum_conclusion"] != MAXIMUM
        or result["sympy_version"] != "1.14.0"
        or result["general_theorem"]["universal_natural_map_without_representation_match"]
        != "ZERO_ONLY"
        or result["c_anchor"]["commutes_with_D"] is not True
        or result["c_anchor"]["changes_intertwiner_rank"] is not False
        or result["c_anchor"]["fixes_angular_normalization"] is not False
    ):
        raise AssertionError("result")

    generators = unique(bundle["generators"], "case_id", 10)
    for case_id, generator in GENERATORS.items():
        _, basis = rank_and_nullspace(coefficient(L, generator))
        if (
            int(generators[case_id]["kernel_dimension"]) != len(basis)
            or int(generators[case_id]["maximum_S_rank"]) != maximum_rank(basis)
        ):
            raise AssertionError(case_id)
    if generators["G01_ANGULAR_IDENTITY"]["classification"] != "ZERO_ONLY":
        raise AssertionError("identity")
    if generators["G04_REPEATED_PLUS_WEIGHT"]["classification"] != "RANK_ONE_ONLY":
        raise AssertionError("rank-one")
    if generators["G10_CONJUGATE_RECIPROCAL"]["classification"] != "INVERTIBLE_AVAILABLE":
        raise AssertionError("conjugate")
    if int(generators["G02_MATCHED_RECIPROCAL"]["kernel_dimension"]) != 2:
        raise AssertionError("matched dimension")

    bilinear = unique(bundle["bilinear"], "case_id", 10)
    for generator_id, generator in GENERATORS.items():
        case_id = generator_id.replace("G", "B", 1)
        _, basis = rank_and_nullspace(coefficient(L, negate(generator)))
        if (
            int(bilinear[case_id]["kernel_dimension"]) != len(basis)
            or int(bilinear[case_id]["maximum_C_rank"])
            != maximum_rank(basis)
        ):
            raise AssertionError(case_id)
    if bilinear["B01_ANGULAR_IDENTITY"]["classification"] != "ZERO_ONLY":
        raise AssertionError("bilinear identity")
    if bilinear["B02_MATCHED_RECIPROCAL"]["classification"] != "INVERTIBLE_AVAILABLE":
        raise AssertionError("bilinear matched")

    seals = unique(bundle["seals"], "case_id", 5)
    for case_id, angular_seal in SEALS.items():
        _, basis = rank_and_nullspace(coefficient(F, angular_seal))
        if (
            int(seals[case_id]["kernel_dimension"]) != len(basis)
            or int(seals[case_id]["maximum_S_rank"]) != maximum_rank(basis)
        ):
            raise AssertionError(case_id)
    if int(seals["S01_PLUS_IDENTITY"]["maximum_S_rank"]) != 1:
        raise AssertionError("seal plus")
    if int(seals["S03_AXIS_REFLECTION"]["maximum_S_rank"]) != 2:
        raise AssertionError("seal axis")

    combined = unique(bundle["combined"], "case_id", 5)
    for case_id, (generator, angular_seal) in COMBINED.items():
        matrix = coefficient(L, generator) + coefficient(F, angular_seal)
        _, basis = rank_and_nullspace(matrix)
        if (
            int(combined[case_id]["kernel_dimension"]) != len(basis)
            or int(combined[case_id]["maximum_S_rank"]) != maximum_rank(basis)
        ):
            raise AssertionError(case_id)
    if int(combined["C01_MATCHED_SAME_BASIS"]["maximum_S_rank"]) != 2:
        raise AssertionError("combined matched")
    if int(combined["C04_RECIPROCAL_PLUS_IDENTITY_SEAL"]["maximum_S_rank"]) != 0:
        raise AssertionError("combined mismatch")

    combined_bilinear = unique(
        bundle["combined_bilinear"], "case_id", 5
    )
    for combined_id, (generator, angular_seal) in COMBINED.items():
        case_id = combined_id.replace("C", "D", 1)
        matrix = coefficient(L, negate(generator)) + coefficient(
            F, angular_seal
        )
        _, basis = rank_and_nullspace(matrix)
        if (
            int(combined_bilinear[case_id]["kernel_dimension"]) != len(basis)
            or int(combined_bilinear[case_id]["maximum_C_rank"])
            != maximum_rank(basis)
        ):
            raise AssertionError(case_id)
    if (
        int(
            combined_bilinear["D01_MATCHED_SAME_BASIS"][
                "maximum_C_rank"
            ]
        )
        != 2
    ):
        raise AssertionError("combined bilinear matched")

    anchor = unique(bundle["anchor"], "control_id", 5)
    if (
        anchor["A03_RAW_METRIC"]["selection_ruling"]
        != "OBSERVATIONAL_SCALE_EXPLICIT"
        or anchor["A05_ANGULAR_NORMALIZATION"]["selection_ruling"]
        != "C_DOES_NOT_FIX_ANGULAR_RADIUS"
    ):
        raise AssertionError("anchor")

    naturality = unique(bundle["naturality"], "candidate_id", 9)
    expected_naturality = {
        "N01_RAW_METRIC_CROSS_BLOCK": "NOT_FULL_FRAME_INVARIANT",
        "N02_PARITY_COMPATIBLE_NONZERO_CROSS_BLOCK": "ALLOWED_NOT_FORCED",
        "N04_RELATIVE_OPERATOR_FROM_G_AND_D": "WOULD_ASSUME_DESIRED_JOIN",
        "N05_NONNULL_DPHI_3PLUS3": "TRANSVERSE_DIRECTION_OR_SECTION_STILL_FREE",
    }
    for candidate, value in expected_naturality.items():
        if value not in naturality[candidate].values():
            raise AssertionError(candidate)

    witnesses = unique(bundle["witnesses"], "witness_id", 3)
    if (
        witnesses["W01_ZERO_CROSS_MATCHED"]["ruling"]
        != "ZERO_BRANCH_REMAINS_ADMISSIBLE"
        or witnesses["W02_NONZERO_MATCHED"]["signature"]
        != "LORENTZ_FOR_POSITIVE_C_AND_ABS_EPSILON_LESS_THAN_ONE"
        or witnesses["W03_NONZERO_INVERSE"]["ruling"]
        != "INVERSE_ASSIGNMENT_EQUALLY_COMPATIBLE"
    ):
        raise AssertionError("witnesses")

    completions = unique(bundle["completions"], "completion_id", 12)
    if (
        any(row["complete_g_phi_witness"] != "NO" for row in completions.values())
        or any(
            row["selection_ruling"]
            != "REGISTERED_ALTERNATIVE_NOT_SELECTED_BY_INTERTWINER"
            for row in completions.values()
        )
        or "SUPPLIED_CONDITIONALLY"
        not in completions["FC12_RECIPROCAL_TORIC_DIAGONAL"][
            "angular_representation_status"
        ]
    ):
        raise AssertionError("completions")

    joins = unique(bundle["joins"], "join_id", 8)
    if joins["J07"]["status"] != "OUT_OF_SCOPE_OPEN":
        raise AssertionError("action promotion")

    sources = unique(bundle["sources"], "path", 25)
    for relative, row in sources.items():
        path = ROOT / relative
        if (
            not path.is_file()
            or digest(path) != row["sha256"]
            or path.stat().st_size != int(row["size"])
        ):
            raise AssertionError("source")

    catches = unique(bundle["catches"], "catch_id", 29)
    if any(row["status"] != "CAUGHT" for row in catches.values()):
        raise AssertionError("catch labels")

    expected_counts = {
        "continuous_generator_cases": 10,
        "bilinear_cross_cases": 10,
        "seal_cases": 5,
        "combined_pair_cases": 5,
        "combined_bilinear_pair_cases": 5,
        "naturality_candidates": 9,
        "conditional_complete_metric_witnesses": 3,
        "completion_rows": 12,
        "complete_g_phi_witnesses": 0,
        "selected_completions": 0,
        "joins": 8,
        "sources": 25,
        "catch_proofs": 29,
    }
    if result["counts"] != expected_counts:
        raise AssertionError("counts")


def expect_failure(bundle, mutation):
    changed = copy.deepcopy(bundle)
    mutation(changed)
    try:
        validate(changed)
    except (AssertionError, KeyError, ValueError):
        return True
    raise AssertionError("mutation escaped")


def main():
    bundle = load_bundle()
    validate(bundle)

    numeric_general_checks = 0
    samples = [
        [[-1, 0], [0, 1]],
        [[1, 0], [0, -1]],
        [[0, -1], [1, 0]],
        [[2, 1], [3, 4]],
        [[-1, 2], [0, 5]],
        [[0, 1], [1, 0]],
    ]
    identity = [[1, 0], [0, 1]]
    for angular in samples:
        matrix = coefficient(L, angular)
        minus = [
            [angular[i][j] - identity[i][j] for j in range(2)]
            for i in range(2)
        ]
        plus = [
            [angular[i][j] + identity[i][j] for j in range(2)]
            for i in range(2)
        ]
        if determinant(matrix) != determinant2(minus) * determinant2(plus):
            raise AssertionError("general determinant")
        numeric_general_checks += 1

    for angular in (
        [[-1, 0], [0, 1]],
        [[1, 0], [0, -1]],
        [[0, 1], [1, 0]],
        [[-1, -2], [0, 1]],
    ):
        _, basis = rank_and_nullspace(coefficient(L, angular))
        if (angular[0][0] + angular[1][1], determinant2(angular)) == (0, -1):
            if maximum_rank(basis) != 2:
                raise AssertionError("trace determinant theorem")

    # c remains explicit in the dimension-matched metric but cannot enter L S=S B.
    for c_value in (Fraction(2), Fraction(3), Fraction(299792458)):
        metric_anchor = [[-c_value * c_value, 0], [0, 1]]
        if metric_anchor[0][0] != -(c_value**2):
            raise AssertionError("c metric")
        _, basis = rank_and_nullspace(coefficient(L, L))
        if maximum_rank(basis) != 2:
            raise AssertionError("c rank")

    # A cross chart manufactures a nonzero block from an exactly block metric.
    c_value = Fraction(3)
    radius = Fraction(5)
    kappa = Fraction(2)
    metric = [
        [-c_value**2, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, radius**2, 0],
        [0, 0, 0, radius**2],
    ]
    chart = [[1, 0, kappa, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    transformed = matmul(transpose(chart), matmul(metric, chart))
    if transformed[0][2] != -(c_value**2) * kappa:
        raise AssertionError("cross chart")
    if determinant(transformed) != determinant(metric):
        raise AssertionError("chart determinant")

    # Rebuild both nonzero complete-metric witnesses without reading their
    # saved matrices.  Use reciprocal weights a*b=1.
    c_value = Fraction(3)
    a_value = Fraction(2)
    b_value = Fraction(1, 2)
    epsilon = Fraction(1, 2)
    h_block = [
        [-(c_value**2) * (a_value**2), 0],
        [0, b_value**2],
    ]
    q_matched = [[a_value**2, 0], [0, b_value**2]]
    q_inverse = [[b_value**2, 0], [0, a_value**2]]
    c_matched = [[0, c_value * epsilon], [epsilon, 0]]
    c_inverse = [[c_value * epsilon, 0], [0, epsilon]]

    def assemble(h_block, c_block, q_block):
        return [
            h_block[0] + c_block[0],
            h_block[1] + c_block[1],
            [c_block[0][0], c_block[1][0]] + q_block[0],
            [c_block[0][1], c_block[1][1]] + q_block[1],
        ]

    expected_witness_det = -(c_value**2) * (
        1 + epsilon**2
    ) * (1 - epsilon**2)
    for witness in (
        assemble(h_block, c_matched, q_matched),
        assemble(h_block, c_inverse, q_inverse),
    ):
        if determinant(witness) != expected_witness_det:
            raise AssertionError("conditional witness determinant")
    if (
        -(c_value**2) * (1 + epsilon**2) >= 0
        or 1 - epsilon**2 <= 0
    ):
        raise AssertionError("conditional witness inertia")

    # Universal naturality under an independent angular scaling by 2 forces S=0.
    scale_equation = coefficient([[0, 0], [0, 0]], [[1, 0], [0, 1]])
    _, scale_basis = rank_and_nullspace(scale_equation)
    if scale_basis:
        raise AssertionError("independent scaling")

    mutations = [
        lambda b: b["generators"].pop(),
        lambda b: b["generators"].append(copy.deepcopy(b["generators"][0])),
        lambda b: b["generators"][0].__setitem__("classification", "INVERTIBLE_AVAILABLE"),
        lambda b: b["bilinear"][0].__setitem__("classification", "INVERTIBLE_AVAILABLE"),
        lambda b: b["generators"][3].__setitem__("maximum_S_rank", "2"),
        lambda b: b["generators"][9].__setitem__("classification", "ZERO_ONLY"),
        lambda b: b["generators"][1].__setitem__("kernel_dimension", "1"),
        lambda b: b["seals"].pop(),
        lambda b: b["seals"][0].__setitem__("maximum_S_rank", "2"),
        lambda b: b["seals"][2].__setitem__("maximum_S_rank", "0"),
        lambda b: b["combined"].pop(),
        lambda b: b["combined_bilinear"].pop(),
        lambda b: b["combined"][3].__setitem__("maximum_S_rank", "2"),
        lambda b: b["combined"][0].__setitem__("maximum_S_rank", "0"),
        lambda b: b["anchor"][2].__setitem__("selection_ruling", "C_REMOVED"),
        lambda b: b["anchor"][4].__setitem__("selection_ruling", "C_FIXES_ANGULAR_RADIUS"),
        lambda b: b["result"]["c_anchor"].__setitem__("changes_intertwiner_rank", True),
        lambda b: b["naturality"][0].__setitem__("frame_status", "FULL_FRAME_INVARIANT"),
        lambda b: b["naturality"][1].__setitem__("soldering_status", "FORCED_NONZERO"),
        lambda b: b["witnesses"][1].__setitem__("signature", "NOT_LORENTZ"),
        lambda b: b["naturality"][4].__setitem__("soldering_status", "DERIVED_WITHOUT_MAP"),
        lambda b: b["naturality"][5].__setitem__("soldering_status", "UNIQUE_ANGULAR_PLANE"),
        lambda b: b["completions"].pop(),
        lambda b: b["completions"].append(copy.deepcopy(b["completions"][0])),
        lambda b: b["completions"][0].__setitem__("selection_ruling", "SELECTED"),
        lambda b: next(
            row
            for row in b["completions"]
            if row["completion_id"] == "FC12_RECIPROCAL_TORIC_DIAGONAL"
        ).__setitem__("selection_ruling", "SELECTED"),
        lambda b: b["completions"][0].__setitem__("complete_g_phi_witness", "YES"),
        lambda b: b["joins"][7].__setitem__("status", "DERIVED"),
        lambda b: b["sources"][0].__setitem__("sha256", "0" * 64),
    ]
    passed = 0
    for mutation_index, mutation in enumerate(mutations, start=1):
        try:
            passed += expect_failure(bundle, mutation)
        except AssertionError as error:
            raise AssertionError(
                f"mutation {mutation_index} escaped"
            ) from error
    if passed != 29:
        raise AssertionError("catches")

    output = {
        "schema": "udt-reciprocal-angular-intertwiner-independent-1.0",
        "status": "PASS",
        "implementation": "stdlib_fraction_row_reduction_no_sympy_no_production_import",
        "continuous_cases": 10,
        "bilinear_cross_cases": 10,
        "seal_cases": 5,
        "combined_pair_cases": 5,
        "combined_bilinear_pair_cases": 5,
        "completion_rows": 12,
        "conditional_complete_metric_witnesses": 3,
        "source_hashes_replayed": 25,
        "general_determinant_controls": numeric_general_checks,
        "c_anchor_values_checked": ["2", "3", "299792458"],
        "cross_chart_control": "PASS",
        "conditional_lorentz_witness_controls": 2,
        "mutation_catches": 29,
        "mutation_catches_passed": passed,
        "maximum_conclusion": MAXIMUM,
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
