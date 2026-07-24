#!/usr/bin/env python3
"""Derive the continuous dual-systole chamber and global transport atlas."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Iterable

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, fields: list[str], rows: Iterable[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fields, delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row[field] for field in fields})


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def verify_inputs() -> list[dict[str, str]]:
    expected_counts = {
        "ANALYTIC_OBJECT_REGISTRY.tsv": 18,
        "COMPLETION_TEST_REGISTRY.tsv": 12,
        "FALSIFICATION_CONTRACT.tsv": 12,
        "PREMISE_LEDGER.tsv": 23,
        "SOURCE_MANIFEST.tsv": 16,
    }
    for name, expected in expected_counts.items():
        found = len(read_tsv(OUT / name))
        if found != expected:
            raise AssertionError(f"{name}: expected {expected}, found {found}")
    rows = []
    for source in read_tsv(OUT / "SOURCE_MANIFEST.tsv"):
        actual = digest(ROOT / source["path"])
        if actual != source["sha256"]:
            raise AssertionError(f"source mismatch: {source['path']}")
        rows.append(
            {
                "source_id": source["source_id"],
                "path": source["path"],
                "expected_sha256": source["sha256"],
                "actual_sha256": actual,
                "status": "PASS",
            }
        )
    return rows


def exact_algebra() -> dict[str, object]:
    phi, shear = sp.symbols("phi shear", real=True)
    x, y = sp.symbols("x y", real=True, positive=False)
    # y is constrained positive by the map, but leaving the symbol generic
    # makes the inverse-substitution check explicit.
    p, q, r, u = sp.symbols("p q r u", integer=True)
    d = sp.Matrix([[sp.exp(-phi), shear], [0, sp.exp(phi)]])
    h = sp.simplify(d.T * d)
    qmetric = sp.simplify(h.inv())
    det_h = sp.simplify(h.det())

    x_map = shear * sp.exp(phi)
    y_map = sp.exp(2 * phi)
    phi_inverse = sp.log(y) / 2
    shear_inverse = x / sp.sqrt(y)
    x_roundtrip = sp.simplify(
        x_map.subs({phi: phi_inverse, shear: shear_inverse}) - x
    )
    y_roundtrip = sp.simplify(y_map.subs(phi, phi_inverse) - y)
    h_upper = sp.Matrix([[1 / y, x / y], [x / y, (x**2 + y**2) / y]])
    h_upper_residual = sp.simplify(
        h.subs({phi: phi_inverse, shear: shear_inverse}) - h_upper
    )

    w = sp.Matrix([p, q])
    v = sp.Matrix([r, u])
    length_phi = sp.expand((w.T * qmetric * w)[0])
    length_upper = sp.expand(((p * x - q) ** 2 + (p * y) ** 2) / y)
    length_residual = sp.simplify(
        length_phi
        - length_upper.subs({x: x_map, y: y_map})
    )
    other_upper = sp.expand(((r * x - u) ** 2 + (r * y) ** 2) / y)
    equality_upper = sp.factor(sp.expand(y * (length_upper - other_upper)))
    equality_phi = sp.factor(
        sp.expand(length_phi - (v.T * qmetric * v)[0])
    )

    ell, inner, ratio = sp.symbols("L B ratio", real=True)
    gram = sp.Matrix([[ell, inner], [inner, ell]])
    gram_det = sp.expand(gram.det())
    reduced_det_residual = sp.simplify(
        gram_det.subs({inner: ratio * ell, ell: 1 / sp.sqrt(1 - ratio**2)})
        - 1
    )
    plus_length = sp.expand((sp.Matrix([1, 1]).T * gram * sp.Matrix([1, 1]))[0])
    minus_length = sp.expand(
        (sp.Matrix([1, -1]).T * gram * sp.Matrix([1, -1]))[0]
    )
    endpoint_plus_residual = sp.simplify(
        plus_length.subs(inner, -ell / 2) - ell
    )
    endpoint_minus_residual = sp.simplify(
        minus_length.subs(inner, ell / 2) - ell
    )

    standard_equality = sp.factor(
        equality_upper.subs({p: 1, q: 0, r: 0, u: 1})
    )
    standard_phi_equality = sp.factor(
        equality_phi.subs({p: 1, q: 0, r: 0, u: 1})
    )
    vertex_phi = sp.log(sp.sqrt(3) / 2) / 2
    vertex_shear = 1 / sp.sqrt(2 * sp.sqrt(3))
    vertex_x_residual = sp.simplify(
        vertex_shear * sp.exp(vertex_phi) - sp.Rational(1, 2)
    )
    vertex_y_residual = sp.simplify(
        sp.exp(2 * vertex_phi) - sp.sqrt(3) / 2
    )

    a, b, c, e = sp.symbols("a b c e", real=True)
    m = sp.Matrix([[a, b], [c, e]])
    q11, q12, q22 = sp.symbols("q11 q12 q22", real=True)
    qgeneric = sp.Matrix([[q11, q12], [q12, q22]])
    wg = sp.Matrix(sp.symbols("w0 w1", real=True))
    sg = sp.Matrix(sp.symbols("S0 S1", real=True))
    transformed_q = m * qgeneric * m.T
    transformed_w = m.inv().T * wg
    transformed_s = m * sg
    covariance_residual = sp.simplify(
        (transformed_w.T * transformed_q * transformed_w)[0]
        - (wg.T * qgeneric * wg)[0]
    )
    connection_residual = sp.simplify(
        (transformed_w.T * transformed_s)[0] - (wg.T * sg)[0]
    )

    residuals = {
        "det_H_minus_one": sp.sstr(det_h - 1),
        "x_roundtrip": sp.sstr(x_roundtrip),
        "y_roundtrip": sp.sstr(y_roundtrip),
        "H_upper_half_plane_residual": [
            [sp.sstr(item) for item in row] for row in h_upper_residual.tolist()
        ],
        "character_norm_residual": sp.sstr(length_residual),
        "reduced_wall_det_residual": sp.sstr(reduced_det_residual),
        "triple_plus_residual": sp.sstr(endpoint_plus_residual),
        "triple_minus_residual": sp.sstr(endpoint_minus_residual),
        "vertex_x_residual": sp.sstr(vertex_x_residual),
        "vertex_y_residual": sp.sstr(vertex_y_residual),
        "GL2_norm_covariance_residual": sp.sstr(covariance_residual),
        "projected_connection_covariance_residual": sp.sstr(connection_residual),
    }
    flattened = [
        residuals["det_H_minus_one"],
        residuals["x_roundtrip"],
        residuals["y_roundtrip"],
        residuals["character_norm_residual"],
        residuals["reduced_wall_det_residual"],
        residuals["triple_plus_residual"],
        residuals["triple_minus_residual"],
        residuals["vertex_x_residual"],
        residuals["vertex_y_residual"],
        residuals["GL2_norm_covariance_residual"],
        residuals["projected_connection_covariance_residual"],
    ]
    flattened.extend(item for row in residuals["H_upper_half_plane_residual"] for item in row)
    if any(item != "0" for item in flattened):
        raise AssertionError(f"exact residual: {residuals}")

    return {
        "D": [[sp.sstr(item) for item in row] for row in d.tolist()],
        "H": [[sp.sstr(item) for item in row] for row in h.tolist()],
        "Q": [[sp.sstr(item) for item in row] for row in qmetric.tolist()],
        "tau_map": "x=shear*exp(phi);y=exp(2*phi)",
        "tau_inverse": "phi=log(y)/2;shear=x/sqrt(y)",
        "character_norm_phi": sp.sstr(length_phi),
        "character_norm_upper": sp.sstr(length_upper),
        "general_equality_upper": sp.sstr(equality_upper),
        "general_equality_phi": sp.sstr(equality_phi),
        "standard_wall_upper": sp.sstr(standard_equality),
        "standard_wall_phi": sp.sstr(standard_phi_equality),
        "standard_wall_segment": "x^2+y^2=1;abs(x)<=1/2;y>0",
        "standard_wall_vertices": {
            "upper": "x=plus_or_minus_1/2;y=sqrt(3)/2",
            "phi": sp.sstr(vertex_phi),
            "shear_magnitude": sp.sstr(vertex_shear),
        },
        "reduced_gram_determinant": sp.sstr(gram_det),
        "reduced_wall_parameter": "B=ratio*L;abs(ratio)<=1/2;L=1/sqrt(1-ratio^2)",
        "residuals": residuals,
    }


def canonical(direction: tuple[int, int]) -> tuple[int, int]:
    if direction[0] < 0 or (direction[0] == 0 and direction[1] < 0):
        return (-direction[0], -direction[1])
    return direction


def primitive_directions(bound: int) -> list[tuple[int, int]]:
    return [
        (first, second)
        for first in range(-bound, bound + 1)
        for second in range(-bound, bound + 1)
        if (first or second)
        and math.gcd(abs(first), abs(second)) == 1
        and canonical((first, second)) == (first, second)
    ]


def quadratic(
    matrix: tuple[tuple[float, float], tuple[float, float]],
    vector: tuple[int, int],
) -> float:
    return (
        matrix[0][0] * vector[0] ** 2
        + 2 * matrix[0][1] * vector[0] * vector[1]
        + matrix[1][1] * vector[1] ** 2
    )


def shortest(
    matrix: tuple[tuple[float, float], tuple[float, float]], bound: int = 20
) -> tuple[float, list[tuple[int, int]], float]:
    values = [(quadratic(matrix, vector), vector) for vector in primitive_directions(bound)]
    best = min(value for value, _ in values)
    directions = sorted(
        vector for value, vector in values if abs(value - best) <= 1e-11
    )
    trace = matrix[0][0] + matrix[1][1]
    discriminant = math.sqrt(
        (matrix[0][0] - matrix[1][1]) ** 2 + 4 * matrix[0][1] ** 2
    )
    lambda_min = (trace - discriminant) / 2
    outside = lambda_min * (bound + 1) ** 2
    if outside <= best:
        raise AssertionError("finite shortest-vector control not exterior-certified")
    return best, directions, outside


def wall_controls() -> list[dict[str, object]]:
    controls = [
        ("T01", Fraction(-1, 2)),
        ("T02", Fraction(-1, 4)),
        ("T03", Fraction(0, 1)),
        ("T04", Fraction(1, 4)),
        ("T05", Fraction(1, 2)),
    ]
    rows = []
    for control_id, ratio in controls:
        ratio_float = float(ratio)
        length = 1 / math.sqrt(1 - ratio_float**2)
        matrix = (
            (length, ratio_float * length),
            (ratio_float * length, length),
        )
        best, directions, outside = shortest(matrix)
        expected = [(0, 1), (1, 0)]
        if ratio == Fraction(-1, 2):
            expected.append((1, 1))
        if ratio == Fraction(1, 2):
            expected.append((1, -1))
        expected = sorted(expected)
        if directions != expected:
            raise AssertionError(f"standard wall control {control_id}: {directions}")
        rows.append(
            {
                "control_id": control_id,
                "ratio_B_over_L": str(ratio),
                "L": f"{length:.17g}",
                "shortest_lines_mod_sign": ";".join(
                    f"({first},{second})" for first, second in directions
                ),
                "multiplicity": len(directions),
                "shortest_norm_squared": f"{best:.17g}",
                "outside_lower_bound": f"{outside:.17g}",
                "status": "PASS",
            }
        )
    return rows


def inverse_integer(
    matrix: tuple[tuple[int, int], tuple[int, int]]
) -> tuple[tuple[int, int], tuple[int, int]]:
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    if abs(determinant) != 1:
        raise AssertionError("not GL2Z")
    return (
        (matrix[1][1] // determinant, -matrix[0][1] // determinant),
        (-matrix[1][0] // determinant, matrix[0][0] // determinant),
    )


def matrix_multiply_fraction(
    left: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]],
    right: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]],
) -> tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]:
    return tuple(
        tuple(
            sum(left[row][k] * right[k][column] for k in range(2))
            for column in range(2)
        )
        for row in range(2)
    )


def transpose_fraction(
    matrix: tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]
) -> tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]:
    return ((matrix[0][0], matrix[1][0]), (matrix[0][1], matrix[1][1]))


def gl2_controls() -> list[dict[str, object]]:
    matrices = {
        "M01": ((1, 0), (0, 1)),
        "M02": ((0, 1), (1, 0)),
        "M03": ((1, 1), (0, 1)),
        "M04": ((0, -1), (1, 0)),
        "M05": ((-1, 0), (0, -1)),
        "M06": ((1, 0), (1, 1)),
    }
    qbase = (
        (Fraction(5, 4), Fraction(1, 4)),
        (Fraction(1, 4), Fraction(17, 20)),
    )
    best, base_shortest, _ = shortest(
        tuple(tuple(float(item) for item in row) for row in qbase)
    )
    if len(base_shortest) != 1:
        raise AssertionError("GL2 covariance base is not unique")
    base_w = base_shortest[0]
    rows = []
    for matrix_id, matrix_int in matrices.items():
        matrix = tuple(
            tuple(Fraction(item) for item in row) for row in matrix_int
        )
        transformed_q = matrix_multiply_fraction(
            matrix, matrix_multiply_fraction(qbase, transpose_fraction(matrix))
        )
        inverse = inverse_integer(matrix_int)
        transformed_w_raw = (
            inverse[0][0] * base_w[0] + inverse[1][0] * base_w[1],
            inverse[0][1] * base_w[0] + inverse[1][1] * base_w[1],
        )
        transformed_w = canonical(transformed_w_raw)
        observed_best, observed, _ = shortest(
            tuple(tuple(float(item) for item in row) for row in transformed_q)
        )
        if observed != [transformed_w]:
            raise AssertionError(f"GL2 shortest-set covariance {matrix_id}")
        predicted_norm = quadratic(
            tuple(tuple(float(item) for item in row) for row in transformed_q),
            transformed_w,
        )
        residual = abs(predicted_norm - best)
        if residual >= 1e-11 or abs(observed_best - best) >= 1e-11:
            raise AssertionError(f"GL2 norm covariance {matrix_id}")
        rows.append(
            {
                "matrix_id": matrix_id,
                "matrix": str(matrix_int),
                "base_shortest": f"({base_w[0]},{base_w[1]})",
                "predicted_shortest_mod_sign": f"({transformed_w[0]},{transformed_w[1]})",
                "observed_shortest_mod_sign": f"({observed[0][0]},{observed[0][1]})",
                "norm_residual": f"{residual:.17g}",
                "connection_covariance": "EXACT_SYMBOLIC",
                "status": "PASS",
            }
        )
    return rows


def continuous_wall_rows() -> list[dict[str, object]]:
    return [
        {
            "item_id": "W01",
            "object": "full_metric_chart",
            "exact_statement": "tau=shear*exp(phi)+i*exp(2phi) bijects R2 with upper_half_plane",
            "status": "DERIVED",
            "scope_or_obstruction": "positive_det_one_angular_metrics",
        },
        {
            "item_id": "W02",
            "object": "character_norm",
            "exact_statement": "L_(p,q)=abs(p*tau-q)^2/Im(tau)=w^T H^-1 w",
            "status": "DERIVED",
            "scope_or_obstruction": "primitive_integral_character_required",
        },
        {
            "item_id": "W03",
            "object": "unique_chamber",
            "exact_statement": "C_w={tau:L_w<L_v_for_all_primitive_v_not_plusminus_w}",
            "status": "DERIVED_DEFINITION",
            "scope_or_obstruction": "infinite_inequality_is_locally_finite",
        },
        {
            "item_id": "W04",
            "object": "general_equality_locus",
            "exact_statement": "(p2-r2)(x2+y2)-2x(pq-ru)+(q2-u2)=0",
            "status": "DERIVED",
            "scope_or_obstruction": "only_admissible_segment_is_shortest_wall",
        },
        {
            "item_id": "W05",
            "object": "co_shortest_pair",
            "exact_statement": "independent_shortest_primitive_w_v_imply_abs(det(w,v))=1",
            "status": "DERIVED",
            "scope_or_obstruction": "uses_two_dimensional_Hermite_bound_derived_from_reduced_basis",
        },
        {
            "item_id": "W06",
            "object": "standard_reduced_wall",
            "exact_statement": "Q_basis=[[L,B],[B,L]];L2-B2=1;abs(B)<=L/2",
            "status": "DERIVED",
            "scope_or_obstruction": "all_walls_are_GL2Z_images",
        },
        {
            "item_id": "W07",
            "object": "wall_parameter",
            "exact_statement": "ratio=B/L_in_[-1/2,1/2];L=1/sqrt(1-ratio2)",
            "status": "DERIVED",
            "scope_or_obstruction": "interior_has_two_shortest_lines",
        },
        {
            "item_id": "W08",
            "object": "triple_vertices",
            "exact_statement": "ratio=-1/2_adds_w+v;ratio=+1/2_adds_w-v",
            "status": "DERIVED",
            "scope_or_obstruction": "three_unoriented_lines",
        },
        {
            "item_id": "W09",
            "object": "maximum_tie_multiplicity",
            "exact_statement": "at_most_three_unoriented_primitive_shortest_lines",
            "status": "DERIVED",
            "scope_or_obstruction": "two_dimensions_and_positive_det_one",
        },
        {
            "item_id": "W10",
            "object": "standard_upper_half_plane_wall",
            "exact_statement": "x2+y2=1;abs(x)<=1/2;y>0",
            "status": "DERIVED",
            "scope_or_obstruction": "tie_between_(1,0)_and_(0,1)",
        },
        {
            "item_id": "W11",
            "object": "local_constancy",
            "exact_statement": "unique_W_min_is_locally_constant_in_lattice_trivialization_off_wall_set",
            "status": "DERIVED",
            "scope_or_obstruction": "discrete_line_changes_only_at_tie",
        },
        {
            "item_id": "W12",
            "object": "wall_crossing",
            "exact_statement": "transverse_crossing_exchanges_unique_minimizer_and_metric_leaves_tie_unoriented",
            "status": "DERIVED",
            "scope_or_obstruction": "continuation_requires_extra_rule",
        },
        {
            "item_id": "W13",
            "object": "projected_connection",
            "exact_statement": "b_w=w^T S_is_GL2Z_covariant_for_supplied_w",
            "status": "DERIVED",
            "scope_or_obstruction": "does_not_supply_phase_section",
        },
        {
            "item_id": "W14",
            "object": "physical_selection",
            "exact_statement": "no_registered_UDT_premise_selects_shortest_character_as_physical",
            "status": "OPEN",
            "scope_or_obstruction": "canonicity_is_not_dynamics_or_ontology",
        },
    ]


def diagonal_path_rows() -> list[dict[str, object]]:
    return [
        {
            "segment_id": "D01",
            "domain": "phi<0;shear=0",
            "Q": "diag(exp(2phi),exp(-2phi))",
            "W_min_mod_sign": "(1,0)",
            "multiplicity": 1,
            "connection_candidate": "first_shift_character",
            "global_continuation": "UNIQUE_WITHIN_SEGMENT",
        },
        {
            "segment_id": "D02",
            "domain": "phi=0;shear=0",
            "Q": "identity",
            "W_min_mod_sign": "(1,0);(0,1)",
            "multiplicity": 2,
            "connection_candidate": "SET_VALUED",
            "global_continuation": "TIE_NO_METRIC_TIE_BREAK",
        },
        {
            "segment_id": "D03",
            "domain": "phi>0;shear=0",
            "Q": "diag(exp(2phi),exp(-2phi))",
            "W_min_mod_sign": "(0,1)",
            "multiplicity": 1,
            "connection_candidate": "second_shift_character",
            "global_continuation": "UNIQUE_WITHIN_SEGMENT",
        },
    ]


def global_transport_rows() -> list[dict[str, object]]:
    common_physical = "OPEN_NOT_SELECTED"
    rows = [
        {
            "completion_id": "FC01_BOUNDARY_BOUNDARY",
            "torus_lattice": "LOCAL_IF_SUPPLIED",
            "W_min_set": "DEFINED_ON_TORIC_REGION",
            "unique_line": "ON_WALL_FREE_SUBREGIONS",
            "sign_orientation": "BOUNDARY_FRAMING_OPEN",
            "projected_connection": "LOCAL_IF_LINE_CHOSEN",
            "phase_section": "BOUNDARY_DATA_REQUIRED",
            "physical_selection": common_physical,
            "global_outcome": "INTERVAL_WALL_CROSSING_AND_BOUNDARY_DEPENDENT",
        },
        {
            "completion_id": "FC02_ONE_CAP_BOUNDARY",
            "torus_lattice": "OFF_CAP_ONLY",
            "W_min_set": "DEFINED_OFF_CAP",
            "unique_line": "WALL_FREE_REGION_ONLY",
            "sign_orientation": "OPEN",
            "projected_connection": "OFF_CAP",
            "phase_section": "CAP_REQUIRES_W_OF_VCAP_ZERO_OR_VANISHING_AMPLITUDE;BOUNDARY_OPEN",
            "physical_selection": common_physical,
            "global_outcome": "ONE_CAP_PLUS_BOUNDARY_CONDITIONAL",
        },
        {
            "completion_id": "FC03_TWO_CAP_P0",
            "torus_lattice": "OFF_CAPS",
            "W_min_set": "DEFINED_OFF_CAPS",
            "unique_line": "WALL_FREE_REGION_ONLY",
            "sign_orientation": "RESIDUAL_CIRCLE_ORIENTATION_OPEN",
            "projected_connection": "ON_SURVIVING_CHARACTER_LINE",
            "phase_section": "ONLY_CHARACTER_ANNIHILATING_DEPENDENT_CAP_CYCLE_CAN_EXTEND_ALONE",
            "physical_selection": common_physical,
            "global_outcome": "P0_RESIDUAL_CIRCLE_AND_HOLONOMY_DEPENDENT",
        },
        {
            "completion_id": "FC04_TWO_CAP_P1",
            "torus_lattice": "OFF_CAPS",
            "W_min_set": "DEFINED_OFF_CAPS",
            "unique_line": "WALL_FREE_REGION_ONLY",
            "sign_orientation": "ORIENTATION_OPEN",
            "projected_connection": "OFF_CAPS",
            "phase_section": "NO_NONZERO_CHARACTER_ANNIHILATES_BOTH_UNIMODULAR_CAP_CYCLES",
            "physical_selection": common_physical,
            "global_outcome": "PHASE_ALONE_CANNOT_GLOBALIZE;LATITUDE_AMPLITUDE_OR_PATCHING_REQUIRED",
        },
        {
            "completion_id": "FC05_TWO_CAP_P_GT1",
            "torus_lattice": "OFF_CAPS_WITH_QUOTIENT",
            "W_min_set": "DEFINED_WITH_QUOTIENT_CONGRUENCE",
            "unique_line": "WALL_FREE_AND_QUOTIENT_COMPATIBLE_ONLY",
            "sign_orientation": "QUOTIENT_DEPENDENT",
            "projected_connection": "CHARACTER_CONGRUENCE_DEPENDENT",
            "phase_section": "CAP_AND_LENS_HOLONOMY_DEPENDENT",
            "physical_selection": common_physical,
            "global_outcome": "LENS_BRANCH_DATA_REQUIRED",
        },
        {
            "completion_id": "FC06_NONPRIMITIVE_CAP",
            "torus_lattice": "ORBIFOLD_OFF_CAP",
            "W_min_set": "DEFINED_OFF_CAP",
            "unique_line": "ORBIFOLD_REPRESENTATION_DEPENDENT",
            "sign_orientation": "STABILIZER_DEPENDENT",
            "projected_connection": "ORBIFOLD_CONNECTION_ONLY",
            "phase_section": "CHARACTER_MUST_BE_TRIVIAL_ON_EXCEPTIONAL_STABILIZER_OR_AMPLITUDE_VANISH",
            "physical_selection": common_physical,
            "global_outcome": "SINGULAR_OR_ORBIFOLD_CONDITIONAL",
        },
        {
            "completion_id": "FC07_PERIODIC_TORUS_BUNDLE",
            "torus_lattice": "GLOBAL_LOCAL_SYSTEM",
            "W_min_set": "GLOBAL_SET_VALUED_INVARIANT_BY_GL2Z_COVARIANCE",
            "unique_line": "GLOBAL_UNORIENTED_SUB_LOCAL_SYSTEM_IF_BRANCH_AVOIDS_TIES",
            "sign_orientation": "MONODROMY_MAY_REVERSE_SIGN",
            "projected_connection": "GLOBAL_LINE_CONNECTION_IF_UNIQUE",
            "phase_section": "CURVATURE_HOLONOMY_AND_SIGN_DEPENDENT",
            "physical_selection": common_physical,
            "global_outcome": "TIE_WALL_MONODROMY_AND_HOLONOMY_DEPENDENT",
        },
        {
            "completion_id": "FC08_MIRROR_DOUBLE",
            "torus_lattice": "LIFT_DEPENDENT",
            "W_min_set": "COVARIANT_SET_IF_LIFT_IS_LATTICE_AUTOMORPHISM",
            "unique_line": "PRESERVED_OR_EXCHANGED_BY_MIRROR",
            "sign_orientation": "PRESERVED_OR_CONJUGATED",
            "projected_connection": "MIRROR_PARITY_DEPENDENT",
            "phase_section": "FIXED_SET_AND_LIFT_DEPENDENT",
            "physical_selection": common_physical,
            "global_outcome": "LIFT_DEPENDENT",
        },
        {
            "completion_id": "FC09_NONORIENTABLE_GLUE",
            "torus_lattice": "TWISTED_LOCAL_SYSTEM",
            "W_min_set": "GLOBAL_SET_POSSIBLE",
            "unique_line": "UNORIENTED_LINE_POSSIBLE_OFF_TIES",
            "sign_orientation": "SIGN_MAY_REVERSE",
            "projected_connection": "REAL_OR_CONJUGATE_LINE_CONNECTION",
            "phase_section": "COMPLEX_PHASE_REQUIRES_ADDITIONAL_REAL_STRUCTURE",
            "physical_selection": common_physical,
            "global_outcome": "ORIENTATION_TWISTED",
        },
        {
            "completion_id": "FC10_STRATIFIED_PROJECTOR",
            "torus_lattice": "STRATUM_DEPENDENT",
            "W_min_set": "DEFINED_ONLY_ON_RANK_TWO_TORIC_STRATA",
            "unique_line": "MAY_TERMINATE_OR_BECOME_SET_VALUED",
            "sign_orientation": "STRATUM_DEPENDENT",
            "projected_connection": "NO_UNIVERSAL_CROSS_STRATUM_OBJECT",
            "phase_section": "STRATUM_MATCHING_OPEN",
            "physical_selection": common_physical,
            "global_outcome": "RANK_CHANGE_OBSTRUCTION",
        },
        {
            "completion_id": "FC11_NONINTEGRABLE_DISTRIBUTION",
            "torus_lattice": "NO_GLOBAL_TORIC_LATTICE",
            "W_min_set": "NO_GLOBAL_DEFINITION",
            "unique_line": "NOT_AVAILABLE_GLOBALLY",
            "sign_orientation": "NOT_APPLICABLE",
            "projected_connection": "NO_GLOBAL_CHARACTER_PROJECTION",
            "phase_section": "NO_GLOBAL_TORIC_PHASE",
            "physical_selection": common_physical,
            "global_outcome": "FROBENIUS_OBSTRUCTION",
        },
        {
            "completion_id": "FC12_RECIPROCAL_TORIC_DIAGONAL",
            "torus_lattice": "SUPPLIED_CONTROL",
            "W_min_set": "EXACT_RECIPROCAL_SWAP",
            "unique_line": "UNIQUE_FOR_PHI_NONZERO;TWO_WAY_TIE_AT_PHI_ZERO",
            "sign_orientation": "OPEN",
            "projected_connection": "SWAPS_CHARACTER_ACROSS_TIE",
            "phase_section": "NO_METRIC_ONLY_CONTINUATION_ACROSS_PHI_ZERO",
            "physical_selection": common_physical,
            "global_outcome": "DIAGONAL_SEAL_CROSSES_SELECTOR_WALL",
        },
    ]
    expected = [
        row["completion_id"] for row in read_tsv(OUT / "COMPLETION_TEST_REGISTRY.tsv")
    ]
    if [row["completion_id"] for row in rows] != expected:
        raise AssertionError("completion coverage mismatch")
    return rows


def main() -> None:
    sources = verify_inputs()
    exact = exact_algebra()
    walls = continuous_wall_rows()
    controls = wall_controls()
    covariance = gl2_controls()
    diagonal = diagonal_path_rows()
    global_rows = global_transport_rows()

    write_tsv(
        OUT / "SOURCE_VERIFICATION.tsv",
        ["source_id", "path", "expected_sha256", "actual_sha256", "status"],
        sources,
    )
    write_tsv(
        OUT / "CONTINUOUS_WALL_ATLAS.tsv",
        ["item_id", "object", "exact_statement", "status", "scope_or_obstruction"],
        walls,
    )
    write_tsv(
        OUT / "STANDARD_WALL_CONTROLS.tsv",
        [
            "control_id",
            "ratio_B_over_L",
            "L",
            "shortest_lines_mod_sign",
            "multiplicity",
            "shortest_norm_squared",
            "outside_lower_bound",
            "status",
        ],
        controls,
    )
    write_tsv(
        OUT / "GL2Z_COVARIANCE.tsv",
        [
            "matrix_id",
            "matrix",
            "base_shortest",
            "predicted_shortest_mod_sign",
            "observed_shortest_mod_sign",
            "norm_residual",
            "connection_covariance",
            "status",
        ],
        covariance,
    )
    write_tsv(
        OUT / "DIAGONAL_PATH_ATLAS.tsv",
        [
            "segment_id",
            "domain",
            "Q",
            "W_min_mod_sign",
            "multiplicity",
            "connection_candidate",
            "global_continuation",
        ],
        diagonal,
    )
    write_tsv(
        OUT / "GLOBAL_TRANSPORT_ATLAS.tsv",
        [
            "completion_id",
            "torus_lattice",
            "W_min_set",
            "unique_line",
            "sign_orientation",
            "projected_connection",
            "phase_section",
            "physical_selection",
            "global_outcome",
        ],
        global_rows,
    )
    write_tsv(
        OUT / "COMPLETION_COVERAGE.tsv",
        [
            "completion_id",
            "registered",
            "classified_once",
            "preferred_or_filtered",
            "physical_selection",
        ],
        [
            {
                "completion_id": row["completion_id"],
                "registered": "YES",
                "classified_once": "YES",
                "preferred_or_filtered": "NO",
                "physical_selection": row["physical_selection"],
            }
            for row in global_rows
        ],
    )

    result = {
        "schema": "udt_dual_systole_global_transport_v1",
        "base_commit": "7feec2b301de9c9626aaac4b513268e7c8ec165a",
        "preregistration_commit": "a99096e34ed5df16873d9a5b7f5a4e4cc8429652",
        "source_count": len(sources),
        "continuous_object_count": len(walls),
        "wall_control_count": len(controls),
        "GL2Z_control_count": len(covariance),
        "diagonal_segment_count": len(diagonal),
        "completion_count": len(global_rows),
        "exact": exact,
        "wall_theorem": {
            "independent_co_shortest_pair": "UNIMODULAR",
            "standard_gram": "[[L,B],[B,L]]",
            "determinant_relation": "L^2-B^2=1",
            "reduction_range": "abs(B)<=L/2",
            "interior_tie_multiplicity": 2,
            "vertex_tie_multiplicity": 3,
            "maximum_unoriented_tie_multiplicity": 3,
        },
        "diagonal_path_ruling": "RECIPROCAL_CHARACTER_SWAP_REQUIRES_TIE_CROSSING",
        "global_ruling": "SET_VALUED_INVARIANT_GLOBAL_WHERE_TORIC__UNIQUE_LINE_ONLY_ON_TIE_FREE_BRANCHES",
        "physical_ruling": "CANONICAL_GEOMETRIC_CHARACTER_NOT_PHYSICALLY_SELECTED",
        "phase_section": "OPEN",
        "density_to_geometry": "OPEN_NOT_SAMPLED",
        "matter_solve_launched": False,
        "gpu_used": False,
    }
    (OUT / "RESULTS.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    print("DUAL_SYSTOLE_GLOBAL_TRANSPORT_AUDIT")
    print(f"sources={len(sources)}")
    print(f"continuous_objects={len(walls)}")
    print(f"wall_controls={len(controls)}")
    print(f"GL2Z_controls={len(covariance)}")
    print(f"completions={len(global_rows)}")
    print("wall_pair=UNIMODULAR")
    print("tie_multiplicity=interior_2 vertex_3 maximum_3")
    print("diagonal=RECIPROCAL_CHARACTER_SWAP_REQUIRES_TIE_CROSSING")
    print("physical_selection=OPEN")
    print("matter_solve=False gpu=False")
    print("PRODUCTION_PASS")


if __name__ == "__main__":
    main()
