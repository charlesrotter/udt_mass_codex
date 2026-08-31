#!/usr/bin/env python3
"""Dependency-free exact production certificate for the bounded G310 audit."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path


LANDING = (
    "ONE_NEW_DIFFERENTIAL_DUAL_RECIPROCITY_POSTULATE_SELECTS_G301_TRACEFREE_CLASS"
    "__NOT_DERIVED_OR_ADOPTED"
)
DIMENSION = 4
SYMMETRIC_INDICES = tuple((i, j) for i in range(DIMENSION) for j in range(i, DIMENSION))
PAIRING_WEIGHTS = tuple(
    (1 if i == j else 2) * (-1 if (i == 0) ^ (j == 0) else 1)
    for i, j in SYMMETRIC_INDICES
)


def matrix(rows: int, columns: int, fill: Fraction = Fraction(0)) -> list[list[Fraction]]:
    return [[fill for _ in range(columns)] for _ in range(rows)]


def identity(size: int) -> list[list[Fraction]]:
    result = matrix(size, size)
    for i in range(size):
        result[i][i] = Fraction(1)
    return result


def diagonal(*entries: int | Fraction) -> list[list[Fraction]]:
    result = matrix(len(entries), len(entries))
    for i, entry in enumerate(entries):
        result[i][i] = Fraction(entry)
    return result


def transpose(value: list[list[Fraction]]) -> list[list[Fraction]]:
    return [list(row) for row in zip(*value)]


def multiply(left: list[list[Fraction]], right: list[list[Fraction]]) -> list[list[Fraction]]:
    return [
        [sum((left[i][k] * right[k][j] for k in range(len(right))), Fraction(0))
         for j in range(len(right[0]))]
        for i in range(len(left))
    ]


def same(left: list[list[Fraction]], right: list[list[Fraction]]) -> bool:
    return left == right


def matrix_key(value: list[list[Fraction]]) -> tuple[Fraction, ...]:
    return tuple(entry for row in value for entry in row)


def symmetric_vector(value: list[list[Fraction]]) -> list[Fraction]:
    return [value[i][j] for i, j in SYMMETRIC_INDICES]


def rank(rows: list[list[Fraction]]) -> int:
    work = [list(row) for row in rows if any(row)]
    if not work:
        return 0
    row_index = 0
    for column in range(len(work[0])):
        pivot = next((i for i in range(row_index, len(work)) if work[i][column]), None)
        if pivot is None:
            continue
        work[row_index], work[pivot] = work[pivot], work[row_index]
        scale = work[row_index][column]
        work[row_index] = [entry / scale for entry in work[row_index]]
        for i in range(len(work)):
            if i == row_index or not work[i][column]:
                continue
            factor = work[i][column]
            work[i] = [a - factor * b for a, b in zip(work[i], work[row_index])]
        row_index += 1
        if row_index == len(work):
            break
    return row_index


def nullspace(rows: list[list[Fraction]]) -> list[list[Fraction]]:
    work = [list(row) for row in rows]
    if not work:
        return []
    pivot_columns: list[int] = []
    row_index = 0
    for column in range(len(work[0])):
        pivot = next((i for i in range(row_index, len(work)) if work[i][column]), None)
        if pivot is None:
            continue
        work[row_index], work[pivot] = work[pivot], work[row_index]
        pivot_value = work[row_index][column]
        work[row_index] = [entry / pivot_value for entry in work[row_index]]
        for i in range(len(work)):
            if i == row_index or not work[i][column]:
                continue
            factor = work[i][column]
            work[i] = [a - factor * b for a, b in zip(work[i], work[row_index])]
        pivot_columns.append(column)
        row_index += 1
        if row_index == len(work):
            break
    free_columns = [column for column in range(len(work[0])) if column not in pivot_columns]
    basis: list[list[Fraction]] = []
    for free in free_columns:
        vector = [Fraction(0) for _ in range(len(work[0]))]
        vector[free] = Fraction(1)
        for i, pivot in enumerate(pivot_columns):
            vector[pivot] = -work[i][free]
        basis.append(vector)
    return basis


def boost(axis: int, sign: int) -> list[list[Fraction]]:
    result = identity(DIMENSION)
    c = Fraction(5, 3)
    s = sign * Fraction(4, 3)
    result[0][0] = c
    result[axis][axis] = c
    result[0][axis] = s
    result[axis][0] = s
    return result


def rotation(first: int, second: int, sign: int) -> list[list[Fraction]]:
    result = identity(DIMENSION)
    c = Fraction(3, 5)
    s = sign * Fraction(4, 5)
    result[first][first] = c
    result[second][second] = c
    result[first][second] = -s
    result[second][first] = s
    return result


def lorentz_orbit() -> tuple[list[list[Fraction]], list[int], int]:
    eta = diagonal(-1, 1, 1, 1)
    seed = diagonal(2, 2, 0, 0)
    generators = [identity(DIMENSION)]
    generators.extend(boost(axis, sign) for axis in range(1, 4) for sign in (1, -1))
    generators.extend(
        rotation(first, second, sign)
        for first, second in ((1, 2), (1, 3), (2, 3))
        for sign in (1, -1)
    )
    candidates = list(generators)
    candidates.extend(multiply(left, right) for left in generators for right in generators)
    transforms: list[list[list[Fraction]]] = []
    seen: set[tuple[Fraction, ...]] = set()
    for candidate in candidates:
        key = matrix_key(candidate)
        if key not in seen:
            seen.add(key)
            transforms.append(candidate)

    orbit: list[list[Fraction]] = []
    for transform in transforms:
        assert same(multiply(multiply(transpose(transform), eta), transform), eta)
        tangent = multiply(multiply(transpose(transform), seed), transform)
        assert sum(eta[i][i] * tangent[i][i] for i in range(DIMENSION)) == 0
        orbit.append(symmetric_vector(tangent))

    selected: list[list[Fraction]] = []
    selected_indices: list[int] = []
    for index, vector in enumerate(orbit):
        if rank(selected + [vector]) > rank(selected):
            selected.append(vector)
            selected_indices.append(index)
        if len(selected) == 9:
            break
    return orbit, selected_indices, len(generators)


def pair_row(tangent: list[Fraction]) -> list[Fraction]:
    return [weight * entry for weight, entry in zip(PAIRING_WEIGHTS, tangent)]


def proportional(left: list[Fraction], right: list[Fraction]) -> bool:
    ratio: Fraction | None = None
    for a, b in zip(left, right):
        if b == 0:
            if a != 0:
                return False
            continue
        candidate = a / b
        if ratio is None:
            ratio = candidate
        elif candidate != ratio:
            return False
    return ratio is not None


def derivative(profile: dict[int, tuple[Fraction, Fraction, Fraction]]) -> dict[int, tuple[Fraction, Fraction, Fraction]]:
    result: dict[int, tuple[Fraction, Fraction, Fraction]] = {}
    for power, coefficient in profile.items():
        if power:
            result[power - 1] = tuple(Fraction(power) * item for item in coefficient)
    return result


def scaled_shifted(
    profile: dict[int, tuple[Fraction, Fraction, Fraction]],
    factor: Fraction,
    shift: int,
) -> dict[int, tuple[Fraction, Fraction, Fraction]]:
    return {
        power + shift: tuple(factor * item for item in coefficient)
        for power, coefficient in profile.items()
    }


def add_profiles(*profiles: dict[int, tuple[Fraction, Fraction, Fraction]]) -> dict[int, tuple[Fraction, Fraction, Fraction]]:
    result: dict[int, tuple[Fraction, Fraction, Fraction]] = {}
    for profile in profiles:
        for power, coefficient in profile.items():
            previous = result.get(power, (Fraction(0), Fraction(0), Fraction(0)))
            value = tuple(a + b for a, b in zip(previous, coefficient))
            if any(value):
                result[power] = value
            elif power in result:
                del result[power]
    return result


def build_result() -> dict[str, object]:
    checks: list[str] = []
    eta = diagonal(-1, 1, 1, 1)
    eta_vector = symmetric_vector(eta)
    seed = diagonal(2, 2, 0, 0)
    seed_trace = sum(eta[i][i] * seed[i][i] for i in range(DIMENSION))
    assert seed_trace == 0
    assert seed == diagonal(2, 2, 0, 0)
    checks.append("full_reciprocal_tangent_seed_is_exact_and_metric_traceless")

    orbit, basis_indices, generator_count = lorentz_orbit()
    shape_rank = rank(orbit)
    generator_rank = rank(orbit[:generator_count])
    assert shape_rank == 9
    assert generator_rank == 8
    checks.extend(("all_plane_shape_rank_is_nine", "uncomposed_generator_control_rank_is_eight"))

    basis = [orbit[index] for index in basis_indices]
    assert rank(basis + [eta_vector]) == 10
    checks.append("common_scale_restores_tenth_direction")

    balance_rows = [pair_row(vector) for vector in orbit]
    annihilator = nullspace(balance_rows)
    assert rank(balance_rows) == 9
    assert len(annihilator) == 1
    assert proportional(annihilator[0], eta_vector)
    assert all(sum(a * b for a, b in zip(row, eta_vector)) == 0 for row in balance_rows)
    checks.extend((
        "balance_functionals_have_rank_nine",
        "annihilator_has_nullity_one",
        "annihilator_is_metric_trace_line",
        "metric_trace_line_annihilates_every_pair_tangent",
    ))

    ricci = [Fraction(i + 1, 7) for i in range(10)]
    scalar = -ricci[0] + ricci[4] + ricci[7] + ricci[9]
    for a in (Fraction(2, 3), Fraction(-5, 7)):
        for b in (Fraction(0), Fraction(3, 11)):
            response = [a * item + b * scalar * metric for item, metric in zip(ricci, eta_vector)]
            for tangent, row in zip(orbit[:25], balance_rows[:25]):
                left = sum(x * y for x, y in zip(row, response))
                right = a * sum(x * y for x, y in zip(row, ricci))
                assert left == right
    checks.append("metric_trace_coefficient_cancels_from_ddr_pairing")

    scalar_only_response = [scalar * item for item in eta_vector]
    assert all(sum(a * b for a, b in zip(row, scalar_only_response)) == 0 for row in balance_rows)
    checks.append("scalar_only_stratum_is_vacuous_and_requires_nonzero_ricci_gate")

    assert any(eta_vector)
    assert all(sum(a * b for a, b in zip(row, eta_vector)) == 0 for row in balance_rows)
    checks.append("ddr_does_not_imply_full_response_zero")

    # Exact primary reduction: f=1+b/r-R0*r^2/12 solves r^2 f''-2f+2=0.
    profile = {
        0: (Fraction(1), Fraction(0), Fraction(0)),
        -1: (Fraction(0), Fraction(1), Fraction(0)),
        2: (Fraction(0), Fraction(0), Fraction(-1, 12)),
    }
    second = derivative(derivative(profile))
    ode = add_profiles(
        scaled_shifted(second, Fraction(1), 2),
        scaled_shifted(profile, Fraction(-2), 0),
        {0: (Fraction(2), Fraction(0), Fraction(0))},
    )
    assert ode == {}
    checks.append("primary_tracefree_family_solves_exact_ode")

    # Exact round reduction after a=X*C, a'=S, a''=C/X and C^2-S^2=1.
    round_q_coefficients = {"C2": 1, "S2": -1, "constant": -1}
    round_q_coefficients["S2"] += round_q_coefficients.pop("C2")
    round_q_coefficients["constant"] += 1
    round_q_coefficients = {key: value for key, value in round_q_coefficients.items() if value}
    assert round_q_coefficients == {}
    checks.append("positive_round_cosh_family_solves_tracefree_residual")

    assert len(nullspace(balance_rows)) == 1
    checks.append("one_common_trace_datum_remains")

    return {
        "landing": LANDING,
        "premise_status": "DDR_IS_NEW_CANDIDATE_POSTULATE_NOT_DERIVED_OR_ADOPTED",
        "founding_chain_alone_selects_residual": False,
        "reciprocal_seed_metric_trace": str(seed_trace),
        "reciprocal_tangent_normalization": "H=2*(u_flat tensor u_flat+n_flat tensor n_flat)",
        "lorentz_orbit_count": len(orbit),
        "generator_only_rank": generator_rank,
        "reciprocal_shape_rank": shape_rank,
        "symmetric_metric_dimension": 10,
        "selected_exact_basis_indices": basis_indices,
        "balance_rank": rank(balance_rows),
        "annihilator_nullity": len(annihilator),
        "annihilator_basis": "span(g_ab)",
        "g301_response": "E_ab=a*Ric_ab+b*R*g_ab",
        "ddr_pairing": "<E,H>=a*<Ric,H> because <g,H>=0",
        "nondegenerate_gate": "a!=0",
        "conditional_selected_residual": "Ric_ab-(R/4)*g_ab=0",
        "connected_bianchi_datum": "dR=0; one scalar curvature constant remains",
        "primary_static_ode": "r^2*f''-2*f+2=0",
        "primary_static_family": "f=1+b/r-(R0/12)*r^2",
        "positive_round_residual": "a*a''-a'^2-1=0",
        "positive_round_family": "a(T)=X*cosh((T-T0)/X)",
        "scale_status": "not fixed by DDR",
        "production_checks": len(checks),
        "check_labels": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build_result()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
