#!/usr/bin/env python3
"""Exact G228 production algebra.

Builds the algebraic covariant-derivative-curvature module, imposes the
differential Bianchi identity, classifies every frozen null-tetrad subset,
and verifies the moving-screen/Jacobi gauge identities.

All physics data are symbolic or exact rational controls.  No numerical
history values are generated.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
from typing import Iterable, Sequence

import sympy as sp


BIVECTORS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
PAIR_INDEX = {pair: i for i, pair in enumerate(BIVECTORS)}
DEPENDENT_SLOT = (2, 3)  # Q[03,12]
INDEPENDENT_SLOTS = tuple(
    (i, j)
    for i in range(6)
    for j in range(i, 6)
    if (i, j) != DEPENDENT_SLOT
)
assert len(INDEPENDENT_SLOTS) == 20

DIRECTIONS = {
    "k": (sp.Integer(1), sp.Integer(0), sp.Integer(0), sp.Integer(1)),
    "l": (sp.Rational(1, 2), sp.Integer(0), sp.Integer(0), sp.Rational(-1, 2)),
    "s1": (sp.Integer(0), sp.Integer(1), sp.Integer(0), sp.Integer(0)),
    "s2": (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(0)),
}
DIRECTION_ORDER = ("k", "l", "s1", "s2")


def canonical_integer_vector(vec: Sequence[sp.Expr]) -> list[int]:
    rationals = [sp.Rational(x) for x in vec]
    lcm = 1
    for value in rationals:
        lcm = sp.ilcm(lcm, int(value.q))
    integers = [int(value * lcm) for value in rationals]
    nonzero = [abs(x) for x in integers if x]
    gcd = 0
    for value in nonzero:
        gcd = math.gcd(gcd, value)
    if gcd:
        integers = [x // gcd for x in integers]
    for value in integers:
        if value:
            if value < 0:
                integers = [-x for x in integers]
            break
    return integers


def matrix_sha256(matrix: sp.Matrix) -> str:
    rows = [",".join(str(sp.Rational(value)) for value in matrix.row(i)) for i in range(matrix.rows)]
    return hashlib.sha256("\n".join(rows).encode("utf-8")).hexdigest()


def q_basis_matrices() -> list[sp.Matrix]:
    """Return the G227-compatible 20-element algebraic-curvature basis."""
    basis: list[sp.Matrix] = []
    for slot in INDEPENDENT_SLOTS:
        q = sp.zeros(6, 6)
        i, j = slot
        q[i, j] = 1
        q[j, i] = 1
        # Q[01,23] - Q[02,13] + Q[03,12] = 0.
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


def riemann_basis_component(basis_index: int, a: int, b: int, c: int, d: int) -> sp.Expr:
    sign1, i = ordered_pair(a, b)
    sign2, j = ordered_pair(c, d)
    if sign1 == 0 or sign2 == 0:
        return sp.Integer(0)
    return sign1 * sign2 * Q_BASIS[basis_index][i, j]


def build_differential_bianchi_matrix() -> tuple[sp.Matrix, list[tuple[int, int, int, int, int]]]:
    rows: list[list[sp.Expr]] = []
    labels: list[tuple[int, int, int, int, int]] = []
    for e, a, b in itertools.combinations(range(4), 3):
        for c, d in BIVECTORS:
            row = [sp.Integer(0)] * 80
            for j in range(20):
                row[e * 20 + j] += riemann_basis_component(j, a, b, c, d)
                row[a * 20 + j] += riemann_basis_component(j, b, e, c, d)
                row[b * 20 + j] += riemann_basis_component(j, e, a, c, d)
            rows.append(row)
            labels.append((e, a, b, c, d))
    return sp.Matrix(rows), labels


def direction_projection(direction: Sequence[sp.Expr]) -> sp.Matrix:
    matrix = sp.zeros(20, 80)
    for component in range(20):
        for mu, coefficient in enumerate(direction):
            matrix[component, mu * 20 + component] = coefficient
    return matrix


def stacked_projection(names: Sequence[str]) -> sp.Matrix:
    return sp.Matrix.vstack(*(direction_projection(DIRECTIONS[name]) for name in names))


def check_null_tetrad() -> dict[str, object]:
    eta = sp.diag(-1, 1, 1, 1)

    def inner(u: Sequence[sp.Expr], v: Sequence[sp.Expr]) -> sp.Expr:
        return sp.simplify((sp.Matrix(u).T * eta * sp.Matrix(v))[0])

    gram = {
        f"{left}_{right}": str(inner(DIRECTIONS[left], DIRECTIONS[right]))
        for left in DIRECTION_ORDER
        for right in DIRECTION_ORDER
    }
    basis_matrix = sp.Matrix.hstack(*(sp.Matrix(DIRECTIONS[name]) for name in DIRECTION_ORDER))
    return {
        "gram": gram,
        "basis_determinant": str(sp.factor(basis_matrix.det())),
        "spans_tangent_space": basis_matrix.rank() == 4,
        "k_null": inner(DIRECTIONS["k"], DIRECTIONS["k"]) == 0,
        "l_null": inner(DIRECTIONS["l"], DIRECTIONS["l"]) == 0,
        "k_dot_l": str(inner(DIRECTIONS["k"], DIRECTIONS["l"])),
    }


def screen_and_phase_checks() -> dict[str, object]:
    theta, omega = sp.symbols("theta omega", real=True)
    a, b, d, ap, bp, dp = sp.symbols("a b d ap bp dp", real=True)
    c = sp.cos(theta)
    s = sp.sin(theta)
    C = sp.Matrix(((c, -s), (s, c)))
    J2 = sp.Matrix(((0, -1), (1, 0)))
    Omega = omega * J2
    Cp = C * Omega
    T = sp.Matrix(((a, b), (b, d)))
    Tp = sp.Matrix(((ap, bp), (bp, dp)))
    TE = sp.simplify(C.T * T * C)
    TEprime = sp.simplify(Cp.T * T * C + C.T * Tp * C + C.T * T * Cp)
    covariant_tide_residual = sp.simplify(TEprime + Omega * TE - TE * Omega - C.T * Tp * C)

    I2 = sp.eye(2)
    Z2 = sp.zeros(2, 2)
    A_parallel = sp.Matrix.vstack(
        sp.Matrix.hstack(Z2, I2),
        sp.Matrix.hstack(-T, Z2),
    )
    H = sp.diag(1, 1, 1, 1)
    H[:2, :2] = C
    H[2:, 2:] = C
    Hprime = sp.zeros(4, 4)
    Hprime[:2, :2] = Cp
    Hprime[2:, 2:] = Cp
    A_moving_from_change = sp.simplify(H.T * A_parallel * H - H.T * Hprime)
    A_moving_expected = sp.Matrix.vstack(
        sp.Matrix.hstack(-Omega, I2),
        sp.Matrix.hstack(-TE, -Omega),
    )
    phase_change_residual = sp.simplify(A_moving_from_change - A_moving_expected)
    symplectic = sp.Matrix.vstack(
        sp.Matrix.hstack(Z2, I2),
        sp.Matrix.hstack(-I2, Z2),
    )
    hamiltonian_residual = sp.simplify(A_moving_expected.T * symplectic + symplectic * A_moving_expected)

    # Exact rational noncommuting catch control.
    Cq = sp.Matrix(((sp.Rational(3, 5), sp.Rational(-4, 5)),
                    (sp.Rational(4, 5), sp.Rational(3, 5))))
    Oq = sp.Rational(7, 3) * J2
    Tq = sp.Matrix(((2, 3), (3, 5)))
    Tpq = sp.Matrix(((7, 11), (11, 13)))
    TEq = Cq.T * Tq * Cq
    TEpq = (Cq * Oq).T * Tq * Cq + Cq.T * Tpq * Cq + Cq.T * Tq * (Cq * Oq)
    omitted_commutator = sp.simplify(TEpq - Cq.T * Tpq * Cq)
    correct_rational = sp.simplify(TEpq + Oq * TEq - TEq * Oq - Cq.T * Tpq * Cq)

    return {
        "covariant_tide_identity": covariant_tide_residual == sp.zeros(2, 2),
        "phase_change_identity": phase_change_residual == sp.zeros(4, 4),
        "hamiltonian_generator": hamiltonian_residual == sp.zeros(4, 4),
        "omega_skew": sp.simplify(Omega.T + Omega) == sp.zeros(2, 2),
        "moving_tide_symmetric": sp.simplify(TE.T - TE) == sp.zeros(2, 2),
        "rational_control_exact": correct_rational == sp.zeros(2, 2),
        "omitted_commutator_detected": omitted_commutator != sp.zeros(2, 2),
        "rational_omitted_commutator": [[str(x) for x in omitted_commutator.row(i)] for i in range(2)],
    }


def rows_as_strings(matrix: sp.Matrix) -> list[list[str]]:
    return [[str(sp.Rational(value)) for value in matrix.row(i)] for i in range(matrix.rows)]


def derive() -> tuple[dict[str, object], dict[str, list[list[int]]], list[dict[str, object]]]:
    bianchi, labels = build_differential_bianchi_matrix()
    bianchi_rank = int(bianchi.rank())
    module_dimension = 80 - bianchi_rank
    kernel_vectors = bianchi.nullspace()
    kernel = sp.Matrix.hstack(*kernel_vectors)
    assert kernel.shape == (80, module_dimension)

    seed = sp.Matrix([((13 * i + 5) % 23) - 11 for i in range(module_dimension)])
    subset_results: list[dict[str, object]] = []
    syzygies: dict[str, list[list[int]]] = {}

    for size in range(1, 5):
        for names in itertools.combinations(DIRECTION_ORDER, size):
            key = "+".join(names)
            projection = stacked_projection(names)
            image = projection * kernel
            rank = int(image.rank())
            target_dimension = 20 * size
            codimension = target_dimension - rank
            left_null = image.T.nullspace()
            integer_syzygies = [canonical_integer_vector(vec) for vec in left_null]
            syzygies[key] = integer_syzygies

            compatible = image * seed
            syzygies_pass = all((sp.Matrix(vec).T * compatible)[0] == 0 for vec in left_null)
            within = compatible + image[:, 0]
            within_pass = all((sp.Matrix(vec).T * within)[0] == 0 for vec in left_null)

            hostile_detected = None
            hostile_index = None
            hostile_residual = None
            if left_null:
                witness = left_null[0]
                hostile_index = next(i for i, value in enumerate(witness) if value != 0)
                hostile = compatible.copy()
                hostile[hostile_index] += 1
                hostile_residual = sp.simplify((witness.T * hostile)[0])
                hostile_detected = hostile_residual != 0

            subset_results.append(
                {
                    "subset": list(names),
                    "key": key,
                    "size": size,
                    "target_dimension": target_dimension,
                    "image_rank": rank,
                    "codimension": codimension,
                    "syzygy_count": len(left_null),
                    "syzygies_pass_seeded_control": syzygies_pass,
                    "within_image_perturbation_accepted": within_pass,
                    "hostile_one_entry_index": hostile_index,
                    "hostile_one_entry_detected": hostile_detected,
                    "hostile_syzygy_residual": None if hostile_residual is None else str(hostile_residual),
                    "image_sha256": matrix_sha256(image),
                }
            )

    restricted_sizes = [row["size"] for row in subset_results if row["codimension"] > 0]
    first_restricted_size = min(restricted_sizes) if restricted_sizes else None
    one_direction_surjective = all(
        row["codimension"] == 0 for row in subset_results if row["size"] == 1
    )

    if not one_direction_surjective:
        selected_alternative = "D_ONE_DIRECTION_ALREADY_RESTRICTED"
    elif module_dimension != 60:
        selected_alternative = "E_DIFFERENTIAL_BIANCHI_MODULE_NOT_DIMENSION_60_OR_OTHER_UNEXPECTED_STRUCTURE"
    elif first_restricted_size == 2:
        selected_alternative = "A_ONE_DIRECTION_SURJECTIVE__FIRST_RESTRICTION_AT_TWO_DIRECTIONS"
    elif first_restricted_size == 3:
        selected_alternative = "B_ONE_DIRECTION_SURJECTIVE__FIRST_RESTRICTION_AT_THREE_DIRECTIONS"
    elif first_restricted_size == 4:
        selected_alternative = "C_ONE_DIRECTION_SURJECTIVE__FIRST_RESTRICTION_AT_FOUR_DIRECTIONS"
    else:
        selected_alternative = "E_DIFFERENTIAL_BIANCHI_MODULE_NOT_DIMENSION_60_OR_OTHER_UNEXPECTED_STRUCTURE"

    screen = screen_and_phase_checks()
    all_subset_controls = all(
        row["syzygies_pass_seeded_control"]
        and row["within_image_perturbation_accepted"]
        and (row["hostile_one_entry_detected"] is True if row["codimension"] else row["hostile_one_entry_detected"] is None)
        for row in subset_results
    )

    result: dict[str, object] = {
        "landing": selected_alternative,
        "raw_derivative_variables": 80,
        "differential_bianchi_generated_rows": bianchi.rows,
        "differential_bianchi_independent_rank": bianchi_rank,
        "compatible_module_dimension": module_dimension,
        "bianchi_matrix_sha256": matrix_sha256(bianchi),
        "kernel_matrix_sha256": matrix_sha256(kernel),
        "null_tetrad": check_null_tetrad(),
        "one_direction_surjective": one_direction_surjective,
        "first_restricted_subset_size": first_restricted_size,
        "subset_count": len(subset_results),
        "all_subset_controls_pass": all_subset_controls,
        "screen_and_phase": screen,
        "all_screen_and_phase_checks_pass": all(bool(v) for key, v in screen.items() if key != "rational_omitted_commutator"),
        "equation_labels": [list(label) for label in labels],
    }
    return result, syzygies, subset_results


def write_outputs(output_dir: Path, result: dict[str, object], syzygies: dict[str, list[list[int]]], subsets: list[dict[str, object]]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "DERIVATION_RESULT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    (output_dir / "SYZYGY_BASIS.json").write_text(json.dumps(syzygies, indent=2, sort_keys=True) + "\n")
    columns = (
        "key", "size", "target_dimension", "image_rank", "codimension", "syzygy_count",
        "syzygies_pass_seeded_control", "within_image_perturbation_accepted",
        "hostile_one_entry_index", "hostile_one_entry_detected", "hostile_syzygy_residual",
        "image_sha256",
    )
    lines = ["\t".join(columns)]
    for row in subsets:
        lines.append("\t".join(str(row[column]) for column in columns))
    (output_dir / "SUBSET_CENSUS.tsv").write_text("\n".join(lines) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()
    result, syzygies, subsets = derive()
    if not args.no_write:
        write_outputs(args.output_dir, result, syzygies, subsets)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
