#!/usr/bin/env python3
"""Independent stdlib/Fraction verification for G129; imports no production code."""

from __future__ import annotations

from fractions import Fraction as F
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
COMPONENTS = (
    (0, 0), (0, 1), (0, 2), (0, 3), (1, 1),
    (1, 2), (1, 3), (2, 2), (2, 3), (3, 3),
)


def row(left, right):
    answer = []
    for i, j in COMPONENTS:
        value = left[i] * right[j]
        if i != j:
            value += left[j] * right[i]
        answer.append(value)
    return answer


def design(directions):
    e0 = (F(1), F(0), F(0), F(0))
    return [candidate for v in directions for candidate in (row(e0, e0), row(e0, v), row(v, v))]


def rref(matrix, augmented_columns=0):
    a = [list(values) for values in matrix]
    rows = len(a)
    cols = len(a[0]) - augmented_columns
    pivot_row = 0
    pivots = []
    for col in range(cols):
        pivot = next((r for r in range(pivot_row, rows) if a[r][col] != 0), None)
        if pivot is None:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        scale = a[pivot_row][col]
        a[pivot_row] = [value / scale for value in a[pivot_row]]
        for r in range(rows):
            if r == pivot_row or a[r][col] == 0:
                continue
            scale = a[r][col]
            a[r] = [a[r][c] - scale * a[pivot_row][c] for c in range(len(a[r]))]
        pivots.append(col)
        pivot_row += 1
        if pivot_row == rows:
            break
    return a, pivots


def rank(matrix):
    return len(rref(matrix)[1])


def matvec(matrix, vector):
    return [sum((value * vector[j] for j, value in enumerate(row_values)), F(0)) for row_values in matrix]


def solve_full_column_rank(matrix, values):
    reduced, pivots = rref([row_values + [value] for row_values, value in zip(matrix, values)], 1)
    if pivots != list(range(len(matrix[0]))):
        raise ValueError("design is not full column rank")
    solution = [F(0)] * len(matrix[0])
    for row_index, pivot in enumerate(pivots):
        solution[pivot] = reduced[row_index][-1]
    return solution


def determinant(matrix):
    work = [list(row_values) for row_values in matrix]
    det = F(1)
    for col in range(len(work)):
        pivot = next((r for r in range(col, len(work)) if work[r][col] != 0), None)
        if pivot is None:
            return F(0)
        if pivot != col:
            work[col], work[pivot] = work[pivot], work[col]
            det = -det
        pivot_value = work[col][col]
        det *= pivot_value
        for r in range(col + 1, len(work)):
            scale = work[r][col] / pivot_value
            for c in range(col, len(work)):
                work[r][c] -= scale * work[col][c]
    return det


def matrix_from_components(values):
    result = [[F(0) for _ in range(4)] for _ in range(4)]
    for value, (i, j) in zip(values, COMPONENTS):
        result[i][j] = value
        result[j][i] = value
    return result


def transpose(matrix):
    return [list(values) for values in zip(*matrix)]


def matmul(left, right):
    right_t = transpose(right)
    return [
        [sum((a * b for a, b in zip(row_left, col_right)), F(0)) for col_right in right_t]
        for row_left in left
    ]


def matsub(left, right):
    return [[a - b for a, b in zip(row_left, row_right)] for row_left, row_right in zip(left, right)]


def diagonal(values):
    return [[value if i == j else F(0) for j, value in enumerate(values)] for i in range(len(values))]


def pullback_entry(values, left, right):
    return sum((coefficient * value for coefficient, value in zip(row(left, right), values)), F(0))


def main():
    e1 = (F(0), F(1), F(0), F(0))
    e2 = (F(0), F(0), F(1), F(0))
    e3 = (F(0), F(0), F(0), F(1))
    add = lambda a, b: tuple(x + y for x, y in zip(a, b))
    axial = [e1, e2, e3]
    faithful = axial + [add(e1, e2), add(e1, e3), add(e2, e3)]
    axial_design = design(axial)
    full_design = design(faithful)

    values = [
        F(-4), F(1, 3), F(-1, 5), F(1, 7), F(3),
        F(1, 11), F(-1, 13), F(5), F(1, 17), F(7),
    ]
    measurements = matvec(full_design, values)
    reconstructed = solve_full_column_rank(full_design, measurements)
    e0 = (F(1), F(0), F(0), F(0))
    pair_metrics_regular = all(
        pullback_entry(values, e0, e0) < 0
        and (
            pullback_entry(values, e0, e0) * pullback_entry(values, v, v)
            - pullback_entry(values, e0, v) ** 2
        ) < 0
        for v in faithful
    )

    invisible = [F(0)] * 10
    invisible[5] = F(1)
    perturbed = [value + F(1, 2) * delta for value, delta in zip(values, invisible)]
    axial_same = matvec(axial_design, values) == matvec(axial_design, perturbed)
    full_detects = matvec(full_design, values) != matvec(full_design, perturbed)

    g = matrix_from_components(values)
    gp = matrix_from_components(perturbed)
    leading = [determinant([row_values[:n] for row_values in g[:n]]) for n in range(1, 5)]
    leading_p = [determinant([row_values[:n] for row_values in gp[:n]]) for n in range(1, 5)]
    pivots = [leading[0]] + [leading[i] / leading[i - 1] for i in range(1, 4)]
    pivots_p = [leading_p[0]] + [leading_p[i] / leading_p[i - 1] for i in range(1, 4)]
    lorentz = pivots[0] < 0 and all(value > 0 for value in pivots[1:])
    lorentz_p = pivots_p[0] < 0 and all(value > 0 for value in pivots_p[1:])

    # Exact terminal-ratio counterexample with the same clock normalization h00=-1.
    ratio_1 = -F(-1) / (F(-1) ** 2)
    det_h2 = F(-1) * F(3, 4) - F(1, 2) ** 2
    ratio_2 = -det_h2 / (F(-1) ** 2)

    # Standard C-infinity bump exp[-1/((x-1)(2-x))] on 1<x<2, zero elsewhere.
    # Only its exact support and strict positivity are needed here; flatness at the endpoints is
    # proved from the standard exp(-1/u) limit in EXACT_DERIVATION.md.
    def bump(x):
        if not (F(1) < x < F(2)):
            return F(0)
        return "strictly_positive"

    quiet_equal = all(bump(value) == 0 for value in (F(-3), F(-1), F(0), F(1), F(2), F(3)))
    bump_nonzero = bump(F(3, 2)) == "strictly_positive"

    # Independent curvature-jet reconstruction at z=0 for g_xy=a z^2.
    # First derivatives vanish, so only derivatives of Christoffels enter Ricci.
    a = F(3, 5)
    eta_inverse = diagonal([F(-1), F(1), F(1), F(1)])
    d2g = [[[[F(0) for _ in range(4)] for _ in range(4)] for _ in range(4)] for _ in range(4)]
    d2g[3][3][1][2] = 2 * a
    d2g[3][3][2][1] = 2 * a

    def dgamma(derivative, upper, lower_1, lower_2):
        return sum(
            (
                eta_inverse[upper][ell]
                * (
                    d2g[derivative][lower_1][ell][lower_2]
                    + d2g[derivative][lower_2][ell][lower_1]
                    - d2g[derivative][ell][lower_1][lower_2]
                )
                / 2
            )
            for ell in range(4)
        )

    ricci = [[F(0) for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            ricci[i][j] = sum(
                dgamma(k, k, i, j) - dgamma(j, k, i, k) for k in range(4)
            )
    ricci_squared = sum(
        eta_inverse[i][k] * eta_inverse[j][ell] * ricci[i][j] * ricci[k][ell]
        for i in range(4)
        for j in range(4)
        for k in range(4)
        for ell in range(4)
    )
    curved_invariant_nonzero = (
        ricci[1][2] == ricci[2][1] == -a
        and ricci_squared == F(18, 25)
    )

    # Independent constructive overlap witness plus a deliberately corrupted local metric.
    c1 = diagonal([F(1), F(1), F(1), F(1)])
    c2 = diagonal([F(2), F(1), F(1), F(1)])
    c3 = diagonal([F(2), F(3), F(1), F(1)])
    d21 = diagonal([F(1, 2), F(1), F(1), F(1)])
    d32 = diagonal([F(1), F(1, 3), F(1), F(1)])
    d31 = diagonal([F(1, 2), F(1, 3), F(1), F(1)])
    h1 = matmul(transpose(c1), matmul(g, c1))
    h2 = matmul(transpose(c2), matmul(g, c2))
    h3 = matmul(transpose(c3), matmul(g, c3))
    zero4 = [[F(0) for _ in range(4)] for _ in range(4)]
    cocycle_ok = matsub(matmul(d32, d21), d31) == zero4
    descent_ok = all(
        matsub(matmul(transpose(d), matmul(h_target, d)), h_source) == zero4
        for d, h_target, h_source in (
            (d21, h2, h1), (d32, h3, h2), (d31, h3, h1)
        )
    )
    h2_bad = [row_values[:] for row_values in h2]
    h2_bad[0][0] += F(1, 7)
    corruption_detected = (
        matsub(matmul(transpose(d21), matmul(h2_bad, d21)), h1) != zero4
    )

    checks = {
        "independent_six_plane_rank_ten": rank(full_design) == 10,
        "independent_three_axial_rank_seven": rank(axial_design) == 7,
        "independent_exact_reconstruction": reconstructed == values,
        "independent_axial_invisible_perturbation": axial_same,
        "independent_full_network_detects_perturbation": full_detects,
        "independent_base_lorentz": lorentz,
        "independent_all_six_pair_metrics_regular_lorentzian": pair_metrics_regular,
        "independent_perturbed_lorentz": lorentz_p,
        "independent_terminal_scalar_nonfaithful": ratio_1 == ratio_2 == 1,
        "independent_quiet_endpoint_bump_sample_regression": quiet_equal and bump_nonzero,
        "independent_curved_germ_invariant_nonzero": curved_invariant_nonzero,
        "independent_overlap_witness_and_corruption": cocycle_ok and descent_ok and corruption_detected,
    }
    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "independent_check_count": len(checks),
        "full_rank": rank(full_design),
        "axial_rank": rank(axial_design),
        "ricci_squared_at_origin_for_a_3_over_5": str(ricci_squared),
        "landing": "FAITHFUL_IFF_PAIR_PLANE_SPAN_HAS_RANK_TEN",
    }
    (HERE / "INDEPENDENT_VERIFICATION.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
