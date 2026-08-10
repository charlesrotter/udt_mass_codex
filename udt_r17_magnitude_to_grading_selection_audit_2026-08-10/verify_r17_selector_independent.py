#!/usr/bin/env python3
"""Git-free independent Fraction/rank reconstruction of the R17 result."""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ZERO = Fraction(0)
ONE = Fraction(1)


def diag(*entries: Fraction) -> list[list[Fraction]]:
    return [[entries[i] if i == j else ZERO for j in range(len(entries))] for i in range(len(entries))]


def mm(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), ZERO) for j in range(len(b[0]))] for i in range(len(a))]


def sub(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def transpose(a: list[list[Fraction]]) -> list[list[Fraction]]:
    return [list(row) for row in zip(*a)]


def rank(matrix: list[list[Fraction]]) -> int:
    work = [row[:] for row in matrix if any(row)]
    if not work:
        return 0
    rows, cols, pivot_row = len(work), len(work[0]), 0
    for col in range(cols):
        pivot = next((row for row in range(pivot_row, rows) if work[row][col]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][col]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for row in range(rows):
            if row != pivot_row and work[row][col]:
                factor = work[row][col]
                work[row] = [work[row][j] - factor * work[pivot_row][j] for j in range(cols)]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def lorentz_basis() -> list[list[list[Fraction]]]:
    basis = []
    slots = [(0, 1, 1), (0, 2, 1), (0, 3, 1), (2, 3, -1), (1, 3, -1), (1, 2, -1)]
    for i, j, reverse_sign in slots:
        matrix = diag(ZERO, ZERO, ZERO, ZERO)
        matrix[i][j] = ONE
        matrix[j][i] = Fraction(reverse_sign)
        basis.append(matrix)
    return basis


def commutator_constraint_rank(matrices: list[list[list[Fraction]]]) -> int:
    columns = []
    for generator in lorentz_basis():
        column = []
        for matrix in matrices:
            commutator = sub(mm(generator, matrix), mm(matrix, generator))
            column.extend(value for row in commutator for value in row)
        columns.append(column)
    return rank([list(row) for row in zip(*columns)])


def main() -> None:
    eta = diag(Fraction(-1), ONE, ONE, ONE)
    identity = diag(ONE, ONE, ONE, ONE)

    def lift(z: Fraction, screen_power: int) -> list[list[Fraction]]:
        return diag(ONE / z, z, z**screen_power, z**screen_power)

    checks: dict[str, bool] = {}
    checks["composition"] = mm(lift(Fraction(3), 1), lift(Fraction(2), 1)) == lift(Fraction(6), 1)
    checks["reversal"] = mm(lift(Fraction(2), 1), lift(Fraction(1, 2), 1)) == identity
    checks["identity_fails_nonzero_depth"] = lift(Fraction(2), 1) != identity
    checks["pair_screen_weight_free"] = all(
        lift(Fraction(2), 0)[i][j] == lift(Fraction(2), 1)[i][j] for i in range(2) for j in range(2)
    )
    metric_a0 = mm(mm(transpose(lift(Fraction(2), 0)), eta), lift(Fraction(2), 0))
    metric_a1 = mm(mm(transpose(lift(Fraction(2), 1)), eta), lift(Fraction(2), 1))
    checks["wrong_screen_weight_changes_metric"] = metric_a0 != metric_a1

    rotation = [[ONE, ZERO, ZERO, ZERO], [ZERO, ONE, ZERO, ZERO], [ZERO, ZERO, ZERO, -ONE], [ZERO, ZERO, ONE, ZERO]]
    rotated = mm(rotation, lift(Fraction(2), 1))
    checks["screen_rotation_isometric"] = mm(mm(transpose(rotation), eta), rotation) == eta
    checks["screen_rotation_distinct_raw_lift"] = rotated != lift(Fraction(2), 1)
    checks["screen_rotation_same_metric"] = mm(mm(transpose(rotated), eta), rotated) == metric_a1
    checks["endpoint_quotient"] = mm(lift(Fraction(7), 1), lift(Fraction(1, 5), 1)) == lift(Fraction(7, 5), 1)

    p_u, p_n, h = diag(ONE, ZERO, ZERO, ZERO), diag(ZERO, ONE, ZERO, ZERO), diag(ZERO, ZERO, ONE, ONE)
    projector_nullity = 6 - commutator_constraint_rank([p_u, p_n, h])
    checks["projector_stabilizer_dimension_one"] = projector_nullity == 1
    grading_dimensions = {}
    for value in [Fraction(-2), Fraction(-1), Fraction(0), Fraction(1, 2), Fraction(1), Fraction(2)]:
        grading = diag(Fraction(-1), ONE, value, value)
        grading_dimensions[str(value)] = 6 - commutator_constraint_rank([grading])
    checks["grading_degeneracies"] = grading_dimensions == {
        "-2": 1, "-1": 3, "0": 1, "1/2": 1, "1": 3, "2": 1
    }

    manifest_lines = (HERE / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()
    source_rows = [row.split("\t") for row in manifest_lines[1:] if row.strip()]
    source_checks = []
    for fields in source_rows:
        if len(fields) != 7:
            raise AssertionError(f"malformed manifest row: {fields!r}")
        path, expected_blob, expected_sha, expected_size = ROOT / fields[1], fields[3], fields[4], int(fields[5])
        data = path.read_bytes()
        source_checks.append(
            path.is_file() and len(data) == expected_size and hashlib.sha256(data).hexdigest() == expected_sha and git_blob(data) == expected_blob
        )
    checks["all_17_sources_present_hash_blob_size_exact"] = len(source_rows) == 17 and all(source_checks)

    if not all(checks.values()):
        raise AssertionError([name for name, passed in checks.items() if not passed])

    result = {
        "verdict": "ACCEPT_ONLY_AS_COMPLETE_COFRAME_CONDITIONAL",
        "primary_landing": "COMPLETE_COFRAME_CONDITIONAL_VERTICAL_RECIPROCAL_METRIC_CLASS_MOD_SO2__FULL_PHYSICAL_ARROW_OPEN",
        "checks": checks,
        "check_count": len(checks),
        "grading_stabilizer_dimensions": grading_dimensions,
        "projector_triple_stabilizer_dimension": projector_nullity,
        "source_manifest_rows": len(source_rows),
        "implementation": "standard-library Fraction/rank/hash reconstruction; no production result import",
    }
    (HERE / "INDEPENDENT_VERIFICATION_RESULT.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"independent checks: {len(checks)}/{len(checks)}")


if __name__ == "__main__":
    main()
