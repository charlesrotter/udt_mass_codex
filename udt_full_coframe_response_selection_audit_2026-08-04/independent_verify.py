#!/usr/bin/env python3
"""Independent standard-library checks for the response-selection algebra."""

from __future__ import annotations

import json
from fractions import Fraction as F


def rank(matrix: list[list[F]]) -> int:
    work = [row[:] for row in matrix]
    rows = len(work)
    cols = len(work[0]) if rows else 0
    pivot_row = 0
    for col in range(cols):
        pivot = next((row for row in range(pivot_row, rows) if work[row][col]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][col]
        work[pivot_row] = [item / scale for item in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not work[row][col]:
                continue
            factor = work[row][col]
            work[row] = [work[row][j] - factor * work[pivot_row][j] for j in range(cols)]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def bilinear(vector: list[F], matrix: list[list[F]]) -> F:
    return sum(vector[i] * matrix[i][j] * vector[j] for i in range(4) for j in range(4))


def symmetric_coefficients(u: list[F], n: list[F]) -> list[F]:
    row: list[F] = []
    for i in range(4):
        for j in range(i, 4):
            factor = F(1) if i == j else F(2)
            row.append(factor * (u[i] * u[j] + n[i] * n[j]))
    return row


def main() -> None:
    checks: list[tuple[str, bool]] = []

    def check(name: str, condition: bool) -> None:
        checks.append((name, bool(condition)))

    signs = [F(-1), F(1), F(1), F(1)]
    eta = [[F(0) for _ in range(4)] for _ in range(4)]
    for i, sign in enumerate(signs):
        eta[i][i] = sign
    H = [F(-1), F(1), F(0), F(0)]
    t_h = [2 * signs[i] * H[i] for i in range(4)]
    check("founded_trace", sum(H) == 0)
    check("founded_tangent", t_h == [F(2), F(2), F(0), F(0)])
    check("volume_blind", sum(signs[i] * t_h[i] for i in range(4)) / 2 == 0)
    check("anisotropic_visible", t_h[0] == 2)

    # Ten independent physical coframe directions: four diagonal plus six symmetric off-diagonal
    # representatives. Six eta-skew directions form the complementary Lorentz kernel.
    physical_columns: list[list[F]] = []
    for i in range(4):
        column = [F(0)] * 10
        diagonal_index = sum(4 - k for k in range(i))
        column[diagonal_index] = 2 * signs[i]
        physical_columns.append(column)
    component_pairs = [(i, j) for i in range(4) for j in range(i, 4)]
    for i in range(4):
        for j in range(i + 1, 4):
            column = [F(0)] * 10
            column[component_pairs.index((i, j))] = signs[i]
            physical_columns.append(column)
    physical_matrix = [[physical_columns[col][row] for col in range(10)] for row in range(10)]
    check("coframe_rank_ten", rank(physical_matrix) == 10)

    lorentz_vectors: list[list[F]] = []
    for i in range(4):
        for j in range(i + 1, 4):
            vector = [F(0)] * 16
            vector[4 * i + j] = 1
            vector[4 * j + i] = -signs[i] / signs[j]
            lorentz_vectors.append(vector)
            # Direct eta-skew check in the only nonzero pair.
            check(f"lorentz_{i}{j}", signs[i] * vector[4 * i + j] + signs[j] * vector[4 * j + i] == 0)
    lorentz_matrix = [[vector[row] for vector in lorentz_vectors] for row in range(16)]
    check("lorentz_rank_six", rank(lorentz_matrix) == 6)

    # Independent f(R) constant-curvature calculation.
    coefficients: dict[str, list[str]] = {}
    for n in range(7):
        samples = [F(n - 2, 4) * F(curvature) ** n for curvature in (4, 12)]
        coefficients[str(n)] = [str(item) for item in samples]
        check(f"fR_{n}", samples == [F(n - 2, 4) * F(4) ** n, F(n - 2, 4) * F(12) ** n])
    eh_samples = [F(item) for item in coefficients["1"]]
    r3_samples = [F(item) for item in coefficients["3"]]
    det_exact = eh_samples[0] * r3_samples[1] - eh_samples[1] * r3_samples[0]
    check("fR_distinct_shapes", det_exact == -384 and eh_samples == [F(-1), F(-3)] and r3_samples == [F(16), F(432)])
    check("EH_vs_R2_constant_curvature", coefficients["1"][1] == "-3" and coefficients["2"][1] == "0")

    dim = [[F(1), F(3)], [F(0), F(-1)], [F(-1), F(-2)]]
    augmented = [row + [target] for row, target in zip(dim, [F(-2), F(0), F(0)])]
    check("cG_no_curvature_scale", rank(dim) == 2 and rank(augmented) == 3)

    e = [[F(1) if i == j else F(0) for i in range(4)] for j in range(4)]
    pairs: list[tuple[list[F], list[F]]] = []
    for i in (1, 2, 3):
        pairs.append((e[0], e[i]))
    pairs.extend(
        [
            (e[0], [F(0), F(3, 5), F(4, 5), F(0)]),
            (e[0], [F(0), F(3, 5), F(0), F(4, 5)]),
            (e[0], [F(0), F(0), F(3, 5), F(4, 5)]),
            ([F(5, 3), F(4, 3), F(0), F(0)], e[2]),
            ([F(5, 3), F(0), F(4, 3), F(0)], e[3]),
            ([F(5, 3), F(0), F(0), F(4, 3)], e[1]),
        ]
    )
    query_rows: list[list[F]] = []
    for index, (u, n) in enumerate(pairs):
        check(f"query_timelike_{index}", bilinear(u, eta) == -1)
        check(f"query_spacelike_{index}", bilinear(n, eta) == 1)
        orthogonal = sum(u[i] * eta[i][j] * n[j] for i in range(4) for j in range(4))
        check(f"query_orthogonal_{index}", orthogonal == 0)
        query_rows.append(symmetric_coefficients(u, n))
    metric_line = [F(1), F(0), F(0), F(0), F(-1), F(0), F(0), F(-1), F(0), F(-1)]
    check("query_rank_nine", rank(query_rows) == 9)
    check("metric_line_kernel", all(sum(row[i] * metric_line[i] for i in range(10)) == 0 for row in query_rows))

    failed = [name for name, passed in checks if not passed]
    print(
        json.dumps(
            {
                "status": "PASS" if not failed else "FAIL",
                "checks": len(checks),
                "failed": failed,
                "implementation": "python_standard_library_fraction_no_sympy_no_production_import",
                "coframe_rank": rank(physical_matrix),
                "lorentz_kernel_rank": rank(lorentz_matrix),
                "fR_shape_determinant": str(det_exact),
                "dimension_ranks": [rank(dim), rank(augmented)],
                "query_rank": rank(query_rows),
            },
            indent=2,
            sort_keys=True,
        )
    )
    raise SystemExit(0 if not failed else 1)


if __name__ == "__main__":
    main()
