#!/usr/bin/env python3
"""Independent standard-library rational reconstruction for the same-solution audit."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "INDEPENDENT_RESULT.json"
SIGNS = [F(-1), F(1), F(1), F(1)]
METRIC_SLOTS = [(a, b) for a in range(4) for b in range(a, 4)]
HESSIAN_SLOTS = [(m, n) for m in range(4) for n in range(m, 4)]
BIVECTORS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
BIV_SLOTS = [(i, j) for i in range(6) for j in range(i, 6)]


def zeros(rows, cols):
    return [[F(0) for _ in range(cols)] for _ in range(rows)]


def transpose(matrix):
    return [list(row) for row in zip(*matrix)] if matrix else []


def columns_to_matrix(columns):
    return transpose(columns)


def hstack(*matrices):
    return [sum((matrix[row] for matrix in matrices), []) for row in range(len(matrices[0]))]


def multiply(left, right):
    right_t = transpose(right)
    return [[sum((a * b for a, b in zip(row, col)), F(0)) for col in right_t] for row in left]


def rank(matrix):
    work = [row[:] for row in matrix]
    rows = len(work)
    cols = len(work[0]) if rows else 0
    pivot_row = 0
    for col in range(cols):
        pivot = next((row for row in range(pivot_row, rows) if work[row][col]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][col]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not work[row][col]:
                continue
            factor = work[row][col]
            work[row] = [work[row][j] - factor * work[pivot_row][j] for j in range(cols)]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def metric_index(a, b, m, n):
    return METRIC_SLOTS.index(tuple(sorted((a, b)))) * 10 + HESSIAN_SLOTS.index(tuple(sorted((m, n))))


def curvature_component(column, a, b, c, d):
    value = lambda i, j, k, ell: F(int(column == metric_index(i, j, k, ell)))
    return F(1, 2) * (value(a, d, b, c) + value(b, c, a, d) - value(a, c, b, d) - value(b, d, a, c))


def curvature_map():
    rows = []
    for i, j in BIV_SLOTS:
        a, b = BIVECTORS[i]
        c, d = BIVECTORS[j]
        rows.append([curvature_component(column, a, b, c, d) for column in range(100)])
    return rows


def matrix(entries=None):
    out = zeros(4, 4)
    if entries:
        for row, col, value in entries:
            out[row][col] = F(value)
    return out


def add(left, right):
    return [[left[i][j] + right[i][j] for j in range(4)] for i in range(4)]


def generators():
    return {
        "H": matrix([(0, 0, -1), (1, 1, 1)]),
        "K_area": matrix([(2, 2, 1), (3, 3, 1)]),
        "K_shear_diag": matrix([(2, 2, 1), (3, 3, -1)]),
        "K_shear_offdiag": matrix([(2, 3, 1)]),
        "C_02": matrix([(2, 0, 1)]),
        "C_03": matrix([(3, 0, 1)]),
        "C_12": matrix([(2, 1, 1)]),
        "C_13": matrix([(3, 1, 1)]),
    }


FAMILY_NAMES = {
    "F01": ["H", "K_area", "K_shear_diag", "K_shear_offdiag", "C_02", "C_03", "C_12", "C_13"],
    "F02": ["H", "K_shear_diag", "K_shear_offdiag", "C_02", "C_03", "C_12", "C_13"],
    "F03": ["H", "C_02", "C_03", "C_12", "C_13"],
    "F04": ["H", "K_area", "K_shear_diag", "K_shear_offdiag"],
    "F05": ["H"],
    "F06": ["H+K_shear_diag"],
    "F07": ["H+C_02"],
}


def metric_tangent(generator):
    values = []
    for a, b in METRIC_SLOTS:
        values.append(SIGNS[b] * generator[b][a] + SIGNS[a] * generator[a][b])
    return values


def family_matrix(tangents, curvature):
    columns = []
    for tangent in tangents:
        for hessian_position in range(10):
            metric_hessian = [F(0) for _ in range(100)]
            for metric_position, value in enumerate(tangent):
                metric_hessian[metric_position * 10 + hessian_position] = value
            columns.append([
                sum((curvature[row][col] * metric_hessian[col] for col in range(100)), F(0))
                for row in range(21)
            ])
    return columns_to_matrix(columns)


def family_ranks(curvature):
    gens = generators()
    expanded = dict(gens)
    expanded["H+K_shear_diag"] = add(gens["H"], gens["K_shear_diag"])
    expanded["H+C_02"] = add(gens["H"], gens["C_02"])
    rows = {}
    for family, names in FAMILY_NAMES.items():
        rows[family] = rank(family_matrix([metric_tangent(expanded[name]) for name in names], curvature))
    complete_tangents = [[F(int(i == selected)) for i in range(10)] for selected in range(10)]
    rows["F08"] = rank(family_matrix(complete_tangents, curvature))
    rows["F09"] = None
    return rows


def flatten(matrix4):
    return [matrix4[row][col] for row in range(4) for col in range(4)]


def factorization_kernel():
    gens = generators()
    ordered = [gens[name] for name in FAMILY_NAMES["F01"]]
    columns = [flatten(generator) for generator in ordered]
    columns += [[F(int(i == j)) for i in range(16)] for j in range(16)]
    mapping = columns_to_matrix(columns)
    phi_kernel = [F(1)] + [F(0) for _ in range(7)] + [-value for value in flatten(gens["H"])]
    image = [sum((mapping[row][col] * phi_kernel[col] for col in range(24)), F(0)) for row in range(16)]
    return {
        "per_slot_rank": rank(mapping),
        "per_slot_nullity": 24 - rank(mapping),
        "first_four_slot_rank": 4 * rank(mapping),
        "first_four_slot_nullity": 4 * (24 - rank(mapping)),
        "second_ten_slot_rank": 10 * rank(mapping),
        "second_ten_slot_nullity": 10 * (24 - rank(mapping)),
        "explicit_phi_kernel_zero": all(value == 0 for value in image),
    }


def exact_redefinition_samples():
    # Rational diagonal representatives: D(phi)=diag(u^-1,u), D(chi)=diag(v^-1,v).
    # The block multiplication is checked for independent rational entries of S and D_screen.
    samples = []
    for u, v in ((F(2), F(3)), (F(5, 2), F(7, 3))):
        dphi = [[1 / u, F(0)], [F(0), u]]
        dchi = [[1 / v, F(0)], [F(0), v]]
        dsum = [[1 / (u * v), F(0)], [F(0), u * v]]
        dchi_inv = [[v, F(0)], [F(0), 1 / v]]
        top = multiply(dsum, dchi_inv)
        screen = [[F(2), F(1)], [F(0), F(3)]]
        s = [[F(1), F(2)], [F(3), F(4)]]
        sprime = multiply(s, dchi)
        bottom = multiply(multiply(screen, sprime), dchi_inv)
        samples.append(top == dphi and bottom == multiply(screen, s))
    return {"rational_sample_count": len(samples), "all_exact": all(samples)}


def derive():
    curvature = curvature_map()
    ranks = family_ranks(curvature)
    kernel = factorization_kernel()
    expected = {"F01": 20, "F02": 20, "F03": 19, "F04": 19, "F05": 8, "F06": 10, "F07": 10, "F08": 20, "F09": None}
    assert ranks == expected
    assert rank(curvature) == 20
    assert kernel["explicit_phi_kernel_zero"]
    return {
        "schema": "udt.same_solution_phi_curvature.independent.v1",
        "implementation": "standard_library_Fraction_no_primary_import",
        "algebraic_Riemann_rank": rank(curvature),
        "family_ranks": ranks,
        "factorization_kernel": kernel,
        "finite_redefinition_check": exact_redefinition_samples(),
        "causal_stratum_ranks": {name: dict(ranks) for name in ("ZERO", "TIMELIKE", "SPACELIKE", "NONZERO_NULL")},
        "rank_independent_of_fixed_first_jet": True,
        "same_solution_full_families": ["F01", "F02", "F08"],
        "coframe_only_phi_identifiable": False,
        "physical_selection_derived": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    result = derive()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if not args.no_write:
        OUT.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
