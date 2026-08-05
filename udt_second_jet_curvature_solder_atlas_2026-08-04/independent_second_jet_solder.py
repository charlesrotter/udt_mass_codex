#!/usr/bin/env python3
"""Independent standard-library rational reconstruction of the second-jet atlas."""

from __future__ import annotations

import argparse
import itertools
import json
import math
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


def transpose(a):
    return [list(row) for row in zip(*a)] if a else []


def columns_to_matrix(columns):
    return [list(row) for row in zip(*columns)] if columns else []


def hstack(*matrices):
    if not matrices:
        return []
    return [sum((matrix[row] for matrix in matrices), []) for row in range(len(matrices[0]))]


def multiply(a, b):
    if not a:
        return []
    bt = transpose(b)
    return [[sum((x * y for x, y in zip(row, column)), F(0)) for column in bt] for row in a]


def rref(a):
    work = [row[:] for row in a]
    rows = len(work)
    cols = len(work[0]) if rows else 0
    pivots = []
    lead = 0
    for row in range(rows):
        while lead < cols:
            pivot = next((r for r in range(row, rows) if work[r][lead]), None)
            if pivot is not None:
                break
            lead += 1
        if lead == cols:
            break
        work[row], work[pivot] = work[pivot], work[row]
        value = work[row][lead]
        work[row] = [entry / value for entry in work[row]]
        for other in range(rows):
            if other == row:
                continue
            factor = work[other][lead]
            if factor:
                work[other] = [work[other][col] - factor * work[row][col] for col in range(cols)]
        pivots.append(lead)
        lead += 1
    return work, pivots


def rank(a):
    return len(rref(a)[1])


def nullspace(a):
    reduced, pivots = rref(a)
    columns = len(a[0]) if a else 0
    free = [column for column in range(columns) if column not in pivots]
    result = []
    for free_column in free:
        vector = [F(0) for _ in range(columns)]
        vector[free_column] = F(1)
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][free_column]
        result.append(vector)
    return result


def primitive(vector):
    denominator = math.lcm(*(entry.denominator for entry in vector))
    integers = [int(entry * denominator) for entry in vector]
    divisor = math.gcd(*(abs(entry) for entry in integers if entry))
    integers = [entry // divisor for entry in integers]
    if next(entry for entry in integers if entry) < 0:
        integers = [-entry for entry in integers]
    return integers


def metric_index(a, b, m, n):
    return METRIC_SLOTS.index(tuple(sorted((a, b)))) * 10 + HESSIAN_SLOTS.index(tuple(sorted((m, n))))


def metric_value(column, a, b, m, n):
    return F(int(column == metric_index(a, b, m, n)))


def curvature_component(column, a, b, c, d):
    return F(1, 2) * (
        metric_value(column, a, d, b, c)
        + metric_value(column, b, c, a, d)
        - metric_value(column, a, c, b, d)
        - metric_value(column, b, d, a, c)
    )


def curvature_map():
    rows = []
    for i, j in BIV_SLOTS:
        a, b = BIVECTORS[i]
        c, d = BIVECTORS[j]
        rows.append([curvature_component(column, a, b, c, d) for column in range(100)])
    return rows


def coframe_metric_map():
    columns = []
    for hessian_position, _ in enumerate(HESSIAN_SLOTS):
        for A in range(4):
            for a in range(4):
                column = [F(0) for _ in range(100)]
                for metric_position, (left, right) in enumerate(METRIC_SLOTS):
                    value = F(0)
                    if a == left and A == right:
                        value += SIGNS[A]
                    if a == right and A == left:
                        value += SIGNS[A]
                    column[metric_position * 10 + hessian_position] = value
                columns.append(column)
    return columns_to_matrix(columns)


BLOCK_ROWS = {
    "base_base": [BIV_SLOTS.index((0, 0))],
    "mixed_mixed": [BIV_SLOTS.index((i, j)) for i in range(1, 5) for j in range(i, 5)],
    "screen_screen": [BIV_SLOTS.index((5, 5))],
    "base_mixed": [BIV_SLOTS.index((0, i)) for i in range(1, 5)],
    "mixed_screen": [BIV_SLOTS.index((i, 5)) for i in range(1, 5)],
    "base_screen": [BIV_SLOTS.index((0, 5))],
}


TANGENTS = {
    "founded": [[F(2) if slot in ((0, 0), (1, 1)) else F(0) for slot in METRIC_SLOTS]],
    "other_base": [
        [F(-2) if slot == (0, 0) else F(2) if slot == (1, 1) else F(0) for slot in METRIC_SLOTS],
        [F(-2) if slot == (0, 1) else F(0) for slot in METRIC_SLOTS],
    ],
    "screen": [
        [F(2) if slot in ((2, 2), (3, 3)) else F(0) for slot in METRIC_SLOTS],
        [F(2) if slot == (2, 2) else F(-2) if slot == (3, 3) else F(0) for slot in METRIC_SLOTS],
        [F(2) if slot == (2, 3) else F(0) for slot in METRIC_SLOTS],
    ],
    "mixing": [
        [F(-2) if slot == (0, 2) else F(0) for slot in METRIC_SLOTS],
        [F(-2) if slot == (0, 3) else F(0) for slot in METRIC_SLOTS],
        [F(2) if slot == (1, 2) else F(0) for slot in METRIC_SLOTS],
        [F(2) if slot == (1, 3) else F(0) for slot in METRIC_SLOTS],
    ],
}


def category_matrix(category, curvature):
    columns = []
    for tangent in TANGENTS[category]:
        for hessian_position in range(10):
            metric_column = [F(0) for _ in range(100)]
            for metric_position, value in enumerate(tangent):
                metric_column[metric_position * 10 + hessian_position] = value
            columns.append([sum((curvature[row][col] * metric_column[col] for col in range(100)), F(0)) for row in range(21)])
    return columns_to_matrix(columns)


def ensemble_result(curvature):
    categories = ["founded", "other_base", "screen", "mixing"]
    matrices = {category: category_matrix(category, curvature) for category in categories}
    rows = []
    for category in categories:
        rows.append({
            "category": category,
            "image_rank": rank(matrices[category]),
            "block_projection_ranks": {name: rank([matrices[category][row] for row in indices]) for name, indices in BLOCK_ROWS.items()},
        })
    unions = []
    for length in range(1, 5):
        for subset in itertools.combinations(categories, length):
            unions.append({"categories": list(subset), "image_rank": rank(hstack(*(matrices[name] for name in subset)))})
    union_rank = {tuple(row["categories"]): row["image_rank"] for row in unions}
    minimal_full = []
    for subset, image_rank in union_rank.items():
        if image_rank != 20:
            continue
        if not any(
            union_rank.get(candidate) == 20
            for length in range(1, len(subset))
            for candidate in itertools.combinations(subset, length)
        ):
            minimal_full.append(list(subset))
    intersections = []
    for left, right in itertools.combinations(categories, 2):
        intersections.append({
            "left": left,
            "right": right,
            "intersection_dimension": rank(matrices[left]) + rank(matrices[right]) - rank(hstack(matrices[left], matrices[right])),
        })
    return {"category_rows": rows, "union_rows": unions, "minimal_full_category_sets": minimal_full, "pairwise_intersections": intersections}


def bivector_coefficient(slot, a, b, c, d):
    if a == b or c == d:
        return F(0)
    sign1 = F(1) if a < b else F(-1)
    sign2 = F(1) if c < d else F(-1)
    i = BIVECTORS.index(tuple(sorted((a, b))))
    j = BIVECTORS.index(tuple(sorted((c, d))))
    target = tuple(sorted((i, j)))
    return sign1 * sign2 if BIV_SLOTS[slot] == target else F(0)


def tidal_map(p, quotient_basis, curvature):
    v = [SIGNS[i] * p[i] for i in range(4)]
    output_rows = []
    for i in range(len(quotient_basis)):
        for j in range(i, len(quotient_basis)):
            row = []
            for slot in range(21):
                value = F(0)
                for a, b, c, d in itertools.product(range(4), repeat=4):
                    value += quotient_basis[i][a] * quotient_basis[j][b] * v[c] * v[d] * bivector_coefficient(slot, a, c, b, d)
                row.append(value)
            output_rows.append(row)
    return multiply(output_rows, curvature) if output_rows else []


def matrix_rank_4(matrix):
    return rank(matrix)


def N_matrix(p):
    v = [SIGNS[i] * p[i] for i in range(4)]
    s = sum((p[i] * v[i] for i in range(4)), F(0))
    return [[s * int(i == j) - v[i] * p[j] for j in range(4)] for i in range(4)], s


def depth_rows(curvature):
    e = [[F(int(i == j)) for i in range(4)] for j in range(4)]
    strata = [
        ("timelike", [F(1), F(0), F(0), F(0)], [e[i] for i in (1, 2, 3)]),
        ("spacelike", [F(0), F(1), F(0), F(0)], [e[i] for i in (0, 2, 3)]),
        ("nonzero_null", [F(1), F(1), F(0), F(0)], [e[i] for i in (2, 3)]),
        ("zero", [F(0), F(0), F(0), F(0)], []),
    ]
    rows = []
    for name, p, quotient in strata:
        nmap, s = N_matrix(p)
        n2 = multiply(nmap, nmap)
        sN = [[s * value for value in row] for row in nmap]
        image = tidal_map(p, quotient, curvature)
        representative_independence = None
        if name == "nonzero_null":
            v = [SIGNS[i] * p[i] for i in range(4)]
            shifted_quotient = [
                [quotient[0][i] + v[i] for i in range(4)],
                [quotient[1][i] - F(2) * v[i] for i in range(4)],
            ]
            representative_independence = tidal_map(p, shifted_quotient, curvature) == image
        rows.append({
            "stratum": name,
            "s_phi": int(s),
            "N_rank": matrix_rank_4(nmap),
            "N_squared_equals_sN": n2 == sN,
            "N_nonzero_nilpotent": name == "nonzero_null" and matrix_rank_4(nmap) == 1 and all(value == 0 for row in n2 for value in row),
            "quotient_dimension": len(quotient),
            "tidal_image_rank": rank(image),
            "null_quotient_representative_independence": representative_independence,
        })
    return rows


def render(value):
    if isinstance(value, F):
        return int(value) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    if isinstance(value, list):
        return [render(item) for item in value]
    if isinstance(value, dict):
        return {key: render(item) for key, item in value.items()}
    return value


def derive():
    curvature = curvature_map()
    coframe_metric = coframe_metric_map()
    coframe_curvature = multiply(curvature, coframe_metric)
    relations = nullspace(transpose(curvature))
    blocks = [{"block": name, "projection_rank": rank([curvature[row] for row in indices])} for name, indices in BLOCK_ROWS.items()]
    ensembles = ensemble_result(curvature)
    return render({
        "schema": "udt.second_jet_curvature_solder.independent.v1",
        "map_ranks": {
            "coframe_to_metric": rank(coframe_metric),
            "metric_to_Riemann": rank(curvature),
            "coframe_to_Riemann": rank(coframe_curvature),
        },
        "Bianchi_relation_dimension": len(relations),
        "Bianchi_primitive_relation": primitive(relations[0]),
        "block_rows": blocks,
        "ensembles": ensembles,
        "depth_rows": depth_rows(curvature),
        "same_solution_source_dphi_join_derived": False,
        "physical_evolution_operator_derived": False,
        "unique_curvature_solder_derived": False,
    })


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
