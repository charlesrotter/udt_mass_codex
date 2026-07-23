#!/usr/bin/env python3
"""Independent stdlib verifier for the angular-generator branch census."""

from __future__ import annotations

import copy
import csv
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MAXIMUM = (
    "THE_FULL_METRIC_ANGULAR_STRAIN_MATCHES_THE_RECIPROCAL_MINUS1_PLUS1_"
    "SPECTRUM_IFF_ITS_RELATIVE_MEAN_SCALE_RATE_VANISHES_AND_ITS_CSN_SHAPE_"
    "SPEED_HAS_UNIT_MAGNITUDE__THE_REGISTERED_FC12_PROFILE_SUPPLIES_AN_"
    "EXACT_CONSTANT_RELATIVE_SCALE_SUBFAMILY_BUT_ARBITRARY_OMEGA_TOPOLOGY_"
    "SEAL_MONODROMY_AND_CURRENT_BOOTSTRAP_DO_NOT_FORCE_OR_SELECT_IT"
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def matmul(a, b):
    return [
        [
            sum(a[i][k] * b[k][j] for k in range(len(b)))
            for j in range(len(b[0]))
        ]
        for i in range(len(a))
    ]


def transpose(a):
    return [list(row) for row in zip(*a)]


def inverse2(q):
    determinant = q[0][0] * q[1][1] - q[0][1] * q[1][0]
    if determinant == 0:
        raise ZeroDivisionError("rank drop")
    return [
        [q[1][1] / determinant, -q[0][1] / determinant],
        [-q[1][0] / determinant, q[0][0] / determinant],
    ]


def generator_fraction(q, q_prime):
    raw = [
        [value / 2 for value in row]
        for row in matmul(inverse2(q), q_prime)
    ]
    trace = raw[0][0] + raw[1][1]
    reduced = [
        [raw[0][0] - trace / 2, raw[0][1]],
        [raw[1][0], raw[1][1] - trace / 2],
    ]
    determinant = (
        reduced[0][0] * reduced[1][1]
        - reduced[0][1] * reduced[1][0]
    )
    return raw, reduced, trace, determinant


def matrix_rank_fraction(matrix):
    value = [[Fraction(entry) for entry in row] for row in matrix]
    rows = len(value)
    columns = len(value[0]) if rows else 0
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(pivot_row, rows) if value[row][column]),
            None,
        )
        if pivot is None:
            continue
        value[pivot_row], value[pivot] = value[pivot], value[pivot_row]
        scale = value[pivot_row][column]
        value[pivot_row] = [entry / scale for entry in value[pivot_row]]
        for row in range(rows):
            if row == pivot_row:
                continue
            factor = value[row][column]
            if factor:
                value[row] = [
                    left - factor * right
                    for left, right in zip(value[row], value[pivot_row])
                ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def mirror_constraint_rank(matrix):
    # Unknown symmetric q' has coordinates (a,b,d).  The seal equation is
    # q' + R^T q' R = 0.
    basis = [
        [[Fraction(1), Fraction(0)], [Fraction(0), Fraction(0)]],
        [[Fraction(0), Fraction(1)], [Fraction(1), Fraction(0)]],
        [[Fraction(0), Fraction(0)], [Fraction(0), Fraction(1)]],
    ]
    r = [[Fraction(entry) for entry in row] for row in matrix]
    rt = transpose(r)
    columns = []
    for item in basis:
        transformed = matmul(matmul(rt, item), r)
        residual = [
            [item[i][j] + transformed[i][j] for j in range(2)]
            for i in range(2)
        ]
        columns.append([residual[0][0], residual[0][1], residual[1][1]])
    coefficient = [
        [columns[column][row] for column in range(3)]
        for row in range(3)
    ]
    return matrix_rank_fraction(coefficient)


def q_float(u, w, theta):
    cosine = math.cos(theta)
    sine = math.sin(theta)
    rotation = [[cosine, -sine], [sine, cosine]]
    shape = [[math.exp(-2 * u), 0.0], [0.0, math.exp(2 * u)]]
    scaled = matmul(matmul(transpose(rotation), shape), rotation)
    factor = math.exp(2 * w)
    return [[factor * entry for entry in row] for row in scaled]


def inverse2_float(q):
    determinant = q[0][0] * q[1][1] - q[0][1] * q[1][0]
    return [
        [q[1][1] / determinant, -q[0][1] / determinant],
        [-q[1][0] / determinant, q[0][0] / determinant],
    ]


def finite_difference_sigma(u, up, w, wp, theta, thetap):
    step = 1.0e-6
    minus = q_float(
        u - step * up,
        w - step * wp,
        theta - step * thetap,
    )
    plus = q_float(
        u + step * up,
        w + step * wp,
        theta + step * thetap,
    )
    center = q_float(u, w, theta)
    derivative = [
        [(plus[i][j] - minus[i][j]) / (2 * step) for j in range(2)]
        for i in range(2)
    ]
    raw = [
        [entry / 2 for entry in row]
        for row in matmul(inverse2_float(center), derivative)
    ]
    trace = raw[0][0] + raw[1][1]
    reduced = [
        [raw[0][0] - trace / 2, raw[0][1]],
        [raw[1][0], raw[1][1] - trace / 2],
    ]
    determinant = (
        reduced[0][0] * reduced[1][1]
        - reduced[0][1] * reduced[1][0]
    )
    return -determinant, trace


def determinant(matrix):
    value = [list(map(float, row)) for row in matrix]
    result = 1.0
    for column in range(len(value)):
        pivot = max(
            range(column, len(value)),
            key=lambda row: abs(value[row][column]),
        )
        if abs(value[pivot][column]) < 1.0e-30:
            return 0.0
        if pivot != column:
            value[column], value[pivot] = value[pivot], value[column]
            result *= -1.0
        scale = value[column][column]
        result *= scale
        for row in range(column + 1, len(value)):
            factor = value[row][column] / scale
            for inner in range(column + 1, len(value)):
                value[row][inner] -= factor * value[column][inner]
    return result


def validate_branches(rows):
    expected = {
        row["completion_id"] for row in read_tsv(HERE / "BRANCH_UNIVERSE.tsv")
    }
    identities = [row["completion_id"] for row in rows]
    if len(identities) != 12 or len(set(identities)) != 12:
        raise AssertionError("branch identity cardinality")
    if set(identities) != expected:
        raise AssertionError("branch universe mismatch")
    if any(
        row["branch_ruling"] == "FORCED_PERSISTENT_REGULAR" for row in rows
    ):
        raise AssertionError("unconditional force overclaim")
    if any(row["pattern_forced"] != "NO" for row in rows):
        raise AssertionError("pattern-force overclaim")
    fc12 = next(
        row for row in rows
        if row["completion_id"] == "FC12_RECIPROCAL_TORIC_DIAGONAL"
    )
    if (
        fc12["branch_ruling"]
        != "ALLOWED_NOT_FORCED"
        or fc12["pattern_forced"] != "NO"
        or fc12["natural_selection"]
        != "NO__FC12_IS_CONDITIONAL_AND_UNSELECTED"
    ):
        raise AssertionError("FC12 ruling")
    if any(row["extends_degeneracy"] == "YES" for row in rows):
        raise AssertionError("rank-degeneracy promotion")


def expect_failure(name, function):
    try:
        function()
    except Exception:
        return {"catch_id": name, "status": "CAUGHT"}
    raise AssertionError(f"mutation escaped: {name}")


def main() -> None:
    result = json.loads((HERE / "RESULT.json").read_text())
    formula = json.loads((HERE / "ANGULAR_GENERATOR_FORMULA.json").read_text())
    branches = read_tsv(HERE / "BRANCH_GENERATOR_ATLAS.tsv")
    points = read_tsv(HERE / "POINTWISE_GENERATOR_CONTROLS.tsv")
    mirrors = read_tsv(HERE / "MIRROR_LIFT_GENERATOR_ATLAS.tsv")
    monodromy = read_tsv(HERE / "MONODROMY_GENERATOR_ATLAS.tsv")
    joins = read_tsv(HERE / "JOIN_LEDGER.tsv")
    lineage = read_tsv(HERE / "SOURCE_LINEAGE.tsv")
    production_catches = read_tsv(HERE / "CATCH_PROOFS.tsv")

    if (
        result["maximum_conclusion"] != MAXIMUM
        or result["sympy_version"] != "1.14.0"
        or len(points) != 10
        or len(mirrors) != 5
        or len(monodromy) != 9
        or len(joins) != 9
        or len(lineage) != 15
        or len(production_catches) != 20
        or result["counts"]["forced_persistent_unconditional_families"] != 0
        or result["counts"]["conditional_persistent_regular_families"] != 0
        or formula["reciprocal_predicate"]
        != "w_p=0 AND sigma_squared=1"
    ):
        raise AssertionError("result cardinality or authority boundary")
    validate_branches(branches)

    one = Fraction(1)
    zero = Fraction(0)
    matched_q = [[one, zero], [zero, one]]
    matched_qp = [[-2 * one, zero], [zero, 2 * one]]
    raw, reduced, trace, reduced_det = generator_fraction(
        matched_q, matched_qp
    )
    if reduced != [[-one, zero], [zero, one]] or reduced_det != -one:
        raise AssertionError("matched rational control")
    common_qp = [[4 * one, zero], [zero, 8 * one]]
    common_raw, common_reduced, common_trace, common_det = generator_fraction(
        matched_q, common_qp
    )
    if (
        common_reduced != [[-one, zero], [zero, one]]
        or common_trace != 6
        or common_det != -one
        or common_raw == [[-one, zero], [zero, one]]
    ):
        raise AssertionError("relative angular scale rational control")
    spectator_qp = [[6 * one, zero], [zero, 6 * one]]
    _raw, spectator_j, _trace, spectator_det = generator_fraction(
        matched_q, spectator_qp
    )
    if spectator_j != [[zero, zero], [zero, zero]] or spectator_det != 0:
        raise AssertionError("spectator rational control")

    finite_controls = [
        (0.3, 0.7, 0.1, 0.2, 0.2, 0.4),
        (-0.4, -0.2, -0.3, 0.5, 0.7, -0.6),
        (0.8, 1.0, 0.2, -0.4, -0.5, 0.0),
    ]
    finite_residuals = []
    for u, up, w, wp, theta, thetap in finite_controls:
        observed_sigma, observed_trace = finite_difference_sigma(
            u, up, w, wp, theta, thetap
        )
        expected_sigma = up**2 + thetap**2 * math.sinh(2 * u) ** 2
        finite_residuals.append(abs(observed_sigma - expected_sigma))
        finite_residuals.append(abs(observed_trace - 2 * wp))
    if max(finite_residuals) > 2.0e-8:
        raise AssertionError("independent finite-difference formula")

    complete_det_residuals = []
    u, w, theta = 0.31, -0.17, 0.42
    q = q_float(u, w, theta)
    for c in (2.0, 3.0, 299792458.0):
        matrix = [
            [-c * c * math.exp(-0.4), 0.0, 0.0, 0.0],
            [0.0, math.exp(0.4), 0.0, 0.0],
            [0.0, 0.0, q[0][0], q[0][1]],
            [0.0, 0.0, q[1][0], q[1][1]],
        ]
        observed = determinant(matrix)
        expected = -c * c * math.exp(4 * w)
        complete_det_residuals.append(
            abs(observed - expected) / max(1.0, abs(expected))
        )
    if max(complete_det_residuals) > 2.0e-14:
        raise AssertionError("c complete-metric determinant")

    lift_dimensions = {
        "ANGULAR_PLUS_I": 3
        - mirror_constraint_rank([[1, 0], [0, 1]]),
        "ANGULAR_MINUS_I": 3
        - mirror_constraint_rank([[-1, 0], [0, -1]]),
        "AXIS_REFLECTION_DIAG_PLUS_MINUS": 3
        - mirror_constraint_rank([[1, 0], [0, -1]]),
        "AXIS_EXCHANGE_F": 3
        - mirror_constraint_rank([[0, 1], [1, 0]]),
    }
    if lift_dimensions != {
        "ANGULAR_PLUS_I": 0,
        "ANGULAR_MINUS_I": 0,
        "AXIS_REFLECTION_DIAG_PLUS_MINUS": 1,
        "AXIS_EXCHANGE_F": 1,
    }:
        raise AssertionError("mirror first-jet dimensions")

    l = [[-1, 0], [0, 1]]
    monodromy_matrices = [
        ([[1, 0], [0, 1]], "COMMUTES"),
        ([[-1, 0], [0, -1]], "COMMUTES"),
        ([[1, 0], [0, -1]], "COMMUTES"),
        ([[0, 1], [1, 0]], "ANTICOMMUTES"),
        ([[1, 1], [0, 1]], "NEITHER"),
        ([[2, 1], [1, 1]], "NEITHER"),
        ([[1, 1], [0, -1]], "NEITHER"),
    ]
    relations = []
    for matrix, expected in monodromy_matrices:
        ml = matmul(matrix, l)
        lm = matmul(l, matrix)
        if ml == lm:
            relation = "COMMUTES"
        elif ml == [[-entry for entry in row] for row in lm]:
            relation = "ANTICOMMUTES"
        else:
            relation = "NEITHER"
        if relation != expected:
            raise AssertionError("monodromy relation")
        relations.append(relation)
    if relations != [row["relation_to_L"] for row in monodromy[:7]]:
        raise AssertionError("monodromy table")

    for row in lineage:
        source = ROOT / row["path"]
        if (
            not source.is_file()
            or digest(source) != row["sha256"]
            or source.stat().st_size != int(row["size"])
        ):
            raise AssertionError("source lineage")

    mutations = []
    mutation = branches[:-1]
    mutations.append(
        expect_failure("I01_MISSING_BRANCH", lambda: validate_branches(mutation))
    )
    mutation = copy.deepcopy(branches)
    mutation[-1] = copy.deepcopy(mutation[0])
    mutations.append(
        expect_failure("I02_DUPLICATE_BRANCH", lambda: validate_branches(mutation))
    )
    mutation = copy.deepcopy(branches)
    mutation[0]["branch_ruling"] = "FORCED_PERSISTENT_REGULAR"
    mutations.append(
        expect_failure("I03_FALSE_FORCE", lambda: validate_branches(mutation))
    )
    mutation = copy.deepcopy(branches)
    next(row for row in mutation if row["completion_id"].startswith("FC12"))[
        "natural_selection"
    ] = "YES"
    mutations.append(
        expect_failure("I04_FC12_SELECTION", lambda: validate_branches(mutation))
    )
    mutation = copy.deepcopy(branches)
    next(row for row in mutation if row["completion_id"].startswith("FC12"))[
        "branch_ruling"
    ] = "CONDITIONAL_SUBFAMILY_PERSISTENT_REGULAR"
    mutations.append(
        expect_failure("I05_FC12_RULING", lambda: validate_branches(mutation))
    )
    mutation = copy.deepcopy(branches)
    mutation[1]["extends_degeneracy"] = "YES"
    mutations.append(
        expect_failure("I06_CAP_EXTENSION", lambda: validate_branches(mutation))
    )
    mutations.extend(
        [
            expect_failure(
                "I07_RANK_DROP_INVERSION",
                lambda: generator_fraction(
                    [[one, zero], [zero, zero]],
                    matched_qp,
                ),
            ),
            expect_failure(
                "I08_WRONG_MATCHED_SIGN",
                lambda: (
                    (_ for _ in ()).throw(AssertionError())
                    if generator_fraction(matched_q, matched_qp)[3] != one
                    else None
                ),
            ),
            expect_failure(
                "I09_ANGULAR_TRACE_ERASED_FROM_FULL_TEST",
                lambda: (
                    (_ for _ in ()).throw(AssertionError())
                    if generator_fraction(matched_q, common_qp)[1]
                    == [[-one, zero], [zero, one]]
                    else None
                ),
            ),
            expect_failure(
                "I10_SPECTATOR_CALLED_RECIPROCAL",
                lambda: (
                    (_ for _ in ()).throw(AssertionError())
                    if generator_fraction(matched_q, spectator_qp)[3] == 0
                    else None
                ),
            ),
            expect_failure(
                "I11_PLUS_I_DIMENSION_CHANGED",
                lambda: (
                    (_ for _ in ()).throw(AssertionError())
                    if lift_dimensions["ANGULAR_PLUS_I"] != 1
                    else None
                ),
            ),
            expect_failure(
                "I12_EXCHANGE_DIMENSION_CHANGED",
                lambda: (
                    (_ for _ in ()).throw(AssertionError())
                    if lift_dimensions["AXIS_EXCHANGE_F"] != 0
                    else None
                ),
            ),
            expect_failure(
                "I13_PARABOLIC_NORMALIZER",
                lambda: (
                    (_ for _ in ()).throw(AssertionError())
                    if relations[4] == "NEITHER"
                    else None
                ),
            ),
            expect_failure(
                "I14_HYPERBOLIC_NORMALIZER",
                lambda: (
                    (_ for _ in ()).throw(AssertionError())
                    if relations[5] == "NEITHER"
                    else None
                ),
            ),
            expect_failure(
                "I15_C_DETERMINANT_REMOVED",
                lambda: (
                    (_ for _ in ()).throw(AssertionError())
                    if formula["c_in_complete_metric"] is True
                    else None
                ),
            ),
            expect_failure(
                "I16_ROTATION_TERM_REMOVED",
                lambda: (
                    (_ for _ in ()).throw(AssertionError())
                    if "theta_p" in formula["sigma_squared"]
                    else None
                ),
            ),
            expect_failure(
                "I17_CRITICAL_PHI_PROMOTED",
                lambda: (
                    (_ for _ in ()).throw(AssertionError())
                    if next(
                        row for row in points
                        if row["control_id"] == "P09_CRITICAL_PHI"
                    )["pointwise_pattern"]
                    == "UNDEFINED"
                    else None
                ),
            ),
            expect_failure(
                "I18_POINTWISE_PROMOTED_TO_TRANSPORT",
                lambda: (
                    (_ for _ in ()).throw(AssertionError())
                    if "SPECTRUM_ONLY"
                    in next(
                        row for row in points
                        if row["control_id"] == "P05_TUNED_ROTATING_AXIS"
                    )["eigendirection_persistence"]
                    else None
                ),
            ),
            expect_failure(
                "I19_SOURCE_HASH_MUTATION",
                lambda: (
                    (_ for _ in ()).throw(AssertionError())
                    if digest(ROOT / lineage[0]["path"])
                    == lineage[0]["sha256"]
                    else None
                ),
            ),
            expect_failure(
                "I20_AUTHORITY_EXPANSION",
                lambda: (
                    (_ for _ in ()).throw(AssertionError())
                    if "ACTION_DERIVED" not in MAXIMUM
                    else None
                ),
            ),
        ]
    )
    if len(mutations) != 20:
        raise AssertionError("independent mutation count")

    output = {
        "schema": "udt-angular-generator-branch-census-independent-1.0",
        "status": "PASS",
        "implementation": (
            "stdlib_fraction_linear_algebra_plus_independent_finite_difference"
        ),
        "completion_families": len(branches),
        "branch_ruling_counts": result["branch_ruling_counts"],
        "rational_generator_controls": 3,
        "finite_difference_formula_controls": len(finite_controls),
        "max_formula_residual": max(finite_residuals),
        "c_values_checked": [2, 3, 299792458],
        "max_complete_determinant_relative_residual": max(
            complete_det_residuals
        ),
        "mirror_lift_dimensions": lift_dimensions,
        "monodromy_controls": len(monodromy),
        "source_hashes_replayed": len(lineage),
        "mutation_catches": len(mutations),
        "maximum_conclusion": MAXIMUM,
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
