#!/usr/bin/env python3
"""Independent stdlib/Fraction reconstruction; does not read production results."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import subprocess
from collections import Counter
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
Q = Fraction


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(name: str, rows: list[dict[str, str]], fields: list[str]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def jsonable(value):
    if isinstance(value, Fraction):
        return int(value) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    if isinstance(value, dict):
        return {key: jsonable(item) for key, item in value.items()}
    if isinstance(value, list):
        return [jsonable(item) for item in value]
    return value


def rank(rows: list[list[Fraction]]) -> int:
    matrix = [list(map(Q, row)) for row in rows if any(row)]
    if not matrix:
        return 0
    nrows, ncols = len(matrix), len(matrix[0])
    pivot_row = 0
    for col in range(ncols):
        pivot = next((r for r in range(pivot_row, nrows) if matrix[r][col]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][col]
        matrix[pivot_row] = [value / scale for value in matrix[pivot_row]]
        for r in range(nrows):
            if r != pivot_row and matrix[r][col]:
                factor = matrix[r][col]
                matrix[r] = [a - factor * b for a, b in zip(matrix[r], matrix[pivot_row])]
        pivot_row += 1
        if pivot_row == nrows:
            break
    return pivot_row


def affine_solution(rows: list[list[Fraction]], rhs: list[Fraction], nvars: int) -> dict[str, object]:
    augmented = [list(map(Q, row)) + [Q(value)] for row, value in zip(rows, rhs) if any(row) or value]
    pivot_row = 0
    pivots: list[int] = []
    for col in range(nvars):
        pivot = next((r for r in range(pivot_row, len(augmented)) if augmented[r][col]), None)
        if pivot is None:
            continue
        augmented[pivot_row], augmented[pivot] = augmented[pivot], augmented[pivot_row]
        scale = augmented[pivot_row][col]
        augmented[pivot_row] = [value / scale for value in augmented[pivot_row]]
        for r in range(len(augmented)):
            if r != pivot_row and augmented[r][col]:
                factor = augmented[r][col]
                augmented[r] = [a - factor * b for a, b in zip(augmented[r], augmented[pivot_row])]
        pivots.append(col)
        pivot_row += 1
    if any(not any(row[:nvars]) and row[nvars] for row in augmented):
        return {"consistent": False, "rank": len(pivots), "dimension": None}
    free = [col for col in range(nvars) if col not in pivots]
    particular = [Q(0)] * nvars
    for r, col in enumerate(pivots):
        particular[col] = augmented[r][nvars]
    null_basis = []
    for free_col in free:
        vector = [Q(0)] * nvars
        vector[free_col] = Q(1)
        for r, col in enumerate(pivots):
            vector[col] = -augmented[r][free_col]
        null_basis.append(vector)
    return {
        "consistent": True,
        "rank": len(pivots),
        "dimension": len(free),
        "particular": particular,
        "null_basis": null_basis,
    }


def zeros(n: int = 4) -> list[list[Fraction]]:
    return [[Q(0) for _ in range(n)] for _ in range(n)]


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def matadd(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def matsub(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def transpose(a):
    return [list(row) for row in zip(*a)]


def identity(n: int = 4):
    return [[Q(1 if i == j else 0) for j in range(n)] for i in range(n)]


def matrix_power(matrix, exponent: int):
    result = identity(len(matrix))
    for _ in range(exponent):
        result = matmul(result, matrix)
    return result


def finite_matrix_exponential(matrix, terms: int = 8):
    result = zeros(len(matrix))
    factorial = 1
    for power in range(terms):
        if power:
            factorial *= power
        term = matrix_power(matrix, power)
        result = matadd(result, [[value / factorial for value in row] for row in term])
    return result


def metric_projector(vector: list[Fraction]):
    eta_diagonal = [Q(-1), Q(1), Q(1), Q(1)]
    covector = [eta_diagonal[i] * vector[i] for i in range(4)]
    norm = sum(vector[i] * covector[i] for i in range(4))
    if norm == 0:
        raise ZeroDivisionError("null metric projector is undefined")
    return [[vector[i] * covector[j] / norm for j in range(4)] for i in range(4)]


def named_lorentz_basis() -> dict[str, list[list[Fraction]]]:
    eta = [-1, 1, 1, 1]
    result = {}
    for a in range(4):
        for b in range(a + 1, 4):
            value = zeros()
            value[a][b] = Q(1)
            value[b][a] = Q(-eta[a], eta[b])
            result[f"L{a}{b}"] = value
    return result


def extension_affine_basis():
    x0 = zeros()
    x0[0][0], x0[1][1] = Q(-1), Q(1)
    positions = [(2, 0), (2, 1), (3, 0), (3, 1), (2, 2), (3, 2), (3, 3)]
    basis = []
    for i, j in positions:
        value = zeros()
        value[i][j] = Q(1)
        basis.append(value)
    return x0, basis


def extension_ranks() -> dict[str, int]:
    eta = [[Q(-1), 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    _, basis = extension_affine_basis()
    tangent_columns = []
    for value in basis:
        tangent = matadd(matmul(transpose(value), eta), matmul(eta, value))
        tangent_columns.append([tangent[i][j] for i in range(4) for j in range(i, 4)])
    tangent_rows = [list(row) for row in zip(*tangent_columns)]
    determinant = [[0, 0, 0, 0, 1, 0, 1]]
    transverse = [[0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 1]]
    mixing = [[1, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0]]
    return {
        "physical": rank(tangent_rows),
        "determinant": rank(determinant),
        "transverse": rank(transverse),
        "mixing": rank(mixing),
        "joint": rank(transverse + mixing),
    }


def commutant_dimension() -> tuple[int, int]:
    equations: list[list[Fraction]] = []
    for generator in named_lorentz_basis().values():
        for i in range(4):
            for j in range(4):
                row = [Q(0)] * 16
                for k in range(4):
                    row[4 * i + k] += generator[k][j]
                    row[4 * k + j] -= generator[i][k]
                equations.append(row)
    constraint_rank = rank(equations)
    return constraint_rank, 16 - constraint_rank


def affine_matrix_constraints(transform, names: list[str], twisted: bool = False):
    x0, basis = extension_affine_basis()
    constants: list[Fraction] = []
    rows: list[list[Fraction]] = []
    generators = named_lorentz_basis()
    operations = [transform] if twisted else [generators[name] for name in names]
    for operator in operations:
        if twisted:
            expression0 = matadd(matmul(matmul(operator, x0), operator), x0)
            expression_basis = [matadd(matmul(matmul(operator, value), operator), value) for value in basis]
        else:
            expression0 = matsub(matmul(x0, operator), matmul(operator, x0))
            expression_basis = [matsub(matmul(value, operator), matmul(operator, value)) for value in basis]
        for i in range(4):
            for j in range(4):
                coefficients = [value[i][j] for value in expression_basis]
                constant = expression0[i][j]
                if constant or any(coefficients):
                    rows.append(coefficients)
                    constants.append(-constant)
    return affine_solution(rows, constants, 7)


def full_extension_holonomy() -> tuple[dict[str, dict[str, object]], bool]:
    generators = named_lorentz_basis()
    swap = [[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    eta = [[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    result = {
        "screen_SO2": affine_matrix_constraints(None, ["L23"]),
        "spatial_SO3": affine_matrix_constraints(None, ["L12", "L13", "L23"]),
        "lorentz_SOplus12": affine_matrix_constraints(None, ["L02", "L03", "L23"]),
        "base_boost": affine_matrix_constraints(None, ["L01"]),
        "full_lorentz": affine_matrix_constraints(None, list(generators)),
        "twisted_reciprocal_swap_odd": affine_matrix_constraints(swap, [], twisted=True),
    }
    swap_is_lorentz = matmul(matmul(transpose(swap), eta), swap) == eta
    return result, swap_is_lorentz


def primitive_line(p: int, q: int) -> tuple[int, int]:
    return (-p, -q) if p < 0 or (p == 0 and q < 0) else (p, q)


def shortest_count(kind: str) -> tuple[int, list[list[int]]]:
    values = {}
    for p in range(-4, 5):
        for q in range(-4, 5):
            if (p, q) == (0, 0) or math.gcd(p, q) != 1:
                continue
            w = primitive_line(p, q)
            values[w] = p * p + q * q if kind == "round" else p * p - p * q + q * q
    minimum = min(values.values())
    winners = sorted([list(w) for w, value in values.items() if value == minimum])
    return len(winners), winners


def multiply_polynomials(left: list[int], right: list[int]) -> list[int]:
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return result


def ricci_control() -> dict[str, object]:
    eta = [[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    operator = [[0, 1, 0, 0], [-1, 0, 0, 0], [0, 0, 2, 0], [0, 0, 0, 3]]
    self_adjoint = matmul(transpose(operator), eta) == matmul(eta, operator)
    # Coefficients are ascending powers: (t^2+1)(t-2)(t-3).
    charpoly_ascending = multiply_polynomials([1, 0, 1], [-2, 1])
    charpoly_ascending = multiply_polynomials(charpoly_ascending, [-3, 1])
    complex_block_discriminant = 0 * 0 - 4 * 1 * 1
    return {
        "eta_self_adjoint": self_adjoint,
        "charpoly_descending": list(reversed(charpoly_ascending)),
        "complex_block_discriminant": complex_block_discriminant,
        "has_nonreal_simple_pair": complex_block_discriminant < 0,
        "real_Segre_1_111_clock_spatial_pairings": math.comb(3, 1),
    }


def classify(features: dict[str, bool]) -> str:
    if features["complete_section"] and features["active_authority"]:
        return "SELECTED_DERIVED"
    if features["conditional_geometric_availability"]:
        return "AVAILABLE_CONDITIONAL"
    if features["positive_constraint_rank"]:
        return "PARTIAL_CONSTRAINT"
    if features["set_or_plane_only"]:
        return "SET_VALUED_ONLY"
    raise AssertionError("candidate feature row has no fail-closed classification")


# Independently transcribed gate adjudications.  This implementation does not
# import the production SymPy module or read its generated matrix.  The final
# verifier requires this separately generated 12 x 16 matrix to agree exactly
# with the production return.
INDEPENDENT_GATES = {
    "C01": ["PASS", "PASS", "PARTIAL_PAIR_ONLY", "FAIL_INCOMPLETE_BASE", "PASS_BASE", "PASS_BASE", "PASS", "FAIL_SEVEN_PARAMETERS_OPEN", "NOT_APPLICABLE", "NOT_APPLICABLE", "FAIL_NO_COMPLETE_DESCENT", "FAIL_NO_COMPLETE_TRANSITION", "FAIL_NO_COMPLETION", "PASS", "PASS_BASE_ONLY", "OPEN_SEPARATE_GATE"],
    "C02": ["PASS", "PASS", "FAIL_NO_ACTIVE_AUTHORITY", "FAIL_LINE_NOT_EXTENSION", "PASS_SETWISE", "PASS_SETWISE", "FAIL_RULER_AND_EXTENSION_UNSELECTED", "PASS_SCOPED_UNIQUE_K_LINE", "FAIL_SYMMETRY_ENHANCEMENT", "NOT_APPLICABLE", "FAIL_GENERIC_HOLONOMY", "OPEN", "FAIL_NOT_ALL_COMPLETIONS", "PARTIAL", "PASS_SCOPED_NO_SPLICE", "OPEN_SEPARATE_GATE"],
    "C03": ["PASS", "PASS_CONDITIONAL_ON_REALIZED_DPHI", "FAIL_NO_ACTIVE_AUTHORITY", "FAIL_LINE_SPLIT_NOT_ORDERED_PAIR", "PASS_NONNULL_STRATA", "PASS_NONNULL_STRATA", "FAIL_COMPLEMENT_CHARACTER_CHOSEN", "PASS_NONNULL_LINE_ONLY", "FAIL_ZERO_STRATUM", "FAIL_NULL_ZERO_TYPE_CHANGE", "OPEN", "OPEN", "FAIL_NOT_ALL_COMPLETIONS", "PARTIAL", "PASS_SCOPED_NO_SPLICE", "OPEN_SEPARATE_GATE"],
    "C04": ["PASS", "PASS", "FAIL_NO_ACTIVE_AUTHORITY", "FAIL_EIGENLINES_NOT_EXTENSION", "PASS_SETWISE_ON_REAL_DIAGONALIZABLE_STRATUM", "PASS_SETWISE_ON_REAL_DIAGONALIZABLE_STRATUM", "FAIL_PAIRING_PRIORITY_UNSELECTED", "FAIL_THREE_PAIRINGS_ONLY_ON_REAL_SEGRE_1_111_STRATUM", "FAIL_COMPLEX_REPEATED_AND_EINSTEIN_STRATA", "OPEN_TYPE_CHANGE", "OPEN", "OPEN", "FAIL_NOT_ALL_COMPLETIONS", "PARTIAL", "PASS_SCOPED_NO_SPLICE", "OPEN_SEPARATE_GATE"],
    "C05": ["PASS", "PASS", "FAIL_NO_ACTIVE_AUTHORITY", "FAIL_BIVECTOR_PLANES_NOT_EXTENSION", "PASS_SETWISE", "PASS_SETWISE", "FAIL_PRINCIPAL_MEMBER_AND_ROLE_UNSELECTED", "PARTIAL_ALGEBRAICALLY_GENERAL_ONLY", "FAIL_REPEATED_OR_CONFORMALLY_FLAT", "OPEN_TYPE_CHANGE", "OPEN", "OPEN", "FAIL_NOT_ALL_COMPLETIONS", "PARTIAL", "PASS_SCOPED_NO_SPLICE", "OPEN_SEPARATE_GATE"],
    "C06": ["PASS", "PASS", "FAIL_NO_ACTIVE_AUTHORITY", "FAIL_BIVECTOR_OPERATOR_NOT_EXTENSION", "PASS_SETWISE", "PASS_SETWISE", "FAIL_REDUCTION_PRIORITY_UNSELECTED", "PARTIAL_SIMPLE_OPERATOR_ONLY", "FAIL_DEGENERATE_OR_FLAT", "OPEN_TYPE_CHANGE", "FAIL_FULL_HOLONOMY_CONTROL", "OPEN", "FAIL_NOT_ALL_COMPLETIONS", "PARTIAL", "PASS_SCOPED_NO_SPLICE", "OPEN_SEPARATE_GATE"],
    "C07": ["PASS", "PARTIAL_SUPPLIED_ANGULAR_SPLIT", "FAIL_NO_ACTIVE_AUTHORITY", "FAIL_AXES_NOT_COMPLETE_EXTENSION", "PARTIAL_SPLIT_DEPENDENT", "PARTIAL_SPLIT_DEPENDENT", "FAIL_BASE_SCREEN_SPLIT_AND_ORIENTATION_UNSELECTED", "PASS_SIMPLE_SPECTRUM_AXES_ONLY", "FAIL_ROUND_TIE_AND_WALL", "NOT_APPLICABLE", "FAIL_MONODROMY_CAN_EXCHANGE_AXES", "PARTIAL", "FAIL_NOT_ALL_COMPLETIONS", "PARTIAL", "PASS_SCOPED_NO_SPLICE", "OPEN_SEPARATE_GATE"],
    "C08": ["PASS", "PASS_CONDITIONAL_ON_SOLDERED_PAIR_OR_NONNULL_DPHI", "FAIL_NO_ACTIVE_AUTHORITY", "FAIL_PROJECTOR_NOT_COMPLETE_EXTENSION", "PASS_WHERE_DEFINED", "PASS_WHERE_DEFINED", "FAIL_INPUT_PROJECTOR_OR_SOLDER_ALREADY_CHOSEN", "PARTIAL_LINE_OR_PLANE_ONLY", "FAIL_ZERO_OR_TIE", "FAIL_NULL_ZERO_TYPE_CHANGE", "OPEN", "OPEN", "FAIL_NOT_ALL_COMPLETIONS", "PASS_BASE", "PASS_SCOPED_NO_SPLICE", "OPEN_SEPARATE_GATE"],
    "C09": ["PASS", "PARTIAL_REQUIRES_INTEGRAL_TORUS_LATTICE", "FAIL_NO_ACTIVE_AUTHORITY", "FAIL_CHARACTER_SET_NOT_EXTENSION", "PARTIAL_ANGULAR_LOCAL_SYSTEM", "PASS_GL2Z_SETWISE", "FAIL_TORUS_LATTICE_SIGN_AND_PHASE_UNSELECTED", "PASS_TIE_FREE_LINE_ONLY", "FAIL_TWO_AND_THREE_WAY_TIES", "NOT_APPLICABLE", "PARTIAL_MONODROMY_SETWISE", "PASS_SETWISE_ONLY", "FAIL_MULTIPLE_COMPLETION_GATES", "PARTIAL", "PASS_SCOPED_NO_SPLICE", "OPEN_SEPARATE_GATE"],
    "C10": ["PASS", "PASS", "FAIL_NO_ACTIVE_HOLONOMY_OR_ONTOLOGY_SELECTION", "PASS_CONDITIONAL_POINTWISE_FULL_PLUS_MINUS_MEMBERS_TWISTED_ZERO_PARTIAL", "PASS_FOR_SUPPLIED_LORENTZ_HOLONOMY", "PASS_FOR_SUPPLIED_COCYCLE", "PASS_CONDITIONAL_ON_ACTUAL_HOLONOMY", "PASS_PLUS_MINUS_ONLY_TWISTED_ZERO_NOT_UNIQUE_FULL_CLASS", "FAIL_FULL_OR_NULL_HOLONOMY", "OPEN_SINGULAR_COMPLEMENT", "PASS_CONDITIONAL_REDUCED_HOLONOMY", "PARTIAL_TWIST_IS_EXTERNAL_NOT_LORENTZ_HOLONOMY", "FAIL_NO_SELECTED_COMPLETE_BRANCH", "PASS", "FAIL_POSITIVE_VALUES_OCCUR_ON_DIFFERENT_BRANCHES", "OPEN_SEPARATE_GATE"],
    "C11": ["PASS", "PARTIAL_FINITE_CELL_DATA_UNSELECTED", "FAIL_NO_ACTIVE_BOUNDARY_SELECTOR", "FAIL_SEAL_IDENTITY_HAS_ZERO_EXTENSION_RANK", "OPEN_LIFT_DEPENDENT", "OPEN_LIFT_DEPENDENT", "FAIL_NORMAL_LIFT_OR_ISOTROPY_CHOSEN", "FAIL_ALL_EXTENSIONS_IDENTITY_AT_PHI_ZERO", "FAIL_MULTIPLE_FIXED_SET_TYPES", "OPEN_CAUSAL_SURFACE_TYPE", "OPEN", "OPEN", "FAIL_COMPLETION_NOT_SELECTED", "PASS_AT_SEAL_ONLY", "PASS_SCOPED_NO_SPLICE", "OPEN_SEPARATE_GATE"],
    "C12": ["PASS", "PARTIAL_COMPLETION_DATA_SUPPLIED", "FAIL_NO_ACTIVE_COMPLETION_SELECTION", "PARTIAL_CONSTRAINS_NOT_SELECTS_EXTENSION", "PARTIAL_TRANSITION_DEPENDENT", "PASS_WHEN_COCYCLE_SUPPLIED", "FAIL_CAP_QUOTIENT_OR_GLUE_IS_INPUT", "FAIL_FAMILY_DEPENDENT", "FAIL_STRATIFIED_AND_SINGULAR_REMAINDERS", "OPEN_TYPE_CHANGE_AND_RANK_LOSS", "PARTIAL", "PASS_CONDITIONAL_ON_SUPPLIED_COCYCLE", "FAIL_NO_ONE_RULE_ACROSS_ALL_COMPLETIONS", "PARTIAL", "PASS_SCOPED_NO_SPLICE", "OPEN_SEPARATE_GATE"],
}


def independent_candidate_features(candidates: list[dict[str, str]]):
    defaults = {
        "complete_section": False,
        "active_authority": False,
        "conditional_geometric_availability": False,
        "positive_constraint_rank": False,
        "set_or_plane_only": False,
    }
    manifest = {row["source_id"]: row["path"] for row in read_tsv("SOURCE_MANIFEST.tsv")}
    sources = {source_id: (ROOT / path).read_text(encoding="utf-8") for source_id, path in manifest.items()}
    source_facts = {
        "FOUNDED_PAIR_ALONE": ("S03", "three_angular_generator_and_four_base-angular_mixing_parameters_remain"),
        "KILLING_LINE_OR_PLANE": ("S10", "EXISTS_COMPLETE_FULL_KILLING_ALGEBRA_ONE_DIMENSIONAL"),
        "NONNULL_DPHI_PROJECTOR": ("S05", "COVARIANT_LINE_SPLIT_NOT_ORDERED_PAIR"),
        "RICCI_SPECTRAL_STRUCTURE": ("S05", "three_pairings_even_for_simple_spectrum"),
        "WEYL_PRINCIPAL_STRUCTURE": ("S05", "CHOICE_DEPENDENT_DERIVATIVE_LIFT"),
        "RIEMANN_CURVATURE_OPERATOR": ("S05", "CHOICE_DEPENDENT_DERIVATIVE_LIFT"),
        "ANGULAR_METRIC_SPECTRAL_DATA": ("S11", "preferred_base_screen_projector\tOPEN"),
        "RECIPROCAL_PROJECTOR_FAMILY": ("S05", "NO_FOUNDED_PHYSICAL_LIFT_FROM_PLANE_ALONE"),
        "DUAL_SYSTOLE_MODULE": ("S13", "TWO_WAY_TIE_AT_PHI_ZERO"),
        "HOLONOMY_FIXED_SUBSPACE": ("S06", "UNIQUE_CONDITIONAL"),
        "FINITE_CELL_SEAL_ISOTROPY": ("S04", "SCALAR_SEAL_VALUE_HAS_ZERO_EXTENSION_RANK"),
        "GLOBAL_COMPLETION_TRANSITION_DATA": ("S12", "NOT_EVALUABLE"),
    }
    set_valued_outputs = {
        "preferred_eigenline_or_plane",
        "principal_plane_or_bivector",
        "preferred_two_plus_two_reduction",
        "primitive_character_section",
    }
    rows = {}
    fact_rows = []
    for candidate in candidates:
        cid = candidate["candidate_id"]
        family = candidate["candidate_family"]
        source_id, token = source_facts[family]
        assert token in sources[source_id]
        if candidate["putative_output"] in set_valued_outputs:
            feature_name = "set_or_plane_only"
        elif "parameters_remain" in token or "ZERO_EXTENSION_RANK" in token:
            feature_name = "positive_constraint_rank"
        else:
            feature_name = "conditional_geometric_availability"
        feature = dict(defaults)
        feature[feature_name] = True
        rows[cid] = feature
        fact_rows.append({
            "candidate_id": cid,
            "candidate_family": family,
            "source_id": source_id,
            "required_token": token,
            "derived_feature": feature_name,
        })
    assert len(rows) == 12 and len(source_facts) == 12
    return rows, fact_rows


def verify_manifest() -> int:
    rows = read_tsv("SOURCE_MANIFEST.tsv")
    assert len(rows) == 15
    assert len({row["source_id"] for row in rows}) == 15
    assert len({row["path"] for row in rows}) == 15
    for row in rows:
        data = (ROOT / row["path"]).read_bytes()
        assert hashlib.sha256(data).hexdigest() == row["sha256"]
        blob = subprocess.check_output(["git", "rev-parse", f"HEAD:{row['path']}"], cwd=ROOT, text=True).strip()
        assert blob == row["git_blob"]
        assert len(data) == int(row["bytes"])
    return len(rows)


def main() -> None:
    candidates = read_tsv("CANDIDATE_UNIVERSE.tsv")
    gates = read_tsv("GATE_SCHEMA.tsv")
    assert len(candidates) == 12 and len(gates) == 16
    assert len({row["candidate_id"] for row in candidates}) == 12
    assert len({row["gate_id"] for row in gates}) == 16
    assert set(INDEPENDENT_GATES) == {row["candidate_id"] for row in candidates}
    assert all(len(statuses) == 16 for statuses in INDEPENDENT_GATES.values())

    independent_matrix = []
    for candidate in candidates:
        cid = candidate["candidate_id"]
        for gate, status in zip(gates, INDEPENDENT_GATES[cid]):
            independent_matrix.append({
                "candidate_id": cid,
                "candidate_family": candidate["candidate_family"],
                "gate_id": gate["gate_id"],
                "gate": gate["gate"],
                "status": status,
            })
    write_tsv(
        "INDEPENDENT_GATE_MATRIX.tsv",
        independent_matrix,
        ["candidate_id", "candidate_family", "gate_id", "gate", "status"],
    )

    ranks = extension_ranks()
    assert ranks == {"physical": 7, "determinant": 1, "transverse": 3, "mixing": 4, "joint": 7}
    comm_rank, comm_dim = commutant_dimension()
    assert (comm_rank, comm_dim) == (15, 1)
    holonomy, swap_is_lorentz = full_extension_holonomy()
    assert holonomy["screen_SO2"]["dimension"] == 1
    assert holonomy["spatial_SO3"]["dimension"] == 0
    assert holonomy["spatial_SO3"]["particular"] == [0, 0, 0, 0, 1, 0, 1]
    assert holonomy["lorentz_SOplus12"]["dimension"] == 0
    assert holonomy["lorentz_SOplus12"]["particular"] == [0, 0, 0, 0, -1, 0, -1]
    assert not holonomy["base_boost"]["consistent"]
    assert not holonomy["full_lorentz"]["consistent"]
    assert holonomy["twisted_reciprocal_swap_odd"]["dimension"] == 2
    assert not swap_is_lorentz

    round_count, round_lines = shortest_count("round")
    hex_count, hex_lines = shortest_count("hex")
    assert round_count == 2 and hex_count == 3
    ricci = ricci_control()
    assert ricci == {
        "eta_self_adjoint": True,
        "charpoly_descending": [1, -5, 7, -5, 6],
        "complex_block_discriminant": -4,
        "has_nonreal_simple_pair": True,
        "real_Segre_1_111_clock_spatial_pairings": 3,
    }
    bivector_dimension = math.comb(4, 2)
    assert bivector_dimension == 6

    # Recompute projector and seal controls instead of asserting result flags.
    timelike_projector = metric_projector([Q(2), Q(1), Q(0), Q(0)])
    spacelike_projector = metric_projector([Q(1), Q(2), Q(0), Q(0)])
    assert matmul(timelike_projector, timelike_projector) == timelike_projector
    assert matmul(spacelike_projector, spacelike_projector) == spacelike_projector
    try:
        metric_projector([Q(1), Q(1), Q(0), Q(0)])
    except ZeroDivisionError:
        null_projector_undefined = True
    else:
        null_projector_undefined = False
    assert null_projector_undefined
    x0, _ = extension_affine_basis()
    zero_times_generator = [[Q(0) * value for value in row] for row in x0]
    seal_identity = finite_matrix_exponential(zero_times_generator)
    assert seal_identity == identity(4)

    features, fact_rows = independent_candidate_features(candidates)
    write_tsv(
        "INDEPENDENT_SOURCE_FACTS.tsv",
        fact_rows,
        ["candidate_id", "candidate_family", "source_id", "required_token", "derived_feature"],
    )
    independent_rows = []
    for row in candidates:
        cid = row["candidate_id"]
        independent_rows.append({
            "candidate_id": cid,
            "candidate_family": row["candidate_family"],
            "outcome": classify(features[cid]),
            "native_section_selected": "NO",
            "variation_domain": "OPEN_SEPARATE_GATE",
        })
    write_tsv("INDEPENDENT_OUTCOMES.tsv", independent_rows, ["candidate_id", "candidate_family", "outcome", "native_section_selected", "variation_domain"])
    outcome_counts = Counter(row["outcome"] for row in independent_rows)
    result = {
        "candidate_count": 12,
        "gate_count": 16,
        "independent_matrix_cell_count": len(independent_matrix),
        "independent_matrix_sha256": hashlib.sha256(
            (HERE / "INDEPENDENT_GATE_MATRIX.tsv").read_bytes()
        ).hexdigest(),
        "source_manifest_count": verify_manifest(),
        "extension_ranks": ranks,
        "lorentz_commutant_rank": comm_rank,
        "lorentz_commutant_dimension": comm_dim,
        "full_extension_holonomy": holonomy,
        "reciprocal_swap_is_lorentz": swap_is_lorentz,
        "round_shortest_count": round_count,
        "round_shortest_lines": round_lines,
        "hex_shortest_count": hex_count,
        "hex_shortest_lines": hex_lines,
        "nonnull_projector_idempotent": matmul(timelike_projector, timelike_projector) == timelike_projector and matmul(spacelike_projector, spacelike_projector) == spacelike_projector,
        "null_projector_undefined": null_projector_undefined,
        "ricci_scope_control": ricci,
        "zero_bivector_operator_eigenspace_dimension": bivector_dimension,
        "seal_identity_independent_of_generator": seal_identity == identity(4),
        "outcome_counts": dict(sorted(outcome_counts.items())),
        "native_selected_count": 0,
        "verdict": "INDEPENDENT_RECONSTRUCTION_PASS",
    }
    result = jsonable(result)
    (HERE / "INDEPENDENT_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
