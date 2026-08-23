#!/usr/bin/env python3
"""Exact G230 curvature-second-jet / metric-fourth-jet calculation.

At one supplied locally inertial event, this constructs the complete linear
highest-derivative map L=g_,4 -> E=nabla^2 R, the differentiated-Bianchi and
Ricci-commutator constraints, the quadratic lower-jet affine offset, and the
complete fifth-order coordinate gauge.  It does not prescribe regional
curvature values or a metric history.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import platform
import subprocess
import sys
from pathlib import Path
from typing import Iterable, Sequence

import sympy as sp
from sympy.polys.matrices import DomainMatrix


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
ETA = (-1, 1, 1, 1)
BIVECTORS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
PAIR_INDEX = {pair: i for i, pair in enumerate(BIVECTORS)}
DEPENDENT_SLOT = (2, 3)
INDEPENDENT_SLOTS = tuple(
    (i, j) for i in range(6) for j in range(i, 6) if (i, j) != DEPENDENT_SLOT
)
SYMMETRIC_PAIRS = tuple(itertools.combinations_with_replacement(range(4), 2))
SYMMETRIC_QUADS = tuple(itertools.combinations_with_replacement(range(4), 4))
SYMMETRIC_QUINTS = tuple(itertools.combinations_with_replacement(range(4), 5))

L_COLUMNS = tuple((ab, cdef) for ab in SYMMETRIC_PAIRS for cdef in SYMMETRIC_QUADS)
G_COLUMNS = tuple((a, bcdef) for a in range(4) for bcdef in SYMMETRIC_QUINTS)
E_ROWS = tuple(
    (f, e, left, right)
    for f in range(4)
    for e in range(4)
    for left, right in INDEPENDENT_SLOTS
)
L_INDEX = {label: i for i, label in enumerate(L_COLUMNS)}
G_INDEX = {label: i for i, label in enumerate(G_COLUMNS)}
E_INDEX = {label: i for i, label in enumerate(E_ROWS)}

assert len(INDEPENDENT_SLOTS) == 20
assert len(L_COLUMNS) == 350
assert len(G_COLUMNS) == 224
assert len(E_ROWS) == 320


def exact_rank(matrix: sp.Matrix) -> int:
    return int(DomainMatrix.from_Matrix(matrix).rank())


def matrix_sha256(matrix: sp.Matrix) -> str:
    lines = [
        ",".join(str(sp.Rational(value)) for value in matrix.row(i))
        for i in range(matrix.rows)
    ]
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()


def q_basis_matrices() -> list[sp.Matrix]:
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


def riemann_component(coeffs: Sequence[sp.Expr], a: int, b: int, c: int, d: int) -> sp.Expr:
    sign1, i = ordered_pair(a, b)
    sign2, j = ordered_pair(c, d)
    if sign1 == 0 or sign2 == 0:
        return sp.Integer(0)
    return sp.expand(
        sign1 * sign2 * sum(coeffs[k] * Q_BASIS[k][i, j] for k in range(20))
    )


def l_entry(
    column: tuple[tuple[int, int], tuple[int, int, int, int]],
    a: int,
    b: int,
    c: int,
    d: int,
    e: int,
    f: int,
) -> int:
    return int(column == (tuple(sorted((a, b))), tuple(sorted((c, d, e, f)))))


def build_c4() -> sp.Matrix:
    rows: list[list[sp.Expr]] = []
    for f, e, left, right in E_ROWS:
        a, b = BIVECTORS[left]
        c, d = BIVECTORS[right]
        row: list[sp.Expr] = []
        for column in L_COLUMNS:
            value = (
                l_entry(column, a, d, b, c, e, f)
                + l_entry(column, b, c, a, d, e, f)
                - l_entry(column, b, d, a, c, e, f)
                - l_entry(column, a, c, b, d, e, f)
            )
            row.append(sp.Rational(value, 2))
        rows.append(row)
    return sp.Matrix(rows)


def build_differentiated_bianchi() -> sp.Matrix:
    rows: list[list[sp.Expr]] = []
    for f in range(4):
        for e, a, b in itertools.combinations(range(4), 3):
            for c, d in BIVECTORS:
                row = [sp.Integer(0)] * 320
                for j in range(20):
                    unit = [sp.Integer(0)] * 20
                    unit[j] = sp.Integer(1)
                    row[E_INDEX[(f, e, *INDEPENDENT_SLOTS[j])]] += riemann_component(
                        unit, a, b, c, d
                    )
                    row[E_INDEX[(f, a, *INDEPENDENT_SLOTS[j])]] += riemann_component(
                        unit, b, e, c, d
                    )
                    row[E_INDEX[(f, b, *INDEPENDENT_SLOTS[j])]] += riemann_component(
                        unit, e, a, c, d
                    )
                rows.append(row)
    return sp.Matrix(rows)


def build_first_differential_bianchi() -> sp.Matrix:
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


def build_commutator_matrix() -> sp.Matrix:
    rows: list[list[int]] = []
    for f, e in itertools.combinations(range(4), 2):
        for slot in INDEPENDENT_SLOTS:
            row = [0] * 320
            row[E_INDEX[(f, e, *slot)]] = 1
            row[E_INDEX[(e, f, *slot)]] = -1
            rows.append(row)
    return sp.Matrix(rows)


def build_quintic_gauge() -> sp.Matrix:
    matrix = sp.zeros(350, 224)
    for row, ((i, j), (c, d, e, f)) in enumerate(L_COLUMNS):
        matrix[row, G_INDEX[(j, tuple(sorted((i, c, d, e, f))))]] += ETA[j]
        matrix[row, G_INDEX[(i, tuple(sorted((j, c, d, e, f))))]] += ETA[i]
    return matrix


def unique_permutations(values: Iterable[int]) -> tuple[tuple[int, ...], ...]:
    return tuple(sorted(set(itertools.permutations(tuple(values)))))


def build_normal4_constraints() -> sp.Matrix:
    matrix = sp.zeros(4 * len(SYMMETRIC_QUINTS), 350)
    row = 0
    for i in range(4):
        for quint in SYMMETRIC_QUINTS:
            for j, k, l, m, n in unique_permutations(quint):
                matrix[
                    row,
                    L_INDEX[(tuple(sorted((i, j))), tuple(sorted((k, l, m, n))))],
                ] += 1
            row += 1
    return matrix


def h_normal(coeffs: Sequence[sp.Expr], a: int, b: int, c: int, d: int) -> sp.Expr:
    return -sp.Rational(1, 3) * (
        riemann_component(coeffs, a, c, b, d)
        + riemann_component(coeffs, a, d, b, c)
    )


def dgamma(
    coeffs: Sequence[sp.Expr], derivative: int, upper: int, lower1: int, lower2: int
) -> sp.Expr:
    return sp.Rational(ETA[upper], 2) * (
        h_normal(coeffs, upper, lower2, lower1, derivative)
        + h_normal(coeffs, upper, lower1, lower2, derivative)
        - h_normal(coeffs, lower1, lower2, upper, derivative)
    )


def q_component(
    coeffs: Sequence[sp.Expr], f: int, e: int, a: int, b: int, c: int, d: int
) -> sp.Expr:
    """Quadratic lower-jet contribution to (nabla_f nabla_e R)_abcd."""
    product = sp.Integer(0)
    for p in range(4):
        product += ETA[p] * (
            dgamma(coeffs, e, p, b, c) * dgamma(coeffs, f, p, a, d)
            + dgamma(coeffs, f, p, b, c) * dgamma(coeffs, e, p, a, d)
            - dgamma(coeffs, e, p, b, d) * dgamma(coeffs, f, p, a, c)
            - dgamma(coeffs, f, p, b, d) * dgamma(coeffs, e, p, a, c)
        )
    covariantization = sp.Integer(0)
    for p in range(4):
        covariantization -= dgamma(coeffs, f, p, e, a) * riemann_component(
            coeffs, p, b, c, d
        )
        covariantization -= dgamma(coeffs, f, p, e, b) * riemann_component(
            coeffs, a, p, c, d
        )
        covariantization -= dgamma(coeffs, f, p, e, c) * riemann_component(
            coeffs, a, b, p, d
        )
        covariantization -= dgamma(coeffs, f, p, e, d) * riemann_component(
            coeffs, a, b, c, p
        )
    return sp.expand(product + covariantization)


def q_vector(coeffs: Sequence[sp.Expr]) -> sp.Matrix:
    values: list[sp.Expr] = []
    for f, e, left, right in E_ROWS:
        a, b = BIVECTORS[left]
        c, d = BIVECTORS[right]
        values.append(q_component(coeffs, f, e, a, b, c, d))
    return sp.Matrix(values)


def commutator_rhs_component(
    coeffs: Sequence[sp.Expr], f: int, e: int, a: int, b: int, c: int, d: int
) -> sp.Expr:
    value = sp.Integer(0)
    for p in range(4):
        raised = ETA[p] * riemann_component(coeffs, p, a, f, e)
        value -= raised * riemann_component(coeffs, p, b, c, d)
        raised = ETA[p] * riemann_component(coeffs, p, b, f, e)
        value -= raised * riemann_component(coeffs, a, p, c, d)
        raised = ETA[p] * riemann_component(coeffs, p, c, f, e)
        value -= raised * riemann_component(coeffs, a, b, p, d)
        raised = ETA[p] * riemann_component(coeffs, p, d, f, e)
        value -= raised * riemann_component(coeffs, a, b, c, p)
    return sp.expand(value)


def commutator_rhs(coeffs: Sequence[sp.Expr]) -> sp.Matrix:
    values: list[sp.Expr] = []
    for f, e in itertools.combinations(range(4), 2):
        for left, right in INDEPENDENT_SLOTS:
            a, b = BIVECTORS[left]
            c, d = BIVECTORS[right]
            values.append(commutator_rhs_component(coeffs, f, e, a, b, c, d))
    return sp.Matrix(values)


def quadratic_polarization_cases() -> list[list[sp.Integer]]:
    cases: list[list[sp.Integer]] = []
    for i in range(20):
        vector = [sp.Integer(0)] * 20
        vector[i] = sp.Integer(1)
        cases.append(vector)
    for i in range(20):
        for j in range(i + 1, 20):
            vector = [sp.Integer(0)] * 20
            vector[i] = sp.Integer(1)
            vector[j] = sp.Integer(1)
            cases.append(vector)
    assert len(cases) == 210
    return cases


def verify_preregistration() -> bool:
    rows = []
    for line in (ROOT / "PREREGISTRATION_HASHES.tsv").read_text(encoding="utf-8").splitlines()[1:]:
        path, digest = line.split("\t")
        actual = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
        rows.append(actual == digest)
    return all(rows)


def verify_sources() -> bool:
    rows = []
    for line in (ROOT / "SOURCE_MANIFEST.tsv").read_text(encoding="utf-8").splitlines()[1:]:
        digest, path = line.split("\t")
        current = hashlib.sha256((REPO / path).read_bytes()).hexdigest()
        if current == digest:
            rows.append(True)
            continue
        frozen = subprocess.run(
            ["git", "show", f"3808e397:{path}"],
            cwd=REPO,
            check=True,
            capture_output=True,
        ).stdout
        rows.append(hashlib.sha256(frozen).hexdigest() == digest)
    return all(rows)


def derive() -> dict[str, object]:
    c4 = build_c4()
    db2 = build_differentiated_bianchi()
    comm = build_commutator_matrix()
    constraints = db2.col_join(comm)
    gauge = build_quintic_gauge()
    normal = build_normal4_constraints()

    ranks = {
        "c4": exact_rank(c4),
        "differentiated_bianchi": exact_rank(db2),
        "commutator": exact_rank(comm),
        "combined_constraints": exact_rank(constraints),
        "quintic_gauge": exact_rank(gauge),
        "normal4": exact_rank(normal),
        "normal4_on_quintic_gauge": exact_rank(normal * gauge),
        "stacked_normal4_c4": exact_rank(normal.col_join(c4)),
    }

    linear_checks = {
        "c4_in_constraint_kernel": constraints * c4 == sp.zeros(constraints.rows, c4.cols),
        "quintic_gauge_in_c4_kernel": c4 * gauge == sp.zeros(c4.rows, gauge.cols),
        "c4_kernel_equals_quintic_gauge_by_rank": ranks["c4"] + ranks["quintic_gauge"] == 350,
        "constraint_kernel_equals_c4_image_by_rank": ranks["combined_constraints"] + ranks["c4"] == 320,
        "normal_slice_dimension_126": 350 - ranks["normal4"] == 126,
        "normal_slice_map_isomorphism": ranks["stacked_normal4_c4"] == 350,
        "normal4_uniquely_fixes_quintic_gauge": ranks["normal4_on_quintic_gauge"] == 224,
    }

    cases = quadratic_polarization_cases()
    nonlinear_pass = True
    witness: dict[str, object] | None = None
    witness_coeffs: list[sp.Integer] | None = None
    max_db_nonzero = 0
    max_comm_nonzero = 0
    for case_index, coeffs in enumerate(cases):
        q = q_vector(coeffs)
        db_residual = db2 * q
        comm_residual = comm * q - commutator_rhs(coeffs)
        db_nonzero = sum(value != 0 for value in db_residual)
        comm_nonzero = sum(value != 0 for value in comm_residual)
        max_db_nonzero = max(max_db_nonzero, db_nonzero)
        max_comm_nonzero = max(max_comm_nonzero, comm_nonzero)
        if db_nonzero or comm_nonzero:
            nonlinear_pass = False
            break
        rhs = commutator_rhs(coeffs)
        if witness is None and rhs != sp.zeros(120, 1):
            witness_coeffs = list(coeffs)
            witness = {
                "case_index": case_index,
                "nonzero_coefficients": [i for i, value in enumerate(coeffs) if value],
                "rhs_nonzero_count": sum(value != 0 for value in rhs),
                "rhs_first_nonzero_row": next(i for i, value in enumerate(rhs) if value),
                "rhs_first_nonzero_value": str(next(value for value in rhs if value)),
            }

    assert witness_coeffs is not None
    g227_residuals = [
        sp.expand(
            riemann_component(witness_coeffs, a, b, c, d)
            + riemann_component(witness_coeffs, a, c, d, b)
            + riemann_component(witness_coeffs, a, d, b, c)
        )
        for a, b, c, d in itertools.product(range(4), repeat=4)
    ]
    first_bianchi = build_first_differential_bianchi()
    zero_d = sp.zeros(80, 1)
    zero_e = sp.zeros(320, 1)
    witness_rhs = commutator_rhs(witness_coeffs)
    lower_order_witness = {
        "g227_algebraic_bianchi_nonzero": sum(value != 0 for value in g227_residuals),
        "g228_zero_D_differential_bianchi_nonzero": sum(
            value != 0 for value in first_bianchi * zero_d
        ),
        "g230_zero_E_differentiated_bianchi_nonzero": sum(value != 0 for value in db2 * zero_e),
        "g230_zero_E_commutator_residual_nonzero": sum(
            value != 0 for value in comm * zero_e - witness_rhs
        ),
    }

    checks = {
        **linear_checks,
        "quadratic_affine_identities_complete_polarization": nonlinear_pass,
        "nonzero_commutator_witness_found": witness is not None,
        "g227_witness_explicit_algebraic_bianchi_pass": lower_order_witness[
            "g227_algebraic_bianchi_nonzero"
        ]
        == 0,
        "g228_zero_D_explicit_differential_bianchi_pass": lower_order_witness[
            "g228_zero_D_differential_bianchi_nonzero"
        ]
        == 0,
        "zero_E_explicit_differentiated_bianchi_pass": lower_order_witness[
            "g230_zero_E_differentiated_bianchi_nonzero"
        ]
        == 0,
        "zero_E_explicit_commutator_failure_detected": lower_order_witness[
            "g230_zero_E_commutator_residual_nonzero"
        ]
        > 0,
        "preregistration_hashes_match": verify_preregistration(),
        "source_manifest_hashes_match": verify_sources(),
    }

    expected_ranks = {
        "c4": 126,
        "differentiated_bianchi": 80,
        "commutator": 120,
        "combined_constraints": 194,
        "quintic_gauge": 224,
        "normal4": 224,
        "normal4_on_quintic_gauge": 224,
        "stacked_normal4_c4": 350,
    }
    rank_expectations_pass = ranks == expected_ranks
    checks["all_preregistered_rank_expectations"] = rank_expectations_pass

    all_pass = all(bool(value) for value in checks.values())
    landing = (
        "FIRST_NONLINEAR_OVERLAP_OBSTRUCTION__FULL_LOCAL_4JET_REALIZATION"
        if all_pass
        else "G230_PREREGISTERED_ALTERNATIVE_REQUIRES_ADJUDICATION"
    )
    return {
        "landing": landing,
        "scope": "one supplied event, fixed tangent frame, metric through quartic Taylor order",
        "dimensions": {
            "metric_fourth_jet": 350,
            "ordered_curvature_second_derivative": 320,
            "compatible_affine_translation": 320 - ranks["combined_constraints"],
            "quintic_coordinate_domain": 224,
        },
        "ranks": ranks,
        "expected_ranks": expected_ranks,
        "checks": checks,
        "quadratic_polarization": {
            "cases": len(cases),
            "covers_diagonal_monomials": 20,
            "covers_cross_monomials": 190,
            "max_differentiated_bianchi_nonzero": max_db_nonzero,
            "max_commutator_nonzero": max_comm_nonzero,
        },
        "nonzero_commutator_witness": witness,
        "lower_order_witness_residuals": lower_order_witness,
        "hashes": {
            "c4": matrix_sha256(c4),
            "differentiated_bianchi": matrix_sha256(db2),
            "commutator": matrix_sha256(comm),
            "combined_constraints": matrix_sha256(constraints),
            "quintic_gauge": matrix_sha256(gauge),
            "normal4": matrix_sha256(normal),
        },
        "environment": {
            "python": sys.version.split()[0],
            "sympy": sp.__version__,
            "platform": platform.platform(),
        },
        "ceiling": (
            "Pointwise fourth-order realization and first nonlinear necessary overlap condition only; "
            "no prescribed regional field, value generation, dynamics, population, transport, or history."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    result = derive()
    text = json.dumps(result, indent=2, sort_keys=True)
    print(text)
    if not args.no_write:
        (ROOT / "exact_results.json").write_text(text + "\n", encoding="utf-8")
    if not all(result["checks"].values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
