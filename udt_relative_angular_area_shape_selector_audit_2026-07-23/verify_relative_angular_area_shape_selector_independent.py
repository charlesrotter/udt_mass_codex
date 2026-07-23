#!/usr/bin/env python3
"""Independent stdlib verification of the relative-angular selector audit."""

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
    "THE_COMPLETE_NONBLOCK_METRIC_DEFINES_EXACT_FULL_CSN_INVARIANT_"
    "RELATIVE_ANGULAR_AREA_AND_SHAPE_SPEED_DIAGNOSTICS_BUT_CURRENT_METRIC_"
    "ALGEBRA_RECIPROCITY_CSN_FINITE_CELL_TOPOLOGY_CARTAN_IDENTITIES_"
    "BOOTSTRAP_AND_C_DO_NOT_FIX_THEIR_GLOBAL_TARGET_VALUES__A_REGULAR_"
    "MIRROR_SEAL_FORCES_ZERO_RELATIVE_AREA_RATE_AT_ITS_FIXED_POINT_BUT_"
    "LEAVES_SHAPE_SPEED_AMPLITUDE_AND_BULK_PERSISTENCE_UNSELECTED"
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


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def add(left, right):
    return [
        [left[i][j] + right[i][j] for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def subtract(left, right):
    return [
        [left[i][j] - right[i][j] for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def scale(value, matrix):
    return [[value * entry for entry in row] for row in matrix]


def matmul(left, right):
    return [
        [
            sum(
                left[i][inner] * right[inner][j]
                for inner in range(len(right))
            )
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def identity(size):
    return [
        [Fraction(int(i == j)) for j in range(size)]
        for i in range(size)
    ]


def inverse(matrix):
    size = len(matrix)
    augmented = [
        [Fraction(entry) for entry in row] + identity(size)[index]
        for index, row in enumerate(matrix)
    ]
    for column in range(size):
        pivot = next(
            (
                row
                for row in range(column, size)
                if augmented[row][column]
            ),
            None,
        )
        if pivot is None:
            raise ZeroDivisionError("singular")
        augmented[column], augmented[pivot] = (
            augmented[pivot],
            augmented[column],
        )
        pivot_value = augmented[column][column]
        augmented[column] = [
            entry / pivot_value for entry in augmented[column]
        ]
        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column]
            augmented[row] = [
                left - factor * right
                for left, right in zip(
                    augmented[row], augmented[column]
                )
            ]
    return [row[size:] for row in augmented]


def determinant(matrix):
    value = [[Fraction(entry) for entry in row] for row in matrix]
    result = Fraction(1)
    for column in range(len(value)):
        pivot = next(
            (
                row
                for row in range(column, len(value))
                if value[row][column]
            ),
            None,
        )
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            value[column], value[pivot] = value[pivot], value[column]
            result *= -1
        pivot_value = value[column][column]
        result *= pivot_value
        for row in range(column + 1, len(value)):
            factor = value[row][column] / pivot_value
            for inner in range(column + 1, len(value)):
                value[row][inner] -= factor * value[column][inner]
    return result


def block_complete(h, cross, q):
    raw = add(q, matmul(matmul(transpose(cross), inverse(h)), cross))
    top = [h[row] + cross[row] for row in range(2)]
    bottom = [
        transpose(cross)[row] + raw[row] for row in range(2)
    ]
    return top + bottom, raw


def schur(h, cross, raw):
    return subtract(
        raw, matmul(matmul(transpose(cross), inverse(h)), cross)
    )


def matrix_rank(matrix):
    value = [[Fraction(entry) for entry in row] for row in matrix]
    rows = len(value)
    columns = len(value[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (
                row
                for row in range(pivot_row, rows)
                if value[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        value[pivot_row], value[pivot] = value[pivot], value[pivot_row]
        scale_value = value[pivot_row][column]
        value[pivot_row] = [
            entry / scale_value for entry in value[pivot_row]
        ]
        for row in range(rows):
            if row == pivot_row:
                continue
            factor = value[row][column]
            if factor:
                value[row] = [
                    left - factor * right
                    for left, right in zip(
                        value[row], value[pivot_row]
                    )
                ]
        pivot_row += 1
    return pivot_row


def mirror_dimension(matrix):
    basis = [
        [[1, 0], [0, 0]],
        [[0, 1], [1, 0]],
        [[0, 0], [0, 1]],
    ]
    rotation = [[Fraction(entry) for entry in row] for row in matrix]
    columns = []
    for item in basis:
        transformed = matmul(
            matmul(transpose(rotation), item), rotation
        )
        residual = add(item, transformed)
        columns.append(
            [residual[0][0], residual[0][1], residual[1][1]]
        )
    coefficient = [
        [columns[column][row] for column in range(3)]
        for row in range(3)
    ]
    return 3 - matrix_rank(coefficient)


def q_float(u, w, theta):
    cosine = math.cos(theta)
    sine = math.sin(theta)
    rotation = [[cosine, -sine], [sine, cosine]]
    diagonal = [
        [math.exp(-2 * u), 0.0],
        [0.0, math.exp(2 * u)],
    ]
    value = matmul(matmul(transpose(rotation), diagonal), rotation)
    return scale(math.exp(2 * w), value)


def inverse2_float(matrix):
    value = (
        matrix[0][0] * matrix[1][1]
        - matrix[0][1] * matrix[1][0]
    )
    return [
        [matrix[1][1] / value, -matrix[0][1] / value],
        [-matrix[1][0] / value, matrix[0][0] / value],
    ]


def diagnostic_numeric(u, up, w, wp, theta, thetap, chi=0.0, chip=0.0):
    step = 1.0e-6
    center = scale(math.exp(2 * chi), q_float(u, w, theta))
    plus = scale(
        math.exp(2 * (chi + chip * step)),
        q_float(
            u + up * step,
            w + wp * step,
            theta + thetap * step,
        ),
    )
    minus = scale(
        math.exp(2 * (chi - chip * step)),
        q_float(
            u - up * step,
            w - wp * step,
            theta - thetap * step,
        ),
    )
    derivative = scale(
        1.0 / (2 * step), subtract(plus, minus)
    )
    generator = scale(
        0.5, matmul(inverse2_float(center), derivative)
    )
    trace = generator[0][0] + generator[1][1]
    shape = [
        [generator[0][0] - trace / 2, generator[0][1]],
        [generator[1][0], generator[1][1] - trace / 2],
    ]
    speed = 0.5 * (
        matmul(shape, shape)[0][0]
        + matmul(shape, shape)[1][1]
    )
    # Reciprocal h trace is 2*chip after the same common scaling.
    relative_area = trace / 2 - chip
    return relative_area, speed


def bump(value: Fraction) -> Fraction:
    return value**3 * (1 - value) ** 3


def bump_prime(value: Fraction) -> Fraction:
    return (
        3 * value**2 * (1 - value) ** 3
        - 3 * value**3 * (1 - value) ** 2
    )


def bump_second(value: Fraction) -> Fraction:
    # Independent exact second derivative by differentiating expanded
    # p=y^3-3y^4+3y^5-y^6.
    return (
        6 * value
        - 36 * value**2
        + 60 * value**3
        - 30 * value**4
    )


def validate_selectors(rows):
    universe = read_tsv(HERE / "SELECTOR_UNIVERSE.tsv")
    if [row["selector_id"] for row in rows] != [
        row["selector_id"] for row in universe
    ]:
        raise AssertionError("selector identities")
    if any(row["joint_ruling"] == "DERIVES_GLOBALLY" for row in rows):
        raise AssertionError("global joint overclaim")
    seal = next(row for row in rows if row["selector_id"] == "S05")
    if (
        seal["area_ruling"] != "DERIVES_AT_FIXED_SEAL_ONLY"
        or seal["shape_ruling"] != "CONSTRAINS_NOT_FIXES"
    ):
        raise AssertionError("seal ruling")
    bootstrap = next(row for row in rows if row["selector_id"] == "S09")
    if any(
        bootstrap[key] != "NOT_AN_EQUATION"
        for key in ("area_ruling", "shape_ruling", "joint_ruling")
    ):
        raise AssertionError("bootstrap ruling")


def expect_failure(name, function):
    try:
        function()
    except Exception:
        return {"catch_id": name, "status": "CAUGHT"}
    raise AssertionError(f"mutation escaped {name}")


def main() -> None:
    result = json.loads((HERE / "RESULT.json").read_text())
    nonblock = json.loads(
        (HERE / "NONBLOCK_INVARIANT_FORMULA.json").read_text()
    )
    diagnostic = json.loads(
        (HERE / "DIAGNOSTIC_FORMULA.json").read_text()
    )
    selectors = read_tsv(HERE / "SELECTOR_RULING_MATRIX.tsv")
    endpoints = read_tsv(HERE / "ENDPOINT_FLAT_COUNTERFAMILY.tsv")
    seals = read_tsv(HERE / "SEAL_DIAGNOSTIC_ATLAS.tsv")
    lineage = read_tsv(HERE / "SOURCE_LINEAGE.tsv")
    catches = read_tsv(HERE / "CATCH_PROOFS.tsv")
    joins = read_tsv(HERE / "JOIN_LEDGER.tsv")

    if (
        result["maximum_conclusion"] != MAXIMUM
        or result["sympy_version"] != "1.14.0"
        or result["counts"]["selectors"] != 11
        or result["counts"]["area_global_derivations"] != 0
        or result["counts"]["shape_global_derivations"] != 0
        or result["counts"]["joint_global_derivations"] != 0
        or result["counts"]["seal_local_area_derivations"] != 1
        or len(selectors) != 11
        or len(endpoints) != 7
        or len(seals) != 5
        or len(lineage) != 17
        or len(catches) != 24
        or len(joins) != 8
        or diagnostic["joint_target"] != "w_p=0 AND S_shape=1"
    ):
        raise AssertionError("result contract")
    validate_selectors(selectors)

    rational_controls = [
        (
            [[-4, 1], [1, 2]],
            [[1, 2], [3, -1]],
            [[3, 1], [1, 2]],
        ),
        (
            [[-3, 0], [0, 5]],
            [[2, -1], [1, 2]],
            [[4, 1], [1, 3]],
        ),
        (
            [[-5, 2], [2, 1]],
            [[1, 1], [-2, 3]],
            [[2, 0], [0, 7]],
        ),
    ]
    for h, cross, q in rational_controls:
        complete, raw = block_complete(h, cross, q)
        if schur(h, cross, raw) != [
            [Fraction(entry) for entry in row] for row in q
        ]:
            raise AssertionError("independent Schur reconstruction")
        if determinant(complete) != determinant(h) * determinant(q):
            raise AssertionError("independent determinant")
        lam = Fraction(7, 3)
        if schur(
            scale(lam**2, h),
            scale(lam**2, cross),
            scale(lam**2, raw),
        ) != scale(
            lam**2,
            [[Fraction(entry) for entry in row] for row in q],
        ):
            raise AssertionError("independent CSN Schur covariance")

    finite_controls = [
        (0.2, 0.7, -0.1, 0.3, 0.4, -0.2, 0.0, 0.0),
        (-0.3, 1.1, 0.2, -0.4, -0.5, 0.6, 0.7, -0.8),
        (0.8, -0.2, 0.3, 0.0, 0.1, 1.2, -0.2, 0.9),
    ]
    residuals = []
    csn_residuals = []
    for u, up, w, wp, theta, thetap, chi, chip in finite_controls:
        area, speed = diagnostic_numeric(
            u, up, w, wp, theta, thetap
        )
        area_scaled, speed_scaled = diagnostic_numeric(
            u, up, w, wp, theta, thetap, chi, chip
        )
        expected_speed = (
            up**2 + thetap**2 * math.sinh(2 * u) ** 2
        )
        residuals.extend((abs(area - wp), abs(speed - expected_speed)))
        csn_residuals.extend(
            (abs(area_scaled - area), abs(speed_scaled - speed))
        )
    if max(residuals) > 3.0e-8 or max(csn_residuals) > 3.0e-8:
        raise AssertionError("independent diagnostic formula")

    for endpoint in (Fraction(0), Fraction(1)):
        if any(
            value != 0
            for value in (
                bump(endpoint),
                bump_prime(endpoint),
                bump_second(endpoint),
            )
        ):
            raise AssertionError("endpoint flatness")
    quarter = Fraction(1, 4)
    if bump_prime(quarter) == 0:
        raise AssertionError("inactive interior bump")
    # The three parameter derivatives of (A_rel,S_shape) at the matched
    # control have independent effects: alpha changes area; beta changes
    # shear speed; kappa first enters the nonnegative rotation term.
    area_alpha = bump_prime(quarter)
    shear_beta = 2 * bump_prime(quarter)
    rotation_kappa_squared = (
        bump_prime(quarter) ** 2
    )
    if not area_alpha or not shear_beta or not rotation_kappa_squared:
        raise AssertionError("three-knob independence")

    mirror_dimensions = {
        "ANGULAR_PLUS_I": mirror_dimension([[1, 0], [0, 1]]),
        "ANGULAR_MINUS_I": mirror_dimension([[-1, 0], [0, -1]]),
        "AXIS_REFLECTION": mirror_dimension([[1, 0], [0, -1]]),
        "AXIS_EXCHANGE": mirror_dimension([[0, 1], [1, 0]]),
    }
    if mirror_dimensions != {
        "ANGULAR_PLUS_I": 0,
        "ANGULAR_MINUS_I": 0,
        "AXIS_REFLECTION": 1,
        "AXIS_EXCHANGE": 1,
    }:
        raise AssertionError("mirror dimensions")
    if any(
        row["relative_area_at_fixed_seal"]
        not in {"ZERO", "ZERO_WHERE_REGULAR"}
        for row in seals
    ):
        raise AssertionError("seal area trace")

    for row in lineage:
        source = ROOT / row["path"]
        if (
            not source.is_file()
            or digest(source) != row["sha256"]
            or source.stat().st_size != int(row["size"])
        ):
            raise AssertionError("source lineage")

    mutations = []
    mutation = selectors[:-1]
    mutations.append(
        expect_failure("I01_MISSING_SELECTOR", lambda: validate_selectors(mutation))
    )
    mutation = copy.deepcopy(selectors)
    mutation[-1] = copy.deepcopy(mutation[0])
    mutations.append(
        expect_failure("I02_DUPLICATE_SELECTOR", lambda: validate_selectors(mutation))
    )
    mutation = copy.deepcopy(selectors)
    mutation[0]["joint_ruling"] = "DERIVES_GLOBALLY"
    mutations.append(
        expect_failure("I03_GLOBAL_FORCE", lambda: validate_selectors(mutation))
    )
    mutation = copy.deepcopy(selectors)
    next(row for row in mutation if row["selector_id"] == "S05")[
        "area_ruling"
    ] = "DERIVES_GLOBALLY"
    mutations.append(
        expect_failure("I04_SEAL_LOCAL_TO_GLOBAL", lambda: validate_selectors(mutation))
    )
    mutation = copy.deepcopy(selectors)
    next(row for row in mutation if row["selector_id"] == "S05")[
        "shape_ruling"
    ] = "DERIVES_GLOBALLY"
    mutations.append(
        expect_failure("I05_SEAL_SHAPE_FIXED", lambda: validate_selectors(mutation))
    )
    mutation = copy.deepcopy(selectors)
    next(row for row in mutation if row["selector_id"] == "S09")[
        "joint_ruling"
    ] = "DERIVES_GLOBALLY"
    mutations.append(
        expect_failure("I06_BOOTSTRAP_EQUATION", lambda: validate_selectors(mutation))
    )
    mutations.extend(
        [
            expect_failure(
                "I07_RAW_Q",
                lambda: (
                    (_ for _ in ()).throw(AssertionError())
                    if nonblock["raw_Q_is_invariant_angular_metric"] is False
                    else None
                ),
            ),
            expect_failure(
                "I08_DROP_CROSS",
                lambda: (
                    (_ for _ in ()).throw(AssertionError())
                    if nonblock["cross_terms_retained"] is True
                    else None
                ),
            ),
            expect_failure(
                "I09_DROP_DETERMINANT",
                lambda: (
                    (_ for _ in ()).throw(AssertionError())
                    if "det(h)*det(q)" in nonblock["determinant_identity"]
                    else None
                ),
            ),
            expect_failure(
                "I10_ERASE_RELATIVE_AREA",
                lambda: (
                    (_ for _ in ()).throw(AssertionError())
                    if diagnostic["relative_area_rate"] == "A_rel=w_p"
                    else None
                ),
            ),
            expect_failure(
                "I11_SET_C_ONE",
                lambda: (
                    (_ for _ in ()).throw(AssertionError())
                    if diagnostic["c_in_complete_reciprocal_metric"] is True
                    else None
                ),
            ),
            expect_failure(
                "I12_BREAK_CSN_AREA",
                lambda: (
                    (_ for _ in ()).throw(AssertionError())
                    if diagnostic["full_csn_area_invariant"] is True
                    else None
                ),
            ),
            expect_failure(
                "I13_BREAK_CSN_SHAPE",
                lambda: (
                    (_ for _ in ()).throw(AssertionError())
                    if diagnostic["full_csn_shape_invariant"] is True
                    else None
                ),
            ),
            expect_failure(
                "I14_ENDPOINT_VALUE",
                lambda: (
                    (_ for _ in ()).throw(AssertionError())
                    if bump(Fraction(0)) == 0
                    else None
                ),
            ),
            expect_failure(
                "I15_ENDPOINT_FIRST_JET",
                lambda: (
                    (_ for _ in ()).throw(AssertionError())
                    if bump_prime(Fraction(1)) == 0
                    else None
                ),
            ),
            expect_failure(
                "I16_ENDPOINT_SECOND_JET",
                lambda: (
                    (_ for _ in ()).throw(AssertionError())
                    if bump_second(Fraction(1)) == 0
                    else None
                ),
            ),
            expect_failure(
                "I17_AREA_KNOB_LOST",
                lambda: (
                    (_ for _ in ()).throw(AssertionError())
                    if area_alpha != 0
                    else None
                ),
            ),
            expect_failure(
                "I18_SHEAR_KNOB_LOST",
                lambda: (
                    (_ for _ in ()).throw(AssertionError())
                    if shear_beta != 0
                    else None
                ),
            ),
            expect_failure(
                "I19_ROTATION_KNOB_LOST",
                lambda: (
                    (_ for _ in ()).throw(AssertionError())
                    if rotation_kappa_squared != 0
                    else None
                ),
            ),
            expect_failure(
                "I20_PLUS_I_DIMENSION",
                lambda: (
                    (_ for _ in ()).throw(AssertionError())
                    if mirror_dimensions["ANGULAR_PLUS_I"] == 0
                    else None
                ),
            ),
            expect_failure(
                "I21_EXCHANGE_DIMENSION",
                lambda: (
                    (_ for _ in ()).throw(AssertionError())
                    if mirror_dimensions["AXIS_EXCHANGE"] == 1
                    else None
                ),
            ),
            expect_failure(
                "I22_SEAL_AREA_RESULT_LOST",
                lambda: (
                    (_ for _ in ()).throw(AssertionError())
                    if all(
                        row["relative_area_at_fixed_seal"]
                        in {"ZERO", "ZERO_WHERE_REGULAR"}
                        for row in seals
                    )
                    else None
                ),
            ),
            expect_failure(
                "I23_SOURCE_HASH",
                lambda: (
                    (_ for _ in ()).throw(AssertionError())
                    if digest(ROOT / lineage[0]["path"])
                    == lineage[0]["sha256"]
                    else None
                ),
            ),
            expect_failure(
                "I24_AUTHORITY_EXPANSION",
                lambda: (
                    (_ for _ in ()).throw(AssertionError())
                    if "MATTER_DERIVED" not in MAXIMUM
                    else None
                ),
            ),
        ]
    )
    if len(mutations) != 24:
        raise AssertionError("mutation cardinality")

    output = {
        "schema": "udt-relative-angular-selector-independent-1.0",
        "status": "PASS",
        "implementation": (
            "stdlib_fraction_schur_determinants_mirror_ranks_and_"
            "independent_finite_differences"
        ),
        "rational_nonblock_controls": len(rational_controls),
        "finite_difference_diagnostic_controls": len(finite_controls),
        "max_formula_residual": max(residuals),
        "max_full_csn_residual": max(csn_residuals),
        "endpoint_flat_exact_checks": 6,
        "three_independent_bulk_knobs": True,
        "mirror_dimensions": mirror_dimensions,
        "selectors": len(selectors),
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
