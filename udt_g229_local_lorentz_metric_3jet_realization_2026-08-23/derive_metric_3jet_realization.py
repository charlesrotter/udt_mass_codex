#!/usr/bin/env python3
"""Exact G229 local Lorentz-metric 3-jet realization derivation.

The calculation is finite-dimensional and exact.  In a fixed locally
inertial frame at one supplied event it constructs

    metric 2-jets H  -> algebraic curvature R,
    metric 3-jets K  -> compatible first curvature derivative D = nabla R,

then compares the kernels with explicit coordinate-gauge images and the
geodesic-normal-coordinate slices.  No metric history or curvature values
are generated.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import platform
import sys
from pathlib import Path
from typing import Iterable, Sequence

import sympy as sp
from sympy.polys.matrices import DomainMatrix


ROOT = Path(__file__).resolve().parent
ETA_SIGNS = (-1, 1, 1, 1)
BIVECTORS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
PAIR_INDEX = {pair: i for i, pair in enumerate(BIVECTORS)}
DEPENDENT_SLOT = (2, 3)  # Q[03,12]
INDEPENDENT_SLOTS = tuple(
    (i, j)
    for i in range(6)
    for j in range(i, 6)
    if (i, j) != DEPENDENT_SLOT
)
SYMMETRIC_PAIRS = tuple(itertools.combinations_with_replacement(range(4), 2))
SYMMETRIC_TRIPLES = tuple(itertools.combinations_with_replacement(range(4), 3))
SYMMETRIC_QUADS = tuple(itertools.combinations_with_replacement(range(4), 4))

H_COLUMNS = tuple((ab, cd) for ab in SYMMETRIC_PAIRS for cd in SYMMETRIC_PAIRS)
K_COLUMNS = tuple((ab, cde) for ab in SYMMETRIC_PAIRS for cde in SYMMETRIC_TRIPLES)
A_COLUMNS = tuple((a, bcd) for a in range(4) for bcd in SYMMETRIC_TRIPLES)
B_COLUMNS = tuple((a, bcde) for a in range(4) for bcde in SYMMETRIC_QUADS)

H_INDEX = {label: i for i, label in enumerate(H_COLUMNS)}
K_INDEX = {label: i for i, label in enumerate(K_COLUMNS)}
A_INDEX = {label: i for i, label in enumerate(A_COLUMNS)}
B_INDEX = {label: i for i, label in enumerate(B_COLUMNS)}

assert len(INDEPENDENT_SLOTS) == 20
assert len(H_COLUMNS) == 100
assert len(K_COLUMNS) == 200
assert len(A_COLUMNS) == 80
assert len(B_COLUMNS) == 140


def exact_rank(matrix: sp.Matrix) -> int:
    return int(DomainMatrix.from_Matrix(matrix).rank())


def matrix_sha256(matrix: sp.Matrix) -> str:
    rows = [
        ",".join(str(sp.Rational(value)) for value in matrix.row(i))
        for i in range(matrix.rows)
    ]
    return hashlib.sha256("\n".join(rows).encode("utf-8")).hexdigest()


def q_basis_matrices() -> list[sp.Matrix]:
    """G227-compatible basis of algebraic curvature tensors."""
    basis: list[sp.Matrix] = []
    for slot in INDEPENDENT_SLOTS:
        q = sp.zeros(6, 6)
        i, j = slot
        q[i, j] = 1
        q[j, i] = 1
        q[2, 3] = -q[0, 5] + q[1, 4]
        q[3, 2] = q[2, 3]
        basis.append(q)
    return basis


Q_BASIS = q_basis_matrices()


def ordered_pair(a: int, b: int) -> tuple[int, int]:
    if a == b:
        return 0, -1
    if a < b:
        return 1, PAIR_INDEX[(a, b)]
    return -1, PAIR_INDEX[(b, a)]


def riemann_component(coefficients: Sequence[sp.Expr], a: int, b: int, c: int, d: int) -> sp.Expr:
    sign1, i = ordered_pair(a, b)
    sign2, j = ordered_pair(c, d)
    if sign1 == 0 or sign2 == 0:
        return sp.Integer(0)
    return sp.expand(
        sign1 * sign2 * sum(coefficients[k] * Q_BASIS[k][i, j] for k in range(20))
    )


def h_entry(column: tuple[tuple[int, int], tuple[int, int]], a: int, b: int, c: int, d: int) -> int:
    return int(column == (tuple(sorted((a, b))), tuple(sorted((c, d)))))


def k_entry(
    column: tuple[tuple[int, int], tuple[int, int, int]],
    a: int,
    b: int,
    c: int,
    d: int,
    e: int,
) -> int:
    return int(column == (tuple(sorted((a, b))), tuple(sorted((c, d, e)))))


def build_c2() -> sp.Matrix:
    rows: list[list[int]] = []
    for left, right in INDEPENDENT_SLOTS:
        a, b = BIVECTORS[left]
        c, d = BIVECTORS[right]
        row = []
        for column in H_COLUMNS:
            value = (
                h_entry(column, a, d, b, c)
                + h_entry(column, b, c, a, d)
                - h_entry(column, b, d, a, c)
                - h_entry(column, a, c, b, d)
            )
            row.append(value // 2 if value % 2 == 0 else sp.Rational(value, 2))
        rows.append(row)
    return sp.Matrix(rows)


def build_c3() -> sp.Matrix:
    rows: list[list[sp.Expr]] = []
    for derivative in range(4):
        for left, right in INDEPENDENT_SLOTS:
            a, b = BIVECTORS[left]
            c, d = BIVECTORS[right]
            row: list[sp.Expr] = []
            for column in K_COLUMNS:
                value = (
                    k_entry(column, a, d, b, c, derivative)
                    + k_entry(column, b, c, a, d, derivative)
                    - k_entry(column, b, d, a, c, derivative)
                    - k_entry(column, a, c, b, d, derivative)
                )
                row.append(sp.Rational(value, 2))
            rows.append(row)
    return sp.Matrix(rows)


def build_differential_bianchi() -> sp.Matrix:
    rows: list[list[sp.Expr]] = []
    for e, a, b in itertools.combinations(range(4), 3):
        for c, d in BIVECTORS:
            row = [sp.Integer(0)] * 80
            for j in range(20):
                unit = [sp.Integer(0)] * 20
                unit[j] = sp.Integer(1)
                row[e * 20 + j] += riemann_component(unit, a, b, c, d)
                row[a * 20 + j] += riemann_component(unit, b, e, c, d)
                row[b * 20 + j] += riemann_component(unit, e, a, c, d)
            rows.append(row)
    return sp.Matrix(rows)


def build_cubic_gauge() -> sp.Matrix:
    matrix = sp.zeros(100, 80)
    for row, ((i, j), (c, d)) in enumerate(H_COLUMNS):
        matrix[row, A_INDEX[(j, tuple(sorted((i, c, d))))]] += ETA_SIGNS[j]
        matrix[row, A_INDEX[(i, tuple(sorted((j, c, d))))]] += ETA_SIGNS[i]
    return matrix


def build_quartic_gauge() -> sp.Matrix:
    matrix = sp.zeros(200, 140)
    for row, ((i, j), (c, d, e)) in enumerate(K_COLUMNS):
        matrix[row, B_INDEX[(j, tuple(sorted((i, c, d, e))))]] += ETA_SIGNS[j]
        matrix[row, B_INDEX[(i, tuple(sorted((j, c, d, e))))]] += ETA_SIGNS[i]
    return matrix


def unique_permutations(values: Iterable[int]) -> tuple[tuple[int, ...], ...]:
    return tuple(sorted(set(itertools.permutations(tuple(values)))))


def build_normal_2_constraints() -> sp.Matrix:
    matrix = sp.zeros(4 * len(SYMMETRIC_TRIPLES), 100)
    row = 0
    for i in range(4):
        for triple in SYMMETRIC_TRIPLES:
            for j, k, l in unique_permutations(triple):
                matrix[row, H_INDEX[(tuple(sorted((i, j))), tuple(sorted((k, l))))]] += 1
            row += 1
    return matrix


def build_normal_3_constraints() -> sp.Matrix:
    matrix = sp.zeros(4 * len(SYMMETRIC_QUADS), 200)
    row = 0
    for i in range(4):
        for quad in SYMMETRIC_QUADS:
            for j, k, l, m in unique_permutations(quad):
                matrix[
                    row,
                    K_INDEX[(tuple(sorted((i, j))), tuple(sorted((k, l, m))))],
                ] += 1
            row += 1
    return matrix


def build_h_inverse() -> sp.Matrix:
    matrix = sp.zeros(100, 20)
    for row, ((a, b), (c, d)) in enumerate(H_COLUMNS):
        for basis_index in range(20):
            unit = [sp.Integer(0)] * 20
            unit[basis_index] = sp.Integer(1)
            matrix[row, basis_index] = -sp.Rational(1, 3) * (
                riemann_component(unit, a, c, b, d)
                + riemann_component(unit, a, d, b, c)
            )
    return matrix


def build_k_inverse(compatible_basis: sp.Matrix) -> sp.Matrix:
    matrix = sp.zeros(200, compatible_basis.cols)
    permutations = tuple(itertools.permutations(range(3)))
    for row, ((a, b), derivative_triple) in enumerate(K_COLUMNS):
        labels = tuple(derivative_triple)
        for basis_index in range(compatible_basis.cols):
            total = sp.Integer(0)
            for permutation in permutations:
                c = labels[permutation[0]]
                d = labels[permutation[1]]
                e = labels[permutation[2]]
                coefficients = compatible_basis[e * 20 : (e + 1) * 20, basis_index]
                total += riemann_component(coefficients, a, c, b, d)
            matrix[row, basis_index] = -sp.Rational(1, 6) * total
    return matrix


def zero(matrix: sp.Matrix) -> bool:
    return matrix == sp.zeros(matrix.rows, matrix.cols)


def derive() -> dict[str, object]:
    c2 = build_c2()
    c3 = build_c3()
    differential_bianchi = build_differential_bianchi()
    compatible_rows = DomainMatrix.from_Matrix(differential_bianchi).nullspace().to_Matrix()
    compatible_basis = compatible_rows.T

    gauge2 = build_cubic_gauge()
    gauge3 = build_quartic_gauge()
    normal2 = build_normal_2_constraints()
    normal3 = build_normal_3_constraints()
    normal2_basis = DomainMatrix.from_Matrix(normal2).nullspace().to_Matrix().T
    normal3_basis = DomainMatrix.from_Matrix(normal3).nullspace().to_Matrix().T
    h_inverse = build_h_inverse()
    k_inverse = build_k_inverse(compatible_basis)

    ranks = {
        "c2": exact_rank(c2),
        "c3": exact_rank(c3),
        "differential_bianchi": exact_rank(differential_bianchi),
        "compatible_basis": exact_rank(compatible_basis),
        "cubic_gauge": exact_rank(gauge2),
        "quartic_gauge": exact_rank(gauge3),
        "normal2_constraints": exact_rank(normal2),
        "normal3_constraints": exact_rank(normal3),
        "normal2_slice": exact_rank(normal2_basis),
        "normal3_slice": exact_rank(normal3_basis),
        "normal2_on_cubic_gauge": exact_rank(normal2 * gauge2),
        "normal3_on_quartic_gauge": exact_rank(normal3 * gauge3),
        "c2_on_normal2": exact_rank(c2 * normal2_basis),
        "c3_on_normal3": exact_rank(c3 * normal3_basis),
        "h_inverse": exact_rank(h_inverse),
        "k_inverse": exact_rank(k_inverse),
    }

    checks = {
        "c3_satisfies_differential_bianchi": zero(differential_bianchi * c3),
        "cubic_gauge_in_c2_kernel": zero(c2 * gauge2),
        "quartic_gauge_in_c3_kernel": zero(c3 * gauge3),
        "h_inverse_is_right_inverse": c2 * h_inverse == sp.eye(20),
        "k_inverse_realizes_compatible_basis": c3 * k_inverse == compatible_basis,
        "h_inverse_is_normal": zero(normal2 * h_inverse),
        "k_inverse_is_normal": zero(normal3 * k_inverse),
        "c2_kernel_equals_cubic_gauge_by_rank": ranks["c2"] + ranks["cubic_gauge"] == 100,
        "c3_kernel_equals_quartic_gauge_by_rank": ranks["c3"] + ranks["quartic_gauge"] == 200,
        "normal2_restriction_isomorphism": (
            ranks["normal2_slice"] == 20 and ranks["c2_on_normal2"] == 20
        ),
        "normal3_restriction_isomorphism": (
            ranks["normal3_slice"] == 60 and ranks["c3_on_normal3"] == 60
        ),
        "normal2_uniquely_fixes_cubic_gauge": ranks["normal2_on_cubic_gauge"] == 80,
        "normal3_uniquely_fixes_quartic_gauge": ranks["normal3_on_quartic_gauge"] == 140,
    }

    expected_ranks = {
        "c2": 20,
        "c3": 60,
        "differential_bianchi": 20,
        "compatible_basis": 60,
        "cubic_gauge": 80,
        "quartic_gauge": 140,
        "normal2_constraints": 80,
        "normal3_constraints": 140,
        "normal2_slice": 20,
        "normal3_slice": 60,
        "normal2_on_cubic_gauge": 80,
        "normal3_on_quartic_gauge": 140,
        "c2_on_normal2": 20,
        "c3_on_normal3": 60,
        "h_inverse": 20,
        "k_inverse": 60,
    }

    finite_polynomial_witness = {
        "metric": "g_ab(x)=eta_ab+(1/2)H_ab,cd x^c x^d+(1/6)K_ab,cde x^c x^d x^e",
        "origin_metric": "eta_ab",
        "origin_first_derivative": "0",
        "origin_second_derivative": "H_ab,cd",
        "origin_third_derivative": "K_ab,cde",
        "radial_normal_coordinate_identity": (
            "g_ab(x)x^b=eta_ab x^b exactly for this cubic polynomial because "
            "H_a(b,cd)=0 and K_a(b,cde)=0; hence radial coordinate lines are "
            "affinely parametrized geodesics."
        ),
        "signature_statement": (
            "For each supplied finite coefficient set, continuity of the eigenvalues and "
            "det(g(0))=-1 gives a data-dependent open neighborhood of the origin with "
            "Lorentz signature; no uniform radius is claimed."
        ),
        "scope": "local supplied point-jet realization only",
    }

    all_checks_pass = all(checks.values()) and ranks == expected_ranks
    landing = (
        "FULL_LOCAL_3JET_REALIZATION__COORDINATE_KERNELS_80_AND_140"
        if all_checks_pass
        else "PREREGISTERED_ALTERNATIVE_TRIGGERED__INSPECT_EXACT_FAILURES"
    )

    matrices = {
        "c2": c2,
        "c3": c3,
        "differential_bianchi": differential_bianchi,
        "compatible_basis": compatible_basis,
        "cubic_gauge": gauge2,
        "quartic_gauge": gauge3,
        "normal2_constraints": normal2,
        "normal3_constraints": normal3,
        "normal2_basis": normal2_basis,
        "normal3_basis": normal3_basis,
        "h_inverse": h_inverse,
        "k_inverse": k_inverse,
    }

    return {
        "landing": landing,
        "all_exact_checks_pass": all_checks_pass,
        "dimensions": {
            "metric_2jet": 100,
            "algebraic_curvature": 20,
            "metric_3jet": 200,
            "reduced_curvature_derivative": 80,
            "compatible_curvature_derivative": 60,
            "cubic_coordinate_gauge": 80,
            "quartic_coordinate_gauge": 140,
        },
        "ranks": ranks,
        "expected_ranks": expected_ranks,
        "checks": checks,
        "matrix_sha256": {name: matrix_sha256(matrix) for name, matrix in matrices.items()},
        "conventions": {
            "eta": "diag(-1,+1,+1,+1)",
            "curvature": (
                "R^rho_(sigma mu nu)=partial_mu Gamma^rho_(nu sigma)-"
                "partial_nu Gamma^rho_(mu sigma)+GammaGamma-GammaGamma"
            ),
            "c2": "1/2(H_ad,bc+H_bc,ad-H_bd,ac-H_ac,bd)",
            "c3": "1/2(K_ad,bce+K_bc,ade-K_bd,ace-K_ac,bde)",
            "algebraic_bianchi": "Q[01,23]-Q[02,13]+Q[03,12]=0",
            "normal2": "H_i(j,kl)=0",
            "normal3": "K_i(j,klm)=0",
        },
        "finite_polynomial_witness": finite_polynomial_witness,
        "coordinate_gauge_derivation": {
            "cubic_change": "x^a=y^a+(1/6)A^a_bcd y^b y^c y^d",
            "quadratic_metric_jet": "Delta H_ij,cd=A_(j i cd)+A_(i j cd)",
            "quartic_change": "x^a=y^a+(1/24)B^a_bcde y^b y^c y^d y^e",
            "cubic_metric_jet": "Delta K_ij,cde=B_(j i cde)+B_(i j cde)",
            "lowering": "A_(a bcd)=eta_ae A^e_bcd and likewise for B",
            "tangent_frame": (
                "The identity linear part fixes the tangent frame. Residual linear Lorentz "
                "changes would only change components; they are outside the fixed-frame kernel test."
            ),
        },
        "scope_ceiling": (
            "Every supplied compatible (R,nabla R) at one event is realized by a local "
            "Lorentz metric 3-jet. This does not generate values, a prescribed curvature "
            "field on a region, observer/null population, dynamics, or global history."
        ),
        "versions": {
            "python": platform.python_version(),
            "sympy": sp.__version__,
            "platform": platform.platform(),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    result = derive()
    if not args.no_write:
        output = ROOT / "exact_results.json"
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["all_exact_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
