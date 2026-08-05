#!/usr/bin/env python3
"""Primary exact algebra for the complete second-jet curvature-solder atlas."""

from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
RESULT_PATH = HERE / "RESULT.json"
ETA = sp.diag(-1, 1, 1, 1)
METRIC_SLOTS = [(a, b) for a in range(4) for b in range(a, 4)]
HESSIAN_SLOTS = [(m, n) for m in range(4) for n in range(m, 4)]
BIVECTORS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
BIV_SLOTS = [(i, j) for i in range(6) for j in range(i, 6)]


def rank(matrix: sp.Matrix) -> int:
    return int(matrix.rank())


def primitive_relation(vector: sp.Matrix) -> list[int]:
    rationals = [sp.Rational(value) for value in vector]
    denominator = sp.ilcm(*(value.q for value in rationals))
    integers = [int(value * denominator) for value in rationals]
    divisor = math.gcd(*(abs(value) for value in integers if value))
    integers = [value // divisor for value in integers]
    first = next(value for value in integers if value)
    if first < 0:
        integers = [-value for value in integers]
    return integers


def coframe_metric_map() -> sp.Matrix:
    columns = []
    for hslot in HESSIAN_SLOTS:
        for flat in range(16):
            x = sp.zeros(4)
            x[flat // 4, flat % 4] = 1
            tangent = x.T * ETA + ETA * x
            column = []
            for metric_slot, derivative_slot in itertools.product(METRIC_SLOTS, HESSIAN_SLOTS):
                column.append(tangent[metric_slot] if derivative_slot == hslot else 0)
            columns.append(sp.Matrix(column))
    return sp.Matrix.hstack(*columns)


def metric_index(a: int, b: int, m: int, n: int) -> int:
    ab = tuple(sorted((a, b)))
    mn = tuple(sorted((m, n)))
    return METRIC_SLOTS.index(ab) * len(HESSIAN_SLOTS) + HESSIAN_SLOTS.index(mn)


def metric_hessian_basis_value(column: int, a: int, b: int, m: int, n: int) -> int:
    return int(column == metric_index(a, b, m, n))


def riemann_component_column(column: int, a: int, b: int, c: int, d: int) -> sp.Rational:
    # R_abcd = 1/2 (g_ad,bc + g_bc,ad - g_ac,bd - g_bd,ac).
    return sp.Rational(1, 2) * (
        metric_hessian_basis_value(column, a, d, b, c)
        + metric_hessian_basis_value(column, b, c, a, d)
        - metric_hessian_basis_value(column, a, c, b, d)
        - metric_hessian_basis_value(column, b, d, a, c)
    )


def curvature_map() -> sp.Matrix:
    rows = []
    for i, j in BIV_SLOTS:
        a, b = BIVECTORS[i]
        c, d = BIVECTORS[j]
        rows.append([riemann_component_column(column, a, b, c, d) for column in range(100)])
    return sp.Matrix(rows)


def full_riemann_from_column(column: int):
    return [[[[riemann_component_column(column, a, b, c, d) for d in range(4)] for c in range(4)] for b in range(4)] for a in range(4)]


def riemann_symmetry_result(curvature: sp.Matrix):
    pair_antisymmetry = pair_exchange = bianchi = True
    for column in range(curvature.cols):
        r = full_riemann_from_column(column)
        for a, b, c, d in itertools.product(range(4), repeat=4):
            pair_antisymmetry &= r[a][b][c][d] == -r[b][a][c][d]
            pair_antisymmetry &= r[a][b][c][d] == -r[a][b][d][c]
            pair_exchange &= r[a][b][c][d] == r[c][d][a][b]
            bianchi &= r[a][b][c][d] + r[a][c][d][b] + r[a][d][b][c] == 0
    relations = curvature.T.nullspace()
    return {
        "pair_antisymmetries_exact": bool(pair_antisymmetry),
        "pair_exchange_exact": bool(pair_exchange),
        "algebraic_Bianchi_exact": bool(bianchi),
        "bivector_symmetric_entries": len(BIV_SLOTS),
        "relation_dimension_among_21_entries": len(relations),
        "primitive_relation": primitive_relation(relations[0]),
        "relation_nonzero_entries": [
            {"slot": list(BIV_SLOTS[i]), "bivectors": [list(BIVECTORS[BIV_SLOTS[i][0]]), list(BIVECTORS[BIV_SLOTS[i][1]])], "coefficient": value}
            for i, value in enumerate(primitive_relation(relations[0])) if value
        ],
    }


BLOCK_ROWS = {
    "base_base": [BIV_SLOTS.index((0, 0))],
    "mixed_mixed": [BIV_SLOTS.index((i, j)) for i in range(1, 5) for j in range(i, 5)],
    "screen_screen": [BIV_SLOTS.index((5, 5))],
    "base_mixed": [BIV_SLOTS.index((0, i)) for i in range(1, 5)],
    "mixed_screen": [BIV_SLOTS.index((i, 5)) for i in range(1, 5)],
    "base_screen": [BIV_SLOTS.index((0, 5))],
}


def block_result(curvature: sp.Matrix):
    rows = []
    for name, indices in BLOCK_ROWS.items():
        projected = curvature[indices, :]
        rows.append(
            {
                "block": name,
                "displayed_entries": len(indices),
                "projection_rank": rank(projected),
                "all_entries_individually_nonzero_available": all(any(curvature[index, column] != 0 for column in range(curvature.cols)) for index in indices),
            }
        )
    return {
        "bivector_order": [list(pair) for pair in BIVECTORS],
        "rows": rows,
        "all_six_block_classes_nonzero": all(row["projection_rank"] > 0 for row in rows),
        "sum_displayed_entries": sum(row["displayed_entries"] for row in rows),
        "joint_rank": rank(curvature),
        "joint_relation_count": len(BIV_SLOTS) - rank(curvature),
    }


def tangent_generators():
    generators = []

    def add_generator(name, category, matrix):
        generators.append((name, category, matrix))

    add_generator("founded_reciprocal_H", "founded", sp.diag(-1, 1, 0, 0))
    add_generator("base_common_scale", "other_base", sp.diag(1, 1, 0, 0))
    base_offdiag = sp.zeros(4)
    base_offdiag[0, 1] = 1
    base_offdiag[1, 0] = -1
    add_generator("base_offdiagonal", "other_base", base_offdiag)
    add_generator("screen_area", "screen", sp.diag(0, 0, 1, 1))
    add_generator("screen_diagonal_shear", "screen", sp.diag(0, 0, 1, -1))
    screen_offdiag = sp.zeros(4)
    screen_offdiag[2, 3] = screen_offdiag[3, 2] = 1
    add_generator("screen_offdiagonal_shear", "screen", screen_offdiag)
    for a in (0, 1):
        for b in (2, 3):
            generator = sp.zeros(4)
            generator[a, b] = 1
            generator[b, a] = 1 if a == 1 else -1
            add_generator(f"mixing_{a}{b}", "mixing", generator)
    return generators


def generator_curvature_columns(curvature: sp.Matrix):
    result = {}
    for name, category, generator in tangent_generators():
        tangent = generator.T * ETA + ETA * generator
        columns = []
        for hslot in HESSIAN_SLOTS:
            metric_jet = sp.zeros(100, 1)
            for metric_position, metric_slot in enumerate(METRIC_SLOTS):
                metric_jet[metric_position * 10 + HESSIAN_SLOTS.index(hslot)] = tangent[metric_slot]
            columns.append(curvature * metric_jet)
        result[name] = {"category": category, "matrix": sp.Matrix.hstack(*columns)}
    return result


def ensemble_result(curvature: sp.Matrix):
    generated = generator_curvature_columns(curvature)
    categories = ["founded", "other_base", "screen", "mixing"]
    category_matrices = {}
    generator_rows = []
    for name, payload in generated.items():
        generator_rows.append({"generator": name, "category": payload["category"], "image_rank": rank(payload["matrix"])})
    for category in categories:
        category_matrices[category] = sp.Matrix.hstack(*(payload["matrix"] for payload in generated.values() if payload["category"] == category))

    category_rows = []
    for category in categories:
        matrix = category_matrices[category]
        block_ranks = {name: rank(matrix[indices, :]) for name, indices in BLOCK_ROWS.items()}
        category_rows.append({"category": category, "generator_count": sum(payload["category"] == category for payload in generated.values()), "image_rank": rank(matrix), "block_projection_ranks": block_ranks})

    union_rows = []
    for length in range(1, len(categories) + 1):
        for subset in itertools.combinations(categories, length):
            matrix = sp.Matrix.hstack(*(category_matrices[name] for name in subset))
            union_rows.append({"categories": list(subset), "image_rank": rank(matrix)})

    union_rank = {tuple(row["categories"]): row["image_rank"] for row in union_rows}
    minimal_full = []
    for subset, image_rank in union_rank.items():
        if image_rank != 20:
            continue
        proper_full = any(
            union_rank.get(candidate) == 20
            for length in range(1, len(subset))
            for candidate in itertools.combinations(subset, length)
        )
        if not proper_full:
            minimal_full.append(list(subset))

    intersections = []
    for left, right in itertools.combinations(categories, 2):
        r_left = rank(category_matrices[left])
        r_right = rank(category_matrices[right])
        r_union = rank(sp.Matrix.hstack(category_matrices[left], category_matrices[right]))
        intersections.append({"left": left, "right": right, "intersection_dimension": r_left + r_right - r_union})
    return {
        "generator_rows": generator_rows,
        "category_rows": category_rows,
        "all_nonempty_category_unions": union_rows,
        "minimal_full_category_sets": minimal_full,
        "pairwise_intersections": intersections,
        "complete_union_rank": next(row["image_rank"] for row in union_rows if len(row["categories"]) == 4),
    }


def bivector_entry_symbols():
    variables = sp.symbols("r0:21")
    matrix = sp.zeros(6)
    for variable, (i, j) in zip(variables, BIV_SLOTS):
        matrix[i, j] = matrix[j, i] = variable
    return variables, matrix


def bivector_component(matrix: sp.Matrix, a: int, b: int, c: int, d: int):
    if a == b or c == d:
        return sp.Integer(0)
    sign1 = 1 if a < b else -1
    sign2 = 1 if c < d else -1
    pair1 = tuple(sorted((a, b)))
    pair2 = tuple(sorted((c, d)))
    return sign1 * sign2 * matrix[BIVECTORS.index(pair1), BIVECTORS.index(pair2)]


def tidal_output_map(p: sp.Matrix, quotient_basis: list[sp.Matrix], curvature: sp.Matrix):
    variables, bivmatrix = bivector_entry_symbols()
    v = ETA * p
    tidal = sp.Matrix(4, 4, lambda a, b: sp.expand(sum(
        bivector_component(bivmatrix, a, c, b, d) * v[c] * v[d]
        for c in range(4) for d in range(4)
    )))
    outputs = []
    for i in range(len(quotient_basis)):
        for j in range(i, len(quotient_basis)):
            outputs.append(sp.expand((quotient_basis[i].T * tidal * quotient_basis[j])[0]))
    coefficient = sp.Matrix(outputs).jacobian(variables) if outputs else sp.zeros(0, len(variables))
    image = coefficient * curvature
    annihilates_v = all(sp.expand((v.T * tidal)[j]) == 0 for j in range(4))
    return tidal, image, annihilates_v


def matrix_as_ints(matrix: sp.Matrix):
    return [[int(matrix[i, j]) for j in range(matrix.cols)] for i in range(matrix.rows)]


def depth_strata_result(curvature: sp.Matrix):
    strata = [
        ("timelike", sp.Matrix([1, 0, 0, 0]), [sp.eye(4)[:, i] for i in (1, 2, 3)]),
        ("spacelike", sp.Matrix([0, 1, 0, 0]), [sp.eye(4)[:, i] for i in (0, 2, 3)]),
        ("nonzero_null", sp.Matrix([1, 1, 0, 0]), [sp.eye(4)[:, i] for i in (2, 3)]),
        ("zero", sp.zeros(4, 1), []),
    ]
    rows = []
    for name, p, quotient_basis in strata:
        v = ETA * p
        s = int((p.T * ETA * p)[0])
        nmap = s * sp.eye(4) - v * p.T
        tidal, image, annihilates_v = tidal_output_map(p, quotient_basis, curvature)
        null_descent = True
        if name == "nonzero_null":
            x = sp.Matrix(sp.symbols("x0:4"))
            null_descent = sp.expand((v.T * tidal * x)[0]) == 0 and sp.expand((x.T * tidal * v)[0]) == 0
        rows.append(
            {
                "stratum": name,
                "p_covector": [int(value) for value in p],
                "p_sharp": [int(value) for value in v],
                "s_phi": s,
                "N": matrix_as_ints(nmap),
                "N_rank": rank(nmap),
                "N_squared_equals_s_times_N": nmap * nmap == s * nmap,
                "N_nilpotent_nonzero": bool(name == "nonzero_null" and nmap != sp.zeros(4) and nmap * nmap == sp.zeros(4)),
                "quotient_dimension": len(quotient_basis),
                "tidal_symmetric_components": len(quotient_basis) * (len(quotient_basis) + 1) // 2,
                "tidal_image_rank": rank(image),
                "tidal_annihilates_p_sharp": bool(annihilates_v),
                "null_quotient_representative_independence": bool(null_descent) if name == "nonzero_null" else None,
            }
        )
    return {
        "rows": rows,
        "nonnull_N_rank_three": all(row["N_rank"] == 3 for row in rows[:2]),
        "null_N_rank_one_nilpotent": rows[2]["N_rank"] == 1 and rows[2]["N_nilpotent_nonzero"],
        "zero_N_and_tidal": rows[3]["N_rank"] == 0 and rows[3]["tidal_image_rank"] == 0,
        "constant_rank_normalized_screen_across_all_strata": False,
    }


def derive():
    coframe_metric = coframe_metric_map()
    curvature = curvature_map()
    coframe_curvature = curvature * coframe_metric
    symmetries = riemann_symmetry_result(curvature)
    blocks = block_result(curvature)
    ensembles = ensemble_result(curvature)
    depth = depth_strata_result(curvature)

    conditions = [
        rank(coframe_metric) == 100,
        rank(curvature) == 20,
        rank(coframe_curvature) == 20,
        symmetries["relation_dimension_among_21_entries"] == 1,
        blocks["all_six_block_classes_nonzero"],
        ensembles["complete_union_rank"] == 20,
        depth["null_N_rank_one_nilpotent"],
        next(row for row in depth["rows"] if row["stratum"] == "nonzero_null")["tidal_image_rank"] == 3,
    ]
    assert all(conditions)
    outcome = (
        "DERIVED_COMPLETE_SECOND_JET_CURVATURE_SURJECTION__"
        "DERIVED_SINGLE_BIANCHI_RECIPROCAL_ANGULAR_BLOCK_RELATION__"
        "DERIVED_CAUSAL_STRATUM_TIDAL_QUOTIENTS__"
        "NO_UNIQUE_CURVATURE_SOLDER_OR_KINEMATIC_EVOLUTION_RETURN"
    )
    return {
        "schema": "udt.second_jet_curvature_solder.v1",
        "sympy_version": sp.__version__,
        "curvature_convention": "R_abcd=1/2(g_ad,bc+g_bc,ad-g_ac,bd-g_bd,ac)",
        "outcome": outcome,
        "second_jet_maps": {
            "coframe_second_jet_components": coframe_metric.cols,
            "metric_second_jet_components": coframe_metric.rows,
            "coframe_to_metric_rank": rank(coframe_metric),
            "coframe_to_metric_nullity": coframe_metric.cols - rank(coframe_metric),
            "metric_to_Riemann_rank": rank(curvature),
            "metric_to_Riemann_nullity": curvature.cols - rank(curvature),
            "coframe_to_Riemann_rank": rank(coframe_curvature),
            "coframe_to_Riemann_nullity": coframe_curvature.cols - rank(coframe_curvature),
            "all_ten_Hessian_slots_released": len(HESSIAN_SLOTS) == 10,
            "time_time_slots": 1,
            "time_space_slots": 3,
            "space_space_slots": 6,
            "extra_kinematic_curvature_constraint_count": 20 - rank(curvature),
        },
        "Riemann_identities": symmetries,
        "bivector_blocks": blocks,
        "source_ensembles": ensembles,
        "depth_strata": depth,
        "rank_and_asymptotic_boundary": {
            "Levi_Civita_curvature_defined_only_at_coframe_rank_four": True,
            "generalized_inverse_or_curvature_continuation_derived": False,
            "finite_phi_pair_determinant": -1,
            "finite_phi_rank_loss": False,
            "phi_asymptotes_are_limit_only": True,
            "Xmax_derived": False,
        },
        "configuration_path_is_physical_time": False,
        "same_solution_source_dphi_join_derived": False,
        "physical_evolution_operator_derived": False,
        "native_bootstrap_return_derived": False,
        "unique_curvature_solder_derived": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    result = derive()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if not args.no_write:
        RESULT_PATH.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
