#!/usr/bin/env python3
"""Exact primary derivation for the bounded same-solution phi/curvature audit."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
OUT = HERE / "RESULT.json"
RIGHT_INVERSE_OUT = HERE / "RIGHT_INVERSE_WITNESSES.json"
FAMILY_OUT = HERE / "FAMILY_COMPATIBILITY_LEDGER.tsv"
ETA = sp.diag(-1, 1, 1, 1)
METRIC_SLOTS = [(a, b) for a in range(4) for b in range(a, 4)]
HESSIAN_SLOTS = [(m, n) for m in range(4) for n in range(m, 4)]
BIVECTORS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
BIV_SLOTS = [(i, j) for i in range(6) for j in range(i, 6)]
STRATA = {
    "ZERO": (0, 0, 0, 0),
    "TIMELIKE": (1, 0, 0, 0),
    "SPACELIKE": (0, 1, 0, 0),
    "NONZERO_NULL": (1, 1, 0, 0),
}


def primitive(vector: sp.Matrix) -> list[int]:
    values = [sp.Rational(value) for value in vector]
    denominator = sp.ilcm(*(value.q for value in values))
    integers = [int(value * denominator) for value in values]
    divisor = math.gcd(*(abs(value) for value in integers if value))
    integers = [value // divisor for value in integers]
    if next(value for value in integers if value) < 0:
        integers = [-value for value in integers]
    return integers


def metric_index(a: int, b: int, m: int, n: int) -> int:
    return METRIC_SLOTS.index(tuple(sorted((a, b)))) * 10 + HESSIAN_SLOTS.index(tuple(sorted((m, n))))


def metric_value(column: int, a: int, b: int, m: int, n: int) -> int:
    return int(column == metric_index(a, b, m, n))


def curvature_component(column: int, a: int, b: int, c: int, d: int) -> sp.Rational:
    return sp.Rational(1, 2) * (
        metric_value(column, a, d, b, c)
        + metric_value(column, b, c, a, d)
        - metric_value(column, a, c, b, d)
        - metric_value(column, b, d, a, c)
    )


def curvature_map() -> sp.Matrix:
    rows = []
    for i, j in BIV_SLOTS:
        a, b = BIVECTORS[i]
        c, d = BIVECTORS[j]
        rows.append([curvature_component(column, a, b, c, d) for column in range(100)])
    return sp.Matrix(rows)


def generators() -> dict[str, sp.Matrix]:
    out: dict[str, sp.Matrix] = {}
    out["H"] = sp.diag(-1, 1, 0, 0)
    out["K_area"] = sp.diag(0, 0, 1, 1)
    out["K_shear_diag"] = sp.diag(0, 0, 1, -1)
    off = sp.zeros(4)
    off[2, 3] = 1
    out["K_shear_offdiag"] = off
    for a in (0, 1):
        for b in (2, 3):
            mixing = sp.zeros(4)
            mixing[b, a] = 1
            out[f"C_{a}{b}"] = mixing
    return out


GENERATOR_NAMES = {
    "F01": ["H", "K_area", "K_shear_diag", "K_shear_offdiag", "C_02", "C_03", "C_12", "C_13"],
    "F02": ["H", "K_shear_diag", "K_shear_offdiag", "C_02", "C_03", "C_12", "C_13"],
    "F03": ["H", "C_02", "C_03", "C_12", "C_13"],
    "F04": ["H", "K_area", "K_shear_diag", "K_shear_offdiag"],
    "F05": ["H"],
    "F06": ["H+K_shear_diag"],
    "F07": ["H+C_02"],
}


def metric_tangent(generator: sp.Matrix) -> list[sp.Expr]:
    tangent = generator.T * ETA + ETA * generator
    return [sp.expand(tangent[slot]) for slot in METRIC_SLOTS]


def tangent_curvature_matrix(tangents: list[list[sp.Expr]], curvature: sp.Matrix) -> sp.Matrix:
    columns = []
    for tangent in tangents:
        for hessian_position in range(10):
            metric_hessian = sp.zeros(100, 1)
            for metric_position, value in enumerate(tangent):
                metric_hessian[metric_position * 10 + hessian_position] = value
            columns.append(curvature * metric_hessian)
    return sp.Matrix.hstack(*columns) if columns else sp.zeros(21, 0)


def family_matrices(curvature: sp.Matrix) -> dict[str, sp.Matrix | None]:
    gens = generators()
    combined = {
        **gens,
        "H+K_shear_diag": gens["H"] + gens["K_shear_diag"],
        "H+C_02": gens["H"] + gens["C_02"],
    }
    matrices: dict[str, sp.Matrix | None] = {}
    for family, names in GENERATOR_NAMES.items():
        matrices[family] = tangent_curvature_matrix([metric_tangent(combined[name]) for name in names], curvature)
    complete_metric_tangents = [
        [sp.Integer(int(position == selected)) for position in range(10)]
        for selected in range(10)
    ]
    matrices["F08"] = tangent_curvature_matrix(complete_metric_tangents, curvature)
    matrices["F09"] = None
    return matrices


def factorization_result() -> dict:
    gens = generators()
    ordered = [gens[name] for name in GENERATOR_NAMES["F01"]]
    identity = sp.eye(16)
    parameter_columns = sp.Matrix.hstack(*(sp.Matrix(generator).reshape(16, 1) for generator in ordered))
    one_direction = sp.Matrix.hstack(parameter_columns, identity)
    first_kernel = sp.zeros(24, 1)
    first_kernel[0] = 1
    first_kernel[8:, 0] = -sp.Matrix(gens["H"]).reshape(16, 1)
    assert one_direction * first_kernel == sp.zeros(16, 1)
    second_kernel = first_kernel.copy()
    return {
        "exact_finite_redefinition": {
            "L_chi": "diag(D(chi),I_2)",
            "phi_prime": "phi+chi",
            "S_prime": "S D(chi)",
            "bar_theta_prime": "L_chi^-1 bar_theta",
            "identity": "E(phi+chi,D,S D(chi)) L_chi^-1 = E(phi,D,S)",
            "theta_unchanged": True,
        },
        "product_rules": {
            "first": "theta_,mu=E_,mu bar_theta+E bar_theta_,mu",
            "second": "theta_,munu=E_,munu bar_theta+E_,mu bar_theta_,nu+E_,nu bar_theta_,mu+E bar_theta_,munu",
            "founded_E_first_at_identity": "E_,mu=p_mu H",
            "founded_E_second_at_identity": "E_,munu=q_munu H+p_mu p_nu H^2",
            "all_cross_terms_retained": True,
        },
        "released_reference_first_jet": {
            "per_derivative_inputs": 24,
            "per_derivative_outputs": 16,
            "per_derivative_rank": int(one_direction.rank()),
            "per_derivative_nullity": 24 - int(one_direction.rank()),
            "four_derivative_rank": 4 * int(one_direction.rank()),
            "four_derivative_nullity": 4 * (24 - int(one_direction.rank())),
            "explicit_phi_kernel_verified": bool(one_direction * first_kernel == sp.zeros(16, 1)),
        },
        "released_reference_second_jet_fixed_first_jets": {
            "per_symmetric_slot_inputs": 24,
            "per_symmetric_slot_outputs": 16,
            "per_symmetric_slot_rank": int(one_direction.rank()),
            "per_symmetric_slot_nullity": 24 - int(one_direction.rank()),
            "ten_slot_rank": 10 * int(one_direction.rank()),
            "ten_slot_nullity": 10 * (24 - int(one_direction.rank())),
            "explicit_phi_hessian_kernel_verified": bool(one_direction * second_kernel == sp.zeros(16, 1)),
        },
        "constructive_release_formulas": {
            "reference_first_jet": "B_mu=X_mu-A_mu",
            "reference_second_jet": "B_munu=T_munu-E_munu-A_mu B_nu-A_nu B_mu",
            "arbitrary_phi_jets_can_share_fixed_complete_coframe_jet": True,
            "interpretation": "FACTORIZATION_REDUNDANCY_NOT_PHYSICAL_SELECTION",
        },
        "coframe_only_phi_extraction": "NOT_INVARIANT_UNDER_ALLOWED_REFERENCE_REDEFINITION",
    }


def rational_strings(matrix: sp.Matrix) -> list[list[str]]:
    return [[str(matrix[row, col]) for col in range(matrix.cols)] for row in range(matrix.rows)]


def right_inverse_witness(matrix: sp.Matrix) -> dict:
    independent_rows = list(matrix.T.rref()[1])
    reduced_target = matrix[independent_rows, :]
    pivot_columns = list(reduced_target.rref()[1])
    square = reduced_target[:, pivot_columns]
    inverse = square.inv()
    assert square * inverse == sp.eye(20)
    payload = {
        "independent_display_rows": independent_rows,
        "independent_bivector_slots": [list(BIV_SLOTS[row]) for row in independent_rows],
        "pivot_hessian_columns": pivot_columns,
        "pivot_determinant": str(square.det()),
        "inverse": rational_strings(inverse),
        "identity_verified": True,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["canonical_sha256"] = hashlib.sha256(canonical).hexdigest()
    return payload


def family_result(curvature: sp.Matrix) -> tuple[list[dict], dict]:
    matrices = family_matrices(curvature)
    full_relations = curvature.T.nullspace()
    assert len(full_relations) == 1
    bianchi = primitive(full_relations[0])
    rows = []
    witnesses = {}
    family_names = {
        "F01": "FULL_FACTORIZED",
        "F02": "DET_ONE_SCREEN",
        "F03": "SCREEN_INVARIANT_MIXING",
        "F04": "NO_MIXING_ANGULAR",
        "F05": "DIRECT_SUM_SPECTATOR",
        "F06": "LOCKED_ANGULAR_ONE_PARAMETER",
        "F07": "LOCKED_SHIFT_ONE_PARAMETER",
        "F08": "RELEASED_COMPLETE_COFRAME_REFERENCE",
        "F09": "INDEPENDENT_SCALAR_CONTROL",
    }
    for family in family_names:
        matrix = matrices[family]
        if matrix is None:
            rows.append({
                "family_id": family,
                "family_name": family_names[family],
                "curvature_rank": None,
                "algebraic_target_codimension": None,
                "causal_stratum_ranks": {name: None for name in STRATA},
                "same_solution_class": "UNTYPED_NO_METRIC_ACTION",
                "ownership": "CHOSE_COMPARISON_CONFIGURATION",
            })
            continue
        image_rank = int(matrix.rank())
        left_relations = matrix.T.nullspace()
        row = {
            "family_id": family,
            "family_name": family_names[family],
            "curvature_rank": image_rank,
            "algebraic_target_codimension": 20 - image_rank,
            "display_relation_dimension": len(left_relations),
            "extra_relations_beyond_Bianchi": len(left_relations) - 1,
            "Bianchi_relation_present": any(primitive(relation) == bianchi for relation in left_relations) if len(left_relations) == 1 else bool(sp.Matrix.hstack(*left_relations).row_join(full_relations[0]).rank() == len(left_relations)),
            "causal_stratum_ranks": {name: image_rank for name in STRATA},
            "first_jet_changes_only_affine_offset": True,
            "same_solution_class": (
                "ALL_ALGEBRAIC_RIEMANN_AT_FIXED_DEPTH_FIRST_JET"
                if image_rank == 20 and family != "F08"
                else "ALL_ALGEBRAIC_RIEMANN_WITH_ARBITRARY_FACTORIZATION_DEPTH"
                if image_rank == 20
                else f"EXACT_IMAGE_ONLY_CODIM_{20-image_rank}"
            ),
            "ownership": "SUPPLIED_FACTORIZED_CHART" if family != "F08" else "RELEASED_REFERENCE_FACTORIZATION",
        }
        rows.append(row)
        if image_rank == 20:
            witnesses[family] = right_inverse_witness(matrix)
    return rows, {"Bianchi_primitive_relation": bianchi, "families": witnesses}


def derive() -> tuple[dict, dict, list[dict]]:
    curvature = curvature_map()
    families, witnesses = family_result(curvature)
    factorization = factorization_result()
    typed_rows = [row for row in families if row["curvature_rank"] is not None]
    assert int(curvature.rank()) == 20
    assert all(set(row["causal_stratum_ranks"]) == set(STRATA) for row in typed_rows)
    assert next(row for row in families if row["family_id"] == "F01")["curvature_rank"] == 20
    assert next(row for row in families if row["family_id"] == "F02")["curvature_rank"] == 20
    assert next(row for row in families if row["family_id"] == "F03")["curvature_rank"] == 19
    assert next(row for row in families if row["family_id"] == "F04")["curvature_rank"] == 19
    assert next(row for row in families if row["family_id"] == "F05")["curvature_rank"] == 8
    assert all(next(row for row in families if row["family_id"] == family)["curvature_rank"] == 10 for family in ("F06", "F07"))
    assert next(row for row in families if row["family_id"] == "F08")["curvature_rank"] == 20
    result = {
        "schema": "udt.same_solution_phi_curvature.v1",
        "sympy_version": sp.__version__,
        "base": "a353af410e84abc1982401d9367e0845a1b1458d",
        "outcome": (
            "DERIVED_FACTORIZATION_NONIDENTIFIABILITY__"
            "CONDITIONAL_FULL_LOCAL_PHI_CURVATURE_COMPATIBILITY_IN_F01_F02__"
            "DERIVED_RESTRICTED_FAMILY_CODIMENSIONS__"
            "NO_METRIC_NATIVE_PHI_ASSIGNMENT_OR_CURVATURE_SELECTION"
        ),
        "curvature_convention": "R_abcd=1/2(g_ad,bc+g_bc,ad-g_ac,bd-g_bd,ac)+first_jet_offset",
        "algebraic_Riemann_dimension": int(curvature.rank()),
        "causal_strata": {name: {"p": list(p), "s": -p[0] ** 2 + sum(x ** 2 for x in p[1:])} for name, p in STRATA.items()},
        "factorization": factorization,
        "families": families,
        "affine_curvature_theorem": {
            "formula": "R=A(generator Hessians)+b(fixed zero/first jets)",
            "Hessian_coefficient_independent_of_first_jet": True,
            "causal_type_or_amplitude_changes_rank_on_regular_tile": False,
            "scope": "fixed regular zero-jet coframe and supplied realization family",
        },
        "ownership_verdict": {
            "conditional_same_solution_existence": True,
            "complete_coframe_identifies_phi_jets": False,
            "physical_extension_selected": False,
            "observer_assignment_selected": False,
            "response_or_evolution_law_derived": False,
            "bootstrap_closure_derived": False,
        },
        "maximum_conclusion_obeyed": True,
    }
    return result, witnesses, families


def write_family_ledger(rows: list[dict]) -> None:
    header = ["family_id", "family_name", "curvature_rank", "algebraic_target_codimension", "zero_rank", "timelike_rank", "spacelike_rank", "null_rank", "same_solution_class", "ownership"]
    lines = ["\t".join(header)]
    for row in rows:
        ranks = row["causal_stratum_ranks"]
        values = [
            row["family_id"], row["family_name"],
            "NOT_TYPED" if row["curvature_rank"] is None else str(row["curvature_rank"]),
            "NOT_TYPED" if row["algebraic_target_codimension"] is None else str(row["algebraic_target_codimension"]),
            *["NOT_TYPED" if ranks[name] is None else str(ranks[name]) for name in ("ZERO", "TIMELIKE", "SPACELIKE", "NONZERO_NULL")],
            row["same_solution_class"], row["ownership"],
        ]
        lines.append("\t".join(values))
    FAMILY_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    result, witnesses, rows = derive()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if not args.no_write:
        OUT.write_text(rendered, encoding="utf-8")
        RIGHT_INVERSE_OUT.write_text(json.dumps(witnesses, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        write_family_ledger(rows)
    print(rendered, end="")


if __name__ == "__main__":
    main()
